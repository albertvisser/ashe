"""
Hierin worden een aantal constanten, functies en een mixin class gedefinieerd
voor de zaken die gui-toolkit onafhankelijk zijn
"""
import os
import BeautifulSoup as bs
if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True
TITEL = "Albert's Simple HTML-editor"
CMSTART = "<!>"
ELSTART = '<>'
CMELSTART = ' '.join((CMSTART, ELSTART))
DTDSTART = "<!DOCTYPE"
BL = "&nbsp;"

def get_html(fname = None, preserve = False):
    """get html from file

    `preserve` anticipates on the possibility to not strip out newlines
    and replace tabs by spaces"""
    if fname:
        with open(fname) as f_in:
            data = ''.join([x.strip() for x in f_in])
        if not preserve:
            data = data.replace('\t',' ')
            data = data.replace('\n','')
        # modify some self-closing tags: to accomodate BS:
        html = data.replace('<br/>','<br />').replace('<hr/>','<hr />')
    else:
        html = '<html><head><title></title></head><body></body></html>'
    return html

def getrelativepath(path, refpath):
    "return path made relative to refpath, or empty string"
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

def getelname(tag, attrs, comment = False):
    """build name for element node

    precede with <!> and/or <>
    follow with key attribute(s)"""
    tagattdict = {
        'div': 'class',
        'span': 'class',
        'a': 'title',
        'img': 'alt',
        'href': 'alt',
        'link': 'rel',
        }
    def expand(att):
        "return expanded key-attr pair if present otherwise return empty string"
        try:
            hlp = attrs[att]
        except KeyError:
            return ''
        else:
            return ' {}="{}"'.format(att, hlp)
    naam = '{} {}{}{}'.format('<>', tag, expand('id'), expand('name'))
    try:
        naam += expand(tagattdict[tag])
    except KeyError:
        pass
    if comment:
        naam = "<!> " + naam
    return naam

def getshortname(text, comment = False):
    "shorten name for text node"
    maxlen = 30
    text = text[:maxlen] + "..." if len(text) > max else text
    if comment:
        text = "<!> " + text
    return text

def escape(text):
    "convert non-ascii characters - not necessary?"
    return text

class EditorMixin(object):
    "mixin class to add gui-independent methods to main frame"

    def init_fn(self):
        "init file"
        if self.xmlfn == '':
            self.root = bs.BeautifulSoup(get_html())
            if DESKTOP:
                ## self.openxml()
                self.init_tree() # tijdens testen even geen open dialoog
            else:
                self.init_tree()
        else:
            self.root = bs.BeautifulSoup(get_html(self.xmlfn))
            self.init_tree()

    def quit(self, evt = None):
        "generic quit method"
        pass

    def newxml(self, evt = None):
        "new file"
        self.root = bs.BeautifulSoup(get_html())
        self.xmlfn = ''
        self.init_tree()

    def openxml(self, evt = None):
        "open file"
        ## em.editormixin.openhtml()
        self.openfile()
        self.init_tree()

    def reopenxml(self, evt = None):
        "reopen file"
        EditorMixin.openfile(self, self.xmlfn)
        self.init_tree()

    def savexml(self, evt = None):
        "save html to file"
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.savexmlfile()

    def savexmlas(self, evt = None):
        "placeholder for gui-specific method"
        pass

    def about(self, evt = None):
        "wordt niet gebruikt?"
        self.abouttext = "\n".join((
            "Made in 2008 by Albert Visser",
            "Written in PythonCE and PocketPyGui"
            ))

    def openfile(self, fname):
        "to be called from gui-specific method"
        # het onderstaande wordt nergens gebruikt:
        try:
            root = bs.BeautifulSoup(get_html(fname)) # fname was eerst h
        except:
            return False
        else:
            self.root = root
            self.xmlfn = fname
            return True

    def init_tree(self, name = ''):
        "build internal tree representation of the html"
        def add_to_tree(item, node, commented = False):
            """add contents of BeautifulSoup node (`node`) to tree item (`item`)
            `commented` flag is used in building item text"""
            ## print hier
            for idx, subnode in enumerate([h for h in node.contents]): # if h != '\n']):
                ## print idx, subnode
                if isinstance(subnode, bs.Tag):
                    data = subnode.attrs
                    dic = dict(data)
                    ## print data,dic
                    naam = getelname(subnode.name, dic, commented)
                    newitem = self.addtreeitem(item, naam, dic)
                    add_to_tree(newitem, subnode, commented)
                elif isinstance(subnode, bs.Declaration):
                    if subnode.startswith(DTDSTART):
                        self.has_dtd = True
                    newitem = self.addtreeitem(item, getshortname(subnode), subnode)
                    # moet hier niet ook nog add_to_tree op volgen?
                elif isinstance(subnode, bs.Comment):
                    ## print subitem.string
                    newnode = bs.BeautifulSoup(subnode.string)
                    add_to_tree(item, newnode, commented = True)
                else:
                    newitem = self.addtreeitem(item, getshortname(str(subnode),
                        commented), str(subnode))
                    # moet hier niet ook nog add_to_tree op volgen?
        self.has_dtd = False
        if name:
            titel = name
        elif self.xmlfn:
            titel = self.xmlfn
        else:
            titel = '[untitled]'
        self.addtreetop(titel, " - ".join((os.path.split(titel)[-1], TITEL)))
        add_to_tree(self.top, self.root)
        self.tree_dirty = False

    def edit(self, evt = None):
        "placeholder for gui-specific method"
        pass

    def cut(self, evt = None):
        "cut = copy with removing item from tree"
        self.copy(cut = True)

    def delete(self, evt = None):
        "delete = copy with removing item from tree and memory"
        self.copy(cut = True, retain = False)

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

    def add_text(self, evt = None):
        "placeholder for gui-specific method"
        pass

def test_getrelativepath():
    "test routine"
    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'http://www.magiokis.nl/index.html'
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == 'http://www.magiokis.nl/index.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'other.html'
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == 'other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = './other.html'
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == './other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = '../other.html'
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == '../other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'F:\\gepruts\\htmleditor\\other.html'
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == 'other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'F:\\gepruts\\xhtmleditor\\other.html'
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == '..\\xhtmleditor\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'F:\\geprutserd\\htmleditor\\other.html'
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == '..\\..\\geprutserd\\htmleditor\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'C:\\gepruts\\htmleditor\\other.html'
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == 'impossible to create relative link'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 =             'F:\\gepruts\\other.html'
    print dir1, dir2
    href = getrelativepath(dir2, dir1)
    try:
        assert href == '..\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n")) # -> ../..//gepruts/other.html

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 =             'F:\\htmleditor\\other.html'
    print dir1, dir2
    href = getrelativepath(dir2, dir1)
    try:
        assert href == '..\\..\\htmleditor\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n")) # -> ../..//htmleditor/other.html

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 =                      'F:\\other.html'
    print dir1, dir2
    href = getrelativepath(dir2, dir1)
    try:
        assert href == '..\\..\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n")) #-> ../..///other.html

    dir1 =             'F:\\gepruts\\index.html'
    dir2 = 'F:\\gepruts\\htmleditor\\other.html'
    print dir1, dir2
    href = getrelativepath(dir2, dir1)
    try:
        assert href == 'htmleditor\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n")) # -> ../../gepruts/htmleditor/other.html

if __name__ == "__main__":
    ## print getelname("a",{"name": 'Hello', "snork": "hahaha"})
    ## print getshortname("Hee hallo")
    test_getrelativepath()
