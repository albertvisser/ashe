"""unittests for ./ashe/base.py
"""
import pathlib
import types
import pytest
from ashe import base as testee

class MockElement:
    """stub for BeautifulSoup.Element
    """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """stub
        """
        return self.name

    def __str__(self):
        """stub
        """
        return self.name


class MockCssEditor:
    """stub for cssedit.editor.Editor
    """
    def __init__(self, *args, **kwargs):
        print('called CssEditor.__init__ with args', args, kwargs)
    def open(self, *args, **kwargs):
        """stub
        """
        print('called CssEditor.open with args', args, kwargs)
    def show_from_external(self):
        """stub
        """
        print('called CssEditor.show_from_external')


class MockEditorGui:
    """stub for .gui.EditorGui
    """
    top = 'top'
    # def __init__(self):
    #     print('called gui.__init__()')
    def __init__(self, *args, **kwargs):
        print('called EditorGui.__init__')
        self.textcounter = self.datacounter = self.childcounter = 0
    def go(self):
        """stub
        """
        print('called EditorGui.go()')
    def close(self):
        """stub
        """
        print('called EditorGui.close()')
    def get_search_args(self, **kwargs):
        """stub
        """
        if kwargs.get('replace', True):
            return True, (('x', 'y', 'z', 'a'), 'search_specs', ('q', 'r', 's', 't'))
        return True, (('x', 'y', 'z', 'a'), 'search_specs')
    def get_selected_item(self):
        """stub
        """
        print('called EditorGui.get_selected_item')
    def set_selected_item(self, *args):
        """stub
        """
        print(f'called EditorGui.set_selected_item(`{args[0]}`)')
    def meld(self, msg):
        """stub
        """
        print(f'called EditorGui.meld with arg `{msg}`')
    def show_statusbar_message(self, msg):
        """stub
        """
        print(f'called EditorGui.show_statusbar_message with arg `{msg}`')
    def get_element_parent(self, node):
        """stub
        """
        return ''
    def get_element_text(self, node):
        """stub
        """
        return ''
    def set_element_text(self, node, data):
        """stub
        """
        print(f'called EditorGui.set_element_text with args `{node}`, `{data}`')
    def get_element_data(self, node):
        """stub
        """
        return {}
    def set_element_data(self, node, data):
        """stub
        """
        print(f'called EditorGui.set_element_data with args `{node}`, `{data}`')
    def set_item_expanded(self, node, value):
        """stub
        """
        print(f'called EditorGui.set_item_expanded with args `{node}`, `{value}`')
    def get_screen_title(self):
        """stub
        """
        return 'screen title'
    def set_screen_title(self, text):
        """stub
        """
        print(f'called EditorGui.set_screen_title with arg `{text}`')
    def get_element_children(self, node):
        """stub
        """
        return []  # 'node1', 'node2'
    def get_element_parentpos(self, *args):
        """stub
        """
        return '', 0
    def addtreetop(self, *args):
        """stub
        """
        print('called EditorGui.addtreetop with args', args)
    def addtreeitem(self, *args):
        """stub
        """
        print('called EditorGui.addtreeitem with args', args)
        return 'node'
    def adjust_dtd_menu(self):
        """stub
        """
        print('called EditorGui.adjust_dtd_menu')
    def do_delete_item(self, arg):
        """stub
        """
        print(f'called EditorGui.do_delete_item with arg `{arg}`')
        return 'preceding item'
    def init_tree(self, *args):
        """stub
        """
        print('called EditorGui.init_tree with args', args)
    def ensure_item_visible(self, arg):
        """stub
        """
        print(f'called EditorGui.ensure_item_visible with arg `{arg}`')
    def ask_for_open_filename(self):
        """stub
        """
        return True, 'x'
    def ask_for_save_filename(self):
        """stub
        """
        return True, 'x'
    def ask_how_to_continue(self):
        """stub
        """
        return True, 'x'
    def get_dtd(self):
        """stub
        """
        return True, 'x'
    def get_css_data(self):
        """stub
        """
        return True, 'x'
    def validate(self, *args):
        """stub
        """
        print('called EditorGui.validate with args', args)
    def do_add_element(self, arg):
        """stub
        """
        print(f'called EditorGui.do_add_element with arg `{arg}`')
        return False, ()
    def do_add_textvalue(self, arg):
        """stub
        """
        print(f'called EditorGui.do_add_textvalue with arg `{arg}`')
        return False, ()


class MockManager:
    """stub for base.CssManager
    """
    def __init__(self, *args):
        print('called CssManager.__init__()')


class MockEditorHelper:
    """stub for base.EditorHelper
    """
    def __init__(self, *args):
        print('called EditorHelper.__init__')

    def edit(self):
        """stub
        """
        print('called EditorHelper.edit')

    def comment(self):
        """stub
        """
        print('called EditorHelper.comment')

    def copy(self, **kwargs):
        """stub
        """
        print('called EditorHelper.copy with args', kwargs)

    def paste(self, **kwargs):
        """stub
        """
        print('called EditorHelper.paste with args', kwargs)

    def insert(self, **kwargs):
        """stub
        """
        print('called EditorHelper.insert with args', kwargs)

    def add_text(self, **kwargs):
        """stub
        """
        print('called EditorHelper.add_text with args', kwargs)


class MockSearchHelper:
    """stub for base.SearchHelper
    """
    def __init__(self, *args):
        print('called SearchHelper.__init__')

    def search(self, **kwargs):
        """stub
        """
        print('called SearchHelper.search with args', kwargs)

    def search_from(self, *args, **kwargs):
        """stub
        """
        print('called SearchHelper.search_from with args', args, kwargs)

    def search_next(self, **kwargs):
        """stub
        """
        print('called SearchHelper.search_next with args', kwargs)

    def replace_from(self, *args, **kwargs):
        """stub
        """
        print('called SearchHelper.replace_from with args', args, kwargs)

    def replace_next(self, **kwargs):
        """stub
        """
        print('called SearchHelper.replace_next with args', kwargs)


class MockEditor:
    """stub for base.Editor
    """
    def __init__(self):
        self.gui = MockEditorGui()
        print('called Editor.__init__()')


def test_getelname():
    """unittest for base.getelname
    """
    testelement = MockElement('elem')
    assert testee.getelname(testelement,
                            {'id': '15', 'name': 'Me'}) == f'{testee.ELSTART} elem id="15" name="Me"'
    testelement = MockElement('div')
    # beautifulsoup heeft een trucje dat als je het element object opvraagt dat je dan de waarde
    # van "name" krijgt als ik dat wil fixen moet ik wat uitzoekwerk doen, kan ook kijken of ik
    # de inner functie naar buiten kan halen
    assert testee.getelname(testelement, {'class': 'body'}) == f'{testee.ELSTART} div'
    assert testee.getelname(testelement, comment=True) == f'{testee.CMELSTART} div'


def test_get_tag_from_elname_old():
    """unittest for base.get_tag_from_elname_old
    """
    assert testee.get_tag_from_elname_old('  some tag') == 'tag'
    assert testee.get_tag_from_elname_old('some tag  ') == 'tag'
    assert testee.get_tag_from_elname_old('some tag') == 'tag'
    with pytest.raises(IndexError):
        assert testee.get_tag_from_elname_old('text') == ''
    assert testee.get_tag_from_elname_old('more text') == 'text'
    assert testee.get_tag_from_elname_old('text with more words') == 'with'
    with pytest.raises(IndexError):
        assert testee.get_tag_from_elname_old(f'{testee.ELSTART}') == 'tag'
    assert testee.get_tag_from_elname_old(f'{testee.ELSTART} tag') == 'tag'
    assert testee.get_tag_from_elname_old(f'{testee.ELSTART} tag plus') == 'tag'
    # niet realistisch:
    assert testee.get_tag_from_elname_old(f'{testee.CMELSTART}') == f'{testee.ELSTART}'
    assert testee.get_tag_from_elname_old(f'{testee.CMSTART} comment') == 'comment'
    assert testee.get_tag_from_elname_old(f'{testee.CMELSTART} style') == f'{testee.ELSTART}'
    assert testee.get_tag_from_elname_old(f'{testee.CMELSTART} commented') == f'{testee.ELSTART}'
    # laatste twee wel realistisch maar moet 'style' zijn


def test_get_tag_from_elname():
    """unittest for base.get_tag_from_elname
    """
    assert testee.get_tag_from_elname('text') == ''
    assert testee.get_tag_from_elname('more text') == ''
    assert testee.get_tag_from_elname('text with more words') == ''
    assert testee.get_tag_from_elname(f'{testee.ELSTART}') == ''
    assert testee.get_tag_from_elname(f'{testee.ELSTART} tag') == 'tag'
    assert testee.get_tag_from_elname(f'{testee.ELSTART} tag plus') == 'tag'
    assert testee.get_tag_from_elname(f'{testee.CMELSTART}') == ''
    assert testee.get_tag_from_elname(f'{testee.CMSTART} comment') == ''
    assert testee.get_tag_from_elname(f'{testee.CMELSTART} style') == 'style'
    assert testee.get_tag_from_elname(f'{testee.CMELSTART} commented element') == 'commented'


def test_get_shortname():
    """unittest for base.get_shortname
    """
    assert testee.getshortname('some\nname') == 'some [+]'
    assert testee.getshortname('looooooooooooooooooooooooooooong name') == (
        'looooooooooooooooooooooooooooo...')
    assert testee.getshortname('looooooooooooooooooooooooooooong\name') == (
        'looooooooooooooooooooooooooooo... [+]')
    assert testee.getshortname('name', comment=True) == '<!> name'


# -- CssManager -----------------------
def test_cssmanager_init(monkeypatch):
    """unittest for base.cssmanager_init
    """
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
    """stub for setting up CssManager
    """
    print('called CssManager.__init__ with args', args)
    self._parent = types.SimpleNamespace(gui=types.SimpleNamespace(app='gui_app'))


def test_call_editor(monkeypatch, capsys):
    """unittest for base.call_editor
    """
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
        """stub
        """
        def __init__(self, *args, **kwargs):
            print('called gui.TextDialog.__init__ with args', args, kwargs)
        def __repr__(self):
            """stub
            """
            return 'MockTextDialog'
    def mock_call(*args):
        """stub
        """
        print('called ashegui.call_dialog with args', args)
        return False, None
    def mock_call_2(*args):
        """stub
        """
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


# 161->166
def test_call_editor_for_stylesheet(monkeypatch, capsys):
    """unittest for base.call_editor_for_stylesheet
    """
    def mock_meld(mld):
        """stub
        """
        print(f'called ashegui.meld with arg `{mld}`')
    def mock_touch(mld):
        """stub
        """
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
    # monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda *x: True)
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
    """unittest for base.call_from_inline
    """
    def mock_call(self, *args):
        """stub
        """
        print('called CssManager.call_editor with args', args)
    monkeypatch.setattr(testee.CssManager, '__init__', mock_cssman_init)
    monkeypatch.setattr(testee.CssManager, 'call_editor', mock_call)
    testobj = testee.CssManager()
    assert capsys.readouterr().out == 'called CssManager.__init__ with args ()\n'
    testobj.call_from_inline(types.SimpleNamespace(), 'styledata')
    assert capsys.readouterr().out == ("called CssManager.call_editor with args"
                                       " (namespace(styledata='styledata'), 'style')\n")


# -- Editor ---------------------------
def mock_refresh(self):
    """stub
    """
    print('called Editor.refresh_preview')


