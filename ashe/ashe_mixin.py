# -*- coding: utf-8 -*-

"""
GUI-toolkit onafhankelijk gedeelte van mijn op een treeview gebaseerde HTML-editor
Hierin worden een aantal constanten, functies en een mixin class gedefinieerd
"""

import os
import shutil
import subprocess as sp
import linecache
import bs4 as bs # BeautifulSoup as bs

if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True
TITEL = "Albert's Simple HTML-editor"
CMSTART = "<!>"
ELSTART = '<>'
CMELSTART = ' '.join((CMSTART, ELSTART))
DTDSTART = "DOCTYPE"
IFSTART = '!IF'
BL = "&nbsp;"

dtdlist = [
        ['HTML 4.1 Strict',
        """HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd" """],
        ['HTML 4.1 Transitional',
        """HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd" """],
        ['HTML 4.1 Frameset',
        """HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
        "http://www.w3.org/TR/html4/frameset.dtd" """],
        ['', '', ''],
        ['HTML 5', 'html'],
        ['', '', ''],
        ['XHTML 1.0 Strict',
        """html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" """],
        ['XHTML 1.0 Transitional',
        """html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" """],
        ['XHTML 1.0 Frameset',
        """html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd" """],
        ['', '', ''],
        ['XHTML 1.1',
        """html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
        "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" """]
            ]

def getrelativepath(path, refpath):
    """return path made relative to refpath, or empty string

    er is ook een functie os.path.relpath(path [,start])"""
    if path.startswith('./') or path.startswith('../') or os.path.sep not in path:
        return path # already relative
    common = os.path.commonprefix([path, refpath]).rsplit(os.path.sep, 1)[0] + os.path.sep
    if not refpath.startswith(common):
        return '' # 'impossible to create relative link'
    ref = os.path.dirname(refpath.replace(common, ''))
    url = path.replace(common,'')
    if ref:
        for _ in ref.split(os.path.sep):
            url = os.path.join('..', url)
    return url

def getelname(tag, attrs = None, comment = False):
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
    tagattdict = {
        'div': 'class',
        'span': 'class',
        'a': 'title',
        'img': 'alt', # "title',
        'link': 'rel',
        'table': 'summary',
        }
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
    return elname.strip().split()[1]

def getshortname(text, comment = False):
    "shorten name for text node"
    maxlen = 30
    more = '\n' in text
    if more: text = text.split('\n', 1)[0]
    if len(text) > maxlen: text = text[:maxlen] + "..."
    if more: text += ' [+]'
    if comment: text = "<!> " + text
    return text

def escape(text):
    "convert non-ascii characters - not necessary?"
    return text

