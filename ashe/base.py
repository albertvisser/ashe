# -*- coding: utf-8 -*-
"""PyQt5 versie van mijn op een treeview gebaseerde HTML-editor

startfunctie en hoofdscherm
"""
import os
import sys
import pathlib
import bs4 as bs  # BeautifulSoup as bs

import ashe.gui_qt as gui

ICO = str(pathlib.Path(__file__).parent / "ashe.ico")
DESKTOP = True  # was bedoeld om onderscheid te maken met de pythonce versie, nog nodig?
TITEL = "Albert's Simple HTML-editor"
CMSTART = "<!>"
ELSTART = '<>'
CMELSTART = ' '.join((CMSTART, ELSTART))
DTDSTART = "DOCTYPE"
IFSTART = '!IF'
BL = "&nbsp;"
INLINE_1 = 'inline stylesheet'


if __name__ == "__main__":
    ashe_gui(sys.argv)

# shared code
dtdlist = (('HTML 4.1 Strict', 'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN'
            ' http://www.w3.org/TR/html4/strict.dtd" '),
           ('HTML 4.1 Transitional', 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN'
            ' http://www.w3.org/TR/html4/loose.dtd" '),
           ('HTML 4.1 Frameset', 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN'
            ' http://www.w3.org/TR/html4/frameset.dtd" '),
           ('', '', ''),
           ('HTML 5', 'html'),
           ('', '', ''),
           ('XHTML 1.0 Strict', 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN'
            ' http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" '),
           ('XHTML 1.0 Transitional', 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN'
            ' http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" '),
           ('XHTML 1.0 Frameset', 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN'
            ' http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd" '),
           ('', '', ''),
           ('XHTML 1.1', 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN'
            ' http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" '))


class ConversionError(ValueError):
    """project-specific error
    """
    pass


def comment_out(node, commented):
    "subitem(s) (ook) op commentaar zetten"
    for subnode in gui.get_element_children(node):
        txt = gui.get_element_text()
        if commented:
            if not txt.startswith(CMSTART):
                new_text = " ".join((CMSTART, txt)))
        else:
            if txt.startswith(CMSTART):
                new_text(0, txt.split(None, 1)[1])
        gui.set_element_text(subnode, new_text)
        comment_out(subnode, commented)


def is_stylesheet_node(node):
    """determine if node is for stylesheet definition
    """
    if gui.get_element_text(node) == ' '.join((ELSTART, 'link')):
        attrdict = gui.get_element_attrs(node)
        if attrdict.get('rel', '') == 'stylesheet':
            return True
    elif gui.get_element_text(node) == ' '.join((ELSTART, 'style')):
        return True
    return False


def in_body(node):
    """determine if we're in the <body> part
    """
    def is_node_ok(node):
        """check node and parents until body or head tag reached
        """
        if gui.get_element_text(node) == ' '.join((ELSTART, 'body')):
            return True
        elif gui.get_element_text(node) == ' '.join((ELSTART, 'head'))
            return False
        elif gui.get_element_parent(node) is None:  # only for <html> tag - do we need this?
            return False
        return is_node_ok(gui.get_element_parent(node))
    return is_node_ok(node)


def flatten_tree(node, top=True):
    """return the tree's structure as a flat list
    probably nicer as a generator function
    """
    name = gui.get_element_text(node)
    count = 0
    if name.startswith(ELSTART):
        count = 2
    elif name.startswith(CMELSTART):
        count = 3
    if count:
        splits = name.split(None, count)
        name = ' '.join(splits[:count])
    elem_list = [(element, name, gui.get_element_attrs(node))]

    subel_list = []
    for subitem in gui.get_element_children(node):
        text = gui.get_element_text(subitem)
        if text.startswith(ELSTART) or text.startswith(CMELSTART):
            subel_list = flatten_tree(subitem, top=False)
            elem_list.extend(subel_list)
        else:
            elem_list.append((subitem, text, {}))
    if top:
        elem_list = elem_list[1:]
    return elem_list


