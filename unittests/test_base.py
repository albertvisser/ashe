import pathlib
import types
import pytest
from ashe import base as testee

class MockElement:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class MockCssEditor:
    def __init__(self, *args, **kwargs):
        print('called CssEditor.__init__ with args', args, kwargs)
    def open(self, *args, **kwargs):
        print('called CssEditor.open with args', args, kwargs)
    def show_from_external(self):
        print('called CssEditor.show_from_external')


class MockEditorGui:
    top = 'top'
    # def __init__(self):
    #     print('called gui.__init__()')
    def __init__(self, *args, **kwargs):
        print('called EditorGui.__init__')
        self.textcounter = self.datacounter = self.childcounter = 0
    def go(self):
        print('called EditorGui.go()')
    def close(self):
        print('called EditorGui.close()')
    def get_search_args(self, **kwargs):
        if kwargs.get('replace', True):
            return True, (('x', 'y', 'z', 'a'), 'search_specs', ('q', 'r', 's', 't'))
        else:
            return True, (('x', 'y', 'z', 'a'), 'search_specs')
    def get_selected_item(self):
        print('called EditorGui.get_selected_item')
    def set_selected_item(self, *args):
        print(f'called EditorGui.set_selected_item(`{args[0]}`)')
    def meld(self, msg):
        print(f'called EditorGui.meld with arg `{msg}`')
    def show_statusbar_message(self, msg):
        print(f'called EditorGui.show_statusbar_message with arg `{msg}`')
    def get_element_parent(self, node):
        return ''
    def get_element_text(self, node):
        return ''
    def set_element_text(self, node, data):
        print(f'called EditorGui.set_element_text for `{node}` to `{data}`')
    def get_element_data(self, node):
        return {}
    def set_element_data(self, node, data):
        print(f'called EditorGui.set_element_data for `{node}` to `{data}`')
    def get_screen_title(self):
        return 'screen title'
    def set_screen_title(self, text):
        print(f'called EditorGui.set_screen_title with arg `{text}`')
    def get_element_children(self, node):
        return []  # 'node1', 'node2'
    def addtreetop(self, *args):
        print('called EditorGui.addtreetop with args', args)
    def addtreeitem(self, *args):
        print('called EditorGui.addtreeitem with args', args)
        return 'node'
    def adjust_dtd_menu(self):
        print('called EditorGui.adjust_dtd_menu')
    def do_delete_item(self, arg):
        print(f'called EditorGui.do_delete_item with arg `{arg}`')
    def init_tree(self, *args):
        print('called EditorGui.init_tree with args', args)
    def ensure_item_visible(self, arg):
        print(f'called EditorGui.ensure_item_visible with arg `{arg}`')
    def ask_for_open_filename(self):
        return True, 'x'
    def ask_for_save_filename(self):
        return True, 'x'
    def ask_how_to_continue(self):
        return True, 'x'
    def get_dtd(self):
        return True, 'x'
    def get_css_data(self):
        return True, 'x'
    def validate(self, *args):
        print('called EditorGui.validate with args', args)


class MockManager:
    def __init__(self, *args):
        print('called CssManager.__init__()')


class MockEditorHelper:
    def __init__(self, *args):
        print('called EditorHelper.__init__')

    def edit(self):
        print('called EditorHelper.edit')

    def comment(self):
        print('called EditorHelper.comment')

    def copy(self, **kwargs):
        print('called EditorHelper.copy with args', kwargs)

    def paste(self, **kwargs):
        print('called EditorHelper.paste with args', kwargs)

    def insert(self, **kwargs):
        print('called EditorHelper.insert with args', kwargs)

    def add_text(self, **kwargs):
        print('called EditorHelper.add_text with args', kwargs)


class MockSearchHelper:
    def __init__(self, *args):
        print('called SearchHelper.__init__')

    def search(self, **kwargs):
        print('called SearchHelper.search with args', kwargs)

    def search_from(self, *args, **kwargs):
        print('called SearchHelper.search_from with args', args, kwargs)

    def search_next(self, **kwargs):
        print('called SearchHelper.search_next with args', kwargs)

    def replace_from(self, *args, **kwargs):
        print('called SearchHelper.replace_from with args', args, kwargs)

    def replace_next(self, **kwargs):
        print('called SearchHelper.replace_next with args', kwargs)


class MockEditor:
    def __init__(self):
        self.gui = MockEditorGui()
        print('called Editor.__init__()')


# def test_check_for_csseditor_fail(monkeypatch, capsys):
#     "patch import to fail for cssedit"
#     def mock_import(name, *args):
#         if name == 'cssedit':
#             raise ModuleNotFoundError
#         return orig_import(name, *args)
#     orig_import = __import__  # Store original __import__
#     import builtins
#     monkeypatch.setattr(builtins, '__import__', mock_import)
#     assert not testee.check_for_csseditor()
#
#
# # wat te denken geeft is dat als ik deze testmethode verplaats naar vóór de vorige
# # dat de vorige dan failt
# def test_check_for_csseditor(monkeypatch, capsys):
#     """if cssedit not found on system, create fake package in user install ('.local')
#     don't forget to remove it after test!
#     """
#     # fake_cssedit_path = ... / 'cssedit'
#     # fake_cssedit_path.mkdir()
#     # (fake_cssedit_path / 'editor').mkdir()
#     # (fake_cssedit_path / 'editor' / 'main.py').touch()
#     assert testee.check_for_csseditor()


def test_getelname(monkeypatch, capsys):
    testelement = MockElement('elem')
    assert testee.getelname(testelement, {'id': '15', 'name': 'Me'}) == '<> elem id="15" name="Me"'
    testelement = MockElement('div')
    # beautifulsoup heeft een trucje dat als je het element object opvraagt dat je dan de waarde
    # van "name" krijgt als ik dat wil fixen moet ik wat uitzoekwerk doen, kan ook kijken of ik
    # de inner functie naar buiten kan halen
    assert testee.getelname(testelement,  {'class': 'body'}) == '<> div'  # ' class="body"'
    assert testee.getelname(testelement, comment=True) == '<!> <> div'


def test_get_tag_from_elname():
    with pytest.raises(IndexError):
        assert testee.get_tag_from_elname('some_tag') == 'some_tag'
    assert testee.get_tag_from_elname('  some tag') == 'tag'
    assert testee.get_tag_from_elname('some tag  ') == 'tag'
    assert testee.get_tag_from_elname('some tag') == 'tag'


def test_get_shortname():
    assert testee.getshortname('some\nname') == 'some [+]'
    assert testee.getshortname('looooooooooooooooooooooooooooong name') == (
             'looooooooooooooooooooooooooooo...')
    assert testee.getshortname('looooooooooooooooooooooooooooong\name') == (
             'looooooooooooooooooooooooooooo... [+]')
    assert testee.getshortname('name', comment=True) == '<!> name'


#-- CssManager -----------------------
def test_cssmanager_init(monkeypatch, capsys):
    monkeypatch.setattr(testee, 'toolkit', 'qt')
    monkeypatch.setattr(testee, 'CSSEDIT_AVAIL', False)
    testobj = testee.CssManager('parent')
    assert testobj._parent == 'parent'
    assert not testobj.cssedit_available
    monkeypatch.setattr(testee, 'CSSEDIT_AVAIL', True)
    testobj = testee.CssManager('parent')
    assert testobj._parent == 'parent'
    assert testobj.cssedit_available
    monkeypatch.setattr(testee, 'toolkit', 'wx')
    testobj = testee.CssManager('parent')
    assert testobj._parent == 'parent'
    assert not testobj.cssedit_available
    monkeypatch.setattr(testee, 'CSSEDIT_AVAIL', False)
    testobj = testee.CssManager('parent')
    assert testobj._parent == 'parent'
    assert not testobj.cssedit_available

def mock_cssman_init(self, *args):
    print('called CssManager.__init__ with args', args)
    self._parent = types.SimpleNamespace(gui=types.SimpleNamespace(app='gui_app'))

def test_call_editor(monkeypatch, capsys):
    monkeypatch.setattr(testee.CssManager, '__init__', mock_cssman_init)
    testobj = testee.CssManager()
    assert capsys.readouterr().out == 'called CssManager.__init__ with args ()\n'
    monkeypatch.setattr(testee.csed, 'Editor', MockCssEditor)
    testobj.cssedit_available = True
    testobjmaster = types.SimpleNamespace(styledata='style_data')
    assert testobj.call_editor(testobjmaster, 'style') == (None, None)
    assert testobj.styledata == 'style_data'
    assert testobj.tag == 'style'
    assert capsys.readouterr().out == ("called CssEditor.__init__ with args"
                                       " (namespace(styledata='style_data'),) {'app': 'gui_app'}\n"
                                       "called CssEditor.open with args () {'text': 'style_data'}\n"
                                       "called CssEditor.show_from_external\n")
    testobjmaster = types.SimpleNamespace(styledata='style_data')
    assert testobj.call_editor(testobjmaster, 'other') == (None, None)
    assert testobj.styledata == 'style_data'
    assert testobj.tag == 'other'
    assert capsys.readouterr().out == ("called CssEditor.__init__ with args"
                                       " (namespace(styledata='style_data'),) {'app': 'gui_app'}\n"
                                       "called CssEditor.open with args"
                                       " () {'tag': 'other', 'text': 'style_data'}\n"
                                       "called CssEditor.show_from_external\n")
    testobj.cssedit_available = False
    class MockTextDialog:
        def __init__(self, *args, **kwargs):
            print('called gui.TextDialog.__init__ with args', args, kwargs)
        def __repr__(self):
            return 'MockTextDialog'
    def mock_call(*args):
        print('called ashegui.call_dialog with args', args)
        return False, None
    def mock_call_2(*args):
        print('called ashegui.call_dialog with args', args)
        return True, ['dialog_data', '']
    # monkeypatch.setattr(testobj._parent.gui, 'call_dialog')
    monkeypatch.setattr(testee.gui, 'TextDialog', MockTextDialog)
    testobj._parent.gui.call_dialog = mock_call
    assert testobj.call_editor(testobjmaster, 'style') == ('style_data', {'styledata': 'style_data'})
    assert capsys.readouterr().out == ("called gui.TextDialog.__init__"
                                       " with args (namespace(app='gui_app',"
                                       f" call_dialog={mock_call}),)"
                                       " {'title': 'Edit inline style', 'text': 'style_data',"
                                       " 'show_commented': False}\n"
                                       "called ashegui.call_dialog with args (MockTextDialog,)\n")
    testobj._parent.gui.call_dialog = mock_call_2
    assert testobj.call_editor(testobjmaster, 'other') == ('dialog_data', {'style': 'dialog_data'})
    assert capsys.readouterr().out == ("called gui.TextDialog.__init__"
                                       " with args (namespace(app='gui_app',"
                                       f" call_dialog={mock_call_2}),)"
                                       " {'title': 'Edit inline style', 'text': 'style_data',"
                                       " 'show_commented': False}\n"
                                       "called ashegui.call_dialog with args (MockTextDialog,)\n")

