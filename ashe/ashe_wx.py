"""wxPython versie van een op een treeview gebaseerde HTML-editor

startfunctie en hoofdscherm
"""
import os
import sys
import wx
import wx.html as html
from wx.lib.dialogs import ScrolledMessageDialog
import bs4 as bs  # BeautifulSoup as bs

import ashe.ashe_mixin as ed
from ashe.ashe_dialogs_wx import cssedit_available, HMASK, ElementDialog, \
    TextDialog, DtdDialog, CssDialog, LinkDialog, ImageDialog, VideoDialog, \
    AudioDialog, ListDialog, TableDialog, ScrolledTextDialog, CodeViewDialog, \
    SearchDialog

# HMASK = "HTML files (*.htm,*.html)|*.htm;*.html|All files (*.*)|*.*"
# IMASK = "All files|*.*"


PPATH = os.path.split(__file__)[0]
DESKTOP = ed.DESKTOP
CMSTART = ed.CMSTART
ELSTART = ed.ELSTART
CMELSTART = ed.CMELSTART
DTDSTART = ed.DTDSTART
BL = ed.BL
TITEL = ed.TITEL


def comment_out(node, commented, tree):
    "subitem(s) (ook) op commentaar zetten"
    subnode, pos = tree.GetFirstChild(node)
    while subnode.IsOk():
        txt = tree.GetItemText(subnode)
        if commented:
            if not txt.startswith(CMSTART):
                tree.SetItemText(subnode, " ".join((CMSTART, txt)))
        else:
            if txt.startswith(CMSTART):
                tree.SetItemText(subnode, txt.split(None, 1)[1])
        comment_out(subnode, commented, tree)
        subnode, pos = tree.GetNextChild(node, pos)


