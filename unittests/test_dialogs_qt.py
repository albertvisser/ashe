"""unittests for ./ashe/dialogs_qt.py
"""
import types
from ashe import dialogs_qt as testee
from mockgui import mockqtwidgets as mockqtw
from unittests.output_fixtures import expected_output

class MockEditorGui:
    """stub for gui_qt.EditorGui object
    """
    def __init__(self):
        self.appicon = "appicon"


class TestElementDialog:
    """unittest for dialogs_qt.ElementDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ElementDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ElementDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ElementDialog, '__init__', mock_init)
        testobj = testee.ElementDialog()
        assert capsys.readouterr().out == 'called ElementDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ElementDialog.__init__
        """
        def mock_flags(self):
            print('called TableItem.flags')
            return testee.core.Qt.ItemFlag.ItemIsEnabled | testee.core.Qt.ItemFlag.ItemIsEditable
        def mock_analyze(*args):
            print('called analyze_element with args', args)
            return 'qqq', False, 'xxx', 'yyy', True, False
        def mock_analyze_2(*args):
            print('called analyze_element with args', args)
            return 'qqq', True, 'xxx', 'yyy', False, True
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee, 'analyze_element', mock_analyze)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        monkeypatch.setattr(testee.qtw, 'QTableWidgetItem', mockqtw.MockTableItem)
        monkeypatch.setattr(testee.qtw.QTableWidgetItem, 'flags', mock_flags)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.ElementDialog(parent)
        assert testobj._parent == parent
        assert testobj.style_text == 'xxx'
        assert testobj.styledata == 'yyy'
        assert testobj.has_style
        assert not testobj.is_stylesheet
        assert not testobj.csseditor_called
        assert testobj.old_styledata == 'yyy'
        assert not testobj.is_style_tag
        assert not testobj.check_changes
        assert isinstance(testobj.tag_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.comment_button, testee.qtw.QCheckBox)
        assert isinstance(testobj.attr_table, testee.qtw.QTableWidget)
        assert isinstance(testobj.add_button, testee.qtw.QPushButton)
        assert isinstance(testobj.delete_button, testee.qtw.QPushButton)
        assert isinstance(testobj.style_button, testee.qtw.QPushButton)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        tag, attrs = '', None
        assert capsys.readouterr().out == expected_output['element_dialog'].format(testobj=testobj,
                                                                                   title='',
                                                                                   tag=f"'{tag}'",
                                                                                   attrs=attrs)
        monkeypatch.setattr(testee, 'analyze_element', mock_analyze_2)
        tag = 'aaa'
        attrs = {'bla': 'dibla', 'style': 'ccc', 'styledata': 'ddd'}
        testobj = testee.ElementDialog(parent, title='title', tag=tag, attrs=attrs)
        assert testobj.style_text == 'xxx'
        assert testobj.styledata == 'yyy'
        assert not testobj.has_style
        assert testobj.is_stylesheet
        assert not testobj.csseditor_called
        assert testobj.old_styledata == 'yyy'
        assert not testobj.is_style_tag
        assert not testobj.check_changes
        assert isinstance(testobj.tag_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.comment_button, testee.qtw.QCheckBox)
        assert isinstance(testobj.attr_table, testee.qtw.QTableWidget)
        assert isinstance(testobj.add_button, testee.qtw.QPushButton)
        assert isinstance(testobj.delete_button, testee.qtw.QPushButton)
        assert isinstance(testobj.style_button, testee.qtw.QPushButton)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['element_dialog2'].format(testobj=testobj,
                                                                                    title='title',
                                                                                    tag=f"'{tag}'",
                                                                                    attrs=attrs)

    def test_on_add(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_add
        """
        def mock_refresh():
            print('called ElementDialog.refresh')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh = mock_refresh
        testobj.attr_table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.on_add()
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called Table.setFocus\n"
                                           "called Table.rowCount\n"
                                           "called Table.insertRow with arg '0'\n"
                                           "called Table.setCurrentCell with args (0, 0)\n")

    def test_on_del(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_del
        """
        def mock_refresh():
            print('called ElementDialog.refresh')
        def mock_current():
            nonlocal counter
            print("called Table.currentRow")
            counter += 1
            return [None, 0, 2][counter - 1]
        def mock_item(x, y):
            nonlocal counter
            print(f"called Table.item with args ({x}, {y})")
            if counter < 3:
                result = mockqtw.MockTableItem('xxx')
            else:
                result = mockqtw.MockTableItem('style')
            return result
        def mock_info(self, *args):
            print("called MessageBox.information with args", args)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh = mock_refresh
        testobj.attr_table = mockqtw.MockTable()
        testobj.attr_table.currentRow = mock_current
        testobj.attr_table.item = mock_item
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.has_style = True
        counter = 0
        testobj.on_del()
        assert testobj.has_style
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called Table.currentRow\n"
                "called MessageBox.information with args"
                " ('Delete attribute', 'press Enter on this item first')\n")
        testobj.on_del()
        assert testobj.has_style
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called Table.currentRow\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called TableItem.__init__ with arg xxx\n"
                                           "called Table.removeRow with arg '0'\n")
        testobj.on_del()
        assert not testobj.has_style
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called Table.currentRow\n"
                                           "called Table.item with args (2, 0)\n"
                                           "called TableItem.__init__ with arg style\n"
                                           "called Table.removeRow with arg '2'\n")

    def test_on_style(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_style
        """
        def mock_refresh():
            print('called ElementDialog.refresh')
        def mock_call_1(arg):
            print(f"called CssManager.call_editor_for_stylesheet with arg '{arg}'")
        def mock_call_2(*args):
            print('called CssManager.call_editor with args', args)
        def mock_find(*args):
            print('called Table.findItems with args', args)
            return ['item1', 'item2', 'item3']
        def mock_col(item):
            print(f"called Table.column with arg '{item}'")
            if item == 'item1':
                return 0
            if item == 'item2':
                return 1
            if item == 'item3':
                return 0
        def mock_row(item):
            print(f"called Table.row with arg '{item}'")
            if item == 'item1':
                return 1
            if item == 'item2':
                return 2
            if item == 'item3':
                return 3
        def mock_item(x, y):
            print(f"called Table.item with args {x}, {y}")
            return types.SimpleNamespace(text=lambda: f'item{x}_{y}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh = mock_refresh
        testobj.is_stylesheet = True
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(
            cssm=types.SimpleNamespace(call_editor_for_stylesheet=mock_call_1,
                                       call_editor=mock_call_2)))
        testobj.style_button = mockqtw.MockPushButton()
        testobj.style_text = 'xxx'
        testobj.tag_text = mockqtw.MockLabel('yyy')
        testobj.attr_table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called Label.__init__ with args ('yyy',)\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.check_changes = True
        testobj.on_style()
        assert not testobj.check_changes
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called PushButton.setText with arg `xxx`\n")
        # testobj.check_changes = False
        testobj.on_style()
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                "called PushButton.setText with arg `Chec&k Changes`\n"
                "called Table.findItems with args"
                f" ('href', {testee.core.Qt.MatchFlag.MatchFixedString!r})\n"
                f"called CssManager.call_editor_for_stylesheet with arg ''\n"
                "called ElementDialog.refresh\n")

        testobj.attr_table.column = mock_col
        testobj.attr_table.row = mock_row
        testobj.attr_table.item = mock_item
        testobj.check_changes = False
        testobj.attr_table.findItems = mock_find
        # breakpoint()
        testobj.on_style()
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                "called PushButton.setText with arg `Chec&k Changes`\n"
                "called Table.findItems with args"
                f" ('href', {testee.core.Qt.MatchFlag.MatchFixedString!r})\n"
                "called Table.column with arg 'item1'\n"
                "called Table.row with arg 'item1'\n"
                "called Table.item with args 1, 1\n"
                "called Table.column with arg 'item2'\n"
                "called Table.row with arg 'item2'\n"
                "called Table.column with arg 'item3'\n"
                "called Table.row with arg 'item3'\n"
                "called Table.item with args 3, 1\n"
                f"called CssManager.call_editor_for_stylesheet with arg 'item3_1'\n"
                "called ElementDialog.refresh\n")

        testobj.is_stylesheet = False
        testobj.on_style()
        assert testobj.check_changes
        assert capsys.readouterr().out == (
                "called PushButton.setText with arg `Chec&k Changes`\n"
                "called Table.findItems with args"
                f" ('href', {testee.core.Qt.MatchFlag.MatchFixedString!r})\n"
                "called Table.column with arg 'item1'\n"
                "called Table.row with arg 'item1'\n"
                "called Table.item with args 1, 1\n"
                "called Table.column with arg 'item2'\n"
                "called Table.row with arg 'item2'\n"
                "called Table.column with arg 'item3'\n"
                "called Table.row with arg 'item3'\n"
                "called Table.item with args 3, 1\n"
                f"called CssManager.call_editor with args ({testobj}, 'yyy')\n")

    def test_refresh(self, monkeypatch, capsys):
        """unittest for ElementDialog.refresh
        """
        def mock_analyze(*args):
            print('called analyze_element with args', args)
            return 'qqq', False, 'xxx', 'yyy', True, False
        monkeypatch.setattr(testee, 'analyze_element', mock_analyze)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.has_style = False
        testobj.styledata = 'styledata'
        testobj.style_button = mockqtw.MockPushButton()
        testobj.tag_text = mockqtw.MockLabel('link')
        testobj.attr_table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called Label.__init__ with args ('link',)\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.refresh()
        assert not testobj.has_style
        assert capsys.readouterr().out == ""
        testobj.tag_text.setText('style')
        testobj.refresh()
        assert testobj.is_style_tag
        assert not testobj.has_style
        assert capsys.readouterr().out == (
                "called Label.setText with arg `style`\n"
                "called Table.rowCount\n"
                "called Table.rowCount\n"
                "called Table.insertRow with arg '0'\n"
                "called Table.setItem with args"
                " (0, 0, item of <class 'PyQt6.QtWidgets.QTableWidgetItem'>)\n"
                "called Table.setItem with args"
                " (0, 1, item of <class 'PyQt6.QtWidgets.QTableWidgetItem'>)\n"
                "called analyze_element with args ('', {'styledata': ''})\n"
                "called PushButton.setText with arg `xxx`\n")
        assert testobj.attr_table.item(0, 0).text() == 'styledata'
        assert testobj.attr_table.item(0, 1).text() == testobj.styledata
        assert capsys.readouterr().out == ("called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n")

        testobj.attr_table.setRowCount(2)
        testobj.attr_table.setColumnCount(2)
        testobj.attr_table.setItem(0, 0, mockqtw.MockTableItem())
        testobj.attr_table.setItem(0, 0, mockqtw.MockTableItem())
        testobj.attr_table.setItem(1, 0, mockqtw.MockTableItem('styledata'))
        testobj.attr_table.setItem(1, 1, mockqtw.MockTableItem())
        assert capsys.readouterr().out == (
                "called Table.setRowCount with arg '2'\n"
                "called Table.setColumnCount with arg '2'\n"
                "called TableItem.__init__ with arg xy\n"
                "called Table.setItem with args"
                " (0, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg xy\n"
                "called Table.setItem with args"
                " (0, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg styledata\n"
                "called Table.setItem with args"
                " (1, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg xy\n"
                "called Table.setItem with args"
                " (1, 1, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n")
        testobj.refresh()
        assert testobj.is_style_tag
        assert not testobj.has_style
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (1, 0)\n"
                                           "called Table.item with args (1, 1)\n"
                                           "called TableItem.settext with arg styledata\n")

        testobj.tag_text.setText(' not style')
        testobj.attr_table.setItem(1, 0, mockqtw.MockTableItem('style'))
        assert capsys.readouterr().out == (
                "called Label.setText with arg ` not style`\n"
                "called TableItem.__init__ with arg style\n"
                "called Table.setItem with args"
                " (1, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n")
        testobj.refresh()
        assert not testobj.is_style_tag
        assert testobj.has_style
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (1, 0)\n"
                                           "called Table.item with args (1, 1)\n"
                                           "called TableItem.settext with arg styledata\n")

    def test_reject(self, monkeypatch, capsys):
        """unittest for ElementDialog.reject
        """
        def mock_refresh():
            print('called ElementDialog.refresh')
        def mock_info(self, *args):
            print("called MessageBox.information with args", args)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh = mock_refresh
        testobj.styledata = testobj.old_styledata = 'xxx'
        testobj.reject()
        assert capsys.readouterr().out == "called Dialog.reject\n"
        testobj.styledata = 'yyy'
        testobj.reject()
        assert capsys.readouterr().out == ("called MessageBox.information with args"
                                           " ('Let op', 'bijbehorende style data is gewijzigd')\n"
                                           "called ElementDialog.refresh\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for ElementDialog.accept
        """
        def mock_refresh():
            print('called ElementDialog.refresh')
        def mock_rows():
            print('called Table.rowCount')
            return 0
        def mock_rows_1():
            print('called Table.rowCount')
            return 1
        def mock_rows_2():
            print('called Table.rowCount')
            return 2
        def mock_item(x, y):
            print(f"called Table.item with args ({x}, {y})")
            if y == 0:
                return listitem1
            return listitem2
        def mock_item2(x, y):
            print(f"called Table.item with args ({x}, {y})")
            return None
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information',
                            mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(dialog_data=())
        testobj.refresh = mock_refresh
        testobj.tag_text = mockqtw.MockLineEdit('hello world')
        testobj.comment_button = mockqtw.MockCheckBox()
        testobj.attr_table = mockqtw.MockTable()
        testobj.attr_table.rowCount = mock_rows
        testobj.attr_table.item = mock_item
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.is_style_tag = False
        testobj.has_style = False
        testobj.styledata = 'styledata'
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called LineEdit.text\n"
                "called MessageBox.information with args"
                f" `{testobj}` `Add an element` `Illegal character(s) in tag name`\n")
        # 202-221
        testobj.tag_text.setText('element')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `element`\n"
        testobj.has_style = True
        testobj.accept()
        assert testobj._parent.dialog_data == ('element', {'style': 'styledata'}, False)
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called Table.rowCount\n"
                                           "called Dialog.accept\n")
        testobj.is_style_tag = True
        testobj.accept()
        assert testobj._parent.dialog_data == ('element', {'styledata': 'styledata'}, False)
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called Table.rowCount\n"
                                           "called Dialog.accept\n")
        # 205-215
        testobj.is_style_tag = False
        testobj.has_style = False
        testobj.attr_table.rowCount = mock_rows_1
        listitem1 = mockqtw.MockListItem('xxx')
        listitem2 = mockqtw.MockListItem('yyy')
        assert capsys.readouterr().out == ("called ListItem.__init__\n"
                                           "called ListItem.__init__\n")
        testobj.accept()
        assert testobj._parent.dialog_data == ('element', {'xxx': 'yyy'}, False)
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n"
                                           "called Dialog.accept\n")
        listitem1 = mockqtw.MockListItem('style')
        listitem2 = mockqtw.MockListItem('yyy')
        assert capsys.readouterr().out == ("called ListItem.__init__\n"
                                           "called ListItem.__init__\n")
        testobj.accept()
        assert testobj._parent.dialog_data == ('element', {}, False)
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n"
                                           "called Dialog.accept\n")
        listitem1 = mockqtw.MockListItem('styledata')
        listitem2 = mockqtw.MockListItem('yyy')
        assert capsys.readouterr().out == ("called ListItem.__init__\n"
                                           "called ListItem.__init__\n")
        testobj.accept()
        assert testobj._parent.dialog_data == ('element', {}, False)
        assert capsys.readouterr().out == ("called ElementDialog.refresh\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n"
                                           "called Dialog.accept\n")
        # 208-210, 212-213
        testobj.attr_table.rowCount = mock_rows_2
        listitem1 = mockqtw.MockListItem('xxx')
        listitem2 = mockqtw.MockListItem('yyy')
        assert capsys.readouterr().out == ("called ListItem.__init__\n"
                                           "called ListItem.__init__\n")
        testobj.accept()
        assert testobj._parent.dialog_data == ('element', {}, False)
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called Table.rowCount\n"
                "called Table.item with args (0, 0)\n"
                "called Table.item with args (0, 1)\n"
                "called Table.item with args (1, 0)\n"
                "called Table.item with args (1, 1)\n"
                "called MessageBox.information with args"
                f" `{testobj}` `Add an element` `Duplicate attributes, please merge`\n")
        # 208-210
        testobj.attr_table.item = mock_item2
        testobj.comment_button.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        testobj.accept()
        assert testobj._parent.dialog_data == ('element', {}, False)
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called Table.rowCount\n"
                "called Table.item with args (0, 0)\n"
                "called MessageBox.information with args"
                f" `{testobj}` `Add an element` `Press enter on this item first`\n")


