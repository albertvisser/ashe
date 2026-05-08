"""unittests for ./ashe/wxgui.py
"""
import types
# import pytest
from ashe import wxgui as testee
from mockgui import mockwxwidgets as mockwx


class TestEditorGui:
    """unittest for gui_wx.EditorGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.EditorGui object

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
        assert capsys.readouterr().out == 'called EditorGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditorGui.__init__
        """
        class MockDisplay:
            def __init__(self):
                print('called display.__init__')
            def GetClientArea(self):
                print('called display.GetClientArea')
                return types.SimpleNamespace(height=dspheight, width=dspwidth)
        def mock_init(self, *args, **kwargs):
            print('called Frame.__init__ with args', args, kwargs)
        def mock_meld(*args):
            print('called EditorGui.meld with args', args)
        def mock_set(*args):
            print('called EditorGui.SetIcon with args', args)
        dspheight = 899
        dspwidth = 1019
        monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        monkeypatch.setattr(testee.wx, 'Display', MockDisplay)
        monkeypatch.setattr(testee.wx.Frame, '__init__', mock_init)
        monkeypatch.setattr(testee.wx.Frame, 'SetIcon', mock_set)
        monkeypatch.setattr(testee.EditorGui, 'meld', mock_meld)
        testobj = testee.EditorGui('editor', 'title', 'icon')
        assert testobj.editor == 'editor'
        assert isinstance(testobj.app, testee.wx.App)
        assert testobj.dialog_data == {}
        assert testobj.search_args == []
        assert capsys.readouterr().out == (
                "called app.__init__ with args ()\n"
                "called display.__init__\n"
                "called display.GetClientArea\n"
                "called Frame.__init__ with args"
                " () {'parent': None, 'title': 'title', 'size': (1019, 899), 'style': 541072960}\n"
                "called Icon.__init__ with args ('icon', 3)\n"
                f"called EditorGui.SetIcon with args ({testobj}, Icon created from 'icon')\n")
        dspheight = 901
        dspwidth = 1021
        monkeypatch.setattr(testee.wx, 'Display', MockDisplay)
        testobj = testee.EditorGui('editor', 'title', 'icon')
        assert testobj.editor == 'editor'
        assert isinstance(testobj.app, testee.wx.App)
        assert testobj.dialog_data == {}
        assert testobj.search_args == []
        assert isinstance(testobj.appicon, testee.wx.Icon)
        assert capsys.readouterr().out == (
                "called app.__init__ with args ()\n"
                "called display.__init__\n"
                "called display.GetClientArea\n"
                "called Frame.__init__ with args"
                " () {'parent': None, 'title': 'title', 'size': (1020, 900), 'style': 541072960}\n"
                "called Icon.__init__ with args ('icon', 3)\n"
                f"called EditorGui.SetIcon with args ({testobj}, Icon created from 'icon')\n")

    def test_create_nemu(self, monkeypatch, capsys):
        """unittest for EditorGui.create_menu
        """
    #     def mock_setup():
    #         print('called EditorGui,setup_menu')
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.setup_menu = mock_setup
    #     testobj.create_menu()
    #     assert not testobj.in_contextmenu
    #     assert capsys.readouterr().out == "called EditorGui,setup_menu\n"
    # def _test_setup_menu(self, monkeypatch, capsys):
    #     """unittest for EditorGui.setup_menu
    #     """
        def mock_get():
            print('called Editor.get_menulist')
            return []
        def mock_get_2():
            print('called Editor.get_menulist')
            return [('xxx', []), ('&Edit', [('aa', 'A', 'A', 'aaaaaa', 'callback1'),
                                            ('bb', 'B', '', 'bbbbbb', 'callback2'),
                                            ('cc', 'C', 'C', 'cccccc', 'callback3')]),
                    ('&View', [('Advance selection...', '', '', 'xxx', 'callback4'),
                               ('qq', 'Q', 'C', 'qqqq', 'callback0')]),
                    ('&Search', [('',)]),
                    ('&HTML', [('Add &DTD', 'D', 'ACS', 'ddddd', 'callback5'),
                               ('Add &Stylesheet', 'E', 'SCA', 'eeeee', 'callback6')])]
        monkeypatch.setattr(testee.wx, 'MenuBar', mockwx.MockMenuBar)
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        monkeypatch.setattr(testee.wx.Frame, 'SetMenuBar', mockwx.MockFrame.SetMenuBar)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(get_menulist=mock_get)
        testobj.create_menu()
        assert testobj.contextmenu_items == []
        # assert isinstance(testobj.adv_menu, testee.wx.MenuItem)
        # assert isinstance(testobj.dtd_menu, testee.wx.MenuItem)
        # assert isinstance(testobj.css_menu, testee.wx.MenuItem)
        # assert testobj.css_menu_text == 'Add &Stylesheet'
        assert capsys.readouterr().out == ("called MenuBar.__init__ with args ()\n"
                                           "called Editor.get_menulist\n"
                                           "called Frame.SetMenuBar with args (A MenuBar,)\n")
        testobj.editor.get_menulist = mock_get_2
        testobj.create_menu()
        assert testobj.contextmenu_items == [('M', '&Edit'), ('A', ('aa', 'callback1', 'aaaaaa')),
                                             ('A', ('bb', 'callback2', 'bbbbbb')),
                                             ('A', ('cc', 'callback3', 'cccccc')),
                                             ('', ''), ('A', ('qq', 'callback0', 'qqqq')),
                                             ('M', '&Search'), ('M', '&HTML')]
        assert isinstance(testobj.adv_menu, testee.wx.MenuItem)
        assert isinstance(testobj.dtd_menu, testee.wx.MenuItem)
        assert isinstance(testobj.css_menu, testee.wx.MenuItem)
        assert testobj.css_menu_text == 'Add &Stylesheet'
        assert capsys.readouterr().out == (
                "called MenuBar.__init__ with args ()\n"
                "called Editor.get_menulist\n"
                "called Menu.__init__ with args ()\n"
                "called menubar.Append with args (A Menu, 'xxx')\n"
                "called Menu.__init__ with args ()\n"
                "called MenuItem.__init__ with args (A Menu, -1, 'aa\\tAlt+A', 'aaaaaa') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback1')\n"
                "called menu.Append with args MockMenuItem\n"
                "called MenuItem.__init__ with args (A Menu, -1, 'bb\\tB', 'bbbbbb') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback2')\n"
                "called menu.Append with args MockMenuItem\n"
                "called MenuItem.__init__ with args (A Menu, -1, 'cc\\tCtrl+C', 'cccccc') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback3')\n"
                "called menu.Append with args MockMenuItem\n"
                "called menubar.Append with args (A Menu, '&Edit')\n"
                "called Menu.__init__ with args ()\n"
                "called MenuItem.__init__ with args"
                " (A Menu, -1, 'Advance selection...', 'xxx', 1) {}\n"
                "called menu.Append with args MockMenuItem\n"
                "called MenuItem.__init__ with args (A Menu, -1, 'qq\\tCtrl+Q', 'qqqq') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback0')\n"
                "called menu.Append with args MockMenuItem\n"
                "called menubar.Append with args (A Menu, '&View')\n"
                "called Menu.__init__ with args ()\n"
                "called menu.AppendSeparator with args ()\n"
                "called menubar.Append with args (A Menu, '&Search')\n"
                "called Menu.__init__ with args ()\n"
                "called MenuItem.__init__ with args"
                " (A Menu, -1, 'Add &DTD\\tShift+Ctrl+Alt+D', 'ddddd') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback5')\n"
                "called menu.Append with args MockMenuItem\n"
                "called MenuItem.__init__ with args"
                " (A Menu, -1, 'Add &Stylesheet\\tShift+Ctrl+Alt+E', 'eeeee') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback6')\n"
                "called menu.Append with args MockMenuItem\n"
                "called menubar.Append with args (A Menu, '&HTML')\n"
                "called Frame.SetMenuBar with args (A MenuBar,)\n")

    def test_create_splitter(self, monkeypatch, capsys):
        """unittest for EditorGui.create_splitter
        """
        monkeypatch.setattr(testee.wx, 'SplitterWindow', mockwx.MockSplitter)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_splitter()
        assert capsys.readouterr().out == (f"called Splitter.__init__ with args ({testobj},) {{}}\n"
                                           "called splitter.SetMinimumPaneSize with args (1,)\n")

    def test_create_tree_on_left(self, monkeypatch, capsys):
        """unittest for EditorGui.create_tree_on_left
        """
        monkeypatch.setattr(testee, 'VisualTree', mockwx.MockTree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__ with args () {}\n"
        testobj.create_tree_on_left()
        assert isinstance(testobj.tree, testee.VisualTree)
        assert capsys.readouterr().out == f"called Tree.__init__ with args ({testobj.pnl},) {{}}\n"

    def test_create_preview_on_right(self, monkeypatch, capsys):
        """unittest for EditorGui.create_preview_on_right
        """
        monkeypatch.setattr(testee.wxhtml, 'WebView', mockwx.MockWebView)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__ with args () {}\n"
        testobj.create_preview_on_right()
        assert isinstance(testobj.html, mockwx.MockWebView)
        assert capsys.readouterr().out == "called WebView.New\n"

    def test_create_statusbar_at_bottom(self, monkeypatch, capsys):
        """unittest for EditorGui.create_statusbar_at_bottom
        """
        monkeypatch.setattr(testee.wx, 'StatusBar', mockwx.MockStatusBar)
        monkeypatch.setattr(testee.wx.Frame, 'SetStatusBar', mockwx.MockFrame.SetStatusBar)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_statusbar_at_bottom()
        assert isinstance(testobj.sb, testee.wx.StatusBar)
        assert capsys.readouterr().out == (
          f"called StatusBar.__init__ with args ({testobj},)\n"
          f"called Frame.GetStatusBar with args ({testobj.sb},)\n")

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for EditorGui.create_finalize_display
        """
        monkeypatch.setattr(testee.wx.Frame, 'Show', mockwx.MockFrame.Show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockSplitter()
        testobj.tree = mockwx.MockTree()
        testobj.html = mockwx.MockWebView().New()
        testobj.adv_menu = mockwx.MockMenuItem()
        assert capsys.readouterr().out == ("called Splitter.__init__ with args () {}\n"
                                           "called Tree.__init__ with args () {}\n"
                                           "called WebView.New\n"
                                           "called MenuItem.__init__ with args () {}\n")
        testobj.finalize_display()
        assert capsys.readouterr().out == (
                f"called splitter.SplitVertically with args ({testobj.tree}, {testobj.html})\n"
                "called splitter.SetSashPosition with args (400, True)\n"
                "called tree.SetFocus\n"
                "called menuitem.Check with arg True\n"
                "called frame.Show with args (True,)\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for EditorGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockwx.MockApp()
        assert capsys.readouterr().out == "called app.__init__ with args ()\n"
        testobj.go()
        assert capsys.readouterr().out == "called app.MainLoop\n"

    def test_close(self, monkeypatch, capsys):
        """unittest for EditorGui.close
        """
        monkeypatch.setattr(testee.wx.Frame, 'Close', mockwx.MockFrame.Close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close()
        assert capsys.readouterr().out == "called Frame.Close with arg False\n"

    def test_get_screen_title(self, monkeypatch, capsys):
        """unittest for EditorGui.get_screen_title
        """
        monkeypatch.setattr(testee.wx.Frame, 'GetTitle', mockwx.MockFrame.GetTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_screen_title() == "frame title"
        assert capsys.readouterr().out == "called Frame.GetTitle with args ()\n"

    def test_set_screen_title(self, monkeypatch, capsys):
        """unittest for EditorGui.set_screen_title
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetTitle', mockwx.MockFrame.SetTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_screen_title('title')
        assert capsys.readouterr().out == ("called Frame.SetTitle with args ('title',)\n")

    def test_get_element_text(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.get_element_text('node') == "itemtext"
        assert capsys.readouterr().out == "called tree.GetItemText with args ('node',)\n"

    def test_get_element_parent(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_parent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.get_element_parent('node') == "parent"
        assert capsys.readouterr().out == "called tree.GetItemParent with args ('node',)\n"

    def test_get_element_parentpos(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_parentpos
        """
        def mock_getp(*args):
            print('called tree.GetItemParent with args', args)
            return parent_item
        def mock_getf(*args):
            print('called tree.GetFirstChild with args', args)
            return first_item, 0
        def mock_getn(*args):
            print('called tree.GetNextChild with args', args)
            if args[1] == 0 :
                return next_item, 1
            return no_item, -1
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        parent_item = mockwx.MockTreeItem('parent')
        first_item = mockwx.MockTreeItem('first')
        next_item = mockwx.MockTreeItem('next')
        no_item = mockwx.MockTreeItem('not ok')
        assert capsys.readouterr().out == ("called Tree.__init__ with args () {}\n"
                                           "called TreeItem.__init__ with args ('parent',)\n"
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('next',)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n")
        testobj.tree.GetItemParent = mock_getp
        testobj.tree.GetFirstChild = mock_getf
        testobj.tree.GetNextChild = mock_getn
        assert testobj.get_element_parentpos(first_item) == (parent_item, 0)
        assert capsys.readouterr().out == (
                f"called tree.GetItemParent with args ({first_item},)\n"
                f"called tree.GetFirstChild with args ({parent_item},)\n"
                "called TreeItem.IsOk\n")
        assert testobj.get_element_parentpos(next_item) == (parent_item, 1)
        assert capsys.readouterr().out == (
                f"called tree.GetItemParent with args ({next_item},)\n"
                f"called tree.GetFirstChild with args ({parent_item},)\n"
                "called TreeItem.IsOk\n"
                f"called tree.GetNextChild with args ({parent_item}, 0)\n"
                "called TreeItem.IsOk\n")
        assert testobj.get_element_parentpos(no_item) == (None, -1)
        assert capsys.readouterr().out == (
                f"called tree.GetItemParent with args ({no_item},)\n"
                f"called tree.GetFirstChild with args ({parent_item},)\n"
                "called TreeItem.IsOk\n"
                f"called tree.GetNextChild with args ({parent_item}, 0)\n"
                "called TreeItem.IsOk\n"
                f"called tree.GetNextChild with args ({parent_item}, 1)\n"
                "called TreeItem.IsOk\n")

    def test_get_element_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.get_element_data('node') == "itemdata"
        assert capsys.readouterr().out == "called tree.GetItemData with args ('node',)\n"

    def test_get_element_children(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_children
        """
        def mock_getf(*args):
            print('called tree.GetFirstChild with args', args)
            return first_item, 0
        def mock_getn(*args):
            print('called tree.GetNextChild with args', args)
            if args[1] == 0 :
                return next_item, 1
            return no_item, -1
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        first_item = mockwx.MockTreeItem('first')
        next_item = mockwx.MockTreeItem('next')
        no_item = mockwx.MockTreeItem('not ok')
        assert capsys.readouterr().out == ("called Tree.__init__ with args () {}\n"
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('next',)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n")
        testobj.tree.GetFirstChild = mock_getf
        testobj.tree.GetNextChild = mock_getn
        assert testobj.get_element_children('node') == [first_item, next_item]
        assert capsys.readouterr().out == (
                "called tree.GetFirstChild with args ('node',)\n"
                "called TreeItem.IsOk\n"
                "called tree.GetNextChild with args ('node', 0)\n"
                "called TreeItem.IsOk\n"
                "called tree.GetNextChild with args ('node', 1)\n"
                "called TreeItem.IsOk\n")

    def test_set_element_text(self, monkeypatch, capsys):
        """unittest for EditorGui.set_element_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.set_element_text('node', 'text')
        assert capsys.readouterr().out == "called tree.SetItemText with args ('node', 'text')\n"

    def test_set_element_data(self, monkeypatch, capsys):
        """unittest for EditorGui.set_element_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.set_element_data('node', 'data')
        assert capsys.readouterr().out == "called tree.SetItemData() with args ('node', 'data')\n"

    def test_addtreeitem(self, monkeypatch, capsys):
        """unittest for EditorGui.addtreeitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.addtreeitem('node', 'naam', 'data') == 'appended item'
        assert capsys.readouterr().out == (
                "called tree.AppendItem with args ('node', 'naam')\n"
                "called tree.SetItemData() with args ('appended item', 'data')\n")
        assert testobj.addtreeitem('node', 'naam', 'data', 1) == 'inserted item'
        assert capsys.readouterr().out == (
                "called tree.InsertItem with args ('node', 1, 'naam')\n"
                "called tree.SetItemData() with args ('inserted item', 'data')\n")

    def test_addtreetop(self, monkeypatch, capsys):
        """unittest for EditorGui.addtreetop
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetTitle', mockwx.MockFrame.SetTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.addtreetop('fname', 'titel')
        assert capsys.readouterr().out == ("called Frame.SetTitle with args ('titel',)\n"
                                           "called tree.DeleteAllItems\n"
                                           "called tree.AddRoot with args ('fname',)\n")

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for EditorGui.get_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.get_selected_item() == "selection"
        assert capsys.readouterr().out == "called tree.GetSelection\n"

    def test_set_selected_item(self, monkeypatch, capsys):
        """unittest for EditorGui.set_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.set_selected_item('item')
        assert capsys.readouterr().out == (# "called tree.GetItemText with args ('item',)\n"
                                           # "in gui.set_selected_item, item is item itemtext\n"
                                           "called tree.SelectItem with args ('item',)\n")

    def test_init_tree(self, monkeypatch, capsys):
        """unittest for EditorGui.init_tree
        """
        def mock_set(*args):
            print('called EditorGui.set_selected_item with args', args)
        def mock_show(*args):
            print('called EditorGui.show_statusbar_message with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.top = 'topitem'
        testobj.set_selected_item = mock_set
        testobj.show_statusbar_message = mock_show
        testobj.adv_menu = mockwx.MockMenuItem()
        assert capsys.readouterr().out == "called MenuItem.__init__ with args () {}\n"
        testobj.init_tree('message')
        assert capsys.readouterr().out == (
                "called EditorGui.set_selected_item with args ('topitem',)\n"
                "called menuitem.Check with arg True\n"
                "called EditorGui.show_statusbar_message with args ('message',)\n")

    def test_show_statusbar_message(self, monkeypatch, capsys):
        """unittest for EditorGui.show_statusbar_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sb = mockwx.MockStatusBar()
        assert capsys.readouterr().out == "called StatusBar.__init__ with args ()\n"
        testobj.show_statusbar_message('text')
        assert capsys.readouterr().out == "called statusbar.SetStatusText with args ('text',)\n"

    def test_adjust_dtd_menu(self, monkeypatch, capsys):
        """unittest for EditorGui.adjust_dtd_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.dtd_menu = mockwx.MockMenuItem()
        assert capsys.readouterr().out == "called MenuItem.__init__ with args () {}\n"
        testobj.editor = types.SimpleNamespace(has_dtd=False)
        testobj.adjust_dtd_menu()
        assert capsys.readouterr().out == (
                "called menuitem.SetItemLabel with arg 'Add &DTD'\n"
                "called menuitem.SetHelp with arg 'Add a document type declaration'\n")
        testobj.editor.has_dtd = True
        testobj.adjust_dtd_menu()
        assert capsys.readouterr().out == (
                "called menuitem.SetItemLabel with arg 'Remove &DTD'\n"
                "called menuitem.SetHelp with arg 'Remove the document type declaration'\n")

    def test_contextmenu(self, monkeypatch, capsys):
        """unittest for EditorGui.contextmenu
        """
        def mock_get(*args, **kwargs):
            print('called tree.GetBoundingRect with args', args, kwargs)
            return (1, 2, 3, 4)
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        monkeypatch.setattr(testee.wx.Frame, 'PopupMenu', mockwx.MockFrame.PopupMenu)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.tree.GetBoundingRect = mock_get
        testobj.contextmenu_items = []
        testobj.contextmenu()
        assert capsys.readouterr().out == (
                "called tree.GetSelection\n"
                "called tree.GetBoundingRect with args ('selection',) {'textOnly': True}\n"
                "called Menu.__init__ with args ()\n"
                "called Frame.PopupMenu with args (A Menu,) {'pos': (6, 8)}\n"
                "called menu.Destroy\n")
        testobj.contextmenu_items = [('A', ('xxx', 'yyy', 'zzz')), ('M', 'xxx'), ('', '')]
        testobj.contextmenu()
        assert capsys.readouterr().out == (
                "called tree.GetSelection\n"
                "called tree.GetBoundingRect with args ('selection',) {'textOnly': True}\n"
                "called Menu.__init__ with args ()\n"
                "called MenuItem.__init__ with args (A Menu, 100, 'xxx', 'zzz') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'yyy')\n"
                "called menu.Append with args MockMenuItem\n"
                "called Menu.__init__ with args ()\n"
                "called menu.AppendSubMenu with args (A Menu, 'xxx')\n"
                "called menu.AppendSeparator with args ()\n"
                "called Frame.PopupMenu with args (A Menu,) {'pos': (6, 8)}\n"
                "called menu.Destroy\n")

    def test_ask_how_to_continue(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_how_to_continue
        """
        def mock_ask(*args):
            print('called ask_yesnocancel with args', args)
            return 'xxx'
        monkeypatch.setattr(testee, 'ask_yesnocancel', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(title='yyy')
        assert testobj.ask_how_to_continue('', 'text') == "xxx"
        assert capsys.readouterr().out == (
                f"called ask_yesnocancel with args ({testobj}, 'text', 'yyy')\n")
        testobj.editor = types.SimpleNamespace(title='yyy')
        assert testobj.ask_how_to_continue('title', 'text') == "xxx"
        assert capsys.readouterr().out == (
                f"called ask_yesnocancel with args ({testobj}, 'text', 'title')\n")

    def test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for EditorGui.set_item_expanded
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.set_item_expanded('item', True)
        assert capsys.readouterr().out == "called tree.ExpandAllChildren with args ('item',)\n"
        testobj.set_item_expanded('item', False)
        assert capsys.readouterr().out == "called tree.CollapseAllChildren with args ('item',)\n"

    def test_expand(self, monkeypatch, capsys):
        """unittest for EditorGui.expand
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.tree.Selection = ''
        testobj.expand()
        assert capsys.readouterr().out == ""
        testobj.tree.Selection = 'item'
        testobj.expand()
        assert capsys.readouterr().out == "called tree.ExpandAllChildren with args ('item',)\n"

    def test_collapse(self, monkeypatch, capsys):
        """unittest for EditorGui.collapse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.tree.Selection = ''
        testobj.collapse()
        assert capsys.readouterr().out == ""
        testobj.tree.Selection = 'item'
        testobj.collapse()
        assert capsys.readouterr().out == "called tree.CollapseAllChildren with args ('item',)\n"

    def test_get_adv_sel_setting(self, monkeypatch, capsys):
        """unittest for EditorGui.get_adv_sel_setting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.adv_menu = mockwx.MockMenuItem()
        assert capsys.readouterr().out == "called MenuItem.__init__ with args () {}\n"
        assert testobj.get_adv_sel_setting() == "value"
        assert capsys.readouterr().out == "called menuitem.IsChecked\n"

    def test_refresh_preview(self, monkeypatch, capsys):
        """unittest for EditorGui.refresh_preview
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.html = mockwx.MockWebView().New()
        assert capsys.readouterr().out == ("called Tree.__init__ with args () {}\n"
                                           "called WebView.New\n")
        testobj.refresh_preview('soup %SOUP-ENCODING%')
        assert capsys.readouterr().out == ("called WebView.SetPage with args ('soup utf-8', '')\n"
                                           "called tree.SetFocus\n")

    def test_do_delete_item(self, monkeypatch, capsys):
        """unittest for EditorGui.do_delete_item
        """
        def mock_prev(*args):
            print('called tree.GetPrevSibling with args', args)
            return prev_item
        def mock_isok(*args):
            print('called treeitem.isok with args', args)
            return False
        def mock_isok_2(*args):
            print('called treeitem.isok with args', args)
            return True
        def mock_getp(*args):
            print('called tree.GetItemParent with args', args)
            return parent_item
        def mock_get_data(*args):
            print('called tree.GetItemData with args', args)
            return 'xxx'
        def mock_get_data_2(*args):
            print('called tree.GetItemData with args', args)
            return 'root'
        def mock_next(*args):
            print('called tree.GetNextSibling with args', args)
            return next_item
        def mock_delete(*args):
            print('called tree.Delete with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(root='root')
        testobj.tree = mockwx.MockTree()
        testobj.tree.GetPrevSibling = mock_prev
        testobj.tree.GetItemParent = mock_getp
        testobj.tree.GetItemData = mock_get_data
        testobj.tree.GetNextSibling = mock_next
        testobj.tree.Delete = mock_delete
        parent_item = mockwx.MockTreeItem('parent')
        this_item = mockwx.MockTreeItem('this')
        prev_item = mockwx.MockTreeItem('prev')
        next_item = mockwx.MockTreeItem('next')
        assert capsys.readouterr().out == ("called Tree.__init__ with args () {}\n"
                                           "called TreeItem.__init__ with args ('parent',)\n"
                                           "called TreeItem.__init__ with args ('this',)\n"
                                           "called TreeItem.__init__ with args ('prev',)\n"
                                           "called TreeItem.__init__ with args ('next',)\n")
        prev_item.IsOk = mock_isok
        assert testobj.do_delete_item('item') == parent_item
        assert capsys.readouterr().out == ("called tree.GetPrevSibling with args ('item',)\n"
                                           "called treeitem.isok with args ()\n"
                                           "called tree.GetItemParent with args ('item',)\n"
                                           "called tree.GetItemData with args (parent,)\n"
                                           "called tree.Delete with args ('item',)\n")
        testobj.tree.GetItemData = mock_get_data_2
        assert testobj.do_delete_item('item') == next_item
        assert capsys.readouterr().out == ("called tree.GetPrevSibling with args ('item',)\n"
                                           "called treeitem.isok with args ()\n"
                                           "called tree.GetItemParent with args ('item',)\n"
                                           "called tree.GetItemData with args (parent,)\n"
                                           "called tree.GetNextSibling with args ('item',)\n"
                                           "called tree.Delete with args ('item',)\n")
        prev_item.IsOk = mock_isok_2
        assert testobj.do_delete_item('item') == prev_item
        assert capsys.readouterr().out == ("called tree.GetPrevSibling with args ('item',)\n"
                                           "called treeitem.isok with args ()\n"
                                           "called tree.Delete with args ('item',)\n")

    def test_meld(self, monkeypatch, capsys):
        """unittest for EditorGui.meld
        """
        monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(title='title')
        testobj.meld('message')
        assert capsys.readouterr().out == (
                f"called wx.MessageBox with args ('message', 'title') {{'parent': {testobj}}}\n")

    def test_ensure_item_visible(self, monkeypatch, capsys):
        """unittest for EditorGui.ensure_item_visible
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.ensure_item_visible('item')
        assert capsys.readouterr().out == "called tree.EnsureVisible with args ('item',)\n"

    # def test_validate(self, monkeypatch, capsys):
    #     """unittest for EditorGui.validate
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.validate(htmlfile, fromdisk)
    #     assert capsys.readouterr().out == ("")

    # def _test_show_code(self, monkeypatch, capsys):
    #     """unittest for EditorGui.show_cod == "expected_result"e
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.show_code(title, caption, data)
    #     assert capsys.readouterr().out == ("")


class TestVisualTree:
    """unittest for gui_wx.VisualTree
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.VisualTree object

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
        assert capsys.readouterr().out == 'called VisualTree.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for VisualTree.__init__
        """
        monkeypatch.setattr(testee.wx.TreeCtrl, '__init__', mockwx.MockTree.__init__)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'Bind', mockwx.MockTree.Bind)
        parent = types.SimpleNamespace(Parent='parent')
        testobj = testee.VisualTree(parent)
        assert capsys.readouterr().out == (
            f"called Tree.__init__ with args ({parent},) {{'style': 2053}}\n"
            f"called tree.Bind with args ({testee.wx.EVT_TREE_BEGIN_DRAG},"
            f" {testobj.OnBeginDrag})\n"
            f"called tree.Bind with args ({testee.wx.EVT_LEFT_DCLICK}, {testobj.on_leftdclick})\n"
            f"called tree.Bind with args ({testee.wx.EVT_RIGHT_DOWN}, {testobj.on_rightdown})\n"
            f"called tree.Bind with args ({testee.wx.EVT_KEY_DOWN}, {testobj.on_key})\n")

    def test_on_leftdclick(self, monkeypatch, capsys):
        """unittest for VisualTree.on_leftdclick
        """
        def mock_edit():
            print('called Editor.edit')
        def mock_hit(*args):
            print('called tree.HitTest with args', args)
            return None, 0
        def mock_hit_2(*args):
            print('called tree.HitTest with args', args)
            return hititem, 1
        def mock_get_text(*args):
            print('called tree.GetItemText with args', args)
            return '<> itemtext'
        def mock_get_text_2(*args):
            print('called tree.GetItemText with args', args)
            return 'itemtext'
        def mock_get_children(*args):
            print('called Tree.GetChildrenCount with args', args)
            return 0
        def mock_get_children_2(*args):
            print('called Tree.GetChildrenCount with args', args)
            return 1
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HitTest = mock_hit
        testobj._parent = types.SimpleNamespace(top='top', edit=mock_edit)
        testobj.on_leftdclick(event)
        assert capsys.readouterr().out == ("called event.GetPosition\n"
                                           "called tree.HitTest with args ('position',)\n"
                                           "called event.Skip\n")
        testobj.HitTest = mock_hit_2
        hititem = 'top'
        testobj.on_leftdclick(event)
        assert capsys.readouterr().out == ("called event.GetPosition\n"
                                           "called tree.HitTest with args ('position',)\n"
                                           "called event.Skip\n")
        hititem = 'item'
        testobj.GetItemText = mock_get_text
        testobj.GetChildrenCount = mock_get_children
        testobj.on_leftdclick(event)
        assert capsys.readouterr().out == ("called event.GetPosition\n"
                                           "called tree.HitTest with args ('position',)\n"
                                           "called tree.GetItemText with args ('item',)\n"
                                           "called Tree.GetChildrenCount with args ('item',)\n"
                                           "called Editor.edit\n"
                                           "called event.Skip\n")
        testobj.GetItemText = mock_get_text_2
        testobj.on_leftdclick(event)
        assert capsys.readouterr().out == ("called event.GetPosition\n"
                                           "called tree.HitTest with args ('position',)\n"
                                           "called tree.GetItemText with args ('item',)\n"
                                           "called Editor.edit\n"
                                           "called event.Skip\n")
        testobj.GetItemText = mock_get_text
        testobj.GetChildrenCount = mock_get_children_2
        testobj.on_leftdclick(event)
        assert capsys.readouterr().out == ("called event.GetPosition\n"
                                           "called tree.HitTest with args ('position',)\n"
                                           "called tree.GetItemText with args ('item',)\n"
                                           "called Tree.GetChildrenCount with args ('item',)\n"
                                           "called event.Skip\n")

    def test_on_rightdown(self, monkeypatch, capsys):
        """unittest for VisualTree.on_rightdown
        """
        def mock_hit(*args):
            print('called tree.HitTest with args', args)
            return None, 0
        def mock_hit_2(*args):
            print('called tree.HitTest with args', args)
            return hititem, 1
        def mock_menu(*args):
            print('called Editor.contextmenu with args', args)
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HitTest = mock_hit
        testobj._parent = types.SimpleNamespace(top='top', contextmenu=mock_menu)
        testobj.on_rightdown(event)
        assert capsys.readouterr().out == ("called event.GetPosition\n"
                                           "called tree.HitTest with args ('position',)\n"
                                           "called event.Skip\n")
        testobj.HitTest = mock_hit_2
        hititem = 'top'
        testobj.on_rightdown(event)
        assert capsys.readouterr().out == ("called event.GetPosition\n"
                                           "called tree.HitTest with args ('position',)\n"
                                           "called event.Skip\n")
        hititem = 'item'
        testobj.on_rightdown(event)
        assert capsys.readouterr().out == ("called event.GetPosition\n"
                                           "called tree.HitTest with args ('position',)\n"
                                           "called Editor.contextmenu with args ('item',)\n"
                                           "called event.Skip\n")

    def test_on_key(self, monkeypatch, capsys):
        """unittest for VisualTree.on_key
        """
        def mock_getkey():
            print('called event.GetKeyCode')
            return 'anything'
        def mock_getkey_2():
            print('called event.GetKeyCode')
            return testee.wx.WXK_MENU
        def mock_menu(*args):
            print('called Editor.contextmenu with args', args)
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        event.GetKeyCode = mock_getkey
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(top='top', contextmenu=mock_menu)
        testobj.on_key(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called event.Skip\n")
        event.GetKeyCode = mock_getkey_2
        testobj.on_key(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called Editor.contextmenu with args ()\n"
                                           "called event.Skip\n")

    def test_OnDrop(self, monkeypatch, capsys):
        """unittest for VisualTree.OnDrop
        """
        def mock_getroot():
            print('called tree.GetRootItem')
            return 'rootitem'
        def mock_get(*args):
            print('called tree.getsubtree with args', args)
            return 'tree to drag', ''
        def mock_delete(*args):
            print('called tree.Delete with args', args)
        def mock_put(*args):
            print('called tree.putsubtree with args', args)
        def mock_expand(*args):
            print('called tree.Expand with args', args)
        def mock_mark(value):
            print(f'called editor.mark_dirty with arg {value}')
        def mock_refresh():
            print('called editor.refresh_preview')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetRootItem = mock_getroot
        testobj.getsubtree = mock_get
        testobj.Delete = mock_delete
        testobj.putsubtree = mock_put
        testobj.Expand = mock_expand
        testobj._parent = types.SimpleNamespace(editor=types.SimpleNamespace(
            root= 'root', mark_dirty=mock_mark, refresh_preview=mock_refresh))
        testobj.OnDrop('rootitem', 'dragitem')
        assert capsys.readouterr().out == "called tree.GetRootItem\n"
        testobj.OnDrop(None, 'dragitem')
        assert capsys.readouterr().out == (
                "called tree.GetRootItem\n"
                "called tree.getsubtree with args ('dragitem', [])\n"
                "called tree.Delete with args ('dragitem',)\n"
                "called tree.putsubtree with args ('root', 'tree to drag')\n"
                "called tree.Expand with args ('root',)\n"
                "called editor.mark_dirty with arg True\n"
                "called editor.refresh_preview\n")
        testobj.OnDrop('dropitem', 'dragitem')
        assert capsys.readouterr().out == (
                "called tree.GetRootItem\n"
                "called tree.getsubtree with args ('dragitem', [])\n"
                "called tree.Delete with args ('dragitem',)\n"
                "called tree.putsubtree with args ('dropitem', 'tree to drag')\n"
                "called tree.Expand with args ('dropitem',)\n"
                "called editor.mark_dirty with arg True\n"
                "called editor.refresh_preview\n")

    def test_getsubtree(self, monkeypatch, capsys):
        """unittest for VisualTree.getsubtree
        """
        class MockItem:
            def __init__(self, text):
                self._text = text
            def __repr__(self):
                return f"<<Item '{self._text}'>>"
            def IsOk(self):
                return not self._text.endswith('not ok')
        def mock_text(self, *args):
            print('called tree.GetItemText with args', *args)
            return 'xxx'
        def mock_text_2(self, *args):
            print('called tree.GetItemText with args', *args)
            return args[0]._text
        def mock_data(self, *args):
            print('called tree.GetItemData with args', *args)
            return 'yyy'
        def mock_first(self, *args):
            print('called tree.GetFirstChild with args', *args)
            return MockItem(f'{args[0]._text.removeprefix('<> ')} first'), 0
        def mock_next(self, *args):
            print('called tree.GetNextChild with args', *args)
            indx = args[1] + 1
            text = f'{args[0]._text.removeprefix('<> ')} {['first', 'next', 'last', 'not ok'][indx]}'
            return MockItem(text), indx
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'GetItemText', mock_text)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'GetItemData', mock_data)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'GetFirstChild', mock_first)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'GetNextChild', mock_next)
        result = testobj.getsubtree('elem', [])
        assert result == [('xxx', 'yyy', [])]
        assert capsys.readouterr().out == (
                f"called tree.GetItemText with args elem\n"
                f"called tree.GetItemData with args elem\n")
        monkeypatch.setattr(testee.wx.TreeCtrl, 'GetItemText', mock_text_2)
        result = testobj.getsubtree(MockItem('<> elem'), [])
        assert result == [('<> elem', 'yyy', [('elem first', 'yyy', []), ('elem next', 'yyy', []),
                                              ('elem last', 'yyy', [])])]
        assert capsys.readouterr().out == (
                "called tree.GetItemText with args <<Item '<> elem'>>\n"
                "called tree.GetItemData with args <<Item '<> elem'>>\n"
                "called tree.GetFirstChild with args <<Item '<> elem'>>\n"
                "called tree.GetItemText with args <<Item 'elem first'>>\n"
                "called tree.GetItemData with args <<Item 'elem first'>>\n"
                "called tree.GetNextChild with args <<Item '<> elem'>> 0\n"
                "called tree.GetItemText with args <<Item 'elem next'>>\n"
                "called tree.GetItemData with args <<Item 'elem next'>>\n"
                "called tree.GetNextChild with args <<Item '<> elem'>> 1\n"
                "called tree.GetItemText with args <<Item 'elem last'>>\n"
                "called tree.GetItemData with args <<Item 'elem last'>>\n"
                "called tree.GetNextChild with args <<Item '<> elem'>> 2\n")

    def test_putsubtree(self, monkeypatch, capsys):
        """unittest for VisualTree.putsubtree
        """
        monkeypatch.setattr(testee.wx.TreeCtrl, 'AppendItem', mockwx.MockTree.AppendItem)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'InsertItem', mockwx.MockTree.InsertItem)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'SetItemData', mockwx.MockTree.SetItemData)
        data = ('<> elem', 'yyy', [('elem first', 'yyy', []), 'elem next',
                                   ('elem last', 'yyy', [('elem under', 'yyy', [])])])
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.putsubtree('item', data)
        assert capsys.readouterr().out == (
                "called tree.AppendItem with args ('item', '<> elem')\n"
                "called tree.SetItemData() with args ('appended item', 'yyy')\n"
                "called tree.AppendItem with args ('appended item', 'elem first')\n"
                "called tree.SetItemData() with args ('appended item', 'yyy')\n"
                "called tree.AppendItem with args ('appended item', 'elem next')\n"
                "called tree.SetItemData() with args ('appended item', '')\n"
                "called tree.AppendItem with args ('appended item', 'elem last')\n"
                "called tree.SetItemData() with args ('appended item', 'yyy')\n"
                "called tree.AppendItem with args ('appended item', 'elem under')\n"
                "called tree.SetItemData() with args ('appended item', 'yyy')\n")
        testobj.putsubtree('item', data, 1)
        assert capsys.readouterr().out == (
                "called tree.InsertItem with args ('item', 1, '<> elem')\n"
                "called tree.SetItemData() with args ('inserted item', 'yyy')\n"
                "called tree.AppendItem with args ('inserted item', 'elem first')\n"
                "called tree.SetItemData() with args ('appended item', 'yyy')\n"
                "called tree.AppendItem with args ('inserted item', 'elem next')\n"
                "called tree.SetItemData() with args ('appended item', '')\n"
                "called tree.AppendItem with args ('inserted item', 'elem last')\n"
                "called tree.SetItemData() with args ('appended item', 'yyy')\n"
                "called tree.AppendItem with args ('appended item', 'elem under')\n"
                "called tree.SetItemData() with args ('appended item', 'yyy')\n")


def test_show_message(monkeypatch, capsys):
    """unittest for wxgui.show_message
    """
    monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
    testee.show_message('parent', 'title', 'message')
    assert capsys.readouterr().out == (
            "called wx.MessageBox with args ('message', 'title') {'parent': 'parent'}\n")


def test_ask_yesnocancel(monkeypatch, capsys):
    """unittest for wxgui.ask_yesnocancel
    """
    def mock_messagebox(*args, **kwargs):
        print(f'called wx.MessageBox with args', args, kwargs)
        return testee.wx.ID_YES
    def mock_messagebox_2(*args, **kwargs):
        print(f'called wx.MessageBox with args', args, kwargs)
        return testee.wx.ID_NO
    def mock_messagebox_3(*args, **kwargs):
        print(f'called wx.MessageBox with args', args, kwargs)
        return testee.wx.ID_CANCEL
    monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox)
    assert testee.ask_yesnocancel('parent', 'prompt', 'title') == 1
    assert capsys.readouterr().out == (
            "called wx.MessageBox with args ('prompt', 'title') {'style': 26}\n")
    monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox_2)
    assert testee.ask_yesnocancel('parent', 'prompt', 'title') == 0
    assert capsys.readouterr().out == (
            "called wx.MessageBox with args ('prompt', 'title') {'style': 26}\n")
    monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox_3)
    assert testee.ask_yesnocancel('parent', 'prompt', 'title') == -1
    assert capsys.readouterr().out == (
            "called wx.MessageBox with args ('prompt', 'title') {'style': 26}\n")