class MainFrame(wx.Frame, ed.EditorMixin):
    "Main GUI"

    def __init__(self, parent, _id, fname=''):
        self.parent = parent
        self.title = "(untitled) - Albert's Simple HTML Editor"
        self.xmlfn = fname
        self.tree_dirty = False
        self.cut_el = self.cut_txt = None
        dsp = wx.Display().GetClientArea()
        high = dsp.height if dsp.height < 900 else 900
        wide = dsp.width if dsp.width < 1020 else 1020
        wx.Frame.__init__(self, parent, _id, pos=(dsp.top, dsp.left), size=(wide, high))
        self.SetIcon(wx.Icon(os.path.join(PPATH, "ashe.ico"), wx.BITMAP_TYPE_ICO))

        self.setup_menu()

        self.pnl = wx.SplitterWindow(self, -1)  # , style=wx.NO_3D)
        self.pnl.SetMinimumPaneSize(1)

        self.tree = wx.TreeCtrl(self.pnl, -1)
        ## isz = (16, 16)
        ## il = wx.ImageList(isz[0], isz[1])
        ## fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        ## fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        ## fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        ## self.tree.SetImageList(il)
        ## self.il = il
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.on_leftdclick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        ## self.tree.Bind(wx.EVT_CONTEXT_MENU, self.onContextMenu)
        self.tree.Bind(wx.EVT_CHAR, self.on_char)
        self.tree.Bind(wx.EVT_KEY_UP, self.on_key)

        self.html = html.HtmlWindow(self.pnl, -1)
        if "gtk2" in wx.PlatformInfo:
            self.html.SetStandardFonts()

        self.pnl.SplitVertically(self.tree, self.html)
        self.pnl.SetSashPosition(400, True)

        self.sb = wx.StatusBar(self)
        self.SetStatusBar(self.sb)

        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.tree, 1, wx.EXPAND)
        sizer0.Add(sizer1, 1, wx.EXPAND)

        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)
        self.tree.SetFocus()
        self.Bind(wx.EVT_CLOSE, self.exit)

        self.err = ed.EditorMixin.getsoup(self, fname)
        self.adv_menu.Check()
        if not self.err:
            self.refresh_preview()

    def setup_menu(self):
        """build application menu
        """
        self.menulist = self.get_menulist()
        self.menu_id = {}
        menu_bar = wx.MenuBar()
        for menu_text, data in self.menulist:
            menu = wx.Menu()
            for item in data:
                if len(item) > 1:
                    menuitem_text, hotkey, modifiers, status_text, callback = item[:5]
                    if 'A' in modifiers:
                        hotkey = "-".join(("Alt", hotkey))
                    if 'C' in modifiers:
                        hotkey = "-".join(("Ctrl", hotkey))
                    if 'S' in modifiers:
                        hotkey = "-".join(("Shift", hotkey))
                    self.menu_id[menuitem_text] = wx.NewId()
                    caption = menuitem_text.ljust(40) + hotkey
                    if menuitem_text.startswith('Advance selection'):
                        self.adv_menu = menu.Append(self.menu_id[menuitem_text], caption,
                                                    status_text, True)  # checkable=True)
                    else:
                        mnu = menu.Append(self.menu_id[menuitem_text], caption, status_text)
                        if menuitem_text == 'Add DTD':
                            self.dtd_menu = mnu
                    self.Connect(self.menu_id[menuitem_text], -1, wx.wxEVT_COMMAND_MENU_SELECTED,
                                 callback)
                else:
                    menu.AppendSeparator()
            menu_bar.Append(menu, menu_text)
        self.SetMenuBar(menu_bar)

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
                           ('E&xit', 'Q', 'C', 'Quit the application', self.quit))),
                ('&View', (('Expand All (sub)Levels', '+', 'C', "Show what's beneath "
                            "the current element", self.expand, True),
                           ('Collapse All (sub)Levels', '-', 'C', "Hide what's beneath "
                            "the current element", self.collapse, True),
                           ('sep1', ),
                           ('Advance selection on add/insert', '', '', "Move the selection to the "
                            "added/pasted item", self.advance_selection_onoff))),
                ('&Edit', (('Edit', 'F2', '', 'Modify the element/text and/or its attributes',
                            self.edit),
                           ('Comment/Uncomment', '#', 'C', 'Comment (out) the current item and '
                            'everything below', self.comment),
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
                           ('Insert Text before', 'Ins', 'SC', 'Add a text node before the current '
                            'one', self.add_text),
                           ('Insert Text after', 'Ins', 'SA', 'Add a text node after the current '
                            'one', self.add_text_after),
                           ('Insert Element Before', 'Ins', 'C', 'Add a new element in front of the '
                            'current', self.insert),
                           ('Insert Element After', 'Ins', 'A', 'Add a new element after the current',
                            self.insert_after),
                           ('Insert Element Under', 'Ins', '', 'Add a new element under the current',
                            self.insert_child))),
                ("&HTML", (('Add DTD', '', '', 'Add a document type description', self.add_dtd),
                           ('Create link (under)', '', '', 'Add a document reference', self.add_link),
                           ('Add image (under)', '', '', 'Include an image', self.add_image),
                           ('Add list (under)', '', '', 'Create a list', self.add_list),
                           ('Add table (under)', '', '', 'Create a table', self.add_table),
                           ('sep1', ),
                           ('Check syntax', '', '', 'Validate HTML with Tidy', self.validate))),
                ("Help", (('&About', '', '', 'Info about this application', self.about), )))

    def check_tree(self):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)"""
        if self.tree_dirty:
            hlp = wx.MessageBox("HTML data has been modified - save before continuing?", self.title,
                                style=wx.YES_NO | wx.CANCEL)
            if hlp == wx.ID_YES:
                self.savexml()
            return hlp
        return None

    def quit(self, evt=None):
        "exit program"
        ## if self.check_tree() != wx.CANCEL:
        self.Close()

    def exit(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna afsluiten"""
        if self.check_tree() != wx.CANCEL:
            self.Destroy()

    def newxml(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna nieuwe html aanmaken"""
        if self.check_tree() != wx.CANCEL:
            ed.EditorMixin.getsoup(self, fname=None)
            self.adv_menu.Check()
            self.sb.SetStatusText("started new document")
            self.refresh_preview()

    def openxml(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna een html bestand kiezen"""
        if self.check_tree() != wx.CANCEL:
            loc = os.path.dirname(self.xmlfn) if self.xmlfn else os.getcwd()
            with wx.FileDialog(self, message="Choose a file", defaultDir=loc, wildcard=HMASK,
                               style=wx.FD_OPEN) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    ed.EditorMixin.getsoup(self, fname=dlg.GetPath())
                    self.adv_menu.Check()
                    self.sb.SetStatusText("loaded {}".format(self.xmlfn))
                    self.refresh_preview()

    def savexml(self, evt=None):
        "save html to file"
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.data2soup()
            try:
                self.soup2file()
            except IOError as err:
                wx.MessageBox(self.title, err, wx.OK | wx.ICON_INFORMATION)
            else:
                self.sb.SetStatusText("saved {}".format(self.xmlfn))

    def savexmlas(self, evt=None):
        """vraag bestand om html op te slaan
        bestand opslaan en naam in titel en root element zetten"""
        if self.xmlfn:
            dname, fname = os.path.split(self.xmlfn)
        else:
            dname = os.getcwd()
            fname = ""
        with wx.FileDialog(self, message="Save file as ...", defaultDir=dname, defaultFile=fname,
                           wildcard=HMASK, style=wx.FD_SAVE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.xmlfn = dlg.GetPath()
                self.data2soup()
                try:
                    self.soup2file(saveas=True)
                except IOError as err:
                    ## dlg.Destroy()
                    wx.MessageBox(self.title, err, wx.OK | wx.ICON_INFORMATION)
                    return
                self.tree.SetItemText(self.top, self.xmlfn)
                self.SetTitle(" - ".join((os.path.basename(self.xmlfn), TITEL)))
                self.sb.SetStatusText("saved as {}".format(self.xmlfn))
            ## dlg.Destroy()

    def reopenxml(self, evt=None):
        """onvoorwaardelijk html bestand opnieuw laden"""
        err = ed.EditorMixin.getsoup(self, fname=self.xmlfn)
        if not err:
            self.adv_menu.Check()
            self.sb.SetStatusText("reloaded {}".format(self.xmlfn))
            self.refresh_preview()
        else:
            wx.MessageBox(self.title, err, wx.OK | wx.INFORMATION)

    def advance_selection_onoff(self, event=None):
        "callback for menu option"
        self.advance_selection_on_add = not self.advance_selection_on_add
        self.adv_menu.Check(self.advance_selection_on_add)

    def mark_dirty(self, state):
        "update visual signs that the source has changed"
        ed.EditorMixin.mark_dirty(self, state)
        title = self.GetTitle()
        if state:
            if not title.endswith(' *'):
                title = title + ' *'
        else:
            title = title.rstrip(' *')
        self.SetTitle(title)

    def refresh_preview(self):
        """update display
        """
        self.data2soup()
        self.data_file = os.path.join(PPATH, "tempfile.html")
        with open(self.data_file, "w") as f_out:
            f_out.write(str(self.soup).replace('%SOUP-ENCODING%', 'utf-8'))
        self.html.LoadPage(self.data_file)
        self.tree.SetFocus()

    def about(self, evt=None):
        "toon programma info"
        abouttext = ed.EditorMixin.about(self)
        wx.MessageBox(abouttext, self.title, wx.OK | wx.ICON_INFORMATION)

    def addtreeitem(self, node, naam, data):
        """itemnaam en -data toevoegen aan de interne tree
        referentie naar treeitem teruggeven"""
        newnode = self.tree.AppendItem(node, naam)
        self.tree.SetItemData(newnode, data)
        return newnode

    def addtreetop(self, fname, titel):
        """titel en root item in tree instellen"""
        self.SetTitle(titel)
        self.top = self.tree.AddRoot(fname)

    def init_tree(self, name=''):
        "nieuwe tree initialiseren"
        self.tree.DeleteAllItems()
        ed.EditorMixin.init_tree(self, name)
        self.adjust_dtd_menu()
        if DESKTOP:
            self.tree.SelectItem(self.top)

    def data2soup(self):
        "interne tree omzetten in BeautifulSoup object"
        def expandnode(node, root, data, commented=False):
            "tree item (node) met inhoud (data) toevoegen aan BS node (root)"
            try:
                for att in data:
                    root[att] = data[att]
            except TypeError:
                pass
            elm, pos = self.tree.GetFirstChild(node)
            while elm.IsOk():
                text = self.tree.GetItemText(elm)
                data = self.tree.GetItemData(elm)
                if text.startswith(ELSTART) or text.startswith(CMELSTART):
                    if text.startswith(CMSTART):
                        text = text.split(None, 1)[1]
                        if not commented:
                            is_comment = True
                            soup = bs.BeautifulSoup('', 'lxml')
                            sub = soup.new_tag(text.split()[1])
                            expandnode(elm, sub, data, is_comment)
                            sub = bs.Comment(str(sub))  # .decode("latin-1"))    # why decode?
                        else:
                            is_comment = False
                            sub = self.soup.new_tag(text.split()[1])
                    else:
                        is_comment = False
                        sub = self.soup.new_tag(text.split()[1])
                    root.append(sub)  # insert(0,sub)
                    if not is_comment:
                        expandnode(elm, sub, data, commented)
                else:
                    #  dit levert fouten op bij het gebruiken van diacrieten
                    ## sub = bs.NavigableString(.ed.escape(data))
                    ## root.append(sub) # insert(0,sub)
                    #  dit niet maar er wordt niet correct gecodeerd
                    ## root.append(ed.escape(data))
                    #  misschien dat dit het doet
                    sub = bs.NavigableString(data)  # .decode("latin-1"))    # again, why? Python 2?
                    if text.startswith(CMSTART) and not commented:
                        sub = bs.Comment(data)  # .decode("latin-1"))
                    root.append(sub)  # data.decode("latin-1")) # insert(0,sub)
                elm, pos = self.tree.GetNextChild(node, pos)
        self.soup = bs.BeautifulSoup('', 'lxml')  # self.root.originalEncoding)
        tag, pos = self.tree.GetFirstChild(self.top)
        while tag.IsOk():
            text = self.tree.GetItemText(tag)
            data = self.tree.GetItemData(tag)
            if text.startswith(DTDSTART):
                root = bs.Declaration(data)
                self.soup.append(root)
            elif text.startswith(ELSTART):
                root = self.soup.new_tag(text.split(None, 2)[1])
                self.soup.append(root)
                expandnode(tag, root, data)
            tag, pos = self.tree.GetNextChild(self.top, pos)

    def on_leftdclick(self, evt=None):
        "start edit bij dubbelklikken tenzij op filenaam"
        item = self.tree.HitTest(evt.GetPosition())[0]
        if item:
            if item == self.top:
                edit = False
            else:
                data = self.tree.GetItemText(item)
                edit = True
                if data.startswith(ELSTART):
                    if self.tree.GetChildrenCount(item):
                        edit = False
        if edit:
            self.edit()
        evt.Skip()

    def on_rightdown(self, evt=None):
        "context menu bij rechtsklikken"
        item = self.tree.HitTest(evt.GetPosition())[0]
        if item and item != self.top:
            self.contextmenu(item)

    def adjust_dtd_menu(self):
        "set text for dtd menu option"
        if self.has_dtd:
            self.dtd_menu.SetText('Remove DTD')
            self.dtd_menu.SetHelp('Remove the document type declaration')
        else:
            self.dtd_menu.SetText('Add DTD')
            self.dtd_menu.SetHelp('Add a document type description')
        ## value = not self.has_dtd
        ## self.dtd_menu.Enable(value)

    def contextmenu(self, item, pos=None):
        'show context menu'
        self.tree.SelectItem(item)
        itemtext = self.tree.GetItemText(item)
        menu = wx.Menu()
        for menu_item in self.menulist[1][1]:
            if menu_item[0].startswith('sep'):
                menu.AppendSeparator()
            elif not menu_item[0].startswith('Advance selection'):
                menu.Append(self.menu_id[menu_item[0]], menu_item[0])
        for menu_text, data in self.menulist[2:4]:
            submenu = wx.Menu()
            for dataitem in data:
                if len(dataitem) == 1:
                    submenu.AppendSeparator()
                elif len(dataitem) < 6 or itemtext.startswith(ELSTART):
                    menu_item = submenu.Append(self.menu_id[dataitem[0]], dataitem[0])
                    if dataitem[0] == 'Add DTD' and self.has_dtd:
                        menu_item.Enable(False)
            menu.AppendMenu(-1, menu_text, submenu)
        if pos:
            self.PopupMenu(menu, pos=pos)
        else:
            self.PopupMenu(menu)
        menu.Destroy()

    def on_key(self, event):
        """afhandeling toetscombinaties"""
        skip = True
        keycode = event.GetKeyCode()
        mods = event.GetModifiers()
        mods_ok = {'': 0, 'C': wx.MOD_CONTROL, 'A': wx.MOD_ALT, 'S': wx.MOD_SHIFT,
                   'CA': wx.MOD_CONTROL | wx.MOD_ALT, 'SC': wx.MOD_CONTROL | wx.MOD_SHIFT,
                   'SA': wx.MOD_SHIFT | wx.MOD_ALT}
        win = event.GetEventObject()
        ## if keycode == wx.WXK_ESCAPE and isinstance(win, html.HtmlWindow):
            ## win.Unbind(wx.EVT_KEY_UP)
            ## self.tree.Bind(wx.EVT_KEY_UP, self.on_key)
            ## event.Skip()
        if keycode == wx.WXK_MENU:
            ## if win == self.tree:
            item = self.tree.Selection
            if item != self.top:
                rect = self.tree.GetBoundingRect(item)
                pos = (rect.GetLeft() + 20, rect.GetBottom())
                self.contextmenu(item, pos=pos)
                return
        for menu, data in self.menulist:
            for submenu in data:
                if len(submenu) < 2 or submenu[1] == '':
                    continue
                go_on = False
                if submenu[1] == 'F2':
                    if keycode == wx.WXK_F2:
                        go_on = True
                elif submenu[1] == 'Ins':
                    if keycode == wx.WXK_INSERT:
                        go_on = True
                elif submenu[1] == 'Del':
                    if keycode == wx.WXK_DELETE:
                        go_on = True
                elif ord(submenu[1]) == keycode:
                    go_on = True
                if go_on and mods != mods_ok[submenu[2]]:
                    go_on = False
                if submenu[1] == '#' and keycode == 51 and mods == mods_ok['SC']:
                    go_on = True
                if go_on:
                    if keycode in (wx.WXK_DELETE, wx.WXK_INSERT, ord('X'), ord('C'), ord('+'),
                                   ord('-')) and win != self.tree:
                        go_on = False
                    else:
                        submenu[4]()
        if event and skip:
            event.Skip()

    def on_char(self, event):
        """speciale afhandeling voor Ctrl-+.
        Deze kan namelijk alleen worden geproduceerd met een modifier (shift of num_keypad)
        en bij EVT_KEY_DOWN wordt de modifier opgevangen en niet de + waarde.
        Daarom zit deze op de EVT_CHAR. Als enige, want het bleek dat de meeste andere dan
        juist weer niet werken."""
        skip = True
        keycode = event.GetKeyCode()
        mods = event.GetModifiers()
        win = event.GetEventObject()
        if keycode == ord("+") and win == self.tree:
            if mods == wx.MOD_CONTROL or mods == wx.MOD_CONTROL | wx.MOD_SHIFT:
                self.expand()
        if skip:
            event.Skip()

    def checkselection(self):
        "controleer of er wel iets geselecteerd is (behalve de filenaam)"
        sel = True
        self.item = self.tree.Selection
        if self.item is None or self.item == self.top:
            wx.MessageBox('You need to select an element or text first', self.title)
            sel = False
        return sel

    def expand(self, evt=None):
        "expandeer tree vanaf huidige item"
        item = self.tree.Selection
        if item:
            self.tree.ExpandAllChildren(item)

    def collapse(self, evt=None):
        "collapse huidige item en daaronder"
        item = self.tree.Selection
        if item:
            self.tree.CollapseAllChildren(item)

    def comment(self, evt=None):
        "(un)comment zonder de edit dialoog"
        if DESKTOP and not self.checkselection():
            return
        tag = self.tree.GetItemText(self.item)
        attrs = self.tree.GetItemData(self.item)
        commented = tag.startswith(CMSTART)
        if commented:
            _, tag = tag.split(None, 1)  # CMSTART eraf halen
        parent = self.tree.GetItemParent(self.item)
        text = self.tree.GetItemText(parent)
        under_comment = text.startswith(CMSTART)
        commented = not commented  # het (un)commenten uitvoeren
        if under_comment:
            commented = True
        print("in comment:", tag, attrs)
        if tag.startswith(ELSTART):
            _, tag = tag.split(None, 1)  # ELSTART eraf halen
            self.tree.SetItemText(self.item, ed.getelname(tag, attrs, commented))
            self.tree.SetItemData(self.item, attrs)
            comment_out(self.item, commented, self.tree)
        else:
            ## txt = CMSTART + " " + tag if commented else tag
            self.tree.SetItemText(self.item, ed.getshortname(tag, commented))
            self.tree.SetItemData(self.item, tag)

    def edit(self, evt=None):
        "start edit m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemText(self.item)
        parent = self.tree.GetItemParent(self.item)
        text = self.tree.GetItemText(parent)
        under_comment = text.startswith(CMSTART)
        modified = False
        if data.startswith(ELSTART) or data.startswith(CMELSTART):
            attrdict = self.tree.GetItemData(self.item)
            was_commented = data.startswith(CMSTART)
            edt = ElementDialog(self, title='Edit an element', tag=data, attrs=attrdict)
            if edt.ShowModal() == wx.ID_SAVE:
                modified = True
                tag = edt.tag_text.GetValue()
                commented = edt.comment_button.GetValue()
                attrs = {}
                for i in range(edt.attr_table.GetNumberRows()):
                    attrs[edt.attr_table.GetCellValue(i, 0)] = edt.attr_table.GetCellValue(i, 1)
                if under_comment:
                    commented = True
                if tag != data or attrs != attrdict:
                    self.tree.SetItemText(self.item, ed.getelname(tag, attrs, commented))
                self.tree.SetItemData(self.item, attrs)
                if commented != was_commented:
                    comment_out(self.item, commented, self.tree)
        else:
            txt = CMSTART + " " if data.startswith(CMSTART) or under_comment else ""
            data = self.tree.GetItemData(self.item)
            edt = TextDialog(self, title='Edit Text', text=txt + data)
            if edt.ShowModal() == wx.ID_SAVE:
                modified = True
                txt = edt.data_text.GetValue()
                commented = edt.comment_button.GetValue()
                if under_comment:
                    commented = True
                self.tree.SetItemText(self.item, ed.getshortname(txt, commented))
                self.tree.SetItemData(self.item, txt)
        if modified:
            self.mark_dirty(True)
            self.refresh_preview()
        edt.Destroy()

    def _copy(self, cut=False, retain=True, ifcheck=True):
        "start copy/cut/delete actie"
        def push_el(elm, result):
            "subitem(s) toevoegen aan copy buffer"
            text = self.tree.GetItemText(elm)
            data = self.tree.GetItemData(elm)
            atrlist = []
            if text.startswith(ELSTART):
                node, pos = self.tree.GetFirstChild(elm)
                while node.IsOk():
                    push_el(node, atrlist)
                    node, pos = self.tree.GetNextChild(elm, pos)
            result.append((text, data, atrlist))
            return result
        if DESKTOP and not self.checkselection():
            return
        text = self.tree.GetItemText(self.item)
        data = self.tree.GetItemData(self.item)
        txt = 'cut' if cut else 'copy'
        if data == self.root:
            wx.MessageBox("Can't %s the root" % txt, self.title)
            return
        if isinstance(data, str) and data.startswith(DTDSTART):
            wx.MessageBox("use the HTML menu's DTD option", self.title)
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
            prev = self.tree.GetPrevSibling(self.item)
            if not prev.IsOk():
                prev = self.tree.GetItemParent(self.item)
                if self.tree.GetItemData(prev) == self.root:
                    prev = self.tree.GetNextSibling(self.item)
            self.tree.Delete(self.item)
            self.mark_dirty(True)
            self.tree.SelectItem(prev)
            self.refresh_preview()

    def cut(self, evt=None):
        "cut = copy with removing item from tree"
        self._copy(cut=True)

    def delete(self, evt=None, ifcheck=True):
        "delete = copy with removing item from tree and memory"
        self._copy(cut=True, retain=False, ifcheck=ifcheck)

    def copy(self, evt=None):
        "copy = transfer item to memory"
        self._copy()

    def _paste(self, before=True, below=False):
        "start paste actie"
        def zetzeronder(node, elm, pos=-1):
            "paste copy buffer into tree"
            if pos == -1:
                subnode = self.tree.AppendItem(node, elm[0])
                self.tree.SetItemData(subnode, elm[1])
            else:
                subnode = self.tree.InsertItem(node, pos, elm[0])
                self.tree.SetItemData(subnode, elm[1])
            for item in elm[2]:
                zetzeronder(subnode, item)
            return subnode
        if not self.cut_el and not self.cut_txt:
            wx.MessageBox('Nothing to paste', self.title)
            return
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemData(self.item)
        if below:
            text = self.tree.GetItemText(self.item)
            if text.startswith(CMSTART):
                wx.MessageBox("Can't paste below comment", self.title)
                return
            if not text.startswith(ELSTART):
                wx.MessageBox("Can't paste below text", self.title)
                return
        if data == self.root:
            if before:
                wx.MessageBox("Can't paste before the root", self.title)
                return
            else:
                wx.MessageBox("Pasting as first element below root", self.title)
                below = True
        if self.cut_txt:
            item = ed.getshortname(self.cut_txt)
            data = self.cut_txt
            if below:
                node = self.tree.AppendItem(self.item, item)
                self.tree.SetItemData(node, data)
            else:
                add_to = self.tree.GetItemParent(self.item)
                added = False
                chld, pos = self.tree.GetFirstChild(add_to)
                for idx in range(self.tree.GetChildrenCount(add_to)):
                    if chld == self.item:
                        if not before:
                            idx += 1
                        node = self.tree.InsertItemBefore(add_to, idx, item)
                        self.tree.SetItemData(node, data)
                        added = True
                        break
                    chld, pos = self.tree.GetNextChild(add_to, pos)
                if not added:
                    node = self.tree.AppendItem(add_to, item)
                    self.tree.SetItemData(node, data)
            if self.advance_selection_on_add:
                self.tree.SelectItem(node)
        elif self.cut_el:
            if below:
                node = self.item
                idx = -1
            else:
                node = self.tree.GetItemParent(self.item)
                item, pos = self.tree.GetFirstChild(node)
                cnt = self.tree.GetChildrenCount(node)
                for idx in range(cnt):
                    if item == self.item:
                        if not before:
                            idx += 1
                        break
                    item, pos = self.tree.GetNextChild(node, pos)
                if idx == cnt:
                    idx -= 1
            new_item = zetzeronder(node, self.cut_el[0], idx)
            if self.advance_selection_on_add:
                self.tree.SelectItem(new_item)
        self.mark_dirty(True)
        self.refresh_preview()

    def paste(self, evt=None):
        "paste before"
        self._paste()

    def paste_after(self, evt=None):
        "paste after instead of before"
        self._paste(before=False)

    def paste_below(self, evt=None):
        "paste below instead of before"
        self._paste(below=True)

    def _insert(self, before=True, below=False):
        "start invoeg actie"
        if DESKTOP and not self.checkselection():
            return
        if below:
            text = self.tree.GetItemText(self.item)
            if text.startswith(CMSTART):
                wx.MessageBox("Can't insert below comment", self.title)
                return
            if not text.startswith(ELSTART) and not text.startswith(CMELSTART):
                wx.MessageBox("Can't insert below text", self.title)
                return
            under_comment = text.startswith(CMSTART)
            where = "under"
        elif before:
            where = "before"
        else:
            where = "after"
        edt = ElementDialog(self, title="New element (insert {0})".format(where))
        if edt.ShowModal() == wx.ID_SAVE:
            tag = edt.tag_text.GetValue()
            attrs = {}
            for idx in range(edt.attr_table.GetNumberRows()):
                attrs[edt.attr_table.GetCellValue(idx, 0)] = edt.attr_table.GetCellValue(idx, 1)
            data = attrs
            commented = edt.comment_button.GetValue()
            if below:
                text = self.tree.GetItemText(self.item)
                under_comment = text.startswith(CMSTART)
                text = ed.getelname(tag, data, commented or under_comment)
                item = self.tree.AppendItem(self.item, text)
                self.tree.SetItemData(item, data)
                self.tree.Expand(self.item)
                if self.advance_selection_on_add:
                    self.tree.SelectItem(item)
            else:
                parent = self.tree.GetItemParent(self.item)
                text = self.tree.GetItemText(parent)
                under_comment = text.startswith(CMSTART)
                text = ed.getelname(tag, data, commented or under_comment)
                item = self.item if not before else self.tree.GetPrevSibling(self.item)
                node = self.tree.InsertItem(parent, item, text)
                self.tree.SetItemData(node, data)
                if self.advance_selection_on_add:
                    self.tree.SelectItem(node)
            self.mark_dirty(True)
            self.refresh_preview()
        edt.Destroy()

    def insert(self, evt=None):
        "insert element before"
        self._insert()

    def insert_after(self, evt=None):
        "insert element after instead of before"
        self._insert(before=False)

    def insert_child(self, evt=None):
        "insert element below instead of before"
        self._insert(below=True)

    def _add_text(self, before=True, below=False):
        "tekst toevoegen onder huidige element"
        if DESKTOP and not self.checkselection():
            return
        if below and not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't insert below text", self.title)
            return
        edt = TextDialog(self, title="New Text")
        if edt.ShowModal() == wx.ID_SAVE:
            txt = edt.data_text.GetValue()
            commented = edt.comment_button.GetValue()
            if below:
                text = self.tree.GetItemText(self.item)
                under_comment = text.startswith(CMSTART)
                text = ed.getshortname(txt, commented or under_comment)
                new_item = self.tree.AppendItem(self.item, text)
            else:
                parent = self.tree.GetItemParent(self.item)
                text = self.tree.GetItemText(parent)
                under_comment = text.startswith(CMSTART)
                text = ed.getshortname(txt, commented or under_comment)
                item = self.item if not before else self.tree.GetPrevSibling(self.item)
                new_item = self.tree.InsertItem(parent, item, text)
            if self.advance_selection_on_add:
                self.tree.SelectItem(new_item)
            self.tree.SetItemData(new_item, txt)
            self.mark_dirty(True)
            self.refresh_preview()
            self.tree.Expand(self.item)
        edt.Destroy()

    def add_text(self, evt=None):
        "insert text before"
        self._add_text()

    def add_text_after(self, evt=None):
        "insert text after instead of before"
        self._add_text(before=False)

    def add_textchild(self, evt=None):
        "insert text below instead of before"
        self._add_text(below=True)

    def add_dtd(self, evt=None):
        "start toevoegen dtd m.b.v. dialoog"
        if self.has_dtd:
            item, pos = self.tree.GetFirstChild(self.top)
            ## print self.tree.GetItemText(item)
            self.tree.Delete(item)
            self.mark_dirty(True)
            self.has_dtd = False
            self.adjust_dtd_menu()
            self.refresh_preview()
            return
        edt = DtdDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            for cap, dtd, radio in edt.dtd_list:
                if radio and radio.GetValue():
                    node = self.tree.InsertItem(self.top, 0, ed.getshortname(dtd))
                    self.tree.SetItemData(node, dtd.rstrip())
                    self.has_dtd = True
                    self.adjust_dtd_menu()
                    self.mark_dirty(True)
                    self.refresh_preview()
                    break
        edt.Destroy()

    def add_link(self, evt=None):
        "start toevoegen link m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't do this below text", self.title)
            return
        edt = LinkDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            data = {"href": edt.link, "title": edt.title_text.GetValue()}
            node = self.tree.AppendItem(self.item, ed.getelname('a', data))
            self.tree.SetItemData(node, data)
            txt = edt.text_text.GetValue()
            new_item = self.tree.AppendItem(node, ed.getshortname(txt))
            self.tree.SetItemData(new_item, txt)
            self.mark_dirty(True)
            self.refresh_preview()
        edt.Destroy()

    def add_image(self, evt=None):
        "start toevoegen image m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't do this below text", self.title)
            return
        edt = ImageDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            data = {"src": edt.link, "alt": edt.alt_text.GetValue(),
                    "title": edt.title_text.GetValue()}
            node = self.tree.AppendItem(self.item, ed.getelname('img', data))
            self.tree.SetItemData(node, data)
            self.mark_dirty(True)
            self.refresh_preview()
        edt.Destroy()

    def add_list(self, evt=None):
        "start toevoegen list m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't do this below text", self.title)
            return
        edt = ListDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            list_type = edt.type_select.GetValue()[0] + "l"
            itemtype = "dt" if list_type == "dl" else "li"
            new_item = self.tree.AppendItem(self.item, ed.getelname(list_type))

            for row in range(edt.list_table.GetNumberRows()):
                new_subitem = self.tree.AppendItem(new_item, ed.getelname(itemtype))
                data = edt.list_table.GetCellValue(row, 0)
                node = self.tree.AppendItem(new_subitem, ed.getshortname(data))
                self.tree.SetItemData(node, data)
                if list_type == "dl":
                    new_subitem = self.tree.AppendItem(new_item, ed.getelname('dd'))
                    data = edt.list_table.GetCellValue(row, 1)
                    node = self.tree.AppendItem(new_subitem, ed.getshortname(data))
                    self.tree.SetItemData(node, data)

            ## for i,data in enumerate(edt.dataitems):
                ## itemtype = "dt" if type == "dl" else "li"
                ## new_data = self.tree.AppendItem(new_item,'<> ' + itemtype)
                ## rr = self.tree.AppendItem(new_data,ed.getshortname(data))
                ## self.tree.SetPyData(rr,data)
                ## if type == "dl":
                    ## new_data = self.tree.AppendItem(new_item,'<> dd')
                    ## text = edt.items
                    ## rr = self.tree.AppendItem(new_data,ed.getshortname(text))
                    ## self.tree.SetPyData(rr,text)
            self.mark_dirty(True)
            self.refresh_preview()
        edt.Destroy()

    def add_table(self, evt=None):
        "start toevoegen tabel m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't do this below text", self.title)
            return
        edt = TableDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            cols = edt.table_table.GetNumberCols()  # int(edt.cols_text.GetValue())
            rows = edt.table_table.GetNumberRows()  # int(edt.rows_text.GetValue())
            data = {"summary": edt.title_text.GetValue()}
            new_item = self.tree.AppendItem(self.item, ed.getelname('table', data))
            self.tree.SetItemData(new_item, data)
            new_row = self.tree.AppendItem(new_item, ed.getelname('tr'))
            for col in range(cols):
                new_head = self.tree.AppendItem(new_row, ed.getelname('th'))
                # try:
                head = edt.table_table.GetColLabelValue(col)  # edt.headings[col]
                # except IndexError:
                if not head:
                    node = self.tree.AppendItem(new_head, ed.getshortname(BL))
                    self.tree.SetItemData(node, BL)
                else:
                    node = self.tree.AppendItem(new_head, ed.getshortname(head))
                    self.tree.SetItemData(node, head)
            for row in range(rows):
                new_row = self.tree.AppendItem(new_item, ed.getelname('tr'))
                for col in range(cols):
                    new_cell = self.tree.AppendItem(new_row, ed.getelname('td'))
                    text = edt.table_table.GetCellValue(row, col)
                    node = self.tree.AppendItem(new_cell, ed.getshortname(text))
                    self.tree.SetItemData(node, text)
            self.mark_dirty(True)
            self.refresh_preview()
        edt.Destroy()

    def validate(self, evt=None):
        """start validation
        """
        if self.tree_dirty or not self.xmlfn:
            htmlfile = '/tmp/ashe_check.html'
            fromdisk = False
            self.data2soup()
            with open(htmlfile, "w") as f_out:
                f_out.write(str(self.soup))
        else:
            htmlfile = self.xmlfn
            fromdisk = True
        if fromdisk:
            wx.MessageBox("\n".join((
                "Validation results are for the file on disk",
                "some errors/warnings may already have been corrected by "
                "BeautifulSoup",
                "(you'll know when they don't show up inthe tree or text view",
                " or when you save the file in memory back to disk)")), self.title)
        data = ed.EditorMixin.validate(self, htmlfile)
        dlg = ScrolledMessageDialog(self, data, "Validation output", size=(600, -1),
                                    style=wx.RESIZE_BORDER)
        dlg.Show()  # in plaats van ShowModal(), om openhouden tijdens aanpassen mogelijk te maken


def ashe_gui(args):
    "start main GUI"
    fname = ''
    if len(args) > 1:
        fname = args[1]
    app = wx.App()  # redirect=True, filename="/home/albert/projects/htmledit/ashe/ashe.log")
    print("\n-- new entry --\n")
    if fname:
        frm = MainFrame(None, -1, fname=fname)
    else:
        frm = MainFrame(None, -1)
    if frm.err:
        wx.MessageBox(str(frm.err), frm.title)
    app.MainLoop()


if __name__ == "__main__":
    ashe_gui(sys.argv)
