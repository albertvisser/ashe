"""wxPython specifieke routines voor mijn op een treeview gebaseerde HTML-editor
"""
import os
import sys
import wx
import wx.grid as wxgrid
import wx.html as wxhtml #  webkit

from ashe.dialogs_wx import cssedit_available, HMASK, ElementDialog, \
    TextDialog, DtdDialog, CssDialog, LinkDialog, ImageDialog, VideoDialog, \
    AudioDialog, ListDialog, TableDialog, ScrolledTextDialog, CodeViewDialog, \
    SearchDialog



class VisualTree(wx.TreeWidget):
    """tree representation of HTML
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__()
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_leftdclick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        ## self.Bind(wx.EVT_CONTEXT_MENU, self.onContextMenu)
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_KEY_UP, self.on_key)
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
        item = self.HitTest(evt.GetPosition())[0]
        if item and item != self._parent.top:
            self._parent.contextmenu(item)  # dan wel self._parent.popup_menu(item)
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


class MainFrame(wx.MainWindow):
    "Main GUI"

    def __init__(self, parent=None, editor=None, err=None, icon=None):
        self.parent = parent
        self.editor = editor
        self.app = wx.App()
        super().__init__(parent, self.editor.title)
        if err:
            self.meld(err)
            return

        self.dialog_data = {}
        self.search_args = []
        if icon:
            self.appicon = gui.QIcon(icon, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.appicon)
        dsp = wx.Display().GetClientArea()
        high = dsp.height if dsp.height < 900 else 900
        wide = dsp.width if dsp.width < 1020 else 1020
        self.resize(wide, high)

        self._setup_menu()
        self.in_contextmenu = False

        self.pnl = wx.Splitter(self)
        self.pnl.SetMinimumPaneSize(1)

        self.tree = VisualTree(self)
        # self.tree.headerItem().setHidden(True)

        self.html = html.HtmlWindow(self.pnl, -1)
        if "gtk2" in wx.PlatformInfo:
            self.html.SetStandardFonts()

        self.pnl.SplitVertically(self.tree, self.html)
        self.pnl.SetSashPosition(400, True)

        self.sb = wx.StatusBar(self)
        self.SetStatusBar(self.sb)

        # self.tree.resize(500, 100)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.panel, 1, wx.EXPAND)
        sizer0.Add(sizer1, 1, wx.EXPAND)

        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        self.Layout()
        self.Show(True)
        self.tree.SetFocus()
        self.Bind(wx.EVT_CLOSE, self.exit)

    def go(self):
        self.adv_menu.setChecked(True)
        self.show()
        err = self.editor.getsoup(self.editor.xmlfn) or ''
        if not err:
            self.editor.refresh_preview()
        self.app.MainLoop()

    def _setup_menu(self):
        """build application menu
        """
        menu_bar = wx.MenuBar()
        self.contextmenu_items = []
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
                caption = "\n".join((menuitem_text, hotkey))
                if menuitem_text.startswith('Advance selection'):
                    self.adv_menu = menu.Append(menuid, caption, status_text, True)  # checkable=True)
                else:
                    mnu = menu.Append(menu_id, caption, status_text)
                    if menu_text == '&View':
                        self.contextmenu_items.append(('A', mnu))
                    elif menuitem_text == 'Add &DTD':
                        self.dtd_menu = mnu
                    elif menuitem_text == 'Add &Stylesheet':
                        self.css_menu = mnu
                        if not cssedit_available:
                            mnu.Enable(False)
                    self.Connect(menuid, -1, wx.wxEVT_COMMAND_MENU_SELECTED, callback)
                if menu_text in ('&Edit', '&HTML'):
                    self.contextmenu_items.append(('M', menu))
            if menu_text == '&View':
                self.contextmenu_items.append(('', ''))
            menu_bar.append(menu, menu_text)

    # def setfilenametooltip((self):
        # """bedoeld om de filename ook als tooltip te tonen, uit te voeren
        # aan het eind van new, open, save, saveas en reload"""
        # zie ticket 406 voor een overweging om dit helemaal achterwege te laten

    def mark_dirty(self, state):
        "update visual signs that the source was changed"
        title = str(self.GetTitle())
        test = ' - ' + self.editor.title
        test2 = '*' + test
        if state:
            if test2 not in title:
                title = title.replace(test, test2)
        else:
            title = title.replace(test2, test)
        self.SetTitle(title)

    def get_element_text(self, node):
        "return text in visual tree for this element"
        return self.tree.GetItemText(node)

    def get_element_parent(self, node):
        "return parent in visual tree for this element"
        return self.tree.GetItemParent(node)

    def get_element_parentpos(self, item):
        "return parent and position under parent in visual tree for this element"
        parent = self.tree.item.GetItemParent()
        pos = 0
        state, child = self.tree.GetFirstChild(parent)
        while child.IsOk():
            if child == item:
                break
            pos += 1
            state, child = self.tree.GetNextChild(parent, state)
        return parent, pos

    def get_element_data(self, node):
        "return attributes stored with this element"
        return self.tree.GetItemData(node)

    def get_element_children(self, node):
        "return iterator over children in visual tree for this element"
        children = []
        state, child = self.tree.GetFirstChild(parent)
        while child.IsOk():
            children.append(child)
            state, child = self.tree.GetNextChild(parent, state)
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
        newnode = self.tree.AppendItem(node, naam)
        # data is ofwel leeg, ofwel een string, ofwel een dictionary
        self.tree.SetItemData(newnode, data)
        return newnode

    def addtreetop(self, fname, titel):
        """titel en root item in tree instellen"""
        self.SetTitle(titel)
        self.tree.DeleteAllItems()
        self.top = self.tree.AddRoot(titel)

    def get_selected_item(self):
        """geef het in de tree geselecteerde item terug
        """
        return self.tree.GetSelection()

    def set_selected_item(self, item):
        """stel het in de tree geselecteerde item in
        """
        self.tree.SelectItem(item)

    def init_tree(self, message):
        "toolkit specifieke voortzetting van gelijknamige editor methode"
        self.tree.set_selected_item(self.top)
        # self.adv_menu.setChecked(True)
        self.show_statusbar_message(message)

    def show_statusbar_message(self, text):
        """toon tekst in de statusbar
        """
        self.sb.SetStatusText(text)

    def adjust_dtd_menu(self):
        "set text for dtd menu option"
        if self.editor.has_dtd:
            self.dtd_menu.SetText('Remove &DTD')
            self.dtd_menu.SetHelp('Remove the document type declaration')
        else:
            self.dtd_menu.SetText('Add &DTD')
            self.dtd_menu.SetHelp('Add a document type description')

    def popup_menu(self, arg=None):
        'build/show context menu'
        # get type of node
        itemtext = self.tree.get_element_text(self.tree.get_selected_item())
        menu = wx.Menu()
        for itemtype, item in self.contextmenu_items:
            if itemtype == 'A':
                menu.Append(item)
                if item == self.css_menu:
                    if not cssedit_available:
                        item.enable(False)
            elif itemtype == 'M':
                menu.Append(item)
            else:
                menu.AppendSeparator()
        # y = self.tree.visualItemRect(arg).bottom()
        # x = self.tree.visualItemRect(arg).left()
        # popup_location = core.QPoint(int(x) + 200, y)
        # self.in_contextmenu = True
        # menu.exec_(self.tree.mapToGlobal(popup_location))
        # self.in_contextmenu = False
        # del menu
        self.PopupMenu(menu)
        menu.Destroy()

    def keyReleaseEvent(self, event):
        "reimplemented event handler"
        skip = self.on_keyup(event)
        if not skip:
            super().keyReleaseEvent(event)

    def on_keyup(self, ev=None):
        "determine if key event needs to be skipped"
        ky = ev.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top:
            if ky == core.Qt.Key_Menu:
                self.popup_menu(item)
                skip = True
        return skip

    def ask_how_to_continue(self, title, text):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)
        retourneert 1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((wx.ID_YES, wx.ID_NO, wx.CANCEL), (1, 0, -1)))
        hlp = wx.MessageBox(text, title, style=wx.YES_NO | wx.CANCEL)
        return retval[hlp]

    def ask_for_open_filename(self):
        """open een dialoog om te vragen welk file geladen moet worden
        """
        filename = ''
        loc = self.editor.xmlfn or os.getcwd()
        with wx.FileDialog(self, message="Choose a file", defaultDir=loc, wildcard=HMASK,
                           style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
        return filename

    def ask_for_save_filename(self):
        """open een dialoog om te vragen onder welke naam de html moet worden opgeslagen
        """
        filename = ''
        if self.xmlfn:
            dname, fname = os.path.split(self.xmlfn)
        else:
            dname = os.getcwd()
            fname = ""
        with wx.FileDialog(self, message="Save file as ...", defaultDir=dname,
                           defaultFile=fname, wildcard=HMASK, style=wx.FD_SAVE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
        return filename

    def set_item_expanded(self, item, state):
        """show item's children
        """
        if self.tree.IsExpanded(item):
            self.tree.Collapse(item)
        else:
            self.tree.ExpandItem(item)

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
        self.data_file = os.path.join(PPATH, "tempfile.html")
        with open(self.data_file, "w") as f_out:
            f_out.write(str(soup).replace('%SOUP-ENCODING%', 'utf-8'))
        self.html.LoadPage(self.data_file)
        self.tree.SetFocus()

    def call_dialog(self, obj):
        "send dialog and transmit results"
        with obj:
            edt = obj.ShowModal()
            if edt == wx.Dialog.Accepted:
                dialog_data = obj.on_ok()
                return True, dialog_data
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
        with wx.textEntryDialog(self, 'Enter the condition', self.title) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                return dlg.GetValue()
        return ''

    def do_delete_item(self, item):
        """remove element from tree
        """
        prev = self.tree.GetPrevSibling(self.item)
        if not prev.IsOk():
            prev = self.tree.GetItemParent(self.item)
            if self.tree.GetItemData(prev) == self.editor.root:
                prev = self.tree.GetNextSibling(self.item)
        self.tree.Delete(self.item)
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
        hlp = wx.MessageBox(text, title, style=wx.YES_NO | wx.CANCEL)
        return retval[hlp]

    def ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        self.in_dialog = True
        with wx.textEntryDialog(self, prompt, self.title) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                return dlg.GetValue(), True
        return '', False

    def ensure_item_visible(self, item):
        """make sure we can see the item
        """
        self.tree.EnsureVisible(iiem)
# tot hiertoe omgeschreven naar gebruik wx
    def get_dtd(self):
        """show dialog for dtd
        """
        return self.call_dialog(DtdDialog(self))
        edt = DtdDialog(self).exec_()
        if edt == wx.Dialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def get_css_data(self):
        """show dialog for new style element
        """
        return self.call_dialog(CssDialog(self))
        edt = CssDialog(self).exec_()
        if edt == wx.Dialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def get_link_data(self):
        """show dialog for new link element
        """
        return self.call_dialog(LinkDialog(self))
        edt = LinkDialog(self).exec_()
        if edt == wx.Dialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def get_image_data(self):
        """show dialog for new image element
        """
        return self.call_dialog(ImageDialog(self))
        edt = ImageDialog(self).exec_()
        if edt == wx.Dialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

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
        # deze dialoog is gecodeerd in de dialogs module maar moet het valideren daarbinnen wel
        # gebeuren?
        dlg = ScrolledTextDialog(self, "Validation output", htmlfile=htmlfile, fromdisk=fromdisk)
        dlg.show()

    def show_code(self, title, caption, data):
        "show dialog for view source"
        dlg = CodeViewDialog(self, title, caption, data)
        dlg.show()