class EditorMixin(object):
    "mixin class to add gui-independent methods to main frame"

    def getsoup(self, fname = "", preserve = False):
        """build initial html or read from file and initialize tree

        `preserve` anticipates on the possibility to not strip out newlines
        and replace tabs by spaces"""
        if fname:
            try:
                with open(fname) as f_in:
                    data = ''.join([x.strip() for x in f_in])
            except UnicodeDecodeError:
                with open(fname, encoding="iso-8859-1") as f_in:
                    data = ''.join([x.strip() for x in f_in])
            if not preserve:
                data = data.replace('\t',' ')
                data = data.replace('\n','')
            # modify some self-closing tags: to accomodate BS:
            html = data.replace('<br/>','<br />').replace('<hr/>','<hr />')
        else:
            html = '<html><head><title></title></head><body></body></html>'
        try:
            root = bs.BeautifulSoup(html)
        except Exception as err:
            print(err)
            raise
        else:
            self.root = root
            self.xmlfn = fname
            self.init_tree(fname)
        self.advance_selection_on_add = True

    def mark_dirty(self, state):
        self.tree_dirty = state

    def init_tree(self, name = ''):
        """build internal tree representation of the html

        calls gui-specific methods to build the visual structure
        to be overridden with gui-specific method that calls this one
        """
        def add_to_tree(item, node, commented=False):
            """add contents of BeautifulSoup node (`node`) to tree item (`item`)
            `commented` flag is used in building item text"""
            for idx, subnode in enumerate([h for h in node.contents]):
                if isinstance(subnode, bs.Tag):
                    data = subnode.attrs
                    dic = dict(data)
                    for key, value in dic.items():
                        if '%SOUP-ENCODING%' in value:
                            dic[key] = value.replace('%SOUP-ENCODING%',
                                self.root.originalEncoding)
                        elif isinstance(value, list): # hack i.v.m. nieuwe versie
                            dic[key] = ' '.join(value)
                    naam = getelname(subnode.name, dic, commented)
                    newitem = self.addtreeitem(item, naam, dic)
                    add_to_tree(newitem, subnode, commented)
                elif isinstance(subnode, bs.Doctype): # Declaration):
                    dtdtext = ' '.join((DTDSTART, str(subnode))) # [2:-1]
                    self.has_dtd = True
                    newitem = self.addtreeitem(item, getshortname(dtdtext), subnode)
                elif isinstance(subnode, bs.Comment):
                    test = subnode.string
                    if test.lower().startswith('[if'):
                        cond, data = test.split(']>', 1)
                        cond = cond[3:].strip()
                        data, _ = data.rsplit('<![', 1)
                        newitem = self.addtreeitem(item, ' '.join((IFSTART, cond)), '')
                        newnode = bs.BeautifulSoup(data).contents[0].contents[0]
                        add_to_tree(newitem, newnode)
                    else:
                        newnode = bs.BeautifulSoup(test)
                        try:
                            # correct BS wrapping this in <html><body>
                            newnode = newnode.find_all('body')[0]
                        except IndexError:
                            pass
                        ## print(newnode.name)
                        add_to_tree(item, newnode, commented=True)
                else:
                    newitem = self.addtreeitem(item, getshortname(str(subnode),
                        commented), str(subnode))
        self.has_dtd = self.has_stylesheet = False
        if name:
            titel = name
        elif self.xmlfn:
            titel = self.xmlfn
        else:
            titel = '[untitled]'
        self.addtreetop(titel, " - ".join((os.path.basename(titel), TITEL)))
        add_to_tree(self.top, self.root)
        self.mark_dirty(False)

    def soup2file(self, saveas = False):
        if not saveas:
            if os.path.exists(self.xmlfn):
                shutil.copyfile(self.xmlfn, self.xmlfn + '.bak')
        with open(self.xmlfn, "w") as f_out:
            f_out.write(str(self.soup))
        self.mark_dirty(False)

    def edit(self, evt = None):
        "placeholder for gui-specific method"
        pass

    def cut(self, evt = None):
        "cut = copy with removing item from tree"
        self.copy(cut = True)

    def delete(self, evt = None, ifcheck=True):
        "delete = copy with removing item from tree and memory"
        self.copy(cut = True, retain = False, ifcheck=ifcheck)

    def copy(self, evt = None, cut = False, retain = True):
        "placeholder for gui-specific method"
        pass

    def paste(self, evt = None, before = True, below = False):
        "placeholder for gui-specific method"
        pass

    def paste_aft(self, evt = None):
        "paste after instead of before"
        self.paste(before=False)

    def paste_blw(self, evt = None):
        "paste below instead of before"
        self.paste(below=True)

    def insert(self, evt = None, before = True, below = False):
        "placeholder for gui-specific method"
        pass

    def ins_aft(self, evt = None):
        "insert after instead of before"
        self.insert(before=False)

    def ins_chld(self, evt = None):
        "insert belof instead of before"
        self.insert(below=True)

    def add_text(self, evt = None, before = True, below = False):
        "placeholder for gui-specific method"
        pass

    def add_text_aft(self, evt = None):
        "placeholder for gui-specific method"
        self.add_text(before=False)

    def add_textchild(self, evt = None):
        "placeholder for gui-specific method"
        self.add_text(below=True)

    def about(self, evt = None):
        return """\
            Tree-based HTML editor with simultaneous preview

            Started in 2008 by Albert Visser
            Versions for PC and PDA available"""

    def validate(self, htmlfile):
        output = '/tmp/ashe_check'
        with open(output, 'w') as f_out:
            pass
        cmd = 'tidy -e -f "{}" "{}"'.format(output, htmlfile)
        retval = sp.call(cmd, shell=True)
        data = ""
        with open(output) as f_in:
            data = f_in.read()
        return data
