import os
import BeautifulSoup as bs
if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True
TITEL = "Albert's Simple HTML-editor"
ELSTART = '<>'
DTDSTART = "<!DOCTYPE"
BL = "&nbsp;"

def get_html(f=None,preserve=False):
    """preserve anticipates on the possibility to not strip out newlines
    and replace tabs by spaces"""
    if f:
        data = ''.join([x.strip() for x in file(f)])
        if not preserve:
            data = data.replace('\t',' ')
            data = data.replace('\n','')
        # modify some self-closing tags: to accomodate BS:
        html = data.replace('<br/>','<br />').replace('<hr/>','<hr />')
    else:
        html = '<html><head><title></title></head><body></body></html>'
    return html

def getrelativepath(path,refpath):
    if path.startswith('./') or path.startswith('../') or os.path.sep not in path:
        return path
    common = os.path.commonprefix([path,refpath]).rsplit(os.path.sep,1)[0] + os.path.sep
    if not refpath.startswith(common):
        return '' # 'impossible to create relative link'
    ref = os.path.dirname(refpath.replace(common,''))
    url = path.replace(common,'')
    if ref:
        h = ref.split(os.path.sep)
        for j in h:
            url = os.path.join('..',url)
    return url

def getelname(x,y):
    def expand(att):
        try:
            hlp = y[att]
        except:
            return ''
        else:
            return ' %s="%s"' % (att,hlp)
    naam = ' '.join(('<>',x))
    naam += expand('id')
    naam += expand('name')
    if x in ('div', 'span'):
        naam += expand('class')
    elif x in ('a'):
        naam += expand('title')
    elif x in ('img', 'href'):
        naam += expand('alt')
    return naam

def getshortname(x):
    max = 30
    x = x[:max] + "..." if len(x) > max else x
    ## if len(x) > 20:
        ## return x[:20] + "..."
    return x

def escape(text):
    # convert non-ascii characters
    return text
class editormixin(object):
    def init_fn(self):
        if self.xmlfn == '':
            self.rt = bs.BeautifulSoup(get_html()) #,selfClosingTags=SELFCLOSING)
            if DESKTOP:
                ## self.openxml()
                self.init_tree() # tijdens testen even geen open dialoog
            else:
                self.init_tree()
        else:
            self.rt = bs.BeautifulSoup(get_html(self.xmlfn))
            self.init_tree()

    def quit(self):
        pass

    def newxml(self):
        self.rt = bs.BeautifulSoup(get_html()) #,selfClosingTags=SELFCLOSING) # is altijd html
        self.xmlfn = ''
        self.init_tree()

    def openxml(self,ev=None):
        ## em.editormixin.openhtml()
        self.openfile()
        self.init_tree()

    def savexml(self,ev=None):
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.savexmlfile()

    def savexmlas(self):
        pass

    def about(self):
        self.abouttext = "\n".join((
            "Made in 2008 by Albert Visser",
            "Written in PythonCE and PocketPyGui"
            ))

    def openfile(self,h):
        try:
            rt = bs.BeautifulSoup(get_html(h)) #,selfClosingTags=SELFCLOSING)
        except:
            return False
        else:
            self.rt = rt
            self.xmlfn = h
            return True

    def init_tree(self,name=''):
        def add_to_tree(node,hier):
            for x,y in enumerate([h for h in hier.contents]): # if h != '\n']):
                if isinstance(y,bs.Tag): ## if type(y) is types.InstanceType:
                    data = y.attrs
                    dic = dict(data)
                    ## print data,dic
                    naam = getelname(y.name,dic)
                    rr = self.addtreeitem(node,naam,dic)
                    add_to_tree(rr,y)
                elif isinstance(y,bs.Declaration):
                    if y.startswith(DTDSTART):
                        self.hasDTD = True
                    rr = self.addtreeitem(node,getshortname(y),y)
                else:
                    rr = self.addtreeitem(node,getshortname(str(y)),str(y))
        self.hasTD = False
        if name:
            titel = name
        elif self.xmlfn:
            titel = self.xmlfn
        else:
            titel = '[untitled]'
        self.addtreetop(titel," - ".join((os.path.split(titel)[-1],TITEL)))
        add_to_tree(self.top,self.rt)

    def edit(self, ev=None):
        pass

    def cut(self, ev=None):
        self.copy(cut=True)

    def delete(self, ev=None):
        self.copy(cut=True, retain=False)

    def copy(self, ev=None, cut=False):
        pass

    def paste(self, ev=None,before=True,below=False):
        pass

    def paste_aft(self, ev=None):
        self.paste(before=False)

    def paste_blw(self, ev=None):
        self.paste(below=True)

    def insert(self, ev=None,before=True,below=False):
        pass

    def ins_aft(self, ev=None):
        self.insert(before=False)

    def ins_chld(self, ev=None):
        self.insert(below=True)

    def add_text(self, ev=None):
        pass

def test_getrelativepath():
    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'http://www.magiokis.nl/index.html'
    print dir1,dir2,
    href = getrelativepath(dir2,dir1)
    try:
        assert href == 'http://www.magiokis.nl/index.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'other.html'
    print dir1,dir2,
    href = getrelativepath(dir2,dir1)
    try:
        assert href == 'other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = './other.html'
    print dir1,dir2,
    href = getrelativepath(dir2,dir1)
    try:
        assert href == './other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = '../other.html'
    print dir1,dir2,
    href = getrelativepath(dir2,dir1)
    try:
        assert href == '../other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'F:\\gepruts\\htmleditor\\other.html'
    print dir1,dir2,
    href = getrelativepath(dir2,dir1)
    try:
        assert href == 'other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'F:\\gepruts\\xhtmleditor\\other.html'
    print dir1,dir2,
    href = getrelativepath(dir2,dir1)
    try:
        assert href == '..\\xhtmleditor\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'F:\\geprutserd\\htmleditor\\other.html'
    print dir1,dir2,
    href = getrelativepath(dir2,dir1)
    try:
        assert href == '..\\..\\geprutserd\\htmleditor\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = 'C:\\gepruts\\htmleditor\\other.html'
    print dir1,dir2,
    href = getrelativepath(dir2,dir1)
    try:
        assert href == 'impossible to create relative link'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n"))

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 =             'F:\\gepruts\\other.html'
    print dir1,dir2
    href = getrelativepath(dir2,dir1)
    try:
        assert href == '..\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n")) # -> ../..//gepruts/other.html

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 =             'F:\\htmleditor\\other.html'
    print dir1,dir2
    href = getrelativepath(dir2,dir1)
    try:
        assert href == '..\\..\\htmleditor\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n")) # -> ../..//htmleditor/other.html

    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 =                      'F:\\other.html'
    print dir1,dir2
    href = getrelativepath(dir2,dir1)
    try:
        assert href == '..\\..\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n")) #-> ../..///other.html

    dir1 =             'F:\\gepruts\\index.html'
    dir2 = 'F:\\gepruts\\htmleditor\\other.html'
    print dir1,dir2
    href = getrelativepath(dir2,dir1)
    try:
        assert href == 'htmleditor\\other.html'
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ","\n")) # -> ../../gepruts/htmleditor/other.html

if __name__ == "__main__":
    ## print getelname("a",{"name": 'Hello', "snork": "hahaha"})
    ## print getshortname("Hee hallo")
    test_getrelativepath()
