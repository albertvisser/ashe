# -*- coding: utf-8 -*-

"""
PyQt4 versie van mijn op een treeview gebaseerde HTML-editor
startfunctie en hoofdscherm
"""

import os
import sys
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import PyQt4.QtWebKit as webkit
import bs4 as bs # BeautifulSoup as bs

import ashe.ashe_mixin as ed
from ashe.ashe_dialogs_qt import cssedit_available, HMASK, ElementDialog, \
    TextDialog, DtdDialog, CssDialog, LinkDialog, ImageDialog, VideoDialog, \
    AudioDialog, ListDialog, TableDialog, ScrolledTextDialog, CodeViewDialog

PPATH = os.path.split(__file__)[0]
DESKTOP = ed.DESKTOP
CMSTART = ed.CMSTART
ELSTART = ed.ELSTART
CMELSTART = ed.CMELSTART
DTDSTART = ed.DTDSTART
IFSTART = ed.IFSTART
BL = ed.BL
TITEL = ed.TITEL
INLINE_1 = 'inline stylesheet'

def comment_out(node, commented):
    "subitem(s) (ook) op commentaar zetten"
    count = node.childCount()
    for idx in range(count):
        subnode = node.child(idx)
        txt = str(subnode.text(0))
        if commented:
            if not txt.startswith(CMSTART):
                subnode.setText(0, " ".join((CMSTART, txt)))
        else:
            if txt.startswith(CMSTART):
                subnode.setText(0, txt.split(None, 1)[1])
        comment_out(subnode, commented)

def finditem(parent, tag, first_only=True):
    """find tag item(s) under a parent

    if first_only is True, one item is returned; otherwise a list of items
    if none found, an empty list is returned
    """
    items = []
    found = False
    for ix in range(parent.childCount()):
        item = parent.child(ix)
        if item.text(0).startswith(' '.join((ELSTART, tag))):
            if first_only:
                return item
                break
            else:
                items.append(item)
    return items # if not first_only else '' - not necessary when testing for if result:

def is_stylesheet_node(node):
    if node.text(0) == ' '.join((ELSTART, 'link')):
        # need to check for rel = stylesheet attribute
        attrdict = node.data(0, core.Qt.UserRole)
        if attrdict.get('rel', '') == 'stylesheet':
            return True
    elif node.text(0) == ' '.join((ELSTART, 'style')):
        return True
    return False

def in_body(node):
    def is_node_ok(node):
        if node.text(0) == ' '.join((ELSTART, 'body')):
            return True
        elif node.text(0) == ' '.join((ELSTART, 'head')) or node.parent() is None:
            return False
        else:
            return is_node_ok(node.parent())
    return is_node_ok(node)


class VisualTree(gui.QTreeWidget):
    def __init__(self, parent):
        self._parent = parent
        gui.QTreeWidget.__init__(self)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.InternalMove)
        self.setDropIndicatorShown(True)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.x(), event.y())
        if item and item != self._parent.top:
            if str(item.text(0)).startswith(ELSTART) and item.childCount() == 0:
                self._parent.edit()
                return
        gui.QTreeWidget.mouseDoubleClickEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == core.Qt.RightButton:
            xc, yc = event.x(), event.y()
            item = self.itemAt(xc, yc)
            if item and item != self._parent.top:
                self.setCurrentItem(item)
                self._parent.popup_menu(item)
                return
        gui.QTreeWidget.mouseReleaseEvent(self, event)

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        item = self.itemAt(event.pos())
        if not item or not item.text(0).startswith(ELSTART):
            gui.QMessageBox.information(self, self._parent.title,
                'Can only drop on element')
            return
        dragitem = self.selectedItems()[0]
        gui.QTreeWidget.dropEvent(self, event)
        self._parent.tree_dirty = True
        dropitem = dragitem.parent()
        self.setCurrentItem(dragitem)
        dropitem.setExpanded(True)
        self._parent.refresh_preview()

