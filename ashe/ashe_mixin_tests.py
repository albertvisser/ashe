from ashe_mixin import getelname, getshortname, getrelativepath

def uitvoeren(dir1, dir2, href):
    print dir1, dir2,
    href = getrelativepath(dir2, dir1)
    try:
        assert href == href
    except AssertionError:
        print "fout"
    else:
        print "ok"
    print href.join(("href was ", "\n"))

def test_getrelativepath():
    "test routine"
    dir1 = 'F:\\gepruts\\htmleditor\\index.html'
    dir2 = href = 'http://www.magiokis.nl/index.html'
    uitvoeren(dir1, dir2, href)

    dir2 = href = 'other.html'
    uitvoeren(dir1, dir2, href)

    dir2 = href = './other.html'
    uitvoeren(dir1, dir2, href)

    dir2 = href = '../other.html'
    uitvoeren(dir1, dir2, href)

    dir2, href = 'F:\\gepruts\\htmleditor\\other.html', 'other.html'
    uitvoeren(dir1, dir2, href)

    dir2 = 'F:\\gepruts\\xhtmleditor\\other.html'
    href = '..\\xhtmleditor\\other.html'
    uitvoeren(dir1, dir2, href)

    dir2 = 'F:\\geprutserd\\htmleditor\\other.html'
    href == '..\\..\\geprutserd\\htmleditor\\other.html'
    uitvoeren(dir1, dir2, href)

    dir2 = 'C:\\gepruts\\htmleditor\\other.html'
    href == 'impossible to create relative link'
    uitvoeren(dir1, dir2, href)

    dir2, href = 'F:\\gepruts\\other.html', '..\\other.html'
    uitvoeren(dir1, dir2, href)

    dir2, href = 'F:\\htmleditor\\other.html', '..\\..\\htmleditor\\other.html'
    uitvoeren(dir1, dir2, href)

    dir2, href = 'F:\\other.html', '..\\..\\other.html'
    uitvoeren(dir1, dir2, href)

    dir1 = 'F:\\gepruts\\index.html'
    dir2 = 'F:\\gepruts\\htmleditor\\other.html'
    href == 'htmleditor\\other.html'
    uitvoeren(dir1, dir2, href)

if __name__ == "__main__":
    ## print getelname("a",{"name": 'Hello', "snork": "hahaha"})
    ## print getshortname("Hee hallo")
    test_getrelativepath()
