import pathlib
import types
import pytest
from ashe import base as testee

def test_check_for_csseditor_fail(monkeypatch, capsys):
    "patch import to fail for cssedit"
    def mock_import(name, *args):
        if name == 'cssedit':
            raise ModuleNotFoundError
        return orig_import(name, *args)
    orig_import = __import__  # Store original __import__
    import builtins
    monkeypatch.setattr(builtins, '__import__', mock_import)
    assert not testee.check_for_csseditor()


def test_check_for_csseditor(monkeypatch, capsys):
    """if cssedit not found on system, create fake package in user install ('.local')
    don't forget to remove it after test!
    """
    # fake_cssedit_path = ... / 'cssedit'
    # fake_cssedit_path.mkdir()
    # (fake_cssedit_path / 'editor').mkdir()
    # (fake_cssedit_path / 'editor' / 'main.py').touch()
    assert testee.check_for_csseditor()


class MockElement:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


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
    monkeypatch.setattr(testee, 'check_for_csseditor', lambda: False)
    testobj = testee.CssManager('parent')
    assert testobj._parent == 'parent'
    assert not testobj.cssedit_available
    monkeypatch.setattr(testee, 'check_for_csseditor', lambda: True)
    testobj = testee.CssManager('parent')
    assert testobj._parent == 'parent'
    assert testobj.cssedit_available
    monkeypatch.setattr(testee, 'toolkit', 'wx')
    testobj = testee.CssManager('parent')
    assert testobj._parent == 'parent'
    assert not testobj.cssedit_available
    monkeypatch.setattr(testee, 'check_for_csseditor', lambda: False)
    testobj = testee.CssManager('parent')
    assert testobj._parent == 'parent'
    assert not testobj.cssedit_available
    monkeypatch.setattr(testee, 'check_for_csseditor', lambda: False)

def mock_cssman_init(self, *args):
    print('called CssManager.__init__ with args', args)
    self._parent = types.SimpleNamespace(gui=types.SimpleNamespace(app='gui_app'))

class MockCssEditor:
    def __init__(self, *args, **kwargs):
        print('called CssEditor.__init__ with args', args, kwargs)
    def open(self, *args, **kwargs):
        print('called CssEditor.open with args', args, kwargs)
    def show_from_external(self):
        print('called CssEditor.show_from_external')

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
    assert capsys.readouterr().out == ('called ashegui.meld with arg `Cannot find'
                                       ' specified stylesheet file on file system`\n')
    # het hieronder opgegeven file bestaat niet maar ik heb kunnen zien dat de naam geresolved
    # wordt tot /home/albert/projects/test.css dus kan netjes verder mee gesimuleerd worden
    # maar dan nu met testee.pathlib.Path.exists
    testobj.call_editor_for_stylesheet('../test.css')
    assert capsys.readouterr().out == ('called ashegui.meld with arg `Cannot find'
                                       ' specified stylesheet file on file system`\n')


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


#-- EditorHelper ---------------------


#-- SearchHelper ---------------------
class MockGui:
    top = 'top'
    def __init__(self):
        print('called gui.__init__()')
        self.textcounter = self.datacounter = self.childcounter = 0
    def get_search_args(self, **kwargs):
        if kwargs.get('replace', True):
            return True, (('x', 'y', 'z', 'a'), 'search_specs', ('q', 'r', 's', 't'))
        else:
            return True, (('x', 'y', 'z', 'a'), 'search_specs')
    def set_selected_item(self, *args):
        print('called gui.set_selected_item(`{}`)'.format(args[0]))
    def meld(self, *args):
        print('called gui.meld(`{}`)'.format(args[0]))
    def get_element_text(self, node):
        return ''
    def set_element_text(self, node, data):
        pass
    def get_element_data(self, node):
        return {}
    def set_element_data(self, node, data):
        pass
    def get_element_children(self, node):
        return []  # 'node1', 'node2'


class MockEditor:
    def __init__(self):
        self.gui = MockGui()
        print('called editor.__init__()')


def test_searchhelper_init(monkeypatch, capsys):
    testobj = testee.SearchHelper(MockEditor())
    assert hasattr(testobj, 'editor')
    assert hasattr(testobj, 'gui')
    assert testobj.search_args == []
    assert testobj.replace_args == []
    assert capsys.readouterr().out == 'called gui.__init__()\ncalled editor.__init__()\n'