class MainFrame(gui.QMainWindow, ed.EditorMixin):
    "Main GUI"

    def __init__(self, parent, _id, fname=''):
        self.parent = parent
        self.title = "(untitled) - Albert's Simple HTML Editor"
        self.xmlfn = fname
        # bepaalt de bij het scherm passende hoogte en breedte
        # dsp = gui.QDisplay().GetClientArea()
        # high = dsp.height if dsp.height < 900 else 900
        # wide = dsp.width if dsp.width < 1020 else 1020
        gui.QMainWindow.__init__(self) #, parent, _id,
            # pos = (dsp.top, dsp.left),
            # size = (wide, high)
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        self.resize(1020, 900)

        self._setup_menu()
        ## act = gui.QAction(self)
        ## act.setShortcut(core.Qt.Key_Super_R)
        ## self.connect(act, core.SIGNAL('triggered()'), self.popup_menu)
        self.in_contextmenu = False

        self.pnl = gui.QSplitter(self)
        self.setCentralWidget(self.pnl)

        self.tree = VisualTree(self)
        self.tree.setItemHidden(self.tree.headerItem(), True)
        self.pnl.addWidget(self.tree)

        self.html = webkit.QWebView(self.pnl) # , -1,
        self.pnl.addWidget(self.html)

        self.sb = self.statusBar()

        self.tree.resize(500, 100)
        self.tree.setFocus()

        ed.EditorMixin.getsoup(self, fname)
        self.adv_menu.setChecked(True)
        self.refresh_preview()

    def _setup_menu(self):
        self.menulist = (
            '&File', (
                ('&New', 'N', 'C', "Start a new HTML document", self.newxml),
                ('&Open', 'O', 'C', "Open an existing HTML document", self.openxml),
                ('&Save', 'S', 'C', "Save the current document", self.savexml),
                ('Save &As', 'S', 'SC',
                    "Save the current document under a different name",
                    self.savexmlas),
                ('&Revert', 'R', 'C', "Discard all changes since the last save",
                    self.reopenxml),
                ('sep1', ),
                ('E&xit', 'Q', 'C', 'Quit the application', self.close),
                ),
                ), (
            '&View', (
                ('E&xpand All (sub)Levels', '+', 'C',
                    "Show what's beneath the current element", self.expand, True),
                ('&Collapse All (sub)Levels', '-', 'C',
                    "Hide what's beneath the current element", self.collapse, True),
                ('sep1', ),
                ('Advance selection on add/insert', '', '',
                    "Move the selection to the added/pasted item",
                    self.advance_selection_onoff),
                ('sep2', ),
                ('&Resync preview', 'F5', '', 'Reset the preview window to the '
                    'contents of the treeview', self.refresh_preview),
                ),
                ), (
            '&Edit', (
                ('Edit', 'F2', '', 'Modify the element/text and/or its attributes',
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
                    self.paste_aft),
                ('Paste Under', 'V', 'C', 'Paste below the current element',
                    self.paste_blw),
                ('sep2', ),
                ('Delete', 'Del', '', 'Delete the current element', self.delete),
                ('Insert Text (under)', 'Ins', 'S',
                    'Add a text node under the current one', self.add_textchild),
                ('Insert Text before', 'Ins', 'SC',
                    'Add a text node before the current one', self.add_text),
                ('Insert Text after', 'Ins', 'SA',
                    'Add a text node after the current one', self.add_text_aft),
                ('Insert Element Before', 'Ins', 'C',
                    'Add a new element in front of the current', self.insert),
                ('Insert Element After', 'Ins', 'A',
                    'Add a new element after the current', self.ins_aft),
                ('Insert Element Under', 'Ins', '',
                    'Add a new element under the current', self.ins_chld),
                ),
                ), (
            "&HTML", (
                ('Add &DTD', '', '', 'Add a document type description', self.add_dtd),
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
                ('&View code', '', '', 'Shows the html pretty-printed',
                    self.view_code),
                ('&Check syntax', '', '', 'Validate HTML with Tidy', self.validate),
                ),
                ), (
            "Help", (
                ('&About', '', '', 'Info about this application', self.about),
                ),
                )
        menu_bar = self.menuBar()
        self.contextmenu_items = []
        for menu_text, data in self.menulist:
            menu = gui.QMenu(menu_text, self)
            for item in data:
                if len(item) == 1:
                    menu.addSeparator()
                    continue
                menuitem_text, hotkey, modifiers, status_text, callback = item[:5]
                if 'A' in modifiers:
                    hotkey = "+".join(("Alt",hotkey))
                if 'C' in modifiers:
                    hotkey = "+".join(("Ctrl",hotkey))
                if 'S' in modifiers:
                    hotkey = "+".join(("Shift",hotkey))
                act = gui.QAction(menuitem_text, self)
                menu.addAction(act)
                act.setStatusTip(status_text)
                act.setShortcut(hotkey)
                self.connect(act, core.SIGNAL('triggered()'), callback)
                if menuitem_text.startswith('Advance selection'):
                    act.setCheckable(True)
                    self.adv_menu = act
                elif menu_text == '&View':
                    self.contextmenu_items.append(('A', act))
                elif menuitem_text == 'Add &DTD':
                    self.dtd_menu = act
                elif menuitem_text == 'Add &Stylesheet':
                    self.css_menu = act
                    if not cssedit_available:
                        act.setDisabled(True)
                if menu_text in ('&Edit', '&HTML'):
                    self.contextmenu_items.append(('M', menu))
            if menu_text == '&View':
                self.contextmenu_items.append(('', ''))
            menu_bar.addMenu(menu)

    def _check_tree(self):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)
        retourneert 1 = Yes, 0 = No, -1 = Cancel
        """
        if self.tree_dirty:
            retval = dict(zip((gui.QMessageBox.Yes, gui.QMessageBox.No,
                gui.QMessageBox.Cancel), (1, 0, -1)))
            hlp = gui.QMessageBox.question(self, self.title, "HTML data has been "
                "modified - save before continuing?",
                gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel,
                defaultButton = gui.QMessageBox.Yes)
            if hlp == gui.QMessageBox.Yes:
                self.savexml()
            return retval[hlp]

    def close(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna afsluiten"""
        if self._check_tree() != -1:
            gui.QMainWindow.close(self)

    def newxml(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna nieuwe html aanmaken"""
        if self._check_tree() != -1:
            try:
                ed.EditorMixin.getsoup(self, fname = None)
                self.adv_menu.setChecked(True)
                self.sb.showMessage("started new document")
                self.refresh_preview()
            except Exception as err:
                gui.QMessageBox.information(self, self.title, str(err))

    def openxml(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna een html bestand kiezen"""
        if self._check_tree() != -1:
            loc = os.path.dirname(self.xmlfn) if self.xmlfn else os.getcwd()
            fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", loc,
                HMASK)
            if fnaam:
                ed.EditorMixin.getsoup(self, fname=str(fnaam))
                self.adv_menu.setChecked(True)
                self.sb.showMessage("loaded {}".format(self.xmlfn))
                self.refresh_preview()

    # def setfilenametooltip((self):
        # """bedoeld om de filename ook als tooltip te tonen, uit te voeren
        # aan het eind van new, open, save, saveas en reload"""
        # zie ticket 406 voor een overweging om dit helemaal achterwege te laten

    def savexml(self, evt=None):
        "save html to file"
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.data2soup()
            try:
                self.soup2file()
            except IOError as err:
                gui.QMessageBox.information(self, self.title, str(err))
                return
            self.sb.showMessage("saved {}".format(self.xmlfn))

    def savexmlas(self, evt=None):
        """vraag bestand om html op te slaan
        bestand opslaan en naam in titel en root element zetten"""
        name = gui.QFileDialog.getSaveFileName(self, "Save file as ...",
            self.xmlfn or os.getcwd(),
            HMASK)
        if name:
            self.xmlfn = str(name)
            self.data2soup()
            try:
                self.soup2file(saveas=True)
            except IOError as err:
                gui.QMessageBox.information(self, self.title, str(err))
                return
            self.top.setText(0, self.xmlfn)
            self.setWindowTitle(" - ".join((os.path.basename(self.xmlfn), TITEL)))
            self.sb.showMessage("saved as {}".format(self.xmlfn))

    def reopenxml(self, evt=None):
        """onvoorwaardelijk html bestand opnieuw laden"""
        try:
            ed.EditorMixin.getsoup(self, fname = self.xmlfn)
            self.adv_menu.setChecked(True)
            self.sb.showMessage("reloaded {}".format(self.xmlfn))
            self.refresh_preview()
        except Exception as err:
            gui.QMessageBox(self, self.title, str(err))

    def advance_selection_onoff(self, event=None):
        self.advance_selection_on_add = self.adv_menu.isChecked()

    def mark_dirty(self, state):
        ed.EditorMixin.mark_dirty(self, state)
        title = str(self.windowTitle())
        test = ' - ' + TITEL
        test2 = '*' + test
        if state:
            if test2 not in title:
                title = title.replace(test, test2)
        else:
            title = title.replace(test2, test)
        self.setWindowTitle(title)

    def refresh_preview(self, event=None):
        self.data2soup()
        self.html.setHtml(str(self.soup).replace('%SOUP-ENCODING%','utf-8'))
        self.tree.setFocus()

    def about(self, evt=None):
        "toon programma info"
        abouttext = ed.EditorMixin.about(self)
        gui.QMessageBox.information(self, self.title, abouttext)

    def addtreeitem(self, node, naam, data, index=-1):
        """itemnaam en -data toevoegen aan de interne tree
        default is achteraan onder node, anders index meegeven
        geeft referentie naar treeitem terug
        """
        newnode = gui.QTreeWidgetItem()
        newnode.setText(0, naam) # self.tree.AppendItem(node, naam)
        # data is ofwel leeg, ofwel een string, ofwel een dictionary
        newnode.setData(0, core.Qt.UserRole, data) # self.tree.SetPyData(newnode, data)
        if index == -1:
            node.addChild(newnode)
        else:
            node.insertChild(index, newnode)
        return newnode

    def addtreetop(self, fname, titel):
        """titel en root item in tree instellen"""
        self.setWindowTitle(titel)
        self.top = gui.QTreeWidgetItem()
        self.top.setText(0, fname)
        self.tree.addTopLevelItem(self.top) # AddRoot(titel)

    def init_tree(self, name=''):
        "nieuwe tree initialiseren"
        self.tree.clear()
        ed.EditorMixin.init_tree(self, name)
        self.adjust_dtd_menu()
        if DESKTOP:
            self.tree.setCurrentItem(self.top)

    def data2soup(self):
        "interne tree omzetten in BeautifulSoup object"
        def expandnode(node, root, data, commented = False):
            "tree item (node) met inhoud (data) toevoegen aan BS node (root)"
            try:
                for att in data:
                    root[str(att)] = str(data[att])
            except TypeError:
                pass
            for ix in range(node.childCount()):
                elm = node.child(ix)
                text = str(elm.text(0))
                data = elm.data(0, core.Qt.UserRole)
                if sys.version < '3':
                    data = data.toPyObject()
                if text.startswith(ELSTART) or text.startswith(CMELSTART):
                    # data is een dict: leeg of een mapping van data op attributen
                    if text.startswith(CMSTART):
                        text = text.split(None, 1)[1]
                        if not commented:
                            is_comment = True
                            soup = bs.BeautifulSoup()
                            sub = soup.new_tag(text.split()[1])
                            expandnode(elm, sub, data, is_comment)
                            sub = bs.Comment(str(sub)) # .decode("utf-8")) niet voor Py3
                        else:
                            is_comment = False
                            sub = self.soup.new_tag(text.split()[1])
                    else:
                        is_comment = False
                        sub = self.soup.new_tag(text.split()[1])
                    root.append(sub) # insert(0,sub)
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
                    for iy in range(elm.childCount()):
                        subel = elm.child(iy)
                        subtext = str(subel.text(0))
                        data = subel.data(0, core.Qt.UserRole)
                        if subtext.startswith(ELSTART):
                            # element in tekst omzetten en deze aan text toevoegen
                            onthou = self.soup
                            self.soup = bs.BeautifulSoup()
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
                    sub = bs.NavigableString(str(data)) #.decode("utf-8")) niet voor Py3
                    if text.startswith(CMSTART) and not commented:
                        sub = bs.Comment(data) # .decode("utf-8")) niet voor Py3
                    root.append(sub) # data.decode("latin-1")) # insert(0,sub)
        self.soup = bs.BeautifulSoup() # self.root.originalEncoding)
        count = self.top.childCount()
        for ix in range(count):
            tag = self.top.child(ix)
            text = str(tag.text(0))
            data = tag.data(0, core.Qt.UserRole)
            if sys.version < '3':
                data = data.toPyObject()
            if text.startswith(DTDSTART):
                root = bs.Doctype(str(data)) # Declaration(str(data))
                self.soup.append(root)
            elif text.startswith(ELSTART):
                root = self.soup.new_tag(text.split(None, 2)[1])
                self.soup.append(root)
                expandnode(tag, root, data)

    def adjust_dtd_menu(self):
        if self.has_dtd:
            self.dtd_menu.setText('Remove &DTD')
            self.dtd_menu.setStatusTip('Remove the document type declaration')
        else:
            self.dtd_menu.setText('Add &DTD')
            self.dtd_menu.setStatusTip('Add a document type description')

    def popup_menu(self, arg=None):
        'build/show context menu'
        # get type of node
        node = self.tree.currentItem()
        menu = gui.QMenu()
        for itemtype, item in self.contextmenu_items:
            if itemtype == 'A':
                menu.addAction(item)
                if item == self.css_menu:
                    if not cssedit_available:
                        act.setDisabled(True)
                    ## elif in_body(item):
                        ## item.setText('Add inline &style')
                        ## if not node.text(0).startswith(ELSTART):
                            ## item.setDisabled(True)
            elif itemtype == 'M':
                menu.addMenu(item)
            else:
                menu.addSeparator()
        y = self.tree.visualItemRect(arg).bottom()
        x = self.tree.visualItemRect(arg).left()
        popup_location = core.QPoint(int(x) + 200, y)
        self.in_contextmenu = True
        menu.exec_(self.tree.mapToGlobal(popup_location))
        self.in_contextmenu = False
        # del menu

    def checkselection(self):
        "controleer of er wel iets geselecteerd is (behalve de filenaam)"
        sel = True
        self.item = self.tree.currentItem()
        if self.item is None or self.item == self.top:
            gui.QMessageBox.information(self, self.title,
                'You need to select an element or text first')
            sel = False
        return sel

    def keyReleaseEvent(self, event):
        skip = self.on_keyup(event)
        if not skip:
            gui.QMainWindow.keyReleaseEvent(self, event)

    def on_keyup(self, ev=None):
        ky = ev.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top:
            if ky == core.Qt.Key_Menu:
                self.popup_menu(item)
                skip = True
        return skip

    def expand(self, evt=None):
        "expandeer tree vanaf huidige item"
        def expand_all(item):
            for ix in range(item.childCount()):
                sub = item.child(ix)
                sub.setExpanded(True)
                expand_all(sub)
        item = self.tree.currentItem()
        self.tree.expandItem(item)
        expand_all(item)
        self.tree.resizeColumnToContents(0)

    def collapse(self, evt=None):
        "collapse huidige item en daaronder"
        def collapse_all(item):
            for ix in range(item.childCount()):
                sub = item.child(ix)
                collapse_all(sub)
                sub.setExpanded(False)
        item = self.tree.currentItem()
        collapse_all(item)
        self.tree.collapseItem(item)
        self.tree.resizeColumnToContents(0)

    def comment(self, evt=None):
        "(un)comment zonder de edit dialoog"
        if DESKTOP and not self.checkselection():
            return
        tag = str(self.item.text(0))
        attrs = self.item.data(0, core.Qt.UserRole)
        if sys.version < '3':
            attrs = attrs.toPyObject()
        commented = tag.startswith(CMSTART)
        if commented:
            _, tag = tag.split(None, 1) # CMSTART eraf halen
        under_comment = str(self.item.parent().text(0)).startswith(CMELSTART)
        commented = not commented # het (un)commenten uitvoeren
        if under_comment:
            commented = True
        if tag.startswith(ELSTART):
            _, tag = tag.split(None, 1) # ELSTART eraf halen
            self.item.setText(0, ed.getelname(tag, attrs, commented))
            self.item.setData(0, core.Qt.UserRole, attrs)
            comment_out(self.item, commented)
        else:
            self.item.setText(0, ed.getshortname(tag, commented))
            self.item.setData(0, core.Qt.UserRole, tag)
        self.refresh_preview()

    def edit(self, evt=None):
        "start edit m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        data = str(self.item.text(0))
        if data.startswith(DTDSTART):
            data = str(self.item.data(0, core.Qt.UserRole))
            prefix = 'HTML PUBLIC "-//W3C//DTD'
            if data.upper().startswith(prefix):
                data = data.upper().replace(prefix, '')
                text = 'doctype is ' + data.split('//EN')[0].strip()
            elif data.strip().lower() == 'html':
                text = 'doctype is HTML 5'
            else:
                text = 'doctype cannot be determined'
            gui.QMessageBox.information(self, self.title, text)
            return
        elif data.startswith(IFSTART):
            gui.QMessageBox.information(self, self.title,
                "About to edit this conditional")
            # start dialog to edit condition
            cond, ok = gui.QInputDialog(self, self.title, data)
            # if confirmed: change element
            if ok:
                gui.QMessageBox.information(self, self.title,
                    "changing to " + str(cond))
            return
        under_comment = str(self.item.parent().text(0)).startswith(CMELSTART)
        modified = False
        if data.startswith(ELSTART) or data.startswith(CMELSTART):
            oldtag = ed.get_tag_from_elname(data)
            attrdict = self.item.data(0, core.Qt.UserRole)
            if oldtag == 'style':
                attrdict['styledata'] = str(
                    self.item.child(0).data(0, core.Qt.UserRole))
            if sys.version < '3':
                attrdict = attrdict.toPyObject()
            was_commented = data.startswith(CMSTART)
            edt = ElementDialog(self, title = 'Edit an element', tag = data,
                attrs = attrdict).exec_()
            if edt == gui.QDialog.Accepted:
                modified = True
                tag, attrs, commented = self.dialog_data
                if under_comment:
                    commented = True
                if tag == 'style':
                    # style data zit in attrs['styledata'] en moet naar tekst element onder tag
                    newtext = str(attrs.pop('styledata', '')) # en daarna moet deze hier weg
                    oldtext = str(self.item.child(0).data(0, core.Qt.UserRole))
                    if newtext != oldtext:
                        ## if newtext == '':
                            ## TODO: remove child, possibly style tag as well
                        self.item.child(0).setText(0, ed.getshortname(newtext))
                        self.item.child(0).setData(0, core.Qt.UserRole, newtext)
                attrdict.pop('styledata', '')
                if tag != oldtag or attrs != attrdict:
                    self.item.setText(0, ed.getelname(tag, attrs, commented))
                self.item.setData(0, core.Qt.UserRole, attrs)
                if commented != was_commented:
                    comment_out(self.item, commented)
        else:
            txt = CMSTART + " " if data.startswith(CMSTART) else ""
            data = self.item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                data = str(data.toPyObject())
            test = str(self.item.parent().text(0))
            if test in (' '.join((ELSTART, 'style')),
                    ' '.join((CMELSTART, 'style'))):
                gui.QMessageBox.information(self, self.title,
                    "Please edit style through parent tag")
                return
            edt = TextDialog(self, title='Edit Text', text = txt + data).exec_()
            if edt == gui.QDialog.Accepted:
                modified = True
                txt, commented = self.dialog_data
                if under_comment:
                    commented = True
                self.item.setText(0, ed.getshortname(txt, commented))
                self.item.setData(0, core.Qt.UserRole, txt)
        if modified:
            self.mark_dirty(True)
            self.refresh_preview()

    def copy(self, evt=None, cut=False, retain=True, ifcheck=True):
        "start copy/cut/delete actie"
        def push_el(elm, result):
            "subitem(s) toevoegen aan copy buffer"
            text = str(elm.text(0))
            data = elm.data(0, core.Qt.UserRole)
            if sys.version < '3':
                data = data.toPyObject()
            atrlist = []
            if text.startswith(ELSTART):
                num = elm.childCount()
                for idx in range(num):
                    node = elm.child(idx)
                    x = push_el(node, atrlist)
            result.append((text, data, atrlist))
            return result
        if DESKTOP and not self.checkselection():
            return
        if self.item == self.root:
            gui.QMessageBox.information(self, self.title, "Can't %s the root" % txt)
            return
        text = str(self.item.text(0))
        if ifcheck and text.startswith(IFSTART):
            gui.QMessageBox.information(self, self.title,
                "Can't do this on a conditional (use menu option to delete)")
            return
        data = self.item.data(0, core.Qt.UserRole)
        if sys.version < '3':
            data = data.toPyObject()
        txt = 'cut' if cut else 'copy'
        if str(text).startswith(DTDSTART):
            gui.QMessageBox.information(self, self.title,
                "Please use the HTML menu's DTD option to remove the DTD")
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
            parent = self.item.parent()
            ix = parent.indexOfChild(self.item)
            if ix > 0:
                ix -= 1
                prev = parent.child(ix)
            else:
                prev = parent
                if prev == self.root:
                    prev = parent.child(ix+1)
            parent.removeChild(self.item)
            self.mark_dirty(True)
            self.tree.setCurrentItem(prev)
            self.refresh_preview()

    def paste(self, evt=None, before=True, below=False):
        "start paste actie"
        def zetzeronder(node, elm, pos = -1):
            "paste copy buffer into tree"
            subnode = gui.QTreeWidgetItem()
            subnode.setText(0, elm[0])
            subnode.setData(0, core.Qt.UserRole, elm[1])
            if pos == -1:
                node.addChild(subnode)
            else:
                node.insertChild(pos, subnode)
            for item in elm[2]:
                zetzeronder(subnode, item)
            return subnode
        if DESKTOP and not self.checkselection():
            return
        data = self.item.data(0, core.Qt.UserRole)
        if sys.version < '3':
            data = data.toPyObject()
        if below:
            text = str(self.item.text(0))
            if text.startswith(CMSTART):
                gui.QMessageBox.information(self, self.title, "Can't paste below comment")
                return
            if not text.startswith(ELSTART) and not text.startswith(IFSTART):
                gui.QMessageBox.information(self, self.title, "Can't paste below text")
                return
        if self.item == self.root:
            if before:
                gui.QMessageBox.information(self, self.title,
                    "Can't paste before the root")
                return
            else:
                gui.QMessageBox.information(self, self.title,
                    "Pasting as first element below root")
                below = True
        if self.cut_txt:
            item = ed.getshortname(self.cut_txt)
            data = self.cut_txt
            node = gui.QTreeWidgetItem()
            node.setText(0, item)
            node.setData(0, core.Qt.UserRole, data)
            if below:
                self.item.addChild(node)
            else:
                add_to = self.item.parent()
                idx = add_to.indexOfChild(self.item)
                if not before:
                    idx += 1
                if idx >= add_to.childCount():
                    add_to.addChild(node)
                else:
                    add_to.insertChild(idx, node)
            if self.advance_selection_on_add:
                self.tree.setCurrentItem(node)
        else:
            if below:
                add_to = self.item
                idx = -1
            else:
                add_to = self.item.parent()
                idx = add_to.indexOfChild(self.item)
                cnt = add_to.childCount()
                if not before:
                    idx += 1
                if idx == cnt:
                    idx = -1
            new_item = zetzeronder(add_to, self.cut_el[0], idx)
            if self.advance_selection_on_add:
                self.tree.setCurrentItem(new_item)
        self.mark_dirty(True)
        self.refresh_preview()

    def add_text(self, evt=None, before=True, below=False):
        "tekst toevoegen onder huidige element"
        if DESKTOP and not self.checkselection():
            return
        if below and not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox.information(self, self.title, "Can't add text below text")
            return
        edt = TextDialog(self, title="New Text").exec_()
        if edt == gui.QDialog.Accepted:
            txt, commented = self.dialog_data
            if below:
                text = str(self.item.text(0))
            else:
                parent = self.item.parent()
                text = str(parent.text(0))
            under_comment = text.startswith(CMSTART)
            text = ed.getshortname(txt, commented or under_comment)
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, text)
            new_item.setData(0, core.Qt.UserRole, txt)
            if below:
                self.item.addChild(new_item)
            else:
                ix = parent.indexOfChild(self.item)
                if not before:
                    ix += 1
                if ix >= parent.childCount():
                    parent.addChild(new_item)
                else:
                    parent.insertChild(ix, new_item)
            if self.advance_selection_on_add:
                self.tree.setCurrentItem(new_item)
            self.mark_dirty(True)
            self.refresh_preview()
            self.item.setExpanded(True)

    def insert(self, evt=None, before=True, below=False):
        "start invoeg actie"
        if DESKTOP and not self.checkselection():
            return
        if below:
            text = str(self.item.text(0))
            if text.startswith(CMSTART):
                gui.QMessageBox.information(self, self.title,
                    "Can't insert below comment")
                return
            if not text.startswith(ELSTART) and not text.startswith(CMELSTART):
                gui.QMessageBox.information(self, self.title,
                    "Can't insert below text")
                return
            under_comment = text.startswith(CMSTART)
            where = "under"
        elif before:
            where = "before"
        else:
            where = "after"
        edt = ElementDialog(self, title="New element (insert {0})".format(where)).exec_()
        if edt == gui.QDialog.Accepted:
            modified = True
            tag, attrs, commented = self.dialog_data
            if below:
                text = str(self.item.text(0))
            else:
                parent = self.item.parent()
                text = str(parent.text(0))
            under_comment = text.startswith(CMSTART)
            text = ed.getelname(tag, attrs, commented or under_comment)
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, text)
            new_item.setData(0, core.Qt.UserRole, attrs)

            if below:
                self.item.addChild(new_item)
            else:
                ix = parent.indexOfChild(self.item)
                if not before:
                    ix += 1
                if ix >= parent.childCount():
                    parent.addChild(new_item)
                else:
                    parent.insertChild(ix, new_item)
            if self.advance_selection_on_add:
                self.tree.setCurrentItem(new_item)
            self.mark_dirty(True)
            self.refresh_preview()
            self.item.setExpanded(True)

    def make_conditional(self, evt=None):
        "zet een IE conditie om het element heen"
        if DESKTOP and not self.checkselection():
            return
        text = str(self.item.text(0))
        if text.startswith(IFSTART):
            gui.QMessageBox.information(self, self.title,
                "This is already a conditional")
            return
        # ask for the condition
        cond, ok = gui.QInputDialog.getText(self, self.title, 'Enter the condition',
            text = '')
        if ok:
            # remember and remove the current element (use "cut"?)
            parent = self.item.parent()
            test = parent.indexOfChild(self.item)
            self.cut()
            # add the conditional in its place
            if parent.childCount() == 1:
                new = self.addtreeitem(parent, ' '.join((IFSTART, cond)), '')
            else:
                new = self.addtreeitem(parent, ' '.join((IFSTART, cond)), '',
                    index=test)
            # put the current element back ("insert under")
            self.tree.setCurrentItem(new)
            self.paste_blw()

    def remove_condition(self, evt=None):
        "haal de IE conditie om het element weg"
        if DESKTOP and not self.checkselection():
            return
        text = str(self.item.text(0))
        if not text.startswith(IFSTART):
            gui.QMessageBox.information(self, self.title,
                "This is not a conditional")
            return
        cond = self.item
        parent = cond.parent()
        # for all elements below this one:
        for ix in range(cond.childCount()):
            # remember and remove it (use "cut"?)
            self.tree.setCurrentItem(cond.child(ix))
            self.copy()
            # "insert" after the conditional or under its parent
            self.tree.setCurrentItem(cond)
            self.paste()
        # remove the conditional -
        self.tree.setCurrentItem(cond)
        self.delete(ifcheck=False)

    def add_dtd(self, evt=None):
        "start toevoegen dtd m.b.v. dialoog"
        if self.has_dtd:
            self.top.removeChild(self.top.child(0))
            self.has_dtd = False
        else:
            edt = DtdDialog(self).exec_()
            if edt == gui.QDialog.Rejected:
                return
            node = gui.QTreeWidgetItem()
            self.top.insertChild(0, node)
            dtd = self.dialog_data
            node.setText(0, ' '.join((DTDSTART, ed.getshortname(dtd))))
            node.setData(0, core.Qt.UserRole, dtd.rstrip())
            self.has_dtd = True
        self.adjust_dtd_menu()
        self.mark_dirty(True)
        self.refresh_preview()
        self.tree.scrollToItem(self.top.child(0))

    def add_css(self, evt=None):
        "start toevoegen stylesheet m.b.v. dialoog"
        edt = CssDialog(self).exec_()
        if edt != gui.QDialog.Accepted:
            return
        data = self.dialog_data
        # determine the place to put the sylesheet
        self.item = None
        for ix in range(self.top.childCount()):
            item = self.top.child(ix)
            if item.text(0) == ' '.join((ELSTART, 'html')):
                for ix in range(item.childCount()):
                    sub = item.child(ix)
                    if sub.text(0) == ' '.join((ELSTART, 'head')):
                        self.item = sub
        if not self.item:
            gui.QMessageBox.information(self, self.title,
                "Error: no <head> element")
            return
        # create the stylesheet node
        node = gui.QTreeWidgetItem()
        if 'href' in data:
            node.setText(0, ed.getelname('link', data))
            subnode = None
        else:
            node.setText(0, ed.getelname('style', data))
            cssdata = data.pop('cssdata')
            subnode = gui.QTreeWidgetItem()
            subnode.setText(0, ed.getshortname(cssdata))
            subnode.setData(0, core.Qt.UserRole, cssdata)
            node.addChild(subnode)
        node.setData(0, core.Qt.UserRole, data)
        self.item.addChild(node)
        self.mark_dirty(True)
        self.refresh_preview()

    def add_link(self, evt=None):
        "start toevoegen link m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox.information(self, self.title, "Can't do this below text")
            return
        edt = LinkDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            txt, data = self.dialog_data
            node = gui.QTreeWidgetItem()
            node.setText(0, ed.getelname('a', data))
            node.setData(0, core.Qt.UserRole, data)
            self.item.addChild(node)
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, ed.getshortname(txt))
            new_item.setData(0, core.Qt.UserRole, txt)
            node.addChild(new_item)
            self.mark_dirty(True)
            self.refresh_preview()

    def add_image(self, evt=None):
        "start toevoegen image m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox.information(self, self.title, "Can't do this below text")
            return
        edt = ImageDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            data = self.dialog_data
            node = gui.QTreeWidgetItem()
            node.setText(0, ed.getelname('img', data))
            node.setData(0, core.Qt.UserRole, data)
            self.item.addChild(node)
            self.mark_dirty(True)
            self.refresh_preview()

    def add_video(self, evt=None):
        "start toevoegen video m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox.information(self, self.title, "Can't do this below text")
            return
        edt = VideoDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            data = self.dialog_data
            data['controls'] = ''
            src = data.pop('src')
            node = gui.QTreeWidgetItem()
            node.setText(0, ed.getelname('video', data))
            node.setData(0, core.Qt.UserRole, data)
            self.item.addChild(node)
            child = gui.QTreeWidgetItem()
            child_data = {'src': src,
                'type': 'video/{}'.format(os.path.splitext(src)[1][1:])}
            child.setText(0, ed.getelname('source', child_data))
            child.setData(0, core.Qt.UserRole, child_data)
            node.addChild(child)
            self.mark_dirty(True)
            self.refresh_preview()

    def add_audio(self, evt=None):
        "start toevoegen audio m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox.information(self, self.title, "Can't do this below text")
            return
        edt = AudioDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            data = self.dialog_data
            data['controls'] = ''
            node = gui.QTreeWidgetItem()
            node.setText(0, ed.getelname('audio', data))
            node.setData(0, core.Qt.UserRole, data)
            self.item.addChild(node)
            self.mark_dirty(True)
            self.refresh_preview()

    def add_list(self, evt=None):
        "start toevoegen list m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox("Can't do this below text", self.title)
            return
        edt = ListDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            list_type, list_data = self.dialog_data
            itemtype = "dt" if list_type == "dl" else "li"
            new_item = gui.QTreeWidgetItem()
            self.item.addChild(new_item)
            new_item.setText(0, ed.getelname(list_type))

            for list_item in list_data:
                new_subitem = gui.QTreeWidgetItem()
                new_item.addChild(new_subitem)
                new_subitem.setText(0, ed.getelname(itemtype))
                data = list_item[0]
                node = gui.QTreeWidgetItem()
                new_subitem.addChild(node)
                node.setText(0, ed.getshortname(data))
                node.setData(0, core.Qt.UserRole, data)
                if list_type == "dl":
                    new_subitem = gui.QTreeWidgetItem()
                    new_item.addChild(new_subitem)
                    new_subitem.setText(0, ed.getelname('dd'))
                    data = list_item[1]
                    node = gui.QTreeWidgetItem()
                    new_subitem.addChild(node)
                    node.setText(0, ed.getshortname(data))
                    node.setData(0, core.Qt.UserRole, data)
            self.mark_dirty(True)
            self.refresh_preview()

    def add_table(self, evt=None):
        "start toevoegen tabel m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox("Can't do this below text", self.title)
            return
        edt = TableDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            summary, titles, headers, items = self.dialog_data
            new_item = gui.QTreeWidgetItem()
            self.item.addChild(new_item)
            data = {'summary': summary}
            new_item.setText(0, ed.getelname('table', data))
            new_item.setData(0, core.Qt.UserRole, data)
            if titles:
                new_row = gui.QTreeWidgetItem()
                new_item.addChild(new_row)
                new_row.setText(0, ed.getelname('tr'))
                for head in headers:
                    new_head = gui.QTreeWidgetItem()
                    new_row.addChild(new_head)
                    new_head.setText(0, ed.getelname('th'))
                    node = gui.QTreeWidgetItem()
                    new_head.addChild(node)
                    text = head or BL
                    node.setText(0, ed.getshortname(text))
                    node.setData(0, core.Qt.UserRole, text)
            for rowitem in items:
                new_row = gui.QTreeWidgetItem()
                new_item.addChild(new_row)
                new_row.setText(0, ed.getelname('tr'))
                for cellitem in rowitem:
                    new_cell = gui.QTreeWidgetItem()
                    new_row.addChild(new_cell)
                    new_cell.setText(0, ed.getelname('td'))
                    text = cellitem
                    node = gui.QTreeWidgetItem()
                    new_cell.addChild(node)
                    node.setText(0, ed.getshortname(text))
                    node.setData(0, core.Qt.UserRole, text)
            self.mark_dirty(True)
            self.refresh_preview()

    def validate(self, evt=None):
        if self.tree_dirty or not self.xmlfn:
            htmlfile = '/tmp/ashe_check.html'
            fromdisk = False
            self.data2soup()
            with open(htmlfile, "w") as f_out:
                f_out.write(self.soup.prettify())
        else:
            htmlfile = self.xmlfn
            fromdisk = True
        dlg = ScrolledTextDialog(self, "Validation output", htmlfile=htmlfile,
            fromdisk=fromdisk)
        dlg.show()

    def view_code(self, evt=None):
        self.data2soup()
        dlg = CodeViewDialog(self, "Source view", "Let op: de tekst wordt niet "
            "ververst bij wijzigingen in het hoofdvenster", self.soup.prettify())
        dlg.show()

def ashe_gui(args):
    "start main GUI"
    fname = ''
    if len(args) > 1:
        fname = args[1]
        if fname and not os.path.exists(fname):
            print('Kan file {} niet openen, '
                'geef s.v.p. een absoluut pad op\n'.format(fname))
    app = gui.QApplication(sys.argv)
    if fname:
        frm = MainFrame(None, -1, fname = fname)
    else:
        frm = MainFrame(None, -1)
    frm.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    ashe_gui(sys.argv)