def mock_mark_dirty(self, value):
    """stub
    """
    print(f'called.Editor.mark_dirty with value `{value}`')


def mock_init_editor(self, filename):
    """stub for initializing Editor
    """
    print(f'called Editor.__init__ with filename `{filename}`')
    self.xmlfn = filename
    self.root = 'root'
    self.gui = MockEditorGui()
    # self.cssm = MockManager()
    self.edhlp = MockEditorHelper()
    self.srchhlp = MockSearchHelper()


def setup_editor(monkeypatch, capsys):
    """stub for using Editor in tests
    """
    monkeypatch.setattr(testee.Editor, '__init__', mock_init_editor)
    testobj = testee.Editor('')
    assert capsys.readouterr().out == ('called Editor.__init__ with filename ``\n'
                                       'called EditorGui.__init__\n'
                                       'called EditorHelper.__init__\n'
                                       'called SearchHelper.__init__\n')
    return testobj


def test_editor_init(monkeypatch, capsys):
    """unittest for base.Editor.init
    """
    def mock_file2soup(self, arg):
        """stub
        """
        print(f'called Editor.file2soup with arg `{arg}`')
    def mock_soup2data(self):
        """stub
        """
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
    """unittest for Editor.file2soup
    """
    def mock_bs(*args):
        """stub
        """
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
    """unittest for Editor.soup2data
    """
    def mock_add_node(self, *args):
        """stub
        """
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
    """unittest for Editor.add_node_to_tree
    """
    def mock_find(*args):
        """stub
        """
        print('called Tag.find_all with args', args)
        return [types.SimpleNamespace(contents=['first body'])]
    class MockBS:
        """stub
        """
        def BeautifulSoup(*args):
            """stub
            """
            print('called BeautifulSoup with args', args)
            return types.SimpleNamespace(find_all=mock_find)
        class Tag:
            """stub
            """
            def __init__(self):
                self.name = 'tagname'
                self.attrs = {'x': '%SOUP-ENCODING%', 'y': 'qqq', 'z': ['a', 'b']}
                self.contents = []
        class Doctype:
            """stub
            """
            def __str__(self):
                """stub
                """
                return 'A doctype'
        class Comment:
            """stub
            """
            def __init__(self):
                self.string = 'a comment'

    def mock_getelname(*args):
        """stub
        """
        print('called getelname with args', args)
    def mock_getshortname(*args):
        """stub
        """
        print('called getshortname with args', args)
    def mock_additem(*args):
        """stub
        """
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
    """unittest for Editor.data2soup
    """
    def mock_expandnode(self, *args):
        """stub
        """
        print('called Editor.expandnode with args', args)
    class MockList(list):
        """stub
        """
        def new_tag(self, text):
            """stub
            """
            print(f'called BeautifulSoup.new_tag with arg {text}')
            return text
    class MockBs:
        """stub
        """
        def BeautifulSoup(*args):
            """stub
            """
            print('called bs.BeautifulSoup with args', args)
            return MockList()
        def Doctype(text):
            """stub
            """
            print(f'called bs.Doctype with arg {text}')
            return text
    def mock_element_children(self, node):
        """stub
        """
        return [['dtd'], ['ele'], ['other']]
    def mock_element_text(self, node):
        """stub
        """
        self.textcounter += 1
        data = ['', 'DOCTYPE xxx', f'{testee.ELSTART} element', 'other']
        return data[self.textcounter - 1]
    def mock_element_data(self, node):
        """stub
        """
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
    """unittest for Editor.expandnode
    """
    def mock_newtag(*args):
        """stub
        """
        print('called BeautifulSoup.new_tag with args', args)
        retval = MockBS.Tag('hola')
        retval.append('first body')
        return retval
    class MockBS:
        """stub
        """
        def BeautifulSoup(*args):
            """stub
            """
            print('called BeautifulSoup with args', args)
            return types.SimpleNamespace(new_tag=mock_newtag)
        class Tag:
            """stub
            """
            def __init__(self, name, attrs=None):
                """stub
                """
                self.name = name
                self.attrs = attrs if attrs else {}
                self.contents = []
            def __str__(self):
                """stub
                """
                return f'element {self.name}'
            def append(self, arg):
                """stub
                """
                print('called Tag.append with arg', arg)
                self.contents.append(arg)
        class Doctype:
            """stub
            """
            def __init__(self, arg):
                """stub
                """
                self.string = f'doctype {arg}'
            def __str__(self):
                """stub
                """
                return self.string
        class Comment:
            """stub
            """
            def __init__(self, arg):
                """stub
                """
                self.string = f'commented {arg}'
            def __str__(self):
                """stub
                """
                return self.string
        class NavigableString:
            """stub
            """
            def __init__(self, arg):
                """stub
                """
                self.string = f'plain {arg}'
            def __str__(self):
                """stub
                """
                return self.string
    def mock_get_children(self, arg):
        """stub
        """
        print('called EditorGui.get_element_children with arg', arg)
        self.textcounter += 1
        if self.textcounter == 1:
            return ['element', 'commented element', f'{testee.DTDSTART} dtd', 'other']
        return ['other']
    def mock_get_text(self, arg):
        """stub
        """
        print('called EditorGui.get_element_text with arg', arg)
        if arg == 'element':
            text = f'{testee.ELSTART} this'
        elif arg == 'commented element':
            text = f'{testee.CMELSTART} that'
        elif arg == 'dtd':
            text = '<doctype>'
        else:  # 'other'
            text = arg
        return text
    def mock_get_data(self, arg):
        """stub
        """
        print('called EditorGui.get_element_data with arg', arg)
        if arg in ('element', 'commented element'):
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
    """unittest for Editor.soup2file
    """
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
    """unittest for Editor.get_menulist
    """
    menuitems_per_menu = (7, 6, 16, 9, 13, 1)
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
    """unittest for Editor.mark_dirty
    """
    testobj = setup_editor(monkeypatch, capsys)
    unchanged = f"xxx - {testee.TITEL}"
    changed =  f"xxx* - {testee.TITEL}"
    monkeypatch.setattr(testobj.gui, 'get_screen_title', lambda *x: 'xxx')
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == 'called EditorGui.set_screen_title with arg `xxx`\n'
    testobj.mark_dirty(False)
    assert not testobj.tree_dirty
    assert capsys.readouterr().out == 'called EditorGui.set_screen_title with arg `xxx`\n'
    monkeypatch.setattr(testobj.gui, 'get_screen_title', lambda *x: unchanged)
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == f"called EditorGui.set_screen_title with arg `{changed}`\n"
    testobj.mark_dirty(False)
    assert not testobj.tree_dirty
    assert capsys.readouterr().out == f"called EditorGui.set_screen_title with arg `{unchanged}`\n"
    monkeypatch.setattr(testobj.gui, 'get_screen_title', lambda *x: changed)
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == f"called EditorGui.set_screen_title with arg `{changed}`\n"
    testobj.mark_dirty(False)
    assert not testobj.tree_dirty
    assert capsys.readouterr().out == f"called EditorGui.set_screen_title with arg `{unchanged}`\n"


def test_check_tree_state(monkeypatch, capsys):
    """unittest for Editor.check_tree_state
    """
    def mock_savexml(self):
        """stub
        """
        print('called Editor.savexml')
    counter = 0
    def mock_ask_how(self, *args):
        """stub
        """
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
    """unittest for Editor.is_stylesheet_node
    """
    def mock_get_text(self, node):
        """stub
        """
        print(f'called EditorGui.get_element_text for `{node}`')
        return 'x'
    def mock_get_text_2(self, node):
        """stub
        """
        print(f'called EditorGui.get_element_text for `{node}`')
        return f'{testee.ELSTART} style'
    def mock_get_text_3(self, node):
        """stub
        """
        print(f'called EditorGui.get_element_text for `{node}`')
        return f'{testee.ELSTART} link'
    def mock_get_data(self, node):
        """stub
        """
        print(f'called EditorGui.get_element_data for `{node}`')
        return {'x': 'y'}
    def mock_get_data_2(self, node):
        """stub
        """
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
    """unittest for Editor.in_body
    """
    def mock_get_text(self, node):
        """stub
        """
        print(f'called EditorGui.get_element_text for `{node}`')
        return 'x'
    def mock_get_text_2(self, node):
        """stub
        """
        print(f'called EditorGui.get_element_text for `{node}`')
        return f'{testee.ELSTART} head'
    def mock_get_text_3(self, node):
        """stub
        """
        print(f'called EditorGui.get_element_text for `{node}`')
        return f'{testee.ELSTART} body'
    def mock_get_text_4(self, node):
        """stub
        """
        nonlocal counter
        counter += 1
        print(f'called EditorGui.get_element_text for `{node}`')
        if counter < 3:
            return 'x'
        return f'{testee.ELSTART} head'
    def mock_get_text_5(self, node):
        """stub
        """
        nonlocal counter
        counter += 1
        print(f'called EditorGui.get_element_text for `{node}`')
        if counter < 3:
            return 'x'
        return f'{testee.ELSTART} body'
    def mock_get_parent(self, node):
        """stub
        """
        print(f'called EditorGui.get_element_parent for `{node}`')
    def mock_get_parent_2(self, node):
        """stub
        """
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
    """unittest for Editor.newxml
    """
    def mock_check_state(self):
        """stub
        """
        print('called Editor.check_tree_state')
        return 0
    def mock_file2soup(self, *args, **kwargs):
        """stub
        """
        print('called Editor.file2soup with args', args, kwargs)
    def mock_soup2data(self, *args, **kwargs):
        """stub
        """
        print('called Editor.soup2data with args', args, kwargs)
    def mock_refresh_preview(self):
        """stub
        """
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
    """unittest for Editor.openxml
    """
    def mock_check_state(self):
        """stub
        """
        print('called Editor.check_tree_state')
        return 0
    def mock_ask_filename(self):
        """stub
        """
        print('called EditorGui.ask_for_open_filename')
    def mock_file2soup(self, *args, **kwargs):
        """stub
        """
        print('called Editor.file2soup with args', args, kwargs)
    def mock_soup2data(self, *args, **kwargs):
        """stub
        """
        print('called Editor.soup2data with args', args, kwargs)
    def mock_refresh_preview(self):
        """stub
        """
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
    """unittest for Editor.savexml
    """
    def mock_savexmlas(self):
        """stub
        """
        print('called Editor.savexmlas')
    def mock_data2soup(self, *args, **kwargs):
        """stub
        """
        print('called Editor.data2soup with args', args, kwargs)
    def mock_soup2file(self, *args, **kwargs):
        """stub
        """
        print('called Editor.soup2file with args', args, kwargs)
    def mock_soup2file_2(self, *args, **kwargs):
        """stub
        """
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
    """unittest for Editor.savexmlas
    """
    def mock_data2soup(self, *args, **kwargs):
        """stub
        """
        print('called Editor.data2soup with args', args, kwargs)
    def mock_soup2file(self, *args, **kwargs):
        """stub
        """
        print('called Editor.soup2file with args', args, kwargs)
    def mock_soup2file_2(self, *args, **kwargs):
        """stub
        """
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
    assert capsys.readouterr().out == (
            'called Editor.data2soup with args () {}\n'
            "called Editor.soup2file with args () {'saveas': True}\n"
            'called EditorGui.set_element_text with args `top`, `filename`\n'
            'called EditorGui.show_statusbar_message with arg `saved as filename`\n')
    monkeypatch.setattr(testee.Editor, 'soup2file', mock_soup2file_2)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.savexmlas()
    assert capsys.readouterr().out == ('called Editor.data2soup with args () {}\n'
                                       'called EditorGui.meld with arg `Error`\n')