class TestTextDialog:
    """unittest for dialogs_qt.TextDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.TextDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__ with args', args)
        monkeypatch.setattr(testee.TextDialog, '__init__', mock_init)
        testobj = testee.TextDialog()
        assert capsys.readouterr().out == 'called TextDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for TextDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.ElementDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.ElementDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.TextDialog(parent, show_commented=False)
        assert testobj._parent == parent
        assert not testobj.show_commented
        assert isinstance(testobj.data_text, testee.qtw.QTextEdit)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['text_dialog'].format(testobj=testobj,
                                                                                title='',
                                                                                text=None)
        testobj = testee.TextDialog(parent)
        assert testobj._parent == parent
        assert testobj.show_commented
        assert isinstance(testobj.comment_button, testee.qtw.QCheckBox)
        assert isinstance(testobj.data_text, testee.qtw.QTextEdit)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['text_dialog3'].format(testobj=testobj,
                                                                                title='',
                                                                                text='')
        testobj = testee.TextDialog(parent, text=f'{testee.CMSTART}')
        assert testobj._parent == parent
        assert testobj.show_commented
        assert isinstance(testobj.comment_button, testee.qtw.QCheckBox)
        assert isinstance(testobj.data_text, testee.qtw.QTextEdit)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['text_dialog2'].format(testobj=testobj,
                                                                                title='',
                                                                                text='')
        testobj = testee.TextDialog(parent, text=f'{testee.CMSTART} xxx')
        assert testobj._parent == parent
        assert testobj.show_commented
        assert isinstance(testobj.comment_button, testee.qtw.QCheckBox)
        assert isinstance(testobj.data_text, testee.qtw.QTextEdit)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['text_dialog2'].format(testobj=testobj,
                                                                                title='',
                                                                                text='xxx')
        testobj = testee.TextDialog(parent, 'title', 'text')
        assert testobj._parent == parent
        assert testobj.show_commented
        assert isinstance(testobj.comment_button, testee.qtw.QCheckBox)
        assert isinstance(testobj.data_text, testee.qtw.QTextEdit)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['text_dialog3'].format(testobj=testobj,
                                                                                title='title',
                                                                                text='text')

    def test_accept(self, monkeypatch, capsys):
        """unittest for TextDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace()
        testobj.show_commented = False
        testobj.data_text = mockqtw.MockEditorWidget('xxx')
        testobj.comment_button = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called Editor.__init__ with args ('xxx',)\n"
                                           "called CheckBox.__init__\n")
        testobj.accept()
        assert testobj._parent.dialog_data == ('xxx', False)
        assert capsys.readouterr().out == ("called Editor.toPlainText\n"
                                           "called Dialog.accept\n")
        testobj.show_commented = True
        testobj.accept()
        assert testobj._parent.dialog_data == ('xxx', False)
        assert capsys.readouterr().out == ("called CheckBox.checkState\n"
                                           "called Editor.toPlainText\n"
                                           "called Dialog.accept\n")
        testobj.comment_button.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        testobj.accept()
        assert testobj._parent.dialog_data == ('xxx', True)
        assert capsys.readouterr().out == ("called CheckBox.checkState\n"
                                           "called Editor.toPlainText\n"
                                           "called Dialog.accept\n")


