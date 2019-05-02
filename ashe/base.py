"""Dit is mijn op een treeview gebaseerde HTML-editor

nieuwe aanpak: de GUI routines worden van hieruit aangeroepen zodat alle business logica hier
blijft
"""
import os
# import sys
import shutil
import pathlib
import subprocess
import bs4 as bs  # BeautifulSoup as bs
try:
    import cssedit.editor.csseditor_qt as csed
    cssedit_available = True
except ImportError:
    cssedit_available = False

from ashe.gui import gui
from ashe.shared import ICO, TITEL, CMSTART, ELSTART, DTDSTART, IFSTART, BL
CMELSTART = ' '.join((CMSTART, ELSTART))


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


class CssManager:
    """shared interface from Edit Element Dialog with css editor
    """
    def __init__(self, parent):
        self._parent = parent
        self.styledata = ''

    def setup_flags(self, styledata, is_stylesheet):
        "set up shared state"
        self.old_styledata = styledata
        self.is_stylesheet = is_stylesheet

    # def setup_flags(self, tag, attrs):
    #     """initialize shared state
    #     """
    #     self.old_styledata = ''
    #     self.is_stylesheet = has_style = iscomment = False
    #     if tag:
    #         x = tag.split(None, 1)
    #         if x[0] == CMSTART:
    #             iscomment = True
    #             x = x[1].split(None, 1)
    #         if x[0] == ELSTART:
    #             x = x[1].split(None, 1)
    #         origtag = x[0]
    #     else:
    #         origtag = tag
    #     if attrs:
    #         for attr, value in attrs.items():
    #             if attr == 'styledata':
    #                 self.old_styledata = value
    #                 continue
    #             elif origtag == 'link' and attr == 'rel' and value == 'stylesheet':
    #                 self.is_stylesheet = True
    #             elif attr == 'style':
    #                 has_style = True
    #                 self.old_styledata = value
    #     if origtag == 'style':  # is_style_tag:
    #         text = '&Edit styles'
    #     elif self.is_stylesheet:
    #         text = '&Edit linked stylesheet'
    #     elif has_style:
    #         text = '&Edit inline style'
    #     else:
    #         text = '&Add inline style'
    #     return origtag, iscomment, has_style, text

    def call_editor(self, tag, fname, app=None):
        """call external css editor from the edit element dialog
        """
        if not self.is_stylesheet:
            css = csed.MainWindow(self, app=app)     # calling the editor
            # with this class as parent should make sure we get the css back as an attribute
            if tag == 'style':
                css.open(text=self.old_styledata)
            else:
                css.open(tag=tag, text=self.old_styledata)
            css.show_from_external()  # sets self.styledata right before closing
            return
        print("started cssedit main window")
        mld = ''
        if not fname:
            mld = 'Please enter a link address first'
        elif fname.startswith('/'):
            mld = "Cannot determine file system location of stylesheet file"
        else:
            if fname.startswith('http'):
                h_fname = os.path.join('/tmp', 'ashe_{}'.format(os.path.basename(fname)))
                subprocess.run(['wget', fname, '-O', h_fname])
                fname = h_fname
            else:
                h_fname = fname
                xmlfn_path = pathlib.Path(self._parent.xmlfn)
                while h_fname.startswith('../'):
                    h_fname = h_fname[3:]
                    xmlfn_path = xmlfn_path.parent
                fname = str(xmlfn_path / h_fname)
            print('constructed filename:', fname)
            self.styledata = self.old_styledata
            try:
                css = csed.MainWindow(app=self._parent.app)
                css.open(filename=fname)
            except Exception as e:
                mld = str(e)
            else:
                css.show_from_external()
        if mld:
            self._parent.gui.meld(mld)

    def check_if_modified(self, tag, attrs):
        """compare with original state saved in setup_flags
        """
        try:
            self.styledata = self.styledata.decode()
        except AttributeError:
            pass
        if self.styledata != self.old_styledata:
            self.old_styledata = self.styledata
        if tag == 'style':
            attrs['styledata'] = self.old_styledata
        else:
            if self.old_styledata:
                attrs['style'] = self.old_styledata
        return self.styledata, attrs

    def call_from_inline(self, win, text):
        """edit from CSS Dialog
        """
        win.dialog_data = {"type": 'text/css'}
        if text:
            win.dialog_data["media"] = text
        css = csed.MainWindow(self, self._parent.app)
        css.open(text="")
        css.show_from_external()
        return win.dialog_data


