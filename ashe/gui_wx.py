"""wxPython specifieke routines voor mijn op een treeview gebaseerde HTML-editor
"""
import os
# import sys
import copy
import wx
# import wx.grid as wxgrid
import wx.html2 as wxhtml  # webkit

from ashe.shared import ELSTART, masks
from ashe.dialogs_wx import ElementDialog, TextDialog, DtdDialog, CssDialog, \
    LinkDialog, ImageDialog, VideoDialog, AudioDialog, ListDialog, TableDialog, \
    ScrolledTextDialog, CodeViewDialog, SearchDialog


class VisualTree(wx.TreeCtrl):
    """tree representation of HTML
    """
    def __init__(self, parent):  # , size):
        self._parent = parent.Parent
        super().__init__(parent)  # , size=size)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_leftdclick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        ## self.Bind(wx.EVT_CONTEXT_MENU, self.onContextMenu)
        # self.Bind(wx.EVT_CHAR, self.on_char)
        # self.Bind(wx.EVT_KEY_UP, self.on_key)
        ## self.setAcceptDrops(True)
        ## self.setDragEnabled(True)
        ## self.setSelectionMode(self.SingleSelection)
        ## self.setDragDropMode(self.InternalMove)
        ## self.setDropIndicatorShown(True)

    def on_leftdclick(self, evt=None):
        "start edit bij dubbelklikken tenzij op filenaam"
        item = self.HitTest(evt.GetPosition())[0]
        if item:
            if item == self._parent.top:
                edit = False
            else:
                data = self.GetItemText(item)
                edit = True
                if data.startswith(ELSTART):
                    if self.GetChildrenCount(item):
                        edit = False
        if edit:
            self._parent.edit()
        evt.Skip()

    def on_rightdown(self, evt=None):
        "context menu bij rechtsklikken"
        print('in on_rightdown: getting position')
        item = self.HitTest(evt.GetPosition())[0]
        print('in on_rightdown:', item, self._parent.top)
        if item and item != self._parent.top:
            self._parent.contextmenu(item)
        evt.Skip()

    ## def mouseReleaseEvent(self, event):
        ## "reimplemented event handler"
        ## if event.button() == core.Qt.RightButton:
            ## xc, yc = event.x(), event.y()
            ## item = self.itemAt(xc, yc)
            ## if item and item != self._parent.top:
                ## return
        ## super().mouseReleaseEvent(event)

    ## def dropEvent(self, event):
        ## """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        ## een ander (dropitem)
        ## Het komt er altijd *onder* te hangen als laatste item
        ## deze methode breidt de Treewidget methode uit met wat visuele zaken
        ## """
        ## item = self.itemAt(event.pos())
        ## if not item or not item.text(0).startswith(self._parent.editor.constants['ELSTART']):
            ## self._parent.meld('Can only drop on element')
            ## return
        ## dragitem = self.selectedItems()[0]
        ## super().dropEvent(event)
        ## self._parent.tree_dirty = True
        ## dropitem = dragitem.parent()
        ## self.setCurrentItem(dragitem)
        ## dropitem.setExpanded(True)
        ## self._parent.refresh_preview()