def test_reopenxml(monkeypatch, capsys):
    """unittest for Editor.reopenxml
    """
    def mock_file2soup(self, *args, **kwargs):
        """stub
        """
        print('called Editor.file2soup with args', args, kwargs)
    def mock_soup2data(self, *args, **kwargs):
        """stub
        """
        print('called Editor.soup2data with args', args, kwargs)
    def mock_refresh_preview(self):
        """stub
        """
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
    """unittest for Editor.close
    """
    def mock_check_state(self):
        """stub
        """
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
    """unittest for Editor.expand
    """
    def mock_expand():
        """stub
        """
        print('called EditorGui.expand')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.expand = mock_expand
    testobj.expand()
    assert capsys.readouterr().out == 'called EditorGui.expand\n'


def test_collapse(monkeypatch, capsys):
    """unittest for Editor.collapse
    """
    def mock_collapse():
        """stub
        """
        print('called EditorGui.collapse')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.collapse = mock_collapse
    testobj.collapse()
    assert capsys.readouterr().out == 'called EditorGui.collapse\n'


def test_advance_selection_onoff(monkeypatch, capsys):
    """unittest for Editor.advance_selection_onoff
    """
    def mock_get_setting():
        """stub
        """
        print('called EditorGui.get_adv_sel_setting')
        return 'sett'
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.get_adv_sel_setting = mock_get_setting
    testobj.advance_selection_onoff()
    assert capsys.readouterr().out == 'called EditorGui.get_adv_sel_setting\n'
    assert testobj.advance_selection_on_add == 'sett'


def test_refresh_preview(monkeypatch, capsys):
    """unittest for Editor.refresh_preview
    """
    def mock_data2soup(self, *args, **kwargs):
        """stub
        """
        print('called Editor.data2soup')
        return 'soup'
    def mock_refresh(arg):
        """stub
        """
        print(f'called EditorGui.refresh_preview with arg `{arg}`')
    monkeypatch.setattr(testee.Editor, 'data2soup', mock_data2soup)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.refresh_preview = mock_refresh
    testobj.refresh_preview()
    assert capsys.readouterr().out == ('called Editor.data2soup\n'
                                       'called EditorGui.refresh_preview with arg `soup`\n')


def test_checkselection(monkeypatch, capsys):
    """unittest for Editor.checkselection
    """
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
    """unittest for Editor.edit
    """
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.edit()
    assert capsys.readouterr().out == 'called EditorHelper.edit\n'
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.edit()
    assert capsys.readouterr().out == ''


def test_comment(monkeypatch, capsys):
    """unittest for Editor.comment
    """
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.comment()
    assert capsys.readouterr().out == 'called EditorHelper.comment\n'
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.comment()
    assert capsys.readouterr().out == ''


def test_cut(monkeypatch, capsys):
    """unittest for Editor.cut
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.cut()
    assert capsys.readouterr().out == "called EditorHelper.copy with args {'cut': True}\n"


def test_delete(monkeypatch, capsys):
    """unittest for Editor.delete
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.delete()
    assert capsys.readouterr().out == ("called EditorHelper.copy with args {'cut': True,"
                                       " 'retain': False}\n")


def test_copy(monkeypatch, capsys):
    """unittest for Editor.copy
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.copy()
    assert capsys.readouterr().out == "called EditorHelper.copy with args {}\n"


def test_paste_after(monkeypatch, capsys):
    """unittest for Editor.paste_after
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.paste_after()
    assert capsys.readouterr().out == "called EditorHelper.paste with args {'before': False}\n"


def test_paste_below(monkeypatch, capsys):
    """unittest for Editor.paste_below
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.paste_below()
    assert capsys.readouterr().out == "called EditorHelper.paste with args {'below': True}\n"


def test_paste(monkeypatch, capsys):
    """unittest for Editor.paste
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.paste()
    assert capsys.readouterr().out == "called EditorHelper.paste with args {}\n"


def test_insert(monkeypatch, capsys):
    """unittest for Editor.insert
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.insert()
    assert capsys.readouterr().out == "called EditorHelper.insert with args {}\n"


def test_insert_after(monkeypatch, capsys):
    """unittest for Editor.insert_after
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.insert_after()
    assert capsys.readouterr().out == "called EditorHelper.insert with args {'before': False}\n"


def test_insert_child(monkeypatch, capsys):
    """unittest for Editor.insert_child
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.insert_child()
    assert capsys.readouterr().out == "called EditorHelper.insert with args {'below': True}\n"


def test_add_text(monkeypatch, capsys):
    """unittest for Editor.add_text
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.add_text()
    assert capsys.readouterr().out == "called EditorHelper.add_text with args {}\n"


def test_add_text_after(monkeypatch, capsys):
    """unittest for Editor.add_text_after
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.add_text_after()
    assert capsys.readouterr().out == "called EditorHelper.add_text with args {'before': False}\n"


def test_add_textchild(monkeypatch, capsys):
    """unittest for Editor.add_textchild
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.add_textchild()
    assert capsys.readouterr().out == "called EditorHelper.add_text with args {'below': True}\n"


def test_build_search_spec(monkeypatch, capsys):
    """unittest for Editor.build_search_spec
    """
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
    """unittest for Editor.search
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.search()
    assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.search_from with args () {'item': None}\n")


def test_search_last(monkeypatch, capsys):
    """unittest for Editor.search_last
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.search_last()
    assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.search_from with args () {'reverse': True, 'item': None}\n")


def test_search_next(monkeypatch, capsys):
    """unittest for Editor.search_next
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.search_next()
    assert capsys.readouterr().out == "called SearchHelper.search_next with args {}\n"


def test_search_prev(monkeypatch, capsys):
    """unittest for Editor.search_prev
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.search_prev()
    assert capsys.readouterr().out == "called SearchHelper.search_next with args {'reverse': True}\n"


def test_replace(monkeypatch, capsys):
    """unittest for Editor.replace
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.replace()
    assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.replace_from with args () {'item': None}\n")


def test_replace_last(monkeypatch, capsys):
    """unittest for Editor.replace_last
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.replace_last()
    assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.replace_from with args () {'reverse': True, 'item': None}\n")


def test_replace_and_next(monkeypatch, capsys):
    """unittest for Editor.replace_and_next
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.replace_and_next()
    assert capsys.readouterr().out == "called SearchHelper.replace_next with args {}\n"


def test_replace_and_prev(monkeypatch, capsys):
    """unittest for Editor.replace_and_prev
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.replace_and_prev()
    assert capsys.readouterr().out == "called SearchHelper.replace_next with args {'reverse': True}\n"