class TestSearchDialog:
    """unittest for dialogs_qt.SearchDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.SearchDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SearchDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SearchDialog, '__init__', mock_init)
        testobj = testee.SearchDialog()
        assert capsys.readouterr().out == 'called SearchDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SearchDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.SearchDialog, 'set_search', lambda *x: True)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        parent.editor = types.SimpleNamespace(srchhlp=types.SimpleNamespace(search_args=()))
        testobj = testee.SearchDialog(parent)
        assert testobj._parent == parent
        assert not testobj.replace
        assert isinstance(testobj.txt_element, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_name, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_val, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.lbl_search, testee.qtw.QLabel)
        assert isinstance(testobj.btn_ok, testee.qtw.QPushButton)
        assert isinstance(testobj.btn_cancel, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['search_dialog'].format(testobj=testobj,
                                                                                  title='')

        parent.editor.srchhlp.search_args = ('a', 'b', 'c', 'd')
        parent.editor.srchhlp.replace_args = ()
        testobj = testee.SearchDialog(parent, 'title', replace=True)
        assert testobj._parent == parent
        assert testobj.replace
        assert isinstance(testobj.txt_element, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_name, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_val, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_element_replace, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_name_replace, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_val_replace, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_text_replace, testee.qtw.QLineEdit)
        assert isinstance(testobj.cb_replace_all, testee.qtw.QCheckBox)
        assert isinstance(testobj.lbl_search, testee.qtw.QLabel)
        assert isinstance(testobj.btn_ok, testee.qtw.QPushButton)
        assert isinstance(testobj.btn_cancel, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['search_dialog2'].format(testobj=testobj,
                                                                                   title='title')

        parent.editor.srchhlp.search_args = ('a', 'b', 'c', 'd')
        parent.editor.srchhlp.replace_args = ('aa', 'bb', 'cc', 'dd')
        testobj = testee.SearchDialog(parent, 'title', replace=True)
        assert testobj._parent == parent
        assert testobj.replace
        assert isinstance(testobj.txt_element, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_name, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_val, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_element_replace, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_name_replace, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_attr_val_replace, testee.qtw.QLineEdit)
        assert isinstance(testobj.txt_text_replace, testee.qtw.QLineEdit)
        assert isinstance(testobj.cb_replace_all, testee.qtw.QCheckBox)
        assert isinstance(testobj.lbl_search, testee.qtw.QLabel)
        assert isinstance(testobj.btn_ok, testee.qtw.QPushButton)
        assert isinstance(testobj.btn_cancel, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['search_dialog3'].format(testobj=testobj,
                                                                                   title='title')

    def test_set_search(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_search
        """
        def mock_build(*args):
            print('called Editor.build_search_spec with args', args)
            return 'search specs'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace = False
        testobj._parent = types.SimpleNamespace(
                editor=types.SimpleNamespace(build_search_spec=mock_build))
        testobj.txt_element = mockqtw.MockLineEdit('x')
        testobj.txt_attr_name = mockqtw.MockLineEdit('y')
        testobj.txt_attr_val = mockqtw.MockLineEdit('z')
        testobj.txt_text = mockqtw.MockLineEdit('q')
        testobj.txt_element_replace = mockqtw.MockLineEdit('a')
        testobj.txt_attr_name_replace = mockqtw.MockLineEdit('b')
        testobj.txt_attr_val_replace = mockqtw.MockLineEdit('c')
        testobj.txt_text_replace = mockqtw.MockLineEdit('d')
        testobj.lbl_search = mockqtw.MockLabel()
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called Label.__init__\n")
        testobj.set_search()
        assert testobj.search_specs == 'search specs'
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called Editor.build_search_spec with args ('x', 'y', 'z', 'q', ())\n"
                "called Label.setText with arg `search specs`\n")
        testobj.replace = True
        testobj.set_search()
        assert testobj.search_specs == 'search specs'
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Editor.build_search_spec with args"
                                           " ('x', 'y', 'z', 'q', ('a', 'b', 'c', 'd'))\n"
                                           "called Label.setText with arg `search specs`\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SearchDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information',
                            mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace = False
        testobj.search_specs = 'search specs'
        testobj._parent = types.SimpleNamespace(dialog_data=(),
                                                editor=types.SimpleNamespace(title='title'))
        testobj.txt_element = mockqtw.MockLineEdit('')
        testobj.txt_attr_name = mockqtw.MockLineEdit('')
        testobj.txt_attr_val = mockqtw.MockLineEdit('')
        testobj.txt_text = mockqtw.MockLineEdit('')
        testobj.txt_element_replace = mockqtw.MockLineEdit('')
        testobj.txt_attr_name_replace = mockqtw.MockLineEdit('')
        testobj.txt_attr_val_replace = mockqtw.MockLineEdit('')
        testobj.txt_text_replace = mockqtw.MockLineEdit('')
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n")
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `Please enter search criteria or press cancel`\n"
                "called LineEdit.setFocus\n")

        testobj.txt_element.setText('xxx')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `xxx`\n"
        testobj.accept()
        assert testobj._parent.dialog_data == (('xxx', '', '', ''), 'search specs', ())
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Dialog.accept\n")

        testobj._parent.dialog_data = ()
        testobj.txt_attr_name.setText('yyy')
        testobj.txt_attr_val.setText('zzz')
        testobj.txt_text.setText('qqq')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `yyy`\n"
                                           "called LineEdit.setText with arg `zzz`\n"
                                           "called LineEdit.setText with arg `qqq`\n")
        testobj.replace = True
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `Please enter replacement criteria or press cancel`\n"
                "called LineEdit.setFocus\n")

        testobj.txt_element_replace.setText('aaa')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `aaa`\n"
        # testobj.txt_attr_name_replace.setText('bbb')
        # testobj.txt_attr_val_replace.setText('ccc')
        # testobj.txt_text_replace.setText('ddd')
        testobj.accept()
        assert testobj._parent.dialog_data == (('xxx', 'yyy', 'zzz', 'qqq'), 'search specs',
                                               ('aaa', '', '', ''))
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Dialog.accept\n")


