"""unittests for ./ashe/main.py
"""
import pathlib
import types
import pytest
from ashe import main as testee

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
    def addtreetop(self, *args):
        print('called EditorGui.addtreetop with args', args)
    def addtreeitem(self, *args):
        print('called EditorGui.addtreeitem with args', args)
        return 'node'
    def adjust_dtd_menu(self):
        print('called EditorGui.adjust_dtd_menu')
    def ask_how_to_continue(self):
        print('called EditorGui.ask_how_to_continue')
        return True, 'x'
    def close(self):
        print('called EditorGui.close()')
    def create_menu(self):
        print('called EditorGui.create_menu')
    def create_splitter(self):
        print('called EditorGui.create_splitter')
    def create_tree_on_left(self):
        print('called EditorGui.create_tree_on_left')
    def create_preview_on_right(self):
        print('called EditorGui.create_preview_on_right')
    def create_statusbar_at_bottom(self):
        print('called EditorGui.create_statusbar_at_bottom')
    def do_add_element(self, arg):
        print(f'called EditorGui.do_add_element with arg `{arg}`')
        return False, ()
    def do_add_textvalue(self, arg):
        print(f'called EditorGui.do_add_textvalue with arg `{arg}`')
        return False, ()
    def do_delete_item(self, arg):
        print(f'called EditorGui.do_delete_item with arg `{arg}`')
        return 'preceding item'
    def ensure_item_visible(self, arg):
        print(f'called EditorGui.ensure_item_visible with arg `{arg}`')
    def finalize_display(self):
        print('called EditorGui.finalize_display')
    def get_css_data(self):
        print('called EditorGui.get_css_data')
        return True, 'x'
    def get_dtd(self):
        print('called EditorGui.get_dtd')
        return True, 'x'
    def get_element_children(self, node):
        print(f'called EditorGui.get_element_children with arg `{node}`')
        return []  # 'node1', 'node2'
    def get_element_data(self, node):
        print(f'called EditorGui.get_element_data with arg `{node}`')
        return {}
    def get_element_parent(self, node):
        print(f'called EditorGui.get_element_parent with arg `{node}`')
        return 'pp'
    def get_element_parentpos(self, *args):
        print('called EditorGui.get_element_parentpos with args', args)
        return 'pp', 0
    def get_element_text(self, node):
        print(f'called EditorGui.get_element_text with arg `{node}`')
        return 'p'
    def get_search_args(self, **kwargs):
        print('called EditorGui.get_search_args with args', kwargs)
        if kwargs.get('replace', True):
            return True, (('x', 'y', 'z', 'a'), 'search_specs', ('q', 'r', 's', 't', False))
        return True, (('x', 'y', 'z', 'a'), 'search_specs')
    def get_screen_title(self):
        return 'screen title'
    def get_selected_item(self):
        print('called EditorGui.get_selected_item')
    def go(self):
        print('called EditorGui.go()')
    def init_tree(self, *args):
        print('called EditorGui.init_tree with args', args)
    def set_element_data(self, node, data):
        print(f'called EditorGui.set_element_data with args `{node}`, `{data}`')
    def set_element_text(self, node, data):
        print(f'called EditorGui.set_element_text with args `{node}`, `{data}`')
    def set_item_expanded(self, node, value):
        print(f'called EditorGui.set_item_expanded with args `{node}`, `{value}`')
    def set_screen_title(self, text):
        print(f'called EditorGui.set_screen_title with arg `{text}`')
    def set_selected_item(self, *args):
        print(f'called EditorGui.set_selected_item(`{args[0]}`)')
    def show_statusbar_message(self, msg):
        print(f'called EditorGui.show_statusbar_message with arg `{msg}`')
    def validate(self, *args):
        print('called EditorGui.validate with args', args)
    def meld(self, msg):
        """stub
        """
        print(f'called EditorGui.meld with arg `{msg}`')


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


def mock_refresh(self):
    """stub
    """
    print('called Editor.refresh_preview')


def mock_mark_dirty(self, value):
    """stub
    """
    print(f'called.Editor.mark_dirty with value `{value}`')


