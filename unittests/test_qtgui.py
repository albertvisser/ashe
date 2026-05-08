"""unittests for ./ashe/qtgui.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from ashe import qtgui as testee
from unittests.output_fixtures import expected_output

class MockEditor:
    """stub for main.Editor object
    """
    constants = {'ELSTART': '<>'}
    def mark_dirty(self, value):
        "stub"
        print(f"called Editor.mark_dirty with arg {value}")
    def refresh_preview(self):
        "stub"
        print("called Editorrefresh_preview")


class MockEditorGui:
    """stub for gui_qt.EditorGui object
    """
    def meld(self, message):
        "stub"
        print(f"called EditorGui.meld with arg '{message}'")


class TestEditorGui:
    """unittest for gui_qt.EditorGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.EditorGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditorGui.__init__ with args', args)
        monkeypatch.setattr(testee.EditorGui, '__init__', mock_init)
        testobj = testee.EditorGui()
        testobj.editor = MockEditor()
        assert capsys.readouterr().out == 'called EditorGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditorGui.__init__
        """
        def mock_init(self, *args):
            print('called MainWindow.__init__ with args', args)
        def mock_init_app(self, *args):
            print('called Application.__init__ with args', args)
        def mock_show(self, *args):
            print(f"called show_message with args", args)
        def mock_meld(self, message):
            print(f"called EditorGui.meld with arg '{message}'")
        monkeypatch.setattr(testee, 'show_message', mock_show)
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowIcon',
                            mockqtw.MockMainWindow.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_init_app)
        monkeypatch.setattr(testee.EditorGui, 'meld', mock_meld)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.sys, 'argv', ['aaa', 'bbb'])
        testobj = testee.EditorGui('editor', 'title', 'icon')
        assert testobj.editor == 'editor'
        assert testobj.dialog_data == {}
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert isinstance(testobj.appicon, testee.gui.QIcon)
        assert capsys.readouterr().out == (
                "called Application.__init__ with args (['aaa', 'bbb'],)\n"
                "called MainWindow.__init__ with args ()\n"
                "called MainWindow.setWindowTitle with arg `title`\n"
                "called Icon.__init__ with arg `icon`\n"
                "called MainWindow.setWindowIcon\n"
                "called MainWindow.resize with args (1200, 900)\n")

    def test_create_menu(self, monkeypatch, capsys):
        """unittest for EditorGui.create_menu
        """
    #     def mock_setup_menu(self):
    #         print('called EditorGui.setup_menu')
    #         self.adv_menu = mockqtw.MockAction()
    #     monkeypatch.setattr(testee.EditorGui, 'setup_menu', mock_setup_menu)
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.create_menu()
    #     assert isinstance(testobj.adv_menu, mockqtw.MockAction)
    #     assert capsys.readouterr().out == (
    #             "called EditorGui.setup_menu\n"
    #             "called Action.__init__ with args ()\n")
    # def test_setup_menu(self, monkeypatch, capsys, expected_output):
        """unittest for EditorGui.setup_menu
        """
        def mock_menubar():
            result = mockqtw.MockMenuBar()
            assert capsys.readouterr().out == "called MenuBar.__init__\n"
            print('called EditorGui.menuBar')
            return result
        def mock_get():
            print('called Editor.get_menulist')
            return []
        def mock_get_2():
            print('called Editor.get_menulist')
            return [('xxx', []), ('&Edit', [('aa', 'A', 'A', 'aaaaaa', testobj.callback1),
                                            ('bb', 'B', '', 'bbbbbb', testobj.callback2),
                                            ('cc', 'C', 'C', 'cccccc', testobj.callback3)]),
                    ('&View', [('Advance selection...', '', '', 'xxx', testobj.callback4),
                               ('qq', 'Q', 'C', 'qqqq', testobj.callback0)]),
                    ('&Search', [('',)]),
                    ('&HTML', [('Add &DTD', 'D', 'ACS', 'ddddd', testobj.callback5),
                               ('Add &Stylesheet', 'E', 'SCA', 'eeeee', testobj.callback6)])]
        monkeypatch.setattr(testee.qtw, 'QMenu', mockqtw.MockMenu)
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menuBar = mock_menubar
        testobj.callback0 = lambda *x: 0
        testobj.callback1 = lambda *x: 1
        testobj.callback2 = lambda *x: 2
        testobj.callback3 = lambda *x: 3
        testobj.callback4 = lambda *x: 4
        testobj.callback5 = lambda *x: 5
        testobj.callback6 = lambda *x: 6
        testobj.editor.get_menulist = mock_get
        testobj.create_menu()
        assert testobj.contextmenu_items == []
        # assert not hasattr(testobj, 'adv_menu')
        # assert not hasattr(testobj, 'dtd_menu')
        # assert not hasattr(testobj, 'css_menu')
        assert capsys.readouterr().out == ("called EditorGui.menuBar\n"
                                           "called Editor.get_menulist\n")

        testobj.editor.get_menulist = mock_get_2
        testobj.create_menu()
        assert len(testobj.contextmenu_items) == 5
        assert [x[0] for x in testobj.contextmenu_items] == ['M', 'A', '', 'M', 'M']
        assert isinstance(testobj.contextmenu_items[0][1], testee.qtw.QMenu)
        assert testobj.contextmenu_items[0][1].title() == '&Edit'
        assert isinstance(testobj.contextmenu_items[1][1], testee.gui.QAction)
        assert testobj.contextmenu_items[1][1].text() == 'qq'
        assert testobj.contextmenu_items[2][1] == ''
        assert isinstance(testobj.contextmenu_items[3][1], testee.qtw.QMenu)
        assert testobj.contextmenu_items[3][1].title() == '&Search'
        assert isinstance(testobj.contextmenu_items[4][1], testee.qtw.QMenu)
        assert testobj.contextmenu_items[4][1].title() == '&HTML'
        assert isinstance(testobj.adv_menu, testee.gui.QAction)
        assert testobj.adv_menu.text() == 'Advance selection...'
        assert isinstance(testobj.dtd_menu, testee.gui.QAction)
        assert testobj.dtd_menu.text() == 'Add &DTD'
        assert isinstance(testobj.css_menu, testee.gui.QAction)
        assert testobj.css_menu.text() == 'Add &Stylesheet'
        # uitgezet want ik kan niet alle variabelen goed weergeven
        # assert capsys.readouterr().out == expected_output['setup_menu'].format(testobj=testobj)

    def test_create_splitter(self, monkeypatch, capsys):
        """unittest for EditorGui.create_splitter
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        monkeypatch.setattr(testee.qtw, 'QSplitter', mockqtw.MockSplitter)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_splitter()
        assert isinstance(testobj.pnl, testee.qtw.QSplitter)
        assert capsys.readouterr().out == (
                "called Splitter.__init__\n"
                "called MainWidget.setCentralWidget with arg `MockSplitter`\n")

    def test_create_tree_on_left(self, monkeypatch, capsys):
        """unittest for EditorGui.create_tree_on_left
        """
        # monkeypatch.setattr(mockqtw.MockSplitter, 'addWidget', mock_add)
        # def mock_add(self, *args):
        #     print(f'called Splitter.addWidget with arg `{args[0]}`')
        monkeypatch.setattr(testee, 'VisualTree', mockqtw.MockTreeWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__\n"
        testobj.create_tree_on_left()
        assert isinstance(testobj.tree, testee.VisualTree)
        assert capsys.readouterr().out == (
                "called Tree.__init__\n"
                "called Tree.headerItem\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setHidden with arg `True`\n"
                f"called Splitter.addWidget with arg MockTreeWidget\n")

    def test_create_preview_on_right(self, monkeypatch, capsys):
        """unittest for EditorGui.create_preview_on_right
        """
        monkeypatch.setattr(testee.webeng, 'QWebEngineView', mockqtw.MockWebEngineView)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__\n"
        testobj.create_preview_on_right()
        assert isinstance(testobj.html, testee.webeng.QWebEngineView)
        assert capsys.readouterr().out == (
                "called WebEngineView.__init__()\n"
                f"called Splitter.addWidget with arg MockWebEngineView\n")

    def test_create_statusbar_at_bottom(self, monkeypatch, capsys):
        """unittest for EditorGui.create_statusbar_at_bottom
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw, 'QStatusBar', mockqtw.MockStatusBar)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_statusbar_at_bottom()
        assert isinstance(testobj.sb, mockqtw.MockStatusBar)
        assert capsys.readouterr().out == (
                "called MainWindow.statusBar\n"
                "called StatusBar.__init__ with args ()\n")

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for EditorGui.create_finalize_display
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mockqtw.MockMainWindow.show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.pnl = mockqtw.MockSplitter()
        testobj.adv_menu = mockqtw.MockAction()
        assert capsys.readouterr().out == ("called Tree.__init__\ncalled Splitter.__init__\n"
                                           "called Action.__init__ with args ()\n")
        testobj.finalize_display()
        assert capsys.readouterr().out == (
                "called Tree.resize with args (500, 100)\n"
                "called Splitter.setSizes with args ([300, 900],)\n"
                "called Tree.setFocus\ncalled Action.setChecked with arg `True`\n"
                "called MainWindow.show\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for EditorGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockqtw.MockApplication()
        with pytest.raises(SystemExit):
            testobj.go()
        assert capsys.readouterr().out == ("called Application.__init__\n"
                                           "called Application.exec\n")

    def test_get_screen_title(self, monkeypatch, capsys):
        """unittest for EditorGui.get_screen_title
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'windowTitle',
                            mockqtw.MockMainWindow.windowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_screen_title() == "text"
        assert capsys.readouterr().out == "called MainWindow.windowTitle\n"

    def test_set_screen_title(self, monkeypatch, capsys):
        """unittest for EditorGui.set_screen_title
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_screen_title('title')
        assert capsys.readouterr().out == "called MainWindow.setWindowTitle with arg `title`\n"

    def test_get_element_text(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('xxx')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx',)\n"
        assert testobj.get_element_text(node) == "xxx"
        assert capsys.readouterr().out == "called TreeItem.text with arg 0\n"

    def test_get_element_parent(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_parent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('xxx')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx',)\n"
        assert testobj.get_element_parent(node) == "parent"
        assert capsys.readouterr().out == "called TreeItem.parent\n"

    def test_get_element_parentpos(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_parentpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent = mockqtw.MockTreeItem('qqq')
        item = mockqtw.MockTreeItem('xxx')
        parent.addChild(item)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('qqq',)\n"
                                           "called TreeItem.__init__ with args ('xxx',)\n"
                                           "called TreeItem.addChild\n")
        assert testobj.get_element_parentpos(item) == (parent, 0)
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.indexOfChild\n")

    def test_get_element_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('xxx')
        node.setData(0, testee.core.Qt.ItemDataRole.UserRole, 'yyy')
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ('xxx',)\n"
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'yyy')\n")
        assert testobj.get_element_data(node) == "yyy"
        assert capsys.readouterr().out == (
                f"called TreeItem.data with args (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n")

    def test_get_element_children(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_children
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('qqq')
        item = mockqtw.MockTreeItem('xxx')
        node.addChild(item)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('qqq',)\n"
                                           "called TreeItem.__init__ with args ('xxx',)\n"
                                           "called TreeItem.addChild\n")
        assert testobj.get_element_children(node) == [item]
        assert capsys.readouterr().out == ("called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n")

    def test_set_element_text(self, monkeypatch, capsys):
        """unittest for EditorGui.set_element_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('xxx')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx',)\n"
        testobj.set_element_text(node, 'text')
        assert capsys.readouterr().out == "called TreeItem.setText with args (0, 'text')\n"

    def test_set_element_data(self, monkeypatch, capsys):
        """unittest for EditorGui.set_element_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('xxx')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx',)\n"
        testobj.set_element_data(node, 'data')
        assert capsys.readouterr().out == (
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'data')\n")

    def test_addtreeitem(self, monkeypatch, capsys):
        """unittest for EditorGui.addtreeitem
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('xxx')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx',)\n"
        result = testobj.addtreeitem(node, 'naam', 'data')
        assert isinstance(result, testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setText with args (0, 'naam')\n"
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'data')\n"
                "called TreeItem.addChild\n")
        result = testobj.addtreeitem(node, 'naam', 'data', 0)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setText with args (0, 'naam')\n"
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'data')\n"
                "called TreeItem.insertChild at pos 0\n")

    def test_addtreetop(self, monkeypatch, capsys):
        """unittest for EditorGui.addtreetop
        """
        # monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.addtreetop('fname', 'titel')
        assert capsys.readouterr().out == ("called MainWindow.setWindowTitle with arg `titel`\n"
                                           "called Tree.clear\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with args (0, 'fname')\n"
                                           "called Tree.addTopLevelItem\n")

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for EditorGui.get_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_selected_item() == "called Tree.currentItem"
        assert capsys.readouterr().out == ""

    def test_set_selected_item(self, monkeypatch, capsys):
        """unittest for EditorGui.set_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj.set_selected_item(item)
        assert capsys.readouterr().out == f"called Tree.setCurrentItem with arg `{item}`\n"

    def test_init_tree(self, monkeypatch, capsys):
        """unittest for EditorGui.init_tree
        """
        def mock_set(text):
            print(f"called EditorGui.show_statusbar_message with arg '{text}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show_statusbar_message = mock_set
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.top = mockqtw.MockTreeItem()
        testobj.adv_menu = mockqtw.MockAction()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n")
        testobj.init_tree('message')
        assert capsys.readouterr().out == (
                f"called Tree.setCurrentItem with arg `{testobj.top}`\n"
                "called Action.setChecked with arg `True`\n"
                "called EditorGui.show_statusbar_message with arg 'message'\n")

    def test_show_statusbar_message(self, monkeypatch, capsys):
        """unittest for EditorGui.show_statusbar_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sb = mockqtw.MockStatusBar()
        assert capsys.readouterr().out == "called StatusBar.__init__ with args ()\n"
        testobj.show_statusbar_message('text')
        assert capsys.readouterr().out == "called StatusBar.showMessage with arg `text`\n"

    def test_adjust_dtd_menu(self, monkeypatch, capsys):
        """unittest for EditorGui.adjust_dtd_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.dtd_menu = mockqtw.MockAction()
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.editor.has_dtd = False
        testobj.adjust_dtd_menu()
        assert capsys.readouterr().out == (
                "called Action.setText with arg `Add &DTD`\n"
                "called Action.setStatusTip with arg 'Add a document type description'\n")
        testobj.editor.has_dtd = True
        testobj.adjust_dtd_menu()
        assert capsys.readouterr().out == (
                "called Action.setText with arg `Remove &DTD`\n"
                "called Action.setStatusTip with arg 'Remove the document type declaration'\n")

    def test_popup_menu(self, monkeypatch, capsys):
        """unittest for EditorGui.popup_menu
        """

        # def mock_rect(arg):
        #     print('called Tree.visualItemRect with arg', arg)
        #     return types.SimpleNamespace(bottom=100, left=100)
        monkeypatch.setattr(testee.qtw, 'QMenu', mockqtw.MockMenu)
        # monkeypatch.setattr(testee.core, 'QPoint', mockqtw.MockPoint)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        # testobj.tree.visualItemRect = mock_rect
        item = mockqtw.MockTreeItem()
        action = mockqtw.MockAction()
        submenu = mockqtw.MockMenu()
        testobj.contextmenu_items = [('A', action), ('M', submenu), ('', '')]
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Menu.__init__ with args ()\n")
        testobj.popup_menu()
        assert capsys.readouterr().out == ""
        testobj.popup_menu(item)
        assert capsys.readouterr().out == (
                "called Menu.__init__ with args ()\n"
                "called Menu.addAction\n"
                f"called Menu.addMenu with args ({submenu},)\n"
                "called Action.__init__ with args ()\n"
                "called Menu.addSeparator\n"
                "called Action.__init__ with args ('-----', None)\n"
                f"called Tree.visualItemRect with arg {item}\n"
                "called Tree.mapToGlobal with arg bottom-right\n"
                "called Menu.exec with args ('mapped-to-global',) {}\n")

    def test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for EditorGui.keyReleaseEvent
        """
        def mock_keyup(event):
            print(f'called EditorGui.on_key_up with arg {event}')
            return True
        def mock_keyup_2(event):
            print(f'called EditorGui.on_key_up with arg {event}')
            return False
        monkeypatch.setattr(testee.qtw.QMainWindow, 'keyReleaseEvent',
                            mockqtw.MockMainWindow.keyReleaseEvent)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_keyup = mock_keyup
        testobj.keyReleaseEvent('event')
        assert capsys.readouterr().out == ("called EditorGui.on_key_up with arg event\n")
        testobj.on_keyup = mock_keyup_2
        testobj.keyReleaseEvent('event')
        assert capsys.readouterr().out == ("called EditorGui.on_key_up with arg event\n"
                                           "called MainWindow.keyReleaseEvent\n")

    def test_on_keyup(self, monkeypatch, capsys):
        """unittest for EditorGui.on_keyup
        """
        def mock_current(self):
            print('called Tree.setCurrentItem')
            return self.current
        def mock_popup(arg):
            print(f'called Tree.popup_menu with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(mockqtw.MockTreeWidget, 'currentItem', mock_current)
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.popup_menu = mock_popup
        testobj.top = mockqtw.MockTreeItem()
        item = mockqtw.MockTreeItem()
        event = mockqtw.MockEvent(key='x')
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n")

        testobj.tree.current = None
        assert not testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called Tree.setCurrentItem\n")
        testobj.tree.current = testobj.top
        assert not testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called Tree.setCurrentItem\n")
        testobj.tree.current = item
        assert not testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called Tree.setCurrentItem\n")
        event = mockqtw.MockEvent(key=testee.core.Qt.Key.Key_Menu)
        assert testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called Tree.setCurrentItem\n"
                                           f"called Tree.popup_menu with arg {item}\n")

    def test_ask_how_to_continue(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_how_to_continue
        """
        def mock_ask(*args):
            print('called ask_yesnocancel with args', args)
            return 'ync'
        monkeypatch.setattr(testee, 'ask_yesnocancel', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(title='title from parent')
        assert testobj.ask_how_to_continue('', 'text') == 'ync'
        assert capsys.readouterr().out == (
                f"called ask_yesnocancel with args ({testobj}, 'text', 'title from parent')\n")
        assert testobj.ask_how_to_continue('title', 'text') == 'ync'
        assert capsys.readouterr().out == (
                f"called ask_yesnocancel with args ({testobj}, 'text', 'title')\n")


    def _test_ask_yes_no_cancel(self, monkeypatch, capsys):
        def mock_ask(*args, **kwargs):
            # we krijgen hier weer zo'n StandardButtons object dus output even laten zitten
            # print(f'called MessageBox.question with args', args, kwargs)
            return testee.qtw.QMessageBox.StandardButton.No
        def mock_ask_2(*args, **kwargs):
            # print(f'called MessageBox.question with args', args, kwargs)
            return testee.qtw.QMessageBox.StandardButton.Yes
        def mock_ask_3(*args, **kwargs):
            # print(f'called MessageBox.question with args', args, kwargs)
            return testee.qtw.QMessageBox.StandardButton.Cancel
        monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_how_to_continue('title', 'text') == 0
        # assert capsys.readouterr().out == ("")
        monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask_2)
        assert testobj.ask_how_to_continue('title', 'text') == 1
        # assert capsys.readouterr().out == ("")
        monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask_3)
        assert testobj.ask_how_to_continue('title', 'text') == -1
        # assert capsys.readouterr().out == ("")

    def test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for EditorGui.set_item_expanded
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_expanded(item, True)
        assert capsys.readouterr().out == ("called TreeItem.setExpanded with arg `True`\n")
        testobj.set_item_expanded(item, False)
        assert capsys.readouterr().out == ("called TreeItem.setExpanded with arg `False`\n")

    def test_expand(self, monkeypatch, capsys):
        """unittest for EditorGui.expand
        """
        def mock_current():
            print('called Tree.currentItem')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.tree.currentItem = mock_current
        item = mockqtw.MockTreeItem('aaa')
        subitem = mockqtw.MockTreeItem('bbb')
        item.addChild(subitem)
        subitem2 = mockqtw.MockTreeItem('ccc')
        item.addChild(subitem2)
        subsubitem = mockqtw.MockTreeItem('ddd')
        subitem2.addChild(subsubitem)
        assert capsys.readouterr().out == (
                "called Tree.__init__\ncalled TreeItem.__init__ with args ('aaa',)\n"
                "called TreeItem.__init__ with args ('bbb',)\ncalled TreeItem.addChild\n"
                "called TreeItem.__init__ with args ('ccc',)\ncalled TreeItem.addChild\n"
                "called TreeItem.__init__ with args ('ddd',)\ncalled TreeItem.addChild\n")
        testobj.expand()
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           f"called Tree.expandItem with arg {item}\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.setExpanded with arg `True`\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.setExpanded with arg `True`\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.setExpanded with arg `True`\n"
                                           "called TreeItem.childCount\n"
                                           "called Tree.resizeColumnToContents with arg 0\n"
                                           f"called Tree.scrollToItem with arg `{subsubitem}`\n")

    def test_collapse(self, monkeypatch, capsys):
        """unittest for EditorGui.collapse
        """
        def mock_current():
            print('called Tree.currentItem')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.tree.currentItem = mock_current
        item = mockqtw.MockTreeItem('aaa')
        subitem = mockqtw.MockTreeItem('bbb')
        item.addChild(subitem)
        subitem2 = mockqtw.MockTreeItem('ccc')
        item.addChild(subitem2)
        subsubitem = mockqtw.MockTreeItem('ddd')
        subitem2.addChild(subsubitem)
        assert capsys.readouterr().out == (
                "called Tree.__init__\ncalled TreeItem.__init__ with args ('aaa',)\n"
                "called TreeItem.__init__ with args ('bbb',)\ncalled TreeItem.addChild\n"
                "called TreeItem.__init__ with args ('ccc',)\ncalled TreeItem.addChild\n"
                "called TreeItem.__init__ with args ('ddd',)\ncalled TreeItem.addChild\n")
        testobj.collapse()
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.setExpanded with arg `False`\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.setExpanded with arg `False`\n"
                                           "called TreeItem.setExpanded with arg `False`\n"
                                           f"called Tree.collapseItem with arg {item}\n"
                                           "called Tree.resizeColumnToContents with arg 0\n")

    def test_get_adv_sel_setting(self, monkeypatch, capsys):
        """unittest for EditorGui.get_adv_sel_setting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.adv_menu = mockqtw.MockAction()
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        assert not testobj.get_adv_sel_setting()
        assert capsys.readouterr().out == "called Action.isChecked\n"
        testobj.adv_menu.setChecked(True)
        assert capsys.readouterr().out == "called Action.setChecked with arg `True`\n"
        assert testobj.get_adv_sel_setting()
        assert capsys.readouterr().out == "called Action.isChecked\n"

    def test_refresh_preview(self, monkeypatch, capsys):
        """unittest for EditorGui.refresh_preview
        """
        monkeypatch.setattr(testee.core, 'QUrl', mockqtw.MockUrl)
        # monkeypatch.setattr(testee.os, 'abspath', lambda x: f'/abs/{x}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.xmlfn = 'xxx'
        testobj.html = mockqtw.MockWebEngineView()
        testobj.tree = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called WebEngineView.__init__()\ncalled Tree.__init__\n"
        testobj.refresh_preview('soup')
        assert capsys.readouterr().out == (
                f"called Url.fromLocalFile with arg '{testee.os.getcwd()}/xxx'\n"
                "called WebEngineView.setHtml() with args"
                f" ('soup',) {{'baseUrl': '{testee.os.getcwd()}/xxx'}}\n"
                "called Tree.setFocus\n")

    def test_do_delete_item(self, monkeypatch, capsys):
        """unittest for EditorGui.do_delete_item

        verwijder het eerste element onder het root element
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.root = parent = mockqtw.MockTreeItem('parent')
        item1 = mockqtw.MockTreeItem('item1')
        item2 = mockqtw.MockTreeItem('item2')
        parent.addChild(item1)
        parent.addChild(item2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('parent',)\n"
                                           "called TreeItem.__init__ with args ('item1',)\n"
                                           "called TreeItem.__init__ with args ('item2',)\n"
                                           "called TreeItem.addChild\ncalled TreeItem.addChild\n")
        testobj.do_delete_item(item1)
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.indexOfChild\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.removeChild\n")

    def test_do_delete_item_2(self, monkeypatch, capsys):
        """unittest for EditorGui.do_delete_item

        verwijder het eerste element onder een subnode van het root element
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.root = mockqtw.MockTreeItem('root')
        parent = mockqtw.MockTreeItem('parent')
        item1 = mockqtw.MockTreeItem('item1')
        item2 = mockqtw.MockTreeItem('item2')
        parent.addChild(item1)
        parent.addChild(item2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('root',)\n"
                                           "called TreeItem.__init__ with args ('parent',)\n"
                                           "called TreeItem.__init__ with args ('item1',)\n"
                                           "called TreeItem.__init__ with args ('item2',)\n"
                                           "called TreeItem.addChild\ncalled TreeItem.addChild\n")
        testobj.do_delete_item(item1)
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.indexOfChild\n"
                                           "called TreeItem.removeChild\n")

    def test_do_delete_item_3(self, monkeypatch, capsys):
        """unittest for EditorGui.do_delete_item

        verwijder het niet-eerste element onder een element
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.root = mockqtw.MockTreeItem('root')
        parent = mockqtw.MockTreeItem('parent')
        item1 = mockqtw.MockTreeItem('item1')
        item2 = mockqtw.MockTreeItem('item2')
        parent.addChild(item1)
        parent.addChild(item2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('root',)\n"
                                           "called TreeItem.__init__ with args ('parent',)\n"
                                           "called TreeItem.__init__ with args ('item1',)\n"
                                           "called TreeItem.__init__ with args ('item2',)\n"
                                           "called TreeItem.addChild\ncalled TreeItem.addChild\n")
        testobj.do_delete_item(item2)
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.indexOfChild\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.removeChild\n")

    def test_meld(self, monkeypatch, capsys):
        """unittest for EditorGui.meld
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.title = 'title'
        testobj.meld('text')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `title` `text`\n")

    # def _test_meld_fout(self, monkeypatch, capsys):
    #     """unittest for EditorGui.meld_fout
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.meld_fout(text, abort=False) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_ask_yesnocancel(self, monkeypatch, capsys):
    #     """unittest for EditorGui.ask_yesnocancel
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.ask_yesnocancel(prompt) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_ask_for_text(self, monkeypatch, capsys):
    #     """unittest for EditorGui.ask_for_text
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.ask_for_text(prompt) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_ensure_item_visible(self, monkeypatch, capsys):
        """unittest for EditorGui.ensure_item_visible
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj.ensure_item_visible(item)
        assert capsys.readouterr().out == (f"called Tree.scrollToItem with arg `{item}`\n")


class TestVisualTree:
    """unittest for gui_qt.VisualTree
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.VisualTree object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called VisualTree.__init__ with args', args)
        monkeypatch.setattr(testee.VisualTree, '__init__', mock_init)
        testobj = testee.VisualTree()
        testobj._parent = MockEditorGui()
        testobj._parent.editor = MockEditor()
        assert capsys.readouterr().out == 'called VisualTree.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for VisualTree.__init__
        """
        parent = 'parent'
        monkeypatch.setattr(testee.qtw.QTreeWidget, '__init__', mockqtw.MockTreeWidget.__init__)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setAcceptDrops',
                            mockqtw.MockTreeWidget.setAcceptDrops)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setDragEnabled',
                            mockqtw.MockTreeWidget.setDragEnabled)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setDragDropMode',
                            mockqtw.MockTreeWidget.setDragDropMode)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setSelectionMode',
                            mockqtw.MockTreeWidget.setSelectionMode)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setDropIndicatorShown',
                            mockqtw.MockTreeWidget.setDropIndicatorShown)
        testobj = testee.VisualTree(parent)
        assert testobj._parent == parent
        assert capsys.readouterr().out == (
                "called Tree.__init__\n"
                "called Tree.setAcceptDrops with arg True\n"
                "called Tree.setDragEnabled with arg True\n"
                "called Tree.setSelectionMode\n"
                "called Tree.setDragDropMode with arg DragDropMode.InternalMove\n"
                "called Tree.setDropIndicatorShown with arg True\n")

    def test_mouseDoubleClickEvent(self, monkeypatch, capsys):
        """unittest for VisualTree.mouseDoubleClickEvent
        """
        def mock_itemat(*args):
            print('called VisualTree.itemAt with args', args)
            return None
        def mock_itemat_2(*args):
            print('called VisualTree.itemAt with args', args)
            return parent_top
        def mock_itemat_3(*args):
            print('called VisualTree.itemAt with args', args)
            return testitem
        def mock_event(self, arg):
            print(f"called TreeWidget.mouseDoubleClickEvent with arg '{arg}'")
        def mock_edit():
            print('called Editor.edit')
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mouseDoubleClickEvent', mock_event)
        parent_top = mockqtw.MockTreeItem('<> elm')
        testitem = mockqtw.MockTreeItem('att = value')
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('<> elm',)\n"
                                           "called TreeItem.__init__ with args ('att = value',)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemAt = mock_itemat
        testobj._parent.top = parent_top
        testobj._parent.editor.constants = {'ELSTART': '<>'}
        testobj._parent.editor.edit = mock_edit
        event = types.SimpleNamespace(position=lambda *x: types.SimpleNamespace(
            toPoint=lambda *x: (1, 2)))
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                f"called TreeWidget.mouseDoubleClickEvent with arg '{event}'\n")
        testobj.itemAt = mock_itemat_2
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                f"called TreeWidget.mouseDoubleClickEvent with arg '{event}'\n")
        testobj.itemAt = mock_itemat_3
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                "called TreeItem.text with arg 0\n"
                f"called TreeWidget.mouseDoubleClickEvent with arg '{event}'\n")
        testitem.setText(0, '<> ele')
        assert capsys.readouterr().out == "called TreeItem.setText with args (0, '<> ele')\n"
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == ("called VisualTree.itemAt with args ((1, 2),)\n"
                                           "called TreeItem.text with arg 0\n"
                                           "called TreeItem.childCount\n"
                                           "called Editor.edit\n")
        testitem.addChild(mockqtw.MockTreeItem('x'))
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('x',)\n"
                                           "called TreeItem.addChild\n")
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                "called TreeItem.text with arg 0\n"
                "called TreeItem.childCount\n"
                f"called TreeWidget.mouseDoubleClickEvent with arg '{event}'\n")

    def test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for VisualTree.mouseReleaseEvent
        """
        def mock_itemat(*args):
            print('called VisualTree.itemAt with args', args)
            return parent_top
        def mock_itemat_2(*args):
            print('called VisualTree.itemAt with args', args)
            return testitem
        def mock_event(self, arg):
            print(f"called TreeWidget.mouseReleaseEvent with arg '{arg}'")
        def mock_popup(arg):
            print(f'called Editor.popup with arg {arg}')
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mouseReleaseEvent', mock_event)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setCurrentItem',
                            mockqtw.MockTreeWidget.setCurrentItem)
        parent_top = mockqtw.MockTreeItem('<> elm')
        testitem = mockqtw.MockTreeItem('att = value')
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('<> elm',)\n"
                                           "called TreeItem.__init__ with args ('att = value',)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemAt = mock_itemat
        testobj._parent.popup_menu = mock_popup
        testobj._parent.top = parent_top
        # event = types.SimpleNamespace(x=lambda *i: 1, y=lambda *i: 2, button=lambda *x: 'button')
        event = types.SimpleNamespace(position=lambda *x: types.SimpleNamespace(
            toPoint=lambda *x: (1, 2)), button=lambda *x: 'button')
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == (
                f"called TreeWidget.mouseReleaseEvent with arg '{event}'\n")
        # event = types.SimpleNamespace(x=lambda *i: 1, y=lambda *i: 2,
        #                               button=lambda *x: testee.core.Qt.MouseButton.RightButton)
        event = types.SimpleNamespace(position=lambda *x: types.SimpleNamespace(
            toPoint=lambda *x: (1, 2)), button=lambda *x: testee.core.Qt.MouseButton.RightButton)
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                f"called TreeWidget.mouseReleaseEvent with arg '{event}'\n")
        testobj.itemAt = mock_itemat_2
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                f"called Tree.setCurrentItem with arg `{testitem}`\n"
                f"called Editor.popup with arg {testitem}\n")

    def test_dropEvent(self, monkeypatch, capsys):
        """unittest for VisualTree.dropEvent
        """
        def mock_itemat(*args):
            print('called VisualTree.itemAt with args', args)
            return None
        def mock_itemat_2(*args):
            print('called VisualTree.itemAt with args', args)
            return testitem
        def mock_event(self, arg):
            print(f"called TreeWidget.dropEvent with arg '{arg}'")
        def mock_selected(self):
            print('called Tree.selectedItems')
            return dragitem, ''
        def mock_show(*args):
            print('called show_message with args', args)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'dropEvent', mock_event)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setCurrentItem',
                            mockqtw.MockTreeWidget.setCurrentItem)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'selectedItems', mock_selected)
        monkeypatch.setattr(testee, 'show_message', mock_show)
        testitem = mockqtw.MockTreeItem('att = value')
        dropitem = mockqtw.MockTreeItem('x')
        dragitem = mockqtw.MockTreeItem('y')
        dropitem.addChild(dragitem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('att = value',)\n"
                                           "called TreeItem.__init__ with args ('x',)\n"
                                           "called TreeItem.__init__ with args ('y',)\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemAt = mock_itemat
        testobj._parent.editor.constants = {'ELSTART': '<>'}
        # event = types.SimpleNamespace(pos=lambda *i: (1, 2))
        event = types.SimpleNamespace(position=lambda *x: types.SimpleNamespace(
            toPoint=lambda *x: (1, 2)))
        testobj.dropEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                "called show_message with args"
                f" ({testobj._parent}, 'HtmlEditor', 'Can only drop on element')\n")
        testobj.itemAt = mock_itemat_2
        testobj.dropEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                "called TreeItem.text with arg 0\n"
                "called show_message with args"
                f" ({testobj._parent}, 'HtmlEditor', 'Can only drop on element')\n")
        testitem.setText(0, '<> ele')
        testobj.dropEvent(event)
        assert capsys.readouterr().out == (
                "called TreeItem.setText with args (0, '<> ele')\n"
                "called VisualTree.itemAt with args ((1, 2),)\n"
                "called TreeItem.text with arg 0\n"
                "called Tree.selectedItems\n"
                f"called TreeWidget.dropEvent with arg '{event}'\n"
                "called TreeItem.parent\n"
                f"called Tree.setCurrentItem with arg `{dragitem}`\n"
                "called TreeItem.setExpanded with arg `True`\n"
                "called Editor.mark_dirty with arg True\n"
                "called Editorrefresh_preview\n")