def convert_link(link, root):
    """attempt to turn the link into one relative to the document
    """
    nice_link = '', ''
    test = link.split('/', 1)
    if not link:
        raise ConversionError("link opgeven of cancel kiezen s.v.p")
    elif not os.path.exists(link):
        nice_link = link
    elif link == '/' or len(test) == 1 or test[0] in ('http://', './', '../'):
        nice_link = link
    else:
        link = os.path.abspath(link)
        if root:
            whereami = os.path.dirname(root)          # os.path.abspath(self._parent.xmlfn)
        else:
            whereami = os.getcwd()                    # os.path.join(os.getcwd(), 'index.html')
        nice_link = os.path.relpath(link, whereami)   # getrelativepath(link, whereami)
    if not nice_link:
        raise ConversionError('Unable to make this local link relative')
    return nice_link


def getelname(tag, attrs=None, comment=False):
    """build name for element node

    precede with <!> and/or <>
    follow with key attribute(s)"""
    def expand(att):
        "return expanded key-attr pair if present otherwise return empty string"
        try:
            hlp = attrs[att]
        except KeyError:
            return ''
        else:
            return ' {}="{}"'.format(att, hlp)
    tagattdict = {'div': 'class',
                  'span': 'class',
                  'a': 'title',
                  'img': 'alt',  # "title',
                  'link': 'rel',
                  'table': 'summary'}
    if attrs is None:
        attrs = {}
    naam = '{} {}{}{}'.format('<>', tag, expand('id'), expand('name'))
    try:
        naam += expand(tagattdict[tag])
    except KeyError:
        pass
    if comment:
        naam = "<!> " + naam
    return naam


def get_tag_from_elname(elname):
    "get first part of node name"
    return elname.strip().split()[1]


def getshortname(text, comment=False):
    "shorten name for text node"
    maxlen = 30
    more = '\n' in text
    if more:
        text = text.split('\n', 1)[0]
    if len(text) > maxlen:
        text = text[:maxlen] + "..."
    if more:
        text += ' [+]'
    if comment:
        text = "<!> " + text
    return text


def escape(text):
    "convert non-ascii characters - not necessary?"
    return text


def find_next(data, search_args, reverse=False, pos=None):
    """searches the flattened tree from start or the given pos
    to find the next item that fulfills the search criteria
    """
    outfile = '/tmp/search_stuff'
    wanted_ele, wanted_attr, wanted_value, wanted_text = search_args
    with open(outfile, 'a') as _o:
        print(search_args, file=_o)
    if pos is None:
        pos = (0, None)
        if reverse:
            pos = (len(data), None)
        with open(outfile, 'a') as _o:
            print(data, file=_o)
    if reverse:
        data.reverse()
    if pos[0]:
        start = len(data) - pos[0] - 1 if reverse else pos[0]
        data = data[start + 1:]

    itemfound = None
    for newpos, data_item in enumerate(data):
        ele_ok = attr_name_ok = attr_value_ok = attr_ok = text_ok = False
        item, element_name, attr_data = data_item

        if element_name.startswith(ELSTART):
            text_ok = True
            ## if not wanted_ele or wanted_ele in element_name.replace(ELSTART, ''):
            if wanted_ele and wanted_ele in element_name.replace(ELSTART, ''):
                ele_ok = True
            for name, value in attr_data.items():
                if not wanted_attr or wanted_attr in name:
                    attr_name_ok = True
                if not wanted_value or wanted_value in value:
                    attr_value_ok = True
                if attr_name_ok and attr_value_ok:
                    attr_ok = True
                    break
            with open(outfile, 'a') as _o:
                print(item.text(0), 'is het niet', file=_o)
        else:
            ele_ok = attr_ok = True
            ## if not wanted_text or wanted_text in element_name:
            if wanted_text and wanted_text in element_name:
                text_ok = True

        with open(outfile, 'a') as _o:
            print(item.text(0), ele_ok, text_ok, attr_ok, file=_o)
        ok = ele_ok and text_ok and attr_ok
        if ok:
            itemfound = item
            break

    if itemfound:
        factor = 1
        if reverse:
            newpos *= - 1
            factor = -1
        if pos[0]:
            pos = newpos + pos[0] + factor
        else:
            pos = newpos + pos[0]
        with open(outfile, 'a') as _o:
            print('return values when found', pos, itemfound, file=_o)
        return pos, itemfound
    return None