class TestEditor:
    """unittests for main.Editor
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Editor object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called Editor.__init__ with args', args)
        monkeypatch.setattr(testee.Editor, '__init__', mock_init)
        testobj = testee.Editor()
        testobj.xmlfn = ''
        testobj.root = 'root'
        testobj.gui = MockEditorGui()
        testobj.edhlp = MockEditorHelper()
        testobj.srchhlp = MockSearchHelper()
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           'called EditorGui.__init__\n'
                                           'called EditorHelper.__init__\n'
                                           'called SearchHelper.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Editor.__init__
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
                                           'called EditorGui.create_menu\n'
                                           'called EditorGui.create_splitter\n'
                                           'called EditorGui.create_tree_on_left\n'
                                           'called EditorGui.create_preview_on_right\n'
                                           'called EditorGui.create_statusbar_at_bottom\n'
                                           'called EditorGui.finalize_display\n'
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
                                           'called EditorGui.create_menu\n'
                                           'called EditorGui.create_splitter\n'
                                           'called EditorGui.create_tree_on_left\n'
                                           'called EditorGui.create_preview_on_right\n'
                                           'called EditorGui.create_statusbar_at_bottom\n'
                                           'called EditorGui.finalize_display\n'
                                           'called CssManager.__init__()\n'
                                           'called EditorHelper.__init__\n'
                                           'called SearchHelper.__init__\n'
                                           'called EditorGui.meld with arg `message`\n'
                                           'called EditorGui.go()\n')

    def test_file2soup(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.file2soup
        """
        def mock_bs(*args):
            """stub
            """
            print('called BeautifulSoup with args', args)
            return 'root'
        monkeypatch.setattr(testee.bs, 'BeautifulSoup', mock_bs)
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_soup2data(self, monkeypatch, capsys):
        """unittest for Editor.soup2data
        """
        def mock_add_node(self, *args):
            """stub
            """
            print('called Editor.add_node_to_tree with args', args)
        monkeypatch.setattr(testee.Editor, 'add_node_to_tree', mock_add_node)
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_add_node_to_tree(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_data2soup(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.data2soup() == ['doctypedata', 'element']
        assert capsys.readouterr().out == (
                "called bs.BeautifulSoup with args ('', 'lxml')\n"
                "called bs.Doctype with arg doctypedata\n"
                "called BeautifulSoup.new_tag with arg element\n"
                "called Editor.expandnode with args (['other'], 'element', 'elementdata')\n")

    def test_expandnode(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_soup2file(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.soup2file
        """
        def mock_init_editor(self, filename):
            """stub for initializing Editor
            """
            print(f'called Editor.__init__ with filename `{filename}`')
            self.xmlfn = filename
        monkeypatch.setattr(testee.Editor, '__init__', mock_init_editor)
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        xmlfn = tmp_path / 'testsoup2file.html'
        backup = tmp_path / 'testsoup2file.html.bak'
        testobj = testee.Editor(str(xmlfn))
        assert capsys.readouterr().out == f'called Editor.__init__ with filename `{xmlfn}`\n'
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.soup = 12
        testobj.soup2file(str(xmlfn))
        assert not backup.exists()
        assert xmlfn.read_text() == '12'
        assert capsys.readouterr().out == 'called.Editor.mark_dirty with value `False`\n'
        xmlfn.unlink()
        testobj.soup2file(str(xmlfn), saveas=True)
        assert not backup.exists()
        assert xmlfn.read_text() == '12'
        assert capsys.readouterr().out == 'called.Editor.mark_dirty with value `False`\n'
        testobj.soup = 15
        testobj.soup2file(str(xmlfn))
        assert backup.read_text() == '12'
        assert xmlfn.read_text() == '15'
        assert capsys.readouterr().out == 'called.Editor.mark_dirty with value `False`\n'
        backup.unlink()
        testobj.soup = 18
        testobj.soup2file(str(xmlfn), saveas=True)
        assert not backup.exists()
        assert xmlfn.read_text() == '18'
        assert capsys.readouterr().out == 'called.Editor.mark_dirty with value `False`\n'

    def test_get_menulist(self, monkeypatch, capsys):
        """unittest for Editor.get_menulist
        """
        menuitems_per_menu = (7, 6, 16, 9, 13, 1)
        sep_locations = ((0, 5), (1, 2), (1, 4), (2, 2), (2, 8), (3, 4), (4, 2), (4, 7), (4, 10))
        with_indicator = ((1, 0), (1, 1))
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_mark_dirty(self, monkeypatch, capsys):
        """unittest for Editor.mark_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        unchanged = f"xxx - {testee.TITEL}"
        changed = f"xxx* - {testee.TITEL}"
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

    def test_check_tree_state(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_is_stylesheet_node(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.is_stylesheet_node('node')
        assert capsys.readouterr().out == 'called EditorGui.get_element_text for `node`\n'

        monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.is_stylesheet_node('node')
        assert capsys.readouterr().out == 'called EditorGui.get_element_text for `node`\n'

        monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_3)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.is_stylesheet_node('node')
        assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                           'called EditorGui.get_element_data for `node`\n')

        monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_3)
        monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_get_data_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.is_stylesheet_node('node')
        assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                           'called EditorGui.get_element_data for `node`\n')

    def test_in_body(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        counter = 0
        assert not testobj.in_body('node')
        assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                           'called EditorGui.get_element_parent for `node`\n')
        # head
        monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_2)
        monkeypatch.setattr(MockEditorGui, 'get_element_parent', mock_get_parent_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        counter = 0
        assert not testobj.in_body('node')
        assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                           'called EditorGui.get_element_parent for `node`\n')
        testobj = self.setup_testobj(monkeypatch, capsys)
        # body
        monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_3)
        testobj = self.setup_testobj(monkeypatch, capsys)
        counter = 0
        assert testobj.in_body('node')
        assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                           'called EditorGui.get_element_parent for `node`\n')
        testobj = self.setup_testobj(monkeypatch, capsys)
        # element onder head
        monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_get_text_4)
        testobj = self.setup_testobj(monkeypatch, capsys)
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        counter = 0
        assert testobj.in_body('node')
        assert capsys.readouterr().out == ('called EditorGui.get_element_text for `node`\n'
                                           'called EditorGui.get_element_parent for `node`\n'
                                           'called EditorGui.get_element_text for `x`\n'
                                           'called EditorGui.get_element_parent for `x`\n'
                                           'called EditorGui.get_element_text for `x`\n'
                                           'called EditorGui.get_element_parent for `x`\n')

    def test_newxml(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.newxml()
        assert capsys.readouterr().out == ("called Editor.check_tree_state\n"
                "called Editor.file2soup with args () {}\n"
                "called Editor.soup2data with args () {'message': 'started new document'}\n"
                "called Editor.refresh_preview\n")
        monkeypatch.setattr(testee.Editor, 'file2soup', lambda *x: 'error')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.newxml()
        assert capsys.readouterr().out == ("called Editor.check_tree_state\n"
                                           "called EditorGui.meld with arg `error`\n")
        monkeypatch.setattr(testee.Editor, 'check_tree_state', lambda *x: -1)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.newxml()
        assert capsys.readouterr().out == ''

    def test_openxml(self, monkeypatch, capsys):
        """unittest for Editor.openxml
        """
        def mock_check_state(self):
            """stub
            """
            print('called Editor.check_tree_state')
            return 0
        def mock_ask_filename(*args):
            print('called gui.ask_for_open_filename with args', args)
            return ''
        def mock_ask_filename_2(*args):
            print('called gui.ask_for_open_filename with args', args)
            return 'filename'
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
        def mock_build(*args):
            print('called Editor.build_mask with args', args)
            return 'filemask'
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_filename)
        monkeypatch.setattr(testee.gui, 'build_mask', mock_build)
        monkeypatch.setattr(testee.Editor, 'check_tree_state', mock_check_state)
        monkeypatch.setattr(testee.Editor, 'file2soup', mock_file2soup)
        monkeypatch.setattr(testee.Editor, 'soup2data', mock_soup2data)
        monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh_preview)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.openxml()
        assert capsys.readouterr().out == (
            'called Editor.check_tree_state\n'
            "called Editor.build_mask with args ('html',)\n"
            "called gui.ask_for_open_filename with args"
            f" ({testobj.gui}, '{testee.os.getcwd()}', 'filemask')\n")

        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_filename_2)
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = 'xmlfile'
        testobj.openxml()
        assert testobj.xmlfn == 'filename'
        assert capsys.readouterr().out == (
            'called Editor.check_tree_state\n'
            "called Editor.build_mask with args ('html',)\n"
            f"called gui.ask_for_open_filename with args ({testobj.gui}, 'xmlfile', 'filemask')\n"
            "called Editor.file2soup with args () {'fname': 'filename'}\n"
            "called Editor.soup2data with args ('filename', 'loaded filename') {}\n"
            "called Editor.refresh_preview\n")
        monkeypatch.setattr(testee.Editor, 'file2soup', lambda *x, **y: 'error')
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = 'xmlfile'
        testobj.openxml()
        assert testobj.xmlfn == 'xmlfile'
        assert capsys.readouterr().out == (
            "called Editor.check_tree_state\n"
            "called Editor.build_mask with args ('html',)\n"
            f"called gui.ask_for_open_filename with args ({testobj.gui}, 'xmlfile', 'filemask')\n"
            "called EditorGui.meld with arg `error`\n")

        monkeypatch.setattr(testee.Editor, 'check_tree_state', lambda *x: -1)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.openxml()
        assert capsys.readouterr().out == ''

    def test_savexml(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = ''
        testobj.savexml()
        assert capsys.readouterr().out == 'called Editor.savexmlas\n'
        testobj.xmlfn = 'filename'
        testobj.savexml()
        assert capsys.readouterr().out == ('called Editor.data2soup with args () {}\n'
                                           "called Editor.soup2file with args ('filename',) {}\n"
                                           'called EditorGui.show_statusbar_message with arg'
                                           ' `saved filename`\n')
        monkeypatch.setattr(testee.Editor, 'soup2file', mock_soup2file_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = 'filename'
        testobj.savexml()
        assert capsys.readouterr().out == ('called Editor.data2soup with args () {}\n'
                                           'called EditorGui.meld with arg `Error`\n')

    def test_savexmlas(self, monkeypatch, capsys):
        """unittest for Editor.savexmlas
        """
        def mock_ask_filename(*args):
            print('called gui.ask_for_save_filename with args', args)
            return ''
        def mock_ask_filename_2(*args):
            print('called gui.ask_for_save_filename with args', args)
            return 'filename'
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
        def mock_build(*args):
            print('called Editor.build_mask with args', args)
            return 'filemask'
        monkeypatch.setattr(testee.gui, 'build_mask', mock_build)
        monkeypatch.setattr(testee.gui, 'ask_for_save_filename', mock_ask_filename)
        monkeypatch.setattr(testee.Editor, 'data2soup', mock_data2soup)
        monkeypatch.setattr(testee.Editor, 'soup2file', mock_soup2file)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.savexmlas()
        assert capsys.readouterr().out == (
            "called Editor.build_mask with args ('html',)\n"
            "called gui.ask_for_save_filename with args"
            f" ({testobj.gui}, '{testee.os.getcwd()}', 'filemask')\n")
        monkeypatch.setattr(testee.gui, 'ask_for_save_filename', mock_ask_filename_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = 'xmlfile'
        testobj.savexmlas()
        assert testobj.xmlfn == 'filename'
        assert capsys.readouterr().out == (
            "called Editor.build_mask with args ('html',)\n"
            f"called gui.ask_for_save_filename with args ({testobj.gui}, 'xmlfile', 'filemask')\n"
            'called Editor.data2soup with args () {}\n'
            "called Editor.soup2file with args ('filename',) {'saveas': True}\n"
            'called EditorGui.set_element_text with args `top`, `filename`\n'
            'called EditorGui.show_statusbar_message with arg `saved as filename`\n')
        monkeypatch.setattr(testee.Editor, 'soup2file', mock_soup2file_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = 'xmlfile'
        testobj.savexmlas()
        assert testobj.xmlfn == 'xmlfile'
        assert capsys.readouterr().out == (
            "called Editor.build_mask with args ('html',)\n"
            f"called gui.ask_for_save_filename with args ({testobj.gui}, 'xmlfile', 'filemask')\n"
            'called Editor.data2soup with args () {}\n'
            'called EditorGui.meld with arg `Error`\n')

    def test_reopenxml(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = 'xxx'
        testobj.reopenxml()
        assert capsys.readouterr().out == (
                "called Editor.file2soup with args () {'fname': 'xxx'}\n"
                "called Editor.soup2data with args ('xxx', 'reloaded xxx') {}\n"
                'called Editor.refresh_preview\n')
        monkeypatch.setattr(testee.Editor, 'file2soup', lambda *x, **y: 'error')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reopenxml()
        assert capsys.readouterr().out == "called EditorGui.meld with arg `error`\n"

    def test_close(self, monkeypatch, capsys):
        """unittest for Editor.close
        """
        def mock_check_state(self):
            """stub
            """
            print('called Editor.check_tree_state')
            return 0
        monkeypatch.setattr(testee.Editor, 'check_tree_state', lambda *x: -1)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testee.Editor, 'check_tree_state', mock_check_state)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close()
        assert capsys.readouterr().out == 'called Editor.check_tree_state\ncalled EditorGui.close()\n'

    def test_expand(self, monkeypatch, capsys):
        """unittest for Editor.expand
        """
        def mock_expand():
            """stub
            """
            print('called EditorGui.expand')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.expand = mock_expand
        testobj.expand()
        assert capsys.readouterr().out == 'called EditorGui.expand\n'

    def test_collapse(self, monkeypatch, capsys):
        """unittest for Editor.collapse
        """
        def mock_collapse():
            """stub
            """
            print('called EditorGui.collapse')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.collapse = mock_collapse
        testobj.collapse()
        assert capsys.readouterr().out == 'called EditorGui.collapse\n'

    def test_advance_selection_onoff(self, monkeypatch, capsys):
        """unittest for Editor.advance_selection_onoff
        """
        def mock_get_setting():
            """stub
            """
            print('called EditorGui.get_adv_sel_setting')
            return 'sett'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_adv_sel_setting = mock_get_setting
        testobj.advance_selection_onoff()
        assert capsys.readouterr().out == 'called EditorGui.get_adv_sel_setting\n'
        assert testobj.advance_selection_on_add == 'sett'

    def test_refresh_preview(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.refresh_preview = mock_refresh
        testobj.refresh_preview()
        assert capsys.readouterr().out == ('called Editor.data2soup\n'
                                           'called EditorGui.refresh_preview with arg `soup`\n')

    def test_checkselection(self, monkeypatch, capsys):
        """unittest for Editor.checkselection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.checkselection()
        assert testobj.item is None
        assert capsys.readouterr().out == (
                'called EditorGui.get_selected_item\n'
                'called EditorGui.meld with arg `You need to select an element or text first`\n')

        monkeypatch.setattr(MockEditorGui, 'get_selected_item', lambda *x: 'top')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.top = 'top'
        assert not testobj.checkselection()
        assert testobj.item == 'top'
        assert capsys.readouterr().out == (
                'called EditorGui.meld with arg `You need to select an element or text first`\n')

        monkeypatch.setattr(MockEditorGui, 'get_selected_item', lambda *x: 'not_top')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.top = 'top'
        assert testobj.checkselection()
        assert testobj.item == 'not_top'
        assert capsys.readouterr().out == ''

    def test_edit(self, monkeypatch, capsys):
        """unittest for Editor.edit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.edit()
        assert capsys.readouterr().out == 'called EditorHelper.edit\n'
        monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.edit()
        assert capsys.readouterr().out == ''

    def test_comment(self, monkeypatch, capsys):
        """unittest for Editor.comment
        """
        monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.comment()
        assert capsys.readouterr().out == 'called EditorHelper.comment\n'
        monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.comment()
        assert capsys.readouterr().out == ''

    def test_cut(self, monkeypatch, capsys):
        """unittest for Editor.cut
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cut()
        assert capsys.readouterr().out == "called EditorHelper.copy with args {'cut': True}\n"

    def test_delete(self, monkeypatch, capsys):
        """unittest for Editor.delete
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.delete()
        assert capsys.readouterr().out == ("called EditorHelper.copy with args {'cut': True,"
                                           " 'retain': False}\n")

    def test_copy(self, monkeypatch, capsys):
        """unittest for Editor.copy
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.copy()
        assert capsys.readouterr().out == "called EditorHelper.copy with args {}\n"

    def test_paste_after(self, monkeypatch, capsys):
        """unittest for Editor.paste_after
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paste_after()
        assert capsys.readouterr().out == "called EditorHelper.paste with args {'before': False}\n"

    def test_paste_below(self, monkeypatch, capsys):
        """unittest for Editor.paste_below
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paste_below()
        assert capsys.readouterr().out == "called EditorHelper.paste with args {'below': True}\n"

    def test_paste(self, monkeypatch, capsys):
        """unittest for Editor.paste
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paste()
        assert capsys.readouterr().out == "called EditorHelper.paste with args {}\n"

    def test_insert(self, monkeypatch, capsys):
        """unittest for Editor.insert
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.insert()
        assert capsys.readouterr().out == "called EditorHelper.insert with args {}\n"

    def test_insert_after(self, monkeypatch, capsys):
        """unittest for Editor.insert_after
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.insert_after()
        assert capsys.readouterr().out == "called EditorHelper.insert with args {'before': False}\n"

    def test_insert_child(self, monkeypatch, capsys):
        """unittest for Editor.insert_child
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.insert_child()
        assert capsys.readouterr().out == "called EditorHelper.insert with args {'below': True}\n"

    def test_add_text(self, monkeypatch, capsys):
        """unittest for Editor.add_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text()
        assert capsys.readouterr().out == "called EditorHelper.add_text with args {}\n"

    def test_add_text_after(self, monkeypatch, capsys):
        """unittest for Editor.add_text_after
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text_after()
        assert capsys.readouterr().out == "called EditorHelper.add_text with args {'before': False}\n"

    def test_add_textchild(self, monkeypatch, capsys):
        """unittest for Editor.add_textchild
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_textchild()
        assert capsys.readouterr().out == "called EditorHelper.add_text with args {'below': True}\n"

    def test_search(self, monkeypatch, capsys):
        """unittest for Editor.search
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search()
        assert capsys.readouterr().out == (
            "called EditorGui.get_selected_item\n"
            "called SearchHelper.search_from with args () {'item': None}\n")

    def test_search_last(self, monkeypatch, capsys):
        """unittest for Editor.search_last
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_last()
        assert capsys.readouterr().out == (
                "called EditorGui.get_selected_item\n"
                "called SearchHelper.search_from with args () {'reverse': True, 'item': None}\n")

    def test_search_next(self, monkeypatch, capsys):
        """unittest for Editor.search_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_next()
        assert capsys.readouterr().out == "called SearchHelper.search_next with args {}\n"

    def test_search_prev(self, monkeypatch, capsys):
        """unittest for Editor.search_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_prev()
        assert capsys.readouterr().out == "called SearchHelper.search_next with args {'reverse': True}\n"

    def test_replace(self, monkeypatch, capsys):
        """unittest for Editor.replace
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace()
        assert capsys.readouterr().out == (
                "called EditorGui.get_selected_item\n"
                "called SearchHelper.replace_from with args () {'item': None}\n")

    def test_replace_last(self, monkeypatch, capsys):
        """unittest for Editor.replace_last
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace_last()
        assert capsys.readouterr().out == (
                "called EditorGui.get_selected_item\n"
                "called SearchHelper.replace_from with args () {'reverse': True, 'item': None}\n")

    def test_replace_and_next(self, monkeypatch, capsys):
        """unittest for Editor.replace_and_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace_and_next()
        assert capsys.readouterr().out == "called SearchHelper.replace_next with args {}\n"

    def test_replace_and_prev(self, monkeypatch, capsys):
        """unittest for Editor.replace_and_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace_and_prev()
        assert capsys.readouterr().out == "called SearchHelper.replace_next with args {'reverse': True}\n"

    def test_add_or_remove_dtd(self, monkeypatch, capsys):
        """unittest for Editor.add_or_remove_dtd
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
        class MockDialog:
            def __init__(self, *args):
                print('called DtdDialog.__init__ with args', args)
        def mock_call(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_call_2(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, 'dialog_data '
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.has_dtd = True
        testobj.gui.top = 'gui.top'
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
        # monkeypatch.setattr(testobj.gui, 'get_dtd', mock_get_dtd)
        monkeypatch.setattr(testee, 'DtdDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj.add_or_remove_dtd()
        assert not testobj.has_dtd
        assert capsys.readouterr().out == (
                'called EditorGui.get_element_children with arg `gui.top`\n'
                'called EditorGui.do_delete_item with arg `first child`\n'
                'called EditorGui.adjust_dtd_menu\n'
                'called.Editor.mark_dirty with value `True`\n'
                'called Editor.refresh_preview\n'
                'called EditorGui.get_element_children with arg `gui.top`\n'
                'called EditorGui.ensure_item_visible with arg `first child`\n')
        testobj.has_dtd = False
        testobj.add_or_remove_dtd()
        assert not testobj.has_dtd
        assert capsys.readouterr().out == (
                f"called DtdDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.add_or_remove_dtd()
        assert testobj.has_dtd
        assert capsys.readouterr().out == (
                f"called DtdDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called EditorGui.addtreeitem with args"
                " ('gui.top', 'DOCTYPE dialog_data ', 'dialog_data', 0)\n"
                "called EditorGui.adjust_dtd_menu\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.get_element_children with arg `gui.top`\n"
                "called EditorGui.ensure_item_visible with arg `first child`\n")

    def test_add_css(self, monkeypatch, capsys):
        """unittest for Editor.add_css
        """
        class MockDialog:
            def __init__(self, *args):
                print('called CssDialog.__init__ with args', args)
        def mock_call(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_call_2(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, {'href': 'some_stylesheet'}
        def mock_call_3(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
        monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
        # monkeypatch.setattr(testobj.gui, 'get_css_data', mock_get_css_no)
        monkeypatch.setattr(testee, 'CssDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj.gui.top = 'gui.top'
        testobj.add_css()
        assert capsys.readouterr().out == (
                f"called CssDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n")
        # monkeypatch.setattr(testobj.gui, 'get_css_data', mock_get_css_external)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children_nohtml)
        testobj.add_css()
        assert capsys.readouterr().out == (
                f"called CssDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called EditorGui.get_element_children with arg `gui.top`\n"
                "called EditorGui.get_element_text with arg `x`\n"
                "called EditorGui.meld with arg"
                " `Error: no <html> and/or no <head> element`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children_nohead)
        testobj.add_css()
        assert capsys.readouterr().out == (
                f"called CssDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
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
                f"called CssDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called EditorGui.get_element_children with arg `gui.top`\n"
                f"called EditorGui.get_element_text with arg `{testee.ELSTART} html`\n"
                f"called EditorGui.get_element_children with arg `{testee.ELSTART} html`\n"
                f"called EditorGui.get_element_text with arg `{testee.ELSTART} head`\n"
                f"called EditorGui.addtreeitem with args ('{testee.ELSTART} head',"
                f" '{testee.ELSTART} link', {{'href': 'some_stylesheet'}}, -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n")
        # monkeypatch.setattr(testobj.gui, 'get_css_data', mock_get_css_internal)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
        counter = 0
        testobj.add_css()
        assert capsys.readouterr().out == (
                f"called CssDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called EditorGui.get_element_children with arg `gui.top`\n"
                f"called EditorGui.get_element_text with arg `{testee.ELSTART} html`\n"
                f"called EditorGui.get_element_children with arg `{testee.ELSTART} html`\n"
                f"called EditorGui.get_element_text with arg `{testee.ELSTART} head`\n"
                f"called EditorGui.addtreeitem with args ('{testee.ELSTART} head',"
                f" '{testee.ELSTART} style', {{'other': 'xxx'}}, -1)\n"
                "called EditorGui.addtreeitem with args ('node', 'yyy', 'yyy', -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n")

    def test_check_if_adding_ok(self, monkeypatch, capsys):
        """unittest for Editor.check_if_adding_ok
        """
        monkeypatch.setattr(MockEditorGui, 'get_element_text', lambda *x: 'text')
        monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.check_if_adding_ok()
        monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
        testobj.item = 'x'
        assert not testobj.check_if_adding_ok()
        monkeypatch.setattr(MockEditorGui, 'get_element_text', lambda *x: f'{testee.ELSTART} text')
        testobj.item = 'x'
        assert testobj.check_if_adding_ok()

    def test_convert_link(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.convert_link
        """
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_add_link(self, monkeypatch, capsys):
        """unittest for Editor.add_link
        """
        class MockDialog:
            def __init__(self, *args):
                print('called LinkDialog.__init__ with args', args)
        def mock_call(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_call_2(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ('txt', 'data')
        # def mock_get_link_data_2():
        #     """stub
        #     """
        #     print('called EditorGui.get_link_data')
        #     return False, ('', '')
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
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.gui.get_link_data = mock_get_link_data
        monkeypatch.setattr(testee, 'LinkDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj.add_link()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
        testobj.add_link()
        assert capsys.readouterr().out == (
                f"called LinkDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.item = 'item'
        testobj.add_link()
        assert capsys.readouterr().out == (
                f"called LinkDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called getelname with args ('a', 'data')\n"
                "called EditorGui.addtreeitem with args ('item', None, 'data', -1)\n"
                "called getshortname with args ('txt',)\n"
                "called EditorGui.addtreeitem with args ('node', None, 'txt', -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n")

    def test_add_image(self, monkeypatch, capsys):
        """unittest for Editor.add_image
        """
        class MockDialog:
            def __init__(self, *args):
                print('called ImageDialog.__init__ with args', args)
        def mock_call(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_call_2(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ('txt', 'data')
        def mock_getelname(*args):
            """stub
            """
            print('called getelname with args', args)
        monkeypatch.setattr(testee, 'getelname', mock_getelname)
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee, 'ImageDialog', MockDialog)
        # testobj.gui.get_image_data = mock_get_image_data
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj.add_image()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
        testobj.add_image()
        assert capsys.readouterr().out == (
                f"called ImageDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n")
        # testobj.gui.get_image_data = mock_get_image_data_1
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.item = 'item'
        testobj.add_image()
        assert capsys.readouterr().out == (
                f"called ImageDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called getelname with args ('img', ('txt', 'data'))\n"
                "called EditorGui.addtreeitem with args ('item', None, ('txt', 'data'), -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n")

    def test_add_video(self, monkeypatch, capsys):
        """unittest for Editor.add_video
        """
        class MockDialog:
            def __init__(self, *args):
                print('called VideoDialog.__init__ with args', args)
        def mock_call(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_call_2(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ({'src': 'y.mp4'})
        def mock_getelname(*args):
            """stub
            """
            print('called getelname with args', args)
        monkeypatch.setattr(testee, 'getelname', mock_getelname)
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee, 'VideoDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
        testobj.add_video()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
        testobj.add_video()
        assert capsys.readouterr().out == (
                f"called VideoDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.item = 'item'
        testobj.add_video()
        assert capsys.readouterr().out == (
                f"called VideoDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called getelname with args ('video', {'controls': ''})\n"
                "called EditorGui.addtreeitem with args ('item', None, {'controls': ''}, -1)\n"
                "called getelname with args ('source', {'src': 'y.mp4', 'type': 'video/mp4'})\n"
                "called EditorGui.addtreeitem with args ('node', None, {'src': 'y.mp4',"
                " 'type': 'video/mp4'}, -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n")

    def test_add_audio(self, monkeypatch, capsys):
        """unittest for Editor.add_audio
        """
        class MockDialog:
            def __init__(self, *args):
                print('called AudioDialog.__init__ with args', args)
        def mock_call(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_call_2(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ({'x': 'y'})
        def mock_getelname(*args):
            """stub
            """
            print('called getelname with args', args)
        monkeypatch.setattr(testee, 'getelname', mock_getelname)
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee, 'AudioDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
        testobj.add_audio()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
        testobj.add_audio()
        assert capsys.readouterr().out == (
            f"called AudioDialog.__init__ with args ({testobj},)\n"
            "called gui.call_dialog with args MockDialog ()\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.item = 'item'
        testobj.add_audio()
        assert capsys.readouterr().out == (
            f"called AudioDialog.__init__ with args ({testobj},)\n"
            "called gui.call_dialog with args MockDialog ()\n"
            "called getelname with args ('audio', {'x': 'y', 'controls': ''})\n"
            "called EditorGui.addtreeitem with args"
            " ('item', None, {'x': 'y', 'controls': ''}, -1)\n"
            "called.Editor.mark_dirty with value `True`\n"
            "called Editor.refresh_preview\n")

    def test_add_list(self, monkeypatch, capsys):
        """unittest for Editor.add_list
        """
        class MockDialog:
            def __init__(self, *args):
                print('called ListDialog.__init__ with args', args)
        def mock_call(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_call_2(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ('', '')
        def mock_call_3(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ('x', [('itemtext', '')])
        def mock_call_4(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ('dl', [('name', 'text')])
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
        monkeypatch.setattr(testee, 'getelname', mock_getelname)
        monkeypatch.setattr(testee, 'getshortname', mock_getshortname)
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
        monkeypatch.setattr(testee, 'ListDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj.add_list()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
        testobj.add_list()
        assert capsys.readouterr().out == (
                f"called ListDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.item = 'testobjitem'
        testobj.add_list()
        assert capsys.readouterr().out == (
                f"called ListDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called getelname with args ('',)\n"
                "called EditorGui.addtreeitem with args ('testobjitem', 'elname', None, -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        testobj.item = 'testobjitem'
        testobj.add_list()
        assert capsys.readouterr().out == (
                f"called ListDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called getelname with args ('x',)\n"
                "called EditorGui.addtreeitem with args ('testobjitem', 'x', None, -1)\n"
                "called getelname with args ('li',)\n"
                "called EditorGui.addtreeitem with args ('node', 'li', None, -1)\n"
                "called getshortname with args ('itemtext',)\n"
                "called EditorGui.addtreeitem with args ('node', 'itemtext', 'itemtext', -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_4)
        testobj.item = 'testobjitem'
        testobj.add_list()
        assert capsys.readouterr().out == (
                f"called ListDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
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

    def test_add_table(self, monkeypatch, capsys):
        """unittest for Editor.add_table
        """
        class MockDialog:
            def __init__(self, *args):
                print('called TableDialog.__init__ with args', args)
        def mock_call(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_call_2(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ('empty table', False, '', [])
        def mock_call_3(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ('table with headers but no items', True, ['x', 'y'], [])
        def mock_call_4(*args):
            print('called gui.call_dialog with args', type(args[0]).__name__, args[1:])
            return True, ('table with items and empty headers', True, ['', ''], [('x', 'y')])
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
        monkeypatch.setattr(testee, 'getelname', mock_getelname)
        monkeypatch.setattr(testee, 'getshortname', mock_getshortname)
        monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
        monkeypatch.setattr(testee.Editor, 'refresh_preview', mock_refresh)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: False)
        monkeypatch.setattr(testee, 'TableDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj.add_table()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testee.Editor, 'check_if_adding_ok', lambda *x: True)
        testobj.add_table()
        assert capsys.readouterr().out == (
                f"called TableDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.item = 'testobjitem'
        testobj.add_table()
        assert capsys.readouterr().out == (
                f"called TableDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called getelname with args ('table', {'summary': 'empty table'})\n"
                "called EditorGui.addtreeitem with args"
                " ('testobjitem', 'table', {'summary': 'empty table'}, -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        testobj.item = 'testobjitem'
        testobj.add_table()
        assert capsys.readouterr().out == (
                f"called TableDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
                "called getelname with args"
                " ('table', {'summary': 'table with headers but no items'})\n"
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
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_4)
        testobj.item = 'testobjitem'
        testobj.add_table()
        assert capsys.readouterr().out == (
                f"called TableDialog.__init__ with args ({testobj},)\n"
                "called gui.call_dialog with args MockDialog ()\n"
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

    def test_validate(self, monkeypatch, capsys):
        """unittest for Editor.validate
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called ScrolledtextDialog.__init__ with args', args, kwargs)
        def mock_show(*args):
            print('called gui.show_dialog with args', type(args[0]).__name__, args[1:])
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
        monkeypatch.setattr(testee, 'ScrolledTextDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree_dirty = False
        testobj.xmlfn = 'test.html'
        testobj.validate()
        assert capsys.readouterr().out == (
                f"called ScrolledtextDialog.__init__ with args ({testobj},"
                " 'Validation output') {'htmlfile': 'test.html', 'fromdisk': True}\n"
                "called gui.show_dialog with args MockDialog ()\n")
        testobj.tree_dirty = True
        testobj.validate()
        assert capsys.readouterr().out == (
                "called tempfile.mkdtemp\n"
                "called Editor.data2soup\n"
                "called Editor.soup.prettify\n"
                "called path.write_text with args"
                " (PosixPath('tempdir/ashe_check.html'), 'prettified soup')\n"
                f"called ScrolledtextDialog.__init__ with args ({testobj},"
                " 'Validation output') {'htmlfile': 'tempdir/ashe_check.html', 'fromdisk': False}\n"
                "called gui.show_dialog with args MockDialog ()\n")
        testobj.tree_dirty = False
        testobj.xmlfn = ''
        testobj.validate()
        assert capsys.readouterr().out == (
                "called tempfile.mkdtemp\n"
                "called Editor.data2soup\n"
                "called Editor.soup.prettify\n"
                "called path.write_text with args"
                " (PosixPath('tempdir/ashe_check.html'), 'prettified soup')\n"
                f"called ScrolledtextDialog.__init__ with args ({testobj},"
                " 'Validation output') {'htmlfile': 'tempdir/ashe_check.html', 'fromdisk': False}\n"
                "called gui.show_dialog with args MockDialog ()\n")

    def test_do_validate(self, monkeypatch, capsys):
        """unittest for Editor.do_validate
        """
        def mock_run(*args, **kwargs):
            """stub
            """
            print("call subprocess.run with args", args, kwargs)
            pathlib.Path('/tmp/ashe_check').write_text('ashe_check')
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_validate('test.html') == 'ashe_check'
        assert capsys.readouterr().out == ("call subprocess.run with args"
                                           " (['tidy', '-e', '-f', '/tmp/ashe_check', 'test.html'],)"
                                           " {'check': False}\n")

    def test_view_code(self, monkeypatch, capsys):
        """unittest for Editor.view_code
        """
        class MockDialog:
            def __init__(self, *args):
                print('called CodeViewDialog.__init__ with args', args)
        def mock_show(*args):
            print('called gui.show_dialog with args', type(args[0]).__name__, args[1:])
            return False, ''
        def mock_data2soup(self, *args, **kwargs):
            """stub
            """
            print('called Editor.data2soup with args', args, kwargs)
        def mock_prettify(*args):
            """stub
            """
            print('called BeautifulSoup.prettify')
            return 'pretty'
        def mock_show_code(*args):
            """stub
            """
            print('called EditorGui.show_code')
        monkeypatch.setattr(testee.Editor, 'data2soup', mock_data2soup)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.soup = types.SimpleNamespace(prettify=mock_prettify)
        testobj.gui.show_code = mock_show_code
        monkeypatch.setattr(testee, 'CodeViewDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj.view_code()
        assert capsys.readouterr().out == (
                'called Editor.data2soup with args () {}\n'
                'called BeautifulSoup.prettify\n'
                f"called CodeViewDialog.__init__ with args ({testobj},"
                " 'Source view', 'Let op: de tekst wordt niet ververst"
                " bij wijzigingen in het hoofdvenster', 'pretty')\n"
                "called gui.show_dialog with args MockDialog ()\n")

    def test_about(self, monkeypatch, capsys):
        """unittest for Editor.about
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.about()
        assert capsys.readouterr().out == f'called EditorGui.meld with arg `{testee.ABOUT}`\n'


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


def test_getshortname():
    """unittest for main.getshortname
    """
    assert testee.getshortname('some\nname') == 'some [+]'
    assert testee.getshortname('looooooooooooooooooooooooooooong name') == (
        'looooooooooooooooooooooooooooo...')
    assert testee.getshortname('looooooooooooooooooooooooooooong\name') == (
        'looooooooooooooooooooooooooooo... [+]')
    assert testee.getshortname('name', comment=True) == '<!> name'


def test_analyze_element():
    """unittest for shared.analyze_element
    """
    assert testee.analyze_element('', {}) == ('', False, 'Add &inline style', '', False, False)
    assert testee.analyze_element('x', {'y': 'z'}) == (
            'x', False, 'Add &inline style', '', False, False)
    assert testee.analyze_element(f'{testee.ELSTART} x', {}) == (
            'x', False, 'Add &inline style', '', False, False)
    assert testee.analyze_element(f'{testee.CMSTART} {testee.ELSTART} x', {}) == (
            'x', True, 'Add &inline style', '', False, False)
    assert testee.analyze_element(f'{testee.CMSTART} x', {}) == (
            'x', True, 'Add &inline style', '', False, False)
    assert testee.analyze_element('link', {'rel': 'stylesheet'}) == (
            'link', False, '&Edit linked stylesheet', '', False, True)
    assert testee.analyze_element('x', {'style': 'y'}) == (
            'x', False, '&Edit inline style', 'y', True, False)
    assert testee.analyze_element('style', {}) == ('style', False, '&Edit styles', '', False, False)
    assert testee.analyze_element('style', {'styledata': 'y'}) == (
            'style', False, '&Edit styles', 'y', False, False)
    # of `'y', True, False)` als ik vind dat bij een style tag has_style ook aan moet staan


class TestCssManager:
    """unittests for main.CssManager
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.CssManager object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called CssManager.__init__ with args', args)
        monkeypatch.setattr(testee.CssManager, '__init__', mock_init)
        testobj = testee.CssManager()
        assert capsys.readouterr().out == 'called CssManager.__init__ with args ()\n'
        testobj.parent = types.SimpleNamespace(gui=types.SimpleNamespace(app='EditorGui.app'))
        return testobj

    def test_init(self, monkeypatch):
        """unittest for CssManager.__init__
        """
        monkeypatch.setattr(testee, 'toolkit', 'qt')
        monkeypatch.setattr(testee, 'CSSEDIT_AVAIL', False)
        testobj = testee.CssManager('parent')
        assert testobj.parent == 'parent'
        assert not testobj.cssedit_available
        monkeypatch.setattr(testee, 'CSSEDIT_AVAIL', True)
        testobj = testee.CssManager('parent')
        assert testobj.parent == 'parent'
        assert testobj.cssedit_available
        monkeypatch.setattr(testee, 'toolkit', 'wx')
        testobj = testee.CssManager('parent')
        assert testobj.parent == 'parent'
        assert not testobj.cssedit_available
        monkeypatch.setattr(testee, 'CSSEDIT_AVAIL', False)
        testobj = testee.CssManager('parent')
        assert testobj.parent == 'parent'
        assert not testobj.cssedit_available

    def test_call_editor(self, monkeypatch, capsys):
        """unittest for CssManager.call_editor
        """
        class MockTextDialog:
            """stub
            """
            def __init__(self, *args, **kwargs):
                print('called TextDialog.__init__ with args', args, kwargs)
                self.gui = 'MockTextDialogGui'
            def __repr__(self):
                """stub
                """
                return 'MockTextDialog'
        def mock_call(*args):
            """stub
            """
            print('called call_dialog with args', args)
            return False, None
        def mock_call_2(*args):
            """stub
            """
            print('called call_dialog with args', args)
            return True, ['dialog_data', '']
        testobj = self.setup_testobj(monkeypatch, capsys)
        # monkeypatch.setattr(testee.CssManager, '__init__', mock_cssman_init)
        # testobj = testee.CssManager()
        # assert capsys.readouterr().out == 'called CssManager.__init__ with args ()\n'
        monkeypatch.setattr(testee.csed, 'Editor', MockCssEditor)
        testobj.cssedit_available = True
        testobjmaster = types.SimpleNamespace(styledata='style_data')
        # assert testobj.call_editor(testobjmaster, 'style') == (None, None)
        testobj.call_editor(testobjmaster, 'style')
        # assert testobj.styledata == 'style_data'
        # assert testobj.tag == 'style'
        assert capsys.readouterr().out == (
                "called CssEditor.__init__ with args"
                " (namespace(styledata='style_data', old_styledata='style_data'),)"
                " {'app': 'EditorGui.app'}\n"
                "called CssEditor.open with args () {'text': 'style_data'}\n"
                "called CssEditor.show_from_external\n")
        testobjmaster = types.SimpleNamespace(styledata='style_data')
        # assert testobj.call_editor(testobjmaster, 'other') == (None, None)
        testobj.call_editor(testobjmaster, 'other')
        # assert testobj.styledata == 'style_data'
        # assert testobj.tag == 'other'
        assert capsys.readouterr().out == (
                "called CssEditor.__init__ with args"
                " (namespace(styledata='style_data', old_styledata='style_data'),)"
                " {'app': 'EditorGui.app'}\n"
                "called CssEditor.open with args () {'tag': 'other', 'text': 'style_data'}\n"
                "called CssEditor.show_from_external\n")
        testobj.cssedit_available = False
        monkeypatch.setattr(testee, 'TextDialog', MockTextDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        # assert testobj.call_editor(testobjmaster, 'style') == ('style_data',
        #                                                        {'styledata': 'style_data'})
        testobj.call_editor(testobjmaster, 'style')
        assert capsys.readouterr().out == (
                f"called TextDialog.__init__ with args ({testobj.parent},)"
                " {'title': 'Edit inline style', 'text': 'style_data',"
                " 'show_comment_switch': False}\n"
                # "called call_dialog with args ('MockTextDialogGui',)\n")
                "called call_dialog with args (MockTextDialog,)\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        # assert testobj.call_editor(testobjmaster, 'other') == ('dialog_data',
        #                                                        {'style': 'dialog_data'})
        testobj.call_editor(testobjmaster, 'other')
        assert capsys.readouterr().out == (
                f"called TextDialog.__init__ with args ({testobj.parent},)"
                " {'title': 'Edit inline style', 'text': 'style_data',"
                " 'show_comment_switch': False}\n"
                # "called call_dialog with args ('MockTextDialogGui',)\n")
                "called call_dialog with args (MockTextDialog,)\n")

    def test_call_editor_for_stylesheet(self, monkeypatch, capsys, tmp_path):
        """unittest for CssManager.call_editor_for_stylesheet
        """
        def mock_meld(*args):
            """stub
            """
            print('called show_message with args', args)
        # monkeypatch.setattr(testee.CssManager, '__init__', mock_cssman_init)
        # testobj = testee.CssManager()
        # assert capsys.readouterr().out == 'called CssManager.__init__ with args ()\n'
        monkeypatch.setattr(testee.gui, 'show_message', mock_meld)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cssedit_available = False
        testobj.call_editor_for_stylesheet('')
        assert capsys.readouterr().out == (
                'called show_message with args'
                f" ({testobj.parent.gui}, 'Edit CSS from HTMLEditor',"
                " 'No CSS editor support; please edit external stylesheet separately')\n")
        testobj.cssedit_available = True
        testobj.call_editor_for_stylesheet('http')
        assert capsys.readouterr().out == (
                'called show_message with args'
                f" ({testobj.parent.gui}, 'Edit CSS from HTMLEditor',"
                " 'Editing of possibly off-site stylesheets (http-links) is disabled')\n")
        # monkeypatch.setattr(testee.os.path, 'exists', lambda *x: False)
        csspath = tmp_path / 'test.css'
        assert not csspath.exists()
        cssfile = str(csspath)
        assert cssfile.startswith('/')
        testobj.call_editor_for_stylesheet(cssfile)
        assert capsys.readouterr().out == (
                'called show_message with args'
                f" ({testobj.parent.gui}, 'Edit CSS from HTMLEditor',"
                " 'Cannot determine file system location of stylesheet file')\n")
        curdir = testee.os.getcwd()
        testee.os.chdir(str(tmp_path))
        assert not csspath.exists()
        testobj.call_editor_for_stylesheet('test.css')
        assert capsys.readouterr().out == (
                'called show_message with args'
                f" ({testobj.parent.gui}, 'Edit CSS from HTMLEditor',"
                " 'Stylesheet does not exist')\n")
        assert not csspath.exists()
        monkeypatch.setattr(testee.csed, 'Editor', MockCssEditor)
        testobj.call_editor_for_stylesheet('')
        assert capsys.readouterr().out == (
                'called show_message with args'
                f" ({testobj.parent.gui}, 'Edit CSS from HTMLEditor',"
                " 'Please provide filename for existing stylesheet')\n")
        testobj.call_editor_for_stylesheet('', new_ok=True)
        assert capsys.readouterr().out == (
            "called CssEditor.__init__ with args () {'app': 'EditorGui.app'}\n"
            "called CssEditor.open with args () {'filename': ''}\n"
            "called CssEditor.show_from_external\n")
        assert not csspath.exists()
        testobj.call_editor_for_stylesheet('test.css', new_ok=True)
        assert capsys.readouterr().out == (
            "called CssEditor.__init__ with args () {'app': 'EditorGui.app'}\n"
            f"called CssEditor.open with args () {{'filename': '{cssfile}'}}\n"
            "called CssEditor.show_from_external\n")
        assert csspath.exists()
        testobj.call_editor_for_stylesheet('test.css')
        assert capsys.readouterr().out == (
            "called CssEditor.__init__ with args () {'app': 'EditorGui.app'}\n"
            f"called CssEditor.open with args () {{'filename': '{cssfile}'}}\n"
            "called CssEditor.show_from_external\n")
        testee.os.chdir(curdir)

    def test_call_from_inline(self, monkeypatch, capsys):
        """unittest for CssManager.call_from_inline
        """
        def mock_call(*args):
            """stub
            """
            print('called CssManager.call_editor with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.call_editor = mock_call
        testobj.call_from_inline(types.SimpleNamespace(), 'styledata')
        assert capsys.readouterr().out == ("called CssManager.call_editor with args"
                                           " (namespace(styledata='styledata'), 'style')\n")


class TestEditorHelper:
    """unittests for main.EditorHelper
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.EditorHelper object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called EditorHelper.__init__ with args', args)
        monkeypatch.setattr(testee.EditorHelper, '__init__', mock_init)
        testobj = testee.EditorHelper()
        testobj.editor = MockEditor()
        testobj.gui = testobj.editor.gui
        assert capsys.readouterr().out == ("called EditorHelper.__init__ with args ()\n"
                                           "called EditorGui.__init__\n"
                                           "called Editor.__init__()\n")
        return testobj

    def test_init(self):
        """unittest for EditorHelper.__init__
        """
        editor = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.EditorHelper(editor)
        assert testobj.editor == editor
        assert testobj.gui == editor.gui

    def test_edit(self, monkeypatch, capsys):
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
        # testobj = testee.EditorHelper(MockEditor())
        # assert capsys.readouterr().out == 'called EditorGui.__init__\ncalled Editor.__init__()\n'
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_show_dtd_info(self, monkeypatch, capsys):
        """unittest for EditorHelper.show_dtd_info
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_process_element_dialog(self, monkeypatch, capsys):
        """unittest for EditorHelper.process_element_dialog
        """
        class MockDialog:
            """stub
            """
            def __init__(self, *args, **kwargs):
                print('called ElementDialog.__init__ with args', args, kwargs)
                self.gui = 'MockElementDialogGui'
            def __repr__(self):
                """stub
                """
                return 'MockElementDialog'
        def mock_call(*args):
            """stub
            """
            print('called call_dialog with args', args)
            return False, None
        def mock_call_2(*args):  # commented
            print('called call_dialog with args', args)
            return True, ('p', {'x': 'z'}, True)
        def mock_call_2a(*args):  # not commented
            print('called call_dialog with args', args)
            return True, ('p', {'x': 'y'}, False)
        def mock_call_3(*args):  # attrs
            print('called call_dialog with args', args)
            return True, ('p', {'x': 'z', 'style': ''}, False)
        def mock_call_3a(*args):  # attrs
            print('called call_dialog with args', args)
            return True, ('p', {'x': 'z', 'style': 'aaaa'}, False)
        # def mock_call_4(*args):  # style_attr
        #     print('called call_dialog with args', args)
        #     return True, ('p', {'style': 'aaaa'}, False)
        # def mock_call_4a(*args):  # style_attr
        #     print('called call_dialog with args', args)
        #     return True, ('p', {'style': ''}, False)
        def mock_call_5(*args):  # style_ele
            print('called call_dialog with args', args)
            return True, ('style', {'x': 'z', 'styledata': 'yyy'}, False)
        def mock_call_6(*args):  # b_not_p
            print('called call_dialog with args', args)
            return True, ('b', {'x': 'z'}, False)
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
        def mock_get_data_2(item):
            """stub
            """
            print(f'called EditorGui.get_element_data with arg `{item}`')
            if item.endswith('p'):
                return {'x': 'y'}
            return 'yyy'
        def mock_get_data_3(item):
            """stub
            """
            print(f'called EditorGui.get_element_data with arg `{item}`')
            if item.endswith('p'):
                return {'x': 'y'}
            return 'yyy'
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
            print(f'called EditorGui.get_element_children with arg `{arg}`')
            return []
        def mock_comment(*args):
            """stub
            """
            print('called EditorHelper.comment_out with args', args)
        monkeypatch.setattr(testee, 'get_tag_from_elname', mock_get_tag)
        monkeypatch.setattr(testee, 'ElementDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'comment_out', mock_comment)
        monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
        monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
        monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_no_children)
        testobj.item = f'{testee.ELSTART} p'
        # canceling the edit dialog
        assert not testobj.process_element_dialog(f'{testee.ELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y', 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n")
        # scenario's:
        # wijzig attributen van een element
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)  # geeft element p terug
        assert testobj.process_element_dialog(f'{testee.ELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y', 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.CMELSTART} p`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n"
            f"called EditorHelper.comment_out with args ('{testee.ELSTART} p', True)\n")
        # voeg inline style toe aan een element
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)  # geeft element p terug
        assert testobj.process_element_dialog(f'{testee.ELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y', 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} p`\n"
            "called EditorGui.set_element_data with args"
            f" `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
        # wijzig inline style van een element
        monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data_2)
        # style xxx naar geen style
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2a)   # geeft element p terug
        assert testobj.process_element_dialog(f'{testee.ELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y', 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            # f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            # f" `{testee.ELSTART} p`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`,"
            " `{'x': 'y'}`\n")
        # style xxx naar style ''
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)  # geeft element p terug
        assert testobj.process_element_dialog(f'{testee.ELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y', 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} p`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`,"
            " `{'x': 'z'}`\n")
        # style xxx naar style 'aaaa'
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3a)  # geeft element p terug
        assert testobj.process_element_dialog(f'{testee.ELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y', 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} p`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`,"
            " `{'x': 'z', 'style': 'aaaa'}`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
        # wijzig naam van een element
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_6)
        assert testobj.process_element_dialog(f'{testee.ELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y', 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} b`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
        # wijzig element x in style element (en voeg style text toe)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_5)
        assert testobj.process_element_dialog(f'{testee.ELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y', 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.addtreeitem with args ('{testee.ELSTART} p', 'yyy', {{}}, -1)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} style`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
        # style element zonder children (geen style data)
        assert testobj.process_element_dialog(f'{testee.ELSTART} style')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} style`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
            # "called EditorGui.get_element_data with arg `text`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            "called ElementDialog.__init__ with args"
            f" ({testobj},) {{'title': 'Edit an element', 'tag': '<> style',"
            " 'attrs': {'x': 'y', 'styledata': ''}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            "called EditorGui.addtreeitem with args ('<> p', 'yyy', {}, -1)\n"
            # "called EditorGui.set_element_text with args `text`, `yyy`\n"
            # "called EditorGui.set_element_data with args `text`, `yyy`\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} style`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
        assert testobj.process_element_dialog(f'{testee.ELSTART} style')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} style`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_data with arg `text`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            "called ElementDialog.__init__ with args"
            f" ({testobj},) {{'title': 'Edit an element', 'tag': '<> style',"
            " 'attrs': {'x': 'y', 'styledata': 'styletext'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            "called EditorGui.set_element_text with args `text`, `yyy`\n"
            "called EditorGui.set_element_data with args `text`, `yyy`\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} style`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
        # wijzig style element in element x
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        assert testobj.process_element_dialog(f'{testee.ELSTART} style')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} style`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_data with arg `text`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit an element', 'tag': '<> style', 'attrs': {'x': 'y',"
            " 'styledata': 'styletext'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} p`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")
        # wijzig style text van een style element
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_5)
        assert testobj.process_element_dialog(f'{testee.ELSTART} style')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} style`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_data with arg `text`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit an element', 'tag': '<> style', 'attrs': {'x': 'y',"
            " 'styledata': 'styletext'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            "called EditorGui.set_element_text with args `text`, `yyy`\n"
            "called EditorGui.set_element_data with args `text`, `yyy`\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} style`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`,"
            " `{'x': 'z'}`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data_3)
        assert testobj.process_element_dialog(f'{testee.ELSTART} style')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.ELSTART} style`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_data with arg `text`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit an element', 'tag': '<> style', 'attrs': {'x': 'y',"
            " 'styledata': 'yyy'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} style`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`,"
            " `{'x': 'z'}`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
        # -- uitgecommentaard element
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        assert testobj.process_element_dialog(f'{testee.CMELSTART} p')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.CMELSTART} p`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            # " {'title': 'Edit an element', 'tag': '<!> <> p', 'attrs': {'x': 'y',"
            # " 'styledata': ''}}\n"
            " {'title': 'Edit an element', 'tag': '<!> <> p', 'attrs': {'x': 'y'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.ELSTART} p`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n"
            f"called EditorHelper.comment_out with args ('{testee.ELSTART} p', False)\n")
        # -- element onder een uitgecommentaard element - blijft uitgecommentaard
        monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_2)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        assert testobj.process_element_dialog(f'{testee.CMELSTART} style')
        assert capsys.readouterr().out == (
            f"called get_tag_from_elname with arg `{testee.CMELSTART} style`\n"
            f"called EditorGui.get_element_data with arg `{testee.ELSTART} p`\n"
            f"called EditorGui.get_element_children with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_data with arg `text`\n"
            f"called EditorGui.get_element_parent with arg `{testee.ELSTART} p`\n"
            "called EditorGui.get_element_text with arg `item parent 2`\n"
            f"called ElementDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit an element', 'tag': '<!> <> style', 'attrs': {'x': 'y',"
            " 'styledata': 'styletext'}}\n"
            "called call_dialog with args (MockElementDialog,)\n"
            f"called EditorGui.set_element_text with args `{testee.ELSTART} p`,"
            f" `{testee.CMELSTART} p`\n"
            f"called EditorGui.set_element_data with args `{testee.ELSTART} p`, `{{'x': 'z'}}`\n")

    def test_process_text_dialog(self, monkeypatch, capsys):
        """unittest for EditorHelper.process_text_dialog
        """
        class MockDialog:
            """stub
            """
            def __init__(self, *args, **kwargs):
                print('called TextDialog.__init__ with args', args, kwargs)
                self.gui = 'MockTextDialogGui'
            def __repr__(self):
                """stub
                """
                return 'MockTextDialog'
        def mock_call(*args):
            """stub
            """
            print('called call_dialog with args', args)
            return False, None
        def mock_call_2(*args):
            """stub
            """
            print('called call_dialog with args', args)
            return True, ('edited text', False)
        def mock_call_3(*args):
            """stub
            """
            print('called call_dialog with args', args)
            return True, ('edited text', True)
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj.gui, 'meld', mock_meld)
        monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
        monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
        monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
        monkeypatch.setattr(testee, 'TextDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj.item = 'testitem'
        assert not testobj.process_text_dialog('xx')
        assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `testitem`\n"
            "called EditorGui.get_element_parent with arg `testitem`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called TextDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit Text', 'text': 'itemtext'}\n"
            "called call_dialog with args (MockTextDialog,)\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        assert testobj.process_text_dialog('xx')
        assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `testitem`\n"
            "called EditorGui.get_element_parent with arg `testitem`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called TextDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit Text', 'text': 'itemtext'}\n"
            "called call_dialog with args (MockTextDialog,)\n"
            "called EditorGui.set_element_text with args `testitem`, `edited text`\n"
            "called EditorGui.set_element_data with args `testitem`, `edited text`\n")
        assert testobj.process_text_dialog(f"{testee.CMSTART} xx")
        assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `testitem`\n"
            "called EditorGui.get_element_parent with arg `testitem`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called TextDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit Text', 'text': '<!> itemtext'}\n"
            "called call_dialog with args (MockTextDialog,)\n"
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
            f"called TextDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit Text', 'text': 'itemtext'}\n"
            "called call_dialog with args (MockTextDialog,)\n"
            "called EditorGui.set_element_text with args `testitem`,"
            f" `{testee.CMSTART} edited text`\n"
            "called EditorGui.set_element_data with args `testitem`, `edited text`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        assert testobj.process_text_dialog('xx')
        assert capsys.readouterr().out == (
            "called EditorGui.get_element_data with arg `testitem`\n"
            "called EditorGui.get_element_parent with arg `testitem`\n"
            "called EditorGui.get_element_text with arg `item parent`\n"
            f"called TextDialog.__init__ with args ({testobj},)"
            " {'title': 'Edit Text', 'text': 'itemtext'}\n"
            "called call_dialog with args (MockTextDialog,)\n"
            "called EditorGui.set_element_text with args `testitem`,"
            f" `{testee.CMSTART} edited text`\n"
            "called EditorGui.set_element_data with args `testitem`, `edited text`\n")

    def test_comment(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.refresh_preview = mock_refresh
        testobj.editor.item = 'element'
        testobj.comment()
        assert testobj.item == testobj.editor.item
        assert capsys.readouterr().out == (
                f"called EditorGui.set_element_text with args `element`, `{testee.CMELSTART}"
                " itemtext`\n"
                "called EditorGui.set_element_data with args `element`, `{'x': 'y'}`\n"
                "called EditorGui.get_element_children with arg `element`\n"
                "called Editor.refresh_preview\n")
        testobj.editor.item = 'commented'
        testobj.comment()
        assert testobj.item == testobj.editor.item
        assert capsys.readouterr().out == (
                f"called EditorGui.set_element_text with args `commented`, `{testee.CMELSTART}"
                " itemtext`\n"
                "called EditorGui.set_element_data with args `commented`, `{'x': 'y'}`\n"
                "called EditorGui.get_element_children with arg `commented`\n"
                "called Editor.refresh_preview\n")
        testobj.editor.item = 'other'
        testobj.comment()
        assert testobj.item == testobj.editor.item
        assert capsys.readouterr().out == (
                f"called EditorGui.set_element_text with args `other`, `{testee.CMSTART} plaintext`\n"
                "called EditorGui.set_element_data with args `other`, `plaintext`\n"
                "called Editor.refresh_preview\n")

    def test_comment_out(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_copy(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_push_el(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_paste(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_zetzeronder(self, monkeypatch, capsys):
        """unittest for EditorHelper.zetzeronder
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.zetzeronder('node', ('item', {'x': 'y'}, [('subel', {}, [])]), 1)
        assert capsys.readouterr().out == (
                "called EditorGui.addtreeitem with args ('node', 'item', {'x': 'y'}, 1)\n"
                "called EditorGui.addtreeitem with args ('node', 'subel', {}, -1)\n")

    def test_insert(self, monkeypatch, capsys):
        """unittest for EditorHelper.insert
        """
        class MockDialog:
            """stub
            """
            def __init__(self, *args, **kwargs):
                print('called ElementDialog.__init__ with args', args, kwargs)
                self.gui = 'MockElementDialogGui'
            def __repr__(self):
                """stub
                """
                return 'MockElementDialog'
        def mock_call(*args):
            print('called call_dialog with args', args)
            return False, None
        def mock_call_2(*args):
            print('called call_dialog with args', args)
            return True, ('new', {'x': 'y'}, False)
        def mock_call_3(*args):
            print('called call_dialog with args', args)
            return True, ('style', {'x': 'y', 'styledata': 'xxx'}, False)
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
        # def mock_get_parent_2(item):
        #     """stub
        #     """
        #     print(f'called EditorGui.get_element_parent with arg `{item}`')
        #     return 'parent'
        def mock_get_children(node):
            print(f'called EditorGui.get_element_children with arg `{node}`')
            return 'node1', 'node2'
        def mock_get_parentpos(*args):
            print('called EditorGui.get_element_parentpos with args', args)
            return 'pp', 1
        def mock_refresh():
            """stub
            """
            print('called Editor.refresh_preview')
        def mock_mark_dirty(value):
            """stub
            """
            print(f'called.Editor.mark_dirty with value `{value}`')
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
        monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
        monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
        monkeypatch.setattr(testee, 'ElementDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
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
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert under)'}\n"
                "called call_dialog with args (MockElementDialog,)\n")
        # deze stond in de oude versie als laatste
        # monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_2)
        # # monkeypatch.setattr(testobj.gui, 'do_add_element', mock_do_add_commented)
        # testobj.insert()
        # assert capsys.readouterr().out == (
        #         "called EditorGui.do_add_element with arg `before`\n"
        #         f"called ElementDialog.__init__ with args ({testobj},)"
        #         " {'title': 'New element (insert under)'}\n"
        #         "called call_dialog with args (MockElementDialog,)\n"
        #         "called EditorGui.get_element_parent with arg `element`\n"
        #         "called EditorGui.get_element_text with arg `parent`\n"
        #         f"called EditorGui.addtreeitem with args ('', '{testee.CMELSTART} new',"
        #         " {'x': 'y'}, -1)\n"
        #         "called EditorGui.set_selected_item(`node`)\n"
        #         "called.Editor.mark_dirty with value `True`\n"
        #         "called Editor.refresh_preview\n"
        #         "called EditorGui.set_item_expanded with args `element`, `True`\n")
        # monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.editor.advance_selection_on_add = False
        testobj.insert(below=True)
        assert capsys.readouterr().out == (
                "called EditorGui.get_element_text with arg `element`\n"
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert under)'}\n"
                "called call_dialog with args (MockElementDialog,)\n"
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
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert under)'}\n"
                "called call_dialog with args (MockElementDialog,)\n"
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
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert under)'}\n"
                "called call_dialog with args (MockElementDialog,)\n"
                "called EditorGui.get_element_text with arg `element`\n"
                f"called EditorGui.addtreeitem with args ('element', '{testee.ELSTART} new',"
                " {'x': 'y'}, -1)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        testobj.insert(before=False)
        assert capsys.readouterr().out == (
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert after)'}\n"
                "called call_dialog with args (MockElementDialog,)\n"
                "called EditorGui.get_element_parent with arg `element`\n"
                "called EditorGui.get_element_text with arg `commented parent`\n"
                "called EditorGui.get_element_parentpos with args ('element',)\n"
                "called EditorGui.get_element_children with arg `pp`\n"
                f"called EditorGui.addtreeitem with args ('pp', '{testee.CMELSTART} new',"
                " {'x': 'y'}, -1)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        testobj.insert()
        assert capsys.readouterr().out == (
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert before)'}\n"
                "called call_dialog with args (MockElementDialog,)\n"
                "called EditorGui.get_element_parent with arg `element`\n"
                "called EditorGui.get_element_text with arg `commented parent`\n"
                # "called EditorGui.get_children with arg `element`\n"
                "called EditorGui.get_element_parentpos with args ('element',)\n"
                "called EditorGui.get_element_children with arg `pp`\n"
                f"called EditorGui.addtreeitem with args ('pp', '{testee.CMELSTART} new',"
                " {'x': 'y'}, -1)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        # monkeypatch.setattr(testobj.gui, 'do_add_element', mock_do_add_style)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        testobj.insert()
        assert capsys.readouterr().out == (
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert before)'}\n"
                "called call_dialog with args (MockElementDialog,)\n"
                "called EditorGui.get_element_parent with arg `element`\n"
                "called EditorGui.get_element_text with arg `commented parent`\n"
                "called EditorGui.get_element_parentpos with args ('element',)\n"
                "called EditorGui.get_element_children with arg `pp`\n"
                "called EditorGui.addtreeitem with args"
                f" ('pp', '{testee.CMELSTART} style', {{'x': 'y', 'styledata': 'xxx'}}, -1)\n"
                # moet die styledata hier niet al uit de attrdict zijn verwijderd?
                "called EditorGui.addtreeitem with args ('node', 'xxx', 'xxx', -1)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_parentpos', mock_get_parentpos)
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
        testobj.insert()
        assert capsys.readouterr().out == (
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element (insert before)'}\n"
                "called call_dialog with args (MockElementDialog,)\n"
                "called EditorGui.get_element_parent with arg `element`\n"
                "called EditorGui.get_element_text with arg `commented parent`\n"
                "called EditorGui.get_element_parentpos with args ('element',)\n"
                "called EditorGui.get_element_children with arg `pp`\n"
                "called EditorGui.addtreeitem with args"
                f" ('pp', '{testee.CMELSTART} style', {{'x': 'y', 'styledata': 'xxx'}}, 1)\n"
                "called EditorGui.addtreeitem with args ('node', 'xxx', 'xxx', -1)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")

    def test_add_text(self, monkeypatch, capsys):
        """unittest for EditorHelper.add_text
        """
        class MockDialog:
            """stub
            """
            def __init__(self, *args, **kwargs):
                print('called TextDialog.__init__ with args', args, kwargs)
                self.gui = 'MockTextDialogGui'
            def __repr__(self):
                """stub
                """
                return 'MockTextDialog'
        def mock_call(*args):
            print('called call_dialog with args', args)
            return False, None
        def mock_call_2(*args):
            print('called call_dialog with args', args)
            return True, ('newtext', False)
        def mock_call_3(*args):
            print('called call_dialog with args', args)
            return True, ('newtext', True)
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
        def mock_get_children(node):
            print(f'called EditorGui.get_element_children with arg `{node}`')
            return 'node1', 'node2'
        def mock_get_parentpos(*args):
            print('called EditorGui.get_element_parentpos with args', args)
            return 'pp', 1
        def mock_refresh():
            """stub
            """
            print('called Editor.refresh_preview')
        def mock_mark_dirty(value):
            """stub
            """
            print(f'called.Editor.mark_dirty with value `{value}`')
        monkeypatch.setattr(testee, 'getelname', mock_getelname)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj.gui, 'get_element_text', mock_get_text)
        monkeypatch.setattr(testobj.gui, 'get_element_data', mock_get_data)
        monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent)
        monkeypatch.setattr(testee, 'TextDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
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
        # monkeypatch.setattr(testobj.gui, 'do_add_textvalue', mock_do_add)
        testobj.editor.advance_selection_on_add = False
        testobj.editor.item = 'element'
        testobj.add_text(below=True)
        assert capsys.readouterr().out == (
                "called EditorGui.get_element_text with arg `element`\n"
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called call_dialog with args (MockTextDialog,)\n")
        # monkeypatch.setattr(testobj.gui, 'do_add_textvalue', mock_do_add_2)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.editor.advance_selection_on_add = False
        testobj.editor.item = 'element'
        testobj.add_text(below=True)
        assert capsys.readouterr().out == (
                "called EditorGui.get_element_text with arg `element`\n"
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called call_dialog with args (MockTextDialog,)\n"
                "called EditorGui.get_element_text with arg `element`\n"
                "called EditorGui.addtreeitem with args ('element', 'newtext', 'newtext', -1)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        testobj.editor.advance_selection_on_add = True
        testobj.add_text(below=True)
        assert capsys.readouterr().out == (
                "called EditorGui.get_element_text with arg `element`\n"
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called call_dialog with args (MockTextDialog,)\n"
                "called EditorGui.get_element_text with arg `element`\n"
                "called EditorGui.addtreeitem with args ('element', 'newtext', 'newtext', -1)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        testobj.add_text(below=True, before=False)
        assert capsys.readouterr().out == (
                "called EditorGui.get_element_text with arg `element`\n"
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called call_dialog with args (MockTextDialog,)\n"
                "called EditorGui.get_element_text with arg `element`\n"
                "called EditorGui.addtreeitem with args ('element', 'newtext', 'newtext', -1)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        testobj.add_text(before=False)
        assert capsys.readouterr().out == (
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called call_dialog with args (MockTextDialog,)\n"
                "called EditorGui.get_element_parent with arg `element`\n"
                "called EditorGui.get_element_text with arg `commented parent`\n"
                "called EditorGui.get_element_parentpos with args ('element',)\n"
                "called getelname with args ('br', {}, False)\n"
                "called EditorGui.addtreeitem with args ('pp', 'br', 'br', 1)\n"
                "called EditorGui.get_element_children with arg `pp`\n"
                "called EditorGui.addtreeitem with args ('pp', 'newtext', 'newtext', -1)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        testobj.add_text()
        assert capsys.readouterr().out == (
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called call_dialog with args (MockTextDialog,)\n"
                "called EditorGui.get_element_parent with arg `element`\n"
                "called EditorGui.get_element_text with arg `commented parent`\n"
                "called EditorGui.get_element_parentpos with args ('element',)\n"
                "called EditorGui.get_element_children with arg `pp`\n"
                "called EditorGui.addtreeitem with args ('pp', 'newtext', 'newtext', -1)\n"
                "called getelname with args ('br', {}, False)\n"
                "called EditorGui.addtreeitem with args ('pp', 'br', 'br', 0)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_parent', mock_get_parent_2)
        # monkeypatch.setattr(testobj.gui, 'do_add_element', mock_do_add_commented)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        testobj.add_text()
        assert capsys.readouterr().out == (
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called call_dialog with args (MockTextDialog,)\n"
                "called EditorGui.get_element_parent with arg `element`\n"
                "called EditorGui.get_element_text with arg `parent`\n"
                "called EditorGui.get_element_parentpos with args ('element',)\n"
                "called EditorGui.get_element_children with arg `pp`\n"
                "called EditorGui.addtreeitem with args ('pp', '<!> newtext', 'newtext', -1)\n"
                "called getelname with args ('br', {}, True)\n"
                "called EditorGui.addtreeitem with args ('pp', 'br', 'br', 0)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")
        monkeypatch.setattr(testobj.gui, 'get_element_parentpos', mock_get_parentpos)
        monkeypatch.setattr(testobj.gui, 'get_element_children', mock_get_children)
        testobj.add_text()
        assert capsys.readouterr().out == (
                f"called TextDialog.__init__ with args ({testobj},) {{'title': 'New Text'}}\n"
                "called call_dialog with args (MockTextDialog,)\n"
                "called EditorGui.get_element_parent with arg `element`\n"
                "called EditorGui.get_element_text with arg `parent`\n"
                "called EditorGui.get_element_parentpos with args ('element',)\n"
                "called EditorGui.get_element_children with arg `pp`\n"
                "called EditorGui.addtreeitem with args ('pp', '<!> newtext', 'newtext', 1)\n"
                "called getelname with args ('br', {}, True)\n"
                "called EditorGui.addtreeitem with args ('pp', 'br', 'br', 2)\n"
                "called EditorGui.set_selected_item(`node`)\n"
                "called.Editor.mark_dirty with value `True`\n"
                "called Editor.refresh_preview\n"
                "called EditorGui.set_item_expanded with args `element`, `True`\n")


class TestSearchHelper:
    """unittests for main.SearchHelper
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.SearchHelper object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called SearchHelper.__init__ with args', args)
        monkeypatch.setattr(testee.SearchHelper, '__init__', mock_init)
        testobj = testee.SearchHelper()
        testobj.editor = MockEditor()
        testobj.gui = testobj.editor.gui
        assert capsys.readouterr().out == ('called SearchHelper.__init__ with args ()\n'
                                           "called EditorGui.__init__\n"
                                           "called Editor.__init__()\n")
        return testobj

    def test_init(self):
        """unittest for SearchHelper.__init__
        """
        editor = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.SearchHelper(editor)
        assert testobj.editor == editor
        assert testobj.gui == editor.gui
        assert testobj.search_args == []
        assert testobj.replace_args == []

    def test_search_from(self, monkeypatch, capsys):
        """unittest for SearchHelper.search_from
        """
        class MockDialog:
            """stub
            """
            def __init__(self, *args, **kwargs):
                print('called SearchDialog.__init__ with args', args, kwargs)
                self.gui = 'MockSearchDialogGui'
            def __repr__(self):
                """stub
                """
                return 'MockSearchDialog'
        def mock_call(*args):
            print('called call_dialog with args', args)
            return False, ()
        def mock_call_2(*args):
            print('called call_dialog with args', args)
            return True, (('x', 'y', 'z', 'a'), 'search_specs')
        def mock_flatten(self, *args):
            """stub
            """
            return (('top', 'filenaam', {}), ('ele', f'{testee.ELSTART} html', {}))
        def mock_next(self, *args):
            """stub
            """
            print('called search.find_next() with args', args)
            return 'pos', 1
        monkeypatch.setattr(testee, 'SearchDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
        monkeypatch.setattr(testobj, 'find_next', mock_next)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj.search_from('top')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search options') {{}}\n"
                "called call_dialog with args (MockSearchDialog,)\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.search_from('top')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search options') {{}}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'), False)\n"
                'called EditorGui.set_selected_item(`1`)\n')
        testobj.search_from('top', True)
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search options') {{}}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'), True)\n"
                'called EditorGui.set_selected_item(`1`)\n')
        testobj.search_from('ele')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search options') {{}}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'), False, (1, 'ele'))\n"
                'called EditorGui.set_selected_item(`1`)\n')
        testobj.search_from('ele', True)
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search options') {{}}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'), True, (1, 'ele'))\n"
                'called EditorGui.set_selected_item(`1`)\n')
        monkeypatch.setattr(testobj, 'find_next', lambda *x: None)  # mock_next)
        testobj.search_from('ele')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search options') {{}}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                'called EditorGui.meld with arg `search_specs\n\nNo (more) results`\n')

    def test_search_next(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
        monkeypatch.setattr(testobj, 'find_next', mock_next)
        testobj.search_args = ()
        testobj.search_next()
        assert capsys.readouterr().out == ""
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

    def test_replace_from(self, monkeypatch, capsys):
        """unittest for SearchHelper.replace_from
        """
        class MockDialog:
            """stub
            """
            def __init__(self, *args, **kwargs):
                print('called SearchDialog.__init__ with args', args, kwargs)
                self.gui = 'MockSearchDialogGui'
            def __repr__(self):
                """stub
                """
                return 'MockSearchDialog'
        def mock_call(*args):
            print('called call_dialog with args', args)
            return False, ()
        def mock_call_2(*args):
            print('called call_dialog with args', args)
            return True, (('x', 'y', 'z', 'a'), 'search_specs', ('q', 'r', 's', 't', False))
        def mock_call_3(*args):
            print('called call_dialog with args', args)
            return True, (('x', 'y', 'z', 'a'), 'search_specs', ('q', 'r', 's', 't', True))
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
        def mock_replall():
            """stub
            """
            print('called search.replace_all')
        monkeypatch.setattr(testee, 'SearchDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
        monkeypatch.setattr(testobj, 'find_next', mock_next)
        monkeypatch.setattr(testobj, 'replace_and_find', mock_replace)
        monkeypatch.setattr(testobj, 'replace_all', mock_replall)
        testobj.replace_from('top')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n")
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_2)
        testobj.replace_from('top')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'), False)\n"
                "called search.replace_and_find() with args `('pos', 1)`, `False`\n")
        testobj.replace_from('top', True)
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'), True)\n"
                "called search.replace_and_find() with args `('pos', 1)`, `True`\n")
        testobj.replace_from('ele')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'), False, (1, 'ele'))\n"
                "called search.replace_and_find() with args `('pos', 1)`, `False`\n")
        testobj.replace_from('ele', True)
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'), True, (1, 'ele'))\n"
                "called search.replace_and_find() with args `('pos', 1)`, `True`\n")
        monkeypatch.setattr(testobj, 'find_next', lambda *x: None)  # mock_next)
        testobj.replace_from('ele')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                'called EditorGui.meld with arg `search_specs\n\nNo (more) results`\n')
        testobj.replace_from('top')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                'called EditorGui.meld with arg `search_specs\n\nNo (more) results`\n')
        monkeypatch.setattr(testee.gui, 'call_dialog', mock_call_3)
        testobj.replace_from('top')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.replace_all\n")
        testobj.replace_from('top', True)
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.replace_all\n")
        testobj.replace_from('ele')
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.replace_all\n")
        testobj.replace_from('ele', True)
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj}, 'Search/Replace options')"
                " {'replace': True}\n"
                "called call_dialog with args (MockSearchDialog,)\n"
                "called search.replace_all\n")

    def test_replace_all(self, monkeypatch, capsys):
        """unittest for SearchHelper.replace_all
        """
        def mock_next(self, *args):
            """stub
            """
            print('called search.find_next() with args', args)
            return ()
        def mock_next_2(self, *args):
            """stub
            """
            print('called search.find_next() with args', args)
            return 'pos', 1
        def mock_replace(*args, **kwargs):
            """stub
            """
            print('called search.replace_and_find() with args', args, kwargs)
            return ()
        def mock_replace_2(*args, **kwargs):
            """stub
            """
            nonlocal counter
            print('called search.replace_and_find() with args', args, kwargs)
            counter += 1
            return () if counter == 3 else ('newpos', counter + 1)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_args = ('x', 'y', 'z', 'a')
        testobj.search_specs = 'search specs'
        monkeypatch.setattr(testobj, 'find_next', mock_next)
        monkeypatch.setattr(testobj, 'replace_and_find', mock_replace)
        counter = 0
        testobj.replace_all()
        assert capsys.readouterr().out == (
                "called EditorGui.get_element_text with arg `top`\n"
                "called EditorGui.get_element_data with arg `top`\n"
                "called EditorGui.get_element_children with arg `top`\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'),)\n"
                "called EditorGui.meld with arg `search specs\n\n"
                "Not found - no replacements done`\n")
        assert counter == 0
        monkeypatch.setattr(testobj, 'find_next', mock_next_2)
        testobj.replace_all()
        assert capsys.readouterr().out == (
                "called EditorGui.get_element_text with arg `top`\n"
                "called EditorGui.get_element_data with arg `top`\n"
                "called EditorGui.get_element_children with arg `top`\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'),)\n"
                "called search.replace_and_find() with args (('pos', 1),) {'reverse': False}\n"
                "called EditorGui.meld with arg `search specs\n\n 1 items replaced`\n")
        assert counter == 0
        monkeypatch.setattr(testobj, 'replace_and_find', mock_replace_2)
        testobj.replace_all()
        assert capsys.readouterr().out == (
                "called EditorGui.get_element_text with arg `top`\n"
                "called EditorGui.get_element_data with arg `top`\n"
                "called EditorGui.get_element_children with arg `top`\n"
                "called search.find_next() with args (('x', 'y', 'z', 'a'),)\n"
                "called search.replace_and_find() with args (('pos', 1),) {'reverse': False}\n"
                "called search.replace_and_find() with args (('newpos', 2),) {'reverse': False}\n"
                "called search.replace_and_find() with args (('newpos', 3),) {'reverse': False}\n"
                "called EditorGui.meld with arg `search specs\n\n 3 items replaced`\n")

    def test_replace_next(self, monkeypatch, capsys):
        """unittest for SearchHelper.replace_next
        """
        def mock_replace(*args):
            """stub
            """
            print(f'called search.replace_and_find() with args `{args[0]}`, `{args[1]}`')
            return True
        def mock_replace_2(*args):
            """stub
            """
            print(f'called search.replace_and_find() with args `{args[0]}`, `{args[1]}`')
            return False
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_specs = 'search specs'
        monkeypatch.setattr(testobj, 'replace_and_find', mock_replace)
        testobj.replace_args = ()
        testobj.replace_next()
        assert capsys.readouterr().out == ""
        testobj.replace_args = ('x', 'y', 'z', 'a')
        testobj.search_pos = '1'
        testobj.replace_next()
        assert capsys.readouterr().out == 'called search.replace_and_find() with args `1`, `False`\n'
        testobj.replace_next(True)
        assert capsys.readouterr().out == 'called search.replace_and_find() with args `1`, `True`\n'
        monkeypatch.setattr(testobj, 'replace_and_find', mock_replace_2)
        testobj.replace_next()
        assert capsys.readouterr().out == ('called search.replace_and_find() with args `1`, `False`\n'
                                           'called EditorGui.meld with arg `search specs\n\n'
                                           'No (more) results`\n')

    def test_replace_and_find(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'replace_element', mock_element)
        monkeypatch.setattr(testobj, 'replace_attr', mock_attr)
        monkeypatch.setattr(testobj, 'replace_text', mock_text)
        monkeypatch.setattr(testobj, 'flatten_tree', mock_flatten)
        monkeypatch.setattr(testobj, 'find_next', mock_next)
        testobj.search_args = ('x', 'y', 'z', 'a')
        testobj.replace_args = ('x', 'y', 'z', 'a')
        testobj.replace_and_find((1, 'ele'), False)
        assert testobj.search_pos == ('pos', 1)
        assert capsys.readouterr().out == (
                'called search.replace_element()\n'
                'called search.replace_attr()\n'
                'called search.replace_text()\n'
                "called search.find_next() with args (('x', 'y', 'z', 'a'), False, (1, 'ele'))\n"
                'called EditorGui.set_selected_item(`1`)\n')
        monkeypatch.setattr(testobj, 'find_next', mock_next_2)
        testobj.search_specs = 'search_specs'
        testobj.replace_and_find((1, 'ele'), True)
        assert capsys.readouterr().out == (
                'called search.replace_element()\n'
                'called search.replace_attr()\n'
                'called search.replace_text()\n'
                "called search.find_next() with args (('x', 'y', 'z', 'a'), True, (1, 'ele'))\n")
                # 'called EditorGui.meld with arg `search_specs\n\nNo (more) results`\n')
        testobj.replace_args = ('', '', '', '')
        testobj.replace_and_find((1, 'ele'), False)
        assert capsys.readouterr().out == (
                "called search.find_next() with args (('x', 'y', 'z', 'a'), False, (1, 'ele'))\n")
                # 'called EditorGui.meld with arg `search_specs\n\nNo (more) results`\n')

    def test_build_search_spec(self, monkeypatch, capsys):
        """unittest for Editor.build_search_spec
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_search_spec('', '', '', '') == ''
        assert testobj.build_search_spec('x', '', '', '') == 'search for a(n) `x` element'
        assert testobj.build_search_spec('', 'x', '', '') == 'search for a(n) `x` attribute'
        assert testobj.build_search_spec('', '', 'x', '') == 'search for an attribute with value `x`'
        assert testobj.build_search_spec('', '', '', 'x') == 'search for text'
        assert testobj.build_search_spec('x', 'y', '', '') == ('search for a(n) `x` element'
                                                               ' with a(n) `y` attribute')
        assert testobj.build_search_spec('x', '', 'y', '') == ('search for a(n) `x` element'
                                                               ' with an attribute with value `y`')
        assert testobj.build_search_spec('x', '', '', 'y') == 'search for text under a(n) `x` element'
        assert testobj.build_search_spec('', 'x', 'y', '') == ('search for a(n) `x` attribute'
                                                               ' with value `y`')
        assert testobj.build_search_spec('', 'x', '', 'y') == ('search for text under an element'
                                                               ' with a(n) `x` attribute')
        assert testobj.build_search_spec('', '', 'x', 'y') == ('search for text under an element'
                                                               ' with an attribute with value `x`')
        assert testobj.build_search_spec('x', 'y', 'z', '') == ('search for a(n) `x` element'
                                                                ' with a(n) `y` attribute'
                                                                ' with value `z`')
        assert testobj.build_search_spec('x', 'y', '', 'z') == ('search for text'
                                                                ' under a(n) `x` element'
                                                                ' with a(n) `y` attribute')
        assert testobj.build_search_spec('x', '', 'y', 'z') == ('search for text'
                                                                ' under a(n) `x` element'
                                                                ' with an attribute with value `y`')
        assert testobj.build_search_spec('', 'x', 'y', 'z') == ('search for text under an element'
                                                                ' with a(n) `x` attribute'
                                                                ' with value `y`')
        assert testobj.build_search_spec('x', 'y', 'z', 'a', ()) == ('search for text'
                                                                     ' under a(n) `x` element'
                                                                     ' with a(n) `y` attribute'
                                                                     ' with value `z`')
        assert testobj.build_search_spec('', '', '', '', ('x')) == (
                'error: element replacement without element search')
        assert testobj.build_search_spec('', '', '', '', ('', 'x')) == (
                'error: attribute replacement without attribute search')
        assert testobj.build_search_spec('', '', '', '', ('', '', 'x')) == (
                'error: attribute value replacement without attribute value search')
        assert testobj.build_search_spec('', '', '', '', ('', '', '', 'x')) == (
                'error: text replacement without text search')
        assert testobj.build_search_spec('x', '', '', '', ('y', '', '', '')) == (
                'search for a(n) `x` element\nand replace element name with `y`')
        assert testobj.build_search_spec('', 'x', '', '', ('', 'y', '', '')) == (
                'search for a(n) `x` attribute\nand replace attribute name with `y`')
        assert testobj.build_search_spec('', '', 'x', '', ('', '', 'y', '')) == (
                'search for an attribute with value `x`\nand replace attribute value with `y`')
        assert testobj.build_search_spec('', '', '', 'x', ('', '', '', 'y')) == (
                'search for text\nand replace text with `y`')
        assert testobj.build_search_spec('x', 'y', 'z', 'a', ('xx', 'yy', 'zz', 'aa')) == (
                'search for text under a(n) `x` element with a(n) `y` attribute'
                ' with value `z`\nand replace element name with `xx`, attribute name with `yy`,'
                ' attribute value with `zz`, text with `aa`')

    def test_find_next(self, monkeypatch, capsys):
        """unittest for SearchHelper.find_next
        """
        treedata = [('ele1', f'{testee.ELSTART} html', {}),
                    ('ele2', f'{testee.ELSTART} div', {}),
                    ('ele3', f'{testee.ELSTART} div', {'id': '1'}),
                    ('text', 'some text', {}),
                    ('ele4', f'{testee.ELSTART} div', {'id': '2'}),
                    ('ele5', f'{testee.ELSTART} div', {'class': 'footer'})]
        testobj = self.setup_testobj(monkeypatch, capsys)
        # not findable
        assert testobj.find_next(treedata, ('p', '', '', '')) is None
        assert testobj.find_next(treedata, ('div', 'test', '', '')) is None
        assert testobj.find_next(treedata, ('div', 'class', 'header', '')) is None
        assert testobj.find_next(treedata, ('div', '', '', 'cheese')) is None
        assert testobj.find_next(treedata, ('p', 'id', '', '')) is None
        assert testobj.find_next(treedata, ('p', '', '1', '')) is None
        assert testobj.find_next(treedata, ('p', '', '', 'some text')) is None
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

    def test_flatten_tree(self, monkeypatch, capsys):
        """unittest for SearchHelper.flatten_tree
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        data = testobj.flatten_tree('top')
        assert data == [('ele1', f'{testee.ELSTART} html', {}),
                        ('ele2', f'{testee.ELSTART} div', {}),
                        ('text', 'some text', {})]

    def test_flatten_tree_2(self, monkeypatch, capsys):
        """unittest for SearchHelper.flatten_tree
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        data = testobj.flatten_tree('top')
        assert data == [('ele1', f'{testee.CMELSTART} html', {}),
                        ('ele2', f'{testee.CMELSTART} div', {}),
                        ('text', f'{testee.CMSTART} some text', {})]

    def test_replace_element(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace_args = ('x', 'y', 'z', 'a')
        testobj.replace_element((1, 'el1'))
        assert capsys.readouterr().out == ('called EditorGui.set_element_text with args `el1`,'
                                           f' `{testee.ELSTART} x`\n')
        testobj.replace_element((2, 'el2'))
        assert capsys.readouterr().out == (
                f'called EditorGui.set_element_text with args `el2`, `{testee.ELSTART} x id="1"`\n')
        testobj.replace_element((3, 'el3'))
        assert capsys.readouterr().out == (
                f'called EditorGui.set_element_text with args `el3`, `{testee.CMELSTART} x`\n')
        testobj.replace_element((4, 'el4'))
        assert capsys.readouterr().out == ('called EditorGui.set_element_text with args `el4`,'
                                           f' `{testee.CMELSTART} x class="centered"`\n')

    def test_replace_attr(self, monkeypatch, capsys):
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_args = ('x', 'id', '1', 'a')
        testobj.replace_args = ('x', 'y', '', 'a')
        testobj.replace_attr((1, 'el1'))
        assert capsys.readouterr().out == (
                "called EditorGui.set_element_data with args `el1`, `{'y': '1'}`\n"
                f"called EditorGui.set_element_text with args `el1`, `{testee.ELSTART} html`\n")
        monkeypatch.setattr(MockEditorGui, 'get_element_text', lambda *x: f'{testee.CMELSTART} div')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_args = ('x', 'id', '1', 'a')
        testobj.replace_args = ('x', 'y', 'z', 'a')
        testobj.replace_attr((2, 'el2'))
        assert capsys.readouterr().out == (
                "called EditorGui.set_element_data with args `el2`, `{'y': 'z'}`\n"
                f"called EditorGui.set_element_text with args `el2`, `{testee.CMELSTART} div`\n")
        monkeypatch.setattr(MockEditorGui, 'get_element_text', lambda *x: f'{testee.CMELSTART} p')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_args = ('x', 'id', '1', 'a')
        testobj.replace_args = ('x', '', 'z', 'a')
        testobj.replace_attr((3, 'el3'))
        assert capsys.readouterr().out == (
                "called EditorGui.set_element_data with args `el3`, `{'id': 'z'}`\n"
                # f'called EditorGui.set_element_text with args `el3`, `{testee.ELSTART} p id="z"`\n')
                f'called EditorGui.set_element_text with args `el3`, `{testee.CMELSTART} p id="z"`\n')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_args = ('x', 'id', '1', 'a')
        testobj.replace_args = ('x', '=/= y', 'z', 'a')
        testobj.replace_attr((4, 'el4'))
        assert capsys.readouterr().out == (
                "called EditorGui.set_element_data with args `el4`, `{'id': 'z'}`\n"
                # f'called EditorGui.set_element_text with args `el4`, `{testee.ELSTART} p id="z"`\n')
                f'called EditorGui.set_element_text with args `el4`, `{testee.CMELSTART} p id="z"`\n')

    def test_replace_text(self, monkeypatch, capsys):
        """unittest for SearchHelper.replace_text
        """
        def mock_element_text(self, node):
            """stub
            """
            return 'abbreviated text'
        def mock_element_data(self, node):
            """stub
            """
            return 'full text'
        monkeypatch.setattr(MockEditorGui, 'get_element_text', mock_element_text)
        monkeypatch.setattr(MockEditorGui, 'get_element_data', mock_element_data)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_args = ('x', 'y', 'z', 'tex')
        testobj.replace_args = ('x', 'y', 'z', 'a')
        testobj.replace_text((1, 'ele'))
        assert capsys.readouterr().out == (
            "called EditorGui.set_element_text with args `ele`, `abbreviated at`\n"
            "called EditorGui.set_element_data with args `ele`, `full at`\n")


class MockEditGui:
    "testdouble voor qtgui.EditDialogGui"
    def __init__(self, *args, **kwargs):
        print('called EditDialogGui.__init__ with args', args, kwargs)
    def add_buttons_to_bottom(self, *args, **kwargs):
        print('called EditDialogGui.add_buttons_to_bottom with args', args, kwargs)
    def add_buttons_to_section(self, *args, **kwargs):
        print('called EditDialogGui.add_buttons_to_section with args', args, kwargs)
        return ['', '', 'style_button']
    def add_checkbox(self, *args, **kwargs):
        print('called EditDialogGui.add_checkbox with args', args, kwargs)
        return 'checkbox'
    def add_content_section(self, *args, **kwargs):
        print('called EditDialogGui.add_content_section with args', args, kwargs)
        return 'section'
    def add_label(self, *args, **kwargs):
        print('called EditDialogGui.add_label with args', args, kwargs)
    def add_radiobutton_to_section(self, *args):
        print('called EditDialogGui.add_radiobutton_to_section with args', args)
        return 'radiobutton'
    def add_table_row(self, *args):
        print('called EditDialogGui.add_table_row with args', args)
    def add_table_rowitem(self, *args, **kwargs):
        print('called EditDialogGui.add_table_rowitem with args', args, kwargs)
    def add_table_to_section(self, *args, **kwargs):
        print('called EditDialogGui.add_table_to_section with args', args, kwargs)
        return 'table'
    def add_textinput(self, *args, **kwargs):
        print('called EditDialogGui.add_textinput with args', args, kwargs)
        return 'textbox'
    def add_textinput_to_section(self, *args, **kwargs):
        print('called EditDialogGui.add_textinput_to_section with args', args, kwargs)
        return 'textbox'
    def add_text_to_section(self, *args):
        print('called EditDialogGui.add_text_to_section with args', args)
    def add_topline(self, *args, **kwargs):
        print('called EditDialogGui.add_topline with args', args, kwargs)
        return 'topline'
    def delete_table_row(self, *args):
        print('called EditDialogGui.delete_table_row with args', args)
    def get_checkbox_state(self, *args):
        print('called EditDialogGui.get_checkbox_state with args', args)
        return False
    def get_radiobutton_state(self, *args):
        print('called EditDialogGui.get_radiobutton_state with args', args)
        return False
    def get_selected_table_row(self, *args):
        print('called EditDialogGui.get_selected_table_row with args', args)
        return ''
    def get_tableitem_text(self, *args):
        print('called EditDialogGui.get_tableitem_text with args', args)
        return 'xxx'
    def get_table_rowcount(self, *args):
        print('called EditDialogGui.get_table_rowcount with args', args)
        return 0
    def get_textarea_contents(self, *args):
        print('called EditDialogGui.get_textarea_contents with args', args)
        return args[0]
    def get_textinput_value(self, *args):
        print('called EditDialogGui.get_textinput_value with args', args)
        return args[0]
    def set_button_text(self, *args):
        print('called EditDialogGui.set_button_text with args', args)
    def set_checkbox_state(self, *args):
        print('called EditDialogGui.set_checkbox_state with args', args)
    def set_radiobutton_state(self, *args):
        print('called EditDialogGui.set_radiobutton_state with args', args)
    def set_focus_to(self, *args, **kwargs):
        print('called EditDialogGui.set_focus_to with args', args, kwargs)
    def set_table_rowheader(self, *args):
        print('called EditDialogGui.set_table_rowheader with args', args)
    def select_table_cell(self, *args):
        print('called EditDialogGui.select_table_cell with args', args)
    def set_tableitem_text(self, *args):
        print('called EditDialogGui.set_tableitem_text with args', args)


class TestElementDialog:
    """unittests for main.ElementDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.ElementDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called ElementDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ElementDialog, '__init__', mock_init)
        testobj = testee.ElementDialog()
        testobj.gui = MockEditGui()
        assert capsys.readouterr().out == ('called ElementDialog.__init__ with args ()\n'
                                           "called EditDialogGui.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ElementDialog.__init__
        """
        def mock_analyze(*args):
            print('called analyze_element with args', args)
            return 'qqq', False, 'xxx', 'yyy', True, False
        def mock_analyze_2(*args):
            print('called analyze_element with args', args)
            return 'qqq', True, 'xxx', 'yyy', False, True
        monkeypatch.setattr(testee.gui, 'EditDialogGui', MockEditGui)
        monkeypatch.setattr(testee, 'analyze_element', mock_analyze)
        parent = types.SimpleNamespace(gui='EditDialogGui')
        testobj = testee.ElementDialog(parent)
        assert testobj.parent == parent
        assert testobj.style_text == 'xxx'
        assert testobj.style_button == 'style_button'
        assert testobj.styledata == 'yyy'
        assert testobj.has_style
        assert not testobj.is_stylesheet
        assert not testobj.csseditor_called
        assert testobj.old_styledata == 'yyy'
        assert not testobj.is_style_tag
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                f"called EditDialogGui.__init__ with args ({testobj}, 'EditDialogGui', '') {{}}\n"
                "called analyze_element with args ('', None)\n"
                "called EditDialogGui.add_topline with args () {}\n"
                "called EditDialogGui.add_label with args ('topline', 'element name:') {}\n"
                "called EditDialogGui.add_textinput with args ('topline', 'qqq', 250) {}\n"
                "called EditDialogGui.add_checkbox with args"
                " ('topline', '&Comment(ed)', False) {}\n"
                "called EditDialogGui.add_content_section with args () {}\n"
                "called EditDialogGui.add_table_to_section with args"
                " ('section', [('attribute', 102), ('value', 152)], None) {}\n"
                "called EditDialogGui.add_buttons_to_section with args"
                f" ('section', [('&Add Attribute', {testobj.on_add}),"
                f" ('&Delete Selected', {testobj.on_del}), ('xxx', {testobj.on_style})]) {{}}\n"
                "called EditDialogGui.add_buttons_to_bottom with args () {}\n"
                "called EditDialogGui.set_focus_to with args ('textbox',) {}\n")
        monkeypatch.setattr(testee, 'analyze_element', mock_analyze_2)
        tag = 'aaa'
        attrs = {'bla': 'dibla', 'style': 'ccc', 'styledata': 'ddd'}
        testobj = testee.ElementDialog(parent, title='title', tag=tag, attrs=attrs)
        assert testobj.parent == parent
        assert testobj.style_text == 'xxx'
        assert testobj.style_button == 'style_button'
        assert testobj.styledata == 'yyy'
        assert not testobj.has_style
        assert testobj.is_stylesheet
        assert not testobj.csseditor_called
        assert testobj.old_styledata == 'yyy'
        assert not testobj.is_style_tag
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                "called EditDialogGui.__init__ with args"
                f" ({testobj}, 'EditDialogGui', 'title') {{}}\n"
                "called analyze_element with args"
                " ('aaa', {'bla': 'dibla', 'style': 'ccc', 'styledata': 'ddd'})\n"
                "called EditDialogGui.add_topline with args () {}\n"
                "called EditDialogGui.add_label with args ('topline', 'element name:') {}\n"
                "called EditDialogGui.add_textinput with args ('topline', 'qqq', 250) {}\n"
                "called EditDialogGui.add_checkbox with args"
                " ('topline', '&Comment(ed)', True) {}\n"
                "called EditDialogGui.add_content_section with args () {}\n"
                "called EditDialogGui.add_table_to_section with args"
                " ('section', [('attribute', 102), ('value', 152)],"
                " {'bla': 'dibla', 'style': 'ccc', 'styledata': 'ddd'""}) {}\n"
                "called EditDialogGui.add_buttons_to_section with args"
                f" ('section', [('&Add Attribute', {testobj.on_add}),"
                f" ('&Delete Selected', {testobj.on_del}), ('xxx', {testobj.on_style})]) {{}}\n"
                "called EditDialogGui.add_buttons_to_bottom with args () {}\n"
                "called EditDialogGui.set_focus_to with args ('textbox',) {}\n")

    def test_on_add(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_add
        """
        def mock_refresh():
            print('called ElementDialog.refresh')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh = mock_refresh
        testobj.attr_table = 'table'
        testobj.on_add()
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.add_table_row with args ('table', 0)\n"
                "called EditDialogGui.set_table_rowheader with args ('table', 0, '')\n"
                "called EditDialogGui.select_table_cell with args ('table', 0, 0)\n")

    def test_on_del(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_del
        """
        def mock_refresh():
            print('called ElementDialog.refresh')
        def mock_show(*args):
            print('called gui.show_message with args', args)
        def mock_get_row(*args):
            print('called EditDialogGui.get_selected_table_row with args', args)
            return 'row'
        def mock_get_text(*args):
            print('called EditDialogGui.get_tableitem_text with args', args)
            return 'style'
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.refresh = mock_refresh
        testobj.attr_table = 'table'
        testobj.on_del()
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called EditDialogGui.get_selected_table_row with args ('table',)\n"
                f"called gui.show_message with args ({testobj.gui}, 'Delete attribute',"
                " 'Select a row by clicking on the row heading')\n")
        testobj.gui.get_selected_table_row = mock_get_row
        testobj.has_style = True
        testobj.on_del()
        assert testobj.has_style
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called EditDialogGui.get_selected_table_row with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 'row', 0)\n"
                "called EditDialogGui.delete_table_row with args ('table', 'row')\n")
        testobj.gui.get_tableitem_text = mock_get_text
        testobj.on_del()
        assert not testobj.has_style
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called EditDialogGui.get_selected_table_row with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 'row', 0)\n"
                "called EditDialogGui.delete_table_row with args ('table', 'row')\n")

    def test_on_style(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_style
        """
        def mock_refresh():
            print('called ElementDialog.refresh')
        def mock_get_rowcount(*args):
            print('called EditDialogGui.get_table_rowcount with args', args)
            return 3
        def mock_get_text(*args):
            print('called EditDialogGui.get_tableitem_text with args', args)
            if args[-2] == 1 and args[-1] == 0:
                return 'href'
            return 'xxx'
        def mock_call_1(arg):
            print(f"called CssManager.call_editor_for_stylesheet with arg '{arg}'")
        def mock_call_2(*args):
            print('called CssManager.call_editor with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_tableitem_text = mock_get_text
        testobj.refresh = mock_refresh
        testobj.is_stylesheet = True
        testobj.parent = types.SimpleNamespace(editor=types.SimpleNamespace(
            cssm=types.SimpleNamespace(call_editor_for_stylesheet=mock_call_1,
                                       call_editor=mock_call_2)))
        testobj.style_button = 'button'
        testobj.style_text = 'xxx'
        testobj.tag_text = 'yyy'
        testobj.attr_table = 'table'
        testobj.check_changes = True
        testobj.on_style()
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                "called ElementDialog.refresh\n"
                "called EditDialogGui.set_button_text with args ('button', 'xxx')\n")
        testobj.check_changes = False
        testobj.on_style()
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                "called EditDialogGui.set_button_text with args ('button', 'Chec&k Changes')\n"
                "called EditDialogGui.get_textinput_value with args ('yyy',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called CssManager.call_editor_for_stylesheet with arg ''\n"
                "called ElementDialog.refresh\n")
        testobj.check_changes = False
        testobj.gui.get_table_rowcount = mock_get_rowcount
        testobj.on_style()
        assert not testobj.check_changes
        assert capsys.readouterr().out == (
                "called EditDialogGui.set_button_text with args ('button', 'Chec&k Changes')\n"
                "called EditDialogGui.get_textinput_value with args ('yyy',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 1)\n"
                "called CssManager.call_editor_for_stylesheet with arg 'xxx'\n"
                "called ElementDialog.refresh\n")
        testobj.check_changes = False
        testobj.is_stylesheet = False
        testobj.on_style()
        assert testobj.check_changes
        assert capsys.readouterr().out == (
                "called EditDialogGui.set_button_text with args ('button', 'Chec&k Changes')\n"
                "called EditDialogGui.get_textinput_value with args ('yyy',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 1)\n"
                f"called CssManager.call_editor with args ({testobj}, 'yyy')\n")

    def test_refresh(self, monkeypatch, capsys):
        """unittest for ElementDialog.refresh
        """
        def mock_analyze(*args):
            print('called analyze_element with args', args)
            return 'qqq', False, 'xxx', 'yyy', True, False
        def mock_get_rowcount(*args):
            print('called EditDialogGui.get_table_rowcount with args', args)
            return 3
        def mock_get_text(*args):
            print('called EditDialogGui.get_tableitem_text with args', args)
            if args[-2] == 1 and args[-1] == 0:
                return 'style'
            return 'xxx'
        monkeypatch.setattr(testee, 'analyze_element', mock_analyze)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_tableitem_text = mock_get_text
        testobj.has_style = False
        testobj.styledata = 'styledata'
        testobj.style_button = 'button'
        testobj.tag_text = 'link'
        testobj.attr_table = 'table'
        testobj.refresh()
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('link',)\n")
        testobj.tag_text = 'text'
        testobj.refresh()
        assert not testobj.is_style_tag
        assert testobj.has_style
        assert testobj.old_styledata == 'styledata'
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('text',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.add_table_row with args ('table', 0)\n"
                "called EditDialogGui.set_table_rowheader with args ('table', 0, '')\n"
                "called EditDialogGui.add_table_rowitem with args"
                " ('table', 0, 0, 'style') {'editable': False}\n"
                "called EditDialogGui.add_table_rowitem with args"
                " ('table', 0, 1, 'styledata') {'editable': False}\n"
                "called analyze_element with args ('', {'style': ''})\n"
                "called EditDialogGui.set_button_text with args ('button', 'xxx')\n")
        testobj.gui.get_table_rowcount = mock_get_rowcount
        testobj.refresh()
        assert not testobj.is_style_tag
        assert testobj.has_style
        assert testobj.old_styledata == 'styledata'
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('text',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 0)\n"
                "called EditDialogGui.set_tableitem_text with args ('table', 1, 1, 'styledata')\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for ElementDialog.confirm
        """
        def mock_get_text(*args):
            print('called EditDialogGui.get_tableitem_text with args', args)
            raise AttributeError
        def mock_get_text_2(*args):
            print('called EditDialogGui.get_tableitem_text with args', args)
            if args[-1] == 0:
                return 'dup'
            return 'xxx'
        def mock_get_text_3(*args):
            print('called EditDialogGui.get_tableitem_text with args', args)
            if args[-2] == 1 and args[-1] == 0:
                return 'style'
            if args[-2] == 2 and args[-1] == 0:
                return 'style'
            return 'xxx'
        def mock_get_rowcount(*args):
            print('called EditDialogGui.get_table_rowcount with args', args)
            return 3
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockEditGui()
        assert capsys.readouterr().out == "called EditDialogGui.__init__ with args () {}\n"
        testobj.gui.get_tableitem_text = mock_get_text
        testobj.parent = types.SimpleNamespace(dialog_data=[])
        testobj.is_style_tag = False
        testobj.has_style = False
        testobj.styledata = 'sss'
        testobj.tag_text = 'x!x'
        testobj.comment_button = 'comment_button'
        testobj.attr_table = 'table'
        assert testobj.confirm() == "Illegal character(s) in tag name"
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('x!x',)\n")
        testobj.tag_text = 'xxx'
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ('xxx', {}, False)
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('xxx',)\n"
                "called EditDialogGui.get_checkbox_state with args ('comment_button',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n")
        testobj.gui.get_table_rowcount = mock_get_rowcount
        assert testobj.confirm() == "Press enter on this item first"
        assert testobj.parent.dialog_data == ('xxx', {}, False)
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('xxx',)\n"
                "called EditDialogGui.get_checkbox_state with args ('comment_button',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 0)\n")
        testobj.gui.get_tableitem_text = mock_get_text_2
        assert testobj.confirm() == "Duplicate attributes, please merge"
        assert testobj.parent.dialog_data == ('xxx', {}, False)
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('xxx',)\n"
                "called EditDialogGui.get_checkbox_state with args ('comment_button',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 1)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 1)\n")
        testobj.gui.get_tableitem_text = mock_get_text_3
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ('xxx', {'xxx': 'xxx'}, False)
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('xxx',)\n"
                "called EditDialogGui.get_checkbox_state with args ('comment_button',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 1)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 1)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 2, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 2, 1)\n")
        testobj.is_style_tag = False
        testobj.has_style = True
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ('xxx', {'xxx': 'xxx', 'style': 'sss'}, False)
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('xxx',)\n"
                "called EditDialogGui.get_checkbox_state with args ('comment_button',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 1)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 1)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 2, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 2, 1)\n")
        testobj.is_style_tag = True
        testobj.has_style = False
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ('xxx', {'xxx': 'xxx', 'styledata': 'sss'}, False)
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textinput_value with args ('xxx',)\n"
                "called EditDialogGui.get_checkbox_state with args ('comment_button',)\n"
                "called EditDialogGui.get_table_rowcount with args ('table',)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 0, 1)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 1, 1)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 2, 0)\n"
                "called EditDialogGui.get_tableitem_text with args ('table', 2, 1)\n")


class TestTextDialog:
    """unittests for main.TextDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.TextDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called TextDialog.__init__ with args', args)
        monkeypatch.setattr(testee.TextDialog, '__init__', mock_init)
        testobj = testee.TextDialog()
        assert capsys.readouterr().out == 'called TextDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TextDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'EditDialogGui', MockEditGui)
        parent = types.SimpleNamespace(gui='EditDialogGui')
        testobj = testee.TextDialog(parent)
        assert testobj.parent == parent
        assert testobj.comment_button == 'checkbox'
        assert testobj.data_text == 'textbox'
        assert capsys.readouterr().out == (
                f"called EditDialogGui.__init__ with args ({testobj}, 'EditDialogGui', '') {{}}\n"
                "called EditDialogGui.add_topline with args () {}\n"
                "called EditDialogGui.add_checkbox with args ('topline', '&Comment(ed)', False) {}\n"
                "called EditDialogGui.add_content_section with args () {}\n"
                "called EditDialogGui.add_textinput_to_section with args"
                " ('section', '', 340, 175) {}\n"
                "called EditDialogGui.add_buttons_to_bottom with args () {}\n"
                "called EditDialogGui.set_focus_to with args ('textbox',) {}\n")
        testobj = testee.TextDialog(parent, title='xxx', text='yyyy')
        assert testobj.parent == parent
        assert testobj.comment_button == 'checkbox'
        assert testobj.data_text == 'textbox'
        assert capsys.readouterr().out == (
                f"called EditDialogGui.__init__ with args ({testobj}, 'EditDialogGui', 'xxx') {{}}\n"
                "called EditDialogGui.add_topline with args () {}\n"
                "called EditDialogGui.add_checkbox with args ('topline', '&Comment(ed)', False) {}\n"
                "called EditDialogGui.add_content_section with args () {}\n"
                "called EditDialogGui.add_textinput_to_section with args"
                " ('section', 'yyyy', 340, 175) {}\n"
                "called EditDialogGui.add_buttons_to_bottom with args () {}\n"
                "called EditDialogGui.set_focus_to with args ('textbox',) {}\n")
        testobj = testee.TextDialog(parent, title='xxx', text='<!> yyyy')
        assert testobj.parent == parent
        assert testobj.comment_button == 'checkbox'
        assert testobj.data_text == 'textbox'
        assert capsys.readouterr().out == (
                f"called EditDialogGui.__init__ with args ({testobj}, 'EditDialogGui', 'xxx') {{}}\n"
                "called EditDialogGui.add_topline with args () {}\n"
                "called EditDialogGui.add_checkbox with args ('topline', '&Comment(ed)', False) {}\n"
                "called EditDialogGui.set_checkbox_state with args ('checkbox', True)\n"
                "called EditDialogGui.add_content_section with args () {}\n"
                "called EditDialogGui.add_textinput_to_section with args"
                " ('section', 'yyyy', 340, 175) {}\n"
                "called EditDialogGui.add_buttons_to_bottom with args () {}\n"
                "called EditDialogGui.set_focus_to with args ('textbox',) {}\n")
        testobj = testee.TextDialog(parent, title='xxx', text='yyyy', show_comment_switch=False)
        assert testobj.parent == parent
        assert not hasattr(testobj, 'comment_button')
        assert testobj.data_text == 'textbox'
        assert capsys.readouterr().out == (
                f"called EditDialogGui.__init__ with args ({testobj}, 'EditDialogGui', 'xxx') {{}}\n"
                "called EditDialogGui.add_content_section with args () {}\n"
                "called EditDialogGui.add_textinput_to_section with args"
                " ('section', 'yyyy', 340, 175) {}\n"
                "called EditDialogGui.add_buttons_to_bottom with args () {}\n"
                "called EditDialogGui.set_focus_to with args ('textbox',) {}\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for TextDialog.confirm
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockEditGui()
        assert capsys.readouterr().out == "called EditDialogGui.__init__ with args () {}\n"
        testobj.parent = types.SimpleNamespace()
        testobj.data_text = 'xxx'
        testobj.confirm()
        assert testobj.parent.dialog_data == ('xxx', False)
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_textarea_contents with args ('xxx',)\n")
        testobj.comment_button = 'checkbox'
        testobj.confirm()
        assert testobj.parent.dialog_data == ('xxx', False)
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_checkbox_state with args ('checkbox',)\n"
                "called EditDialogGui.get_textarea_contents with args ('xxx',)\n")


class MockSearchGui:
    "testdouble voor qtgui.SearchDialogGui"
    def __init__(self, *args, **kwargs):
        print('called SearchDialogGui.__init__ with args', args, kwargs)
    def add_buttons_to_bottom(self):
        print('called SearchDialogGui.add_buttons_to_bottom')
    def add_checkbox(self, *args):
        print('called SearchDialogGui.add_checkbox with args', args)
        return 'checkbox'
    def add_description(self):
        print('called SearchDialogGui.add_description')
        return 'text'
    def add_lineinput(self, *args):
        print('called SearchDialogGui.add_lineinput with args', args)
        return 'lineinput'
    def add_text(self, *args):
        print('called SearchDialogGui.add_text with args', args)
    def add_title(self, *args):
        print('called SearchDialogGui.add_title with args', args)
    def get_checkbox_state(self, *args):
        print('called SearchDialogGui.get_checkbox_state with args', args)
        return False
    def get_lineinput_value(self, *args):
        print('called SearchDialogGui.get_lineinput_value with args', args)
        return args[0]
    def set_focus_to(self, *args):
        print('called SearchDialogGui.set_focus_to with args', args)
    def set_label_text(self, *args):
        print('called SearchDialogGui.set_label_text with args', args)
    def set_lineinput_value(self, *args):
        print('called SearchDialogGui.set_lineinput_value with args', args)
    def setup_container(self):
        print('called SearchDialogGui.setup_container')
    def update_size(self):
        print('called SearchDialogGui.update_size')


class TestSearchDialog:
    """unittests for main.SearchDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.SearchDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called SearchDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SearchDialog, '__init__', mock_init)
        testobj = testee.SearchDialog()
        testobj.gui = MockSearchGui()
        assert capsys.readouterr().out == ('called SearchDialog.__init__ with args ()\n'
                                           "called SearchDialogGui.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SearchDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'SearchDialogGui', MockSearchGui)
        parent = types.SimpleNamespace(editor=types.SimpleNamespace(), gui='EditorGui',
                                       search_args=())
        testobj = testee.SearchDialog(parent)
        assert testobj.parent == parent
        assert not testobj.replace
        assert testobj.txt_element == 'lineinput'
        assert testobj.txt_attr_name == 'lineinput'
        assert testobj.txt_attr_val == 'lineinput'
        assert testobj.txt_text == 'lineinput'
        assert not hasattr(testobj, 'txt.element')
        assert not hasattr(testobj, 'txt.attr_name')
        assert not hasattr(testobj, 'txt.attr_val')
        assert not hasattr(testobj, 'txt.text')
        assert capsys.readouterr().out == (
                f"called SearchDialogGui.__init__ with args ({testobj}, 'EditorGui', '') {{}}\n"
                "called SearchDialogGui.setup_container\n"
                "called SearchDialogGui.add_title with args (None, 'Search for:', 0, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'Element', 1, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 1, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 1, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Attribute', 2, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 2, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 2, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 3, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 3, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Text', 4, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 4, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 4, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_description\n"
                "called SearchDialogGui.add_buttons_to_bottom\n"
                "called SearchDialogGui.set_focus_to with args ('lineinput',)\n")
        parent.search_args = ('a', 'b', 'c', 'd')
        parent.replace_args = ()
        testobj = testee.SearchDialog(parent, 'title', replace=True)
        assert testobj.parent == parent
        assert testobj.replace
        assert testobj.txt_element == 'lineinput'
        assert testobj.txt_attr_name == 'lineinput'
        assert testobj.txt_attr_val == 'lineinput'
        assert testobj.txt_text == 'lineinput'
        assert testobj.txt_element_replace == 'lineinput'
        assert testobj.txt_attr_name_replace == 'lineinput'
        assert testobj.txt_attr_val_replace == 'lineinput'
        assert testobj.txt_text_replace == 'lineinput'
        assert capsys.readouterr().out == (
                f"called SearchDialogGui.__init__ with args ({testobj}, 'EditorGui', 'title') {{}}\n"
                "called SearchDialogGui.setup_container\n"
                "called SearchDialogGui.add_title with args (None, 'Search for:', 0, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'Element', 1, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 1, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 1, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Attribute', 2, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 2, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 2, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 3, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 3, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Text', 4, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 4, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 4, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_title with args (None, 'Replace with:', 0, 3)\n"
                "called SearchDialogGui.add_text with args (None, 'Element', 1, 4)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 1, 5)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 1, 6, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Attribute', 2, 4)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 2, 5)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 2, 6, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 3, 5)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 3, 6, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Text', 4, 4)\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 4, 5)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 4, 6, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_checkbox with args (None, 'Replace All', 5, 3)\n"
                "called SearchDialogGui.add_description\n"
                "called SearchDialogGui.add_buttons_to_bottom\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'a')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'b')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'c')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'd')\n"
                "called SearchDialogGui.set_focus_to with args ('lineinput',)\n")
        parent.search_args = ('a', 'b', 'c', 'd')
        parent.replace_args = ('aa', 'bb', 'cc', 'dd')
        testobj = testee.SearchDialog(parent, 'title', replace=True)
        assert testobj.parent == parent
        assert testobj.replace
        assert testobj.txt_element == 'lineinput'
        assert testobj.txt_attr_name == 'lineinput'
        assert testobj.txt_attr_val == 'lineinput'
        assert testobj.txt_text == 'lineinput'
        assert testobj.txt_element_replace == 'lineinput'
        assert testobj.txt_attr_name_replace == 'lineinput'
        assert testobj.txt_attr_val_replace == 'lineinput'
        assert testobj.txt_text_replace == 'lineinput'
        assert capsys.readouterr().out == (
                f"called SearchDialogGui.__init__ with args ({testobj}, 'EditorGui', 'title') {{}}\n"
                "called SearchDialogGui.setup_container\n"
                "called SearchDialogGui.add_title with args (None, 'Search for:', 0, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'Element', 1, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 1, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 1, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Attribute', 2, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 2, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 2, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 3, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 3, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Text', 4, 0)\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 4, 1)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 4, 2, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_title with args (None, 'Replace with:', 0, 3)\n"
                "called SearchDialogGui.add_text with args (None, 'Element', 1, 4)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 1, 5)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 1, 6, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Attribute', 2, 4)\n"
                "called SearchDialogGui.add_text with args (None, 'name:', 2, 5)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 2, 6, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 3, 5)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 3, 6, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_text with args (None, 'Text', 4, 4)\n"
                "called SearchDialogGui.add_text with args (None, 'value:', 4, 5)\n"
                "called SearchDialogGui.add_lineinput with args"
                f" (None, 4, 6, {testobj.update_search_text})\n"
                "called SearchDialogGui.add_checkbox with args (None, 'Replace All', 5, 3)\n"
                "called SearchDialogGui.add_description\n"
                "called SearchDialogGui.add_buttons_to_bottom\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'a')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'b')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'c')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'd')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'aa')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'bb')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'cc')\n"
                "called SearchDialogGui.set_lineinput_value with args ('lineinput', 'dd')\n"
                "called SearchDialogGui.set_focus_to with args ('lineinput',)\n")

    def test_update_search_text(self, monkeypatch, capsys):
        """unittest for SearchDialog.update_search_text
        """
        def mock_build(*args):
            print('called EditorHelper.build_search_specs with args', args)
            return 'search specs'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(build_search_spec=mock_build)
        testobj.txt_element = 'ele'
        testobj.txt_attr_name = 'attr'
        testobj.txt_attr_val = 'val'
        testobj.txt_text = 'txt'
        testobj.txt_element_replace = 'new ele'
        testobj.txt_attr_name_replace = 'new attr'
        testobj.txt_attr_val_replace = 'new val'
        testobj.txt_text_replace = 'new txt'
        testobj.lbl_search = 'search'
        testobj.replace = False
        testobj.update_search_text()
        assert testobj.search_specs == 'search specs'
        assert capsys.readouterr().out == (
                "called SearchDialogGui.get_lineinput_value with args ('ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('txt',)\n"
                "called EditorHelper.build_search_specs with args"
                " ('ele', 'attr', 'val', 'txt', ())\n"
                "called SearchDialogGui.set_label_text with args ('search', 'search specs')\n"
                "called SearchDialogGui.update_size\n")
        testobj.replace = True
        testobj.update_search_text()
        assert testobj.search_specs == 'search specs'
        assert capsys.readouterr().out == (
                "called SearchDialogGui.get_lineinput_value with args ('new ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new txt',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('txt',)\n"
                "called EditorHelper.build_search_specs with args"
                " ('ele', 'attr', 'val', 'txt', ('new ele', 'new attr', 'new val', 'new txt'))\n"
                "called SearchDialogGui.set_label_text with args ('search', 'search specs')\n"
                "called SearchDialogGui.update_size\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SearchDialog.confirm
        """
        def mock_get(*args):
            print('called SearchDialogGui.get_lineinput_value with args', args)
            return ''
        def mock_get_2(*args):
            print('called SearchDialogGui.get_lineinput_value with args', args)
            return args[0]
        def mock_get_3(*args):
            print('called SearchDialogGui.get_lineinput_value with args', args)
            if args[0].startswith('new'):
                return ''
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace()
        testobj.gui.get_lineinput_value = mock_get
        testobj.search_specs = 'search spacs'
        testobj.txt_element = 'ele'
        testobj.txt_attr_name = 'attr'
        testobj.txt_attr_val = 'val'
        testobj.txt_text = 'txt'
        testobj.txt_element_replace = 'new ele'
        testobj.txt_attr_name_replace = 'new attr'
        testobj.txt_attr_val_replace = 'new val'
        testobj.txt_text_replace = 'new txt'
        testobj.cb_replace_all = 'replace_all'
        testobj.replace = False
        testobj.parent.dialog_data = ()
        assert testobj.confirm() == 'Please enter search criteria or press cancel'
        assert testobj.parent.dialog_data == ()
        assert capsys.readouterr().out == (
                "called SearchDialogGui.get_lineinput_value with args ('ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('txt',)\n")
        testobj.gui.get_lineinput_value = mock_get_2
        # testobj.parent.dialog_data = ()
        assert testobj.confirm() == ''
        assert testobj.parent.dialog_data == (('ele', 'attr', 'val', 'txt'), 'search spacs', ())
        assert capsys.readouterr().out == (
                "called SearchDialogGui.get_lineinput_value with args ('ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('txt',)\n")
        testobj.replace = True
        testobj.gui.get_lineinput_value = mock_get_3
        testobj.parent.dialog_data = ()
        assert testobj.confirm() == 'Please enter replacement criteria or press cancel'
        assert testobj.parent.dialog_data == ()
        assert capsys.readouterr().out == (
                "called SearchDialogGui.get_lineinput_value with args ('ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('txt',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new txt',)\n")
        testobj.gui.get_lineinput_value = mock_get_2
        testobj.parent.dialog_data = ()
        assert testobj.confirm() == ''
        assert testobj.parent.dialog_data == (('ele', 'attr', 'val', 'txt'), 'search spacs',
                                              ('new ele', 'new attr', 'new val', 'new txt', False))
        assert capsys.readouterr().out == (
                "called SearchDialogGui.get_lineinput_value with args ('ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('txt',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new ele',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new attr',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new val',)\n"
                "called SearchDialogGui.get_lineinput_value with args ('new txt',)\n"
                "called SearchDialogGui.get_checkbox_state with args ('replace_all',)\n")


class TestDtdDialog:
    """unittests for main.DtdDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.DtdDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called DtdDialog.__init__ with args', args)
        monkeypatch.setattr(testee.DtdDialog, '__init__', mock_init)
        testobj = testee.DtdDialog()
        testobj.gui = MockEditGui()
        assert capsys.readouterr().out == ('called DtdDialog.__init__ with args ()\n'
                                           "called EditDialogGui.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DtdDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'EditDialogGui', MockEditGui)
        parent = types.SimpleNamespace(gui='EditDialogGui', dtdlist=[])
        with pytest.raises(IndexError):
            testobj = testee.DtdDialog(parent, title='Add DTD')
        capsys.readouterr()   # ignore and flush captured output
        parent.dtdlist = [('xxx', 'yyy', 'zzz'), ('HTML 5', 'bbb', 'ccc')]
        testobj = testee.DtdDialog(parent, title='Add DTD')
        assert testobj.parent == parent
        assert testobj.dtd_list == [('xxx', 'yyy', 'radiobutton'),
                                    ('HTML 5', 'bbb', 'radiobutton')]
        assert capsys.readouterr().out == (
                "called EditDialogGui.__init__ with args"
                f" ({testobj}, 'EditDialogGui', 'Add DTD') {{}}\n"
                "called EditDialogGui.add_content_section with args () {}\n"
                "called EditDialogGui.add_text_to_section with args"
                " ('section', 'Select document type:')\n"
                "called EditDialogGui.add_radiobutton_to_section with args"
                " ('section', 'xxx', True, False)\n"
                "called EditDialogGui.add_radiobutton_to_section with args"
                " ('section', 'HTML 5', False, True)\n"
                "called EditDialogGui.add_buttons_to_bottom with args () {}\n"
                "called EditDialogGui.set_focus_to with args ('radiobutton',) {}\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for DtdDialog.confirm
        """
        def mock_get(*args):
            nonlocal counter
            print('called EditDialogGui.get_radiobutton_state with args', args)
            counter += 1
            return counter > 1
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_radiobutton_state = mock_get
        testobj.parent = types.SimpleNamespace()
        testobj.dtd_list = []
        testobj.confirm()
        assert not hasattr(testobj.parent, 'dialog_data')
        assert capsys.readouterr().out == ""
        testobj.dtd_list = [('xxx', 'yyy', 'radiobutton'), ('aaa', 'bbb', 'radiobutton')]
        counter = 0
        testobj.confirm()
        assert testobj.parent.dialog_data == 'bbb'
        assert capsys.readouterr().out == (
                "called EditDialogGui.get_radiobutton_state with args ('radiobutton',)\n"
                "called EditDialogGui.get_radiobutton_state with args ('radiobutton',)\n")


class MockAddGui:
    "testdouble voor qtgui.AddDialogGui"
    def __init__(self, *args, **kwargs):
        print('called AddDialogGui.__init__ with args', args, kwargs)
    def add_button_line_to_section(self, *args):
        print('called AddDialogGui.add_button_line_to_section with args', args)
        return [x[0] for x in args[2]]
    def add_buttons_to_bottom(self, **kwargs):
        print('called AddDialogGui.add_buttons_to_bottom with args', kwargs)
        return ['extra_button'] if 'extra' in kwargs else None
    def add_checkbox_to_section(self, *args, **kwargs):
        print('called AddDialogGui.add_checkbox_to_section with args', args, kwargs)
        return 'checkbox'
    def add_combobox_to_section(self, *args, **kwargs):
        print('called AddDialogGui.add_combobox_to_section with args', args, kwargs)
        return 'combobox'
    def add_content_section(self):
        print('called AddDialogGui.add_content_section')
        return 'grid'
    def add_spinbox_to_section(self, *args, **kwargs):
        print('called AddDialogGui.add_spinbox_to_section with args', args, kwargs)
        return 'spinner'
    def add_table_column(self, *args):
        print('called AddDialogGui.add_table_column with args', args)
    def add_table_row(self, *args):
        print('called AddDialogGui.add_table_row with args', args)
    def add_table_to_section(self, *args, **kwargs):
        print('called AddDialogGui.add_table_to_section with args', args, kwargs)
        return 'table'
    def add_textinput_to_section(self, *args, **kwargs):
        print('called AddDialogGui.add_textinput_to_section with args', args, kwargs)
        return 'text'
    def add_text_to_section(self, *args):
        print('called AddDialogGui.add_text_to_section with args', args)
    def enable_table_header(self, *args):
        print('called AddDialogGui.enable_table_header with args', args)
    def enable_widget(self, *args):
        print('called AddDialogGui.enable_widget with args', args)
    def get_checkbox_state(self, *args):
        print('called AddDialogGui.get_checkbox_state with args', args)
        return False
    def get_conbobox_text(self, *args):
        print('called AddDialogGui.get_conbobox_text with args', args)
        return 'value from combobox'
    def get_spinbox_value(self, *args):
        print('called AddDialogGui.get_spinbox_value with args', args)
        return 'spinbox value'
    def get_table_column(self, *args):
        print('called AddDialogGui.get_table_column with args', args)
        return 'colno'
    def get_table_columncount(self, *args):
        print('called AddDialogGui.get_table_columncount with args', args)
        return 0
    def get_table_rowcount(self, *args):
        print('called AddDialogGui.get_table_rowcount with args', args)
        return 0
    def get_tablecell_itemtext(self, *args):
        print('called AddDialogGui.get_tablecell_itemtext with args', args)
        return 'itemtext'
    def get_textinput_value(self, *args):
        print('called AddDialogGui.get_textinput_value with args', args)
        return 'text'
    def remove_table_column(self, *args):
        print('called AddDialogGui.remove_table_column with args', args)
    def remove_table_row(self, *args):
        print('called AddDialogGui.remove_table_row with args', args)
    def set_focus_to(self, *args):
        print('called AddDialogGui.set_focus_to with args', args)
    def set_table_headers(self, *args):
        print('called AddDialogGui.set_table_headers with args', args)
    def set_textinput_value(self, *args):
        print('called AddDialogGui.set_textinput_value with args', args)


class TestCssDialog:
    """unittests for main.CssDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.CssDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called CssDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CssDialog, '__init__', mock_init)
        testobj = testee.CssDialog()
        testobj.gui = MockAddGui()
        assert capsys.readouterr().out == ('called CssDialog.__init__ with args ()\n'
                                           'called AddDialogGui.__init__ with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for CssDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'AddDialogGui', MockAddGui)
        parent = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.CssDialog(parent, title='Add StyleSheet')
        assert testobj.parent == parent
        assert testobj.link_text == 'text'
        assert testobj.new_button == '&Select'
        assert testobj.choose_button == 'C&reate'
        assert testobj.edit_button == 'Select + &Edit'
        assert testobj.inline_button == 'extra_button'
        assert testobj.text_text == 'text'
        assert capsys.readouterr().out == (
                "called AddDialogGui.__init__ with args"
                f" ({testobj}, 'EditorGui', 'Add StyleSheet') {{}}\n"
                "called AddDialogGui.add_content_section\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'link to stylesheet:', 0, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                " ('grid', 0, 1, 'http://') {}\n"
                "called AddDialogGui.add_button_line_to_section with args"
                f" ('grid', 1, [('&Select', {testobj.kies}), ('C&reate', {testobj.nieuw}),"
                f" ('Select + &Edit', {testobj.edit})])\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'for media type(s):', 2, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args ('grid', 2, 1) {}\n"
                "called AddDialogGui.add_buttons_to_bottom with args"
                f" {{'extra': ('&Add inline', {testobj.on_inline})}}\n"
                "called AddDialogGui.set_focus_to with args ('text',)\n")

    def test_kies(self, monkeypatch, capsys):
        """unittest for CssDialog.kies
        """
        def mock_select(*args):
            print('called CssDialog.select_file with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_file = mock_select
        testobj.kies()
        assert capsys.readouterr().out == "called CssDialog.select_file with args ()\n"

    def test_nieuw(self, monkeypatch, capsys):
        """unittest for CssDialog.nieuw
        """
        def mock_select(**kwargs):
            print('called CssDialog.select_file with args', kwargs)
            return ''
        def mock_select_2(**kwargs):
            print('called CssDialog.select_file with args', kwargs)
            return 'xxx'
        def mock_call(*args, **kwargs):
            print('called CssManager.call_editor_for_stylesheet with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(cssm=types.SimpleNamespace(
            call_editor_for_stylesheet=mock_call))
        testobj.select_file = mock_select
        testobj.nieuw()
        assert capsys.readouterr().out == (
                "called CssDialog.select_file with args {'create': True}\n")
        testobj.select_file = mock_select_2
        testobj.nieuw()
        assert capsys.readouterr().out == (
                "called CssDialog.select_file with args {'create': True}\n"
                "called CssManager.call_editor_for_stylesheet with args"
                " ('xxx',) {'new_ok': True}\n")

    def test_edit(self, monkeypatch, capsys):
        """unittest for CssDialog.edit
        """
        def mock_select(**kwargs):
            print('called CssDialog.select_file with args', kwargs)
            return ''
        def mock_select_2(**kwargs):
            print('called CssDialog.select_file with args', kwargs)
            return 'xxx'
        def mock_call(*args, **kwargs):
            print('called CssManager.call_editor_for_stylesheet with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(cssm=types.SimpleNamespace(
            call_editor_for_stylesheet=mock_call))
        testobj.select_file = mock_select
        testobj.edit()
        assert capsys.readouterr().out == "called CssDialog.select_file with args {}\n"
        testobj.select_file = mock_select_2
        testobj.edit()
        assert capsys.readouterr().out == (
                "called CssDialog.select_file with args {}\n"
                "called CssManager.call_editor_for_stylesheet with args ('xxx',) {}\n")

    def test_select_file(self, monkeypatch, capsys):
        """unittest for CssDialog.select_file
        """
        def mock_get(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        def mock_build(*args):
            print('called gui.build_mask with args', args)
            return 'mask'
        def mock_ask_save(*args):
            print('called gui.ask_for_save_filename with args', args)
            return ''
        def mock_ask_save_2(*args):
            print('called gui.ask_for_save_filename with args', args)
            return 'xxx'
        def mock_ask_open(*args):
            print('called gui.ask_for_open_filename with args', args)
            return ''
        def mock_ask_open_2(*args):
            print('called gui.ask_for_open_filename with args', args)
            return 'xxx'
        monkeypatch.setattr(testee.gui, 'ask_for_save_filename', mock_ask_save)
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_textinput_value = mock_get
        testobj.parent = types.SimpleNamespace(xmlfn='path/to/xxx')
        testee.gui.build_mask = mock_build
        testobj.link_text = 'xxx'
        assert testobj.select_file() == ""
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n"
                "called gui.build_mask with args ('css',)\n"
                f"called gui.ask_for_open_filename with args ({testobj.gui}, 'xxx', 'mask')\n")
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open_2)
        assert testobj.select_file() == "xxx"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n"
                "called gui.build_mask with args ('css',)\n"
                f"called gui.ask_for_open_filename with args ({testobj.gui}, 'xxx', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('xxx', 'xxx')\n")
        assert testobj.select_file(create=True) == ""
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n"
                "called gui.build_mask with args ('css',)\n"
                f"called gui.ask_for_save_filename with args ({testobj.gui}, 'xxx', 'mask')\n")
        monkeypatch.setattr(testee.gui, 'ask_for_save_filename', mock_ask_save_2)
        assert testobj.select_file(create=True) == "xxx"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n"
                "called gui.build_mask with args ('css',)\n"
                f"called gui.ask_for_save_filename with args ({testobj.gui}, 'xxx', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('xxx', 'xxx')\n")
        testobj.link_text = ''
        assert testobj.select_file() == "xxx"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('',)\n"
                "called gui.build_mask with args ('css',)\n"
                f"called gui.ask_for_open_filename with args ({testobj.gui}, 'path/to', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('', 'xxx')\n")
        testobj.parent.xmlfn = ''
        assert testobj.select_file() == "xxx"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('',)\n"
                "called gui.build_mask with args ('css',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, '{testee.os.getcwd()}', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('', 'xxx')\n")
        testobj.link_text = 'http://xxx'
        assert testobj.select_file() == "xxx"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('http://xxx',)\n"
                "called gui.build_mask with args ('css',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, '{testee.os.getcwd()}', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('http://xxx', 'xxx')\n")

    def test_on_inline(self, monkeypatch, capsys):
        """unittest for CssDialog.on_inline
        """
        def mock_call(*args, **kwargs):
            print('called CssManager.call_From_inline with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(cssm=types.SimpleNamespace(
            call_from_inline=mock_call))
        testobj.link_text = 'text'
        testobj.new_button = '&Select'
        testobj.choose_button = 'C&reate'
        testobj.edit_button = 'Select + &Edit'
        testobj.inline_button = '&Inline'
        testobj.on_inline()
        assert capsys.readouterr().out == (
                f"called CssManager.call_From_inline with args ({testobj}, '') {{}}\n"
                "called AddDialogGui.enable_widget with args ('text', False)\n"
                "called AddDialogGui.enable_widget with args ('&Select', False)\n"
                "called AddDialogGui.enable_widget with args ('Select + &Edit', False)\n"
                "called AddDialogGui.enable_widget with args ('C&reate', False)\n"
                "called AddDialogGui.enable_widget with args ('&Inline', False)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for CssDialog.confirm
        """
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Error on convert')
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            return args[0]
        def mock_get(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_textinput_value = mock_get
        testobj.parent = types.SimpleNamespace(convert_link=mock_convert, xmlfn='path/to/me.html')
        testobj.link_text = ''
        testobj.text_text = ''
        testobj.styledata = 'styledata'
        assert testobj.confirm() == ''
        assert testobj.parent.dialog_data == {'cssdata': 'styledata'}
        assert capsys.readouterr().out == ""
        testobj.styledata = ''
        testobj.cssfilename = ''
        assert testobj.confirm() == 'bestandsnaam opgeven of inline stylesheet definiëren s.v.p'
        assert testobj.parent.dialog_data == {}
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('',)\n")
        testobj.cssfilename = 'xxx'
        testobj.link_text = 'http://'
        assert testobj.confirm() == 'bestandsnaam opgeven of inline stylesheet definiëren s.v.p'
        assert testobj.parent.dialog_data == {}
        assert capsys.readouterr().out == (
                "called AddDialogGui.set_textinput_value with args ('http://', 'xxx')\n"
                "called AddDialogGui.get_textinput_value with args ('http://',)\n")
        testobj.link_text = 'linktext'
        assert testobj.confirm() == 'Error on convert'
        assert testobj.parent.dialog_data == {}
        assert capsys.readouterr().out == (
                "called AddDialogGui.set_textinput_value with args ('linktext', 'xxx')\n"
                "called AddDialogGui.get_textinput_value with args ('linktext',)\n"
                "called Editor.convert_link with args ('linktext', 'path/to/me.html')\n")
        testobj.parent.convert_link = mock_convert_2
        assert testobj.confirm() == ''
        assert testobj.parent.dialog_data == {'rel': 'stylesheet', 'href': 'linktext',
                                              'type': 'text/css'}
        assert capsys.readouterr().out == (
                "called AddDialogGui.set_textinput_value with args ('linktext', 'xxx')\n"
                "called AddDialogGui.get_textinput_value with args ('linktext',)\n"
                "called Editor.convert_link with args ('linktext', 'path/to/me.html')\n"
                "called AddDialogGui.get_textinput_value with args ('',)\n")
        testobj.text_text = 'text_text'
        assert testobj.confirm() == ''
        assert testobj.parent.dialog_data == {'rel': 'stylesheet', 'href': 'linktext',
                                              'type': 'text/css', 'media': 'text_text'}
        assert capsys.readouterr().out == (
                "called AddDialogGui.set_textinput_value with args ('linktext', 'xxx')\n"
                "called AddDialogGui.get_textinput_value with args ('linktext',)\n"
                "called Editor.convert_link with args ('linktext', 'path/to/me.html')\n"
                "called AddDialogGui.get_textinput_value with args ('text_text',)\n")


class TestLinkDialog:
    """unittests for main.LinkDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.LinkDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called LinkDialog.__init__ with args', args)
        monkeypatch.setattr(testee.LinkDialog, '__init__', mock_init)
        testobj = testee.LinkDialog()
        testobj.gui = MockAddGui()
        assert capsys.readouterr().out == ('called LinkDialog.__init__ with args ()\n'
                                           'called AddDialogGui.__init__ with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for LinkDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'AddDialogGui', MockAddGui)
        parent = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.LinkDialog(parent, title='Add Link')
        assert testobj.parent == parent
        assert testobj.link_text == 'text'
        assert testobj.linktxt == ''
        assert testobj.choose_button == '&Browse'
        assert testobj.title_text == 'text'
        assert testobj.text_text == 'text'
        assert capsys.readouterr().out == (
                "called AddDialogGui.__init__ with args"
                f" ({testobj}, 'EditorGui', 'Add Link') {{}}\n"
                "called AddDialogGui.add_content_section\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'link to document:', 0, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                f" ('grid', 0, 1, 'http://') {{'callback': {testobj.set_ltext}}}\n"
                "called AddDialogGui.add_button_line_to_section with args"
                f" ('grid', 1, [('&Browse', {testobj.kies})])\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'descriptive title:', 2, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                " ('grid', 2, 1) {'width': 250}\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'link text:', 3, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                f" ('grid', 3, 1) {{'callback': {testobj.set_ttext}}}\n"
                "called AddDialogGui.add_buttons_to_bottom with args {}\n"
                "called AddDialogGui.set_focus_to with args ('text',)\n")

    def test_kies(self, monkeypatch, capsys):
        """unittest for LinkDialog.kies
        """
        def mock_build(*args):
            print('called Editor.build_mask with args', args)
            return 'mask'
        def mock_ask_open(*args):
            print('called gui.ask_for_open_filename with args', args)
            return ''
        def mock_ask_open_2(*args):
            print('called gui.ask_for_open_filename with args', args)
            return 'xxx'
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(xmlfn='path/to/xxx', build_mask=mock_build)
        testobj.link_text = 'linktext'
        testobj.kies()
        assert capsys.readouterr().out == (
                "called gui.build_mask with args ('html',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, 'path/to/xxx', 'mask')\n")
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open_2)
        testobj.kies()
        assert capsys.readouterr().out == (
                "called gui.build_mask with args ('html',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, 'path/to/xxx', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('linktext', 'xxx')\n")

    def test_set_ltext(self, monkeypatch, capsys):
        """unittest for LinkDialog.set_ltext
        """
        def mock_get(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_textinput_value = mock_get
        testobj.linktxt = 'xxx'
        testobj.link_text = 'link_text'
        testobj.text_text = 'xxx'
        testobj.set_ltext()
        assert testobj.linktxt == 'link_text'
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('link_text',)\n"
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n"
                "called AddDialogGui.set_textinput_value with args ('xxx', 'link_text')\n")

        testobj.linktxt = ''
        testobj.link_text = 'link_text'
        testobj.text_text = 'text_text'
        testobj.set_ltext()
        assert testobj.linktxt == ''
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('link_text',)\n"
                "called AddDialogGui.get_textinput_value with args ('text_text',)\n")

        # testobj.link_text = 'linktxt'  # dit kan niet, moet gelijk zijn aan de meegegeven waarde
        # testobj.linktxt = ''
        # testobj.gui.get_textinput_value = mock_get
        # testobj.title_text = 'xxx'
        # testobj.set_ltext('chgtext')
        # assert testobj.linktxt == 'linktxt'
        # assert capsys.readouterr().out == (
        #         "called AddDialogGui.get_textinput_value with args ('xxx',)\n")
        # testobj.title_text = 'chgtext'
        # testobj.set_ltext('chgtext')
        # assert testobj.linktxt == 'linktxt'
        # assert capsys.readouterr().out == (
        #         "called AddDialogGui.get_textinput_value with args ('chgtext',)\n")
        # testobj.title_text = 'linktxt'
        # testobj.set_ltext('chgtext')
        # assert testobj.linktxt == 'chgtext'
        # assert capsys.readouterr().out == (
        #         "called AddDialogGui.get_textinput_value with args ('linktxt',)\n"
        #         "called AddDialogGui.set_textinput_value with args ('linktxt', 'chgtext')\n")

    def test_set_ttext(self, monkeypatch, capsys):
        """unittest for LinkDialog.set_ttext
        """
        def mock_get(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_textinput_value = mock_get
        testobj.linktxt = 'xxx'
        testobj.text_text = 'text_text'
        testobj.set_ttext()
        assert testobj.linktxt == 'xxx'
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('text_text',)\n")
        testobj.text_text = ''
        testobj.set_ttext()
        assert testobj.linktxt == ''
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('',)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for LinkDialog.confirm
        """
        def mock_get(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Error on convert')
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_textinput_value = mock_get
        testobj.parent = types.SimpleNamespace(convert_link=mock_convert, xmlfn='path/to/me.html')
        testobj.link_text = 'qqq'
        testobj.text_text = ''
        testobj.title_text = 'title'
        assert testobj.confirm() == "Link text is empty"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('',)\n")
        testobj.text_text = 'xxx'
        assert testobj.confirm() == "Error on convert"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n"
                "called AddDialogGui.get_textinput_value with args ('qqq',)\n"
                "called Editor.convert_link with args ('qqq', 'path/to/me.html')\n")
        testobj.parent.convert_link = mock_convert_2
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ['xxx', {'href': 'qqq', 'title': 'title'}]
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n"
                "called AddDialogGui.get_textinput_value with args ('qqq',)\n"
                "called Editor.convert_link with args ('qqq', 'path/to/me.html')\n"
                "called AddDialogGui.get_textinput_value with args ('title',)\n")


class TestImageDialog:
    """unittests for main.ImageDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.ImageDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called ImageDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ImageDialog, '__init__', mock_init)
        testobj = testee.ImageDialog()
        testobj.gui = MockAddGui()
        assert capsys.readouterr().out == ('called ImageDialog.__init__ with args ()\n'
                                           'called AddDialogGui.__init__ with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ImageDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'AddDialogGui', MockAddGui)
        parent = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.ImageDialog(parent, title='Add Image')
        assert testobj.parent == parent
        assert testobj.link_text == 'text'
        assert testobj.linktxt == ''
        assert testobj.choose_button == '&Browse'
        assert testobj.title_text == 'text'
        assert testobj.alt_text == 'text'
        assert capsys.readouterr().out == (
                "called AddDialogGui.__init__ with args"
                f" ({testobj}, 'EditorGui', 'Add Image') {{}}\n"
                "called AddDialogGui.add_content_section\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'link to image:', 0, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                f" ('grid', 0, 1, 'http://') {{'callback': {testobj.set_ltext}}}\n"
                "called AddDialogGui.add_button_line_to_section with args"
                f" ('grid', 1, [('&Browse', {testobj.kies})])\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'descriptive title:', 2, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                " ('grid', 2, 1) {'width': 250}\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'alternate text:', 3, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                f" ('grid', 3, 1) {{'callback': {testobj.set_ttext}}}\n"
                "called AddDialogGui.add_buttons_to_bottom with args {}\n"
                "called AddDialogGui.set_focus_to with args ('text',)\n")

    def test_kies(self, monkeypatch, capsys):
        """unittest for ImageDialog.kies
        """
        def mock_build(*args):
            print('called Editor.build_mask with args', args)
            return 'mask'
        def mock_ask_open(*args):
            print('called gui.ask_for_open_filename with args', args)
            return ''
        def mock_ask_open_2(*args):
            print('called gui.ask_for_open_filename with args', args)
            return 'xxx'
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(xmlfn='path/to/xxx', build_mask=mock_build)
        testobj.link_text = 'linktext'
        testobj.kies()
        assert capsys.readouterr().out == (
                "called gui.build_mask with args ('image',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, 'path/to/xxx', 'mask')\n")
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open_2)
        testobj.kies()
        assert capsys.readouterr().out == (
                "called gui.build_mask with args ('image',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, 'path/to/xxx', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('linktext', 'xxx')\n")

    def test_set_ltext(self, monkeypatch, capsys):
        """unittest for ImageDialog.set_ltext
        """
        def mock_get(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_textinput_value = mock_get
        testobj.linktxt = 'linktxt'
        testobj.link_text = 'link_text'
        testobj.alt_text = 'xxx'
        testobj.set_ltext()
        assert testobj.linktxt == 'linktxt'
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('link_text',)\n"
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n")
        testobj.alt_text = 'linktxt'
        testobj.set_ltext()
        assert testobj.linktxt == 'link_text'
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('link_text',)\n"
                "called AddDialogGui.get_textinput_value with args ('linktxt',)\n"
                "called AddDialogGui.set_textinput_value with args ('linktxt', 'link_text')\n")

    def test_set_ttext(self, monkeypatch, capsys):
        """unittest for ImageDialog.set_ttext
        """
        def mock_get(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_textinput_value = mock_get
        testobj.linktxt = 'linktxt'
        testobj.link_text = 'link_text'
        testobj.alt_text = 'xxx'
        testobj.set_ttext()
        assert testobj.linktxt == 'linktxt'
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('xxx',)\n")
        testobj.alt_text = ''
        testobj.set_ttext()
        assert testobj.linktxt == ''
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('',)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for ImageDialog.confirm
        """
        def mock_get(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Error on convert')
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_textinput_value = mock_get
        testobj.parent = types.SimpleNamespace(convert_link=mock_convert, xmlfn='path/to/file')
        testobj.link_text = 'qqq'
        testobj.alt_text = 'rrr'
        testobj.title_text = 'title'
        assert testobj.confirm() == "Error on convert"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('qqq',)\n"
                "called Editor.convert_link with args ('qqq', 'path/to/file')\n")
        testobj.parent.convert_link = mock_convert_2
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == {'src': 'qqq', 'alt': 'rrr', 'title': 'title'}
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('qqq',)\n"
                "called Editor.convert_link with args ('qqq', 'path/to/file')\n"
                "called AddDialogGui.get_textinput_value with args ('rrr',)\n"
                "called AddDialogGui.get_textinput_value with args ('title',)\n")


class TestVideoDialog:
    """unittests for main.VideoDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.VideoDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called VideoDialog.__init__ with args', args)
        monkeypatch.setattr(testee.VideoDialog, '__init__', mock_init)
        testobj = testee.VideoDialog()
        testobj.gui = MockAddGui()
        assert capsys.readouterr().out == ('called VideoDialog.__init__ with args ()\n'
                                           'called AddDialogGui.__init__ with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for VideoDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'AddDialogGui', MockAddGui)
        parent = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.VideoDialog(parent, title='Add Video')
        assert testobj.parent == parent
        assert testobj.link_text == 'text'
        assert testobj.choose_button == '&Browse'
        assert testobj.hig_text == 'spinner'
        assert testobj.wid_text == 'spinner'
        assert capsys.readouterr().out == (
                "called AddDialogGui.__init__ with args"
                f" ({testobj}, 'EditorGui', 'Add Video') {{}}\n"
                "called AddDialogGui.add_content_section\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'link to video:', 0, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                " ('grid', 0, 1, 'http://') {}\n"
                "called AddDialogGui.add_button_line_to_section with args"
                f" ('grid', 1, [('&Browse', {testobj.kies})])\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'height of video window:', 2, 0)\n"
                "called AddDialogGui.add_spinbox_to_section with args"
                f" ('grid', 2, 1, 1200, 200) {{'callback': {testobj.on_height}}}\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'width of video window:', 3, 0)\n"
                "called AddDialogGui.add_spinbox_to_section with args"
                f" ('grid', 3, 1, 2400, 400) {{'callback': {testobj.on_width}}}\n"
                "called AddDialogGui.add_buttons_to_bottom with args {}\n"
                "called AddDialogGui.set_focus_to with args ('text',)\n")

    def test_kies(self, monkeypatch, capsys):
        """unittest for VideoDialog.kies
        """
        def mock_build(*args):
            print('called Editor.build_mask with args', args)
            return 'mask'
        def mock_ask_open(*args):
            print('called gui.ask_for_open_filename with args', args)
            return ''
        def mock_ask_open_2(*args):
            print('called gui.ask_for_open_filename with args', args)
            return 'xxx'
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(xmlfn='path/to/xxx', build_mask=mock_build)
        testobj.link_text = 'linktext'
        testobj.kies()
        assert capsys.readouterr().out == (
                "called gui.build_mask with args ('video',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, 'path/to/xxx', 'mask')\n")
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open_2)
        testobj.kies()
        assert capsys.readouterr().out == (
                "called gui.build_mask with args ('video',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, 'path/to/xxx', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('linktext', 'xxx')\n")

    def test_on_height(self, monkeypatch, capsys):
        """unittest for VideoDialog.on_height
        """
        def mock_show(*args):
            print('called gui.show_message with args', args)
        def mock_get(*args):
            print('called gui.get_spinbox_value with args', args)
            return value
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_spinbox_value = mock_get
        testobj.hig_text = 'hig_text'
        value = 'number'
        testobj.on_height()
        assert capsys.readouterr().out == (
                "called gui.get_spinbox_value with args ('hig_text',)\n"
                "called gui.show_message with args"
                f" ({testobj.gui}, 'Add Image', 'Number must be numeric integer')\n")
        value = '1'
        testobj.on_height()
        assert capsys.readouterr().out == "called gui.get_spinbox_value with args ('hig_text',)\n"

    def test_on_width(self, monkeypatch, capsys):
        """unittest for VideoDialog.on_width
        """
        def mock_show(*args):
            print('called gui.show_message with args', args)
        def mock_get(*args):
            print('called gui.get_spinbox_value with args', args)
            return value
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_spinbox_value = mock_get
        testobj.wid_text = 'wid_text'
        value = 'number'
        testobj.on_width()
        assert capsys.readouterr().out == (
                "called gui.get_spinbox_value with args ('wid_text',)\n"
                "called gui.show_message with args"
                f" ({testobj.gui}, 'Add Image', 'Number must be numeric integer')\n")
        value = '1'
        testobj.on_width()
        assert capsys.readouterr().out == "called gui.get_spinbox_value with args ('wid_text',)\n"

    def test_confirm(self, monkeypatch, capsys):
        """unittest for VideoDialog.confirm
        """
        # def mock_get(*args):
        #     print('called AddDialogGui.get_textinput_value with args', args)
        #     return args[0]
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Error on convert')
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(convert_link=mock_convert, xmlfn='path/to/file')
        testobj.link_text = 'linktxt'
        testobj.hig_text = '1'
        testobj.wid_text = '1'
        assert testobj.confirm() == "Error on convert"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('linktxt',)\n"
                "called Editor.convert_link with args ('text', 'path/to/file')\n")
        testobj.parent.convert_link = mock_convert_2
        assert testobj.confirm() == ""
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('linktxt',)\n"
                "called Editor.convert_link with args ('text', 'path/to/file')\n"
                "called AddDialogGui.get_spinbox_value with args ('1',)\n"
                "called AddDialogGui.get_spinbox_value with args ('1',)\n")


class TestAudioDialog:
    """unittests for main.AudioDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.AudioDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called AudioDialog.__init__ with args', args)
        monkeypatch.setattr(testee.AudioDialog, '__init__', mock_init)
        testobj = testee.AudioDialog()
        testobj.gui = MockAddGui()
        assert capsys.readouterr().out == ('called AudioDialog.__init__ with args ()\n'
                                           'called AddDialogGui.__init__ with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AudioDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'AddDialogGui', MockAddGui)
        parent = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.AudioDialog(parent, title='Add Audio')
        assert testobj.parent == parent
        assert testobj.link_text == 'text'
        assert testobj.choose_button == '&Browse'
        assert capsys.readouterr().out == (
                "called AddDialogGui.__init__ with args"
                f" ({testobj}, 'EditorGui', 'Add Audio') {{}}\n"
                "called AddDialogGui.add_content_section\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'link to audio fragment:', 0, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                " ('grid', 0, 1, 'http://') {}\n"
                "called AddDialogGui.add_button_line_to_section with args"
                f" ('grid', 1, [('&Browse', {testobj.kies})])\n"
                "called AddDialogGui.add_buttons_to_bottom with args {}\n"
                "called AddDialogGui.set_focus_to with args ('text',)\n")

    def test_kies(self, monkeypatch, capsys):
        """unittest for AudioDialog.kies
        """
        def mock_build(*args):
            print('called Editor.build_mask with args', args)
            return 'mask'
        def mock_ask_open(*args):
            print('called gui.ask_for_open_filename with args', args)
            return ''
        def mock_ask_open_2(*args):
            print('called gui.ask_for_open_filename with args', args)
            return 'xxx'
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(xmlfn='path/to/xxx', build_mask=mock_build)
        testobj.link_text = 'linktext'
        testobj.kies()
        assert capsys.readouterr().out == (
                "called gui.build_mask with args ('audio',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, 'path/to/xxx', 'mask')\n")
        monkeypatch.setattr(testee.gui, 'ask_for_open_filename', mock_ask_open_2)
        testobj.kies()
        assert capsys.readouterr().out == (
                "called gui.build_mask with args ('audio',)\n"
                "called gui.ask_for_open_filename with args"
                f" ({testobj.gui}, 'path/to/xxx', 'mask')\n"
                "called AddDialogGui.set_textinput_value with args ('linktext', 'xxx')\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for AudioDialog.confirm
        """
        # def mock_get(*args):
        #     print('called AddDialogGui.get_textinput_value with args', args)
        #     return args[0]
        def mock_convert(*args):
            print('called Editor.convert_link with args', args)
            raise ValueError('Error on convert')
        def mock_convert_2(*args):
            print('called Editor.convert_link with args', args)
            return args[0]
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(convert_link=mock_convert, xmlfn='path/to/file')
        testobj.link_text = 'linktxt'
        testobj.hig_text = '1'
        testobj.wid_text = '1'
        assert testobj.confirm() == "Error on convert"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('linktxt',)\n"
                "called Editor.convert_link with args ('text', 'path/to/file')\n")
        testobj.parent.convert_link = mock_convert_2
        assert testobj.confirm() == ""
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('linktxt',)\n"
                "called Editor.convert_link with args ('text', 'path/to/file')\n")


class TestListDialog:
    """unittests for main.ListDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.ListDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called ListDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ListDialog, '__init__', mock_init)
        testobj = testee.ListDialog()
        testobj.gui = MockAddGui()
        assert capsys.readouterr().out == ('called ListDialog.__init__ with args ()\n'
                                           'called AddDialogGui.__init__ with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ListDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'AddDialogGui', MockAddGui)
        parent = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.ListDialog(parent, title='Add a List')
        assert testobj.parent == parent
        assert testobj.type_select == 'combobox'
        assert testobj.rows_text == 'spinner'
        assert testobj.list_table == 'table'
        assert capsys.readouterr().out == (
                "called AddDialogGui.__init__ with args"
                f" ({testobj}, 'EditorGui', 'Add a List') {{}}\n"
                "called AddDialogGui.add_content_section\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'choose type of list:', 0, 0)\n"
                "called AddDialogGui.add_combobox_to_section with args"
                " ('grid', 0, 1, ['unordered', 'ordered', 'definition'])"
                f" {{'callback': {testobj.on_type}}}\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'initial number of items:', 1, 0)\n"
                "called AddDialogGui.add_spinbox_to_section with args"
                f" ('grid', 1, 1) {{'startvalue': 1, 'callback': {testobj.on_rows}}}\n"
                "called AddDialogGui.add_table_to_section with args"
                " ('grid', 2, 1, ['list item']) {}\n"
                "called AddDialogGui.add_buttons_to_bottom with args {}\n"
                "called AddDialogGui.set_focus_to with args ('combobox',)\n")

    def test_on_type(self, monkeypatch, capsys):
        """unittest for ListDialog.on_type
        """
        def mock_get_text(*args):
            print('called AddDialogGui.get_conbobox_text with args', args)
            return 'def'
        def mock_get_text_2(*args):
            print('called AddDialogGui.get_conbobox_text with args', args)
            return 'not def'
        def mock_get_count(*args):
            print('called AddDialogGui.get_table_columncount with args', args)
            return 1
        def mock_get_count_2(*args):
            print('called AddDialogGui.get_table_columncount with args', args)
            return 2
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.type_select = 'type'
        testobj.list_table = 'table'
        testobj.gui.get_combobox_text = mock_get_text
        testobj.gui.get_table_columncount = mock_get_count
        testobj.on_type()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_conbobox_text with args ('type',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n"
                "called AddDialogGui.add_table_column with args ('table', 0)\n"
                "called AddDialogGui.set_table_headers with args"
                " ('table', ['term', 'description'], (102, 152))\n")
        testobj.gui.get_combobox_text = mock_get_text_2
        testobj.gui.get_table_columncount = mock_get_count
        testobj.on_type()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_conbobox_text with args ('type',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n")
        testobj.gui.get_combobox_text = mock_get_text
        testobj.gui.get_table_columncount = mock_get_count_2
        testobj.on_type()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_conbobox_text with args ('type',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n")
        testobj.gui.get_combobox_text = mock_get_text_2
        testobj.gui.get_table_columncount = mock_get_count_2
        testobj.on_type()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_conbobox_text with args ('type',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n"
                "called AddDialogGui.remove_table_column with args ('table', 0)\n"
                "called AddDialogGui.set_table_headers with args"
                " ('table', ['list item'], (254,))\n")

    def test_on_rows(self, monkeypatch, capsys):
        """unittest for ListDialog.on_rows
        """
        def mock_get_value(*args):
            print('called AddDialogGui.get_spinbox_value with args', args)
            return args[0]
        def mock_get_rowcount(*args):
            print('called AddDialogGui.get_table_rowcount with args', args)
            return 1
        def mock_show(*args):
            print('called gui.show_message with args', args)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.list_table = 'table'
        testobj.gui.get_spinbox_value = mock_get_value
        testobj.gui.get_table_rowcount = mock_get_rowcount
        testobj.rows_text = 'number'
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('number',)\n"
                "called gui.show_message with args"
                f" ({testobj.gui}, 'Add list', 'Number must be numeric integer')\n")
        testobj.rows_text = '0'
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('0',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.remove_table_row with args ('table', 0)\n")
        testobj.rows_text = '1'
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('1',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n")
        testobj.rows_text = '2'
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('2',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.add_table_row with args ('table', 1)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for ListDialog.confirm
        """
        def mock_get_text(*args):
            print('called AddDialogGui.get_combobox_text with args', args)
            return args[0]
        def mock_get_rowcount(*args):
            print('called AddDialogGui.get_table_rowcount with args', args)
            return 0
        def mock_get_rowcount_2(*args):
            print('called AddDialogGui.get_table_rowcount with args', args)
            return 2
        def mock_get_itemtext(*args):
            print('called AddDialogGui.get_tablecell_itemtext with args', args)
            raise AttributeError
        def mock_get_itemtext_2(*args):
            print('called AddDialogGui.get_tablecell_itemtext with args', args)
            if args[-1] == 0:
                return 'xxx'
            raise AttributeError
        def mock_get_itemtext_3(*args):
            print('called AddDialogGui.get_tablecell_itemtext with args', args)
            return f'item{args[-2]}{args[-1]}'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace()
        testobj.type_select = 'combobox'
        testobj.list_table = 'table'
        testobj.gui.get_combobox_text = mock_get_text
        testobj.gui.get_table_rowcount = mock_get_rowcount
        testobj.gui.get_tablecell_itemtext = mock_get_itemtext
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ('cl', [])
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_combobox_text with args ('combobox',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n")
        testobj.parent.dialog_data = ()
        testobj.gui.get_table_rowcount = mock_get_rowcount_2
        testobj.type_select = 'list'
        assert testobj.confirm() == "Graag nog even het laatste item bevestigen (...)"
        assert testobj.parent.dialog_data == ()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_combobox_text with args ('list',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 0)\n")
        testobj.type_select = 'def'
        testobj.gui.get_tablecell_itemtext = mock_get_itemtext_2
        assert testobj.confirm() == "Graag nog even het laatste item bevestigen (...)"
        assert testobj.parent.dialog_data == ()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_combobox_text with args ('def',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 0)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 1)\n")
        testobj.gui.get_tablecell_itemtext = mock_get_itemtext_3
        testobj.type_select = 'list'
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ('ll', [['item00'], ['item10']])
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_combobox_text with args ('list',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 0)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 1, 0)\n")
        testobj.type_select = 'def'
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ('dl', [['item00', 'item01'], ['item10', 'item11']])
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_combobox_text with args ('def',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 0)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 1)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 1, 0)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 1, 1)\n")


class TestTableDialog:
    """unittests for main.TableDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.TableDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called TableDialog.__init__ with args', args)
        monkeypatch.setattr(testee.TableDialog, '__init__', mock_init)
        testobj = testee.TableDialog()
        testobj.gui = MockAddGui()
        assert capsys.readouterr().out == ('called TableDialog.__init__ with args ()\n'
                                           'called AddDialogGui.__init__ with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TableDialog.__init__
        """
        monkeypatch.setattr(testee.gui, 'AddDialogGui', MockAddGui)
        parent = types.SimpleNamespace(gui='EditorGui')
        testobj = testee.TableDialog(parent, title='Add a Table')
        assert testobj.parent == parent
        assert testobj.headings == ['']
        assert testobj.title_text == 'text'
        assert testobj.rows_text == 'spinner'
        assert testobj.cols_text == 'spinner'
        assert testobj.show_titles == 'checkbox'
        assert testobj.table_table == 'table'
        assert capsys.readouterr().out == (
                "called AddDialogGui.__init__ with args"
                f" ({testobj}, 'EditorGui', 'Add a Table') {{}}\n"
                "called AddDialogGui.add_content_section\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'summary (description):', 0, 0)\n"
                "called AddDialogGui.add_textinput_to_section with args"
                " ('grid', 0, 1) {'width': 250}\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'initial number of rows:', 1, 0)\n"
                "called AddDialogGui.add_spinbox_to_section with args"
                f" ('grid', 1, 1) {{'startvalue': 1, 'callback': {testobj.on_rows}}}\n"
                "called AddDialogGui.add_text_to_section with args"
                " ('grid', 'initial number of columns:', 2, 0)\n"
                "called AddDialogGui.add_spinbox_to_section with args"
                f" ('grid', 2, 1) {{'startvalue': 1, 'callback': {testobj.on_cols}}}\n"
                "called AddDialogGui.add_checkbox_to_section with args"
                " ('grid', 3, 1, 'Show Titles')"
                f" {{'checked': True, 'callback': {testobj.on_check}}}\n"
                "called AddDialogGui.add_table_to_section with args"
                f" ('grid', 4, 1, ['']) {{'callback': {testobj.on_title}}}\n"
                "called AddDialogGui.add_buttons_to_bottom with args {}\n"
                "called AddDialogGui.set_focus_to with args ('text',)\n")

    def test_on_rows(self, monkeypatch, capsys):
        """unittest for TableDialog.on_rows
        """
        def mock_get_value(*args):
            print('called AddDialogGui.get_spinbox_value with args', args)
            return args[0]
        def mock_get_rowcount(*args):
            print('called AddDialogGui.get_table_rowcount with args', args)
            return 1
        def mock_show(*args):
            print('called gui.show_message with args', args)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table_table = 'table'
        testobj.gui.get_spinbox_value = mock_get_value
        testobj.gui.get_table_rowcount = mock_get_rowcount
        testobj.rows_text = 'number'
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('number',)\n"
                "called gui.show_message with args"
                f" ({testobj.gui}, 'Add list', 'Number must be numeric integer')\n")
        testobj.rows_text = '0'
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('0',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.remove_table_row with args ('table', 0)\n")
        testobj.rows_text = '1'
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('1',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n")
        testobj.rows_text = '2'
        testobj.on_rows()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('2',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.add_table_row with args ('table', 1)\n")

    def test_on_cols(self, monkeypatch, capsys):
        """unittest for TableDialog.on_cols
        """
        def mock_get_value(*args):
            print('called AddDialogGui.get_spinbox_value with args', args)
            return args[0]
        def mock_get_colcount(*args):
            print('called AddDialogGui.get_table_columncount with args', args)
            return len(testobj.headings)
        def mock_show(*args):
            print('called gui.show_message with args', args)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table_table = 'table'
        testobj.gui.get_spinbox_value = mock_get_value
        testobj.gui.get_table_columncount = mock_get_colcount
        testobj.cols_text = 'number'
        testobj.headings = ['xx']
        testobj.on_cols()
        assert testobj.headings == ['xx']
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('number',)\n"
                "called gui.show_message with args"
                f" ({testobj.gui}, 'Add list', 'Number must be numeric integer')\n")
        testobj.cols_text = '0'
        testobj.on_cols()
        assert testobj.headings == []
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('0',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n"
                "called AddDialogGui.remove_table_column with args ('table', 0)\n"
                "called AddDialogGui.set_table_headers with args ('table', [], [])\n")
        testobj.headings = ['xx']
        testobj.cols_text = '1'
        testobj.on_cols()
        assert testobj.headings == ['xx']
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('1',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n")
        testobj.headings = ['xx']
        testobj.cols_text = '2'
        testobj.on_cols()
        assert testobj.headings == ['xx', '']
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_spinbox_value with args ('2',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n"
                "called AddDialogGui.add_table_column with args ('table', 1)\n"
                "called AddDialogGui.set_table_headers with args ('table', ['xx', ''], [])\n")

    def test_on_check(self, monkeypatch, capsys):
        """unittest for TableDialog.on_check
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table_table = 'table'
        testobj.show_titles = 'show'
        testobj.on_check()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_checkbox_state with args ('show',)\n"
                "called AddDialogGui.enable_table_header with args ('table', False)\n")

    def test_on_title(self, monkeypatch, capsys):
        """unittest for TableDialog.on_title
        """
        def mock_get(*args):
            print('called AddDialogGui.get_table_column with args', args)
            return 0
        def mock_get_2(*args):
            print('called AddDialogGui.get_table_column with args', args)
            return 1
        def mock_get_3(*args):
            print('called AddDialogGui.get_table_column with args', args)
            return -1
        def mock_ask(*args):
            print('called gui.ask_for_text with args', args)
            return ''
        def mock_ask_2(*args):
            print('called gui.ask_for_text with args', args)
            return 'xxx'
        monkeypatch.setattr(testee.gui, 'ask_for_text', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.table_table = 'table'
        testobj.headings = ['', '']
        testobj.gui.get_table_column = mock_get
        testobj.on_title()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_table_column with args ()\n"
                "called gui.ask_for_text with args"
                f" ({testobj.gui}, 'Add a table', 'Enter a title for this column:')\n")
        testobj.gui.get_table_column = mock_get_2
        testobj.on_title()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_table_column with args ()\n"
                "called gui.ask_for_text with args"
                f" ({testobj.gui}, 'Add a table', 'Enter a title for this column:')\n")
        monkeypatch.setattr(testee.gui, 'ask_for_text', mock_ask_2)
        testobj.on_title()
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_table_column with args ()\n"
                "called gui.ask_for_text with args"
                f" ({testobj.gui}, 'Add a table', 'Enter a title for this column:')\n"
                "called AddDialogGui.set_table_headers with args ('table', ['', 'xxx'], [])\n")
        testobj.gui.get_table_column = mock_get_3
        testobj.on_title()
        assert capsys.readouterr().out == "called AddDialogGui.get_table_column with args ()\n"

    def test_confirm(self, monkeypatch, capsys):
        """unittest for TableDialog.confirm
        """
        def mock_get_text(*args):
            print('called AddDialogGui.get_textinput_value with args', args)
            return args[0]
        def mock_get_rowcount(*args):
            print('called AddDialogGui.get_table_rowcount with args', args)
            return 2
        def mock_get_colcount(*args):
            print('called AddDialogGui.get_table_columncount with args', args)
            return 2
        def mock_get_itemtext(*args):
            print('called AddDialogGui.get_tablecell_itemtext with args', args)
            raise AttributeError
        def mock_get_itemtext_2(*args):
            print('called AddDialogGui.get_tablecell_itemtext with args', args)
            return f'item{args[-2]}{args[-1]}'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace()
        testobj.title_text = 'summary'
        testobj.table_table = 'table'
        testobj.show_titles = 'checkbox'
        testobj.headings = ['xxx', 'yyy']
        testobj.gui.get_textinput_value = mock_get_text
        testobj.gui.get_table_rowcount = mock_get_rowcount
        testobj.gui.get_table_columncount = mock_get_colcount
        testobj.gui.get_tablecell_itemtext = mock_get_itemtext
        assert testobj.confirm() == "Graag nog even het laatste item bevestigen (...)"
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('summary',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 0)\n")
        testobj.gui.get_tablecell_itemtext = mock_get_itemtext_2
        assert testobj.confirm() == ""
        assert testobj.parent.dialog_data == ('summary', False, ['xxx', 'yyy'],
                                              [['item00', 'item01'], ['item10', 'item11']])
        assert capsys.readouterr().out == (
                "called AddDialogGui.get_textinput_value with args ('summary',)\n"
                "called AddDialogGui.get_table_columncount with args ('table',)\n"
                "called AddDialogGui.get_table_rowcount with args ('table',)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 0)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 0, 1)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 1, 0)\n"
                "called AddDialogGui.get_tablecell_itemtext with args ('table', 1, 1)\n"
                "called AddDialogGui.get_checkbox_state with args ('checkbox',)\n")


class TestScrolledTextDialog:
    """unittests for main.ScrolledTextDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.ScrolledTextDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called ScrolledTextDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ScrolledTextDialog, '__init__', mock_init)
        testobj = testee.ScrolledTextDialog()
        assert capsys.readouterr().out == 'called ScrolledTextDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialog.__init__
        """
        class MockGui:
            def __init__(self, *args):
                print('called ScrolledTextDialogGui.__init__ with args', args)
            def add_top_label(self, arg):
                print(f"called ScrolledTextDialogGui.add_top_label with arg '{arg}'")
            def add_text_area(self):
                print('called ScrolledTextDialogGui.add_text_area')
                return 'textfield'
            def close(self):
                print('called ScrolledTextDialogGui.close')
            def add_bottom_buttons(self, *args):
                print('called ScrolledTextDialogGui.add_bottom_buttons with args', args)
            def set_textarea_contents(self, *args):
                print('called ScrolledTextDialogGui.set_textarea_contents with args', args)
        def mock_validate(arg):
            print(f"called Editor.do_validate with arg '{arg}'")
        monkeypatch.setattr(testee.gui, 'ScrolledTextDialogGui', MockGui)
        parent = types.SimpleNamespace(gui='EditorGui', do_validate=mock_validate)
        testobj = testee.ScrolledTextDialog(parent)
        assert capsys.readouterr().out == (
                "called ScrolledTextDialogGui.__init__ with args ('EditorGui', '')\n"
                "called ScrolledTextDialogGui.add_top_label with arg ''\n"
                "called ScrolledTextDialogGui.add_text_area\n"
                "called ScrolledTextDialogGui.add_bottom_buttons with args"
                f" ([('&Done', {testobj.gui.close})],)\n")
        testobj = testee.ScrolledTextDialog(parent, title='xxx', htmlfile='qqq')
        assert capsys.readouterr().out == (
                "called ScrolledTextDialogGui.__init__ with args ('EditorGui', 'xxx')\n"
                "called ScrolledTextDialogGui.add_top_label with arg ''\n"
                "called ScrolledTextDialogGui.add_text_area\n"
                "called ScrolledTextDialogGui.add_bottom_buttons with args"
                f" ([('&Done', {testobj.gui.close}),"
                f" ('&View submitted source', {testobj.show_source})],)\n"
                "called Editor.do_validate with arg 'qqq'\n")
        testobj = testee.ScrolledTextDialog(parent, title='xxx', data='yyy')
        assert capsys.readouterr().out == (
                "called ScrolledTextDialogGui.__init__ with args ('EditorGui', 'xxx')\n"
                "called ScrolledTextDialogGui.add_top_label with arg ''\n"
                "called ScrolledTextDialogGui.add_text_area\n"
                "called ScrolledTextDialogGui.add_bottom_buttons with args"
                f" ([('&Done', {testobj.gui.close})],)\n"
                "called ScrolledTextDialogGui.set_textarea_contents with args"
                " ('textfield', 'yyy')\n")
        testobj = testee.ScrolledTextDialog(parent, title='xxx', fromdisk=True)
        assert capsys.readouterr().out == (
                "called ScrolledTextDialogGui.__init__ with args ('EditorGui', 'xxx')\n"
                "called ScrolledTextDialogGui.add_top_label with arg"
                " 'Validation results are for the file on disk\n"
                "some errors/warnings may already have been corrected by BeautifulSoup\n"
                "(you'll know when they don't show up in the tree or text view\n"
                " or when you save the file in memory back to disk)'\n"
                "called ScrolledTextDialogGui.add_text_area\n"
                "called ScrolledTextDialogGui.add_bottom_buttons with args"
                f" ([('&Done', {testobj.gui.close})],)\n")

    def test_show_source(self, monkeypatch, capsys, tmp_path):
        """unittest for ScrolledTextDialog.show_source
        """
        class MockDialog:
            def __init__(self, *args, **kwargs):
                print('called CodeViewDialog.__init__ with args', args, kwargs)
                self.gui = 'CodeViewDialogGui'
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
        monkeypatch.setattr(testee, 'CodeViewDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        htmlfile = tmp_path / 'text.html'
        htmlfile.write_text('')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.htmlfile = str(htmlfile)
        testobj.show_source()
        assert capsys.readouterr().out == ""
        htmlfile.write_text('xxx\nyyy')
        testobj.show_source()
        assert capsys.readouterr().out == (
                "called CodeViewDialog.__init__ with args"
                f" ({testobj}, 'Submitted source') {{'data': 'xxx\\nyyy'}}\n"
                f"called gui.show_dialog with args ({testobj.dlg},)\n")


class TestCodeViewDialog:
    """unittests for main.CodeViewDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.CodeViewDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called CodeViewDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CodeViewDialog, '__init__', mock_init)
        testobj = testee.CodeViewDialog()
        assert capsys.readouterr().out == 'called CodeViewDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for CodeViewDialog.__init__
        """
        class MockGui:
            def __init__(self, *args):
                print('called CodeViewDialogGui.__init__ with args', args)
            def add_top_message(self, arg):
                print(f"called CodeViewDialogGui.add_top_message with arg '{arg}'")
            def add_content_area(self, arg):
                print(f"called CodeViewDialogGui.add_content_area with arg '{arg}'")
                return 'textfield'
            def add_bottom_button(self):
                print('called CodeViewDialogGui.add_bottom_button')
        monkeypatch.setattr(testee.gui, 'CodeViewDialogGui', MockGui)
        parent = types.SimpleNamespace(gui='EditorGui')
        testee.CodeViewDialog(parent)
        assert capsys.readouterr().out == (
                "called CodeViewDialogGui.__init__ with args ('EditorGui', '')\n"
                "called CodeViewDialogGui.add_top_message with arg ''\n"
                "called CodeViewDialogGui.add_content_area with arg ''\n"
                "called CodeViewDialogGui.add_bottom_button\n")
        testee.CodeViewDialog(parent, title='xxx', caption='yyy', data='zzz', size=(60, 40))
        assert capsys.readouterr().out == (
                "called CodeViewDialogGui.__init__ with args ('EditorGui', 'xxx')\n"
                "called CodeViewDialogGui.add_top_message with arg 'yyy'\n"
                "called CodeViewDialogGui.add_content_area with arg 'zzz'\n"
                "called CodeViewDialogGui.add_bottom_button\n")