class MainFrame(wx.Frame):
    "Main GUI"

    def __init__(self, parent=None, editor=None, err=None, icon=None):
        self.parent = parent
        self.editor = editor
        self.app = wx.App()
        dsp = wx.Display().GetClientArea()
        high = dsp.height if dsp.height < 900 else 900
        wide = dsp.width if dsp.width < 1020 else 1020
        super().__init__(parent, title=self.editor.title, size=(wide, high),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        if err:
            self.meld(err)
            return

        self.dialog_data = {}
        self.search_args = []
        if icon:
            self.appicon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.appicon)

        self._setup_menu()
        self.in_contextmenu = False

        self.pnl = wx.SplitterWindow(self)
        self.pnl.SetMinimumPaneSize(1)

        self.tree = VisualTree(self.pnl)  # , size=(500,100))
        # self.tree.headerItem().setHidden(True)

        self.html = wxhtml.WebView.New(self.pnl)  # , size=(800, high))
        # if "gtk2" in wx.PlatformInfo:
        #     self.html.SetStandardFonts()

        self.pnl.SplitVertically(self.tree, self.html)
        self.pnl.SetSashPosition(400, True)

        self.sb = wx.StatusBar(self)
        self.SetStatusBar(self.sb)

        # self.tree.SetSize(500, 100)
        # sizer0 = wx.BoxSizer(wx.VERTICAL)
        # sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        # sizer1.Add(self.pnl, 1, wx.EXPAND)
        # sizer0.Add(sizer1, 1, wx.EXPAND)

        # self.SetSizer(sizer0)
        # self.SetAutoLayout(True)
        # sizer0.Fit(self)
        # sizer0.SetSizeHints(self)
        # self.Layout()
        self.tree.SetFocus()
        # self.Bind(wx.EVT_CLOSE, self.editor.close)
        self.adv_menu.Check(True)
        self.Show(True)

    def go(self):
        """show the screen
        """
        self.app.MainLoop()

    def close(self):
        """shut down the application
        """
        self.Close()

    def _setup_menu(self):
        """build application menu
        """
        menu_bar = wx.MenuBar()
        self.contextmenu_items = []  #TODO alleen de teksten hierin zetten, niet de menuid's
        for menu_text, data in self.editor.get_menulist():
            menu = wx.Menu()
            for item in data:
                if len(item) == 1:
                    menu.AppendSeparator()
                    continue
                menuitem_text, hotkey, modifiers, status_text, callback = item[:5]
                if 'A' in modifiers:
                    hotkey = "+".join(("Alt", hotkey))
                if 'C' in modifiers:
                    hotkey = "+".join(("Ctrl", hotkey))
                if 'S' in modifiers:
                    hotkey = "+".join(("Shift", hotkey))
                # act = wx.Action(menuitem_text, self)
                # menu.addAction(act)
                # act.setStatusTip(status_text)
                # act.setShortcut(hotkey)
                # act.triggered.connect(callback)
                menuid = wx.NewId()
                caption = "\t".join((menuitem_text, hotkey)) if hotkey else menuitem_text
                if menuitem_text.startswith('Advance selection'):
                    self.adv_menu = wx.MenuItem(menu, menuid, caption, status_text, wx.ITEM_CHECK)
                    mnu = self.adv_menu
                else:
                    mnu = wx.MenuItem(menu, menuid, caption, status_text)
                    if menu_text == '&View':
                        self.contextmenu_items.append(('A', mnu))
                        # self.popup_menu.Append(mnu)
                    elif menuitem_text == 'Add &DTD':
                        self.dtd_menu = mnu
                    elif menuitem_text == 'Add &Stylesheet':
                        self.css_menu = mnu
                        if not self.editor.cssedit_available:
                            mnu.Enable(False)
                    self.Bind(wx.EVT_MENU, callback, mnu)
                menu.Append(mnu)
                if menu_text in ('&Edit', '&Search', '&HTML'):
                    item = ('M', (menu, menu_text))
                    if item not in self.contextmenu_items:
                        self.contextmenu_items.append(item)
                        # self.popup_menu.AppendSubMenu(menu, menu_text)
            if menu_text == '&View':
                self.contextmenu_items.append(('', ''))
                # self.popup_menu.AppendSeparator()
            menu_bar.Append(menu, menu_text)
        self.SetMenuBar(menu_bar)
        # dit lijkt code voor het popup menu de werkt, maar dan werkt het gewone menu niet?
        self.popup_menu = wx.Menu()
        for itemtype, item in self.contextmenu_items:
            if itemtype == 'A':
                self.popup_menu.Append(item)
                if item == self.css_menu:
                    if not self.editor.cssedit_available:
                        item.enable(False)
            elif itemtype == 'M':
                subm, text = item
                self.popup_menu.AppendSubMenu(subm, text)
            else:
                self.popup_menu.AppendSeparator()

    # def setfilenametooltip((self):
        # """bedoeld om de filename ook als tooltip te tonen, uit te voeren
        # aan het eind van new, open, save, saveas en reload"""
        # zie ticket 406 voor een overweging om dit helemaal achterwege te laten

    def get_screen_title(self):
        "retrieve the screen's title"
        return self.GetTitle()

    def set_screen_title(self, title):
        "change the screen's title"
        self.SetTitle(title)

    def get_element_text(self, node):
        "return text in visual tree for this element"
        return self.tree.GetItemText(node)

    def get_element_parent(self, node):
        "return parent in visual tree for this element"
        return self.tree.GetItemParent(node)

    def get_element_parentpos(self, item):
        "return parent and position under parent in visual tree for this element"
        parent = self.tree.GetItemParent(item)
        pos = 0
        child, state = self.tree.GetFirstChild(parent)
        while child.IsOk():
            if child == item:
                break
            pos += 1
            child, state = self.tree.GetNextChild(parent, state)
        return parent, pos

    def get_element_data(self, node):
        "return attributes stored with this element"
        return self.tree.GetItemData(node)

    def get_element_children(self, node):
        "return iterator over children in visual tree for this element"
        children = []
        child, state = self.tree.GetFirstChild(node)
        while child.IsOk():
            children.append(child)
            child, state = self.tree.GetNextChild(node, state)
        return children

    def set_element_text(self, node, text):
        "change text in visual tree for this element"
        self.tree.SetItemText(node, text)

    def set_element_data(self, node, data):
        "change stored attrs for this element"""
        self.tree.SetItemData(node, data)

    def addtreeitem(self, node, naam, data, index=-1):
        """itemnaam en -data toevoegen aan de interne tree
        geeft referentie naar treeitem terug
        """
        if index == -1:
            newnode = self.tree.AppendItem(node, naam)
        else:
            newnode = self.tree.InsertItem(node, index, naam)
        # data is ofwel leeg, ofwel een string, ofwel een dictionary
        self.tree.SetItemData(newnode, data)
        return newnode

    def addtreetop(self, fname, titel):
        """titel en root item in tree instellen"""
        self.SetTitle(titel)
        self.tree.DeleteAllItems()
        self.top = self.tree.AddRoot(fname)

    def get_selected_item(self):
        """geef het in de tree geselecteerde item terug
        """
        return self.tree.GetSelection()

    def set_selected_item(self, item):
        """stel het in de tree geselecteerde item in
        """
        print('in gui.set_selected_item, item is', item)
        self.tree.SelectItem(item)

    def init_tree(self, message):
        "toolkit specifieke voortzetting van gelijknamige editor methode"
        self.set_selected_item(self.top)
        self.adv_menu.Check(True)
        self.show_statusbar_message(message)

    def show_statusbar_message(self, text):
        """toon tekst in de statusbar
        """
        self.sb.SetStatusText(text)

    def adjust_dtd_menu(self):
        "set text for dtd menu option"
        if self.editor.has_dtd:
            self.dtd_menu.SetItemLabel('Remove &DTD')
            self.dtd_menu.SetHelp('Remove the document type declaration')
        else:
            self.dtd_menu.SetItemLabel('Add &DTD')
            self.dtd_menu.SetHelp('Add a document type description')

    def contextmenu(self, arg=None):
        'build/show context menu'
        # get type of node
        print('in contextmenU: itemtext is ', self.get_element_text(self.get_selected_item()))
        # menu = wx.Menu()
        # for itemtype, item in self.contextmenu_items[:]:
        #     if itemtype == 'A':
        #         menu.Append(item)
        #         if item == self.css_menu:
        #             if not self.editor.cssedit_available:
        #                 item.enable(False)
        #     elif itemtype == 'M':
        #         subm, text = item
        #         menu.AppendSubMenu(subm, text)
        #     else:
        #         menu.AppendSeparator()
        # y = self.tree.visualItemRect(arg).bottom()
        # x = self.tree.visualItemRect(arg).left()
        # popup_location = core.QPoint(int(x) + 200, y)
        # self.in_contextmenu = True
        # menu.exec_(self.tree.mapToGlobal(popup_location))
        # self.in_contextmenu = False
        # del menu
        # self.PopupMenu(menu)
        # menu.Destroy()
        # onderstaande reageert meestal goed als de code in setup menu gebruikt wordt
        self.PopupMenu(self.popup_menu)

    # TODO: hier moet nog iets komen om erin te voorzien dat de menu knop (rechter Windows key)
    # gebruikt wordt, maar die heb ik niet op mijn huidige toetesenbord
    # in de qt versie is dat een keyrelease event

    @staticmethod
    def ask_how_to_continue(title, text):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)
        retourneert 1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((wx.YES, wx.NO, wx.CANCEL), (1, 0, -1)))
        hlp = wx.MessageBox(text, title, style=wx.YES_NO | wx.CANCEL)
        return retval[hlp]

    @staticmethod
    def build_mask(ftype):
        """build mask for FileDialog
        """
        text, filetypes = masks['all']
        all_mask = "{0} ({1})|{1}".format(text, filetypes[0])
        text, filetypes = masks[ftype]
        filetypes_text = ",".join(filetypes)
        if os.name == 'posix':
            filetypes_text = ','.join((filetypes_text, filetypes_text.upper()))
        extensions_text = filetypes_text.replace(',', ';')
        return "{} ({})|{}".format(text, filetypes_text, extensions_text) + '|' + all_mask

    def ask_for_filename(self, message, style):
        """open een dialoog om te vragen met welk file iets gedaan moet worden

        note: wx maakt opgegeven paden niet automatisch absoluut in de filedialoog (Qt wel)
        """
        filename = ''
        if self.editor.xmlfn:
            dname, fname = os.path.split(os.path.abspath(self.editor.xmlfn))
        else:
            dname = os.getcwd()
            fname = ""
        mask = self.build_mask('html')
        with wx.FileDialog(self, message=message, defaultDir=dname, defaultFile=fname,
                           wildcard=mask, style=style) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
        return filename

    def ask_for_open_filename(self):
        """open een dialoog om te vragen welk file geladen moet worden
        """
        return self.ask_for_filename("Choose a file", wx.FD_OPEN)

    def ask_for_save_filename(self):
        """open een dialoog om te vragen onder welke naam de html moet worden opgeslagen
        """
        return self.ask_for_filename("Save file as ...", wx.FD_SAVE)

    def set_item_expanded(self, item, state):
        """show item's children
        """
        if self.tree.IsExpanded(item):
            # self.tree.Collapse(item)
            self.tree.CollapseAllChildren(item)
        else:
            # self.tree.Expand(item)
            self.tree.ExpandAllChildren(item)

    def expand(self):
        "toolkit specifieke voortzetting van gelijknamige editor methode"
        item = self.tree.Selection
        if item:
            self.tree.ExpandAllChildren(item)
        # self.tree.scrollToItem(results[-1]) -- laatste item onder huidige

    def collapse(self):
        "toolkit specifieke voortzetting van gelijknamige editor methode"
        item = self.tree.Selection
        if item:
            self.tree.CollapseAllChildren(item)

    def get_adv_sel_setting(self):
        "callback for menu option"
        self.advance_selection_on_add = self.adv_menu.IsChecked()

    def refresh_preview(self, soup):
        "toolkit specifieke voortzetting van gelijknamige editor methode"
        # self.data_file = os.path.join('/tmp', "ashe_tempfile.html")
        # with open(self.data_file, "w") as f_out:
        #     f_out.write(str(soup).replace('%SOUP-ENCODING%', 'utf-8'))
        # self.html.LoadURL('file://' + self.data_file)
        self.html.SetPage(str(soup).replace('%SOUP-ENCODING%', 'utf-8'), '')
        self.tree.SetFocus()

    @staticmethod
    def call_dialog(obj):
        "send dialog and transmit results"
        obj.resend = False
        with obj:
            send = True
            while send:
                edt = obj.ShowModal()
                if edt in (wx.ID_SAVE, wx.ID_OK, wx.ID_APPLY):
                    ok, dialog_data = obj.on_ok()
                    if ok:
                        send = False
                        return True, dialog_data
                if obj.resend:  # can be set in obj.on_ok()
                    obj.resend = False
                else:
                    send = False
        return False, None

    def do_edit_element(self, tagdata, attrdict):
        """show dialog for existing element"""
        obj = ElementDialog(self, title='Edit an element', tag=tagdata, attrs=attrdict)
        return self.call_dialog(obj)

    def do_add_element(self, where):
        """show dialog for new element"""
        obj = ElementDialog(self, title="New element (insert {0})".format(where))
        return self.call_dialog(obj)

    def do_edit_textvalue(self, textdata):
        """show dialog for existing text"""
        return self.call_dialog(TextDialog(self, title='Edit Text', text=textdata))

    def do_add_textvalue(self):
        """show dialog for new text"""
        return self.call_dialog(TextDialog(self, title="New Text"))

    def ask_for_condition(self):
        "zet een IE conditie om het element heen"
        with wx.TextEntryDialog(self, 'Enter the condition', self.editor.title) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                return dlg.GetValue()
        return ''

    def do_delete_item(self, item):
        """remove element from tree
        """
        prev = self.tree.GetPrevSibling(item)
        if not prev.IsOk():
            prev = self.tree.GetItemParent(item)
            if self.tree.GetItemData(prev) == self.editor.root:
                prev = self.tree.GetNextSibling(item)
        self.tree.Delete(item)
        return prev

    def get_search_args(self):
        """show search options dialog"""
        # self._parent.search_args =
        return self.call_dialog(SearchDialog(self, title='Search options'))

    def meld(self, text):
        """notify about some information"""
        self.in_dialog = True
        wx.MessageBox(text, self.editor.title, parent=self)

    def meld_fout(self, text, abort=False):
        """notify about an error"""
        self.in_dialog = True
        wx.MessageBox(text, self.title, wx.ICON_ERROR, parent=self)
        if abort:
            self.quit()

    def ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((wx.ID_YES, wx.ID_NO, wx.CANCEL), (1, 0, -1)))
        self.in_dialog = True
        hlp = wx.MessageBox(prompt, self._parent.title, style=wx.YES_NO | wx.CANCEL)
        return retval[hlp]

    def ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        self.in_dialog = True
        with wx.TextEntryDialog(self, prompt, self.title) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                return dlg.GetValue(), True
        return '', False

    def ensure_item_visible(self, item):
        """make sure we can see the item
        """
        self.tree.EnsureVisible(item)

    def get_dtd(self):
        """show dialog for dtd
        """
        return self.call_dialog(DtdDialog(self))

    def get_css_data(self):
        """show dialog for new style element
        """
        return self.call_dialog(CssDialog(self))

    def get_link_data(self):
        """show dialog for new link element
        """
        return self.call_dialog(LinkDialog(self))

    def get_image_data(self):
        """show dialog for new image element
        """
        return self.call_dialog(ImageDialog(self))

    def get_video_data(self):
        """show dialog for new video element
        """
        return self.call_dialog(VideoDialog(self))

    def get_audio_data(self):
        """show dialog for new audio element
        """
        return self.call_dialog(AudioDialog(self))

    def get_list_data(self):
        """show dialog for new list element
        """
        return self.call_dialog(ListDialog(self))

    def get_table_data(self):
        """show dialog for new table element
        """
        return self.call_dialog(TableDialog(self))

    def validate(self, htmlfile, fromdisk):
        "start validation"
        with ScrolledTextDialog(self, "Validation output",
                                htmlfile=htmlfile, fromdisk=fromdisk) as dlg:
            dlg.ShowModal()

    def show_code(self, title, caption, data):
        "show dialog for view source"
        with CodeViewDialog(self, title, caption, data) as dlg:
            dlg.ShowModal()
