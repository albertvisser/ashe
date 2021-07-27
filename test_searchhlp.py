import pytest
import ashe.base as base

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


def test_init(monkeypatch, capsys):
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', 'y', '', 'a')
    testobj.replace_attr(('el1',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_data for `el1` to `{'y': '1'}`\n"
                                       "called node.set_element_text for `el1` to `<> html`\n")
    def mock_element_text(self, node):
        return '<!> <> div'
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    testobj = base.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_attr(('el2',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_data for `el2` to `{'y': 'z'}`\n"
                                       "called node.set_element_text for `el2` to `<!> <> div`\n")
    def mock_element_text(self, node):
        return '<> p'
    monkeypatch.setattr(MockGui, 'get_element_text', mock_element_text)
    testobj = base.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'id', '1', 'a')
    testobj.replace_args = ('x', '', 'z', 'a')
    testobj.replace_attr(('el3',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_data for `el3` to `{'id': 'z'}`\n"
                                       'called node.set_element_text for `el3` to `<> p id="z"`\n')
    testobj = base.SearchHelper(MockEditor())
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
    testobj = base.SearchHelper(MockEditor())
    testobj.search_args = ('x', 'y', 'z', 'tex')
    testobj.replace_args = ('x', 'y', 'z', 'a')
    testobj.replace_text(('ele',))
    assert capsys.readouterr().out == ('called gui.__init__()\ncalled editor.__init__()\n'
                                       "called node.set_element_text for `ele` to `some at`\n")