class TestDtdDialog:
    """unittest for dialogs_qt.DtdDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.DtdDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called DtdDialog.__init__ with args', args)
        monkeypatch.setattr(testee.DtdDialog, '__init__', mock_init)
        testobj = testee.DtdDialog()
        assert capsys.readouterr().out == 'called DtdDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for DtdDialog.__init__
        """
        parent = MockEditorGui()
        parent.editor = types.SimpleNamespace(dtdlist=[('xxx', 'yyy'), ('', ''), ('HTML 5', 'zzzz')])
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.DtdDialog(parent)
        assert len(testobj.dtd_list) == 2
        assert [(x[0], x[1]) for x in testobj.dtd_list] == [('xxx', 'yyy'), ('HTML 5', 'zzzz')]
        assert isinstance(testobj.dtd_list[0][2], testee.qtw.QRadioButton)
        assert isinstance(testobj.dtd_list[1][2], testee.qtw.QRadioButton)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['dtd_dialog'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for DtdDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        rb = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == 'called RadioButton.__init__ with args () {}\n'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(dialog_data='')
        testobj.dtd_list = [('xx', 'XXXX', None)]
        testobj.accept()
        assert testobj._parent.dialog_data == ''
        assert capsys.readouterr().out == ("called Dialog.accept\n")
        testobj.dtd_list = [('xx', 'XXXX', rb)]
        testobj.accept()
        assert testobj._parent.dialog_data == ''
        assert capsys.readouterr().out == ("called RadioButton.isChecked\n"
                                           "called Dialog.accept\n")
        rb.setChecked(True)
        assert capsys.readouterr().out == 'called RadioButton.setChecked with arg `True`\n'
        testobj.accept()
        assert testobj._parent.dialog_data == 'XXXX'
        assert capsys.readouterr().out == ("called RadioButton.isChecked\n"
                                           "called Dialog.accept\n")


class TestCssDialog:
    """unittest for dialogs_qt.CssDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.CssDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CssDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CssDialog, '__init__', mock_init)
        testobj = testee.CssDialog()
        assert capsys.readouterr().out == 'called CssDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for CssDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.CssDialog(parent)
        assert testobj._parent == parent
        assert testobj.styledata == ''
        assert testobj.cssfilename == ''
        assert isinstance(testobj.link_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.new_button, testee.qtw.QPushButton)
        assert isinstance(testobj.choose_button, testee.qtw.QPushButton)
        assert isinstance(testobj.edit_button, testee.qtw.QPushButton)
        assert isinstance(testobj.text_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.inline_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['css_dialog'].format(testobj=testobj)

    def test_kies(self, monkeypatch, capsys):
        """unittest for CssDialog.kies
        """
        def mock_select():
            print('called CssDialog.select_file')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_file = mock_select
        testobj.kies()
        assert capsys.readouterr().out == ("called CssDialog.select_file\n")

    def test_nieuw(self, monkeypatch, capsys):
        """unittest for CssDialog.nieuw
        """
        def mock_select(**kwargs):
            print('called CssDialog.select_file with args', kwargs)
        def mock_select_2(**kwargs):
            print('called CssDialog.select_file with args', kwargs)
            return 'xxx'
        def mock_call(*args, **kwargs):
            print('called CssManager.call_editor_for_stylesheet with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_file = mock_select
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(
            cssm=types.SimpleNamespace(call_editor_for_stylesheet=mock_call)))
        testobj.nieuw('evt')
        assert capsys.readouterr().out == (
                "called CssDialog.select_file with args {'create': True}\n")
        testobj.select_file = mock_select_2
        testobj.nieuw('evt')
        assert capsys.readouterr().out == (
                "called CssDialog.select_file with args {'create': True}\n"
                "called CssManager.call_editor_for_stylesheet with args ('xxx',) {'new_ok': True}\n")

    def test_edit(self, monkeypatch, capsys):
        """unittest for CssDialog.edit
        """
        def mock_select():
            print('called CssDialog.select_file')
        def mock_select_2():
            print('called CssDialog.select_file')
            return 'xxx'
        def mock_call(*args):
            print('called CssManager.call_editor_for_stylesheet with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_file = mock_select
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(
            cssm=types.SimpleNamespace(call_editor_for_stylesheet=mock_call)))
        testobj.edit('evt')
        assert capsys.readouterr().out == (
                "called CssDialog.select_file\n")
        testobj.select_file = mock_select_2
        testobj.edit('evt')
        assert capsys.readouterr().out == (
                "called CssDialog.select_file\n"
                "called CssManager.call_editor_for_stylesheet with args ('xxx',)\n")

    def test_select_file(self, monkeypatch, capsys):
        """unittest for CssDialog.select_file
        """
        def mock_build(arg):
            print(f"called EditorGui.build_mask with arg '{arg}'")
            return arg
        def mock_text():
            print('called LineEdit.text')
            return ''
        def mock_text_2():
            print('called LineEdit.text')
            return 'http-and-more'
        def mock_text_3():
            print('called LineEdit.text')
            return 'http://xxxx'
        def mock_text_4():
            print('called LineEdit.text')
            return 'yyyy/zzz'
        def mock_open(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
            return 'xxx', True
        def mock_save(parent, *args, **kwargs):
            print('called FileDialog.getSaveFileName with args', parent, args, kwargs)
            return 'yyy', True
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(xmlfn='xxx'))
        testobj._parent.build_mask = mock_build
        testobj.link_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.link_text.text = mock_text
        assert testobj.select_file() == ""
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called EditorGui.build_mask with arg 'css'\n"
                "called FileDialog.getOpenFileName with args"
                f" {testobj} ('Choose a file', '{testee.os.getcwd()}', 'css') {{}}\n")

        testobj.link_text.text = mock_text_2
        assert testobj.select_file() == ""
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called EditorGui.build_mask with arg 'css'\n"
                "called FileDialog.getOpenFileName with args"
                f" {testobj} ('Choose a file', 'http-and-more', 'css') {{}}\n")

        testobj.link_text.text = mock_text_3
        assert testobj.select_file(True) == ""
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called EditorGui.build_mask with arg 'css'\n"
                "called FileDialog.getSaveFileName with args"
                f" {testobj} ('Choose a file', '{testee.os.getcwd()}', 'css') {{}}\n")

        monkeypatch.setattr(testee.qtw.QFileDialog, 'getSaveFileName', mock_save)
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_open)
        testobj._parent.editor.xmlfn = 'qqq/rrr'
        assert testobj.select_file() == "xxx"
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called EditorGui.build_mask with arg 'css'\n"
                "called FileDialog.getOpenFileName with args"
                f" {testobj} ('Choose a file', 'qqq', 'css') {{}}\n"
                "called LineEdit.setText with arg `xxx`\n")

        testobj.link_text.text = mock_text_4
        assert testobj.select_file(True) == "yyy"
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called EditorGui.build_mask with arg 'css'\n"
                "called FileDialog.getSaveFileName with args"
                f" {testobj} ('Choose a file', 'yyyy/zzz', 'css') {{}}\n"
                "called LineEdit.setText with arg `yyy`\n")

    def test_on_inline(self, monkeypatch, capsys):
        """unittest for CssDialog.on_inline
        """
        def mock_call(*args, **kwargs):
            print('called CssManager.call_from_inline with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(
            cssm=types.SimpleNamespace(call_from_inline=mock_call)))
        testobj.link_text = mockqtw.MockLineEdit()
        testobj.new_button = mockqtw.MockPushButton()
        testobj.edit_button = mockqtw.MockPushButton()
        testobj.choose_button = mockqtw.MockPushButton()
        testobj.inline_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.on_inline()
        assert capsys.readouterr().out == (
                f"called CssManager.call_from_inline with args ({testobj}, '') {{}}\n"
                "called LineEdit.setDisabled with arg True\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n"
                "called PushButton.setDisabled with arg `True`\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for CssDialog.accept
        """
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            return 'xxx'
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Not a valid link')
        def mock_meld(message):
            print(f"called EditorGui.meld with arg '{message}'")
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(meld=mock_meld, editor=types.SimpleNamespace(
            xmlfn='qqq', convert_link=mock_convert))
        testobj.link_text = mockqtw.MockLineEdit()
        testobj.text_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n")
        testobj.styledata = 'xxx'
        testobj.accept()
        assert testobj._parent.dialog_data == {'cssdata': 'xxx'}
        assert capsys.readouterr().out == "called Dialog.accept\n"

        testobj._parent.dialog_data = {}
        testobj.styledata = ''
        testobj.cssfilename = ''
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called EditorGui.meld with arg"
                " 'bestandsnaam opgeven of inline stylesheet definiëren s.v.p'\n")

        testobj.cssfilename = 'http://'
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == (
                "called LineEdit.setText with arg `http://`\n"
                "called LineEdit.text\n"
                "called EditorGui.meld with arg"
                " 'bestandsnaam opgeven of inline stylesheet definiëren s.v.p'\n")

        testobj.cssfilename = 'http://qqq/rrr'
        testobj.accept()
        assert testobj._parent.dialog_data == {'href': 'xxx', 'rel': 'stylesheet',
                                               'type': 'text/css'}
        assert capsys.readouterr().out == (
                "called LineEdit.setText with arg `http://qqq/rrr`\n"
                "called LineEdit.text\n"
                "called Editor.convert_link with args ('http://qqq/rrr', 'qqq')\n"
                "called LineEdit.text\n"
                "called Dialog.accept\n")

        testobj.text_text.setText('abcdef')
        testobj.accept()
        assert testobj._parent.dialog_data == {'href': 'xxx', 'rel': 'stylesheet',
                                               'type': 'text/css', 'media': 'abcdef'}
        assert capsys.readouterr().out == (
                "called LineEdit.setText with arg `abcdef`\n"
                "called LineEdit.setText with arg `http://qqq/rrr`\n"
                "called LineEdit.text\n"
                "called Editor.convert_link with args ('http://qqq/rrr', 'qqq')\n"
                "called LineEdit.text\n"
                "called Dialog.accept\n")

        testobj._parent.editor.convert_link = mock_convert_2
        testobj._parent.dialog_data = {}
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == (
                "called LineEdit.setText with arg `http://qqq/rrr`\n"
                "called LineEdit.text\n"
                "called Editor.convert_link with args ('http://qqq/rrr', 'qqq')\n"
                "called EditorGui.meld with arg 'Not a valid link'\n")