def test_show_message(monkeypatch, capsys):
    """unittest for qtgui.show_message
    """
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testee.show_message('parent', 'title', 'message')
    assert capsys.readouterr().out == (
            "called MessageBox.information with args `parent` `title` `message`\n")


def test_ask_yesnocancel(monkeypatch, capsys):
    """unittest for qtgui.ask_yesnocancel
    """
    def mock_ask(*args, **kwargs):
        print('called MessageBox.question with args', args, kwargs)
        return mockqtw.MockMessageBox.StandardButton.Yes
    def mock_ask_2(*args, **kwargs):
        print('called MessageBox.question with args', args, kwargs)
        return mockqtw.MockMessageBox.StandardButton.Cancel
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    assert testee.ask_yesnocancel('parent', 'prompt', 'title') == 0
    assert capsys.readouterr().out == (
            "called MessageBox.question with args `parent` `title` `prompt` `14` `4`\n")
    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask)
    assert testee.ask_yesnocancel('parent', 'prompt', 'title') == 1
    assert capsys.readouterr().out == (
            "called MessageBox.question with args"
            " ('parent', 'title', 'prompt', 14) {'defaultButton': 4}\n")
    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask_2)
    assert testee.ask_yesnocancel('parent', 'prompt', 'title') == -1
    assert capsys.readouterr().out == (
            "called MessageBox.question with args"
            " ('parent', 'title', 'prompt', 14) {'defaultButton': 4}\n")