def test_call_editor_for_stylesheet(monkeypatch, capsys):
    def mock_meld(mld):
        print(f'called ashegui.meld with arg `{mld}`')
    def mock_touch(mld):
        print(f'called path.touch with arg `{mld}`')
    monkeypatch.setattr(testee.CssManager, '__init__', mock_cssman_init)
    testobj = testee.CssManager()
    assert capsys.readouterr().out == 'called CssManager.__init__ with args ()\n'
    testobj._parent.gui.meld = mock_meld
    testobj.cssedit_available = False
    testobj.call_editor_for_stylesheet('')
    assert capsys.readouterr().out == ('called ashegui.meld with arg `No CSS editor support;'
                                       ' please edit external stylesheet separately`\n')
    testobj.cssedit_available = True
    testobj.call_editor_for_stylesheet('http')
    assert capsys.readouterr().out == ('called ashegui.meld with arg `Editing of possibly'
                                       ' off-site stylesheets (http-links) is disabled`\n')
    monkeypatch.setattr(testee.os.path, 'exists', lambda *x: False)
    testobj.call_editor_for_stylesheet('/test')
    assert capsys.readouterr().out == ('called ashegui.meld with arg `Cannot determine'
                                       ' file system location of stylesheet file`\n')
    monkeypatch.setattr(testee.os.path, 'exists', lambda *x: True)
    testobj.call_editor_for_stylesheet('/test')
    assert capsys.readouterr().out == ('called ashegui.meld with arg `Stylesheet does not exist`\n')
    monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda *x: False)
    monkeypatch.setattr(testee.pathlib.Path, 'touch', mock_touch)
    testobj.call_editor_for_stylesheet('../test.css')
    assert capsys.readouterr().out == ('called ashegui.meld with arg `Stylesheet does not exist`\n')
    monkeypatch.setattr(testee.csed, 'Editor', MockCssEditor)
    testobj.call_editor_for_stylesheet('../test.css', new_ok=True)
    assert capsys.readouterr().out == (
            "called path.touch with arg `/home/albert/projects/test.css`\n"
            "called CssEditor.__init__ with args () {'app': 'gui_app'}\n"
            "called CssEditor.open with args () {'filename': '/home/albert/projects/test.css'}\n"
            "called CssEditor.show_from_external\n")
    testobj.call_editor_for_stylesheet('')
    assert capsys.readouterr().out == ('called ashegui.meld with arg `Please provide filename'
                                       ' for existing stylesheet`\n')
    testobj.call_editor_for_stylesheet('', new_ok=True)
    assert capsys.readouterr().out == (
            "called CssEditor.__init__ with args () {'app': 'gui_app'}\n"
            "called CssEditor.open with args () {'filename': ''}\n"
            "called CssEditor.show_from_external\n")

def test_call_from_inline(monkeypatch, capsys):
    def mock_call(self, *args):
        print('called CssManager.call_editor with args', args)
    monkeypatch.setattr(testee.CssManager, '__init__', mock_cssman_init)
    monkeypatch.setattr(testee.CssManager, 'call_editor', mock_call)
    testobj = testee.CssManager()
    assert capsys.readouterr().out == 'called CssManager.__init__ with args ()\n'
    testobj.call_from_inline(types.SimpleNamespace(), 'styledata')
    assert capsys.readouterr().out == ("called CssManager.call_editor with args"
                                       " (namespace(styledata='styledata'), 'style')\n")


#-- Editor ---------------------------
def mock_refresh(self):
    print('called Editor.refresh_preview')

def mock_mark_dirty(self, value):
    print(f'called.Editor.mark_dirty with value `{value}`')

def mock_init_editor(self, filename):
    print(f'called Editor.__init__ with filename `{filename}`')
    self.xmlfn = filename
    self.root = 'root'
    self.gui = MockEditorGui()
    # self.cssm = MockManager()
    self.edhlp = MockEditorHelper()
    self.srchhlp = MockSearchHelper()

def setup_editor(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_init_editor)
    testobj = testee.Editor('')
    assert capsys.readouterr().out == ('called Editor.__init__ with filename ``\n'
                                       'called EditorGui.__init__\n'
                                       'called EditorHelper.__init__\n'
                                       'called SearchHelper.__init__\n')
    return testobj

def test_editor_init(monkeypatch, capsys):
    def mock_file2soup(self, arg):
        print(f'called Editor.file2soup with arg `{arg}`')
    def mock_soup2data(self):
        print('called Editor.soup2data')
    monkeypatch.setattr(testee.gui, 'EditorGui', MockEditorGui)
    monkeypatch.setattr(testee, 'CssManager', MockManager)
    monkeypatch.setattr(testee, 'EditorHelper', MockEditorHelper)
    monkeypatch.setattr(testee, 'SearchHelper', MockSearchHelper)
    monkeypatch.setattr(testee.Editor, 'file2soup', mock_file2soup)
    monkeypatch.setattr(testee.Editor, 'soup2data', mock_soup2data)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = testee.Editor('x')
    assert testobj.title == "(untitled) - Albert's Simple HTML Editor"
    assert testobj.constants == {'ELSTART': testee.ELSTART}
    assert not testobj.tree_dirty
    assert testobj.xmlfn == 'x'
    assert isinstance(testobj.gui, testee.gui.EditorGui)
    assert isinstance(testobj.cssm, testee.CssManager)
    assert isinstance(testobj.edhlp, testee.EditorHelper)
    assert isinstance(testobj.srchhlp, testee.SearchHelper)
    assert capsys.readouterr().out == ('called EditorGui.__init__\n'
                                       'called CssManager.__init__()\n'
                                       'called EditorHelper.__init__\n'
                                       'called SearchHelper.__init__\n'
                                       'called Editor.file2soup with arg `x`\n'
                                       'called Editor.soup2data\n'
                                       'called Editor.refresh_preview\n'
                                       'called EditorGui.go()\n')
    monkeypatch.setattr(testee.Editor, 'file2soup', lambda *x: 'message')
    testobj = testee.Editor()
    assert testobj.title == "(untitled) - Albert's Simple HTML Editor"
    assert testobj.constants == {'ELSTART': testee.ELSTART}
    assert not testobj.tree_dirty
    assert testobj.xmlfn == ''
    assert isinstance(testobj.gui, testee.gui.EditorGui)
    assert isinstance(testobj.cssm, testee.CssManager)
    assert isinstance(testobj.edhlp, testee.EditorHelper)
    assert isinstance(testobj.srchhlp, testee.SearchHelper)
    assert capsys.readouterr().out == ('called EditorGui.__init__\n'
                                       'called CssManager.__init__()\n'
                                       'called EditorHelper.__init__\n'
                                       'called SearchHelper.__init__\n'
                                       'called EditorGui.meld with arg `message`\n'
                                       'called EditorGui.go()\n')

def test_file2soup(monkeypatch, capsys, tmp_path):
    def mock_bs(*args):
        print('called BeautifulSoup with args', args)
        return 'root'
    monkeypatch.setattr(testee.bs, 'BeautifulSoup', mock_bs)
    testobj = setup_editor(monkeypatch, capsys)
    assert testobj.file2soup() is None
    assert testobj.root == 'root'
    assert capsys.readouterr().out == ("called BeautifulSoup with args ('<html><head><title>"
                                       "</title></head><body></body></html>', 'lxml')\n")
    testfilename = tmp_path / 'test_file2soup.html'
    assert testobj.file2soup(testfilename) == ('[Errno 2] No such file or directory:'
                                               f" '{testfilename}'")
    assert capsys.readouterr().out == ''
    with testfilename.open('w', encoding='latin-1') as out:
        out.write('<html>\n\t<body>\n\t\ttëstfile\n\t</body>\n</html>\n')
    assert testobj.file2soup(testfilename, preserve=True) is None
    assert capsys.readouterr().out == ("called BeautifulSoup with args ('<html>\\n\\t<body>\\n"
                                       "\\t\\ttëstfile\\n\\t</body>\\n</html>\\n', 'lxml')\n")
    with testfilename.open('w', encoding='utf-8') as out:
        out.write('<html>\n\t<body>\n\t\ttëstfile<br/><hr/>\n\t</body>\n</html>\n')
    assert testobj.file2soup(testfilename) is None
    assert capsys.readouterr().out == ("called BeautifulSoup with args ('<html>"
                                       " <body>  tëstfile<br /><hr /> </body></html>', 'lxml')\n")

def test_soup2data(monkeypatch, capsys):
    def mock_add_node(self, *args):
        print('called Editor.add_node_to_tree with args', args)
    monkeypatch.setattr(testee.Editor, 'add_node_to_tree', mock_add_node)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.soup2data()
    assert not testobj.has_dtd
    assert not testobj.has_stylesheet
    assert capsys.readouterr().out == ("called EditorGui.addtreetop with args ('[untitled]',"
                                       """ "[untitled] - Albert's Simple HTML-editor")\n"""
                                       "called Editor.add_node_to_tree with args ('top', 'root')\n"
                                       "called EditorGui.adjust_dtd_menu\n"
                                       "called EditorGui.init_tree with args ('',)\n"
                                       "called.Editor.mark_dirty with value `False`\n")
    testobj.soup2data('name', 'message')
    assert not testobj.has_dtd
    assert not testobj.has_stylesheet
    assert capsys.readouterr().out == ("called EditorGui.addtreetop with args ('name',"
                                       """ "name - Albert's Simple HTML-editor")\n"""
                                       "called Editor.add_node_to_tree with args ('top', 'root')\n"
                                       "called EditorGui.adjust_dtd_menu\n"
                                       "called EditorGui.init_tree with args ('message',)\n"
                                       "called.Editor.mark_dirty with value `False`\n")
    testobj.xmlfn = 'path/to/file.html'
    testobj.soup2data()
    assert not testobj.has_dtd
    assert not testobj.has_stylesheet
    assert capsys.readouterr().out == ("called EditorGui.addtreetop with args ('path/to/file.html',"
                                       """ "file.html - Albert's Simple HTML-editor")\n"""
                                       "called Editor.add_node_to_tree with args ('top', 'root')\n"
                                       "called EditorGui.adjust_dtd_menu\n"
                                       "called EditorGui.init_tree with args ('',)\n"
                                       "called.Editor.mark_dirty with value `False`\n")

def test_add_node_to_tree(monkeypatch, capsys):
    def mock_find(*args):
        print('called Tag.find_all with args', args)
        return [types.SimpleNamespace(contents=['first body'])]
    class MockBS:
        def BeautifulSoup(*args):
            print('called BeautifulSoup with args', args)
            return types.SimpleNamespace(find_all=mock_find)
        class Tag:
            def __init__(self):
                self.name = 'tagname'
                self.attrs = {'x': '%SOUP-ENCODING%', 'y': 'qqq', 'z': ['a', 'b']}
                self.contents = []
        class Doctype:
            def __str__(self):
                return 'A doctype'
        class Comment:
            def __init__(self):
                self.string = 'a comment'

    def mock_getelname(*args):
        print('called getelname with args', args)
    def mock_getshortname(*args):
        print('called getshortname with args', args)
    def mock_additem(*args):
        print('called EditorGui.addtreeitem with args', args)
    monkeypatch.setattr(testee, 'getelname', mock_getelname)
    monkeypatch.setattr(testee, 'getshortname', mock_getshortname)
    monkeypatch.setattr(testee, 'bs', MockBS)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.root = types.SimpleNamespace(originalEncoding='original')
    monkeypatch.setattr(testobj.gui, 'addtreeitem', mock_additem)
    dt = testee.bs.Doctype()
    node = types.SimpleNamespace(contents=[testee.bs.Tag(), dt, testee.bs.Comment()])
    testobj.add_node_to_tree('item', node)
    assert capsys.readouterr().out == (
        "called getelname with args ('tagname', {'x': 'original', 'y': 'qqq', 'z': 'a b'}, False)\n"
        "called EditorGui.addtreeitem with args"
        " ('item', None, {'x': 'original', 'y': 'qqq', 'z': 'a b'})\n"
        "called getshortname with args ('DOCTYPE A doctype',)\n"
        f"called EditorGui.addtreeitem with args ('item', None, {dt!r})\n"
        "called BeautifulSoup with args ('a comment', 'lxml')\n"
        "called Tag.find_all with args ('body',)\n"
        "called getshortname with args ('first body', True)\n"
        "called EditorGui.addtreeitem with args ('item', None, 'first body')\n")