class TestLinkDialog:
    """unittest for dialogs_qt.LinkDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.LinkDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LinkDialog.__init__ with args', args)
        monkeypatch.setattr(testee.LinkDialog, '__init__', mock_init)
        testobj = testee.LinkDialog()
        assert capsys.readouterr().out == 'called LinkDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for LinkDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.LinkDialog(parent)
        assert testobj._parent == parent
        assert testobj.linktxt == ''
        assert isinstance(testobj.link_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.choose_button, testee.qtw.QPushButton)
        assert isinstance(testobj.title_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.text_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output["link_dialog"].format(testobj=testobj)

    def test_kies(self, monkeypatch, capsys):
        """unittest for LinkDialog.kies
        """
        def mock_get(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
            return 'qqq', True
        def mock_build(arg):
            print(f"called EditorGui.build mask with arg '{arg}'")
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.link_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(xmlfn=''))
        testobj._parent.build_mask = mock_build
        testobj.kies()
        assert capsys.readouterr().out == (
                "called EditorGui.build mask with arg 'html'\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                f" ('Choose a file', '{testee.os.getcwd()}', None) {{}}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get)
        testobj._parent.editor.xmlfn = 'xxx'
        testobj.kies()
        assert capsys.readouterr().out == (
                "called EditorGui.build mask with arg 'html'\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                " ('Choose a file', 'xxx', None) {}\n"
                "called LineEdit.setText with arg `qqq`\n")

    def test_set_ltext(self, monkeypatch, capsys):
        """unittest for LinkDialog.set_ltext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.title_text = mockqtw.MockLineEdit('qqq')
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.linktxt = 'link text'
        testobj.set_ltext('chgtext')
        assert testobj.linktxt == 'link text'
        assert capsys.readouterr().out == "called LineEdit.text\n"
        testobj.linktxt = 'qqq'
        testobj.set_ltext('chgtext')
        assert testobj.linktxt == 'chgtext'
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.setText with arg `chgtext`\n")

    def test_set_ttext(self, monkeypatch, capsys):
        """unittest for LinkDialog.set_ttext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.linktxt = 'link text'
        testobj.set_ttext('chgtext')
        assert testobj.linktxt == 'link text'
        testobj.set_ttext('')
        assert testobj.linktxt == ''

    def test_accept(self, monkeypatch, capsys):
        """unittest for LinkDialog.accept
        """
        def mock_question(parent, *args, **kwargs):
            print('called MessageBox.question with args', args[:2])
            return testee.qtw.QMessageBox.StandardButton.No
        def mock_question_2(parent, *args, **kwargs):
            print('called MessageBox.question with args', args[:2])
            return testee.qtw.QMessageBox.StandardButton.Yes
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            return 'xxx'
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Not a valid link')
        def mock_meld(message):
            print(f"called EditorGui.meld with arg '{message}'")
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(meld=mock_meld, editor=types.SimpleNamespace(
            xmlfn='qqq', convert_link=mock_convert))
        testobj.link_text = mockqtw.MockLineEdit('link')
        testobj.text_text = mockqtw.MockLineEdit()
        testobj.title_text = mockqtw.MockLineEdit('title')
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\n")
        testobj._parent.dialog_data = ()
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called MessageBox.question with args"
                                           " ('Add Link', 'Link text is empty - are you sure?')\n")
        monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question_2)
        testobj.accept()
        assert testobj._parent.dialog_data == ['', {'href': 'xxx', 'title': 'title'}]
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called MessageBox.question with args"
                                           " ('Add Link', 'Link text is empty - are you sure?')\n"
                                           "called LineEdit.text\n"
                                           "called Editor.convert_link with args ('link', 'qqq')\n"
                                           "called LineEdit.text\n"
                                           "called Dialog.accept\n")

        testobj._parent.dialog_data = ()
        testobj.text_text.setText('text')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `text`\n"
        testobj.accept()
        assert testobj._parent.dialog_data == ['text', {'href': 'xxx', 'title': 'title'}]
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Editor.convert_link with args ('link', 'qqq')\n"
                                           "called LineEdit.text\n"
                                           "called Dialog.accept\n")

        testobj._parent.dialog_data = ()
        testobj._parent.editor.convert_link = mock_convert_2
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Editor.convert_link with args ('link', 'qqq')\n"
                                           "called EditorGui.meld with arg 'Not a valid link'\n")


class TestImageDialog:
    """unittest for dialogs_qt.ImageDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ImageDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ImageDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ImageDialog, '__init__', mock_init)
        testobj = testee.ImageDialog()
        assert capsys.readouterr().out == 'called ImageDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ImageDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.ImageDialog(parent)
        assert testobj._parent == parent
        assert testobj.linktxt == ''
        assert isinstance(testobj.link_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.choose_button, testee.qtw.QPushButton)
        assert isinstance(testobj.title_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.alt_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output["image_dialog"].format(testobj=testobj)

    def test_kies(self, monkeypatch, capsys):
        """unittest for ImageDialog.kies
        """
        def mock_get(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
            return 'qqq', True
        def mock_build(arg):
            print(f"called EditorGui.build mask with arg '{arg}'")
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.link_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(xmlfn=''))
        testobj._parent.build_mask = mock_build
        testobj.kies()
        assert capsys.readouterr().out == (
                "called EditorGui.build mask with arg 'image'\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                f" ('Choose a file', '{testee.os.getcwd()}', None) {{}}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get)
        testobj._parent.editor.xmlfn = 'xxx'
        testobj.kies()
        assert capsys.readouterr().out == (
                "called EditorGui.build mask with arg 'image'\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                " ('Choose a file', 'xxx', None) {}\n"
                "called LineEdit.setText with arg `qqq`\n")

    def test_set_ltext(self, monkeypatch, capsys):
        """unittest for ImageDialog.set_ltext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.alt_text = mockqtw.MockLineEdit('qqq')
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.linktxt = 'link text'
        testobj.set_ltext('chgtext')
        assert testobj.linktxt == 'link text'
        assert capsys.readouterr().out == "called LineEdit.text\n"
        testobj.linktxt = 'qqq'
        testobj.set_ltext('chgtext')
        assert testobj.linktxt == 'chgtext'
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.setText with arg `chgtext`\n")

    def test_set_ttext(self, monkeypatch, capsys):
        """unittest for ImageDialog.set_ttext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.linktxt = 'link text'
        testobj.set_ttext('chgtext')
        assert testobj.linktxt == 'link text'
        testobj.set_ttext('')
        assert testobj.linktxt == ''

    def test_accept(self, monkeypatch, capsys):
        """unittest for ImageDialog.accept
        """
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            return 'xxx'
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Not a valid link')
        def mock_meld(message):
            print(f"called EditorGui.meld with arg '{message}'")
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(meld=mock_meld, editor=types.SimpleNamespace(
            xmlfn='qqq', convert_link=mock_convert))
        testobj.link_text = mockqtw.MockLineEdit('text')
        testobj.alt_text = mockqtw.MockLineEdit('alt')
        testobj.title_text = mockqtw.MockLineEdit('title')
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n")
        testobj.accept()
        assert testobj._parent.dialog_data == {'src': 'xxx', 'alt': 'alt', 'title': 'title'}
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called Editor.convert_link with args ('text', 'qqq')\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Dialog.accept\n")
        testobj._parent.editor.convert_link = mock_convert_2
        testobj.accept()
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called Editor.convert_link with args ('text', 'qqq')\n"
                                           "called EditorGui.meld with arg 'Not a valid link'\n")