class Editor(object):
    "Gui-independent start of application"
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

    def __init__(self, fname=''):
        self.title = "(untitled) - Albert's Simple HTML Editor"
        self.constants = {'ELSTART': ELSTART}
        self.tree_dirty = False
        self.xmlfn = fname
        self.cssedit_available = cssedit_available
        self.search_args = []
        self.gui = gui.MainFrame(editor=self, icon=ICO)
        self.cssm = CssManager(self) if cssedit_available else None
        err = self.getsoup(self.xmlfn) or ''
        if err:
            self.gui.meld(str(err))
        else:
            self.refresh_preview()
        self.gui.go()

    def mark_dirty(self, state):
        """set "modified" indicator
        """
        self.tree_dirty = state
        title = self.gui.get_screen_title()
        test = ' - ' + self.title
        test2 = '*' + test
        if state:
            if test2 not in title:
                title = title.replace(test, test2)
        else:
            title = title.replace(test2, test)
        self.gui.set_screen_title(title)

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
        self.init_tree()
        self.advance_selection_on_add = True
        return None

    def init_tree(self, name='', message=''):  # voor consistentie hernoemen naar soup2data
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
        self.gui.addtreetop(titel, " - ".join((os.path.basename(titel), TITEL)))
        add_to_tree(self.gui.top, self.root)
        self.gui.adjust_dtd_menu()
        self.gui.init_tree(message)
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
                data = self.gui.get_element_data(elm)
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
        for tag in self.gui.get_element_children(self.gui.top):
            text = self.gui.get_element_text(tag)
            data = self.gui.get_element_data(tag)
            if text.startswith(DTDSTART):
                root = bs.Doctype(str(data))  # Declaration(str(data))
                self.soup.append(root)
            elif text.startswith(ELSTART):
                root = self.soup.new_tag(text.split(None, 2)[1])
                self.soup.append(root)
                expandnode(tag, root, data)
        return self.soup

    def soup2file(self, saveas=False):
        "write HTML to file"
        if not saveas:
            if os.path.exists(self.xmlfn):
                shutil.copyfile(self.xmlfn, self.xmlfn + '.bak')
        with open(self.xmlfn, "w") as f_out:
            f_out.write(str(self.soup))
        self.mark_dirty(False)

    def check_tree_state(self):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)
        retourneert 1 = Yes, 0 = No, -1 = Cancel
        """
        if self.tree_dirty:
            text = "HTML data has been modified - save before continuing?"
            retval = self.gui.ask_how_to_continue(self.title, text)
            if retval > 0:
                self.savexml()
            return retval
        return None

    def get_menulist(self):
        """menu definition
        """
        return (('&File', (('&New', 'N', 'C', "Start a new HTML document", self.newxml),
                           ('&Open', 'O', 'C', "Open an existing HTML document", self.openxml),
                           ('&Save', 'S', 'C', "Save the current document", self.savexml),
                           ('Save &As', 'S', 'SC', "Save the current document under a different "
                            "name", self.savexmlas),
                           ('&Revert', 'R', 'C', "Discard all changes since the last save",
                            self.reopenxml),
                           ('sep1', ),
                           ('E&xit', 'Q', 'C', 'Quit the application', self.close))),
                ('&View', (('E&xpand All (sub)Levels', '+', 'C', "Show what's beneath "
                            "the current element", self.expand, True),
                           ('&Collapse All (sub)Levels', '-', 'C', "Hide what's beneath "
                            "the current element", self.collapse, True),
                           ('sep1', ),
                           ('Advance selection on add/insert', '', '', "Move the selection to the "
                            "added/pasted item", self.advance_selection_onoff),
                           ('sep2', ),
                           ('&Resync preview', 'F5', '', 'Reset the preview window to the '
                            'contents of the treeview', self.refresh_preview))),
                ('&Edit', (('Edit', 'F2', '', 'Modify the element/text and/or its attributes',
                            self.edit),
                           ('Comment/Uncomment', '#', 'C', 'Comment (out) the current item and '
                            'everything below', self.comment),
                           ('Add condition', '', '', 'Put a condition on showing the current '
                            'item', self.make_conditional),
                           ('Remove condition', '', '', 'Remove this condition from the '
                            'elements below it', self.remove_condition),
                           ('sep1', ),
                           ('Cut', 'X', 'C', 'Copy and delete the current element', self.cut),
                           ('Copy', 'C', 'C', 'Copy the current element', self.copy),
                           ('Paste Before', 'V', 'SC', 'Paste before of the current element',
                            self.paste),
                           ('Paste After', 'V', 'CA', 'Paste after the current element',
                            self.paste_after),
                           ('Paste Under', 'V', 'C', 'Paste below the current element',
                            self.paste_below),
                           ('sep2', ),
                           ('Delete', 'Del', '', 'Delete the current element', self.delete),
                           ('Insert Text (under)', 'Ins', 'S', 'Add a text node under the current '
                            'one', self.add_textchild),
                           ('Insert Text before', 'Ins', 'SC', 'Add a text node before the current'
                            ' one', self.add_text),
                           ('Insert Text after', 'Ins', 'SA', 'Add a text node after the current '
                            'one', self.add_text_after),
                           ('Insert Element Before', 'Ins', 'C', 'Add a new element in front of '
                            'the current', self.insert),
                           ('Insert Element After', 'Ins', 'A', 'Add a new element after the '
                            'current', self.insert_after),
                           ('Insert Element Under', 'Ins', '', 'Add a new element under the '
                            'current', self.insert_child))),
                ('&Search', (("&Find", 'F', 'C', 'Open dialog to specify search and find first',
                              self.search),
                             ## ("&Replace", 'H', 'C', 'Search and replace', self.replace),
                             ("Find &Last", 'F', 'SC', 'Find last occurrence of search argument',
                              self.search_last),
                             ("Find &Next", 'F3', '', 'Find next occurrence of search argument',
                              self.search_next),
                             ("Find &Previous", 'F3', 'S', 'Find previous occurrence of search '
                              'argument', self.search_prev))),
                ("&HTML", (('Add &DTD', '', '', 'Add a document type description', self.add_dtd),
                           ('Add &Stylesheet', '', '', 'Add a stylesheet', self.add_css),
                           ('sep1', ),
                           ('Create &link (under)', '', '', 'Add a document reference',
                            self.add_link),
                           ('Add i&mage (under)', '', '', 'Include an image', self.add_image),
                           ('Add v&ideo (under)', '', '', 'Add a video element', self.add_video),
                           ('Add a&udio (under)', '', '', 'Add an audio fragment', self.add_audio),
                           ('sep1', ),
                           ('Add l&ist (under)', '', '', 'Create a list', self.add_list),
                           ('Add &table (under)', '', '', 'Create a table', self.add_table),
                           ('sep3', ),
                           ('&View code', '', '', 'Shows the html pretty-printed', self.view_code),
                           ('&Check syntax', '', '', 'Validate HTML with Tidy', self.validate))),
                ("Help", (('&About', '', '', 'Info about this application', self.about), )))

    def is_stylesheet_node(self, node):
        """determine if node is for stylesheet definition
        """
        test = self.gui.get_element_text(node)
        if test == ' '.join((ELSTART, 'link')):
            attrdict = self.gui.get_element_data(node)
            if attrdict.get('rel', '') == 'stylesheet':
                return True
        elif test == ' '.join((ELSTART, 'style')):
            return True
        return False

    def in_body(self, node):
        """determine if we're in the <body> part
        """
        def is_node_ok(node):
            """check node and parents until body or head tag reached
            """
            test = self.gui.get_element_text(node)
            parent = self.gui.get_element_parent(node)
            if test == ' '.join((ELSTART, 'body')):
                return True
            elif test == ' '.join((ELSTART, 'head')):
                return False
            elif parent is None:  # only for <html> tag - do we need this?
                return False
            return is_node_ok(parent)
        return is_node_ok(node)

    def flatten_tree(self, node, top=True):
        """return the tree's structure as a flat list
        probably nicer as a generator function
        """
        name = self.gui.get_element_text(node)
        count = 0
        if name.startswith(ELSTART):
            count = 2
        elif name.startswith(CMELSTART):
            count = 3
        if count:
            splits = name.split(None, count)
            name = ' '.join(splits[:count])
        elem_list = [(node, name, self.gui.get_element_data(node))]

        subel_list = []
        for subitem in self.gui.get_element_children(node):
            text = self.gui.get_element_text(subitem)
            if text.startswith(ELSTART) or text.startswith(CMELSTART):
                subel_list = self.flatten_tree(subitem, top=False)
                elem_list.extend(subel_list)
            else:
                elem_list.append((subitem, text, {}))
        if top:
            elem_list = elem_list[1:]
        return elem_list

    def newxml(self, event=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna nieuwe html aanmaken"""
        if self.check_tree_state() != -1:
            err = self.getsoup()
            if err:
                self.gui.meld(str(err))
            else:
                self.init_tree(message='started new document')
                self.refresh_preview()

    def openxml(self, event=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna een html bestand kiezen"""
        if self.check_tree_state() != -1:
            fnaam = self.gui.ask_for_open_filename()
            if fnaam:
                err = self.getsoup(fname=str(fnaam))
                if err:
                    self.gui.meld(str(err))
                else:
                    self.init_tree(fnaam, 'loaded {}'.format(fnaam))  # self.xmlfn
                    self.refresh_preview()

    def savexml(self, event=None):
        "save html to file"
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.data2soup()
            try:
                self.soup2file()
            except IOError as err:
                self.gui.meld(str(err))
                return
            self.gui.show_statusbar_message("saved {}".format(self.xmlfn))

    def savexmlas(self, event=None):
        """vraag bestand om html op te slaan
        bestand opslaan en naam in titel en root element zetten"""
        fname = self.gui.ask_for_save_filename()
        if fname:
            self.xmlfn = fname
            self.data2soup()
            try:
                self.soup2file(saveas=True)
            except IOError as err:
                self.gui.meld(str(err))
                return
            self.gui.set_element_text(self.gui.top, self.xmlfn)
            self.gui.show_statusbar_message("saved as {}".format(self.xmlfn))

    def reopenxml(self, event=None):
        """onvoorwaardelijk html bestand opnieuw laden"""
        ret = self.getsoup(fname=self.xmlfn)
        if ret:
            self.gui.meld(str(ret))
        else:
            self.init_tree(self.xmlfn, 'reloaded {}'.format(self.xmlfn))
            self.refresh_preview()

    def close(self, event=None):
        """kijken of er wijzigingen opgeslagen moeten worden -  daarna afsluiten
        """
        if self.check_tree_state() != -1:
            self.gui.close()

    def expand(self, event=None):
        "expandeer tree vanaf huidige item"
        self.gui.expand()

    def collapse(self, event=None):
        "collapse huidige item en daaronder"
        self.gui.collapse()

    def advance_selection_onoff(self, event=None):
        "callback for menu option"
        self.advance_selection_on_add = self.gui.get_adv_sel_setting()

    def refresh_preview(self, event=None):
        "update display"
        self.gui.refresh_preview(self.data2soup())

    def checkselection(self):
        "controleer of er wel iets geselecteerd is (behalve de filenaam)"
        sel = True
        self.item = self.gui.get_selected_item()
        if self.item is None or self.item == self.gui.top:
            self.gui.meld('You need to select an element or text first')
            sel = False
        return sel

    def edit(self, event=None):
        "start edit m.b.v. dialoog"
        if not self.checkselection():
            return
        data = self.gui.get_element_text(self.item)
        test = self.gui.get_element_children(self.item)
        if test:
            style_item = test[0]
        if data.startswith(DTDSTART):
            data = self.gui.get_element_data(self.item)
            prefix = 'HTML PUBLIC "-//W3C//DTD'
            if data.upper().startswith(prefix):
                data = data.upper().replace(prefix, '')
                text = 'doctype is ' + data.split('//EN')[0].strip()
            elif data.strip().lower() == 'html':
                text = 'doctype is HTML 5'
            else:
                text = 'doctype cannot be determined'
            self.gui.meld(text)
            return
        elif data.startswith(IFSTART):
            self.gui.meld("About to edit this conditional")
            # start dialog to edit condition
            cond, ok = self.gui.ask_for_text(data)
            # if confirmed: change element
            if ok:
                self.gui.meld("changing to " + str(cond))
                # nou nog echt doen (of gebeurt dat in de dialoog? dacht het niet)
            return
        under_comment = self.gui.get_element_text(
            self.gui.get_element_parent(self.item)).startswith(CMELSTART)
        modified = False
        if data.startswith(ELSTART) or data.startswith(CMELSTART):
            oldtag = get_tag_from_elname(data)
            attrdict = self.gui.get_element_data(self.item)
            if oldtag == 'style':
                attrdict['styledata'] = self.gui.get_element_attrs(style_item)
            was_commented = data.startswith(CMSTART)
            ok, dialog_data = self.gui.do_edit_element(data, attrdict)
            print(ok, dialog_data)
            if ok:
                modified = True
                tag, attrs, commented = dialog_data
                if under_comment:
                    commented = True
                if tag == 'style':
                    # style data zit in attrs['styledata'] en moet naar tekst element onder tag
                    newtext = str(attrs.pop('styledata', ''))  # en daarna moet deze hier weg
                    oldtext = self.gui.get_element_data(style_item)
                    if newtext != oldtext:
                        self.gui.set_element_text(style_item, getshortname(newtext))
                        self.gui.set_element_data(style_item, newtext)
                attrdict.pop('styledata', '')
                if tag != oldtag or attrs != attrdict:
                    self.gui.set_element_text(self.item, getelname(tag, attrs, commented))
                self.gui.set_element_data(self.item, attrs)
                if commented != was_commented:
                    self.comment_out(self.item, commented)
        else:
            txt = CMSTART + " " if data.startswith(CMSTART) else ""
            data = self.gui.get_element_data(self.item)
            test = self.gui.get_element_text(self.gui.get_element_parent(self.item))
            if test in (' '.join((ELSTART, 'style')), ' '.join((CMELSTART, 'style'))):
                self.gui.meld("Please edit style through parent tag")
                return
            ok, dialog_data = self.gui.do_edit_textvalue(txt + data)
            print(ok, dialog_data)
            if ok:
                modified = True
                txt, commented = dialog_data
                if under_comment:
                    commented = True
                self.gui.set_element_text(self.item, getshortname(txt, commented))
                self.gui.set_element_data(self.item, txt)
        if modified:
            self.mark_dirty(True)
            self.refresh_preview()

    def comment(self, event=None):
        "(un)comment zonder de edit dialoog"
        if not self.checkselection():
            return
        tag = self.gui.get_element_text(self.item)
        attrs = self.gui.get_element_data(self.item)
        commented = tag.startswith(CMSTART)
        if commented:
            _, tag = tag.split(None, 1)  # CMSTART eraf halen
        under_comment = self.gui.get_element_text(
            self.gui.get_element_parent(self.item)).startswith(CMELSTART)
        commented = not commented  # het (un)commenten uitvoeren
        if under_comment:
            commented = True
        if tag.startswith(ELSTART):
            _, tag = tag.split(None, 1)  # ELSTART eraf halen
            self.gui.set_element_text(self.item, getelname(tag, attrs, commented))
            self.gui.set_element_data(self.item, attrs)
            self.comment_out(self.item, commented)
        else:
            self.gui.set_element_text(self.item, commented)
            self.gui.set_element_data(self.item, tag)
        self.refresh_preview()

    def comment_out(self, node, commented):
        "subitem(s) (ook) op commentaar zetten"
        for subnode in self.gui.get_element_children(node):
            txt = self.gui.get_element_text(subnode)
            if commented:
                if not txt.startswith(CMSTART):
                    new_text = " ".join((CMSTART, txt))
            else:
                if txt.startswith(CMSTART):
                    new_text = txt.split(None, 1)[1]
            self.gui.set_element_text(subnode, new_text)
            self.comment_out(subnode, commented)

    def make_conditional(self, event=None):
        "zet een IE conditie om het element heen"
        if not self.checkselection():
            return
        text = self.gui.get_element_text(self.item)
        if text.startswith(IFSTART):
            self.gui.meld("This is already a conditional")
            return
        # ask for the condition
        cond = self.gui.ask_for_condition()
        if cond:
            # remember and remove the current element (use "cut"?)
            parent, pos = self.gui.get_element_parentpos(self.item)
            self.cut()
            # add the conditional in its place
            new_item = self.gui.addtreeitem(parent, ' '.join((IFSTART, cond)), None, pos)
            # put the current element back ("insert under")
            self.gui.set_selected_item(new_item)
            self.paste()

    def remove_condition(self, event=None):
        "haal de IE conditie om het element weg"
        if not self.checkselection():
            return
        text = self.gui.get_element_text(self.item)
        if not text.startswith(IFSTART):
            self.gui.meld("This is not a conditional")
            return
        # for all elements below this one:
        for item in self.gui.get_element_children(self.item):
            # remember and remove it (use "cut"?)
            self.gui.set_selected_item(item)
            self.copy()
            # "insert" after the conditional or under its parent
            self.gui.set_selected_item(self.item)
            self.paste()
        # remove the conditional
        self.gui.set_selected_item(self.item)
        self._copy(cut=True, retain=False, ifcheck=False)

    def _copy(self, cut=False, retain=True, ifcheck=True):
        "start copy/cut/delete actie"
        def push_el(elm, result):
            "subitem(s) toevoegen aan copy buffer"
            text = self.gui.get_element_text(elm)
            data = self.gui.get_element_data(elm)
            atrlist = []
            if text.startswith(ELSTART):
                for node in self.gui.get_element_children(elm):
                    push_el(node, atrlist)
            result.append((text, data, atrlist))
            return result
        if not self.checkselection():
            return
        if self.item == self.root:
            txt = 'cut' if cut else 'copy' if retain else 'delete'
            self.gui.meld("Can't %s the root" % txt)
            return
        text = self.gui.get_element_text(self.item)
        if ifcheck and text.startswith(IFSTART):
            self.gui.meld("Can't do thisJ on a conditional (use menu option to delete)")
            return
        data = self.gui.get_element_data(self.item)
        if str(text).startswith(DTDSTART):
            self.gui.meld("Please use the HTML menu's DTD option to remove the DTD")
            return
        if retain:
            if text.startswith(ELSTART):
                self.cut_el = []
                self.cut_el = push_el(self.item, self.cut_el)
                self.cut_txt = None
            else:
                self.cut_el = None
                self.cut_txt = data
        if cut:
            prev_item = self.gui.do_delete_item(self.item)
            self.mark_dirty(True)
            self.gui.set_selected_item(prev_item)
            self.refresh_preview()

    def cut(self, event=None):
        "cut = copy with removing item from tree"
        self._copy(cut=True)

    def delete(self, event=None):
        "delete = copy with removing item from tree and memory"
        self._copy(cut=True, retain=False)

    def copy(self, event=None):
        "copy = transfer item to memory"
        self._copy()

    def _paste(self, before=True, below=False):
        "start paste actie"
        def zetzeronder(node, elm, pos=-1):
            "paste copy buffer into tree"
            subnode = self.gui.addtreeitem(node, elm[0], elm[1], pos)
            for item in elm[2]:
                zetzeronder(subnode, item)
            return subnode
        if not self.checkselection():
            return
        data = self.gui.get_element_data(self.item)
        if below:
            text = self.gui.get_element_text(self.item)
            if text.startswith(CMSTART):
                self.gui.meld("Can't paste below comment")
                return
            if not text.startswith(ELSTART) and not text.startswith(IFSTART):
                self.gui.meld("Can't paste below text")
                return
        if self.item == self.root:
            if before:
                self.gui.meld("Can't paste before the root")
                return
            else:
                self.gui.meld("Pasting as first element below root")
                below = True
        if self.cut_txt:
            item = getshortname(self.cut_txt)
            data = self.cut_txt
            if below:
                node = self.gui.addtreeitem(self.item, item, data, -1)
            else:
                add_to, idx = self.gui.get_item_parentpos(self.item)
                if not before:
                    idx += 1
                node = self.gui.addtreeitem(add_to, self.item, data, idx)
            if self.advance_selection_on_add:
                self.gui.set_selected_item(node)
        else:
            if below:
                add_to = self.item
                idx = -1
            else:
                add_to, idx = self.gui.get_element_parentpos(self.item)
                if not before:
                    idx += 1
                if idx == len(self.gui.get_element_children(add_to)):
                    idx = -1
            new_item = zetzeronder(add_to, self.cut_el[0], idx)
            if self.advance_selection_on_add:
                self.gui.set_selected_item(new_item)
        self.mark_dirty(True)
        self.refresh_preview()

    def paste_after(self, event=None):
        "paste after instead of before"
        self._paste(before=False)

    def paste_below(self, event=None):
        "paste below instead of before"
        self._paste(below=True)

    def paste(self, event=None):
        "paste before"
        self._paste()

    def _insert(self, before=True, below=False):
        "start invoeg actie"
        if not self.checkselection():
            return
        if below:
            text = self.gui.get_element_text(self.item)
            if text.startswith(CMSTART):
                self.gui.meld("Can't insert below comment")
                return
            if not text.startswith(ELSTART) and not text.startswith(CMELSTART):
                self.gui.meld("Can't insert below text")
                return
            under_comment = text.startswith(CMSTART)
            where = "under"
        elif before:
            where = "before"
        else:
            where = "after"
        ok, dialog_data = self.gui.do_add_element(where)
        if ok:
            tag, attrs, commented = dialog_data
            item = self.item if below else self.gui.get_element_parent(self.item)
            under_comment = self.gui.get_element_text(item).startswith(CMSTART)
            text = getelname(tag, attrs, commented or under_comment)
            if below:
                new_item = self.gui.addtreeitem(self.item, text, attrs, -1)
            else:
                parent, pos = self.gui.get_element_parentpos(self.item)
                if not before:
                    pos += 1
                if pos >= len(self.gui.get_element_children(parent)):
                    pos = -1
                new_item = self.gui.addtreeitem(parent, text, attrs, pos)
            if self.advance_selection_on_add:
                self.gui.set_selected_item(new_item)
            self.mark_dirty(True)
            self.refresh_preview()
            self.gui.set_item_expanded(self.item, True)

    def insert(self, event=None):
        "insert element before"
        self._insert()

    def insert_after(self, event=None):
        "insert element after instead of before"
        self._insert(before=False)

    def insert_child(self, event=None):
        "insert element below instead of before"
        self._insert(below=True)

    def _add_text(self, before=True, below=False):
        "tekst toevoegen onder huidige element"
        if not self.checkselection():
            return
        if below and not self.gui.get_element_text(self.item).startswith(ELSTART):
            self.gui.meld("Can't add text below text")
            return
        ok, dialog_data = self.gui.do_add_textvalue()
        if ok:
            txt, commented = dialog_data
            item = self.item if below else self.gui.get_element_parent(self.item)
            under_comment = self.gui.get_element_text(item).startswith(CMSTART)
            text = getshortname(txt, commented or under_comment)
            if below:
                new_item = self.gui.addtreeitem(self.item, text, txt, -1)
            else:
                parent, pos = self.gui.get_element_parentpos(self.item)
                if not before:
                    pos += 1
                    br = 'br'
                    brs = getelname('br', {}, commented or under_comment)
                    self.gui.addtreeitem(parent, brs, br, pos)
                    pos += 1
                if pos >= len(self.gui.get_element_children(parent)):
                    pos = -1
                new_item = self.gui.addtreeitem(parent, text, txt, pos)
                if before:
                    pos += 1
                    br = 'br'
                    brs = getelname('br', {}, commented or under_comment)
                    self.gui.addtreeitem(parent, brs, br, pos)
            if self.advance_selection_on_add:
                self.gui.set_selected_item(new_item)
            self.mark_dirty(True)
            self.refresh_preview()
            self.gui.set_item_expanded(self.item, True)

    def add_text(self, event=None):
        "insert text before"
        self._add_text()

    def add_text_after(self, event=None):
        "insert text after instead of before"
        self._add_text(before=False)

    def add_textchild(self, event=None):
        "insert text below instead of before"
        self._add_text(below=True)

    def find_next(self, data, search_args, reverse=False, pos=None):
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
            # with open(outfile, 'a') as _o:
            #     print(data, file=_o)
        if reverse:
            data.reverse()
        if pos[0]:
            start = len(data) - pos[0] - 1 if reverse else pos[0]
            data = data[start + 1:]

        itemfound = None
        ele_ok = attr_name_ok = attr_value_ok = attr_ok = text_ok = False
        for newpos, data_item in enumerate(data):
            item, element_name, attr_data = data_item
            with open(outfile, 'a') as _o:
                print(data_item, file=_o)

            itemtext = self.gui.get_element_text(item)
            if element_name.startswith(ELSTART):
                ele_ok = attr_name_ok = attr_value_ok = attr_ok = text_ok = False
                ## if not wanted_ele or wanted_ele in element_name.replace(ELSTART, ''):
                if wanted_ele and wanted_ele in element_name.replace(ELSTART, ''):
                    with open(outfile, 'a') as _o:
                        print('found ele', file=_o)
                    ele_ok = True
                if not attr_data:
                    with open(outfile, 'a') as _o:
                        print('attrs not needed', file=_o)
                    attr_ok = True
                for name, value in attr_data.items():
                    if not wanted_attr or wanted_attr in name:
                        with open(outfile, 'a') as _o:
                            print('found attr name or attr name not needed', file=_o)
                        attr_name_ok = True
                    if not wanted_value or wanted_value in value:
                        with open(outfile, 'a') as _o:
                            print('found attr value or attr value not needed', file=_o)
                        attr_value_ok = True
                    if attr_name_ok and attr_value_ok:
                        attr_ok = True
                        break
                if not wanted_text:
                    with open(outfile, 'a') as _o:
                        print('text value not needed', file=_o)
                    text_ok = True
                # with open(outfile, 'a') as _o:
                #     print(itemtext, 'is het niet', file=_o)
            else:
                text_ok = False
                ele_ok = attr_ok = True
                ## if not wanted_text or wanted_text in element_name:
                if wanted_text and wanted_text in element_name:
                    with open(outfile, 'a') as _o:
                        print('found text value', file=_o)
                    text_ok = True

            with open(outfile, 'a') as _o:
                print(itemtext, ele_ok, attr_ok, text_ok, file=_o)
            ok = ele_ok and attr_ok and text_ok
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

    def _search(self, reverse=False):
        "start search after asking for options"
        self._search_pos = None
        ok = False
        if not reverse or not self.search_args:
            ok, dialog_data = self.gui.get_search_args()
            if ok:
                self.search_args, self.search_specs = dialog_data
        if reverse or ok:
            found = self.find_next(self.flatten_tree(self.gui.top), self.search_args, reverse)
            if found:
                self.gui.set_selected_item(found[1])
                self._search_pos = found
            else:
                self.gui.meld(self.search_specs + '\n\nNo (more) results')

    @staticmethod
    def build_search_spec(ele, attr_name, attr_val, text, attr):
        "build text describing search action"
        if ele:
            ele = '\n an element named `{}`'.format(ele)
        if attr_name or attr_val:
            attr = '\n an attribute'
            if attr_name:
                attr += ' named `{}`'.format(attr_name)
            if attr_val:
                attr += '\n that has value `{}`'.format(attr_val)
            if ele:
                attr = '\n with' + attr[1:]
        out = ''
        if text:
            out = 'search for text'
            if ele:
                out += '\n under' + ele[1:]
            elif attr:
                out += '\n under an element\n with'
            if attr:
                out += attr
        elif ele:
            out = 'search for' + ele
            if attr:
                out += attr
        elif attr:
            out = 'search for' + attr
        outfile = '/tmp/search_stuff'
        with open(outfile, 'w') as _o:
            print(out, file=_o)
        return out

    def search(self, event=None):
        "start search"
        self._search()

    def search_last(self, event=None):
        "start backwards search"
        self._search(reverse=True)

    def _search_next(self, reverse=False):
        "find (default is forward)"
        if not self.search_args:
            return
        found = self.find_next(self.flatten_tree(self.gui.top), self.search_args, reverse,
                               self._search_pos)
        if found:
            self.gui.set_selected_item(found[1])
            self._search_pos = found
        else:
            self.gui.meld(self.search_specs + '\n\nNo (more) results')

    def search_next(self, event=None):
        "find forward"
        self._search_next()

    def search_prev(self, event=None):
        "find backwards"
        self._search_next(reverse=True)

    def replace(self, event=None):
        "replace an element"
        self.gui.meld('Replace: not sure if I wanna implement this')

    def add_dtd(self, event=None):
        "start toevoegen dtd m.b.v. dialoog"
        if self.has_dtd:
            self.gui.do_delete_item(self.gui.get_element_children(self.gui.top)[0])
            self.has_dtd = False
        else:
            ok, dialog_data = self.gui.get_dtd()
            if not ok:
                return
            dtd = dialog_data
            self.gui.addtreeitem(self.gui.top, ' '.join((DTDSTART, getshortname(dtd))),
                                 dtd.rstrip(), 0)
            self.has_dtd = True
        self.gui.adjust_dtd_menu()
        self.mark_dirty(True)
        self.refresh_preview()
        self.gui.ensure_item_visible(self.gui.get_element_children(self.gui.top)[0])

    def add_css(self, event=None):
        "start toevoegen stylesheet m.b.v. dialoog"
        ok, dialog_data = self.gui.get_css_data()
        if not ok:
            return
        data = dialog_data
        # determine the place to put the sylesheet
        self.item = None
        for item in self.gui.get_element_children(self.gui.top):
            if self.gui.get_element_text(item) == ' '.join((ELSTART, 'html')):
                for sub in self.gui.get_element_children(item):
                    if self.gui.get_element_text(sub) == ' '.join((ELSTART, 'head')):
                        self.item = sub
        if not self.item:
            self.gui.meld("Error: no <head> element")
            return
        # create the stylesheet node
        if 'href' in data:
            text = getelname('link', data)
        else:
            text = getelname('style', data)
            cssdata = data.pop('cssdata')
        node = self.gui.addtreeitem(self.item, text, data, -1)
        if 'href' not in data:
            self.gui.addtreeitem(node, getshortname(cssdata), cssdata, -1)
        self.mark_dirty(True)
        self.refresh_preview()

    def check_if_adding_ok(self):
        "check if element can be added here"
        ok = True
        if not self.checkselection():
            ok = False
        elif not self.gui.get_element_text(self.item).startswith(ELSTART):
            self.gui.meld("Can't do this below text")
            ok = False
        return ok

    @staticmethod
    def convert_link(link, root):
        """attempt to turn the link into one relative to the document
        """
        nice_link = '', ''
        test = link.split('/', 1)
        if not link:
            raise ValueError("link opgeven of cancel kiezen s.v.p")
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
            raise ValueError('Unable to make this local link relative')
        return nice_link

    def add_link(self, event=None):
        "start toevoegen link m.b.v. dialoog"
        if self.check_if_adding_ok():
            ok, dialog_data = self.gui.get_link_data()
            if ok:
                txt, data = dialog_data
                node = self.gui.addtreeitem(self.item, getelname('a', data), data, -1)
                self.gui.addtreeitem(node, getshortname(txt), txt, -1)
                self.mark_dirty(True)
                self.refresh_preview()

    def add_image(self, event=None):
        "start toevoegen image m.b.v. dialoog"
        if self.check_if_adding_ok():
            ok, dialog_data = self.gui.get_image_data()
            if ok:
                data = dialog_data
                self.gui.addtreeitem(self.item, getelname('image', data), data, -1)
                self.mark_dirty(True)
                self.refresh_preview()

    def add_audio(self, event=None):
        "start toevoegen audio m.b.v. dialoog"
        if self.check_if_adding_ok():
            ok, dialog_data = self.gui.get_audio_data()
            if ok:
                data = dialog_data
                data['controls'] = ''
                self.gui.addtreeitem(self.item, getelname('audio', data), data, -1)
                self.mark_dirty(True)
                self.refresh_preview()

    def add_video(self, event=None):
        "start toevoegen video m.b.v. dialoog"
        if self.check_if_adding_ok():
            ok, dialog_data = self.gui.get_video_data()
            if ok:
                data = dialog_data
                data['controls'] = ''
                src = data.pop('src')
                node = self.gui.addtreeitem(self.item, getelname('video', data), data, -1)
                child_data = {'src': src,
                              'type': 'video/{}'.format(pathlib.Path(src).suffix[1:])}
                self.gui.addtreeitem(node, getelname('source', child_data), child_data, -1)
                self.mark_dirty(True)
                self.refresh_preview()

    def add_list(self, event=None):
        "start toevoegen list m.b.v. dialoog"
        if self.check_if_adding_ok():
            ok, dialog_data = self.gui.get_list_data()
            if ok:
                list_type, list_data = dialog_data
                itemtype = "dt" if list_type == "dl" else "li"
                new_item = self.gui.addtreeitem(self.item, getelname(list_type), None, -1)
                for list_item in list_data:
                    new_subitem = self.gui.addtreeitem(new_item, getelname(itemtype), None, -1)
                    data = list_item[0]
                    self.gui.addtreeitem(new_subitem, getshortname(data), data, -1)
                    if list_type == "dl":
                        new_subitem = self.gui.addtreeitem(new_item, getelname('dd'), None, -1)
                        data = list_item[1]
                        self.gui.addtreeitem(new_subitem, getshortname(data), data, -1)
                self.mark_dirty(True)
                self.refresh_preview()

    def add_table(self, event=None):
        "start toevoegen tabel m.b.v. dialoog"
        if self.check_if_adding_ok():
            ok, dialog_data = self.gui.get_table_data()
            if ok:
                summary, titles, headers, items = dialog_data
                data = {'summary': summary}
                tbl_item = self.gui.addtreeitem(self.item, getelname('table', data), data, -1)
                if titles:
                    new_row = self.gui.addtreeitem(tbl_item, getelname('tr'), None, -1)
                    for head in headers:
                        new_head = self.gui.addtreeitem(new_row, getelname('th'), None, -1)
                        text = head or BL
                        self.gui.addtreeitem(new_head, getshortname(text), text, -1)
                for rowitem in items:
                    new_row = self.gui.addtreeitem(tbl_item, getelname('tr'), None, -1)
                    for cellitem in rowitem:
                        new_cell = self.gui.addtreeitem(new_row, getelname('td'), None, -1)
                        text = cellitem
                        self.gui.addtreeitem(new_cell, getshortname(text), text, -1)
                self.mark_dirty(True)
                self.refresh_preview()

    def validate(self, event=None):
        """validate HTML source
        """
        if self.tree_dirty or not self.xmlfn:
            htmlfile = '/tmp/ashe_check.html'
            fromdisk = False
            self.data2soup()
            with open(htmlfile, 'w') as f_out:
                f_out.write(self.soup.prettify())
        else:
            htmlfile = self.xmlfn
            fromdisk = True
        self.gui.validate(htmlfile, fromdisk)

    @staticmethod
    def do_validate(htmlfile):
        """get validated html
        """
        output = '/tmp/ashe_check'
        print(output, htmlfile)
        subprocess.run(['tidy', '-e', '-f', output, htmlfile])
        data = ""
        with open(output) as f_in:
            data = f_in.read()
        return data

    def view_code(self, event=None):
        "start source viewer"
        self.data2soup()
        self.gui.show_code("Source view", "Let op: de tekst wordt niet ververst"
                           " bij wijzigingen in het hoofdvenster", self.soup.prettify())

    def about(self, event=None):
        "get info about the application"
        self.gui.meld("""\
            Tree-based HTML editor with simultaneous preview

            Started in 2008 by Albert Visser
            Versions for PC and PDA available""")