def test_data2soup(monkeypatch, capsys):
    def mock_expandnode(self, *args):
        print('called Editor.expandnode with args', args)
    class MockList(list):
        def new_tag(self, text):
            print(f'called BeautifulSoup.new_tag with arg {text}')
            return text
    class MockBs:
        def BeautifulSoup(*args):
            print('called bs.BeautifulSoup with args', args)
            return MockList()
        def Doctype(text):
            print(f'called bs.Doctype with arg {text}')
            return text
    def mock_element_children(self, node):
        return [['dtd'], ['ele'], ['other']]
    def mock_element_text(self, node):
        self.textcounter += 1
        data = ['', 'DOCTYPE xxx', '<> element', 'other']
        return data[self.textcounter - 1]
    def mock_element_data(self, node):
        self.datacounter += 1
        data = ['', 'doctypedata', 'elementdata', 'otherdata']
        return data[self.datacounter - 1]
    monkeypatch.setattr(MockEditorGui, 'get_element_children', mock_element_children)
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_element_data)
    monkeypatch.setattr(testee, 'bs', MockBs)
    monkeypatch.setattr(testee.Editor, 'expandnode', mock_expandnode)
    testobj = setup_editor(monkeypatch, capsys)
    assert testobj.data2soup() == ['doctypedata', 'element']
    assert capsys.readouterr().out == (
            "called bs.BeautifulSoup with args ('', 'lxml')\n"
            "called bs.Doctype with arg doctypedata\n"
            "called BeautifulSoup.new_tag with arg element\n"
            "called Editor.expandnode with args (['other'], 'element', 'elementdata')\n")

def test_expandnode(monkeypatch, capsys):
    def mock_newtag(*args):
        print('called BeautifulSoup.new_tag with args', args)
        retval = MockBS.Tag('hola')
        retval.append('first body')
        return retval
    class MockBS:
        def BeautifulSoup(*args):
            print('called BeautifulSoup with args', args)
            return types.SimpleNamespace(new_tag=mock_newtag)
        class Tag:
            def __init__(self, name, attrs=None):
                self.name = name
                self.attrs = attrs if attrs else {}
                self.contents = []
            def __str__(self):
                return f'element {self.name}'
            def append(self, arg):
                print('called Tag.append with arg', arg)
                self.contents.append(arg)
        class Doctype:
            def __init__(self, arg):
                self.string = f'doctype {arg}'
            def __str__(self):
                return self.string
        class Comment:
            def __init__(self, arg):
                self.string = f'commented {arg}'
            def __str__(self):
                return self.string
        class NavigableString:
            def __init__(self, arg):
                self.string = f'plain {arg}'
            def __str__(self):
                return self.string
    def mock_get_children(self, arg):
        print('called EditorGui.get_element_children with arg', arg)
        self.textcounter += 1
        if self.textcounter == 1:
            return ['element', 'commented element', f'{testee.DTDSTART} dtd', 'other']
        return ['other']
    def mock_get_text(self, arg):
        print('called EditorGui.get_element_text with arg', arg)
        if arg == 'element':
            text = '<> this'
        elif arg == 'commented element':
            text = '<!> <> that'
        elif arg == 'dtd':
            text = '<doctype>'
        else:  # 'other'
            text = arg
        return text
    def mock_get_data(self, arg):
        print('called EditorGui.get_element_data with arg', arg)
        if arg == 'element':
            data = {'x': 'xx', 'y': 'yy'}
        elif arg == 'commented element':
            data = {'x': 'xx', 'y': 'yy'}
        elif arg == 'dtd':
            data = 'doctype'
        else:  # 'other'
            data = 'other text'
        return data
    monkeypatch.setattr(MockEditorGui, 'get_element_children', mock_get_children)
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_get_data)
    monkeypatch.setattr(testee, 'bs', MockBS)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.soup = testee.bs.BeautifulSoup('', 'lxml')
    assert capsys.readouterr().out == "called BeautifulSoup with args ('', 'lxml')\n"
    # NB node is een BS Tag object em root ook namelijk direct daaronder
    # daarom kent deze zowel een dict attribuut als een append methode
    node = testee.bs.Tag('element', {'attrname': 'attrvalue'})
    origroot = testee.bs.Tag('subelement', {'xx': 'yyyy'})
    root = origroot
    # breakpoint()
    testobj.expandnode(node, root, {})
    assert root == origroot
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_children with arg element element\n"
            "called EditorGui.get_element_text with arg element\n"
            "called EditorGui.get_element_data with arg element\n"
            "called BeautifulSoup.new_tag with args ('this',)\n"
            "called Tag.append with arg first body\n"
            "called Tag.append with arg element hola\n"
            "called EditorGui.get_element_children with arg element\n"
            "called EditorGui.get_element_text with arg other\n"
            "called EditorGui.get_element_data with arg other\n"
            "called Tag.append with arg plain other text\n"
            "called EditorGui.get_element_text with arg commented element\n"
            "called EditorGui.get_element_data with arg commented element\n"
            "called BeautifulSoup with args ('', 'lxml')\n"
            "called BeautifulSoup.new_tag with args ('that',)\n"
            "called Tag.append with arg first body\n"
            "called EditorGui.get_element_children with arg commented element\n"
            "called EditorGui.get_element_text with arg other\n"
            "called EditorGui.get_element_data with arg other\n"
            "called Tag.append with arg plain other text\n"
            "called Tag.append with arg commented element hola\n"
            "called EditorGui.get_element_text with arg DOCTYPE dtd\n"
            "called EditorGui.get_element_data with arg DOCTYPE dtd\n"
            "called Tag.append with arg doctype other text\n"
            "called EditorGui.get_element_text with arg other\n"
            "called EditorGui.get_element_data with arg other\n"
            "called Tag.append with arg plain other text\n")
    root = origroot
    testobj.expandnode(node, root, {}, commented=True)
    assert root == origroot
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_children with arg element element\n"
            "called EditorGui.get_element_text with arg other\n"
            "called EditorGui.get_element_data with arg other\n"
            "called Tag.append with arg plain other text\n")

def test_soup2file(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(testee.Editor, '__init__', mock_init_editor)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    xmlfn = tmp_path / 'testsoup2file.html'
    backup = tmp_path / 'testsoup2file.html.bak'
    testobj = testee.Editor(str(xmlfn))
    assert capsys.readouterr().out == (f'called Editor.__init__ with filename `{xmlfn}`\n'
                                       'called EditorGui.__init__\n'
                                       'called EditorHelper.__init__\n'
                                       'called SearchHelper.__init__\n')
    # testobj = setup_editor(monkeypatch, capsys)
    testobj.soup = 12
    testobj.soup2file()
    assert not backup.exists()
    assert xmlfn.read_text() == '12'
    assert capsys.readouterr().out == 'called.Editor.mark_dirty with value `False`\n'
    xmlfn.unlink()
    testobj.soup2file(saveas=True)
    assert not backup.exists()
    assert xmlfn.read_text() == '12'
    assert capsys.readouterr().out == 'called.Editor.mark_dirty with value `False`\n'
    testobj.soup = 15
    testobj.soup2file()
    assert backup.read_text() == '12'
    assert xmlfn.read_text() == '15'
    assert capsys.readouterr().out == 'called.Editor.mark_dirty with value `False`\n'
    backup.unlink()
    testobj.soup = 12
    testobj.soup2file(saveas=True)

def test_get_menulist(monkeypatch, capsys):
    menuitems_per_menu = (7, 6, 16, 9, 13 ,1)
    sep_locations = ((0, 5), (1, 2), (1, 4), (2, 2), (2, 8), (3, 4), (4, 2), (4, 7), (4, 10))
    with_indicator = ((1, 0), (1, 1))
    testobj = setup_editor(monkeypatch, capsys)
    data = testobj.get_menulist()
    assert len(data) == 6
    for menuseq, menu in enumerate(data):
        name, menuitems = menu
        assert len(menuitems) == menuitems_per_menu[menuseq]
        for itemseq, menuitem in enumerate(menuitems):
            if (menuseq, itemseq) in sep_locations:
                assert len(menuitem) == 1
            elif (menuseq, itemseq) in with_indicator:
                assert len(menuitem) == 6
            else:
                assert len(menuitem) == 5

def test_mark_dirty(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.title = 'x'
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == 'called EditorGui.set_screen_title with arg `screen title`\n'
    # waarom krijg ik geen sterretje?
    testobj.mark_dirty(False)
    assert not testobj.tree_dirty
    assert capsys.readouterr().out == 'called EditorGui.set_screen_title with arg `screen title`\n'
    monkeypatch.setattr(testobj.gui, 'get_screen_title', lambda *x: '* some text')
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == 'called EditorGui.set_screen_title with arg `* some text`\n'
    testobj.mark_dirty(False)
    assert not testobj.tree_dirty
    assert capsys.readouterr().out == 'called EditorGui.set_screen_title with arg `* some text`\n'
    # waarom verdwijnt het sterretje niet?

def test_check_tree_state(monkeypatch, capsys):
    def mock_savexml(self):
        print('called Editor.savexml')
    counter = 0
    def mock_ask_how(self, *args):
        nonlocal counter
        counter += 1
        print('called EditorGui.ask_how_to_continue with args', args)
        return counter - 1
    monkeypatch.setattr(testee.Editor, 'savexml', mock_savexml)
    monkeypatch.setattr(MockEditorGui, 'ask_how_to_continue', mock_ask_how)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.tree_dirty = False
    assert testobj.check_tree_state() == 0
    assert capsys.readouterr().out == ''
    testobj.tree_dirty = True
    testobj.title = 'title'
    assert testobj.check_tree_state() == 0
    assert capsys.readouterr().out == ("called EditorGui.ask_how_to_continue with args ('title', "
                                       "'HTML data has been modified - save before continuing?')\n")
    assert testobj.check_tree_state() == 1
    assert capsys.readouterr().out == ("called EditorGui.ask_how_to_continue with args ('title', "
                                       "'HTML data has been modified - save before continuing?')\n"
                                       'called Editor.savexml\n')

def test_is_stylesheet_node(monkeypatch, capsys):
    def mock_get_text(self, node):
        print(f'called EditorGui.get_element_text for `{node}`')
        return 'x'
    def mock_get_text_2(self, node):
        print(f'called EditorGui.get_element_text for `{node}`')
        return f'{testee.ELSTART} style'
    def mock_get_text_3(self, node):
        print(f'called EditorGui.get_element_text for `{node}`')
        return f'{testee.ELSTART} link'
    def mock_get_data(self, node):
        print(f'called EditorGui.get_element_data for `{node}`')
        return {'x': 'y'}
    def mock_get_data_2(self, node):
        print(f'called EditorGui.get_element_data for `{node}`')
        return {'rel': 'stylesheet'}
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_get_data)
    testobj = setup_editor(monkeypatch, capsys)
    assert not testobj.is_stylesheet_node('node')
    assert capsys.readouterr().out == 'called EditorGui.get_element_text for `node`\n'

    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_2)
    testobj = setup_editor(monkeypatch, capsys)
    assert testobj.is_stylesheet_node('node')
    assert capsys.readouterr().out == 'called EditorGui.get_element_text for `node`\n'

    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_3)
    testobj = setup_editor(monkeypatch, capsys)
    assert not testobj.is_stylesheet_node('node')
    assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                       'called EditorGui.get_element_data for `node`\n')

    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_3)
    monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_get_data_2)
    testobj = setup_editor(monkeypatch, capsys)
    assert testobj.is_stylesheet_node('node')
    assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                       'called EditorGui.get_element_data for `node`\n')