def test_add_dtd(monkeypatch, capsys):
    """unittest for Editor.add_dtd
    """
    def mock_get_children(arg):
        """stub
        """
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        return ['first child']
    def mock_get_dtd():
        """stub
        """
        print('called EditorGui.get_dtd')
        return True, 'A doctype'
    def mock_get_dtd_no():
        """stub
        """
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
    """unittest for Editor.add_css
    """
    def mock_get_css_no():
        """stub
        """
        print('called EditorGui.get_css_data')
        return False, ''
    def mock_get_css_external():
        """stub
        """
        print('called EditorGui.get_css_data')
        return True, {'href': 'some_stylesheet'}
    def mock_get_css_internal():
        """stub
        """
        print('called EditorGui.get_css_data')
        return True, {'other': 'xxx', 'cssdata': 'yyy'}
    def mock_get_children_nohtml(arg):
        """stub
        """
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        return ['x']
    counter = 0
    def mock_get_children_nohead(arg):
        """stub
        """
        nonlocal counter
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        counter += 1
        if counter == 1:
            return [f'{testee.ELSTART} html']
        return ['first child']
    def mock_get_children(arg):
        """stub
        """
        nonlocal counter
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        counter += 1
        if counter == 1:
            return [f'{testee.ELSTART} html']
        if counter == 2:
            return [f'{testee.ELSTART} head']
        return ['first child']
    def mock_get_text(arg):
        """stub
        """
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
    assert capsys.readouterr().out == (
            "called EditorGui.get_css_data\n"
            "called EditorGui.get_element_children with arg `gui.top`\n"
            f"called EditorGui.get_element_text with arg `{testee.ELSTART} html`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} html`\n"
            "called EditorGui.get_element_text with arg `first child`\n"
            "called EditorGui.meld with arg"
            " `Error: no <html> and/or no <head> element`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    counter = 0
    testobj.add_css()
    assert capsys.readouterr().out == (
            "called EditorGui.get_css_data\n"
            "called EditorGui.get_element_children with arg `gui.top`\n"
            f"called EditorGui.get_element_text with arg `{testee.ELSTART} html`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} html`\n"
            f"called EditorGui.get_element_text with arg `{testee.ELSTART} head`\n"
            f"called EditorGui.addtreeitem with args ('{testee.ELSTART} head',"
            f" '{testee.ELSTART} link', {{'href': 'some_stylesheet'}}, -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    monkeypatch.setattr(testobj.gui, 'get_css_data', mock_get_css_internal)
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    counter = 0
    testobj.add_css()
    assert capsys.readouterr().out == (
            "called EditorGui.get_css_data\n"
            "called EditorGui.get_element_children with arg `gui.top`\n"
            f"called EditorGui.get_element_text with arg `{testee.ELSTART} html`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} html`\n"
            f"called EditorGui.get_element_text with arg `{testee.ELSTART} head`\n"
            f"called EditorGui.addtreeitem with args ('{testee.ELSTART} head',"
            f" '{testee.ELSTART} style', {{'other': 'xxx'}}, -1)\n"
            "called EditorGui.addtreeitem with args ('node', 'yyy', 'yyy', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")


def test_check_if_adding_ok(monkeypatch, capsys):
    """unittest for Editor.check_if_adding_ok
    """
    monkeypatch.setattr(MockEditorGui, 'get_element_text', lambda *x: 'text')
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
    testobj = setup_editor(monkeypatch, capsys)
    assert not testobj.check_if_adding_ok()
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.item = 'x'
    assert not testobj.check_if_adding_ok()
    monkeypatch.setattr(MockEditorGui, 'get_element_text', lambda *x: f'{testee.ELSTART} text')
    testobj.item = 'x'
    assert testobj.check_if_adding_ok()


def test_convert_link(monkeypatch, capsys, tmp_path):
    """unittest for Editor.convert_link
    """
    # orig_abspath = testee.os.path.abspath
    # def mock_abspath(arg):
    #     print(f'called os.path.abspath with arg `{arg}`')
    #     orig_abspath(arg)
    # def mock_getcwd():
    #     print('called os.getcwd')
    #     return os.path.dirname(__path__)
    def mock_relpath(*args):
        """stub
        """
        print('called os.path.relpath with args', args)
        raise ValueError('os.path.relpath failed')
    def mock_relpath_2(*args):
        """stub
        """
        print('called os.path.relpath with args', args)
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
    """unittest for Editor.add_link
    """
    def mock_get_link_data():
        """stub
        """
        print('called EditorGui.get_link_data')
        return True, ('txt', 'data')
    def mock_get_link_data_2():
        """stub
        """
        print('called EditorGui.get_link_data')
        return False, ('', '')
    def mock_getelname(*args):
        """stub
        """
        print('called getelname with args', args)
    def mock_getshortname(*args):
        """stub
        """
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
    """unittest for Editor.add_image
    """
    def mock_get_image_data():
        """stub
        """
        print('called EditorGui.get_image_data')
        return True, ('txt', 'data')
    def mock_get_image_data_2():
        """stub
        """
        print('called EditorGui.get_image_data')
        return False, ('', '')
    def mock_getelname(*args):
        """stub
        """
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
    """unittest for Editor.add_audio
    """
    def mock_get_audio_data():
        """stub
        """
        print('called EditorGui.get_audio_data')
        return True, ({'x': 'y'})
    def mock_get_audio_data_2():
        """stub
        """
        print('called EditorGui.get_audio_data')
        return False, ('', '')
    def mock_getelname(*args):
        """stub
        """
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
    """unittest for Editor.add_video
    """
    def mock_get_video_data():
        """stub
        """
        print('called EditorGui.get_video_data')
        return True, ({'src': 'y.mp4'})
    def mock_get_video_data_2():
        """stub
        """
        print('called EditorGui.get_video_data')
        return False, ('', '')
    def mock_getelname(*args):
        """stub
        """
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
    """unittest for Editor.add_list
    """
    def mock_getelname(*args):
        """stub
        """
        print('called getelname with args', args)
        return args[0] or 'elname'
    def mock_getshortname(*args):
        """stub
        """
        print('called getshortname with args', args)
        return args[0] or 'shortname'
    def mock_get_no_list_data():
        """stub
        """
        print('called EditorGui.get_list_data')
        return False, ('', '')
    def mock_get_list_data():
        """stub
        """
        print('called EditorGui.get_list_data')
        return True, ('', '')
    def mock_get_list_data_dl():
        """stub
        """
        print('called EditorGui.get_list_data')
        return True, ('dl', [('name', 'text')])
    def mock_get_list_data_other():
        """stub
        """
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
    """unittest for Editor.add_table
    """
    def mock_getelname(*args):
        """stub
        """
        print('called getelname with args', args)
        return args[0] or 'elname'
    def mock_getshortname(*args):
        """stub
        """
        print('called getshortname with args', args)
        return args[0] or 'shortname'
    def mock_get_no_table_data():
        """stub
        """
        print('called EditorGui.get_table_data')
        return False, ('', '')
    def mock_get_table_data():
        """stub
        """
        print('called EditorGui.get_table_data')
        return True, ('empty table', False, '', [])
    def mock_get_table_data_headers():
        """stub
        """
        print('called EditorGui.get_table_data')
        return True, ('table with headers but no items', True, ['x', 'y'], [])
    def mock_get_table_data_items():
        """stub
        """
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
            " ('testobjitem', 'table', {'summary': 'empty table'}, -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.gui.get_table_data = mock_get_table_data_headers
    testobj.item = 'testobjitem'
    testobj.add_table()
    assert capsys.readouterr().out == (
            'called EditorGui.get_table_data\n'
            "called getelname with args ('table', {'summary': 'table with headers but no items'})\n"
            "called EditorGui.addtreeitem with args"
            " ('testobjitem', 'table', {'summary': 'table with headers but no items'}, -1)\n"
            "called getelname with args ('tr',)\n"
            "called EditorGui.addtreeitem with args ('node', 'tr', None, -1)\n"
            "called getelname with args ('th',)\n"
            "called EditorGui.addtreeitem with args ('node', 'th', None, -1)\n"
            "called getshortname with args ('x',)\n"
            "called EditorGui.addtreeitem with args ('node', 'x', 'x', -1)\n"
            "called getelname with args ('th',)\n"
            "called EditorGui.addtreeitem with args ('node', 'th', None, -1)\n"
            "called getshortname with args ('y',)\n"
            "called EditorGui.addtreeitem with args ('node', 'y', 'y', -1)\n"
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
            " ('testobjitem', 'table', {'summary': 'table with items and empty headers'}, -1)\n"
            "called getelname with args ('tr',)\n"
            "called EditorGui.addtreeitem with args ('node', 'tr', None, -1)\n"
            "called getelname with args ('th',)\n"
            "called EditorGui.addtreeitem with args ('node', 'th', None, -1)\n"
            "called getshortname with args ('&nbsp;',)\n"
            "called EditorGui.addtreeitem with args ('node', '&nbsp;', '&nbsp;', -1)\n"
            "called getelname with args ('th',)\n"
            "called EditorGui.addtreeitem with args ('node', 'th', None, -1)\n"
            "called getshortname with args ('&nbsp;',)\n"
            "called EditorGui.addtreeitem with args ('node', '&nbsp;', '&nbsp;', -1)\n"
            "called getelname with args ('tr',)\n"
            "called EditorGui.addtreeitem with args ('node', 'tr', None, -1)\n"
            "called getelname with args ('td',)\n"
            "called EditorGui.addtreeitem with args ('node', 'td', None, -1)\n"
            "called getshortname with args ('x',)\n"
            "called EditorGui.addtreeitem with args ('node', 'x', 'x', -1)\n"
            "called getelname with args ('td',)\n"
            "called EditorGui.addtreeitem with args ('node', 'td', None, -1)\n"
            "called getshortname with args ('y',)\n"
            "called EditorGui.addtreeitem with args ('node', 'y', 'y', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")


def test_validate(monkeypatch, capsys):
    """unittest for Editor.validate
    """
    def mock_mkdtemp():
        """stub
        """
        print('called tempfile.mkdtemp')
        return 'tempdir'
    def mock_prettify():
        """stub
        """
        print('called Editor.soup.prettify')
        return 'prettified soup'
    def mock_data2soup(self):
        """stub
        """
        print('called Editor.data2soup')
        self.soup = types.SimpleNamespace(prettify=mock_prettify)
    def mock_write(*args):
        """stub
        """
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
    """unittest for Editor.do_validate
    """
    def mock_run(*args, **kwargs):
        """stub
        """
        print("call subprocess.run with args", args, kwargs)
        pathlib.Path('/tmp/ashe_check').write_text('ashe_check')
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    testobj = setup_editor(monkeypatch, capsys)
    assert testobj.do_validate('test.html') == 'ashe_check'
    assert capsys.readouterr().out == ("call subprocess.run with args"
                                       " (['tidy', '-e', '-f', '/tmp/ashe_check', 'test.html'],)"
                                       " {'check': False}\n")


def test_view_code(monkeypatch, capsys):
    """unittest for Editor.view_code
    """
    def mock_data2soup(self, *args, **kwargs):
        """stub
        """
        print('called Editor.data2soup with args', args, kwargs)
    def mock_prettify(*args):
        """stub
        """
        print('called BeautifulSoup.prettify')
    def mock_show_code(*args):
        """stub
        """
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
    """unittest for Editor.about
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.about()
    assert capsys.readouterr().out == f'called EditorGui.meld with arg `{testee.ABOUT}`\n'


# -- EditorHelper ---------------------
def test_editorhelper_init():
    """unittest for EditorHelper.init
    """
    testobj = testee.EditorHelper(MockEditor())
    assert hasattr(testobj, 'editor')
    assert hasattr(testobj, 'gui')


def test_editorhelper_edit(monkeypatch, capsys):
    """unittest for EditorHelper.edit
    """
    def mock_get_text(self, arg):
        """stub
        """
        print('called EditorGui.get_element_text with arg', arg)
        if arg == 'element':
            text = f'{testee.ELSTART} this'
        elif arg == 'commented element':
            text = f'{testee.CMELSTART} that'
        elif arg == 'dtd':
            text = f'{testee.DTDSTART} xx'
        else:  # 'other'
            text = arg
        return text
    def mock_show_dtd():
        """stub
        """
        print('called EditorHelper.show_dtd_info')
    def mock_element_dialog(arg):
        """stub
        """
        print(f'called EditorHelper.process_element_dialog with arg `{arg}`')
        return True
    def mock_text_dialog(arg):
        """stub
        """
        print(f'called EditorHelper.process_text_dialog with arg `{arg}`')
        return False
    def mock_refresh():
        """stub
        """
        print('called Editor.refresh_preview')
    def mock_mark_dirty(value):
        """stub
        """
        print(f'called.Editor.mark_dirty with value `{value}`')
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text)
    # monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
    # monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    testobj.editor.refresh_preview = mock_refresh
    testobj.editor.mark_dirty = mock_mark_dirty
    testobj.show_dtd_info = mock_show_dtd
    testobj.process_element_dialog = mock_element_dialog
    testobj.process_text_dialog = mock_text_dialog
    testobj.editor.item = 'element'
    testobj.edit()
    assert capsys.readouterr().out == (
            'called EditorGui.get_element_text with arg element\n'
            f'called EditorHelper.process_element_dialog with arg `{testee.ELSTART} this`\n'
            'called.Editor.mark_dirty with value `True`\n'
            'called Editor.refresh_preview\n')
    testobj.editor.item = 'commented element'
    testobj.edit()
    assert capsys.readouterr().out == (
            'called EditorGui.get_element_text with arg commented element\n'
            f'called EditorHelper.process_element_dialog with arg `{testee.CMELSTART} that`\n'
            'called.Editor.mark_dirty with value `True`\n'
            'called Editor.refresh_preview\n')
    testobj.editor.item = 'dtd'
    testobj.edit()
    assert capsys.readouterr().out == (
            'called EditorGui.get_element_text with arg dtd\n'
            'called EditorHelper.show_dtd_info\n')
    testobj.editor.item = 'other'
    testobj.edit()
    assert capsys.readouterr().out == (
            'called EditorGui.get_element_text with arg other\n'
            'called EditorHelper.process_text_dialog with arg `other`\n')


def test_editorhelper_show_dtd(monkeypatch, capsys):
    """unittest for EditorHelper.show_dtd
    """
    def mock_get(self, item):
        """stub
        """
        print(f'called EditorGui.get_element_text with arg `{item}`')
        return item
    def mock_meld(self, text):
        """stub
        """
        print(f'called EditorGui.meld with arg `{text}`')
    monkeypatch.setattr(MockEditorGui, 'meld', mock_meld)
    monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_get)
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    testobj.item = 'testitem'
    testobj.show_dtd_info()
    assert capsys.readouterr().out == (
            'called EditorGui.get_element_text with arg `testitem`\n'
            'called EditorGui.meld with arg `doctype cannot be determined`\n')
    testobj.item = 'html'
    testobj.show_dtd_info()
    assert capsys.readouterr().out == (
            'called EditorGui.get_element_text with arg `html`\n'
            'called EditorGui.meld with arg `doctype is HTML 5`\n')
    testobj.item = 'HTML PUBLIC "-//W3C//DTD xx//ENyy'
    testobj.show_dtd_info()
    assert capsys.readouterr().out == (
            'called EditorGui.get_element_text with arg `HTML PUBLIC "-//W3C//DTD xx//ENyy`\n'
            'called EditorGui.meld with arg `doctype is XX`\n')


def test_editorhelper_process_element(monkeypatch, capsys):
    """unittest for EditorHelper.process_element
    """
    orig_get_tag = testee.get_tag_from_elname
    def mock_get_tag(text):
        """stub
        """
        print(f'called get_tag_from_elname with arg `{text}`')
        return orig_get_tag(text)
    def mock_get_data(item):
        """stub
        """
        print(f'called EditorGui.get_element_data with arg `{item}`')
        if item.endswith('p'):
            return {'x': 'y'}
        if item.endswith('p2'):
            return {'x': 'y', 'style': 'xxx'}
        return 'styletext'
    def mock_get_text(item):
        """stub
        """
        print(f'called EditorGui.get_element_text with arg `{item}`')
        if item == 'item parent 2':
            return f'{testee.CMELSTART} parent'
        return 'parent text'
    def mock_get_parent(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'item parent'
    def mock_get_parent_2(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'item parent 2'
    def mock_get_children(arg):
        """stub
        """
        print(f'called EditorGui.get_element_children with arg `{arg}`')
        return ['text']
    def mock_get_no_children(arg):
        """stub
        """
        print('called EditorGui.get_element_children with arg `{arg}`')
        return []
    def mock_comment(*args):
        """stub
        """
        print('called EditorHelper.comment_out with args', args)
    def mock_do_not_edit(item, attrdict):
        """stub
        """
        print(f'called EditorGui.do_edit_element with arg `{item}`')
        return False, ()
    def mock_do_edit_commented(item, attrdict):
        """stub
        """
        print(f'called EditorGui.do_edit_element with arg `{item}`')
        return True, ('p', {'x': 'z'}, True)
    def mock_do_edit_attrs(item, attrdict):
        """stub
        """
        print(f'called EditorGui.do_edit_element with arg `{item}`')
        return True, ('p', {'x': 'z', 'style': ''}, False)
    def mock_do_edit_style_attr(item, attrdict):
        """stub
        """
        print(f'called EditorGui.do_edit_element with arg `{item}`')
        return True, ('p', {'style': 'aaaa'}, False)
    def mock_do_edit_style_ele(item, attrdict):
        """stub
        """
        print(f'called EditorGui.do_edit_element with arg `{item}`')
        return True, ('style', {'x': 'z', 'styledata': 'yyy'}, False)
    def mock_do_edit_b_not_p(item, attrdict):
        """stub
        """
        print(f'called EditorGui.do_edit_element with arg `{item}`')
        return True, ('b', {'x': 'z'}, False)
    monkeypatch.setattr(MockEditorGui, 'get_element_children', mock_get_children)
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == "called EditorGui.__init__\ncalled Editor.__init__()\n"
    monkeypatch.setattr(testee, 'get_tag_from_elname', mock_get_tag)
    monkeypatch.setattr(testobj, 'comment_out', mock_comment)
    monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
    monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    testobj.gui.do_edit_element = mock_do_not_edit
    testobj.item = f'{testee.ELSTART} p'
    # canceling the edit dialog
    assert not testobj.process_element_dialog(f'{testee.ELSTART} p')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.ELSTART} p`\n")
    # scenario's:
    # wijzig attributen van een element
    testobj.gui.do_edit_element = mock_do_edit_commented
    assert testobj.process_element_dialog(f'{testee.ELSTART} p')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`, `{testee.CMELSTART} p`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n"
        f"called EditorHelper.comment_out with args ('{testee.ELSTART} p', True)\n")
    # voeg inline style toe aan een element
    testobj.gui.do_edit_element = mock_do_edit_attrs
    assert testobj.process_element_dialog(f'{testee.ELSTART} p2')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.ELSTART} p2`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.ELSTART} p2`\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`, `{testee.ELSTART} p`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
    # wjzig inline style van een element (in dit geval: leegmaken)
    testobj.gui.do_edit_element = mock_do_edit_style_attr
    assert testobj.process_element_dialog(f'{testee.ELSTART} p2')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.ELSTART} p2`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.ELSTART} p2`\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`, `{testee.ELSTART} p`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'style': 'aaaa'}}`\n")
    # wijzig naam van een element
    testobj.gui.do_edit_element = mock_do_edit_b_not_p
    assert testobj.process_element_dialog(f'{testee.ELSTART} p')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`, `{testee.ELSTART} b`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
    # wijzig element x in style element (en voeg style text toe)
    testobj.gui.do_edit_element = mock_do_edit_style_ele
    assert testobj.process_element_dialog(f'{testee.ELSTART} p')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.addtreeitem with args ('{testee.ELSTART} p', 'yyy', {{}}, -1)\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
        f" `{testee.ELSTART} style`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
    # wijzig style element in element x
    testobj.gui.do_edit_element = mock_do_edit_attrs
    assert testobj.process_element_dialog(f'{testee.ELSTART} style')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.ELSTART} style`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_data with arg `text`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.ELSTART} style`\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`, `{testee.ELSTART} p`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
    # wijzig style text van een style element
    testobj.gui.do_edit_element = mock_do_edit_style_ele
    assert testobj.process_element_dialog(f'{testee.ELSTART} style')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.ELSTART} style`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_data with arg `text`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.ELSTART} style`\n"
        "called EditorGui.set_element_text with args `yyy`, `yyy`\n"
        "called EditorGui.set_element_data with args `yyy`, `yyy`\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
        f" `{testee.ELSTART} style`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
    # -- uitgecommentaard element
    testobj.gui.do_edit_element = mock_do_edit_attrs
    assert testobj.process_element_dialog(f'{testee.CMELSTART} p')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.CMELSTART} p`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_element with arg `{testee.CMELSTART} p`\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`, `{testee.ELSTART} p`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n"
        f"called EditorHelper.comment_out with args ('{testee.ELSTART} p', False)\n")
    # -- element onder een uitgecommentaard element - blijft uitgecommentaard
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_2)
    testobj.gui.do_edit_element = mock_do_edit_commented
    assert testobj.process_element_dialog(f'{testee.CMELSTART} style')
    assert capsys.readouterr().out == (
        f"called get_tag_from_elname with arg `{testee.CMELSTART} style`\n"
        f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
        f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_data with arg `text`\n"
        f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
        "called EditorGui.get_element_text with arg `item parent 2`\n"
        f"called EditorGui.do_edit_element with arg `{testee.CMELSTART} style`\n"
        f"called EditorGui.set_element_text with args `{testee.ELSTART} p`, `{testee.CMELSTART} p`\n"
        f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")


def test_editorhelper_process_text(monkeypatch, capsys):
    """unittest for EditorHelper.process_text
    """
    def mock_get_data(item):
        """stub
        """
        print(f'called EditorGui.get_element_data with arg `{item}`')
        return 'itemtext'
    def mock_get_text(item):
        """stub
        """
        print(f'called EditorGui.get_element_text with arg `{item}`')
        try:
            return {'item parent 2': f'{testee.ELSTART} style',
                    'item parent 3': f'{testee.CMELSTART} style',
                    'item parent 4': f'{testee.CMELSTART} parent'}[item]
        except KeyError:
            return 'parent text'
    def mock_get_parent(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'item parent'
    def mock_get_parent_2(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'item parent 2'
    def mock_get_parent_3(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'item parent 3'
    def mock_get_parent_4(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'item parent 4'
    def mock_meld(text):
        """stub
        """
        print(f'called EditorGui.meld with arg `{text}`')
    def mock_do_edit(item):
        """stub
        """
        print(f'called EditorGui.do_edit_textvalue with arg `{item}`')
        return True, ('edited text', False)
    def mock_do_edit_2(item):
        """stub
        """
        print(f'called EditorGui.do_edit_textvalue with arg `{item}`')
        return True, ('edited text', True)
    def mock_do_edit_3(item):
        """stub
        """
        print(f'called EditorGui.do_edit_textvalue with arg `{item}`')
        return False, ()
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == "called EditorGui.__init__\ncalled Editor.__init__()\n"
    monkeypatch.setattr(testobj.gui, 'meld', mock_meld)
    monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
    monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
    # monkeypatch.setattr(testobj.gui, 'do_edit_textvalue', mock_do_edit)
    testobj.gui.do_edit_textvalue = mock_do_edit
    testobj.item = 'testitem'
    assert testobj.process_text_dialog('xx')
    assert capsys.readouterr().out == (
        "called EditorGui.get_element_data with arg `testitem`\n"
        "called EditorGui.get_element_parent with arg `testitem`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        "called EditorGui.do_edit_textvalue with arg `itemtext`\n"
        "called EditorGui.set_element_text with args `testitem`, `edited text`\n"
        "called EditorGui.set_element_data with args `testitem`, `edited text`\n")
    assert testobj.process_text_dialog(f"{testee.CMSTART} xx")
    assert capsys.readouterr().out == (
        "called EditorGui.get_element_data with arg `testitem`\n"
        "called EditorGui.get_element_parent with arg `testitem`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        f"called EditorGui.do_edit_textvalue with arg `{testee.CMSTART} itemtext`\n"
        "called EditorGui.set_element_text with args `testitem`, `edited text`\n"
        "called EditorGui.set_element_data with args `testitem`, `edited text`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_2)
    assert not testobj.process_text_dialog('xx')
    assert capsys.readouterr().out == (
        "called EditorGui.get_element_data with arg `testitem`\n"
        "called EditorGui.get_element_parent with arg `testitem`\n"
        "called EditorGui.get_element_text with arg `item parent 2`\n"
        "called EditorGui.meld with arg `Please edit style through parent tag`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_3)
    assert not testobj.process_text_dialog('xx')
    assert capsys.readouterr().out == (
        "called EditorGui.get_element_data with arg `testitem`\n"
        "called EditorGui.get_element_parent with arg `testitem`\n"
        "called EditorGui.get_element_text with arg `item parent 3`\n"
        "called EditorGui.meld with arg `Please edit style through parent tag`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_4)
    assert testobj.process_text_dialog('xx')
    assert capsys.readouterr().out == (
        "called EditorGui.get_element_data with arg `testitem`\n"
        "called EditorGui.get_element_parent with arg `testitem`\n"
        "called EditorGui.get_element_text with arg `item parent 4`\n"
        "called EditorGui.do_edit_textvalue with arg `itemtext`\n"
        f"called EditorGui.set_element_text with args `testitem`, `{testee.CMSTART} edited text`\n"
        "called EditorGui.set_element_data with args `testitem`, `edited text`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
    testobj.gui.do_edit_textvalue = mock_do_edit_2
    assert testobj.process_text_dialog('xx')
    assert capsys.readouterr().out == (
        "called EditorGui.get_element_data with arg `testitem`\n"
        "called EditorGui.get_element_parent with arg `testitem`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        "called EditorGui.do_edit_textvalue with arg `itemtext`\n"
        f"called EditorGui.set_element_text with args `testitem`, `{testee.CMSTART} edited text`\n"
        "called EditorGui.set_element_data with args `testitem`, `edited text`\n")
    testobj.gui.do_edit_textvalue = mock_do_edit_3
    assert not testobj.process_text_dialog('xx')
    assert capsys.readouterr().out == (
        "called EditorGui.get_element_data with arg `testitem`\n"
        "called EditorGui.get_element_parent with arg `testitem`\n"
        "called EditorGui.get_element_text with arg `item parent`\n"
        "called EditorGui.do_edit_textvalue with arg `itemtext`\n")


def test_editorhelper_comment(monkeypatch, capsys):
    """unittest for EditorHelper.comment
    """
    def mock_get_parent(self, node):
        """stub
        """
        if node == 'commented':
            return 'above commented'
        return 'element_above'
    def mock_get_text(self, node):
        """stub
        """
        try:
            return {'element': f'{testee.ELSTART} itemtext',
                    'commented': f'{testee.CMELSTART} itemtext',
                    'other': 'plaintext',
                    'above commented': f'{testee.CMELSTART} abovetext'}[node]
        except KeyError:
            return f'{testee.ELSTART} abovetext'
    def mock_get_data(self, node):
        """stub
        """
        return {'x': 'y'}
    def mock_refresh():
        """stub
        """
        print('called Editor.refresh_preview')
    monkeypatch.setattr(MockEditorGui, 'get_element_parent', mock_get_parent)
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_get_data)
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == "called EditorGui.__init__\ncalled Editor.__init__()\n"
    testobj.editor.refresh_preview = mock_refresh
    testobj.editor.item = 'element'
    testobj.comment()
    assert testobj.item == testobj.editor.item
    assert capsys.readouterr().out == (
            f"called EditorGui.set_element_text with args `element`, `{testee.CMELSTART}"
            " itemtext`\n"
            "called EditorGui.set_element_data with args `element`, `{'x': 'y'}`\n"
            "called Editor.refresh_preview\n")
    testobj.editor.item = 'commented'
    testobj.comment()
    assert testobj.item == testobj.editor.item
    assert capsys.readouterr().out == (
            f"called EditorGui.set_element_text with args `commented`, `{testee.CMELSTART}"
            " itemtext`\n"
            "called EditorGui.set_element_data with args `commented`, `{'x': 'y'}`\n"
            "called Editor.refresh_preview\n")
    testobj.editor.item = 'other'
    testobj.comment()
    assert testobj.item == testobj.editor.item
    assert capsys.readouterr().out == (
            f"called EditorGui.set_element_text with args `other`, `{testee.CMSTART} plaintext`\n"
            "called EditorGui.set_element_data with args `other`, `plaintext`\n"
            "called Editor.refresh_preview\n")


def test_editorhelper_comment_out(monkeypatch, capsys):
    """unittest for EditorHelper.comment_out
    """
    def mock_get_children(self, node):
        """stub
        """
        if node == 'root':
            return ['element', 'commented', 'other']
        return []
    def mock_get_text(self, node):
        """stub
        """
        if node == 'element':
            return f'{testee.ELSTART} itemtext'
        if node == 'commented':
            return f'{testee.CMELSTART} itemtext'
        # elif node == 'other':
        return 'plaintext'
    monkeypatch.setattr(MockEditorGui, 'get_element_children', mock_get_children)
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text)
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == "called EditorGui.__init__\ncalled Editor.__init__()\n"
    testobj.comment_out('root', False)
    assert capsys.readouterr().out == (
            f"called EditorGui.set_element_text with args `element`, `{testee.ELSTART} itemtext`\n"
            f"called EditorGui.set_element_text with args `commented`, `{testee.ELSTART} itemtext`\n"
            "called EditorGui.set_element_text with args `other`, `plaintext`\n")
    testobj.comment_out('root', True)
    assert capsys.readouterr().out == (
            f"called EditorGui.set_element_text with args `element`, `{testee.CMELSTART} itemtext`\n"
            "called EditorGui.set_element_text with args `commented`,"
            f" `{testee.CMELSTART} itemtext`\n"
            f"called EditorGui.set_element_text with args `other`, `{testee.CMSTART} plaintext`\n")


def test_editorhelper_copy(monkeypatch, capsys):
    """unittest for EditorHelper.copy
    """
    def mock_get_data(item):
        """stub
        """
        print(f'called EditorGui.get_element_data with arg `{item}`')
        if item == 'item':
            return {'x': 'y'}
        return 'textdata'
    def mock_get_text(item):
        """stub
        """
        print(f'called EditorGui.get_element_text with arg `{item}`')
        if item == 'dtd':
            return f'{testee.DTDSTART} item'
        if item == 'item':
            return f'{testee.ELSTART} item'
        return 'text'
    def mock_push_el(*args):
        """stub
        """
        print('called EditorHelper.push_el with args', args)
        return ['pushed element', 'subelement']
    def mock_refresh():
        """stub
        """
        print('called Editor.refresh_preview')
    def mock_mark_dirty(value):
        """stub
        """
        print(f'called.Editor.mark_dirty with value `{value}`')
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
    testobj.editor.refresh_preview = mock_refresh
    testobj.editor.mark_dirty = mock_mark_dirty
    monkeypatch.setattr(testobj, 'push_el', mock_push_el)
    testobj.editor.checkselection = lambda *x: False
    testobj.copy()
    assert capsys.readouterr().out == ''
    testobj.editor.checkselection = lambda *x: True
    testobj.editor.root = 'root'
    testobj.editor.item = testobj.editor.root
    testobj.copy()
    assert capsys.readouterr().out == "called EditorGui.meld with arg `Can't copy the root`\n"
    testobj.copy(cut=True)
    assert capsys.readouterr().out == "called EditorGui.meld with arg `Can't cut the root`\n"
    testobj.copy(retain=False)
    assert capsys.readouterr().out == "called EditorGui.meld with arg `Can't delete the root`\n"
    testobj.editor.item = 'dtd'
    testobj.copy()
    assert capsys.readouterr().out == ("called EditorGui.get_element_text with arg `dtd`\n"
                                       "called EditorGui.get_element_data with arg `dtd`\n"
                                       "called EditorGui.meld with arg"
                                       " `Please use the HTML menu's DTD option to remove the DTD`\n")
    testobj.editor.item = 'textitem'
    testobj.copy()
    assert testobj.editor.cut_el is None
    assert testobj.editor.cut_txt == 'textdata'
    assert capsys.readouterr().out == ("called EditorGui.get_element_text with arg `textitem`\n"
                                       "called EditorGui.get_element_data with arg `textitem`\n")
    testobj.editor.item = 'item'
    testobj.copy()
    assert testobj.editor.cut_el == ['pushed element', 'subelement']
    assert testobj.editor.cut_txt is None
    assert capsys.readouterr().out == ("called EditorGui.get_element_text with arg `item`\n"
                                       "called EditorGui.get_element_data with arg `item`\n"
                                       "called EditorHelper.push_el with args ('item', [])\n")
    testobj.editor.item = 'item'
    testobj.copy(retain=False)
    assert testobj.editor.cut_el == ['pushed element', 'subelement']
    assert testobj.editor.cut_txt is None
    assert capsys.readouterr().out == ("called EditorGui.get_element_text with arg `item`\n"
                                       "called EditorGui.get_element_data with arg `item`\n")
    testobj.editor.item = 'item'
    testobj.copy(cut=True)
    assert testobj.editor.cut_el == ['pushed element', 'subelement']
    assert testobj.editor.cut_txt is None
    assert capsys.readouterr().out == ("called EditorGui.get_element_text with arg `item`\n"
                                       "called EditorGui.get_element_data with arg `item`\n"
                                       "called EditorHelper.push_el with args ('item', [])\n"
                                       "called EditorGui.do_delete_item with arg `item`\n"
                                       "called.Editor.mark_dirty with value `True`\n"
                                       "called EditorGui.set_selected_item(`preceding item`)\n"
                                       "called Editor.refresh_preview\n")
    # testobj.editor.item = 'item'
    # testobj.copy(cut=True, retain=False)
    # assert testobj.editor.cut_el == ['pushed element', 'subelement']
    # assert testobj.editor.cut_txt == None
    # assert capsys.readouterr().out == ("called EditorGui.get_element_text with arg `item`\n"
    #                                    "called EditorGui.get_element_data with arg `item`\n"
    #                                    "called EditorHelper.push_el with args ('item', [])\n")


def test_editorhelper_push_el(monkeypatch, capsys):
    """unittest for EditorHelper.push_el
    """
    def mock_get_data(item):
        """stub
        """
        print(f'called EditorGui.get_element_data with arg `{item}`')
        if item == 'node':
            return {}
        if item == 'item':
            return {'x': 'y'}
        return 'textdata'
    def mock_get_text(item):
        """stub
        """
        print(f'called EditorGui.get_element_text with arg `{item}`')
        if item == 'text':
            return 'text'
        return f'{testee.ELSTART} {item}'
    counter = 0
    def mock_get_children(item):
        """stub
        """
        nonlocal counter
        print(f'called EditorGui.get_element_children with arg `{item}`')
        counter += 1
        if counter == 1:
            return ['item', 'text']
        return []
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    assert testobj.push_el('node', []) == [('<> node', {},
                                            [('<> item', {'x': 'y'}, []),
                                             ('text', 'textdata', [])])]
    assert capsys.readouterr().out == ("called EditorGui.get_element_text with arg `node`\n"
                                       "called EditorGui.get_element_data with arg `node`\n"
                                       "called EditorGui.get_element_children with arg `node`\n"
                                       "called EditorGui.get_element_text with arg `item`\n"
                                       "called EditorGui.get_element_data with arg `item`\n"
                                       "called EditorGui.get_element_children with arg `item`\n"
                                       "called EditorGui.get_element_text with arg `text`\n"
                                       "called EditorGui.get_element_data with arg `text`\n")


def test_editorhelper_paste(monkeypatch, capsys):
    """unittest for EditorHelper.paste
    """
    def mock_get_data(item):
        """stub
        """
        print(f'called EditorGui.get_element_data with arg `{item}`')
        if item.endswith('p'):
            return {'x': 'y'}
        if item.endswith('p2'):
            return {'x': 'y', 'style': 'xxx'}
        return 'styletext'
    def mock_get_text(item):
        """stub
        """
        print(f'called EditorGui.get_element_text with arg `{item}`')
        if item == 'commented':
            return f'{testee.CMSTART} item'
        if item == 'textitem':
            return 'not an element'
        return f'{testee.ELSTART} item'
    def mock_get_parentpos(item):
        """stub
        """
        print(f'called EditorGui.get_element_parentpos with arg `{item}`')
        return 'parent', 2
    def mock_get_children(item):
        """stub
        """
        print(f'called EditorGui.get_element_children with arg `{item}`')
        return []
    def mock_get_children_2(item):
        """stub
        """
        print(f'called EditorGui.get_element_children with arg `{item}`')
        return ['x', 'y']
    def mock_zetzeronder(*args):
        """stub
        """
        print('called Editorhelper.zetzeronder with args', args)
    def mock_refresh():
        """stub
        """
        print('called Editor.refresh_preview')
    def mock_mark_dirty(value):
        """stub
        """
        print(f'called.Editor.mark_dirty with value `{value}`')
    # testee.getshortname
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
    monkeypatch.setattr(testobj.gui, 'get_element_parentpos', mock_get_parentpos)
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
    testobj.editor.refresh_preview = mock_refresh
    testobj.editor.mark_dirty = mock_mark_dirty
    testobj.zetzeronder = mock_zetzeronder
    testobj.editor.checkselection = lambda *x: False
    testobj.paste()
    assert capsys.readouterr().out == ''
    testobj.editor.checkselection = lambda *x: True
    testobj.editor.item = 'commented'
    testobj.paste(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `commented`\n"
            "called EditorGui.get_element_text with arg `commented`\n"
            "called EditorGui.meld with arg `Can't paste below comment`\n")
    testobj.editor.item = 'textitem'
    testobj.paste(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `textitem`\n"
            "called EditorGui.get_element_text with arg `textitem`\n"
            "called EditorGui.meld with arg `Can't paste below text`\n")
    testobj.editor.root = 'root'
    testobj.editor.item = testobj.editor.root
    testobj.paste(before=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `root`\n"
            "called EditorGui.meld with arg `Can't paste before the root`\n")
    testobj.editor.cut_txt = 'cut_text'
    testobj.editor.advance_selection_on_add = False
    testobj.paste(before=False)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `root`\n"
            "called EditorGui.meld with arg `Pasting as first element below root`\n"
            "called EditorGui.addtreeitem with args ('root', 'cut_text', 'cut_text', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.editor.item = 'item'
    testobj.editor.advance_selection_on_add = True
    testobj.paste(before=False)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `item`\n"
            "called EditorGui.get_element_parentpos with arg `item`\n"
            "called EditorGui.addtreeitem with args ('parent', 'item', 'cut_text', 3)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.paste(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `item`\n"
            "called EditorGui.get_element_text with arg `item`\n"
            "called EditorGui.addtreeitem with args ('item', 'cut_text', 'cut_text', -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.paste()
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `item`\n"
            "called EditorGui.get_element_parentpos with arg `item`\n"
            "called EditorGui.addtreeitem with args ('parent', 'item', 'cut_text', 2)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.editor.cut_txt = ''
    testobj.editor.cut_el = ['cut_el', []]
    testobj.editor.advance_selection_on_add = False
    testobj.paste(before=False)  # zou 1244 moeten raken
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `item`\n"
            "called EditorGui.get_element_parentpos with arg `item`\n"
            "called EditorGui.get_element_children with arg `parent`\n"
            "called Editorhelper.zetzeronder with args ('parent', 'cut_el', 3)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    testobj.editor.advance_selection_on_add = True
    testobj.paste(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `item`\n"
            "called EditorGui.get_element_text with arg `item`\n"
            "called Editorhelper.zetzeronder with args ('item', 'cut_el', -1)\n"
            "called EditorGui.set_selected_item(`None`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")
    monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children_2)
    testobj.paste()
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `item`\n"
            "called EditorGui.get_element_parentpos with arg `item`\n"
            "called EditorGui.get_element_children with arg `parent`\n"
            "called Editorhelper.zetzeronder with args ('parent', 'cut_el', -1)\n"
            "called EditorGui.set_selected_item(`None`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")


def test_editorhelper_zetzeronder(capsys):
    """unittest for EditorHelper.zetzeronder
    """
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    testobj.zetzeronder('node', ('item', {'x': 'y'}, [('subel', {}, [])]), 1)
    assert capsys.readouterr().out == (
            "called EditorGui.addtreeitem with args ('node', 'item', {'x': 'y'}, 1)\n"
            "called EditorGui.addtreeitem with args ('node', 'subel', {}, -1)\n")


def test_editorhelper_insert(monkeypatch, capsys):
    """unittest for EditorHelper.insert
    """
    def mock_get_data(item):
        """stub
        """
        print(f'called EditorGui.get_element_data with arg `{item}`')
        if item.endswith('p'):
            return {'x': 'y'}
        if item.endswith('p2'):
            return {'x': 'y', 'style': 'xxx'}
        return 'styletext'
    def mock_get_text(item):
        """stub
        """
        print(f'called EditorGui.get_element_text with arg `{item}`')
        if item == 'commented':
            return f'{testee.CMSTART} comment'
        if item == 'textitem':
            return 'textdata'
        if item == 'commented parent':
            return f'{testee.CMSTART} parent'
        if item == 'parent 2':
            return f'{testee.ELSTART} parent'
        return f'{testee.ELSTART} element'
    def mock_get_parent(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'commented parent'
    def mock_get_parent_2(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'parent'
    def mock_do_add(arg):
        """stub
        """
        print(f'called EditorGui.do_add_element with arg `{arg}`')
        return True, ('new', {'x': 'y'}, False)
    def mock_do_add_commented(arg):
        """stub
        """
        print(f'called EditorGui.do_add_element with arg `{arg}`')
        return True, ('new', {'x': 'y'}, True)
    def mock_do_add_style(arg):
        """stub
        """
        print(f'called EditorGui.do_add_element with arg `{arg}`')
        return True, ('style', {'x': 'y', 'styledata': 'xxx'}, False)
    def mock_refresh():
        """stub
        """
        print('called Editor.refresh_preview')
    def mock_mark_dirty(value):
        """stub
        """
        print(f'called.Editor.mark_dirty with value `{value}`')
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
    testobj.editor.refresh_preview = mock_refresh
    testobj.editor.mark_dirty = mock_mark_dirty
    testobj.editor.checkselection = lambda *x: False
    testobj.insert()
    assert capsys.readouterr().out == ''
    testobj.editor.checkselection = lambda *x: True
    testobj.editor.item = 'commented'
    testobj.insert(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `commented`\n"
            "called EditorGui.meld with arg `Can't insert below comment`\n")
    testobj.editor.item = 'textitem'
    testobj.insert(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `textitem`\n"
            "called EditorGui.meld with arg `Can't insert below text`\n")
    testobj.editor.item = 'element'
    testobj.insert(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.do_add_element with arg `under`\n")
    monkeypatch.setattr(testobj.gui, 'do_add_element', mock_do_add)
    testobj.editor.advance_selection_on_add = False
    testobj.insert(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.do_add_element with arg `under`\n"
            "called EditorGui.get_element_text with arg `element`\n"
            f"called EditorGui.addtreeitem with args ('element', '{testee.ELSTART} new',"
            " {'x': 'y'}, -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    testobj.editor.advance_selection_on_add = True
    testobj.insert(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.do_add_element with arg `under`\n"
            "called EditorGui.get_element_text with arg `element`\n"
            f"called EditorGui.addtreeitem with args ('element', '{testee.ELSTART} new',"
            " {'x': 'y'}, -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    testobj.insert(below=True, before=False)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.do_add_element with arg `under`\n"
            "called EditorGui.get_element_text with arg `element`\n"
            f"called EditorGui.addtreeitem with args ('element', '{testee.ELSTART} new',"
            " {'x': 'y'}, -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    testobj.insert(before=False)
    assert capsys.readouterr().out == (
            "called EditorGui.do_add_element with arg `after`\n"
            "called EditorGui.get_element_parent with arg `element`\n"
            "called EditorGui.get_element_text with arg `commented parent`\n"
            f"called EditorGui.addtreeitem with args ('', '{testee.CMELSTART} new',"
            " {'x': 'y'}, -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    testobj.insert()
    assert capsys.readouterr().out == (
            "called EditorGui.do_add_element with arg `before`\n"
            "called EditorGui.get_element_parent with arg `element`\n"
            "called EditorGui.get_element_text with arg `commented parent`\n"
            f"called EditorGui.addtreeitem with args ('', '{testee.CMELSTART} new',"
            " {'x': 'y'}, -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    monkeypatch.setattr(testobj.gui, 'do_add_element', mock_do_add_style)
    testobj.insert()
    assert capsys.readouterr().out == (
            "called EditorGui.do_add_element with arg `before`\n"
            "called EditorGui.get_element_parent with arg `element`\n"
            "called EditorGui.get_element_text with arg `commented parent`\n"
            "called EditorGui.addtreeitem with args"
            f" ('', '{testee.CMELSTART} style', {{'x': 'y', 'styledata': 'xxx'}}, -1)\n"
            # moet die styledata hier niet al uit de attrdict zijn verwijderd?
            "called EditorGui.addtreeitem with args ('node', 'xxx', 'xxx', -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_2)
    monkeypatch.setattr(testobj.gui, 'do_add_element', mock_do_add_commented)
    testobj.insert()
    assert capsys.readouterr().out == (
            "called EditorGui.do_add_element with arg `before`\n"
            "called EditorGui.get_element_parent with arg `element`\n"
            "called EditorGui.get_element_text with arg `parent`\n"
            f"called EditorGui.addtreeitem with args ('', '{testee.CMELSTART} new',"
            " {'x': 'y'}, -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")


def test_editorhelper_add_text(monkeypatch, capsys):
    """unittest for EditorHelper.add_text
    """
    def mock_getelname(*args):
        """stub
        """
        print('called getelname with args', args)
        return args[0] or 'elname'
    def mock_get_data(item):
        """stub
        """
        print(f'called EditorGui.get_element_data with arg `{item}`')
        if item.endswith('p'):
            return {'x': 'y'}
        if item.endswith('p2'):
            return {'x': 'y', 'style': 'xxx'}
        return 'styletext'
    def mock_get_text(item):
        """stub
        """
        print(f'called EditorGui.get_element_text with arg `{item}`')
        if item == 'commented':
            return f'{testee.CMSTART} comment'
        if item == 'textitem':
            return 'textdata'
        return f'{testee.ELSTART} comment'
    def mock_get_parent(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'commented parent'
    def mock_get_parent_2(item):
        """stub
        """
        print(f'called EditorGui.get_element_parent with arg `{item}`')
        return 'parent'
    def mock_do_add():
        """stub
        """
        print('called EditorGui.do_add_textvalue')
        return False, ()
    def mock_do_add_2():
        """stub
        """
        print('called EditorGui.do_add_textvalue')
        return True, ('newtext', False)
    def mock_do_add_commented():
        """stub
        """
        print('called EditorGui.do_add_textvalue')
        return True, ('newtext', True)
    def mock_refresh():
        """stub
        """
        print('called Editor.refresh_preview')
    def mock_mark_dirty(value):
        """stub
        """
        print(f'called.Editor.mark_dirty with value `{value}`')
    monkeypatch.setattr(testee, 'getelname', mock_getelname)
    testobj = testee.EditorHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
    monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
    testobj.editor.refresh_preview = mock_refresh
    testobj.editor.mark_dirty = mock_mark_dirty
    testobj.editor.checkselection = lambda *x: False
    testobj.add_text()
    assert capsys.readouterr().out == ''
    testobj.editor.checkselection = lambda *x: True
    testobj.editor.item = 'textitem'
    testobj.add_text(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `textitem`\n"
            "called EditorGui.meld with arg `Can't add text below text`\n")
    monkeypatch.setattr(testobj.gui, 'do_add_textvalue', mock_do_add)
    testobj.editor.advance_selection_on_add = False
    testobj.editor.item = 'element'
    testobj.add_text(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.do_add_textvalue\n")
    monkeypatch.setattr(testobj.gui, 'do_add_textvalue', mock_do_add_2)
    testobj.editor.advance_selection_on_add = False
    testobj.editor.item = 'element'
    testobj.add_text(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.do_add_textvalue\n"
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.addtreeitem with args ('element', 'newtext', 'newtext', -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    testobj.editor.advance_selection_on_add = True
    testobj.add_text(below=True)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.do_add_textvalue\n"
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.addtreeitem with args ('element', 'newtext', 'newtext', -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    testobj.add_text(below=True, before=False)
    assert capsys.readouterr().out == (
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.do_add_textvalue\n"
            "called EditorGui.get_element_text with arg `element`\n"
            "called EditorGui.addtreeitem with args ('element', 'newtext', 'newtext', -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    testobj.add_text(before=False)
    assert capsys.readouterr().out == (
            "called EditorGui.do_add_textvalue\n"
            "called EditorGui.get_element_parent with arg `element`\n"
            "called EditorGui.get_element_text with arg `commented parent`\n"
            "called getelname with args ('br', {}, False)\n"
            "called EditorGui.addtreeitem with args ('', 'br', 'br', 1)\n"
            "called EditorGui.addtreeitem with args ('', 'newtext', 'newtext', -1)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    testobj.add_text()
    assert capsys.readouterr().out == (
            "called EditorGui.do_add_textvalue\n"
            "called EditorGui.get_element_parent with arg `element`\n"
            "called EditorGui.get_element_text with arg `commented parent`\n"
            "called EditorGui.addtreeitem with args ('', 'newtext', 'newtext', -1)\n"
            "called getelname with args ('br', {}, False)\n"
            "called EditorGui.addtreeitem with args ('', 'br', 'br', 0)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")
    monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_2)
    monkeypatch.setattr(testobj.gui, 'do_add_element', mock_do_add_commented)
    testobj.add_text()
    assert capsys.readouterr().out == (
            "called EditorGui.do_add_textvalue\n"
            "called EditorGui.get_element_parent with arg `element`\n"
            "called EditorGui.get_element_text with arg `parent`\n"
            "called EditorGui.addtreeitem with args ('', 'newtext', 'newtext', -1)\n"
            "called getelname with args ('br', {}, False)\n"
            "called EditorGui.addtreeitem with args ('', 'br', 'br', 0)\n"
            "called EditorGui.set_selected_item(`node`)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n"
            "called EditorGui.set_item_expanded with args `element`, `True`\n")


# -- SearchHelper ---------------------
def test_searchhelper_init(capsys):
    """unittest for SearchHelper.init
    """
    testobj = testee.SearchHelper(MockEditor())
    assert hasattr(testobj, 'editor')
    assert hasattr(testobj, 'gui')
    assert testobj.search_args == []
    assert testobj.replace_args == []
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'


def test_searchhelper_search_from(monkeypatch, capsys):
    """unittest for SearchHelper.search_from
    """
    def mock_flatten(self, *args):
        """stub
        """
        return (('top', 'filenaam', {}), ('ele', f'{testee.ELSTART} html', {}))
    def mock_next(self, *args):
        """stub
        """
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
    monkeypatch.setattr(testobj, 'find_next', lambda *x: None)  # mock_next)
    testobj.search_from('ele')
    assert capsys.readouterr().out == ('called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')
    monkeypatch.setattr(MockEditorGui, 'get_search_args', lambda *x: (False, None))
    testobj.search_from('top')
    assert capsys.readouterr().out == ""


def test_searchhelper_search_next(monkeypatch, capsys):
    """unittest for SearchHelper.search_next
    """
    def mock_flatten(self, *args):
        """stub
        """
        return (('top', 'filenaam', {}), ('ele', f'{testee.ELSTART} html', {}))
    def mock_next(self, *args):
        """stub
        """
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
    monkeypatch.setattr(testobj, 'find_next', lambda *x: None)  # mock_next)
    testobj.search_specs = 'search_specs'
    testobj.search_next()
    assert capsys.readouterr().out == ('called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')


def test_searchhelper_replace_from(monkeypatch, capsys):
    """unittest for SearchHelper.replace_from
    """
    def mock_flatten(self, *args):
        """stub
        """
        return (('top', 'filenaam', {}), ('ele', f'{testee.ELSTART} html', {}))
    def mock_next(self, *args):
        """stub
        """
        print('called search.find_next() with args', args)
        return 'pos', 1
    def mock_replace(*args):
        """stub
        """
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
    monkeypatch.setattr(testobj, 'find_next', lambda *x: None)  # mock_next)
    testobj.replace_from('ele')
    assert capsys.readouterr().out == ('called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')
    monkeypatch.setattr(MockEditorGui, 'get_search_args', lambda *x, **y: (False, None))
    testobj.replace_from('top')
    assert capsys.readouterr().out == ""


def test_searchhelper_replace_next(monkeypatch, capsys):
    """unittest for SearchHelper.replace_next
    """
    def mock_replace(*args):
        """stub
        """
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
    """unittest for SearchHelper.replace_and_find
    """
    def mock_element(self, *args):
        """stub
        """
        print('called search.replace_element()')
    def mock_attr(self, *args):
        """stub
        """
        print('called search.replace_attr()')
    def mock_text(self, *args):
        """stub
        """
        print('called search.replace_text()')
    def mock_flatten(self, *args):
        """stub
        """
        return (('top', 'filenaam', {}), ('ele', f'{testee.ELSTART} html', {}))
    def mock_next(self, *args):
        """stub
        """
        print('called search.find_next() with args', args)
        return 'pos', 1
    def mock_next_2(self, *args):
        """stub
        """
        print('called search.find_next() with args', args)
        return ()
    testobj = testee.SearchHelper(MockEditor())
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
    monkeypatch.setattr(testobj, 'replace_element', mock_element)
    monkeypatch.setattr(testobj, 'replace_attr', mock_attr)
    monkeypatch.setattr(testobj, 'replace_text', mock_text)
    monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_args = ('x', 'y', 'z', 'a')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_and_find((1, 'ele'), False)
    assert testobj.search_pos == ('pos', 1)
    assert capsys.readouterr().out == ('called search.replace_element()\n'
                                       'called search.replace_attr()\n'
                                       'called search.replace_text()\n'
                                       "called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))\n"
                                       'called EditorGui.set_selected_item(`1`)\n')
    monkeypatch.setattr(testobj, 'find_next', mock_next_2)
    testobj.search_specs = 'search_specs'
    testobj.replace_and_find((1, 'ele'), True)
    assert capsys.readouterr().out == ('called search.replace_element()\n'
                                       'called search.replace_attr()\n'
                                       'called search.replace_text()\n'
                                       "called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", True, (1, 'ele'))\n"
                                       'called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')
    testobj.replace_args = ('', '', '', '')
    testobj.replace_and_find((1, 'ele'), False)
    assert capsys.readouterr().out == ("called search.find_next() with args (('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))\n"
                                       'called EditorGui.meld with arg `search_specs\n\n'
                                       'No (more) results`\n')


def test_searchhelper_find_next():
    """unittest for SearchHelper.find_next
    """
    treedata = [('ele1', f'{testee.ELSTART} html', {}),
                ('ele2', f'{testee.ELSTART} div', {}),
                ('ele3', f'{testee.ELSTART} div', {'id': '1'}),
                ('text', 'some text', {}),
                ('ele4', f'{testee.ELSTART} div', {'id': '2'}),
                ('ele5', f'{testee.ELSTART} div', {'class': 'footer'})]
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


def test_searchhelper_flatten_tree_1(capsys):
    """unittest for SearchHelper.flatten_tree: no children
    """
    testobj = testee.SearchHelper(MockEditor())
    data = testobj.flatten_tree('top')
    assert data == []
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'


def test_searchhelper_flatten_tree_2(monkeypatch, capsys):
    """unittest for SearchHelper.flatten_tree: regular
    """
    def mock_element_text(self, node):
        """stub
        """
        self.textcounter += 1
        data = (['', 'filenaam'] + 2 * [f'{testee.ELSTART} html']
                + 2 * [f'{testee.ELSTART} div id="1"'] + 2 * ['some text'])
        return data[self.textcounter]
    def mock_element_children(self, node):
        """stub
        """
        self.childcounter += 1
        return ['', ['ele1'], ['ele2'], ['text'], []][self.childcounter]
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_children', mock_element_children)
    testobj = testee.SearchHelper(MockEditor())
    # import pdb; pdb.set_trace()
    data = testobj.flatten_tree('top')
    assert data == [('ele1', f'{testee.ELSTART} html', {}), ('ele2', f'{testee.ELSTART} div', {}),
                    ('text', 'some text', {})]
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'


def test_searchhelper_flatten_tree_3(monkeypatch, capsys):
    """unittest for SearchHelper.flatten_tree: commented
    """
    def mock_element_text(self, node):
        """stub
        """
        self.textcounter += 1
        data = (['', 'fnm'] + 2 * [f'{testee.CMELSTART} html']
                + 2 * [f'{testee.CMELSTART} div id="1"'] + 2 * [f'{testee.CMSTART} some text'])
        return data[self.textcounter]
    def mock_element_children(self, node):
        """stub
        """
        self.childcounter += 1
        return [['top'], ['ele1'], ['ele2'], ['text'], []][self.childcounter]
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockEditorGui, 'get_element_children', mock_element_children)
    testobj = testee.SearchHelper(MockEditor())
    data = testobj.flatten_tree('top')
    assert data == [('ele1', f'{testee.CMELSTART} html', {}), ('ele2', f'{testee.CMELSTART} div', {}),
                    ('text', f'{testee.CMSTART} some text', {})]
    assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'


def test_searchhelper_replace_element(monkeypatch, capsys):
    """unittest for SearchHelper.replace_element
    """
    def mock_element_text(self, node):
        """stub
        """
        self.textcounter += 1
        data = ['', f'{testee.ELSTART} html', f'{testee.ELSTART} div id="1"',
                f'{testee.CMELSTART} hr', f'{testee.CMELSTART} p class="centered"']
        return data[self.textcounter]
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_element(('el1',))
    assert capsys.readouterr().out == ('called EditorGui.__init__\ncalled Editor.__init__()\n'
                                       'called EditorGui.set_element_text with args `el1`,'
                                       f' `{testee.ELSTART} x`\n')
    testobj.replace_element(('el2',))
    assert capsys.readouterr().out == (
            f'called EditorGui.set_element_text with args `el2`, `{testee.ELSTART} x id="1"`\n')
    testobj.replace_element(('el3',))
    assert capsys.readouterr().out == (
            f'called EditorGui.set_element_text with args `el3`, `{testee.CMELSTART} x`\n')
    testobj.replace_element(('el4',))
    assert capsys.readouterr().out == ('called EditorGui.set_element_text with args `el4`,'
                                       f' `{testee.CMELSTART} x class="centered"`\n')


def test_searchhelper_replace_attr(monkeypatch, capsys):
    """unittest for SearchHelper.replace_attr
    """
    def mock_element_data(self, node):
        """stub
        """
        return {"id": "1"}
    def mock_element_text(self, node):
        """stub
        """
        return f'{testee.ELSTART} html'
    monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_element_data)
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', 'y', '', 'a')
    testobj.replace_attr(('el1',))
    assert capsys.readouterr().out == (
            'called EditorGui.__init__\ncalled Editor.__init__()\n'
            "called EditorGui.set_element_data with args `el1`, `{'y': '1'}`\n"
            f"called EditorGui.set_element_text with args `el1`, `{testee.ELSTART} html`\n")
    monkeypatch.setattr(MockEditorGui, 'get_element_text', lambda *x: f'{testee.CMELSTART} div')
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_attr(('el2',))
    assert capsys.readouterr().out == (
            'called EditorGui.__init__\ncalled Editor.__init__()\n'
            "called EditorGui.set_element_data with args `el2`, `{'y': 'z'}`\n"
            f"called EditorGui.set_element_text with args `el2`, `{testee.CMELSTART} div`\n")
    monkeypatch.setattr(MockEditorGui, 'get_element_text', lambda *x: f'{testee.CMELSTART} p')
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', '', 'z', 'a')
    testobj.replace_attr(('el3',))
    assert capsys.readouterr().out == (
            'called EditorGui.__init__\ncalled Editor.__init__()\n'
            "called EditorGui.set_element_data with args `el3`, `{'id': 'z'}`\n"
            # f'called EditorGui.set_element_text with args `el3`, `{testee.ELSTART} p id="z"`\n')
            f'called EditorGui.set_element_text with args `el3`, `{testee.CMELSTART} p id="z"`\n')
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', '=/= y', 'z', 'a')
    testobj.replace_attr(('el4',))
    assert capsys.readouterr().out == (
            'called EditorGui.__init__\ncalled Editor.__init__()\n'
            "called EditorGui.set_element_data with args `el4`, `{'id': 'z'}`\n"
            # f'called EditorGui.set_element_text with args `el4`, `{testee.ELSTART} p id="z"`\n')
            f'called EditorGui.set_element_text with args `el4`, `{testee.CMELSTART} p id="z"`\n')


def test_searchhelper_replace_text(monkeypatch, capsys):
    """unittest for SearchHelper.replace_text
    """
    def mock_element_text(self, node):
        """stub
        """
        return 'some text'
    monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'y', 'z', 'tex')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_text(('ele',))
    assert capsys.readouterr().out == (
        'called EditorGui.__init__\ncalled Editor.__init__()\n'
        "called EditorGui.set_element_text with args `ele`, `some at`\n")