def test_search_from(monkeypatch, capsys):
    def mock_flatten(self, *args):
        return (('top', 'filenaam', {}), ('ele', '<> html', {}))
    def mock_next(self, *args):
        print('called search.find_next() with args `{}`'.format(args))
        return 'pos', 1
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_from('top')
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", False)`\n"
                                       'called gui.set_selected_item(`1`)\n')
    testobj.search_from('top', True)
    assert capsys.readouterr().out == ("called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", True)`\n"
                                       'called gui.set_selected_item(`1`)\n')
    testobj.search_from('ele')
    assert capsys.readouterr().out == ("called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))`\n"
                                       'called gui.set_selected_item(`1`)\n')
    testobj.search_from('ele', True)
    assert capsys.readouterr().out == ("called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", True, (1, 'ele'))`\n"
                                       'called gui.set_selected_item(`1`)\n')
    def mock_next(self, *args):
        return None
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_from('ele')
    assert capsys.readouterr().out == 'called gui.meld(`search_specs\n\nNo (more) results`)\n'


def test_search_next(monkeypatch, capsys):
    def mock_flatten(self, *args):
        return (('top', 'filenaam', {}), ('ele', '<> html', {}))
    def mock_next(self, *args):
        print('called search.find_next() with args `{}`'.format(args))
        return 'pos', 1
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_next()
    assert capsys.readouterr().out == 'called gui.__init__()\ncalled editor.__init__()\n'
    testobj.search_args = ('x', 'y', 'z', 'a')
    testobj.search_pos = (1, 'ele')
    testobj.search_next()
    assert capsys.readouterr().out == ("called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))`\n"
                                       'called gui.set_selected_item(`1`)\n')
    def mock_next(self, *args):
        return None
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_specs = 'search_specs'
    testobj.search_next()
    assert capsys.readouterr().out == 'called gui.meld(`search_specs\n\nNo (more) results`)\n'


def test_replace_from(monkeypatch, capsys):
    def mock_flatten(self, *args):
        return (('top', 'filenaam', {}), ('ele', '<> html', {}))
    def mock_next(self, *args):
        print('called search.find_next() with args `{}`'.format(args))
        return 'pos', 1
    def mock_replace(*args):
        print('called search.replace_and_find() with args `{}`, `{}`'.format(args[0], args[1]))
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    monkeypatch.setattr(testobj, 'replace_and_find', mock_replace)
    testobj.replace_from('top')
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", False)`\n"
                                       "called search.replace_and_find() with args `('pos', 1)`,"
                                       ' `False`\n')
    testobj.replace_from('top', True)
    assert capsys.readouterr().out == ("called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", True)`\n"
                                       "called search.replace_and_find() with args `('pos', 1)`,"
                                       ' `True`\n')
    testobj.replace_from('ele')
    assert capsys.readouterr().out == ("called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))`\n"
                                       "called search.replace_and_find() with args `('pos', 1)`,"
                                       ' `False`\n')
    testobj.replace_from('ele', True)
    assert capsys.readouterr().out == ("called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", True, (1, 'ele'))`\n"
                                       "called search.replace_and_find() with args `('pos', 1)`,"
                                       ' `True`\n')
    def mock_next(self, *args):
        return None
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.replace_from('ele')
    assert capsys.readouterr().out == 'called gui.meld(`search_specs\n\nNo (more) results`)\n'


def test_replace_next(monkeypatch, capsys):
    def mock_replace(*args):
        print('called search.replace_and_find() with args `{}`, `{}`'.format(args[0], args[1]))
    testobj = testee.SearchHelper(MockEditor())
    monkeypatch.setattr(testobj, 'replace_and_find', mock_replace)
    testobj.replace_next()
    assert capsys.readouterr().out == 'called gui.__init__()\ncalled editor.__init__()\n'
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.search_pos = '1'
    testobj.replace_next()
    assert capsys.readouterr().out == 'called search.replace_and_find() with args `1`, `False`\n'
    testobj.replace_next(True)
    assert capsys.readouterr().out == 'called search.replace_and_find() with args `1`, `True`\n'


def test_replace_and_find(monkeypatch, capsys):
    def mock_element(self, *args):
        print('called search.replace_element()')
    def mock_attr(self, *args):
        print('called search.replace_attr()')
    def mock_text(self, *args):
        print('called search.replace_text()')
    def mock_flatten(self, *args):
        return (('top', 'filenaam', {}), ('ele', '<> html', {}))
    def mock_next(self, *args):
        print('called search.find_next() with args `{}`'.format(args))
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
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       'called search.replace_element()\n'
                                       'called search.replace_attr()\n'
                                       'called search.replace_text()\n'
                                       "called search.find_next() with args `(('x', 'y', 'z', 'a')"
                                       ", False, (1, 'ele'))`\n"
                                       'called gui.set_selected_item(`1`)\n')
    def mock_next(self, *args):
        return None
    monkeypatch.setattr(testobj, 'find_next', mock_next)
    testobj.search_specs = 'search_specs'
    testobj.replace_next()
    assert capsys.readouterr().out == ('called search.replace_element()\n'
                                       'called search.replace_attr()\n'
                                       'called search.replace_text()\n'
                                       'called gui.meld(`search_specs\n\nNo (more) results`)\n')