def test_in_body(monkeypatch, capsys):
    def mock_get_text(self, node):
        print(f'called EditorGui.get_element_text for `{node}`')
        return 'x'
    def mock_get_text_2(self, node):
        print(f'called EditorGui.get_element_text for `{node}`')
        return f'{testee.ELSTART} head'
    def mock_get_text_3(self, node):
        print(f'called EditorGui.get_element_text for `{node}`')
        return f'{testee.ELSTART} body'
    def mock_get_text_4(self, node):
        nonlocal counter
        counter += 1
        print(f'called EditorGui.get_element_text for `{node}`')
        if counter < 3:
            return 'x'
        return f'{testee.ELSTART} head'
    def mock_get_text_5(self, node):
        nonlocal counter
        counter += 1
        print(f'called EditorGui.get_element_text for `{node}`')
        if counter < 3:
            return 'x'
        return f'{testee.ELSTART} body'
    def mock_get_parent(self, node):
        print(f'called EditorGui.get_element_parent for `{node}`')
    def mock_get_parent_2(self, node):
        print(f'called EditorGui.get_element_parent for `{node}`')
        return 'x'
    # element zonder parent
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_parent', mock_get_parent)
    testobj = setup_editor(monkeypatch, capsys)
    counter = 0
    assert not testobj.in_body('node')
    assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                       'called EditorGui.get_element_parent for `node`\n')
    # head
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_2)
    monkeypatch.setattr(MockEditorGui, 'get_element_parent', mock_get_parent_2)
    testobj = setup_editor(monkeypatch, capsys)
    counter = 0
    assert not testobj.in_body('node')
    assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                       'called EditorGui.get_element_parent for `node`\n')
    testobj = setup_editor(monkeypatch, capsys)
    # body
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_3)
    testobj = setup_editor(monkeypatch, capsys)
    counter = 0
    assert testobj.in_body('node')
    assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                       'called EditorGui.get_element_parent for `node`\n')
    testobj = setup_editor(monkeypatch, capsys)
    # element onder head
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_4)
    testobj = setup_editor(monkeypatch, capsys)
    counter = 0
    assert not testobj.in_body('node')
    assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                       'called EditorGui.get_element_parent for `node`\n'
                                       'called EditorGui.get_element_text for `x`\n'
                                       'called EditorGui.get_element_parent for `x`\n'
                                       'called EditorGui.get_element_text for `x`\n'
                                       'called EditorGui.get_element_parent for `x`\n')
    # element onder body
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_5)
    testobj = setup_editor(monkeypatch, capsys)
    counter = 0
    assert testobj.in_body('node')
    assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                       'called EditorGui.get_element_parent for `node`\n'
                                       'called EditorGui.get_element_text for `x`\n'
                                       'called EditorGui.get_element_parent for `x`\n'
                                       'called EditorGui.get_element_text for `x`\n'
                                       'called EditorGui.get_element_parent for `x`\n')

def test_newxml(monkeypatch, capsys):
    def mock_check_state(self):
        print('called Editor.check_tree_state')
        return 0
    def mock_file2soup(self, *args, **kwargs):
        print('called Editor.file2soup with args', args, kwargs)
    def mock_soup2data(self, *args, **kwargs):
        print('called Editor.soup2data with args', args, kwargs)
    def mock_refresh_preview(self):
        print('called Editor.refresh_preview')
    monkeypatch.setattr(testee.Editor, 'check_tree_state', mock_check_state)
    monkeypatch.setattr(testee.Editor, 'file2soup', mock_file2soup)
    monkeypatch.setattr(testee.Editor, 'soup2data', mock_soup2data)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh_preview)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.newxml()
    assert capsys.readouterr().out == ("called Editor.check_tree_state\n"
            "called Editor.file2soup with args () {}\n"
            "called Editor.soup2data with args () {'message': 'started new document'}\n"
            "called Editor.refresh_preview\n")
    monkeypatch.setattr(testee.Editor, 'file2soup', lambda *x: 'error')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.newxml()
    assert capsys.readouterr().out == ("called Editor.check_tree_state\n"
                                       "called EditorGui.meld with arg `error`\n")
    monkeypatch.setattr(testee.Editor, 'check_tree_state', lambda *x: -1)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.newxml()
    assert capsys.readouterr().out == ''

def test_openxml(monkeypatch, capsys):
    def mock_check_state(self):
        print('called Editor.check_tree_state')
        return 0
    def mock_ask_filename(self):
        print('called EditorGui.ask_for_open_filename')
    def mock_file2soup(self, *args, **kwargs):
        print('called Editor.file2soup with args', args, kwargs)
    def mock_soup2data(self, *args, **kwargs):
        print('called Editor.soup2data with args', args, kwargs)
    def mock_refresh_preview(self):
        print('called Editor.refresh_preview')
    monkeypatch.setattr(MockEditorGui, 'ask_for_open_filename', mock_ask_filename)
    monkeypatch.setattr(testee.Editor, 'check_tree_state', mock_check_state)
    monkeypatch.setattr(testee.Editor, 'file2soup', mock_file2soup)
    monkeypatch.setattr(testee.Editor, 'soup2data', mock_soup2data)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh_preview)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.openxml()
    assert capsys.readouterr().out == ('called Editor.check_tree_state\n'
                                       'called EditorGui.ask_for_open_filename\n')

    monkeypatch.setattr(MockEditorGui, 'ask_for_open_filename', lambda *x: 'somefile')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.openxml()
    assert capsys.readouterr().out == ('called Editor.check_tree_state\n'
            "called Editor.file2soup with args () {'fname': 'somefile'}\n"
            "called Editor.soup2data with args ('somefile', 'loaded somefile') {}\n"
            "called Editor.refresh_preview\n")
    monkeypatch.setattr(testee.Editor, 'file2soup', lambda *x, **y: 'error')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.openxml()
    assert capsys.readouterr().out == ("called Editor.check_tree_state\n"
                                       "called EditorGui.meld with arg `error`\n")

    monkeypatch.setattr(testee.Editor, 'check_tree_state', lambda *x: -1)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.openxml()
    assert capsys.readouterr().out == ''

def test_savexml(monkeypatch, capsys):
    def mock_savexmlas(self):
        print('called Editor.savexmlas')
    def mock_data2soup(self, *args, **kwargs):
        print('called Editor.data2soup with args', args, kwargs)
    def mock_soup2file(self, *args, **kwargs):
        print('called Editor.soup2file with args', args, kwargs)
    def mock_soup2file_2(self, *args, **kwargs):
        raise OSError('Error')
    monkeypatch.setattr(testee.Editor, 'savexmlas', mock_savexmlas)
    monkeypatch.setattr(testee.Editor, 'data2soup', mock_data2soup)
    monkeypatch.setattr(testee.Editor, 'soup2file', mock_soup2file)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.xmlfn = ''
    testobj.savexml()
    assert capsys.readouterr().out == 'called Editor.savexmlas\n'
    testobj.xmlfn = 'filename'
    testobj.savexml()
    assert capsys.readouterr().out == ('called Editor.data2soup with args () {}\n'
                                       'called Editor.soup2file with args () {}\n'
                                       'called EditorGui.show_statusbar_message with arg'
                                       ' `saved filename`\n')
    monkeypatch.setattr(testee.Editor, 'soup2file', mock_soup2file_2)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.xmlfn = 'filename'
    testobj.savexml()
    assert capsys.readouterr().out == ('called Editor.data2soup with args () {}\n'
                                       'called EditorGui.meld with arg `Error`\n')

def test_savexmlas(monkeypatch, capsys):
    def mock_data2soup(self, *args, **kwargs):
        print('called Editor.data2soup with args', args, kwargs)
    def mock_soup2file(self, *args, **kwargs):
        print('called Editor.soup2file with args', args, kwargs)
    def mock_soup2file_2(self, *args, **kwargs):
        raise OSError('Error')
    monkeypatch.setattr(MockEditorGui, 'ask_for_save_filename', lambda *x: '')
    monkeypatch.setattr(testee.Editor, 'data2soup', mock_data2soup)
    monkeypatch.setattr(testee.Editor, 'soup2file', mock_soup2file)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.savexmlas()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(MockEditorGui, 'ask_for_save_filename', lambda *x: 'filename')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.savexmlas()
    assert capsys.readouterr().out == ('called Editor.data2soup with args () {}\n'
                                       "called Editor.soup2file with args () {'saveas': True}\n"
                                       'called EditorGui.set_element_text for `top` to `filename`\n'
                                       'called EditorGui.show_statusbar_message with arg'
                                       ' `saved as filename`\n')
    monkeypatch.setattr(testee.Editor, 'soup2file', mock_soup2file_2)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.savexmlas()
    assert capsys.readouterr().out == ('called Editor.data2soup with args () {}\n'
                                       'called EditorGui.meld with arg `Error`\n')

def test_reopenxml(monkeypatch, capsys):
    def mock_file2soup(self, *args, **kwargs):
        print('called Editor.file2soup with args', args, kwargs)
    def mock_soup2data(self, *args, **kwargs):
        print('called Editor.soup2data with args', args, kwargs)
    def mock_refresh_preview(self):
        print('called Editor.refresh_preview')
    monkeypatch.setattr(testee.Editor, 'file2soup', mock_file2soup)
    monkeypatch.setattr(testee.Editor, 'soup2data', mock_soup2data)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh_preview)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.xmlfn = 'xxx'
    testobj.reopenxml()
    assert capsys.readouterr().out == (
            "called Editor.file2soup with args () {'fname': 'xxx'}\n"
            "called Editor.soup2data with args ('xxx', 'reloaded xxx') {}\n"
            'called Editor.refresh_preview\n')
    monkeypatch.setattr(testee.Editor, 'file2soup', lambda *x, **y: 'error')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.reopenxml()
    assert capsys.readouterr().out == "called EditorGui.meld with arg `error`\n"