class Editor(object):
    "mixin class to add gui-independent methods to main frame"

    def __init__(self, fname=''):
        err = self.getsoup(fname) or ''
        self.title = "(untitled) - Albert's Simple HTML Editor"
        self.tree_dirty = False
        self.xmlfn = fname                                  # ingesteld in getsoup
        self.gui = gui.MainFrame(editor=self, err=err)
        sys.exit(self.gui.app.exec_())

    def mark_dirty(self, state):
        """set "modified" indicator
        """
        self.tree_dirty = state
        self.gui.mark_dirty(self, state)

    def getsoup(self, fname="", preserve=False):  # voor consistentie misschien file2soup
        """build initial html or read from file and initialize tree

        `preserve` anticipates on the possibility to not strip out newlines
        and replace tabs by spaces"""
        if fname:
            # fname = os.path.abspath(os.path.expanduser(fname))
            fpath = pathlib.Path(fname).expanduser().resolve()
            try:
                with fpath.open() as f_in:
                    data = ''.join([x.strip() for x in f_in])
            except FileNotFoundError as err:
                return err
            except UnicodeDecodeError:
                with fpath.open(encoding="iso-8859-1") as f_in:
                    data = ''.join([x.strip() for x in f_in])
            if not preserve:
                data = data.replace('\t', ' ')
                data = data.replace('\n', '')
            # modify some self-closing tags: to accomodate BS:
            html = data.replace('<br/>', '<br />').replace('<hr/>', '<hr />')
        else:
            html = '<html><head><title></title></head><body></body></html>'
        try:
            root = bs.BeautifulSoup(html, 'lxml')
        except Exception as err:
            return err

        self.root = root
        self.xmlfn = fname
        self.init_tree(fname)
        self.advance_selection_on_add = True
        return None

    def init_tree(self, name=''):  # voor consistentie hernoemen naar soup2data
        """build internal tree representation of the html

        calls gui-specific methods to build the visual structure
        to be overridden with gui-specific method that calls this one
        """
        def add_to_tree(item, node, commented=False):
            """add contents of BeautifulSoup node (`node`) to tree item (`item`)
            `commented` flag is used in building item text"""
            for subnode in [h for h in node.contents]:
                if isinstance(subnode, bs.Tag):
                    data = subnode.attrs
                    dic = dict(data)
                    for key, value in dic.items():
                        if '%SOUP-ENCODING%' in value:
                            dic[key] = value.replace('%SOUP-ENCODING%',
                                                     self.root.originalEncoding)
                        elif isinstance(value, list):  # hack i.v.m. nieuwe versie
                            dic[key] = ' '.join(value)
                    naam = getelname(subnode.name, dic, commented)
                    newitem = self.gui.addtreeitem(item, naam, dic)
                    add_to_tree(newitem, subnode, commented)
                elif isinstance(subnode, bs.Doctype):  # Declaration):
                    dtdtext = ' '.join((DTDSTART, str(subnode)))
                    self.has_dtd = True
                    newitem = self.gui.addtreeitem(item, getshortname(dtdtext), subnode)
                elif isinstance(subnode, bs.Comment):
                    test = subnode.string
                    if test.lower().startswith('[if'):
                        cond, data = test.split(']>', 1)
                        cond = cond[3:].strip()
                        data, _ = data.rsplit('<![', 1)
                        newitem = self.gui.addtreeitem(item, ' '.join((IFSTART, cond)), '')
                        newnode = bs.BeautifulSoup(data, 'lxml').contents[0].contents[0]
                        add_to_tree(newitem, newnode)
                    else:
                        newnode = bs.BeautifulSoup(test, 'lxml')
                        try:
                            # correct BS wrapping this in <html><body>
                            newnode = newnode.find_all('body')[0]
                        except IndexError:
                            pass
                        ## print(newnode.name)
                        add_to_tree(item, newnode, commented=True)
                else:
                    newitem = self.gui.addtreeitem(item, getshortname(str(subnode), commented),
                                                   str(subnode))

        self.has_dtd = self.has_stylesheet = False
        if name:
            titel = name
        elif self.xmlfn:
            titel = self.xmlfn
        else:
            titel = '[untitled]'
        self.gui.tree.clear()
        self.gui.addtreetop(titel, " - ".join((os.path.basename(titel), TITEL)))
        add_to_tree(self.top, self.root)
        self.gui.adjust_dtd_menu()
        self.gui.init_tree()
        self.mark_dirty(False)

    def data2soup(self):
        "interne tree omzetten in BeautifulSoup object"
        def expandnode(node, root, data, commented=False):
            "tree item (node) met inhoud (data) toevoegen aan BS node (root)"
            try:
                for att in data:
                    root[str(att)] = str(data[att])
            except TypeError:
                pass
            for elm in self.gui.get_element_children(node):
                text = self.gui.get_element_text(elm)
                data = self.gui.get_element_attrs(elm)
                if text.startswith(ELSTART) or text.startswith(CMELSTART):
                    # data is een dict: leeg of een mapping van data op attributen
                    if text.startswith(CMSTART):
                        text = text.split(None, 1)[1]
                        if not commented:
                            is_comment = True
                            soup = bs.BeautifulSoup('', 'lxml')
                            sub = soup.new_tag(text.split()[1])
                            expandnode(elm, sub, data, is_comment)
                            sub = bs.Comment(str(sub))  # .decode("utf-8")) niet voor Py3
                        else:
                            is_comment = False
                            sub = self.soup.new_tag(text.split()[1])
                    else:
                        is_comment = False
                        sub = self.soup.new_tag(text.split()[1])
                    root.append(sub)  # insert(0,sub)
                    if not is_comment:
                        expandnode(elm, sub, data, commented)
                elif text.startswith(DTDSTART):
                    text = text.split(None, 1)[1]
                    sub = bs.Doctype(data)
                    root.append(sub)
                elif text.startswith(IFSTART):
                    # onthou conditie
                    cond = text.split(None, 1)[1]
                    text = ''
                    # onderliggende elementen langslopen
                    for subel in self.gui.get_element_children(elm):
                        subtext = self.gui.get_element_text(subel)
                        data = self.gui.get_element_attrs(subel)
                        if subtext.startswith(ELSTART):
                            # element in tekst omzetten en deze aan text toevoegen
                            onthou = self.soup
                            self.soup = bs.BeautifulSoup('', 'lxml')
                            tag = self.soup.new_tag(subtext.split()[1])
                            expandnode(subel, tag, data)
                            text += str(tag)
                            self.soup = onthou
                        else:
                            # tekst aan text toevoegen
                            text += str(data)
                    # complete tekst als commentaar element aan de soup toevoegen
                    sub = bs.Comment('[if {}]>{}<![endif]'.format(cond, text))
                    root.append(sub)
                else:
                    sub = bs.NavigableString(str(data))  # .decode("utf-8")) niet voor Py3
                    if text.startswith(CMSTART) and not commented:
                        sub = bs.Comment(data)  # .decode("utf-8")) niet voor Py3
                    root.append(sub)  # data.decode("latin-1")) # insert(0,sub)
        self.soup = bs.BeautifulSoup('', 'lxml')  # self.root.originalEncoding)
        for tag in self.gui.get_element_children(self.top):
            text = self.gui.get_element_text(tag)
            data = self.gui.get_element_attrs(tag)
            if text.startswith(DTDSTART):
                root = bs.Doctype(str(data))  # Declaration(str(data))
                self.soup.append(root)
            elif text.startswith(ELSTART):
                root = self.soup.new_tag(text.split(None, 2)[1])
                self.soup.append(root)
                expandnode(tag, root, data)

    def soup2file(self, saveas=False):
        "write HTML to file"
        if not saveas:
            if os.path.exists(self.xmlfn):
                shutil.copyfile(self.xmlfn, self.xmlfn + '.bak')
        with open(self.xmlfn, "w") as f_out:
            f_out.write(str(self.soup))
        self.mark_dirty(False)

    def newxml(self):
        pass

    def openxml(self):
        pass

    def savexml(self):
        pass

    def savexmlas(self):
        pass

    def reopenxml(self):
        pass

    def close(self):
        pass

    def expand(self):
        pass

    def collapse(self):
        pass

    def advance_selection_onoff(self):
        pass

    def refresh_preview(self):
        pass

    def edit(self):
        "placeholder for gui-specific method"
        pass

    def comment(self):
        pass

    def make_conditional(self):
        pass

    def remove_condition(self):
        pass

    def _copy(self, cut=False, retain=True, ifcheck=True):
        "call gui-specific method"
        self.gui.do_copy(cut, retain, ifcheck)

    def cut(self):
        "cut = copy with removing item from tree"
        self._copy(cut=True)

    def delete(self, ifcheck=True):
        "delete = copy with removing item from tree and memory"
        self._copy(cut=True, retain=False, ifcheck=ifcheck)

    def copy(self):
        "copy = transfer item to memory"
        self._copy()

    def _paste(self, before=True, below=False):
        "call gui-specific method"
        self.gui.do_paste(before, below)

    def paste_after(self):
        "paste after instead of before"
        self._paste(before=False)

    def paste_below(self):
        "paste below instead of before"
        self._paste(below=True)

    def paste(self):
        "paste before"
        self._paste()

    def _insert(self, before=True, below=False):
        "call gui-specific method"
        self.gui.do_insert(before, below)

    def insert(self):
        "insert element before"
        self._insert(below=True)

    def insert_after(self):
        "insert element after instead of before"
        self._insert(before=False)

    def insert_child(self):
        "insert element below instead of before"
        self._insert()

    def _add_text(self, before=True, below=False):
        "call gui-specific method"
        self.gui.do_add_text(before, below)

    def add_text(self):
        "insert text before"
        self._add_text()

    def add_text_after(self):
        "insert text after instead of before"
        self._add_text(before=False)

    def add_textchild(self):
        "insert text below instead of before"
        self._add_text(below=True)

    def search(self):
        pass

    def search_last(self):
        pass

    def search_next(self):
        pass

    def search_prev(self):
        pass

    def add_dtd(self):
        pass

    def add_css(self):
        pass

    def add_link(self):
        pass

    def add_image(self):
        pass

    def add_audio(self):
        pass

    def add_video(self):
        pass

    def add_list(self):
        pass

    def add_table(self):
        pass

    def validate(self, htmlfile):
        """validate HTML source
        """
        output = '/tmp/ashe_check'
        sp.run(['tidy', '-e', '-f', output, htmlfile])
        data = ""
        with open(output) as f_in:
            data = f_in.read()
        return data

    def view_code(self):
        "start source viewer"
        self.data2soup()
        self.gui.show_code("Source view", "Let op: de tekst wordt niet ververst"
                             " bij wijzigingen in het hoofdvenster", self.soup.prettify()

    def about(self):
        "get info about the application"
        self.gui.about("""\
            Tree-based HTML editor with simultaneous preview

            Started in 2008 by Albert Visser
            Versions for PC and PDA available""")