def test_ask_for_text(monkeypatch, capsys):
    """unittest for wxgui.ask_for_text
    """
    def mock_show(self):
        print('called TextDialog.ShowModal')
        return testee.wx.ID_OK
    def mock_get(self):
        print('called TextDialog.GetValue')
        return 'xxx'
    monkeypatch.setattr(testee.wx, 'TextEntryDialog', mockwx.MockTextDialog)
    assert testee.ask_for_text('parent', 'title', 'caption') == ""
    assert capsys.readouterr().out == (
            "called TextDialog.__init__ with args ('caption', 'title') {}\n"
            "called TextDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockTextDialog, 'ShowModal', mock_show)
    assert testee.ask_for_text('parent', 'title', 'caption') == ""
    assert capsys.readouterr().out == (
            "called TextDialog.__init__ with args ('caption', 'title') {}\n"
            "called TextDialog.ShowModal\n"
            "called TextDialog.GetValue\n")
    monkeypatch.setattr(mockwx.MockTextDialog, 'GetValue', mock_get)
    assert testee.ask_for_text('parent', 'title', 'caption') == "xxx"
    assert capsys.readouterr().out == (
            "called TextDialog.__init__ with args ('caption', 'title') {}\n"
            "called TextDialog.ShowModal\n"
            "called TextDialog.GetValue\n")


def test_call_dialog(monkeypatch, capsys):
    """unittest for wxgui.call_dialog
    """
    class MockDialog:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return True
        def ShowModal(self):
            print('called dialog.ShowModal')
            return answer
        def on_ok(self):
            nonlocal counter
            print('called dialog.on_ok')
            counter += 1
            if counter == 1:
                return False, ''
            return True, 'dialog_data'
    obj = types.SimpleNamespace(gui=MockDialog())
    counter = 0
    answer = testee.wx.ID_CANCEL
    assert testee.call_dialog(obj) == (False, None)
    answer = testee.wx.ID_SAVE
    assert testee.call_dialog(obj) == (True, 'dialog_data')
    assert capsys.readouterr().out == ("called dialog.ShowModal\n"
                                       "called dialog.ShowModal\n"
                                       "called dialog.on_ok\n"
                                       "called dialog.ShowModal\n"
                                       "called dialog.on_ok\n")
    answer = testee.wx.ID_OK
    assert testee.call_dialog(obj) == (True, 'dialog_data')
    assert capsys.readouterr().out == ("called dialog.ShowModal\n"
                                       "called dialog.on_ok\n")
    answer = testee.wx.ID_APPLY
    assert testee.call_dialog(obj) == (True, 'dialog_data')
    assert capsys.readouterr().out == ("called dialog.ShowModal\n"
                                       "called dialog.on_ok\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for wxgui.show_dialog
    """
    class MockDialog:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return True
        def Show(self):
            print('called dialog.show')
    obj = types.SimpleNamespace(gui=MockDialog())
    testee.show_dialog(obj)
    assert capsys.readouterr().out == ("called dialog.show\n")


def test_ask_for_save_filename(monkeypatch, capsys):
    """unittest for wxgui.ask_for_save_filename
    """
    def mock_ask(*args):
        print('called ask_for_filename with args', args)
        return 'xxx'
    monkeypatch.setattr(testee, 'ask_for_filename', mock_ask)
    assert testee.ask_for_save_filename('parent', 'loc', 'mask') == "xxx"
    assert capsys.readouterr().out == (
            "called ask_for_filename with args ('parent', 'loc', 'mask', 'Save file as ...', 2)\n")


def test_ask_for_open_filename(monkeypatch, capsys):
    """unittest for wxgui.ask_for_open_filename
    """
    def mock_ask(*args):
        print('called ask_for_filename with args', args)
        return 'xxx'
    monkeypatch.setattr(testee, 'ask_for_filename', mock_ask)
    assert testee.ask_for_open_filename('parent', 'loc', 'mask') == "xxx"
    assert capsys.readouterr().out == (
            "called ask_for_filename with args ('parent', 'loc', 'mask', 'Choose a file', 1)\n")


def test_ask_for_filename(monkeypatch, capsys, tmp_path):
    """unittest for wxgui.ask_for_filename
    """
    def mock_show(self):
        print('called FileDialog.ShowModal')
        return testee.wx.ID_CANCEL
    def mock_show_2(self):
        print('called FileDialog.ShowModal')
        return testee.wx.ID_OK
    monkeypatch.setattr(testee.wx, 'FileDialog', mockwx.MockFileDialog)
    loc = str(tmp_path)
    monkeypatch.setattr(mockwx.MockFileDialog, 'ShowModal', mock_show)
    assert testee.ask_for_filename('parent', loc, 'mask', 'message', 'style') == ""
    assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args"
            f" () {{'message': 'message', 'defaultDir': '{loc}', 'defaultFile': '',"
            " 'wildcard': 'mask', 'style': 'style'}\n"
            "called FileDialog.ShowModal\n")
    filename = tmp_path / 'testfile'
    filename.touch()
    loc = str(filename)
    monkeypatch.setattr(mockwx.MockFileDialog, 'ShowModal', mock_show_2)
    assert testee.ask_for_filename('parent', loc, 'mask', 'message', 'style') == "dirname/filename"
    assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args"
            f" () {{'message': 'message', 'defaultDir': '{tmp_path}', 'defaultFile': 'testfile',"
            " 'wildcard': 'mask', 'style': 'style'}\n"
            "called FileDialog.ShowModal\n"
            "called FileDialog.GetPath\n")


def test_build_mask(monkeypatch, capsys):
    """unittest for wxgui.build_mask
    """
    monkeypatch.setattr(testee, 'masks', {'all': ('all', 'All'), 'xxx': ('xxx', 'Xxx')})
    assert testee.build_mask('xxx') == "xxx (X,x,x,X,X,X)|X;x;x;X;X;X|all (A)|A"
    assert capsys.readouterr().out == ("")


class TestEditDialogGui:
    """unittests for wxgui.EditDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.EditDialogGui object

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
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = testee.EditDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title', 'style': 536877120}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def test_add_topline(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_topline
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.add_topline(), testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 368, 20)\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_label
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        topline = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_label(topline, 'text')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'element name:'}}\n"
                "called  sizer.Add with args MockStaticText (0, 2048)\n")

    def test_add_textinput(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_textinput
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        topline = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_textinput(topline, 'text', 'width'), testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': ('width', -1)}}\n"
                "called text.SetValue with args ('text',)\n"
                "called  sizer.Add with args MockTextCtrl (0, 2048)\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        topline = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_checkbox(topline, 'text', 'state'), testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called checkbox.SetValue with args ('state',)\n"
                "called  sizer.Add with args MockCheckBox (0, 2048)\n")

    def test_add_content_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_content_section
        """
        monkeypatch.setattr(testee.wx, 'StaticBox', mockwx.MockStaticBox)
        monkeypatch.setattr(testee.wx, 'StaticBoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.add_content_section(), testee.wx.StaticBoxSizer)
        assert capsys.readouterr().out == (
                f"called StaticBox.__init__ with args ({testobj}, -1) {{}}\n"
                f"called BoxSizer.__init__ with args ({testobj.frm}, 8)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8432, 5)\n")

    def test_add_table_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_table_to_section
        """
        def mock_get():
            print('called size.GetWidth')
            return 200
        def mock_getsize(self):
            print('called dialog.GetSize')
            return types.SimpleNamespace(GetWidth=mock_get)
        class MockSettings:
            def __init__(self):
                print('called wx.SystemSettings.__init__')
            def GetColour(self, *args):
                print('called SystemSettings.GetColour with args', args)
                return 'grey'
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wxgrid, 'Grid', mockwx.MockGrid)
        monkeypatch.setattr(testee.wx.Dialog, 'GetSize', mock_getsize)
        monkeypatch.setattr(testee.wx, 'SystemSettings', MockSettings)
        section = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_table_to_section(section, [], {})
        assert isinstance(result, testee.wxgrid.Grid)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Grid.__init__ with args ({testobj},) {{}}\n"
                "called Grid.CreateGrid with args (0, 2)\n"
                "called Grid.SetRowLabelSize with args (19,)\n"
                "called dialog.GetSize\n"
                "called size.GetWidth\n"
                "called Grid.SetColSize with args (1, 88)\n"
                "called wx.SystemSettings.__init__\n"
                "called SystemSettings.GetColour with args (17,)\n"
                "called hori sizer.Add with args MockGrid (1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8432, 5)\n")
        result = testobj.add_table_to_section(
                section, ['xx', 'yy'], {'attr': 'val', 'style': 'qq', 'styledata': 'rr'})
        assert isinstance(result, testee.wxgrid.Grid)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Grid.__init__ with args ({testobj},) {{}}\n"
                "called Grid.CreateGrid with args (0, 2)\n"
                "called Grid.SetRowLabelSize with args (19,)\n"
                "called Grid.SetColLabelValue with args (0, 'x')\n"
                "called Grid.SetColSize with args (0, 'x')\n"
                "called Grid.SetColLabelValue with args (1, 'y')\n"
                "called Grid.SetColSize with args (1, 'y')\n"
                "called dialog.GetSize\n"
                "called size.GetWidth\n"
                "called Grid.SetColSize with args (1, 88)\n"
                "called wx.SystemSettings.__init__\n"
                "called SystemSettings.GetColour with args (17,)\n"
                "called Grid.AppendRows with args (1,)\n"
                "called Grid.GetNumberRows with args ()\n"
                "called Grid.SetRowLabelValue with args (-1, '')\n"
                "called Grid.SetCellValue with args (-1, 0, 'attr')\n"
                "called Grid.SetCellValue with args (-1, 1, 'val')\n"
                "called Grid.AppendRows with args (1,)\n"
                "called Grid.GetNumberRows with args ()\n"
                "called Grid.SetRowLabelValue with args (-1, '')\n"
                "called Grid.SetCellValue with args (-1, 0, 'style')\n"
                "called Grid.SetCellValue with args (-1, 1, 'qq')\n"
                "called Grid.SetReadOnly with args (-1, 0, True)\n"
                "called Grid.SetCellTextColour with args (-1, 0, 'grey')\n"
                "called Grid.AppendRows with args (1,)\n"
                "called Grid.GetNumberRows with args ()\n"
                "called Grid.SetRowLabelValue with args (-1, '')\n"
                "called Grid.SetCellValue with args (-1, 0, 'styledata')\n"
                "called Grid.SetCellValue with args (-1, 1, 'rr')\n"
                "called Grid.SetReadOnly with args (-1, 0, True)\n"
                "called Grid.SetCellTextColour with args (-1, 0, 'grey')\n"
                "called hori sizer.Add with args MockGrid (1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8432, 5)\n")

    def test_add_buttons_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_buttons_to_section
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        section = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(style_text='styletext')
        testobj.add_buttons_to_section(section, [])
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args (4,)\n"
                                           "called  sizer.Add with args MockBoxSizer (0, 496, 1)\n")
        testobj.add_buttons_to_section(section, [('xx', 'callback1'), ('yy', 'callback2')])
        assert not hasattr(testobj, 'style_button')
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback1') {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 1)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'yy'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback2') {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 1)\n"
                "called  sizer.Add with args MockBoxSizer (0, 496, 1)\n")
        testobj.add_buttons_to_section(section, [('styletext', 'callback')])
        assert isinstance(testobj.style_button, testee.wx.Button)
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'styletext'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback') {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 1)\n"
                "called  sizer.Add with args MockBoxSizer (0, 496, 1)\n")

    def test_add_textinput_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_textinput_to_section
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        section = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_textinput_to_section(section, 'text', 'width', 'height')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj},) {{'size': ('width', 'height'), 'style': 32}}\n"
                "called text.SetValue with args ('text',)\n"
                "called hori sizer.Add with args MockTextCtrl (1, 8432, 5)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8304, 20)\n")

    def test_add_text_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_text_to_section
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        section = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text_to_section(section, 'text')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called  sizer.Add with args MockStaticText (0, 64, 10)\n")

    def test_add_radiobutton_to_section(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_radiobutton_to_section
        """
        monkeypatch.setattr(testee.wx, 'RadioButton', mockwx.MockRadioButton)
        section = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_radiobutton_to_section(section, '', True, False)
        assert result is None
        assert capsys.readouterr().out == "called  sizer.AddSpacer with args ()\n"
        result = testobj.add_radiobutton_to_section(section, 'text', True, False)
        assert isinstance(result, testee.wx.RadioButton)
        assert capsys.readouterr().out == (
                "called RadioButton.__init__ with args"
                f" ({testobj},) {{'label': 'text', 'style': 4}}\n"
                "called  sizer.Add with args MockRadioButton (0, 240, 2)\n")
        result = testobj.add_radiobutton_to_section(section, 'text', False, True)
        assert isinstance(result, testee.wx.RadioButton)
        assert capsys.readouterr().out == (
                f"called RadioButton.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called radiobutton.SetValue with args (True,)\n"
                "called  sizer.Add with args MockRadioButton (0, 240, 2)\n")

    def test_add_buttons_to_bottom(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_buttons_to_bottom
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetAffirmativeId',
                            mockwx.MockDialog.SetAffirmativeId)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttons_to_bottom()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5003}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {testobj.on_ok}) {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called Button.Bind with args"
                f" ({testee.wx.EVT_BUTTON}, {testobj.on_cancel}) {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                "called dialog.SetAffirmativeId with args (5003,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 2480, 20)\n")

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_focus_to
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Control.SetFocus\n"

    def _test_on_add(self, monkeypatch, capsys):
        """unittest for EditDialogGui.on_add
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_add(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_del(self, monkeypatch, capsys):
        """unittest for EditDialogGui.on_del
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_del(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_style(self, monkeypatch, capsys):
        """unittest for EditDialogGui.on_style
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_style(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh(self, monkeypatch, capsys):
        """unittest for EditDialogGui.refresh
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_cancel(self, monkeypatch, capsys):
        """unittest for EditDialogGui.on_cancel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_cancel(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_get_radiobutton_state(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_radiobutton_state
        """
        rb = mockwx.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_radiobutton_state(rb) == "value from radiobutton"
        assert capsys.readouterr().out == "called radiobutton.GetValue\n"

    def test_set_radiobutton_state(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_radiobutton_state
        """
        rb = mockwx.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_radiobutton_state(rb, 'value')
        assert capsys.readouterr().out == "called radiobutton.SetValue with args ('value',)\n"

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_textinput_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textinput_value(field) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_get_textarea_contents(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_textarea_contents
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textarea_contents(field) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_checkbox_state
        """
        field = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_state(field) == "value from checkbox"
        assert capsys.readouterr().out == "called checkbox.GetValue\n"

    def test_set_button_text(self, monkeypatch, capsys):
        """unittest  for EditDialogGui.set_button_text
        """
        btn = mockwx.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_button_text(btn, 'text')
        assert capsys.readouterr().out == "called Button.SetLabel with arg 'text'\n"

    def test_get_table_rowcount(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_table_rowcount
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_rowcount(table) == 0
        assert capsys.readouterr().out == "called Grid.GetNumberRows with args ()\n"

    def test_add_table_row(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_table_row
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_row(table, 'row')
        assert capsys.readouterr().out == "called Grid.AppendRows with args (1,)\n"

    def test_add_table_rowitem(self, monkeypatch, capsys):
        """unittest for EditDialogGui.add_table_rowitem
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.inactive_colour = 'grey'
        testobj.add_table_rowitem(table, 'row', 'col', 'text')
        assert capsys.readouterr().out == (
                "called Grid.SetCellValue with args ('row', 'col', 'text')\n")
        testobj.add_table_rowitem(table, 'row', 'col', 'text', editable=False)
        assert capsys.readouterr().out == (
                "called Grid.SetCellValue with args ('row', 'col', 'text')\n"
                "called Grid.SetReadOnly with args ('row', 'col', True)\n"
                "called Grid.SetCellTextColour with args ('row', 'col', 'grey')\n")

    def test_delete_table_row(self, monkeypatch, capsys):
        """unittest for EditDialogGui.delete_table_row
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.delete_table_row(table, 'row')
        assert capsys.readouterr().out == "called Grid.DeleteRows with args ('row', 1)\n"

    def test_set_table_rowheader(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_table_rowheader
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_table_rowheader(table, 2, 'text')
        assert capsys.readouterr().out == "called Grid.SetRowLabelValue with args (1, '')\n"

    def test_select_table_cell(self, monkeypatch, capsys):
        """unittest for EditDialogGui.select_table_cell
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_table_cell(table, 'row', 'col')
        assert capsys.readouterr().out == (
                "called Grid.SelectBlock with args ('row', 'col', 'row', 'col')\n")

    def test_get_selected_table_row(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_selected_table_row
        """
        def mock_get():
            print('called Grid.GetSelectedRows')
            return ['row0', 'row1']
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_table_row(table) is None
        assert capsys.readouterr().out == "called Grid.GetSelectedRows\n"
        table.GetSelectedRows = mock_get
        assert testobj.get_selected_table_row(table) == 'row0'
        assert capsys.readouterr().out == "called Grid.GetSelectedRows\n"

    def test_get_tableitem_text(self, monkeypatch, capsys):
        """unittest for EditDialogGui.get_tableitem_text
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_tableitem_text(table, 'row', 'col') == "value at ('row', 'col')"
        assert capsys.readouterr().out == "called Grid.GetCellValue with args ('row', 'col')\n"

    def test_set_tableitem_text(self, monkeypatch, capsys):
        """unittest for EditDialogGui.set_tableitem_text
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_tableitem_text(table, 'row', 'col', 'text')
        assert capsys.readouterr().out == (
                "called Grid.SetCellValue with args ('row', 'col', 'text')\n")

    def test_on_cancel(self, monkeypatch, capsys):
        """unittest for EditDialogGui.on_cancel
        """
        def mock_refresh():
            print('called EditDialogGui.refresh')
        monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
        monkeypatch.setattr(testee.wx.Dialog, 'EndModal', mockwx.MockDialog.EndModal)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh = mock_refresh
        testobj.master = types.SimpleNamespace(old_styledata='styledata')
        testobj.on_cancel('event')
        assert capsys.readouterr().out == ("called Dialog.EndModal with arg 5101\n")
        testobj.master.styledata = 'styledata'
        testobj.on_cancel('event')
        assert capsys.readouterr().out == ("called Dialog.EndModal with arg 5101\n")
        testobj.master.styledata = 'new styledata'
        testobj.on_cancel('event')
        assert capsys.readouterr().out == (
                "called wx.MessageBox with args"
                " ('Bijbehorende style data is gewijzigd', 'Let op', 256) {}\n"
                "called EditDialogGui.refresh\n")

    def test_on_ok(self, monkeypatch, capsys):
        """unittest for EditDialogGui.on_ok
        """
        def mock_confirm():
            print('called EditDialog.confirm')
            return 'error'
        def mock_confirm_2():
            print('called EditDialog.confirm')
            return ''
        def mock_refresh():
            print('called EditDialogGui.refresh')
        monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.title = 'xxxx'
        testobj.refresh = mock_refresh
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert not testobj.on_ok()
        assert capsys.readouterr().out == (
                "called EditDialog.confirm\n"
                "called wx.MessageBox with args ('error', 'xxxx', 512) {}\n")
        testobj.master.attr_table = 'attr_table'
        assert not testobj.on_ok()
        assert capsys.readouterr().out == (
                "called EditDialogGui.refresh\n"
                "called EditDialog.confirm\n"
                "called wx.MessageBox with args ('error', 'xxxx', 512) {}\n")
        testobj.master.confirm = mock_confirm_2
        assert testobj.on_ok()
        assert capsys.readouterr().out == ('called EditDialogGui.refresh\n'
                                           'called EditDialog.confirm\n')


class TestSearchDialogGui:
    """unittests for wxgui.SearchDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.SearchDialogGui object

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
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = testee.SearchDialogGui('parent')
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': ''}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")
        testobj = testee.SearchDialogGui('parent', 'title')
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title'}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def test_setup_container(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.setup_container
        """
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.setup_container(), testee.wx.GridBagSizer)
        assert capsys.readouterr().out == (
                "called GridSizer.__init__ with args (4, 4) {}\n"
                "called  sizer.Add with args MockGridSizer (1, 368, 8)\n")

    def test_add_title(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_title
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_title(gsizer, 'text', 'row', 'col')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called GridSizer.Add with args MockStaticText (('row', 'col'), (1, 3))\n")

    def test_add_text(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_text
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text(gsizer, 'text', 'row', 'col')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called GridSizer.Add with args MockStaticText (('row', 'col'),) {'flag': 2048}\n")

    def test_add_lineinput(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_lineinput)
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_lineinput(gsizer, 'row', 'col', 'callback')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': (120, -1)}}\n"
                f"called TextCtrl.Bind with args ({testee.wx.EVT_TEXT}, 'callback')\n"
                "called GridSizer.Add with args MockTextCtrl (('row', 'col'),)\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_checkbox(gsizer, 'text', 'row', 'col')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj}, 'text') {{}}\n"
                "called GridSizer.Add with args MockCheckBox (('row', 'col'), (1, 3))\n")

    def test_add_description(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_description
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.add_description(), testee.wx.StaticText)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': ''}}\n"
                "called hori sizer.Add with args MockStaticText ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 48, 8)\n")

    def test_add_buttons_to_bottom(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.add_buttons_to_bottom
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttons_to_bottom()
        assert capsys.readouterr().out == ("called dialog.CreateButtonSizer with args (20,)\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called  sizer.Add with args MockBoxSizer ()\n")

    def test_set_lineinput_value(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.set_lineinput_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_lineinput_value(field, 'text')
        assert capsys.readouterr().out == "called text.SetValue with args ('text',)\n"

    def test_get_lineinput_value(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.get_lineinput_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_lineinput_value(field) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.get_checkbox_state
        """
        field = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_state(field) == "value from checkbox"
        assert capsys.readouterr().out == "called checkbox.GetValue\n"

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.set_focus_to
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Control.SetFocus\n"

    def test_set_label_text(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.set_label_text
        """
        field = mockwx.MockStaticText()
        assert capsys.readouterr().out == "called StaticText.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_label_text(field, 'text')
        assert capsys.readouterr().out == "called StaticText.SetLabel with args ('text',) {}\n"

    def test_update_size(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.update_size
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.update_size()
        assert capsys.readouterr().out == "called  sizer.Fit with args ()\n"

    def test_on_ok(self, monkeypatch, capsys):
        """unittest for SearchDialogGui.on_ok
        """
        def mock_confirm():
            print('called SearchDialog.confirm')
            return 'results'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.on_ok() == "results"
        assert capsys.readouterr().out == "called SearchDialog.confirm\n"


class TestAddDialogGui:
    """unittests for wxgui.AddDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.AddDialogGui object

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
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = testee.AddDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title', 'style': 536877120}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def test_add_content_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_content_section
        """
        monkeypatch.setattr(testee.wx, 'StaticBox', mockwx.MockStaticBox)
        monkeypatch.setattr(testee.wx, 'StaticBoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.add_content_section(), testee.wx.GridBagSizer)
        assert capsys.readouterr().out == (
                f"called StaticBox.__init__ with args ({testobj}, -1) {{}}\n"
                f"called BoxSizer.__init__ with args ({testobj.frm}, 8)\n"
                "called  sizer.Add with args MockBoxSizer (0, 112, 15)\n"
                "called GridSizer.__init__ with args (4, 4) {}\n"
                "called  sizer.Add with args MockGridSizer (0, 240, 10)\n")

    def test_add_text_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_text_to_section
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text_to_section(grid, 'text', 'row', 'col')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called GridSizer.Add with args MockStaticText (('row', 'col'),) {'flag': 2048}\n")

    def test_add_textinput_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_textinput_to_section
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_textinput_to_section(grid, 'row', 'col')
        assert capsys.readouterr().out == (
                "called TextCtrl.__init__ with args"
                f" ({testobj},) {{'size': (250, -1), 'value': ''}}\n"
                "called GridSizer.Add with args MockTextCtrl (('row', 'col'),)\n")
        result = testobj.add_textinput_to_section(grid, 'row', 'col', 'xx', 10, 'callback')
        assert capsys.readouterr().out == (
                "called TextCtrl.__init__ with args"
                f" ({testobj},) {{'size': (10, -1), 'value': 'xx'}}\n"
                f"called TextCtrl.Bind with args ({testee.wx.EVT_TEXT}, 'callback')\n"
                "called GridSizer.Add with args MockTextCtrl (('row', 'col'),)\n")

    def test_add_button_line_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_button_line_to_section
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_button_line_to_section(grid, 'row', [])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called GridSizer.Add with args MockBoxSizer (('row', 0), (1, 2), 256)\n")
        testobj.add_button_line_to_section(grid, 'row', [('xx', 'callback1'), ('yy', 'callback2')])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback1') {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'yy'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback2') {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                "called GridSizer.Add with args MockBoxSizer (('row', 0), (1, 2), 256)\n")

    def test_add_spinbox_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_spinbox_to_section
        """
        monkeypatch.setattr(testee.wx, 'SpinCtrl', mockwx.MockSpinCtrl)
        grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_spinbox_to_section(grid, 'row', 'col')
        assert isinstance(result, testee.wx.SpinCtrl)
        assert capsys.readouterr().out == (
                f"called SpinCtrl.__init__ with args ({testobj},) {{}}\n"
                "called SpinCtrl.SetMax with args (0,)\n"
                "called SpinCtrl.SetValue with args (0,)\n"
                "called GridSizer.Add with args MockSpinCtrl (('row', 'col'),)\n")
        result = testobj.add_spinbox_to_section(grid, 'row', 'col', 10, 1, 'callback')
        assert isinstance(result, testee.wx.SpinCtrl)
        assert capsys.readouterr().out == (
                f"called SpinCtrl.__init__ with args ({testobj},) {{}}\n"
                "called SpinCtrl.SetMax with args (10,)\n"
                "called SpinCtrl.SetValue with args (1,)\n"
                f"called SpinCtrl.bind with args ({testee.wx.EVT_SPINCTRL}, 'callback')\n"
                "called GridSizer.Add with args MockSpinCtrl (('row', 'col'),)\n")

    def test_add_combobox_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_combobox_to_section
        """
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_combobox_to_section(grid, 'row', 'col', [])
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                f"called ComboBox.__init__ with args ({testobj},) {{'style': 32, 'choices': []}}\n"
                "called GridSizer.Add with args MockComboBox ('row', 'col')\n")
        result = testobj.add_combobox_to_section(grid, 'row', 'col', ['xx', 'yy'], 'callback')
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args"
                f" ({testobj},) {{'style': 32, 'choices': ['xx', 'yy']}}\n"
                f"called ComboBox.Bind with args ({testee.wx.EVT_COMBOBOX}, 'callback') {{}}\n"
                "called GridSizer.Add with args MockComboBox ('row', 'col')\n")

    def test_add_checkbox_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_checkbox_to_section
        """
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_checkbox_to_section(grid, 'row', 'col', 'text')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called GridSizer.Add with args"
                " MockCheckBox (('row', 'col'),) {'flag': 240, 'border': 5}\n")
        result = testobj.add_checkbox_to_section(grid, 'row', 'col', 'text', True, 'callback')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called checkbox.SetValue with args (True,)\n"
                f"called CheckBox.Bind with args ({testee.wx.EVT_CHECKBOX}, 'callback') {{}}\n"
                "called GridSizer.Add with args"
                " MockCheckBox (('row', 'col'),) {'flag': 240, 'border': 5}\n")

    def test_add_table_to_section(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_table_to_section
        """
        monkeypatch.setattr(testee.wx.Dialog, 'Bind', mockwx.MockDialog.Bind)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wxgrid, 'Grid', mockwx.MockGrid)
        grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_table_to_section(grid, 'row', 0, [])
        assert isinstance(result, testee.wxgrid.Grid)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Grid.__init__ with args ({testobj},) {{'size': (340, 120)}}\n"
                "called Grid.CreateGrid with args (0, 0)\n"
                "called GridSizer.Add with args MockGrid (('row', 1), (1, 2), 8304, 20)\n")
        result = testobj.add_table_to_section(grid, 'row', 1, ['xx', 'yy'], 'callback')
        assert isinstance(result, testee.wxgrid.Grid)
        assert capsys.readouterr().out == (
            "called BoxSizer.__init__ with args (4,)\n"
            f"called Grid.__init__ with args ({testobj},) {{'size': (340, 120)}}\n"
            "called Grid.CreateGrid with args (1, 2)\n"
            # "called Grid.SetColSize with args (0, 240)\n"
            "called Grid.SetColLabelValue with args (0, 'xx')\n"
            "called Grid.SetColLabelValue with args (1, 'yy')\n"
            f"called Grid.Bind with args ({testee.wxgrid.EVT_GRID_LABEL_LEFT_CLICK}, 'callback')\n"
            f"called Grid.Bind with args ({testee.wxgrid.EVT_GRID_LABEL_LEFT_DCLICK}, 'callback')\n"
            f"called Grid.Bind with args ({testee.wxgrid.EVT_GRID_LABEL_RIGHT_CLICK}, 'callback')\n"
            f"called Grid.Bind with args ({testee.wxgrid.EVT_GRID_LABEL_RIGHT_DCLICK}, 'callback')\n"
            "called GridSizer.Add with args MockGrid (('row', 1), (1, 2), 8304, 20)\n")

    def test_add_buttons_to_bottom(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_buttons_to_bottom
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetAffirmativeId',
                            mockwx.MockDialog.SetAffirmativeId)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttons_to_bottom()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5003}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {testobj.on_ok}) {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {testobj.on_cancel}) {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                "called dialog.SetAffirmativeId with args (5003,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 2480, 20)\n")
        testobj.add_buttons_to_bottom(extra=('xx', 'callback'))
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5003}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {testobj.on_ok}) {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback') {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {testobj.on_cancel}) {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                "called dialog.SetAffirmativeId with args (5003,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 2480, 20)\n")

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_textinput_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textinput_value(field) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_set_textinput_value(self, monkeypatch, capsys):
        """unittest for AddDialogGui.set_textinput_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textinput_value(field, 'value')
        assert capsys.readouterr().out == "called text.SetValue with args ('value',)\n"

    def test_get_conbobox_text(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_conbobox_text
        """
        cb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_conbobox_text(cb) == "value from combobox"
        assert capsys.readouterr().out == "called combobox.GetValue\n"

    def test_get_spinbox_value(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_spinbox_value
        """
        sb = mockwx.MockSpinCtrl()
        assert capsys.readouterr().out == "called SpinCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_spinbox_value(sb) == "value from spinctrl"
        assert capsys.readouterr().out == "called SpinCtrl.GetValue\n"

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_checkbox_state
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_state(cb) == "value from checkbox"
        assert capsys.readouterr().out == "called checkbox.IsChecked\n"

    def test_get_table_columncount(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_table_columncount
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_columncount(table) == 0
        assert capsys.readouterr().out == "called Grid.GetNumberCols with args ()\n"

    def test_get_table_rowcount(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_table_rowcount
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_rowcount(table) == 0
        assert capsys.readouterr().out == "called Grid.GetNumberRows with args ()\n"

    def test_get_tablecell_itemtext(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_tablecell_itemtext
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_tablecell_itemtext(table, 'row', 'col') == "value at ('row', 'col')"
        assert capsys.readouterr().out == "called Grid.GetCellValue with args ('row', 'col')\n"

    def test_set_table_headers(self, monkeypatch, capsys):
        """unittest for AddDialogGui.set_table_headers
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_table_headers(table, [], [])
        assert capsys.readouterr().out == ""
        testobj.set_table_headers(table, ['xx', 'yy'], [10, 20])
        assert capsys.readouterr().out == ("called Grid.SetColLabelValue with args (0, 'xx')\n"
                                           "called Grid.SetColLabelValue with args (1, 'yy')\n"
                                           "called Grid.SetColSize with args (0, 10)\n"
                                           "called Grid.SetColSize with args (1, 20)\n")

    def test_enable_table_header(self, monkeypatch, capsys):
        """unittest for AddDialogGui.enable_table_header
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_table_header(table, False)
        assert capsys.readouterr().out == "called Grid.SetColLabelSize with args (0,)\n"
        testobj.enable_table_header(table, True)
        assert capsys.readouterr().out == "called Grid.SetColLabelSize with args (24,)\n"

    def test_add_table_column(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_table_column
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_column(table, 'colno')
        assert capsys.readouterr().out == "called Grid.InsertCols with args ('colno', 1)\n"

    def test_add_table_row(self, monkeypatch, capsys):
        """unittest for AddDialogGui.add_table_row
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_table_row(table, 'colno')
        assert capsys.readouterr().out == ("called Grid.AppendRows with args (1,)\n"
                                           "called Grid.SetRowLabelValue with args ('colno', '')\n")

    def test_remove_table_column(self, monkeypatch, capsys):
        """unittest for AddDialogGui.remove_table_column
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_table_column(table, 'colno')
        assert capsys.readouterr().out == "called Grid.DeleteCols with args ('colno',)\n"

    def test_remove_table_row(self, monkeypatch, capsys):
        """unittest for AddDialogGui.remove_table_row
        """
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_table_row(table, 'colno')
        assert capsys.readouterr().out == "called Grid.DeleteRows with args ('colno',)\n"

    def test_get_table_column(self, monkeypatch, capsys):
        """unittest for AddDialogGui.get_table_column
        """
        def mock_get():
            print('called event.GetCol')
            return 'col'
        table = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args () {}\n"
        event = types.SimpleNamespace(GetCol=mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_column(event) == "col"
        assert capsys.readouterr().out == "called event.GetCol\n"

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for AddDialogGui.enable_widget
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_widget(widget, False)
        assert capsys.readouterr().out == "called Control.Enable with arg False\n"
        testobj.enable_widget(widget, True)
        assert capsys.readouterr().out == "called Control.Enable with arg True\n"

    def test_on_cancel(self, monkeypatch, capsys):
        """unittest for EditDialogGui.on_cancel
        """
        monkeypatch.setattr(testee.wx.Dialog, 'EndModal', mockwx.MockDialog.EndModal)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_cancel('event')
        assert capsys.readouterr().out == "called Dialog.EndModal with arg 5101\n"

    def test_on_ok(self, monkeypatch, capsys):
        """unittest for EditDialogGui.on_ok
        """
        def mock_confirm():
            print('called EditDialog.confirm')
            return 'error'
        def mock_confirm_2():
            print('called EditDialog.confirm')
            return ''
        monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.title = 'xxxx'
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert not testobj.on_ok()
        assert capsys.readouterr().out == (
                "called EditDialog.confirm\n"
                "called wx.MessageBox with args ('error', 'xxxx', 512) {}\n")
        testobj.master.confirm = mock_confirm_2
        assert testobj.on_ok()
        assert capsys.readouterr().out == "called EditDialog.confirm\n"


class TestScrolledTextDialogGui:
    """unittests for wxgui.ScrolledTextDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.ScrolledTextDialogGui object

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
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = testee.ScrolledTextDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title', 'size': (600, 400)}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def test_add_top_label(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.add_top_label
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_top_label('text')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{}}\n"
                "called StaticText.SetLabel with args ('text',) {}\n"
                "called hori sizer.Add with args MockStaticText ()\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_text_area(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.add_text_area
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.add_text_area(), testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called TextCtrl.__init__ with args ({testobj},) {{'style': 48}}\n"
                "called hori sizer.Add with args MockTextCtrl (1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_bottom_buttons(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.add_bottom_buttons
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetAffirmativeId',
                            mockwx.MockDialog.SetAffirmativeId)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_bottom_buttons([])
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args (4,)\n"
                                           "called  sizer.Add with args MockBoxSizer ()\n")
        testobj.add_bottom_buttons([('xx', 'callback1'), ('yy', 'callback2')])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xx'}}\n"
                "called Button.GetId\n"
                "called dialog.SetAffirmativeId with args ('id',)\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'yy'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback2') {{}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_set_textarea_contents(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialogGui.set_textarea_contents
        """
        textfield = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textarea_contents(textfield, 'data')
        assert capsys.readouterr().out == "called text.SetValue with args ('data',)\n"


class TestCodeViewDialogGui:
    """unittests for wxgui.CodeViewDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.CodeViewDialogGui object

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
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = testee.CodeViewDialogGui('parent', 'title')
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                # "called Dialog.__init__ with args () {'title': 'title', 'size': (600, 400)}\n"
                "called Dialog.__init__ with args () {'title': 'title'}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def test_add_top_message(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.add_top_message
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_top_message('text')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText ()\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_content_area(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.add_content_area
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wxstc, 'StyledTextCtrl', mockwx.MockEditor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_content_area('data')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Editor.__init__ with args ({testobj},) {{}}\n"
                "called editor.SetText with arg `data`\n"
                "called editor.SetReadOnly with arg `True`\n"
                "called hori sizer.Add with args MockEditor (1, 8432)\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_bottom_button(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.add_bottom_button
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetAffirmativeId',
                            mockwx.MockDialog.SetAffirmativeId)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_bottom_button()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': '&Done'}}\n"
                "called Button.GetId\n"
                "called dialog.SetAffirmativeId with args ('id',)\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def _test_setup_text(self, monkeypatch, capsys):
        """unittest for CodeViewDialogGui.setup_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_text() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented - no unittest