class TestVideoDialog:
    """unittest for dialogs_qt.VideoDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.VideoDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called VideoDialog.__init__ with args', args)
        monkeypatch.setattr(testee.VideoDialog, '__init__', mock_init)
        testobj = testee.VideoDialog()
        assert capsys.readouterr().out == 'called VideoDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for VideoDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.VideoDialog(parent)
        assert testobj._parent == parent
        assert testobj.linktxt == ''
        assert isinstance(testobj.link_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.choose_button, testee.qtw.QPushButton)
        assert isinstance(testobj.hig_text, testee.qtw.QSpinBox)
        assert isinstance(testobj.wid_text, testee.qtw.QSpinBox)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output["video_dialog"].format(testobj=testobj)

    def test_kies(self, monkeypatch, capsys):
        """unittest for VideoDialog.kies
        """
        def mock_get(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
            return 'qqq', True
        def mock_build(arg):
            print(f"called EditorGui.build mask with arg '{arg}'")
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.link_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(xmlfn=''))
        testobj._parent.build_mask = mock_build
        testobj.kies()
        assert capsys.readouterr().out == (
                "called EditorGui.build mask with arg 'video'\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                f" ('Choose a file', '{testee.os.getcwd()}', None) {{}}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get)
        testobj._parent.editor.xmlfn = 'xxx'
        testobj.kies()
        assert capsys.readouterr().out == (
                "called EditorGui.build mask with arg 'video'\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                " ('Choose a file', 'xxx', None) {}\n"
                "called LineEdit.setText with arg `qqq`\n")

    def test_on_text(self, monkeypatch, capsys):
        """unittest for VideoDialog.on_text
        """
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information',
                            mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(title='title')
        testobj.on_text('xxx')
        assert capsys.readouterr().out == (
                "called MessageBox.information with args"
                f" `{testobj}` `title` `Number must be numeric integer`\n")
        testobj.on_text(1)
        assert capsys.readouterr().out == ""

    def test_accept(self, monkeypatch, capsys):
        """unittest for VideoDialog.accept
        """
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            return 'xxx'
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Not a valid link')
        def mock_meld(message):
            print(f"called EditorGui.meld with arg '{message}'")
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(meld=mock_meld, editor=types.SimpleNamespace(
            xmlfn='qqq', convert_link=mock_convert))
        testobj.link_text = mockqtw.MockLineEdit('text')
        testobj.hig_text = mockqtw.MockSpinBox()
        testobj.wid_text = mockqtw.MockSpinBox()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called SpinBox.__init__\ncalled SpinBox.__init__\n")
        testobj.accept()
        assert testobj._parent.dialog_data == {'src': 'xxx', 'height': '0', 'width': '0'}
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called Editor.convert_link with args ('text', 'qqq')\n"
                                           "called SpinBox.value\n"
                                           "called SpinBox.value\n"
                                           "called Dialog.accept\n")
        testobj._parent.editor.convert_link = mock_convert_2
        testobj.accept()
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called Editor.convert_link with args ('text', 'qqq')\n"
                                           "called EditorGui.meld with arg 'Not a valid link'\n")


class TestAudioDialog:
    """unittest for dialogs_qt.AudioDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.AudioDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called AudioDialog.__init__ with args', args)
        monkeypatch.setattr(testee.AudioDialog, '__init__', mock_init)
        testobj = testee.AudioDialog()
        assert capsys.readouterr().out == 'called AudioDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for AudioDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.AudioDialog(parent)
        assert testobj._parent == parent
        assert testobj.linktxt == ''
        assert isinstance(testobj.link_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.choose_button, testee.qtw.QPushButton)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output["audio_dialog"].format(testobj=testobj)

    def test_kies(self, monkeypatch, capsys):
        """unittest for AudioDialog.kies
        """
        def mock_get(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
            return 'qqq', True
        def mock_build(arg):
            print(f"called EditorGui.build mask with arg '{arg}'")
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.link_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(xmlfn=''))
        testobj._parent.build_mask = mock_build
        testobj.kies()
        assert capsys.readouterr().out == (
                "called EditorGui.build mask with arg 'audio'\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                f" ('Choose a file', '{testee.os.getcwd()}', None) {{}}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get)
        testobj._parent.editor.xmlfn = 'xxx'
        testobj.kies()
        assert capsys.readouterr().out == (
                "called EditorGui.build mask with arg 'audio'\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                " ('Choose a file', 'xxx', None) {}\n"
                "called LineEdit.setText with arg `qqq`\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for AudioDialog.accept
        """
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            return 'xxx'
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Not a valid link')
        def mock_meld(message):
            print(f"called EditorGui.meld with arg '{message}'")
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(meld=mock_meld, editor=types.SimpleNamespace(
            xmlfn='qqq', convert_link=mock_convert))
        testobj.link_text = mockqtw.MockLineEdit('text')
        assert capsys.readouterr().out == ("called LineEdit.__init__\n")
        testobj.accept()
        assert testobj._parent.dialog_data == {'src': 'xxx'}
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called Editor.convert_link with args ('text', 'qqq')\n"
                                           "called Dialog.accept\n")
        testobj._parent.editor.convert_link = mock_convert_2
        testobj.accept()
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called Editor.convert_link with args ('text', 'qqq')\n"
                                           "called EditorGui.meld with arg 'Not a valid link'\n")


class TestListDialog:
    """unittest for dialogs_qt.ListDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ListDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ListDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ListDialog, '__init__', mock_init)
        testobj = testee.ListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ListDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.ListDialog(parent)
        assert testobj._parent == parent
        assert testobj.items == []
        assert testobj.dataitems == []
        assert isinstance(testobj.type_select, testee.qtw.QComboBox)
        assert isinstance(testobj.rows_text, testee.qtw.QSpinBox)
        assert isinstance(testobj.list_table, testee.qtw.QTableWidget)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['list_dialog'].format(testobj=testobj)

    def test_on_type(self, monkeypatch, capsys):
        """unittest for ListDialog.on_type
        """
        def mock_current():
            print('called ComboBox.currentText')
            return 'xxxxx'
        def mock_current_2():
            print('called ComboBox.currentText')
            return 'ddddd'
        def mock_colcount_1():
            print("called Table.columnCount")
            return 1
        def mock_colcount_2():
            print("called Table.columnCount")
            return 2
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.type_select = mockqtw.MockComboBox()
        testobj.list_table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.type_select.currentText = mock_current
        testobj.on_type()
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Table.columnCount\n"
                                           "called Table.horizontalHeader\n")
        testobj.type_select.currentText = mock_current_2
        testobj.on_type()
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Table.columnCount\n"
                                           "called Table.horizontalHeader\n")
        testobj.list_table.columnCount = mock_colcount_1
        testobj.type_select.currentText = mock_current
        testobj.on_type()
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Table.columnCount\n"
                                           "called Table.horizontalHeader\n")
        testobj.type_select.currentText = mock_current_2
        testobj.on_type()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called Table.columnCount\n"
                "called Table.horizontalHeader\n"
                "called Table.insertColumn with arg '0'\n"
                "called Table.setHorizontalHeaderLabels with arg '['term', 'description']'\n"
                "called Header.resizeSection for col 0 width 102\n"
                "called Header.resizeSection for col 1 width 152\n")
        testobj.list_table.columnCount = mock_colcount_2
        testobj.type_select.currentText = mock_current
        testobj.on_type()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called Table.columnCount\n"
                "called Table.horizontalHeader\n"
                "called Table.removeColumn with arg '0'\n"
                "called Table.setHorizontalHeaderLabels with arg '['list item']'\n"
                "called Header.resizeSection for col 0 width 254\n")
        testobj.type_select.currentText = mock_current_2
        testobj.on_type()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called Table.columnCount\n"
                "called Table.horizontalHeader\n")

    def test_on_rows(self, monkeypatch, capsys):
        """unittest for ListDialog.on_rows
        """
        def mock_value():
            print("called SpinBox.value")
            return 'xx'
        def mock_value_1():
            print("called SpinBox.value")
            return 1
        def mock_value_2():
            print("called SpinBox.value")
            return 2
        def mock_value_3():
            print("called SpinBox.value")
            return 3
        def mock_rows():
            print("called Table.rowCount")
            return 2
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information',
                            mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(title='title')
        testobj.rows_text = mockqtw.MockSpinBox()
        testobj.list_table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called SpinBox.__init__\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj.rows_text.value = mock_value
        testobj.list_table.rowCount = mock_rows
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called SpinBox.value\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `Number must be numeric integer`\n")
        testobj.rows_text.value = mock_value_1
        testobj.on_rows()
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called Table.rowCount\n"
                                           "called Table.removeRow with arg '1'\n")
        testobj.rows_text.value = mock_value_2
        testobj.on_rows()
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called Table.rowCount\n")
        testobj.rows_text.value = mock_value_3
        testobj.on_rows()
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called Table.rowCount\n"
                                           "called Table.insertRow with arg '2'\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for ListDialog.accept
        """
        def mock_rows():
            print('called Table.rowCount')
            return 1
        def mock_item(x, y):
            print(f"called Table.item with args ({x}, {y})")
            return None
        def mock_item2(x, y):
            print(f"called Table.item with args ({x}, {y})")
            return listitem
        def mock_item3(x, y):
            print(f"called Table.item with args ({x}, {y})")
            if y == 0:
                return listitem
            return None
        def mock_meld(message):
            print(f"called EditorGui.meld with arg '{message}'")
        def mock_text():
            print('called ComboBox.currentText')
            return 'ddddd'
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(meld=mock_meld, dialog_data=())
        testobj.type_select = mockqtw.MockComboBox()
        testobj.list_table = mockqtw.MockTable()
        listitem = mockqtw.MockTableItem('xxx')
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n"
                                           "called TableItem.__init__ with arg xxx\n")
        testobj.accept()
        assert testobj._parent.dialog_data == ('cl', [])
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Table.rowCount\n"
                                           "called Dialog.accept\n")

        testobj._parent.dialog_data = ()
        testobj.list_table.rowCount = mock_rows
        testobj.list_table.item = mock_item
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called EditorGui.meld with arg"
                                           " 'Graag nog even het laatste item bevestigen (...)'\n")

        testobj._parent.dialog_data = ()
        testobj.list_table.item = mock_item2
        testobj.accept()
        assert testobj._parent.dialog_data == ('cl', [['xxx']])
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Dialog.accept\n")

        testobj._parent.dialog_data = ()
        testobj.list_table.item = mock_item3
        testobj.type_select.currentText = mock_text
        testobj.accept()
        assert not testobj._parent.dialog_data
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n"
                                           "called EditorGui.meld with arg"
                                           " 'Graag nog even het laatste item bevestigen (...)'\n")

        testobj.list_table.item = mock_item2
        testobj.accept()
        assert testobj._parent.dialog_data == ('dl', [['xxx', 'xxx']])
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n"
                                           "called Dialog.accept\n")


class TestTableDialog:
    """unittest for dialogs_qt.TableDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.TableDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TableDialog.__init__ with args', args)
        monkeypatch.setattr(testee.TableDialog, '__init__', mock_init)
        testobj = testee.TableDialog()
        assert capsys.readouterr().out == 'called TableDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for TableDialog.__init__
        """
        parent = MockEditorGui()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', lambda *x: True)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', lambda *x: False)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.TableDialog(parent)
        assert testobj._parent == parent
        assert testobj.headings == ['']
        assert isinstance(testobj.title_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.rows_text, testee.qtw.QSpinBox)
        assert isinstance(testobj.cols_text, testee.qtw.QSpinBox)
        assert isinstance(testobj.table_table, testee.qtw.QTableWidget)
        assert isinstance(testobj.ok_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['table_dialog'].format(testobj=testobj)

    def test_on_rows(self, monkeypatch, capsys):
        """unittest for TableDialog.on_rows
        """
        def mock_value():
            print("called SpinBox.value")
            return 'xx'
        def mock_value_1():
            print("called SpinBox.value")
            return 1
        def mock_value_2():
            print("called SpinBox.value")
            return 2
        def mock_value_3():
            print("called SpinBox.value")
            return 3
        def mock_rows():
            print("called Table.rowCount")
            return 2
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information',
                            mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(title='title')
        testobj.rows_text = mockqtw.MockSpinBox()
        testobj.table_table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called SpinBox.__init__\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj.rows_text.value = mock_value
        testobj.table_table.rowCount = mock_rows
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called SpinBox.value\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `Number must be numeric integer`\n")
        testobj.rows_text.value = mock_value_1
        testobj.on_rows()
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called Table.rowCount\n"
                                           "called Table.removeRow with arg '1'\n")
        testobj.rows_text.value = mock_value_2
        testobj.on_rows()
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called Table.rowCount\n")
        testobj.rows_text.value = mock_value_3
        testobj.on_rows()
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called Table.rowCount\n"
                                           "called Table.insertRow with arg '2'\n")

    def test_on_cols(self, monkeypatch, capsys):
        """unittest for TableDialog.on_cols
        """
        def mock_value():
            print("called SpinBox.value")
            return 'xx'
        def mock_value_1():
            print("called SpinBox.value")
            return 1
        def mock_value_2():
            print("called SpinBox.value")
            return 2
        def mock_value_3():
            print("called SpinBox.value")
            return 3
        def mock_cols():
            print("called Table.columnCount")
            return 2
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information',
                            mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(title='title')
        testobj.cols_text = mockqtw.MockSpinBox()
        testobj.table_table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called SpinBox.__init__\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj.cols_text.value = mock_value
        testobj.table_table.columnCount = mock_cols
        testobj.on_cols()
        assert capsys.readouterr().out == (
                "called SpinBox.value\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `Number must be numeric integer`\n")
        testobj.cols_text.value = mock_value_1
        testobj.headings = ['', '']
        testobj.on_cols()
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called Table.columnCount\n"
                                           "called Table.removeColumn with arg '1'\n")
        assert testobj.headings == ['']
        testobj.cols_text.value = mock_value_2
        testobj.headings = ['', '']
        testobj.on_cols()
        assert testobj.headings == ['', '']
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called Table.columnCount\n")
        testobj.cols_text.value = mock_value_3
        testobj.headings = ['', '']
        testobj.on_cols()
        assert testobj.headings == ['', '', '']
        assert capsys.readouterr().out == (
                "called SpinBox.value\n"
                "called Table.columnCount\n"
                "called Table.insertColumn with arg '2'\n"
                "called Table.setHorizontalHeaderLabels with arg '['', '', '']'\n")

    def test_on_check(self, monkeypatch, capsys):
        """unittest for TableDialog.on_check
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hdr = mockqtw.MockHeader()
        assert capsys.readouterr().out == "called Header.__init__\n"
        testobj.on_check()
        assert capsys.readouterr().out == "called Header.setVisible with args 'False'\n"
        testobj.on_check(0)
        assert capsys.readouterr().out == "called Header.setVisible with args 'False'\n"
        testobj.on_check(1)
        assert capsys.readouterr().out == "called Header.setVisible with args 'True'\n"

    def test_on_title(self, monkeypatch, capsys):
        """unittest for TableDialog.on_title
        """
        def mock_text(parent, *args, **kwargs):
            print('called InputDialog.getText with args', parent, args, kwargs)
            return '', True
        def mock_text_2(parent, *args, **kwargs):
            print('called InputDialog.getText with args', parent, args, kwargs)
            return 'xxx', True
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mockqtw.MockInputDialog.getText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table_table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.headings = {}
        testobj.on_title(2)
        assert not testobj.headings
        assert capsys.readouterr().out == (
                "called InputDialog.getText with args"
                f" {testobj} ('Add a table', 'Enter a title for this column:') {{'text': ''}}\n")
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_text)
        testobj.on_title(2)
        assert not testobj.headings
        assert capsys.readouterr().out == (
                "called InputDialog.getText with args"
                f" {testobj} ('Add a table', 'Enter a title for this column:') {{'text': ''}}\n")
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_text_2)
        testobj.on_title(2)
        assert testobj.headings == {2: 'xxx'}
        assert capsys.readouterr().out == (
                "called InputDialog.getText with args"
                f" {testobj} ('Add a table', 'Enter a title for this column:') {{'text': ''}}\n"
                "called Table.setHorizontalHeaderLabels with arg '{2: 'xxx'}'\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for TableDialog.accept
        """
        def mock_rows():
            print('called Table.rowCount')
            return 1
        def mock_cols():
            print('called Table.columnCount')
            return 1
        def mock_item(x, y):
            print(f"called Table.item with args ({x}, {y})")
            return None
        def mock_item2(x, y):
            print(f"called Table.item with args ({x}, {y})")
            return tableitem
        def mock_meld(message):
            print(f"called EditorGui.meld with arg '{message}'")
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(meld=mock_meld)
        testobj.table_table = mockqtw.MockTable()
        tableitem = mockqtw.MockTableItem('xxx')
        testobj.title_text = mockqtw.MockLineEdit('qqq')
        testobj.show_titles = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n"
                                           "called TableItem.__init__ with arg xxx\n"
                                           "called LineEdit.__init__\n"
                                           "called CheckBox.__init__\n")
        testobj.headings = []
        testobj.accept()
        assert testobj._parent.dialog_data == ('qqq', False, [], [])
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.columnCount\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")
        testobj._parent.dialog_data = ()
        testobj.table_table.rowCount = mock_rows
        testobj.table_table.columnCount = mock_cols
        testobj.table_table.item = mock_item
        testobj.headings = ['yyy']
        testobj.accept()
        assert testobj._parent.dialog_data == ()
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.columnCount\n"
                                           "called LineEdit.text\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called EditorGui.meld with arg"
                                           " 'Graag nog even het laatste item bevestigen (...)'\n")
        testobj.table_table.item = mock_item2
        testobj.show_titles.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        testobj.accept()
        assert testobj._parent.dialog_data == ('qqq', True, ['yyy'], [['xxx']])
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.columnCount\n"
                                           "called LineEdit.text\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")


class TestScrolledTextDialog:
    """unittest for dialogs_qt.ScrolledTextDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ScrolledTextDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ScrolledTextDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ScrolledTextDialog, '__init__', mock_init)
        testobj = testee.ScrolledTextDialog()
        assert capsys.readouterr().out == 'called ScrolledTextDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ScrolledTextDialog.__init__
        """
        def mock_do(arg):
            print(f'called Editor.do_validate with arg {arg}')
        parent = MockEditorGui()
        parent.editor = types.SimpleNamespace(do_validate=mock_do)
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = testee.ScrolledTextDialog(parent, data='data')
        assert testobj.parent == parent
        assert testobj.htmlfile == ''
        assert isinstance(testobj.message, testee.qtw.QLabel)
        assert capsys.readouterr().out == expected_output['scrolled_dialog'].format(
                testobj=testobj, title='', size=(600, 400), msg='')

        testobj = testee.ScrolledTextDialog(parent, title='title', htmlfile='htmlfile',
                                            fromdisk=True, size=(100, 200))
        assert testobj.htmlfile == 'htmlfile'
        assert capsys.readouterr().out == expected_output['scrolled_dialog2'].format(
                testobj=testobj, title='title', size=(100, 200), msg='\n' + testee.VAL_MESSAGE)

    def test_show_source(self, monkeypatch, capsys, tmp_path):
        """unittest for ScrolledTextDialog.show_source
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called CodeViewDialog.__init__ with args', args, kwargs)
            def show(self):
                print('called CodeViewDialog.show')
        monkeypatch.setattr(testee, 'CodeViewDialog', MockDialog)
        testfile = tmp_path / 'testhtml'
        testfile.touch()
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.htmlfile = testfile
        testobj.show_source()
        assert capsys.readouterr().out == ""
        testfile.write_text('xxxx\nyyyy\nzzzz\n')
        testobj.show_source()
        assert capsys.readouterr().out == (
                "called CodeViewDialog.__init__ with args"
                f" ({testobj}, 'Submitted source') {{'data': 'xxxx\\nyyyy\\nzzzz\\n'}}\n"
                "called CodeViewDialog.show\n")