def test_close(monkeypatch, capsys):
    def mock_check_state(self):
        print('called Editor.check_tree_state')
        return 0
    monkeypatch.setattr(testee.Editor, 'check_tree_state', lambda *x: -1)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.close()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testee.Editor, 'check_tree_state', mock_check_state)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.close()
    assert capsys.readouterr().out == 'called Editor.check_tree_state\ncalled EditorGui.close()\n'

def test_expand(monkeypatch, capsys):
    def mock_expand():
        print('called EditorGui.expand')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.expand = mock_expand
    testobj.expand()
    assert capsys.readouterr().out == 'called EditorGui.expand\n'

def test_collapse(monkeypatch, capsys):
    def mock_collapse():
        print('called EditorGui.collapse')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.collapse = mock_collapse
    testobj.collapse()
    assert capsys.readouterr().out == 'called EditorGui.collapse\n'

def test_advance_selection_onoff(monkeypatch, capsys):
    def mock_get_setting():
        print('called EditorGui.get_adv_sel_setting')
        return 'sett'
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.get_adv_sel_setting = mock_get_setting
    testobj.advance_selection_onoff()
    assert capsys.readouterr().out == 'called EditorGui.get_adv_sel_setting\n'
    assert testobj.advance_selection_on_add == 'sett'

def test_refresh_preview(monkeypatch, capsys):
    def mock_data2soup(self, *args, **kwargs):
        print('called Editor.data2soup')
        return 'soup'
    def mock_refresh(arg):
        print(f'called EditorGui.refresh_preview with arg `{arg}`')
    monkeypatch.setattr(testee.Editor, 'data2soup', mock_data2soup)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.refresh_preview = mock_refresh
    testobj.refresh_preview()
    assert capsys.readouterr().out == ('called Editor.data2soup\n'
                                       'called EditorGui.refresh_preview with arg `soup`\n')