def test_find_next(monkeypatch, capsys):
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


def test_flatten_tree_1(monkeypatch, capsys):
    "no children"
    testobj = testee.SearchHelper(MockEditor())
    data = testobj.flatten_tree('top')
    assert data == []


def test_flatten_tree_2(monkeypatch, capsys):
    "regular"
    def mock_element_text(self, node):
        self.textcounter += 1
        data = ['', 'filenaam'] + 2 * ['<> html'] + 2 * ['<> div id="1"'] + 2 * ['some text']
        return data[self.textcounter]
    def mock_element_children(self, node):
        self.childcounter += 1
        return ['', ['ele1'], ['ele2'], ['text'], []][self.childcounter]
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockGui, 'get_element_children', mock_element_children)
    testobj = testee.SearchHelper(MockEditor())
    # import pdb; pdb.set_trace()
    data = testobj.flatten_tree('top')
    assert data == [('ele1', '<> html', {}), ('ele2', '<> div', {}), ('text', 'some text', {})]


def test_flatten_tree_3(monkeypatch, capsys):
    "commented"
    def mock_element_text(self, node):
        self.textcounter += 1
        data = ['', 'fnm'] + 2 * ['<!> <> html'] + 2 * ['<!> <> div id="1"'] + 2 * ['<!> some text']
        return data[self.textcounter]
    def mock_element_children(self, node):
        self.childcounter += 1
        return [['top'], ['ele1'], ['ele2'], ['text'], []][self.childcounter]
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockGui, 'get_element_children', mock_element_children)
    testobj = testee.SearchHelper(MockEditor())
    data = testobj.flatten_tree('top')
    assert data == [('ele1', '<!> <> html', {}), ('ele2', '<!> <> div', {}),
                    ('text', '<!> some text', {})]


def test_replace_element(monkeypatch, capsys):
    def mock_element_text(self, node):
        self.textcounter += 1
        data = ['', '<> html', '<> div id="1"', '<!> <> hr', '<!> <> p class="centered"']
        return data[self.textcounter]
    def mock_set_text(self, node, *args):
        print('called node.set_element_text for `{}` to `{}`'.format(node, args[0]))
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockGui, 'set_element_text', mock_set_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_element(('el1',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       'called node.set_element_text for `el1` to `<> x`\n')
    testobj.replace_element(('el2',))
    assert capsys.readouterr().out == 'called node.set_element_text for `el2` to `<> x id="1"`\n'
    testobj.replace_element(('el3',))
    assert capsys.readouterr().out == 'called node.set_element_text for `el3` to `<!> <> x`\n'
    testobj.replace_element(('el4',))
    assert capsys.readouterr().out == ('called node.set_element_text for `el4` to `<!> <> x '
                                       'class="centered"`\n')


def test_replace_attr(monkeypatch, capsys):
    def mock_element_data(self, node):
        return {"id": "1"}
    def mock_set_data(self, node, *args):
        print('called node.set_element_data for `{}` to `{}`'.format(node, args[0]))
    def mock_element_text(self, node):
        return '<> html'
    def mock_set_text(self, node, *args):
        print('called node.set_element_text for `{}` to `{}`'.format(node, args[0]))
    monkeypatch.setattr(MockGui, 'get_element_data', mock_element_data)
    monkeypatch.setattr(MockGui, 'set_element_data', mock_set_data)
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockGui, 'set_element_text', mock_set_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', 'y', '', 'a')
    testobj.replace_attr(('el1',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_data for `el1` to `{'y': '1'}`\n"
                                       "called node.set_element_text for `el1` to `<> html`\n")
    def mock_element_text(self, node):
        return '<!> <> div'
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_attr(('el2',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_data for `el2` to `{'y': 'z'}`\n"
                                       "called node.set_element_text for `el2` to `<!> <> div`\n")
    def mock_element_text(self, node):
        return '<> p'
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', '', 'z', 'a')
    testobj.replace_attr(('el3',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_data for `el3` to `{'id': 'z'}`\n"
                                       'called node.set_element_text for `el3` to `<> p id="z"`\n')
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', '=/= y', 'z', 'a')
    testobj.replace_attr(('el4',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_data for `el4` to `{'id': 'z'}`\n"
                                       'called node.set_element_text for `el4` to `<> p id="z"`\n')


def test_replace_text(monkeypatch, capsys):
    def mock_element_text(self, node):
        return 'some text'
    def mock_set_text(self, node, *args):
        print('called node.set_element_text for `{}` to `{}`'.format(node, args[0]))
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    monkeypatch.setattr(MockGui, 'set_element_text', mock_set_text)
    testobj = testee.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'y', 'z', 'tex')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_text(('ele',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_text for `ele` to `some at`\n")