class TestCodeViewDialog:
    """unittest for dialogs_qt.CodeViewDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.CodeViewDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CodeViewDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CodeViewDialog, '__init__', mock_init)
        testobj = testee.CodeViewDialog()
        assert capsys.readouterr().out == 'called CodeViewDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for CodeViewDialog.__init__
        """
        def mock_setup(self):
            print('called CodeViewDialog.setup_text')
        parent = MockEditorGui()
        parent.editor = types.SimpleNamespace()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        # monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.sci, 'QsciScintilla', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.CodeViewDialog, 'setup_text', mock_setup)
        testobj = testee.CodeViewDialog(parent)
        assert capsys.readouterr().out == expected_output['code_dialog'].format(testobj=testobj,
                                                                                title='',
                                                                                size=(600, 400),
                                                                                caption='',
                                                                                data='')
        testobj = testee.CodeViewDialog(parent, title='title', caption='caption', data='data',
                                        size=(200, 100))
        assert capsys.readouterr().out == expected_output['code_dialog'].format(testobj=testobj,
                                                                                title='title',
                                                                                size=(200, 100),
                                                                                caption='caption',
                                                                                data='data')

    def test_setup_text(self, monkeypatch, capsys):
        """unittest for CodeViewDialog.setup_text
        """
        monkeypatch.setattr(testee.gui, 'QFont', mockqtw.MockFont)
        monkeypatch.setattr(testee.gui, 'QFontMetrics', mockqtw.MockFontMetrics)
        monkeypatch.setattr(testee.gui, 'QColor', mockqtw.MockColor)
        monkeypatch.setattr(testee.sci, 'QsciLexerHTML', mockqtw.MockLexer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.setup_text()
        assert capsys.readouterr().out == (
                "called Font.__init__\n"
                "called Font.setFamily\n"
                "called Font.setFixedPitch\n"
                "called Font.setPointSize\n"
                "called Editor.setFont\n"
                "called Editor.setMarginsFont\n"
                "called Fontmetrics.__init__()\n"
                "called Editor.setMarginsFont\n"
                "called Editor.horizontalAdvance()\n"
                "called Editor.setMarginWidth with args (0, None)\n"
                "called Editor.setMarginLineNumbers with args (0, True)\n"
                "called Editor.setMarginsBackgroundColor with arg 'color #cccccc'\n"
                "called Editor.setBraceMatching with arg `BraceMatch.SloppyBraceMatch`\n"
                "called Editor.setAutoIndent with arg `True`\n"
                "called Editor.setFolding with arg `FoldStyle.PlainFoldStyle`\n"
                "called Editor.setCaretLineVisible with arg `True`\n"
                "called Editor.setCaretLineBackgroundColor with arg 'color #ffe4e4'\n"
                "called Lexer.__init__()\n"
                "called Editor.setDefaultFont\n"
                "called Editor.setLexer\n")