def test_ask_for_text(monkeypatch, capsys):
    """unittest for qtgui.ask_for_text
    """
    def mock_get(parent, *args, **kwargs):
        print('called InputDialog.getText with args', parent, args, kwargs)
        return 'xxx', True
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    assert testee.ask_for_text('parent', 'title', 'caption') == ""
    assert capsys.readouterr().out == (
            "called InputDialog.getText with args parent ('title', 'caption') {}\n")
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getText', mock_get)
    assert testee.ask_for_text('parent', 'title', 'caption') == "xxx"
    assert capsys.readouterr().out == (
            "called InputDialog.getText with args parent ('title', 'caption') {}\n")


def test_call_dialog(monkeypatch, capsys):
    """unittest for qtgui.call_dialog
    """
    def mock_exec():
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Rejected
    def mock_exec_2():
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Accepted
    obj = types.SimpleNamespace(gui=types.SimpleNamespace(exec=mock_exec))
    obj.parent = types.SimpleNamespace(dialog_data="dialogdata")
    assert testee.call_dialog(obj) == (False, None)
    assert capsys.readouterr().out == "called Dialog.exec\n"
    obj.gui.exec = mock_exec_2
    assert testee.call_dialog(obj) == (True, 'dialogdata')
    assert capsys.readouterr().out == "called Dialog.exec\n"