def test_checkselection(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    assert not testobj.checkselection()
    assert testobj.item is None
    assert capsys.readouterr().out == (
            'called EditorGui.get_selected_item\n'
            'called EditorGui.meld with arg `You need to select an element or text first`\n')

    monkeypatch.setattr(MockEditorGui, 'get_selected_item', lambda *x: 'top')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.top = 'top'
    assert not testobj.checkselection()
    assert testobj.item == 'top'
    assert capsys.readouterr().out == (
            'called EditorGui.meld with arg `You need to select an element or text first`\n')

    monkeypatch.setattr(MockEditorGui, 'get_selected_item', lambda *x: 'not_top')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.top = 'top'
    assert testobj.checkselection()
    assert testobj.item == 'not_top'
    assert capsys.readouterr().out == ''

def test_edit(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.edit()
    assert capsys.readouterr().out == 'called EditorHelper.edit\n'
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.edit()
    assert capsys.readouterr().out == ''

def test_comment(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.comment()
    assert capsys.readouterr().out == 'called EditorHelper.comment\n'
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.comment()
    assert capsys.readouterr().out == ''

# def _test_make_conditional(monkeypatch, capsys):
#     testobj = setup_editor(monkeypatch, capsys)

# def _test_remove_condition(monkeypatch, capsys):
#     testobj = setup_editor(monkeypatch, capsys)

def test_cut(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.cut()
    assert capsys.readouterr().out == "called EditorHelper.copy with args {'cut': True}\n"

def test_delete(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.delete()
    assert capsys.readouterr().out == ("called EditorHelper.copy with args {'cut': True,"
                                       " 'retain': False}\n")

def test_copy(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.copy()
    assert capsys.readouterr().out == "called EditorHelper.copy with args {}\n"

def test_paste_after(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.paste_after()
    assert capsys.readouterr().out == "called EditorHelper.paste with args {'before': False}\n"

def test_paste_below(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.paste_below()
    assert capsys.readouterr().out == "called EditorHelper.paste with args {'below': True}\n"

def test_paste(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.paste()
    assert capsys.readouterr().out == "called EditorHelper.paste with args {}\n"

def test_insert(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.insert()
    assert capsys.readouterr().out == "called EditorHelper.insert with args {}\n"

def test_insert_after(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.insert_after()
    assert capsys.readouterr().out == "called EditorHelper.insert with args {'before': False}\n"

def test_insert_child(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.insert_child()
    assert capsys.readouterr().out == "called EditorHelper.insert with args {'below': True}\n"

def test_add_text(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.add_text()
    assert capsys.readouterr().out == "called EditorHelper.add_text with args {}\n"

def test_add_text_after(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.add_text_after()
    assert capsys.readouterr().out == "called EditorHelper.add_text with args {'before': False}\n"

def test_add_textchild(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.add_textchild()
    assert capsys.readouterr().out == "called EditorHelper.add_text with args {'below': True}\n"

def test_build_search_spec(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    assert testobj.build_search_spec('', '', '', '') == ''
    assert testobj.build_search_spec('x', '', '', '') == 'search for an element named `x`'
    assert testobj.build_search_spec('', 'x', '', '') == 'search for an attribute named `x`'
    assert testobj.build_search_spec('', '', 'x', '') == 'search for an attribute that has value `x`'
    assert testobj.build_search_spec('', '', '', 'x') == 'search for text'
    assert testobj.build_search_spec('x', 'y', '', '') == ('search for an element named `x`'
                                                           ' with an attribute named `y`')
    assert testobj.build_search_spec('x', '', 'y', '') == ('search for an element named `x`'
                                                           ' with an attribute that has value `y`')
    assert testobj.build_search_spec('x', '', '', 'y') == 'search for text under an element named `x`'
    assert testobj.build_search_spec('', 'x', 'y', '') == ('search for an attribute named `x`'
                                                           ' that has value `y`')
    assert testobj.build_search_spec('', 'x', '', 'y') == ('search for text under an element'
                                                           ' with an attribute named `x`')
    assert testobj.build_search_spec('', '', 'x', 'y') == ('search for text under an element'
                                                           ' with an attribute that has value `x`')
    assert testobj.build_search_spec('x', 'y', 'z', '') == ('search for an element named `x`'
                                                            ' with an attribute named `y`'
                                                            ' that has value `z`')
    assert testobj.build_search_spec('x', 'y', '', 'z') == ('search for text'
                                                            ' under an element named `x`'
                                                            ' with an attribute named `y`')
    assert testobj.build_search_spec('x', '', 'y', 'z') == ('search for text'
                                                            ' under an element named `x`'
                                                            ' with an attribute that has value `y`')
    assert testobj.build_search_spec('', 'x', 'y', 'z') == ('search for text under an element'
                                                            ' with an attribute named `x`'
                                                            ' that has value `y`')
    assert testobj.build_search_spec('x', 'y', 'z', 'a', ()) == ('search for text'
                                                                 ' under an element named `x`'
                                                                 ' with an attribute named `y`'
                                                                 ' that has value `z`')
    assert testobj.build_search_spec('', '', '', '', ('x')) == (
            'error: element replacement without element search')
    assert testobj.build_search_spec('', '', '', '', ('', 'x')) == (
            'error: attribute replacement without attribute search')
    assert testobj.build_search_spec('', '', '', '', ('', '', 'x')) == (
            'error: attribute value replacement without attribute value search')
    assert testobj.build_search_spec('', '', '', '', ('', '', '', 'x')) == (
            'error: text replacement without text search')
    assert testobj.build_search_spec('x', '', '', '', ('y', '', '', '')) == (
            'search for an element named `x`\nand replace element name with `y`')
    assert testobj.build_search_spec('', 'x', '', '', ('', 'y', '', '')) == (
            'search for an attribute named `x`\nand replace attribute name with `y`')
    assert testobj.build_search_spec('', '', 'x', '', ('', '', 'y', '')) == (
            'search for an attribute that has value `x`\nand replace attribute value with `y`')
    assert testobj.build_search_spec('', '', '', 'x', ('', '', '', 'y')) == (
            'search for text\nand replace text with `y`')
    assert testobj.build_search_spec('x', 'y', 'z', 'a', ('xx', 'yy', 'zz', 'aa')) == (
            'search for text under an element named `x` with an attribute named `y`'
            ' that has value `z`\nand replace element name with `xx`, attribute name with `yy`,'
            ' attribute value with `zz`, text with `aa`')

def test_search(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.search()
    assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.search_from with args () {'item': None}\n")

def test_search_last(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.search_last()
    assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.search_from with args () {'reverse': True, 'item': None}\n")

def test_search_next(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.search_next()
    assert capsys.readouterr().out == "called SearchHelper.search_next with args {}\n"

def test_search_prev(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.search_prev()
    assert capsys.readouterr().out == "called SearchHelper.search_next with args {'reverse': True}\n"

def test_replace(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.replace()
    assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.replace_from with args () {'item': None}\n")

def test_replace_last(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.replace_last()
    assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.replace_from with args () {'reverse': True, 'item': None}\n")

def test_replace_and_next(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.replace_and_next()
    assert capsys.readouterr().out == "called SearchHelper.replace_next with args {}\n"

def test_replace_and_prev(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.replace_and_prev()
    assert capsys.readouterr().out == "called SearchHelper.replace_next with args {'reverse': True}\n"

def test_add_dtd(monkeypatch, capsys):
    def mock_get_children(arg):
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        return ['first child']
    def mock_get_dtd():
        print('called EditorGui.get_dtd')
        return True, 'A doctype'
    def mock_get_dtd_no():
        print('called EditorGui.get_dtd')
        return False, ''
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.has_dtd = True
    testobj.gui.top = 'gui.top'
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    monkeypatch.setattr(testobj.gui, 'get_dtd', mock_get_dtd)
    testobj.add_or_remove_dtd()
    assert not testobj.has_dtd
    assert capsys.readouterr().out == ('called EditorGui.get_element_children with arg `gui.top`\n'
                                       'called EditorGui.do_delete_item with arg `first child`\n'
                                       'called EditorGui.adjust_dtd_menu\n'
                                       'called.Editor.mark_dirty with value `True`\n'
                                       'called Editor.refresh_preview\n'
                                       'called EditorGui.get_element_children with arg `gui.top`\n'
                                       'called EditorGui.ensure_item_visible with arg'
                                       ' `first child`\n')
    testobj.has_dtd = False
    testobj.add_or_remove_dtd()
    assert testobj.has_dtd
    assert capsys.readouterr().out == ("called EditorGui.get_dtd\n"
                                       "called EditorGui.addtreeitem with args"
                                       " ('gui.top', 'DOCTYPE A doctype', 'A doctype', 0)\n"
                                       "called EditorGui.adjust_dtd_menu\n"
                                       "called.Editor.mark_dirty with value `True`\n"
                                       "called Editor.refresh_preview\n"
                                       "called EditorGui.get_element_children with arg `gui.top`\n"
                                       "called EditorGui.ensure_item_visible with arg"
                                       " `first child`\n")
    testobj.has_dtd = False
    monkeypatch.setattr(testobj.gui, 'get_dtd', mock_get_dtd_no)
    testobj.add_or_remove_dtd()
    assert not testobj.has_dtd
    assert capsys.readouterr().out == "called EditorGui.get_dtd\n"

def test_add_css(monkeypatch, capsys):
    def mock_get_css_no():
        print('called EditorGui.get_css_data')
        return False, ''
    def mock_get_css_external():
        print('called EditorGui.get_css_data')
        return True, {'href': 'some_stylesheet'}
    def mock_get_css_internal():
        print('called EditorGui.get_css_data')
        return True, {'other': 'xxx', 'cssdata': 'yyy'}
    def mock_get_children_nohtml(arg):
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        return ['x']
    counter = 0
    def mock_get_children_nohead(arg):
        nonlocal counter
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        counter += 1
        if counter == 1:
            return [f'{testee.ELSTART} html']
        return ['first child']
    def mock_get_children(arg):
        nonlocal counter
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        counter += 1
        if counter == 1:
            return [f'{testee.ELSTART} html']
        if counter == 2:
            return [f'{testee.ELSTART} head']
        return ['first child']
    def mock_get_text(arg):
        print(f'called EditorGui.get_element_text with arg `{arg}`')
        return arg
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = setup_editor(monkeypatch, capsys)
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(testobj.gui, 'get_css_data', mock_get_css_no)
    testobj.gui.top = 'gui.top'
    testobj.add_css()
    assert capsys.readouterr().out == "called EditorGui.get_css_data\n"
    monkeypatch.setattr(testobj.gui, 'get_css_data', mock_get_css_external)
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children_nohtml)
    testobj.add_css()
    assert capsys.readouterr().out == ("called EditorGui.get_css_data\n"
                                       "called EditorGui.get_element_children with arg `gui.top`\n"
                                       "called EditorGui.get_element_text with arg `x`\n"
                                       "called EditorGui.meld with arg"
                                       " `Error: no <html> and/or no <head> element`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children_nohead)
    testobj.add_css()
    assert capsys.readouterr().out == ("called EditorGui.get_css_data\n"
                                       "called EditorGui.get_element_children with arg `gui.top`\n"
                                       "called EditorGui.get_element_text with arg `<> html`\n"
                                       "called EditorGui.get_element_children with arg `<> html`\n"
                                       "called EditorGui.get_element_text with arg `first child`\n"
                                       "called EditorGui.meld with arg"
                                       " `Error: no <html> and/or no <head> element`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    counter = 0
    testobj.add_css()
    assert capsys.readouterr().out == ("called EditorGui.get_css_data\n"
                                       "called EditorGui.get_element_children with arg `gui.top`\n"
                                       "called EditorGui.get_element_text with arg `<> html`\n"
                                       "called EditorGui.get_element_children with arg `<> html`\n"
                                       "called EditorGui.get_element_text with arg `<> head`\n"
                                       "called EditorGui.addtreeitem with args ('<> head',"
                                       " '<> link', {'href': 'some_stylesheet'}, -1)\n"
                                       "called.Editor.mark_dirty with value `True`\n"
                                       "called Editor.refresh_preview\n")
    monkeypatch.setattr(testobj.gui, 'get_css_data', mock_get_css_internal)
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    counter = 0
    testobj.add_css()
    assert capsys.readouterr().out == ("called EditorGui.get_css_data\n"
                                       "called EditorGui.get_element_children with arg `gui.top`\n"
                                       "called EditorGui.get_element_text with arg `<> html`\n"
                                       "called EditorGui.get_element_children with arg `<> html`\n"
                                       "called EditorGui.get_element_text with arg `<> head`\n"
                                       "called EditorGui.addtreeitem with args ('<> head',"
                                       " '<> style', {'other': 'xxx'}, -1)\n"
                                       "called EditorGui.addtreeitem with args ('node',"
                                       " 'yyy', 'yyy', -1)\n"
                                       "called.Editor.mark_dirty with value `True`\n"
                                       "called Editor.refresh_preview\n")


def test_check_if_adding_ok(monkeypatch, capsys):
    monkeypatch.setattr(MockEditorGui, 'get_element_text',lambda *x: 'text')
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
    testobj = setup_editor(monkeypatch, capsys)
    assert not testobj.check_if_adding_ok()
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.item = 'x'
    assert not testobj.check_if_adding_ok()
    monkeypatch.setattr(MockEditorGui, 'get_element_text',lambda *x: '<> text')
    testobj.item = 'x'
    assert testobj.check_if_adding_ok()

def test_convert_link(monkeypatch, capsys, tmp_path):
    # orig_abspath = testee.os.path.abspath
    # def mock_abspath(arg):
    #     print(f'called os.path.abspath with arg `{arg}`')
    #     orig_abspath(arg)
    # def mock_getcwd():
    #     print('called os.getcwd')
    #     return os.path.dirname(__path__)
    def mock_relpath(*args):
         print(f'called os.path.relpath with args', args)
         raise ValueError('os.path.relpath failed')
    def mock_relpath_2(*args):
         print(f'called os.path.relpath with args', args)
         return ''
    testobj = setup_editor(monkeypatch, capsys)
    with pytest.raises(ValueError) as exc:
        testobj.convert_link('', 'anything')
    assert str(exc.value) == 'link opgeven of cancel kiezen s.v.p'
    # monkeypatch.setattr(testee.os, 'getcwd', mock_getcwd)
    # monkeypatch.setattr(testee.os.path, 'abspath', mock_abspath)
    mock_link = tmp_path / 'htmledit' / 'test.html'
    mock_root = tmp_path / 'htmledit'
    # neither path exists at this time
    assert testobj.convert_link(str(mock_link), '') == str(mock_link)
    mock_root.mkdir()
    mock_link.touch()
    # now they do
    assert testobj.convert_link(str(mock_link), '') == '../../../..' + str(mock_link)
    assert testobj.convert_link(str(mock_link), mock_root) == 'htmledit/test.html'
    assert testobj.convert_link('/', 'anything') == '/'
    assert testobj.convert_link('http://here', 'anything') == 'http://here'
    assert testobj.convert_link('./here', 'anything') == './here'
    assert testobj.convert_link('../here', 'anything') == '../here'
    assert testobj.convert_link('file', 'this') == 'file'
    monkeypatch.setattr(testee.os.path, 'relpath', mock_relpath)
    with pytest.raises(ValueError) as exc:
        testobj.convert_link(str(mock_link), '')
    assert str(exc.value) == 'os.path.relpath failed'
    assert capsys.readouterr().out == ('called os.path.relpath with args'
                                       f" ('{mock_link}', '{testee.os.getcwd()}')\n")
    monkeypatch.setattr(testee.os.path, 'relpath', mock_relpath_2)
    with pytest.raises(ValueError) as exc:
        testobj.convert_link(str(mock_link), '')
    assert str(exc.value) == 'Unable to make this local link relative'
    assert capsys.readouterr().out == ('called os.path.relpath with args'
                                       f" ('{mock_link}', '{testee.os.getcwd()}')\n")

def test_add_link(monkeypatch, capsys):
    def mock_get_link_data():
        print('called EditorGui.get_link_data')
        return True, ('txt', 'data')
    def mock_get_link_data_2():
        print('called EditorGui.get_link_data')
        return False, ('', '')
    def mock_getelname(*args):
        print('called getelname with args', args)
    def mock_getshortname(*args):
        print('called getshortname with args', args)
    monkeypatch.setattr(testee, 'getelname', mock_getelname)
    monkeypatch.setattr(testee, 'getshortname', mock_getshortname)
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.get_link_data = mock_get_link_data
    testobj.item = 'item'
    testobj.add_link()
    assert capsys.readouterr().out == (
            "called EditorGui.get_link_data\n"
            "called getelname with args ('a', 'data')\n"
            "called EditorGui.addtreeitem with args ('item', None, 'data', -1)\n"
            "called getshortname with args ('txt',)\n"
            "called EditorGui.addtreeitem with args ('node', None, 'txt', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_link_data = mock_get_link_data_2
    testobj.add_link()
    assert capsys.readouterr().out == 'called EditorGui.get_link_data\n'
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
    testobj.add_link()
    assert capsys.readouterr().out == ''

def test_add_image(monkeypatch, capsys):
    def mock_get_image_data():
        print('called EditorGui.get_image_data')
        return True, ('txt', 'data')
    def mock_get_image_data_2():
        print('called EditorGui.get_image_data')
        return False, ('', '')
    def mock_getelname(*args):
        print('called getelname with args', args)
    monkeypatch.setattr(testee, 'getelname', mock_getelname)
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.get_image_data = mock_get_image_data
    testobj.item = 'item'
    testobj.add_image()
    assert capsys.readouterr().out == (
            "called EditorGui.get_image_data\n"
            "called getelname with args ('image', ('txt', 'data'))\n"
            "called EditorGui.addtreeitem with args ('item', None, ('txt', 'data'), -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_image_data = mock_get_image_data_2
    testobj.add_image()
    assert capsys.readouterr().out == 'called EditorGui.get_image_data\n'
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
    testobj.add_image()
    assert capsys.readouterr().out == ''

def test_add_audio(monkeypatch, capsys):
    def mock_get_audio_data():
        print('called EditorGui.get_audio_data')
        return True, ({'x': 'y'})
    def mock_get_audio_data_2():
        print('called EditorGui.get_audio_data')
        return False, ('', '')
    def mock_getelname(*args):
        print('called getelname with args', args)
    monkeypatch.setattr(testee, 'getelname', mock_getelname)
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.get_audio_data = mock_get_audio_data
    testobj.item = 'item'
    testobj.add_audio()
    assert capsys.readouterr().out == (
            "called EditorGui.get_audio_data\n"
            "called getelname with args ('audio', {'x': 'y', 'controls': ''})\n"
            "called EditorGui.addtreeitem with args ('item', None, {'x': 'y', 'controls': ''}, -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_audio_data = mock_get_audio_data_2
    testobj.add_audio()
    assert capsys.readouterr().out == 'called EditorGui.get_audio_data\n'
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
    testobj.add_audio()
    assert capsys.readouterr().out == ''

def test_add_video(monkeypatch, capsys):
    def mock_get_video_data():
        print('called EditorGui.get_video_data')
        return True, ({'src': 'y.mp4'})
    def mock_get_video_data_2():
        print('called EditorGui.get_video_data')
        return False, ('', '')
    def mock_getelname(*args):
        print('called getelname with args', args)
    monkeypatch.setattr(testee, 'getelname', mock_getelname)
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.get_video_data = mock_get_video_data
    testobj.item = 'item'
    testobj.add_video()
    assert capsys.readouterr().out == (
            "called EditorGui.get_video_data\n"
            "called getelname with args ('video', {'controls': ''})\n"
            "called EditorGui.addtreeitem with args ('item', None, {'controls': ''}, -1)\n"
            "called getelname with args ('source', {'src': 'y.mp4', 'type': 'video/mp4'})\n"
            "called EditorGui.addtreeitem with args ('node', None, {'src': 'y.mp4',"
            " 'type': 'video/mp4'}, -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_video_data = mock_get_video_data_2
    testobj.add_video()
    assert capsys.readouterr().out == 'called EditorGui.get_video_data\n'
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
    testobj.add_video()
    assert capsys.readouterr().out == ''

def test_add_list(monkeypatch, capsys):
    def mock_getelname(*args):
        print('called getelname with args', args)
        return args[0] or 'elname'
    def mock_getshortname(*args):
        print('called getshortname with args', args)
        return args[0] or 'shortname'
    def mock_get_no_list_data():
        print('called EditorGui.get_list_data')
        return False, ('', '')
    def mock_get_list_data():
        print('called EditorGui.get_list_data')
        return True, ('', '')
    def mock_get_list_data_dl():
        print('called EditorGui.get_list_data')
        return True, ('dl', [('name', 'text')])
    def mock_get_list_data_other():
        print('called EditorGui.get_list_data')
        return True, ('x', [('itemtext', '')])
    monkeypatch.setattr(testee, 'getelname', mock_getelname)
    monkeypatch.setattr(testee, 'getshortname', mock_getshortname)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = setup_editor(monkeypatch, capsys)
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
    testobj.gui.get_list_data = mock_get_no_list_data
    testobj.add_list()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
    testobj.add_list()
    assert capsys.readouterr().out == 'called EditorGui.get_list_data\n'
    testobj.gui.get_list_data = mock_get_list_data
    testobj.item = 'testobjitem'
    testobj.add_list()
    assert capsys.readouterr().out == (
            'called EditorGui.get_list_data\n'
            "called getelname with args ('',)\n"
            "called EditorGui.addtreeitem with args ('testobjitem', 'elname', None, -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_list_data = mock_get_list_data_dl
    testobj.item = 'testobjitem'
    testobj.add_list()
    assert capsys.readouterr().out == (
            "called EditorGui.get_list_data\n"
            "called getelname with args ('dl',)\n"
            "called EditorGui.addtreeitem with args ('testobjitem', 'dl', None, -1)\n"
            "called getelname with args ('dt',)\n"
            "called EditorGui.addtreeitem with args ('node', 'dt', None, -1)\n"
            "called getshortname with args ('name',)\n"
            "called EditorGui.addtreeitem with args ('node', 'name', 'name', -1)\n"
            "called getelname with args ('dd',)\n"
            "called EditorGui.addtreeitem with args ('node', 'dd', None, -1)\n"
            "called getshortname with args ('text',)\n"
            "called EditorGui.addtreeitem with args ('node', 'text', 'text', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_list_data = mock_get_list_data_other
    testobj.item = 'testobjitem'
    testobj.add_list()
    assert capsys.readouterr().out == (
            "called EditorGui.get_list_data\n"
            "called getelname with args ('x',)\n"
            "called EditorGui.addtreeitem with args ('testobjitem', 'x', None, -1)\n"
            "called getelname with args ('li',)\n"
            "called EditorGui.addtreeitem with args ('node', 'li', None, -1)\n"
            "called getshortname with args ('itemtext',)\n"
            "called EditorGui.addtreeitem with args ('node', 'itemtext', 'itemtext', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")

def test_add_table(monkeypatch, capsys):
    def mock_getelname(*args):
        print('called getelname with args', args)
    def mock_getshortname(*args):
        print('called getshortname with args', args)
    def mock_get_no_table_data():
        print('called EditorGui.get_table_data')
        return False, ('', '')
    def mock_get_table_data():
        print('called EditorGui.get_table_data')
        return True, ('empty table', False, '', [])
    def mock_get_table_data_headers():
        print('called EditorGui.get_table_data')
        return True, ('table with headers but no items', True, ['x', 'y'], [])
    def mock_get_table_data_items():
        print('called EditorGui.get_table_data')
        return True, ('table with items and empty headers', True, ['', ''], [('x', 'y')])
    monkeypatch.setattr(testee, 'getelname', mock_getelname)
    monkeypatch.setattr(testee, 'getshortname', mock_getshortname)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    testobj = setup_editor(monkeypatch, capsys)
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
    testobj.gui.get_table_data = mock_get_no_table_data
    testobj.add_table()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
    testobj.add_table()
    assert capsys.readouterr().out == 'called EditorGui.get_table_data\n'
    testobj.gui.get_table_data = mock_get_table_data
    testobj.item = 'testobjitem'
    testobj.add_table()
    assert capsys.readouterr().out == (
            'called EditorGui.get_table_data\n'
            "called getelname with args ('table', {'summary': 'empty table'})\n"
            "called EditorGui.addtreeitem with args"
            " ('testobjitem', None, {'summary': 'empty table'}, -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_table_data = mock_get_table_data_headers
    testobj.item = 'testobjitem'
    testobj.add_table()
    assert capsys.readouterr().out == (
            'called EditorGui.get_table_data\n'
            "called getelname with args ('table', {'summary': 'table with headers but no items'})\n"
            "called EditorGui.addtreeitem with args"
            " ('testobjitem', None, {'summary': 'table with headers but no items'}, -1)\n"
            "called getelname with args ('tr',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getelname with args ('th',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getshortname with args ('x',)\n"
            "called EditorGui.addtreeitem with args ('node', None, 'x', -1)\n"
            "called getelname with args ('th',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getshortname with args ('y',)\n"
            "called EditorGui.addtreeitem with args ('node', None, 'y', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_table_data = mock_get_table_data_items
    testobj.item = 'testobjitem'
    testobj.add_table()
    assert capsys.readouterr().out == (
            'called EditorGui.get_table_data\n'
            "called getelname with args "
            "('table', {'summary': 'table with items and empty headers'})\n"
            "called EditorGui.addtreeitem with args"
            " ('testobjitem', None, {'summary': 'table with items and empty headers'}, -1)\n"
            "called getelname with args ('tr',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getelname with args ('th',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getshortname with args ('&nbsp;',)\n"
            "called EditorGui.addtreeitem with args ('node', None, '&nbsp;', -1)\n"
            "called getelname with args ('th',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getshortname with args ('&nbsp;',)\n"
            "called EditorGui.addtreeitem with args ('node', None, '&nbsp;', -1)\n"
            "called getelname with args ('tr',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getelname with args ('td',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getshortname with args ('x',)\n"
            "called EditorGui.addtreeitem with args ('node', None, 'x', -1)\n"
            "called getelname with args ('td',)\n"
            "called EditorGui.addtreeitem with args ('node', None, None, -1)\n"
            "called getshortname with args ('y',)\n"
            "called EditorGui.addtreeitem with args ('node', None, 'y', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")

def test_validate(monkeypatch, capsys):
    def mock_mkdtemp():
        print('called tempfile.mkdtemp')
        return 'tempdir'
    def mock_prettify():
        print('called Editor.soup.prettify')
        return 'prettified soup'
    def mock_data2soup(self):
        print('called Editor.data2soup')
        self.soup = types.SimpleNamespace(prettify=mock_prettify)
    def mock_write(*args):
        print('called path.write_text with args', args)
    monkeypatch.setattr(testee.tempfile, 'mkdtemp', mock_mkdtemp)
    monkeypatch.setattr(testee.pathlib.Path, 'write_text', mock_write)
    monkeypatch.setattr(testee.Editor, 'data2soup', mock_data2soup)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.tree_dirty = False
    testobj.xmlfn = 'test.html'
    testobj.validate()
    assert capsys.readouterr().out == "called EditorGui.validate with args ('test.html', True)\n"
    testobj.tree_dirty = True
    testobj.validate()
    assert capsys.readouterr().out == ("called tempfile.mkdtemp\n"
                                       "called Editor.data2soup\n"
                                       "called Editor.soup.prettify\n"
                                       "called path.write_text with args"
                                       " (PosixPath('tempdir/ashe_check.html'), 'prettified soup')\n"
                                       "called EditorGui.validate with args"
                                       " ('tempdir/ashe_check.html', False)\n")
    testobj.tree_dirty = False
    testobj.xmlfn = ''
    testobj.validate()
    assert capsys.readouterr().out == ("called tempfile.mkdtemp\n"
                                       "called Editor.data2soup\n"
                                       "called Editor.soup.prettify\n"
                                       "called path.write_text with args"
                                       " (PosixPath('tempdir/ashe_check.html'), 'prettified soup')\n"
                                       "called EditorGui.validate with args"
                                       " ('tempdir/ashe_check.html', False)\n")


def test_do_validate(monkeypatch, capsys):
    def mock_run(*args, **kwargs):
        print("call subprocess.run with args", args, kwargs)
        pathlib.Path('/tmp/ashe_check').write_text('ashe_check')
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    testobj = setup_editor(monkeypatch, capsys)
    assert testobj.do_validate('test.html') == 'ashe_check'
    assert capsys.readouterr().out == ("call subprocess.run with args"
                                       " (['tidy', '-e', '-f', '/tmp/ashe_check', 'test.html'],)"
                                       " {'check': False}\n")

def test_view_code(monkeypatch, capsys):
    def mock_data2soup(self, *args, **kwargs):
        print('called Editor.data2soup with args', args, kwargs)
    def mock_prettify(*args):
        print('called BeautifulSoup.prettify')
    def mock_show_code(*args):
        print('called EditorGui.show_code')
    monkeypatch.setattr(testee.Editor, 'data2soup', mock_data2soup)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.soup = types.SimpleNamespace(prettify=mock_prettify)
    testobj.gui.show_code = mock_show_code
    testobj.view_code()
    assert capsys.readouterr().out == ('called Editor.data2soup with args () {}\n'
                                       'called BeautifulSoup.prettify\n'
                                       'called EditorGui.show_code\n')

def test_about(monkeypatch, capsys):
    testobj = setup_editor(monkeypatch, capsys)
    testobj.about()
    assert capsys.readouterr().out == f'called EditorGui.meld with arg `{testee.ABOUT}`\n'

#-- EditorHelper ---------------------
def test_editorhelper_init(monkeypatch, capsys):
    testobj = testee.EditorHelper(MockEditor())
    assert hasattr(testobj, 'editor')
    assert hasattr(testobj, 'gui')

def _test_editorhelper_edit(monkeypatch, capsys):
    testobj = testee.EditorHelper(MockEditor())

def _test_editorhelper_comment(monkeypatch, capsys):
    testobj = testee.EditorHelper(MockEditor())

def _test_editorhelper_comment_out(monkeypatch, capsys):
    testobj = testee.EditorHelper(MockEditor())

def _test_editorhelper_copy(monkeypatch, capsys):
    testobj = testee.EditorHelper(MockEditor())

def _test_editorhelper_paste(monkeypatch, capsys):
    testobj = testee.EditorHelper(MockEditor())

def _test_editorhelper_insert(monkeypatch, capsys):
    testobj = testee.EditorHelper(MockEditor())

def _test_editorhelper_add_text(monkeypatch, capsys):
    testobj = testee.EditorHelper(MockEditor())


#-- SearchHelper ---------------------
def test_searchhelper_init(monkeypatch, capsys):
    testobj = testee.SearchHelper(MockEditor())
    assert hasattr(testobj, 'editor')
    assert hasattr(testobj, 'gui')
    assert testobj.search_args == []
    assert testobj.replace_args == []
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'


def test_searchhelper_search_from(monkeypatch, capsys):
    def mock_flatten(self, *args):
        return (('top', 'filenaam', {}), ('ele', '<> html', {}))
    def mock_next(self, *args):
        print('called search.find_next() with args', args)
        return 'pos', 1
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_from('top')
    assert capsys.readouterr().out == ('called EditorGui.__init__\ncalled Editor.__init__()\n'
                                       "called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", False)\n"
                                       'called EditorGui.set_selected_item(`1`)\n')
    testobj.search_from('top', True)
    assert capsys.readouterr().out == ("called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", True)\n"
                                       'called EditorGui.set_selected_item(`1`)\n')
    testobj.search_from('ele')
    assert capsys.readouterr().out == ("called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))\n"
                                       'called EditorGui.set_selected_item(`1`)\n')
    testobj.search_from('ele', True)
    assert capsys.readouterr().out == ("called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", True, (1, 'ele'))\n"
                                       'called EditorGui.set_selected_item(`1`)\n')
    def mock_next(self, *args):
        return None
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_from('ele')
    assert capsys.readouterr().out == ('called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')


def test_searchhelper_search_next(monkeypatch, capsys):
    def mock_flatten(self, *args):
        return (('top', 'filenaam', {}), ('ele', '<> html', {}))
    def mock_next(self, *args):
        print('called search.find_next() with args', args)
        return 'pos', 1
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_next()
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    testobj.search_args = ('x', 'y', 'z', 'a')
    testobj.search_pos = (1, 'ele')
    testobj.search_next()
    assert capsys.readouterr().out == ("called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))\n"
                                       'called EditorGui.set_selected_item(`1`)\n')
    def mock_next(self, *args):
        return None
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_specs = 'search_specs'
    testobj.search_next()
    assert capsys.readouterr().out == ('called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')


def test_searchhelper_replace_from(monkeypatch, capsys):
    def mock_flatten(self, *args):
        return (('top', 'filenaam', {}), ('ele', '<> html', {}))
    def mock_next(self, *args):
        print('called search.find_next() with args', args)
        return 'pos', 1
    def mock_replace(*args):
        print(f'called search.replace_and_find() with args `{args[0]}`, `{args[1]}`')
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    monkeypatch.setattr(testobj, 'replace_and_find', mock_replace)
    testobj.replace_from('top')
    assert capsys.readouterr().out == ('called EditorGui.__init__\ncalled Editor.__init__()\n'
                                       "called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", False)\n"
                                       "called search.replace_and_find() with args `('pos', 1)`,"
                                       ' `False`\n')
    testobj.replace_from('top', True)
    assert capsys.readouterr().out == ("called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", True)\n"
                                       "called search.replace_and_find() with args `('pos', 1)`,"
                                       ' `True`\n')
    testobj.replace_from('ele')
    assert capsys.readouterr().out == ("called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))\n"
                                       "called search.replace_and_find() with args `('pos', 1)`,"
                                       ' `False`\n')
    testobj.replace_from('ele', True)
    assert capsys.readouterr().out == ("called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", True, (1, 'ele'))\n"
                                       "called search.replace_and_find() with args `('pos', 1)`,"
                                       ' `True`\n')
    def mock_next(self, *args):
        return None
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.replace_from('ele')
    assert capsys.readouterr().out == ('called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')


def test_searchhelper_replace_next(monkeypatch, capsys):
    def mock_replace(*args):
        print(f'called search.replace_and_find() with args `{args[0]}`, `{args[1]}`')
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'replace_and_find', mock_replace)
    testobj.replace_next()
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.search_pos = '1'
    testobj.replace_next()
    assert capsys.readouterr().out == 'called search.replace_and_find() with args `1`, `False`\n'
    testobj.replace_next(True)
    assert capsys.readouterr().out == 'called search.replace_and_find() with args `1`, `True`\n'


def test_searchhelper_replace_and_find(monkeypatch, capsys):
    def mock_element(self, *args):
        print('called search.replace_element()')
    def mock_attr(self, *args):
        print('called search.replace_attr()')
    def mock_text(self, *args):
        print('called search.replace_text()')
    def mock_flatten(self, *args):
        return (('top', 'filenaam', {}), ('ele', '<> html', {}))
    def mock_next(self, *args):
        print('called search.find_next() with args', args)
        return 'pos', 1
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'replace_element', mock_element)
    monkeypatch.setattr(testobj, 'replace_attr', mock_attr)
    monkeypatch.setattr(testobj, 'replace_text', mock_text)
    monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_args = ('x', 'y', 'z', 'a')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_and_find((1, 'ele'), False)
    assert testobj.search_pos == ('pos', 1)
    assert capsys.readouterr().out == ('called EditorGui.__init__\ncalled Editor.__init__()\n'
                                       'called search.replace_element()\n'
                                       'called search.replace_attr()\n'
                                       'called search.replace_text()\n'
                                       "called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))\n"
                                       'called EditorGui.set_selected_item(`1`)\n')
    def mock_next(self, *args):
        return None
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_specs = 'search_specs'
    testobj.replace_next()
    assert capsys.readouterr().out == ('called search.replace_element()\n'
                                       'called search.replace_attr()\n'
                                       'called search.replace_text()\n'
                                       'called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')


def test_searchhelper_find_next(monkeypatch, capsys):
    treedata = [('ele1', '<> html', {}),
                ('ele2', '<> div', {}),
                ('ele3', '<> div', {'id': '1'}),
                ('text', 'some text', {}),
                ('ele4', '<> div', {'id': '2'}),
                ('ele5', '<> div', {'class': 'footer'})]
    testobj = testee.SearchHelper(MockEditor())
    # not findable
    assert testobj.find_next(treedata, ('p', '', '', '')) is None
    assert testobj.find_next(treedata, ('div', 'test', '', '')) is None
    assert testobj.find_next(treedata, ('div', 'class', 'header', '')) is None
    assert testobj.find_next(treedata, ('div', '', '', 'cheese')) is None
    # findable
    assert testobj.find_next(treedata, ('div', '', '', '')) == (1, 'ele2')
    assert testobj.find_next(treedata, ('div', 'id', '', '')) == (2, 'ele3')
    assert testobj.find_next(treedata, ('div', 'class', '', ''), pos=(2, 'ele3')) == (5, 'ele5')
    assert testobj.find_next(treedata, ('div', 'id', '2', '')) == (4, 'ele4')
    assert testobj.find_next(treedata, ('div', '', '', 'tex')) == (3, 'text')
    # backwards - dit klopt niet overal
    assert testobj.find_next(treedata, ('html', '', '', ''), True) == (0, 'ele1')
    assert testobj.find_next(treedata, ('div', 'class', '', ''), True) == (0, 'ele5')
    assert testobj.find_next(treedata, ('div', 'id', '1', ''), True) == (2, 'ele3')
    assert testobj.find_next(treedata, ('div', '', '', 'ome'), True) == (2, 'text')


def test_searchhelper_flatten_tree_1(monkeypatch, capsys):
    "no children"
    testobj = testee.SearchHelper(MockEditor())
    data = testobj.flatten_tree('top')
    assert data == []
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'


def test_searchhelper_flatten_tree_2(monkeypatch, capsys):
    "regular"
    def mock_element_text(self, node):
        self.textcounter += 1
        data = ['', 'filenaam'] + 2 * ['<> html'] + 2 * ['<> div id="1"'] + 2 * ['some text']
        return data[self.textcounter]
    def mock_element_children(self, node):
        self.childcounter += 1
        return ['', ['ele1'], ['ele2'], ['text'], []][self.childcounter]
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_children', mock_element_children)
    testobj = testee.SearchHelper(MockEditor())
    # import pdb; pdb.set_trace()
    data = testobj.flatten_tree('top')
    assert data == [('ele1', '<> html', {}), ('ele2', '<> div', {}), ('text', 'some text', {})]
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'


def test_searchhelper_flatten_tree_3(monkeypatch, capsys):
    "commented"
    def mock_element_text(self, node):
        self.textcounter += 1
        data = ['', 'fnm'] + 2 * ['<!> <> html'] + 2 * ['<!> <> div id="1"'] + 2 * ['<!> some text']
        return data[self.textcounter]
    def mock_element_children(self, node):
        self.childcounter += 1
        return [['top'], ['ele1'], ['ele2'], ['text'], []][self.childcounter]
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_children', mock_element_children)
    testobj = testee.SearchHelper(MockEditor())
    data = testobj.flatten_tree('top')
    assert data == [('ele1', '<!> <> html', {}), ('ele2', '<!> <> div', {}),
                    ('text', '<!> some text', {})]
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'


def test_searchhelper_replace_element(monkeypatch, capsys):
    def mock_element_text(self, node):
        self.textcounter += 1
        data = ['', '<> html', '<> div id="1"', '<!> <> hr', '<!> <> p class="centered"']
        return data[self.textcounter]
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_element(('el1',))
    assert capsys.readouterr().out == ('called EditorGui.__init__\ncalled Editor.__init__()\n'
                                       'called EditorGui.set_element_text for `el1` to `<> x`\n')
    testobj.replace_element(('el2',))
    assert capsys.readouterr().out == 'called EditorGui.set_element_text for `el2` to `<> x id="1"`\n'
    testobj.replace_element(('el3',))
    assert capsys.readouterr().out == 'called EditorGui.set_element_text for `el3` to `<!> <> x`\n'
    testobj.replace_element(('el4',))
    assert capsys.readouterr().out == ('called EditorGui.set_element_text for `el4` to `<!> <> x '
                                       'class="centered"`\n')


def test_searchhelper_replace_attr(monkeypatch, capsys):
    def mock_element_data(self, node):
        return {"id": "1"}
    def mock_element_text(self, node):
        return '<> html'
    monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_element_data)
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', 'y', '', 'a')
    testobj.replace_attr(('el1',))
    assert capsys.readouterr().out == (
            'called EditorGui.__init__\ncalled Editor.__init__()\n'
            "called EditorGui.set_element_data for `el1` to `{'y': '1'}`\n"
            "called EditorGui.set_element_text for `el1` to `<> html`\n")
    def mock_element_text(self, node):
        return '<!> <> div'
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_attr(('el2',))
    assert capsys.readouterr().out == (
            'called EditorGui.__init__\ncalled Editor.__init__()\n'
            "called EditorGui.set_element_data for `el2` to `{'y': 'z'}`\n"
            "called EditorGui.set_element_text for `el2` to `<!> <> div`\n")
    def mock_element_text(self, node):
        return '<> p'
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', '', 'z', 'a')
    testobj.replace_attr(('el3',))
    assert capsys.readouterr().out == (
            'called EditorGui.__init__\ncalled Editor.__init__()\n'
            "called EditorGui.set_element_data for `el3` to `{'id': 'z'}`\n"
            'called EditorGui.set_element_text for `el3` to `<> p id="z"`\n')
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', '=/= y', 'z', 'a')
    testobj.replace_attr(('el4',))
    assert capsys.readouterr().out == (
            'called EditorGui.__init__\ncalled Editor.__init__()\n'
            "called EditorGui.set_element_data for `el4` to `{'id': 'z'}`\n"
            'called EditorGui.set_element_text for `el4` to `<> p id="z"`\n')


def test_searchhelper_replace_text(monkeypatch, capsys):
    def mock_element_text(self, node):
        return 'some text'
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'y', 'z', 'tex')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_text(('ele',))
    assert capsys.readouterr().out == ('called EditorGui.__init__\ncalled Editor.__init__()\n'
                                       "called EditorGui.set_element_text for `ele` to `some at`\n")
