"""unittests for ./ashe/gui_qt.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from ashe import gui_qt as testee
from unittests.output_fixtures import expected_output

class MockEditor:
    """stub for main.Editor object
    """
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
                "called TreeItem.text for col 0\n"
                f"called TreeWidget.mouseDoubleClickEvent with arg '{event}'\n")
        testitem.setText(0, '<> ele')
        assert capsys.readouterr().out == "called TreeItem.setText with arg `<> ele` for col 0\n"
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == ("called VisualTree.itemAt with args ((1, 2),)\n"
                                           "called TreeItem.text for col 0\n"
                                           "called Editor.edit\n")
        testitem.addChild(mockqtw.MockTreeItem('x'))
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('x',)\n"
                                           "called TreeItem.addChild\n")
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                "called TreeItem.text for col 0\n"
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
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'dropEvent', mock_event)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setCurrentItem',
                            mockqtw.MockTreeWidget.setCurrentItem)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'selectedItems', mock_selected)
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
                "called EditorGui.meld with arg 'Can only drop on element'\n")
        testobj.itemAt = mock_itemat_2
        testobj.dropEvent(event)
        assert capsys.readouterr().out == (
                "called VisualTree.itemAt with args ((1, 2),)\n"
                "called TreeItem.text for col 0\n"
                "called EditorGui.meld with arg 'Can only drop on element'\n")
        testitem.setText(0, '<> ele')
        testobj.dropEvent(event)
        assert capsys.readouterr().out == (
                "called TreeItem.setText with arg `<> ele` for col 0\n"
                "called VisualTree.itemAt with args ((1, 2),)\n"
                "called TreeItem.text for col 0\ncalled Tree.selectedItems\n"
                f"called TreeWidget.dropEvent with arg '{event}'\n"
                "called TreeItem.parent\n"
                f"called Tree.setCurrentItem with arg `{dragitem}`\n"
                "called TreeItem.setExpanded with arg `True`\n"
                "called Editor.mark_dirty with arg True\n"
                "called Editorrefresh_preview\n")


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
        # class MockTree:
        #     """stub for gui_qt.VisualTree
        #     """
        #     def __init__(self, arg):
        #         print(f'called VisualTree.__init__ with arg {arg}')
        def mock_init(self, *args):
            print('called MainWindow.__init__ with args', args)
        def mock_init_app(self, *args):
            print('called Application.__init__ with args', args)
        def mock_meld(self, message):
            print(f"called EditorGui.meld with arg '{message}'")
        def mock_setup_menu(self):
            print('called EditorGui.setup_menu')
            self.adv_menu = mockqtw.MockAction()
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowIcon',
                            mockqtw.MockMainWindow.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mockqtw.MockMainWindow.show)
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_init_app)
        monkeypatch.setattr(testee.EditorGui, 'meld', mock_meld)
        monkeypatch.setattr(testee.EditorGui, 'setup_menu', mock_setup_menu)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.qtw, 'QSplitter', mockqtw.MockSplitter)
        monkeypatch.setattr(testee, 'VisualTree', mockqtw.MockTreeWidget)
        monkeypatch.setattr(testee.webeng, 'QWebEngineView', mockqtw.MockWebEngineView)
        monkeypatch.setattr(testee.qtw, 'QStatusBar', mockqtw.MockStatusBar)
        monkeypatch.setattr(testee.sys, 'argv', ['aaa', 'bbb'])
        testobj = testee.EditorGui(err='xxx')
        assert testobj.parent is None
        assert testobj.editor is None
        assert capsys.readouterr().out == (
                "called Application.__init__ with args (['aaa', 'bbb'],)\n"
                "called MainWindow.__init__ with args ()\n"
                "called EditorGui.meld with arg 'xxx'\n")
        editor = MockEditor()
        editor.title = 'title'
        testobj = testee.EditorGui('parent', editor)
        assert testobj.parent == 'parent'
        assert testobj.editor == editor
        assert testobj.dialog_data == {}
        assert isinstance(testobj.appicon, testee.gui.QIcon)
        assert isinstance(testobj.pnl, testee.qtw.QSplitter)
        assert isinstance(testobj.tree, testee.VisualTree)
        assert isinstance(testobj.html, testee.webeng.QWebEngineView)
        assert isinstance(testobj.sb, mockqtw.MockStatusBar)
        assert isinstance(testobj.adv_menu, mockqtw.MockAction)
        assert capsys.readouterr().out == (
                "called Application.__init__ with args (['aaa', 'bbb'],)\n"
                "called MainWindow.__init__ with args ()\n"
                "called MainWindow.setWindowTitle with arg `title`\n"
                "called Icon.__init__ with arg `None`\n"
                "called MainWindow.setWindowIcon\n"
                "called MainWindow.resize with args (1200, 900)\n"
                "called EditorGui.setup_menu\ncalled Action.__init__ with args ()\n"
                "called Splitter.__init__\n"
                "called MainWidget.setCentralWindow with arg of type"
                " `<class 'mockgui.mockqtwidgets.MockSplitter'>`\n"
                "called Tree.__init__\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setHidden with arg `True`\n"
                f"called Splitter.addWidget with arg `{testobj.tree}`\n"
                "called WebEngineView.__init__()\n"
                f"called Splitter.addWidget with arg `{testobj.html}`\n"
                "called MainWindow.statusBar\n"
                "called StatusBar.__init__ with args ()\n"
                "called Tree.resize with args (500, 100)\n"
                "called Splitter.setSizes with args ([300, 900],)\n"
                "called Tree.setFocus\ncalled Action.setChecked with arg `True`\n"
                "called MainWindow.show\n")
        editor = MockEditor()
        editor.title = 'title'
        testobj = testee.EditorGui('parent', editor, icon='icon')
        assert testobj.parent == 'parent'
        assert testobj.editor == editor
        assert testobj.dialog_data == {}
        assert isinstance(testobj.appicon, testee.gui.QIcon)
        assert isinstance(testobj.pnl, testee.qtw.QSplitter)
        assert isinstance(testobj.tree, testee.VisualTree)
        assert isinstance(testobj.html, testee.webeng.QWebEngineView)
        assert isinstance(testobj.sb, mockqtw.MockStatusBar)
        assert isinstance(testobj.adv_menu, mockqtw.MockAction)
        assert capsys.readouterr().out == (
                "called Application.__init__ with args (['aaa', 'bbb'],)\n"
                "called MainWindow.__init__ with args ()\n"
                "called MainWindow.setWindowTitle with arg `title`\n"
                "called Icon.__init__ with arg `icon`\n"
                "called MainWindow.setWindowIcon\n"
                "called MainWindow.resize with args (1200, 900)\n"
                "called EditorGui.setup_menu\ncalled Action.__init__ with args ()\n"
                "called Splitter.__init__\n"
                "called MainWidget.setCentralWindow with arg of type"
                " `<class 'mockgui.mockqtwidgets.MockSplitter'>`\n"
                "called Tree.__init__\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setHidden with arg `True`\n"
                f"called Splitter.addWidget with arg `{testobj.tree}`\n"
                "called WebEngineView.__init__()\n"
                f"called Splitter.addWidget with arg `{testobj.html}`\n"
                "called MainWindow.statusBar\n"
                "called StatusBar.__init__ with args ()\n"
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

    def test_setup_menu(self, monkeypatch, capsys, expected_output):
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
        testobj.setup_menu()
        assert testobj.contextmenu_items == []
        # assert not hasattr(testobj, 'adv_menu')
        # assert not hasattr(testobj, 'dtd_menu')
        # assert not hasattr(testobj, 'css_menu')
        assert capsys.readouterr().out == ("called EditorGui.menuBar\n"
                                           "called Editor.get_menulist\n")

        testobj.editor.get_menulist = mock_get_2
        testobj.setup_menu()
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
        assert capsys.readouterr().out == "called TreeItem.text for col 0\n"

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
                "called TreeItem.setData to `yyy`"
                f" with role {testee.core.Qt.ItemDataRole.UserRole} for col 0\n")
        assert testobj.get_element_data(node) == "yyy"
        assert capsys.readouterr().out == (
                f"called TreeItem.data for col 0 role {testee.core.Qt.ItemDataRole.UserRole}\n")

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
        assert capsys.readouterr().out == ("called TreeItem.child with arg 0\n")

    def test_set_element_text(self, monkeypatch, capsys):
        """unittest for EditorGui.set_element_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('xxx')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx',)\n"
        testobj.set_element_text(node, 'text')
        assert capsys.readouterr().out == "called TreeItem.setText with arg `text` for col 0\n"

    def test_set_element_data(self, monkeypatch, capsys):
        """unittest for EditorGui.set_element_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('xxx')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx',)\n"
        testobj.set_element_data(node, 'data')
        assert capsys.readouterr().out == (
                "called TreeItem.setData to `data`"
                f" with role {testee.core.Qt.ItemDataRole.UserRole} for col 0\n")

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
                "called TreeItem.setText with arg `naam` for col 0\n"
                "called TreeItem.setData to `data` with role"
                f" {testee.core.Qt.ItemDataRole.UserRole} for col 0\n"
                "called TreeItem.addChild\n")
        result = testobj.addtreeitem(node, 'naam', 'data', 0)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setText with arg `naam` for col 0\n"
                "called TreeItem.setData to `data` with role"
                f" {testee.core.Qt.ItemDataRole.UserRole} for col 0\n"
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
                                           "called TreeItem.setText with arg `fname` for col 0\n"
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
        assert capsys.readouterr().out == "called Action.setText with arg `Add &DTD`\n"
        testobj.editor.has_dtd = True
        testobj.adjust_dtd_menu()
        assert capsys.readouterr().out == "called Action.setText with arg `Remove &DTD`\n"

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

    def test_build_mask(self, monkeypatch, capsys):
        """unittest for EditorGui.build_mask
        """
        monkeypatch.setattr(testee, 'masks', {'all': ('*', ['*.*']), 'xy': ('x+y', ['x', 'y'])})
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.os, 'name', 'not posix')
        assert testobj.build_mask('xy') == "x+y (x y);;* (*.*)"
        monkeypatch.setattr(testee.os, 'name', 'posix')
        assert testobj.build_mask('xy') == "x+y (x y X Y);;* (*.*)"

    def test_ask_for_open_filename(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_for_open_filename
        """
        monkeypatch.setattr(testee.os, 'getcwd', lambda: 'xxx')
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.build_mask = lambda x: [f'*.{x}', 'x']
        testobj.editor.xmlfn = ''
        assert testobj.ask_for_open_filename() == ""
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args {testobj}"
                " ('Choose a file', 'xxx', ['*.html', 'x']) {}\n")
        testobj.editor.xmlfn = 'yyy'
        assert testobj.ask_for_open_filename() == ""
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args {testobj}"
                " ('Choose a file', 'yyy', ['*.html', 'x']) {}\n")

    def test_ask_for_save_filename(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_for_save_filename
        """
        monkeypatch.setattr(testee.os, 'getcwd', lambda: 'xxx')
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.build_mask = lambda x: [f'*.{x}', 'x']
        testobj.editor.xmlfn = ''
        assert testobj.ask_for_save_filename() == ""
        assert capsys.readouterr().out == (
                f"called FileDialog.getSaveFileName with args {testobj}"
                " ('Save file as ...', 'xxx', ['*.html', 'x']) {}\n")
        testobj.editor.xmlfn = 'yyy'
        assert testobj.ask_for_save_filename() == ""
        assert capsys.readouterr().out == (
                f"called FileDialog.getSaveFileName with args {testobj}"
                " ('Save file as ...', 'yyy', ['*.html', 'x']) {}\n")

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
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.setExpanded with arg `True`\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.setExpanded with arg `True`\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.setExpanded with arg `True`\n"
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
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.setExpanded with arg `False`\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.child with arg 0\n"
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

    def test_call_dialog(self, monkeypatch, capsys):
        """unittest for EditorGui.call_dialog
        """
        def mock_exec(self):
            print('called Dialog.exec')
            return testee.qtw.QDialog.DialogCode.Accepted
        testobj = self.setup_testobj(monkeypatch, capsys)
        obj = mockqtw.MockDialog()
        assert capsys.readouterr().out == "called Dialog.__init__ with args None () {}\n"
        testobj.dialog_data = {'x': 'y'}
        assert testobj.call_dialog(obj) == (False, None)
        assert capsys.readouterr().out == ("called Dialog.exec\n")
        monkeypatch.setattr(mockqtw.MockDialog, 'exec', mock_exec)
        assert testobj.call_dialog(obj) == (True, {'x': 'y'})
        assert capsys.readouterr().out == ("called Dialog.exec\n")

    def test_do_edit_element(self, monkeypatch, capsys):
        """unittest for EditorGui.do_edit_element
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called ElementDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'ElementDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.do_edit_element('tagdata', 'attrdict')
        assert isinstance(result, testee.ElementDialog)
        assert capsys.readouterr().out == (
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'Edit an element', 'tag': 'tagdata', 'attrs': 'attrdict'}\n"
                "called EditorGui.call_dialog\n")

    def test_do_add_element(self, monkeypatch, capsys):
        """unittest for EditorGui.do_add_element
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called ElementDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'ElementDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.do_add_element('where')
        assert isinstance(result, testee.ElementDialog)
        assert capsys.readouterr().out == (
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert where)'}\n"
                "called EditorGui.call_dialog\n")

    def test_do_edit_textvalue(self, monkeypatch, capsys):
        """unittest for EditorGui.do_edit_textvalue
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called TextDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'TextDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.do_edit_textvalue('textdata')
        assert isinstance(result, testee.TextDialog)
        assert capsys.readouterr().out == (
                f"called TextDialog.__init__ with args ({testobj},)"
                " {'title': 'Edit Text', 'text': 'textdata'}\n"
                "called EditorGui.call_dialog\n")

    def test_do_add_textvalue(self, monkeypatch, capsys):
        """unittest for EditorGui.do_add_textvalue
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called TextDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'TextDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.do_add_textvalue()
        assert isinstance(result, testee.TextDialog)
        assert capsys.readouterr().out == (
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called EditorGui.call_dialog\n")

    def test_do_delete_item(self, monkeypatch, capsys):
        """unittest for EditorGui.do_delete_item
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
        testobj.do_delete_item(item2)
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.indexOfChild\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.removeChild\n")

    def test_do_delete_item_2(self, monkeypatch, capsys):
        """unittest for EditorGui.do_delete_item
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

    def test_do_delete_item_3(self, monkeypatch, capsys):
        """unittest for EditorGui.do_delete_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent = mockqtw.MockTreeItem('root')
        testobj.editor.root = mockqtw.MockTreeItem('parent')
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

    def test_get_search_args(self, monkeypatch, capsys):
        """unittest for EditorGui.get_search_args
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called SearchDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'SearchDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_search_args()
        assert isinstance(result, testee.SearchDialog)
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search options', False) {{}}\n"
                "called EditorGui.call_dialog\n")
        result = testobj.get_search_args(replace=True)
        assert isinstance(result, testee.SearchDialog)
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search options', True) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_meld(self, monkeypatch, capsys):
        """unittest for EditorGui.meld
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.title = 'title'
        testobj.meld('text')
        assert testobj.in_dialog
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

    def test_get_dtd(self, monkeypatch, capsys):
        """unittest for EditorGui.get_dtd
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called DtdDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'DtdDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_dtd()
        assert isinstance(result, testee.DtdDialog)
        assert capsys.readouterr().out == (
                f"called DtdDialog.__init__ with args ({testobj},) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_get_css_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_css_data
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called CssDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'CssDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_css_data()
        assert isinstance(result, testee.CssDialog)
        assert capsys.readouterr().out == (
                f"called CssDialog.__init__ with args ({testobj},) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_get_link_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_link_data
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called LinkDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'LinkDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_link_data()
        assert isinstance(result, testee.LinkDialog)
        assert capsys.readouterr().out == (
                f"called LinkDialog.__init__ with args ({testobj},) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_get_image_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_image_data
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called ImageDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'ImageDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_image_data()
        assert isinstance(result, testee.ImageDialog)
        assert capsys.readouterr().out == (
                f"called ImageDialog.__init__ with args ({testobj},) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_get_video_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_video_data
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called VideoDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'VideoDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_video_data()
        assert isinstance(result, testee.VideoDialog)
        assert capsys.readouterr().out == (
                f"called VideoDialog.__init__ with args ({testobj},) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_get_audio_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_audio_data
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called AudioDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'AudioDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_audio_data()
        assert isinstance(result, testee.AudioDialog)
        assert capsys.readouterr().out == (
                f"called AudioDialog.__init__ with args ({testobj},) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_get_list_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_list_data
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called ListDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'ListDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_list_data()
        assert isinstance(result, testee.ListDialog)
        assert capsys.readouterr().out == (
                f"called ListDialog.__init__ with args ({testobj},) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_get_table_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_table_data
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called TableDialog.__init__ with args', args, kwargs)
        def mock_call(arg):
            print('called EditorGui.call_dialog')
            return arg  # dit is niet wat er in de testee uitkomt
                        # maar bedoeld om het argument te verifiëren
        monkeypatch.setattr(testee, 'TableDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_dialog = mock_call
        result = testobj.get_table_data()
        assert isinstance(result, testee.TableDialog)
        assert capsys.readouterr().out == (
                f"called TableDialog.__init__ with args ({testobj},) {{}}\n"
                "called EditorGui.call_dialog\n")

    def test_validate(self, monkeypatch, capsys):
        """unittest for EditorGui.validate
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called ScrolledTextDialog.__init__ with args', args, kwargs)
            def show(self):
                print('called ScrolledTextDialog.show')
        monkeypatch.setattr(testee, 'ScrolledTextDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.validate('htmlfile', 'fromdisk')
        assert capsys.readouterr().out == (
                f"called ScrolledTextDialog.__init__ with args ({testobj}, 'Validation output')"
                " {'htmlfile': 'htmlfile', 'fromdisk': 'fromdisk'}\n"
                "called ScrolledTextDialog.show\n")

    def test_show_code(self, monkeypatch, capsys):
        """unittest for EditorGui.show_code
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called CodeViewDialog.__init__ with args', args, kwargs)
            def show(self):
                print('called CodeViewDialog.show')
        monkeypatch.setattr(testee, 'CodeViewDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show_code('title', 'caption', 'data')
        assert capsys.readouterr().out == (
                f"called CodeViewDialog.__init__ with args ({testobj},"
                " 'title', 'caption', 'data') {}\n"
                "called CodeViewDialog.show\n")