def test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog
    """
    def mock_show():
        print('called Dialog.show')
    obj = types.SimpleNamespace(gui=types.SimpleNamespace(show=mock_show))
    testee.show_dialog(obj)
    assert capsys.readouterr().out == ("called Dialog.show\n")


def test_ask_for_save_filename(monkeypatch, capsys):
    """unittest for qtgui.ask_for_save_filename
    """
    monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
    assert testee.ask_for_save_filename('parent', 'loc', 'mask') == ""
    assert capsys.readouterr().out == ("called FileDialog.getSaveFileName with args"
                                       " parent ('Save file as ...', 'loc', 'mask') {}\n")


def test_ask_for_open_filename(monkeypatch, capsys):
    """unittest for qtgui.ask_for_open_filename
    """
    monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
    assert testee.ask_for_open_filename('parent', 'loc', 'mask') == ""
    assert capsys.readouterr().out == ("called FileDialog.getOpenFileName with args"
                                       " parent ('Choose a file', 'loc', 'mask') {}\n")


def test_build_mask(monkeypatch, capsys):
    """unittest for qtgui.build_mask
    """
    monkeypatch.setattr(testee, 'masks', {'all': ('all', 'All'), 'xxx': ('xxx', 'Xxx')})
    assert testee.build_mask('xxx') == "xxx (X x x X X X);;all (A)"
    assert capsys.readouterr().out == ("")


class TestEditDialogGui:
    """unittests for qtgui.EditDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.EditDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called EditDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.EditDialogGui, '__init__', mock_init)
        testobj = testee.EditDialogGui()
        assert capsys.readouterr().out == 'called EditDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditDialogGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.EditDialogGui('master', parent, 'title')
        assert testobj.parent == parent
        assert testobj.master == 'master'
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args namespace(appicon='icon') () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called Dialog.setWindowIcon with args ('icon',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_topline(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_topline
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.add_topline(), testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        topline = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_label(topline, 'text')
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n")

    def test_add_textinput(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_textinput
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        topline = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_textinput(topline, 'text', 'width'), testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                f"called LineEdit.__init__ with args ({testobj},)\n"
                "called LineEdit.setMinimumWidth with arg `width`\n"
                "called LineEdit.setText with arg `text`\n"
                "called HBox.addWidget with arg MockLineEdit\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_checkbox
        """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        topline = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_checkbox(topline, 'text', ''), testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                "called HBox.addWidget with arg MockCheckBox\n")
        assert isinstance(testobj.add_checkbox(topline, 'text', 'state'), testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                "called CheckBox.toggle\n"
                "called HBox.addWidget with arg MockCheckBox\n")

    def test_add_content_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_content_section
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.add_content_section(), testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called Frame.setFrameStyle with arg `32`\n"
                                           "called VBox.__init__\n"
                                           "called Frame.setLayout with arg MockVBoxLayout\n"
                                           "called VBox.addWidget with arg MockFrame\n")

    def test_add_table_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_table_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        section = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_to_section(section, [], {})
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setColumnCount with arg '2'\n"
                "called Table.setHorizontalHeaderLabels with arg '[]'\n"
                "called Table.horizontalHeader\n"
                "called Header.setStretchLastSection with arg True\n"
                "called Table.setTabKeyNavigation with arg False\n"
                "called HBox.addWidget with arg MockTable\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_table_to_section(section, [('column', 1), ('defs', 2)],
                                     {'x': 'y', 'style': 'z', 'styledata': 'q'})
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setColumnCount with arg '2'\n"
                "called Table.setHorizontalHeaderLabels with arg '['column', 'defs']'\n"
                "called Table.horizontalHeader\n"
                "called Header.resizeSection with args (0, 1)\n"
                "called Header.resizeSection with args (1, 2)\n"
                "called Header.setStretchLastSection with arg True\n"
                "called Table.setTabKeyNavigation with arg False\n"
                "called Table.rowCount\n"
                "called Table.insertRow with arg '0'\n"
                "called Table.setVerticalHeaderItem for row 0\n"
                "called Table.setItem with args (0, 0, QTableWidgetItem)\n"
                "called Table.setItem with args (0, 1, QTableWidgetItem)\n"
                "called Table.rowCount\ncalled Table.insertRow with arg '1'\n"
                "called Table.setVerticalHeaderItem for row 1\n"
                "called Table.setItem with args (1, 0, QTableWidgetItem)\n"
                "called Table.setItem with args (1, 1, QTableWidgetItem)\n"
                "called Table.rowCount\ncalled Table.insertRow with arg '2'\n"
                "called Table.setVerticalHeaderItem for row 2\n"
                "called Table.setItem with args (2, 0, QTableWidgetItem)\n"
                "called Table.setItem with args (2, 1, QTableWidgetItem)\n"
                "called HBox.addWidget with arg MockTable\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_buttons_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_buttons_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        section = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(style_text='qq')
        testobj.add_buttons_to_section(section, [])
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.master = types.SimpleNamespace(style_text='yy')
        testobj.add_buttons_to_section(section, [('xx', 'callback1'), ('yy', 'callback2')])
        assert isinstance(testobj.style_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback1',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback2',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_textinput_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_textinput_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        section = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_textinput_to_section(section, 'text', 'width', 'height')
        assert isinstance(result, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Editor.__init__ with args ({testobj},)\n"
                                           "called Editor.resize with args ('width', 'height')\n"
                                           "called Editor.setText with arg `text`\n"
                                           "called HBox.addWidget with arg MockEditorWidget\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_text_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_text_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        section = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text_to_section(section, 'text')
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('Select document type:', {testobj})\n"
                "called VBox.addWidget with arg MockLabel\n")

    def test_add_radiobutton_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_radiobutton_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        section = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_radiobutton_to_section(section, '', False, False)
        assert capsys.readouterr().out == "called VBox.addSpacing\n"
        result = testobj.add_radiobutton_to_section(section, 'text', True, False)
        assert isinstance(result, testee.qtw.QRadioButton)
        assert isinstance(testobj.grp, testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == (
                "called ButtonGroup.__init__ with args ()\n"
                f"called RadioButton.__init__ with args ('text', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called VBox.addWidget with arg MockRadioButton\n")
        result = testobj.add_radiobutton_to_section(section, 'text', False, True)
        assert isinstance(result, testee.qtw.QRadioButton)
        assert capsys.readouterr().out == (
                f"called RadioButton.__init__ with args ('text', {testobj}) {{}}\n"
                "called RadioButton.setChecked with arg `True`\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called VBox.addWidget with arg MockRadioButton\n")

    def test_add_buttons_to_bottom(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_buttons_to_bottom
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons_to_bottom()
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('&Save', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                "called PushButton.setDefault with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_focus_to
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Widget.setFocus\n"

    # def _test_on_add(self, monkeypatch, capsys):
    #     """unittest for EditDialogGui.on_add
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.on_add() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_on_del(self, monkeypatch, capsys):
    #     """unittest for EditDialogGui.on_del
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.on_del() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_on_style(self, monkeypatch, capsys):
    #     """unittest for EditDialogGui.on_style
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.on_style() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_refresh(self, monkeypatch, capsys):
    #     """unittest for EditDialogGui.refresh
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.refresh() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_get_radiobutton_state(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_radiobutton_state
        """
        rb = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_radiobutton_state(rb)
        assert capsys.readouterr().out == "called RadioButton.isChecked\n"

    def test_set_radiobutton_state(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_radiobutton_state
        """
        rb = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_radiobutton_state(rb, 'state')
        assert capsys.readouterr().out == "called RadioButton.setChecked with arg `state`\n"

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_textinput_value
        """
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textinput_value(field) == ""
        assert capsys.readouterr().out == "called LineEdit.text\n"

    def test_get_textarea_contents(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_textarea_contents
        """
        field = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textarea_contents(field) == "editor text"
        assert capsys.readouterr().out == "called Editor.toPlainText\n"

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_checkbox_state
        """
        field = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_checkbox_state(field)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_set_button_text(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_button_text
        """
        btn = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_button_text(btn, 'text')
        assert capsys.readouterr().out == "called PushButton.setText with arg `text`\n"

    def test_get_table_rowcount(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_table_rowcount
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_rowcount(table) == 0
        assert capsys.readouterr().out == "called Table.rowCount\n"

    def test_add_table_row(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_table_row
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_row(table, 'row')
        assert capsys.readouterr().out == "called Table.insertRow with arg 'row'\n"

    def test_add_table_rowitem(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_table_rowitem
        """
        class MockTableItem:
            def __init__(self, arg):
                print(f"called TableItem.__init__ with arg '{arg}'")
            def flags(self):
                print('called tableitem.flags')
                # return (testee.core.Qt.ItemFlag.ItemIsSelectable
                #         | testee.core.Qt.ItemFlag.ItemIsEditable)
                return testee.core.Qt.ItemFlag.ItemIsEditable
            def setFlags(self, value):
                print(f'called tableitem.setFlags with arg {value}')
        monkeypatch.setattr(testee.qtw, 'QTableWidgetItem', MockTableItem)
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_rowitem(table, 'row', 'col', 'text')
        assert capsys.readouterr().out == (
                "called TableItem.__init__ with arg 'text'\n"
                "called Table.setItem with args (row, col, MockTableItem)\n")
        testobj.add_table_rowitem(table, 'row', 'col', 'text', editable=False)
        assert capsys.readouterr().out == (
                "called TableItem.__init__ with arg 'text'\n"
                "called Table.setItem with args (row, col, MockTableItem)\n"
                "called tableitem.flags\n"
                "called tableitem.setFlags with arg ItemFlag.NoItemFlags\n")

    def test_delete_table_row(self, monkeypatch, capsys):
        """unittest for EditDialogGui.delete_table_row
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.delete_table_row(table, 'row')
        assert capsys.readouterr().out == "called Table.removeRow with arg 'row'\n"

    def test_set_table_rowheader(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_table_rowheader
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_table_rowheader(table, 'row', 'text')
        assert capsys.readouterr().out == "called Table.setVerticalHeaderItem for row row\n"

    def test_select_table_cell(self, monkeypatch, capsys):
        """unittest for EditDialogGui.select_table_cell
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_table_cell(table, 'row', 'col')
        assert capsys.readouterr().out == "called Table.setCurrentCell with args ('row', 'col')\n"

    def test_get_selected_table_row(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_selected_table_row
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_table_row(table) == 2
        assert capsys.readouterr().out == "called Table.currentRow\n"

    def test_get_tableitem_text(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_tableitem_text
        """
        def mock_text():
            print('called tableitem.text')
            return 'xxx'
        def mock_item(x, y):
            print(f"called Table.item with args ({x}, {y})")
            return types.SimpleNamespace(text=mock_text)
        table = mockqtw.MockTable()
        table.item = mock_item
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_tableitem_text(table, 'row', 'col') == "xxx"
        assert capsys.readouterr().out == ("called Table.item with args (row, col)\n"
                                           "called tableitem.text\n")

    def test_set_tableitem_text(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_tableitem_text
        """
        def mock_text(*args):
            print('called tableitem.setText with args', args)
        def mock_item(x, y):
            print(f"called Table.item with args ({x}, {y})")
            return types.SimpleNamespace(setText=mock_text)
        table = mockqtw.MockTable()
        table.item = mock_item
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_tableitem_text(table, 'row', 'col', 'text')
        assert capsys.readouterr().out == ("called Table.item with args (row, col)\n"
                                           "called tableitem.setText with args ('text',)\n")

    def test_reject(self, monkeypatch, capsys):
        """unittest for EditDialogGui.reject
        """
        def mock_reject(*args):
            print("called Dialog.reject")
        def mock_show(*args):
            print("called shoe_message with args", args)
        def mock_refresh():
            print("called EditDialog.refresh")
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mock_reject)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(old_styledata='xxx')
        testobj.refresh = mock_refresh
        testobj.reject()
        assert capsys.readouterr().out == "called Dialog.reject\n"
        testobj.master.styledata = 'yyy'
        testobj.reject()
        assert capsys.readouterr().out == (
                "called MessageBox.information with args"
                f" `{testobj}` `Let op` `bijbehorende style data is gewijzigd`\n"
                "called EditDialog.refresh\n")
        testobj.master.styledata = 'xxx'
        testobj.reject()
        assert capsys.readouterr().out == "called Dialog.reject\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for EditDialogGui.accept
        """
        def mock_accept(*args):
            print("called Dialog.accept")
        def mock_show(*args):
            print("called shoe_message with args", args)
        def mock_confirm():
            print("called DialogParent.confirm")
            return 'No luck'
        def mock_confirm_2():
            print("called DialogParent.confirm")
            return ''
        def mock_refresh():
            print("called EditDialog.refresh")
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.title = 'title'
        testobj.refresh = mock_refresh
        testobj.accept()
        assert capsys.readouterr().out == (
                "called DialogParent.confirm\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `No luck`\n")
        testobj.master.attr_table = 'xxx'
        testobj.accept()
        assert capsys.readouterr().out == (
                "called EditDialog.refresh\n"
                "called DialogParent.confirm\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `No luck`\n")
        testobj.master.confirm = mock_confirm_2
        testobj.accept()
        assert capsys.readouterr().out == (
                "called EditDialog.refresh\n"
                "called DialogParent.confirm\n"
                "called Dialog.accept\n")


class TestSearchDialogGui:
    """unittests for qtgui.SearchDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SearchDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called SearchDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SearchDialogGui, '__init__', mock_init)
        testobj = testee.SearchDialogGui()
        assert capsys.readouterr().out == 'called SearchDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        # monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.SearchDialogGui('master', parent, title="title")
        assert testobj.parent == parent
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args namespace(appicon='icon') () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                # "called Dialog.setWindowIcon with args ('icon',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_setup_container(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.setup_container
        """
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.setup_container(), testee.qtw.QGridLayout)
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called VBox.addLayout with arg MockGridLayout\n")

    def test_add_title(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_title
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_title(gsizer, 'text', 'row', 'col')
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at ('row', 'col', 1, 3)\n")

    def test_add_text(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_text
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text(gsizer, 'text', 'row', 'col')
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at ('row', 'col')\n")

    def test_add_lineinput(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_lineinput
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_lineinput(gsizer, 'row', 'col', 'callback')
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                f"called LineEdit.__init__ with args ({testobj},)\n"
                "called Signal.connect with args ('callback',)\n"
                "called Grid.addWidget with arg MockLineEdit at ('row', 'col')\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_checkbox
        """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_checkbox(gsizer, 'text', 'row', 'col')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockCheckBox at (5, 3, 1, 3)\n")

    def test_add_description(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_description
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.add_description(), testee.qtw.QLabel)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Label.__init__ with args ('', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                "called Label.setWordWrap with arg True\n")

    def test_add_buttons_to_bottom(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_buttons_to_bottom
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons_to_bottom()
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('&Ok', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                "called PushButton.setDefault with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_lineinput_value(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.set_lineinput_value
        """
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_lineinput_value(field, 'text')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `text`\n"

    def test_get_lineinput_value(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.get_lineinput_value
        """
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_lineinput_value(field) == ""
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_checkbox_state
        """
        field = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_checkbox_state(field)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.set_focus_to
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Widget.setFocus\n"

    def test_set_label_text(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.set_label_text
        """
        field = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_label_text(field, 'text')
        assert capsys.readouterr().out == "called Label.setText with arg `text`\n"

    def test_update_size(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.update_size
        """
        # not implemented

    def test_accept(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.accept
        """
        def mock_confirm():
            print('called DialogParent.confirm')
            return 'No search'
        def mock_confirm_2():
            print('called DialogParent.confirm')
            return 'No replace'
        def mock_confirm_3():
            print('called DialogParent.confirm')
            return ''
        def mock_set(*args):
            print('called SearchDialog.set_focus_to with args', args)
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to = mock_set
        testobj.parent = types.SimpleNamespace(title='title')
        testobj.txt_element = 'search'
        testobj.txt_element_replace = 'replace'
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == (
                "called DialogParent.confirm\n"
                f"called MessageBox.information with args `{testobj}` `title` `No search`\n"
                "called SearchDialog.set_focus_to with args ('search',)\n")
        testobj.master.confirm = mock_confirm_2
        testobj.accept()
        assert capsys.readouterr().out == (
                "called DialogParent.confirm\n"
                f"called MessageBox.information with args `{testobj}` `title` `No replace`\n"
                "called SearchDialog.set_focus_to with args ('replace',)\n")
        testobj.master.confirm = mock_confirm_3
        testobj.accept()
        assert capsys.readouterr().out == ("called DialogParent.confirm\n"
                                           "called Dialog.accept\n")


class TestAddDialogGui:
    """unittests for qtgui.AddDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.AddDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called AddDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.AddDialogGui, '__init__', mock_init)
        testobj = testee.AddDialogGui()
        assert capsys.readouterr().out == 'called AddDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AddDialogGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.AddDialogGui('master', parent, 'title')
        assert testobj.parent == parent
        assert testobj.master == 'master'
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args namespace(appicon='icon') () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called Dialog.setWindowIcon with args ('icon',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_content_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_content_section
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        assert isinstance(testobj.add_content_section(), testee.qtw.QGridLayout)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called Frame.setFrameStyle with arg `32`\n"
                                           "called Grid.__init__\n"
                                           "called Frame.setLayout with arg MockGridLayout\n"
                                           "called Grid.addWidget with arg MockFrame at ()\n")

    def test_add_text_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_text_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        section = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text_to_section(section, 'text', 'row', 'col')
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at ('row', 'col')\n")

    def test_add_textinput_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_textinput_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        section = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_textinput_to_section(section, 'row', 'col')
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                f"called LineEdit.__init__ with args ('', {testobj})\n"
                "called Grid.addWidget with arg MockLineEdit at ('row', 'col')\n")
        result = testobj.add_textinput_to_section(section, 'row', 'col', 'text', 'width', 'callback')
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                f"called LineEdit.__init__ with args ('text', {testobj})\n"
                "called LineEdit.setMinimumWidth with arg `width`\n"
                "called Signal.connect with args ('callback',)\n"
                "called Grid.addWidget with arg MockLineEdit at ('row', 'col')\n")

    def test_add_button_line_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_button_line_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        section = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(style_text='qq')
        assert testobj.add_button_line_to_section(section, 'row', []) == []
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.master = types.SimpleNamespace(style_text='yy')
        result = testobj.add_button_line_to_section(section, 'row', [('xx', 'callback1'),
                                                                     ('yy', 'callback2')])
        assert len(result) == 2
        assert isinstance(result[0], testee.qtw.QPushButton)
        assert isinstance(result[1], testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback1',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback2',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_spinbox_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_spinbox_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        section = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_spinbox_to_section(section, 'row', 'col')
        assert isinstance(result, testee.qtw.QSpinBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called SpinBox.__init__\n"
                "called SpinBox.setMaximum with arg '0'\n"
                "called SpinBox.setValue with arg '0'\n"
                "called HBox.addWidget with arg MockSpinBox\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 'col')\n")
        result = testobj.add_spinbox_to_section(section, 'row', 'col', 'max', 'start', 'callback')
        assert isinstance(result, testee.qtw.QSpinBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called SpinBox.__init__\n"
                "called SpinBox.setMaximum with arg 'max'\n"
                "called SpinBox.setValue with arg 'start'\n"
                "called Signal.connect with args ('callback',)\n"
                "called HBox.addWidget with arg MockSpinBox\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 'col')\n")

    def test_add_combobox_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_combobox_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        section = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_combobox_to_section(section, 'row', 'col', [])
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.addItems with arg []\n"
                "called Grid.addWidget with arg MockComboBox at ('row', 'col')\n")
        result = testobj.add_combobox_to_section(section, 'row', 'col', ['x', 'y'], 'callback')
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.addItems with arg ['x', 'y']\n"
                "called Signal.connect with args ('callback',)\n"
                "called Grid.addWidget with arg MockComboBox at ('row', 'col')\n")

    def test_add_checkbox_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_checkbox_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        section = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_checkbox_to_section(section, 'row', 'col', 'text')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                "called HBox.__init__\n"
                "called HBox.addWidget with arg MockCheckBox\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 'col')\n")
        result = testobj.add_checkbox_to_section(section, 'row', 'col', 'text', True, 'callback')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                "called CheckBox.setChecked with arg True\n"
                "called Signal.connect with args ('callback',)\n"
                "called HBox.__init__\n"
                "called HBox.addWidget with arg MockCheckBox\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 'col')\n")

    def test_add_table_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_table_to_section
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        section = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_to_section(section, 'row', 0, [])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setRowCount with arg '0'\n"
                "called Table.setColumnCount with arg '0'\n"
                "called Table.setHorizontalHeaderLabels with arg '[]'\n"
                "called Table.horizontalHeader\n"
                "called Table.verticalHeader\n"
                "called Header.setVisible with arg False\n"
                "called HBox.addWidget with arg MockTable\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 0, 1, 2)\n")
        testobj.add_table_to_section(section, 'row', 1, ['column', 'defs'], 'callback')
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setRowCount with arg '1'\n"
                "called Table.setColumnCount with arg '2'\n"
                "called Table.setHorizontalHeaderLabels with arg '['column', 'defs']'\n"
                "called Table.horizontalHeader\n"
                "called Header.setSectionsClickable with arg True\n"
                "called Signal.connect with args ('callback',)\n"
                "called Table.verticalHeader\n"
                "called Header.setVisible with arg False\n"
                "called HBox.addWidget with arg MockTable\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 0, 1, 2)\n")

    def test_add_buttons_to_bottom(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_buttons_to_bottom
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons_to_bottom()
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('&Save', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                "called PushButton.setDefault with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_buttons_to_bottom(extra=('name', 'callback'))
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('&Save', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                "called PushButton.setDefault with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('name', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for AddDialogGui.set_focus_to
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Widget.setFocus\n"

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_textinput_value
        """
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textinput_value(field) == ""
        assert capsys.readouterr().out == "called LineEdit.text\n"

    def test_set_textinput_value(self, monkeypatch, capsys):
        """unittest for AddDialogGui.set_textinput_value
        """
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textinput_value(field, 'value')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `value`\n"

    def test_get_conbobox_text(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_conbobox_text
        """
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_conbobox_text(cmb) == 'current text'
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_get_spinbox_value(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_spinbox_value
        """
        sb = mockqtw.MockSpinBox()
        assert capsys.readouterr().out == "called SpinBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_spinbox_value(sb) == 0
        assert capsys.readouterr().out == "called SpinBox.value\n"

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_checkbox_state
        """
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_checkbox_state(cb)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_get_table_columncount(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_table_columncount
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_columncount(table) == 0
        assert capsys.readouterr().out == "called Table.columnCount\n"

    def test_get_table_rowcount(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_table_rowcount
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_rowcount(table) == 0
        assert capsys.readouterr().out == "called Table.rowCount\n"

    def test_get_tablecell_itemtext(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_tablecell_itemtext
        """
        def mock_text():
            print('called tableitem.text')
            return 'xxx'
        def mock_item(x, y):
            print(f"called Table.item with args ({x}, {y})")
            return types.SimpleNamespace(text=mock_text)
        table = mockqtw.MockTable()
        table.item = mock_item
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_tablecell_itemtext(table, 'row', 'col') == "xxx"
        assert capsys.readouterr().out == ("called Table.item with args (row, col)\n"
                                           "called tableitem.text\n")

    def test_set_table_headers(self, monkeypatch, capsys):
        """unittest for AddDialogGui.set_table_headers
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_table_headers(table, ['xx', 'yy'], [10, 20])
        assert capsys.readouterr().out == (
                "called Table.horizontalHeader\n"
                "called Header.setHorizontalHeaderLabels with arg ['xx', 'yy']\n"
                "called Header.resizeSection with args (0, 10)\n"
                "called Header.resizeSection with args (1, 20)\n")

    def test_enable_table_header(self, monkeypatch, capsys):
        """unittest for AddDialogGui.enable_table_header
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_table_header(table, 'value')
        assert capsys.readouterr().out == ("called Table.horizontalHeader\n"
                                           "called Header.setVisible with arg value\n")

    def test_add_table_column(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_table_column
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_column(table, 'colno')
        assert capsys.readouterr().out == ("called Table.insertColumn with arg 'colno'\n")

    def test_add_table_row(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_table_row
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_row(table, 'row')
        assert capsys.readouterr().out == "called Table.insertRow with arg 'row'\n"

    def test_remove_table_column(self, monkeypatch, capsys):
        """unittest for AddDialogGui.remove_table_column
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_table_column(table, 'colno')
        assert capsys.readouterr().out == ("called Table.removeColumn with arg 'colno'\n")

    def test_remove_table_row(self, monkeypatch, capsys):
        """unittest for AddDialogGui.remove_table_row
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_table_row(table, 'row')
        assert capsys.readouterr().out == "called Table.removeRow with arg 'row'\n"

    def test_get_table_column(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_table_column
        """
        table = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_column('x', 'y') == "x"
        assert capsys.readouterr().out == ("")

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for AddDialogGui.enable_widget
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_widget(widget, 'value')
        assert capsys.readouterr().out == "called Widget.setEnabled with arg value\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for AddDialogGui.accept
        """
        def mock_accept(*args):
            print("called Dialog.accept")
        def mock_show(*args):
            print("called shoe_message with args", args)
        def mock_confirm():
            print("called DialogParent.confirm")
            return 'No luck'
        def mock_confirm_2():
            print("called DialogParent.confirm")
            return ''
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.title = 'title'
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == (
                "called DialogParent.confirm\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `No luck`\n")
        testobj.master.attr_table = 'xxx'
        testobj.accept()
        assert capsys.readouterr().out == (
                "called DialogParent.confirm\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `No luck`\n")
        testobj.master.confirm = mock_confirm_2
        testobj.accept()
        assert capsys.readouterr().out == (
                "called DialogParent.confirm\n"
                "called Dialog.accept\n")


class TestScrolledTextDialogGui:
    """unittests for qtgui.ScrolledTextDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.ScrolledTextDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called ScrolledTextDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.ScrolledTextDialogGui, '__init__', mock_init)
        testobj = testee.ScrolledTextDialogGui()
        assert capsys.readouterr().out == 'called ScrolledTextDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.ScrolledTextDialogGui('master', parent, 'title')
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args namespace(appicon='icon') () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called Dialog.setWindowIcon with args ('icon',)\n"
                "called Dialog.resize with args (600, 400)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_top_label(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.add_top_label
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_top_label('text')
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Label.__init__ with args ({testobj},)\n"
                "called Label.setText with arg `text`\n"
                "called HBox.addWidget with arg MockLabel\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_text_area(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.add_text_area
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.add_text_area(), testee.qtw.QTextEdit)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Editor.__init__ with args ({testobj},)\n"
                                           "called Editor.setReadOnly with arg `True`\n"
                                           "called HBox.addWidget with arg MockEditorWidget\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_bottom_buttons(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.add_bottom_buttons
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_bottom_buttons([('xx', 'callback1'), ('yy', 'callback2')])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback1',)\n"
                "called PushButton.setDefault with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback2',)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_textarea_contents(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.set_textarea_contents
        """
        textfield = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textarea_contents(textfield, 'data')
        assert capsys.readouterr().out == "called Editor.setPlainText with arg `data`\n"


class TestCodeViewDialogGui:
    """unittests for qtgui.CodeViewDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.CodeViewDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called CodeViewDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.CodeViewDialogGui, '__init__', mock_init)
        testobj = testee.CodeViewDialogGui()
        assert capsys.readouterr().out == 'called CodeViewDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.__init__
        """
        assert capsys.readouterr().out == ("")
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        # monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.CodeViewDialogGui('master', parent, 'title')
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args namespace(appicon='icon') () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                # "called Dialog.setWindowIcon with args ('icon',)\n"
                "called Dialog.resize with args (600, 400)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_top_message(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.add_top_message
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_top_message('text')
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_content_area(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.add_content_area
        """
        def mock_setup(arg):
            print(f'called CodeViewDialogGui.setup_text with arg {arg}')
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qsc, 'QsciScintilla', mockqtw.MockEditorWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.setup_text = mock_setup
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_content_area('data')
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Editor.__init__ with args ({testobj},)\n"
                f"called CodeViewDialogGui.setup_text with arg {result}\n"
                "called Editor.setText with arg `data`\n"
                "called Editor.setReadOnly with arg `True`\n"
                "called HBox.addWidget with arg MockEditorWidget\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_bottom_button(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.add_bottom_button
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_bottom_button()
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('&Done', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.close},)\n"
                "called PushButton.setDefault with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_setup_text(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.setup_text
        """
        class MockLexer:
            def __init__(self):
                print('called lexer.__init__')
            def __repr__(self):
                return 'HTML lezer'
            def setDefaultFont(self, font):
                print(f'called lexer.setDefaultFont with arg {font}')
        monkeypatch.setattr(testee.gui, 'QFont', mockqtw.MockFont)
        monkeypatch.setattr(testee.gui, 'QFontMetrics', mockqtw.MockFontMetrics)
        monkeypatch.setattr(testee.gui, 'QColor', mockqtw.MockColor)
        monkeypatch.setattr(testee.qsc, 'QsciLexerHTML', MockLexer)
        textfield = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.setup_text(textfield)
        assert capsys.readouterr().out == (
                "called Font.__init__\n"
                "called Font.setFamily\n"
                "called Font.setFixedPitch with arg `True`\n"
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
                "called lexer.__init__\n"
                f"called lexer.setDefaultFont with arg {result}\n"
                "called Editor.setLexer\n")
