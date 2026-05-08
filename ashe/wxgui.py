"""wxPython specifieke routines voor mijn op een treeview gebaseerde HTML-editor
"""
import os
import wx
import wx.grid as wxgrid
import wx.lib.mixins.treemixin as treemix
import wx.html2 as wxhtml  # webkit
import wx.stc as wxstc

from ashe.shared import ELSTART, masks, analyze_element
# from ashe.dialogs_wx import (ElementDialog, TextDialog, DtdDialog, CssDialog, LinkDialog,
#                              ImageDialog, VideoDialog, AudioDialog, ListDialog, TableDialog,
#                              ScrolledTextDialog, CodeViewDialog, SearchDialog)


class EditorGui(wx.Frame):
    "Main GUI"

    def __init__(self, editor, title, icon):
        self.editor = editor
        self.app = wx.App()
        dsp = wx.Display().GetClientArea()
        minheight, minwidth = 900, 1020
        high = dsp.height if dsp.height < minheight else minheight
        wide = dsp.width if dsp.width < minwidth else minwidth
        super().__init__(parent=None, title=title, size=(wide, high),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.dialog_data = {}
        self.search_args = []
        self.appicon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.appicon)

    def create_menu(self):
        """build application menu
        """
        menu_bar = wx.MenuBar()
        self.contextmenu_items = []
        for menu_text, data in self.editor.get_menulist():
            menu = wx.Menu()
            if menu_text in ('&Edit', '&Search', '&HTML'):
                self.contextmenu_items.append(('M', menu_text))
            elif menu_text == '&View':
                self.contextmenu_items.append(('', ''))
            for item in data:
                if len(item) == 1:
                    menu.AppendSeparator()
                    continue
                menuitem_text, hotkey, modifiers, status_text, callback = item[:5]
                if 'A' in modifiers:
                    hotkey = f"Alt+{hotkey}"
                if 'C' in modifiers:
                    hotkey = f"Ctrl+{hotkey}"
                if 'S' in modifiers:
                    hotkey = f"Shift+{hotkey}"
                menuid = wx.ID_ANY  # NewId()
                caption = f"{menuitem_text}\t{hotkey}" if hotkey else menuitem_text
                if menuitem_text.startswith('Advance selection'):
                    mnu = wx.MenuItem(menu, menuid, caption, status_text, wx.ITEM_CHECK)
                    self.adv_menu = mnu
                else:
                    mnu = wx.MenuItem(menu, menuid, caption, status_text)
                    if menuitem_text == 'Add &DTD':
                        self.dtd_menu = mnu
                    elif menuitem_text == 'Add &Stylesheet':
                        self.css_menu = mnu
                        self.css_menu_text = menuitem_text
                    else:
                        self.contextmenu_items.append(('A', (menuitem_text, callback, status_text)))
                    self.Bind(wx.EVT_MENU, callback, mnu)
                menu.Append(mnu)
            menu_bar.Append(menu, menu_text)
        self.SetMenuBar(menu_bar)

    def create_splitter(self):
        "create main window"
        self.pnl = wx.SplitterWindow(self)
        self.pnl.SetMinimumPaneSize(1)

    def create_tree_on_left(self):
        "create treeview for editing"
        self.tree = VisualTree(self.pnl)  # , size=(500,100))
        # self.tree.headerItem().setHidden(True)

    def create_preview_on_right(self):
        "create html view"
        self.html = wxhtml.WebView.New(self.pnl)  # , size=(800, high))

    def create_statusbar_at_bottom(self):
        "create area for status messages"
        self.sb = wx.StatusBar(self)
        self.SetStatusBar(self.sb)

    def finalize_display(self):
        "finish off screen creation"
        self.pnl.SplitVertically(self.tree, self.html)
        self.pnl.SetSashPosition(400, True)

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
        while True:
            if not child.IsOk():
                return None, -1
            if child == item:
                break
            pos += 1
            child, state = self.tree.GetNextChild(parent, state)
        return parent, pos

    def get_element_data(self, node):
        "return attributes or inline text stored with this element"
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
        "change stored attrs or inline text for this element"
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
        # print('in gui.set_selected_item, item is', item, self.get_element_text(item))
        self.tree.SelectItem(item)

    def init_tree(self, message):
        "toolkit specifieke zaken voor tree instellen"
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
            self.dtd_menu.SetHelp('Add a document type declaration')

    def contextmenu(self, *args):
        'build/show context menu'
        rect = self.tree.GetBoundingRect(self.get_selected_item(), textOnly=True)
        menupos = (rect[0] + rect[2] + 2, rect[1] + rect[3] + 2)
        popup_menu = menu = wx.Menu()
        for itemtype, item in self.contextmenu_items:
            if itemtype == 'A':
                menuitem = wx.MenuItem(menu, wx.NewId(), item[0], item[2])
                self.Bind(wx.EVT_MENU, item[1], menuitem)
                menu.Append(menuitem)
            elif itemtype == 'M':
                menu = wx.Menu()
                popup_menu.AppendSubMenu(menu, item)
            else:
                popup_menu.AppendSeparator()
        self.PopupMenu(popup_menu, pos=menupos)
        popup_menu.Destroy()

    def ask_how_to_continue(self, title, text):
        """vraag of de wijzigingen moet worden opgeslagen
        """
        title = title or self.editor.title
        return ask_yesnocancel(self, text, title)


    # def ask_for_filename(self, message, style):
    #     """open een dialoog om te vragen met welk file iets gedaan moet worden

    #     note: wx maakt opgegeven paden niet automatisch absoluut in de filedialoog (Qt wel)
    #     """
    #     filename = ''
    #     if self.editor.xmlfn:
    #         dname, fname = os.path.split(os.path.abspath(self.editor.xmlfn))
    #     else:
    #         dname = os.getcwd()
    #         fname = ""
    #     mask = self.build_mask('html')
    #     with wx.FileDialog(self, message=message, defaultDir=dname, defaultFile=fname,
    #                        wildcard=mask, style=style) as dlg:
    #         if dlg.ShowModal() == wx.ID_OK:
    #             filename = dlg.GetPath()
    #     return filename

    # def ask_for_open_filename(self):
    #     """open een dialoog om te vragen welk file geladen moet worden
    #     """
    #     return self.ask_for_filename("Choose a file", wx.FD_OPEN)

    # def ask_for_save_filename(self):
    #     """open een dialoog om te vragen onder welke naam de html moet worden opgeslagen
    #     """
    #     return self.ask_for_filename("Save file as ...", wx.FD_SAVE)

    def set_item_expanded(self, item, state):
        """show item's children
        """
        if not state:  # :self.tree.IsExpanded(item):
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
        return self.adv_menu.IsChecked()

    def refresh_preview(self, soup):
        "toolkit specifieke implementatie van gelijknamige editor methode"
        # self.data_file = os.path.join('/tmp', "ashe_tempfile.html")
        # with open(self.data_file, "w") as f_out:
        #     f_out.write(str(soup).replace('%SOUP-ENCODING%', 'utf-8'))
        # self.html.LoadURL('file://' + self.data_file)
        self.html.SetPage(str(soup).replace('%SOUP-ENCODING%', 'utf-8'), '')
        self.tree.SetFocus()

    # def do_edit_element(self, tagdata, attrdict):
    #     """show dialog for existing element"""
    #     obj = ElementDialog(self, title='Edit an element', tag=tagdata, attrs=attrdict)
    #     return self.call_dialog(obj)

    # def do_add_element(self, where):
    #     """show dialog for new element"""
    #     obj = ElementDialog(self, title=f"New element (insert {where})")
    #     return self.call_dialog(obj)

    # def do_edit_textvalue(self, textdata):
    #     """show dialog for existing text"""
    #     return self.call_dialog(TextDialog(self, title='Edit Text', text=textdata))

    # def do_add_textvalue(self):
    #     """show dialog for new text"""
    #     return self.call_dialog(TextDialog(self, title="New Text"))

    # IE support misschien kan dit een keer echt weg
    # def ask_for_condition(self):
    #     "zet een IE conditie om het element heen"
    #     with wx.TextEntryDialog(self, 'Enter the condition', self.editor.title) as dlg:
    #         if dlg.ShowModal() == wx.ID_OK:
    #             return dlg.GetValue()
    #     return ''

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

    # def get_search_args(self):
    #     """show search options dialog"""
    #     # self._parent.search_args =
    #     return self.call_dialog(SearchDialog(self, title='Search options'))

    def meld(self, text):
        """notify about some information"""
        wx.MessageBox(text, self.editor.title, parent=self)

#     def meld_fout(self, text, abort=False):
#         """notify about an error"""
#         wx.MessageBox(text, self.title, wx.ICON_ERROR, parent=self)
#         if abort:
#             self.quit()
#
#     def ask_yesnocancel(self, prompt):
#         """stelt een vraag en retourneert het antwoord
#         1 = Yes, 0 = No, -1 = Cancel
#         """
#         retval = dict(zip((wx.ID_YES, wx.ID_NO, wx.CANCEL), (1, 0, -1)))
#         hlp = wx.MessageBox(prompt, self._parent.title, style=wx.YES_NO | wx.CANCEL)
#         return retval[hlp]
#
#     def ask_for_text(self, prompt):
#         """vraagt om tekst en retourneert het antwoord"""
#         with wx.TextEntryDialog(self, prompt, self.title) as dlg:
#             if dlg.ShowModal() == wx.ID_OK:
#                 return dlg.GetValue(), True
#         return '', False

    def ensure_item_visible(self, item):
        """make sure we can see the item
        """
        self.tree.EnsureVisible(item)

    # def get_dtd(self):
    #     """show dialog for dtd
    #     """
    #     return self.call_dialog(DtdDialog(self))

    # def get_css_data(self):
    #     """show dialog for new style element
    #     """
    #     return self.call_dialog(CssDialog(self))

    # def get_link_data(self):
    #     """show dialog for new link element
    #     """
    #     return self.call_dialog(LinkDialog(self))

    # def get_image_data(self):
    #     """show dialog for new image element
    #     """
    #     return self.call_dialog(ImageDialog(self))

    # def get_video_data(self):
    #     """show dialog for new video element
    #     """
    #     return self.call_dialog(VideoDialog(self))

    # def get_audio_data(self):
    #     """show dialog for new audio element
    #     """
    #     return self.call_dialog(AudioDialog(self))

    # def get_list_data(self):
    #     """show dialog for new list element
    #     """
    #     return self.call_dialog(ListDialog(self))

    # def get_table_data(self):
    #     """show dialog for new table element
    #     """
    #     return self.call_dialog(TableDialog(self))

    # def validate(self, htmlfile, fromdisk):
    #     "start validation"
    #     with ScrolledTextDialog(self, "Validation output",
    #                             htmlfile=htmlfile, fromdisk=fromdisk) as dlg:
    #         dlg.ShowModal()

    # def show_code(self, title, caption, data):
    #     "show dialog for view source"
    #     with CodeViewDialog(self, title, caption, data) as dlg:
    #         dlg.ShowModal()


class VisualTree(treemix.DragAndDrop, wx.TreeCtrl):
    """tree representation of HTML
    """
    def __init__(self, parent):  # , size):
        self._parent = parent.Parent
        super().__init__(parent)  # , size=size)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_leftdclick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        ## drag-n-drop - nog niet geactiveerd
        # self.setAcceptDrops(True)
        # self.setDragEnabled(True)
        # self.setSelectionMode(self.SingleSelection)
        # self.setDragDropMode(self.InternalMove)
        # self.setDropIndicatorShown(True)

    def on_leftdclick(self, evt):
        "start edit bij dubbelklikken tenzij op filenaam"
        item = self.HitTest(evt.GetPosition())[0]
        # if item:
        #     if item == self._parent.top:
        #         edit = False
        #     else:
        #         data = self.GetItemText(item)
        #         edit = True
        #         if data.startswith(ELSTART) and self.GetChildrenCount(item):
        #             edit = False
        edit = False
        if item and item != self._parent.top:
            data = self.GetItemText(item)
            edit = not (data.startswith(ELSTART) and self.GetChildrenCount(item))
        if edit:
            self._parent.edit()
        evt.Skip()

    def on_rightdown(self, evt):
        "context menu bij rechtsklikken"
        item = self.HitTest(evt.GetPosition())[0]
        if item and item != self._parent.top:
            self._parent.contextmenu(item)
        evt.Skip()

    def on_key(self, event):
        # we are only interested in the menu button(s)
        # maar is dit ook niet afhankelijk van de selectiepositie?
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_MENU:
            self._parent.contextmenu()
        event.Skip()

    def OnDrop(self, dropitem, dragitem):
        """reimplemented from treemix.DragAndDrop

        wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        """
        if dropitem == self.GetRootItem():
            return
        if dropitem is None:
            dropitem = self._parent.editor.root
        dragtree = []
        dragtree = self.getsubtree(dragitem, dragtree)[0]
        # zelfde code als bij Editor.delete
        # prev_item = self.GetPrevSibling(dragitem)
        # if not prev_item.IsOk():
        #     prev_item = self.GetItemParent(dragitem)
        #     if self.GetItemData(prev_item) == self._parent.editor.root:
        #         prev_item = self.GetNextSibling(dragitem)
        # maar waarom voer ik die hier uit als ik niks met prev_item doe?
        self.Delete(dragitem)
        self.putsubtree(dropitem, dragtree)
        self.Expand(dropitem)
        self._parent.editor.mark_dirty(True)
        self._parent.editor.refresh_preview()

    def getsubtree(self, elm, result):  # uit copy functie
        "recursief subitem(s) toevoegen aan copy buffer"
        text = self.GetItemText(elm)
        data = self.GetItemData(elm)
        attrlist = []
        if text.startswith(ELSTART):
            # children = []
            child, state = self.GetFirstChild(elm)
            while child.IsOk():
                self.getsubtree(child, attrlist)  # attrlist is updated implicitely
                child, state = self.GetNextChild(elm, state)
        result.append((text, data, attrlist))
        return result

    def putsubtree(self, node, eltree, pos=-1):  # uit paste functie
        "recursively paste copy buffer into tree"
        if len(eltree) == len(['text', 'data', 'subtree']):
            text, data, subtree = eltree
        else:
            text, data, subtree = eltree, '', []
        newnode = self.AppendItem(node, text) if pos == -1 else self.InsertItem(node, pos, text)
        # data is ofwel leeg, ofwel een string, ofwel een dictionary
        self.SetItemData(newnode, data)
        for item in subtree:
            self.putsubtree(newnode, item)
        return newnode


def show_message(parent, title, message):
    "show a message to the user"
    wx.MessageBox(message, title, parent=parent)


def ask_yesnocancel(parent, prompt, title):
     """stelt een vraag en retourneert het antwoord
     1 = Yes, 0 = No, -1 = Cancel
     """
     retval = dict(zip((wx.ID_YES, wx.ID_NO, wx.ID_CANCEL), (1, 0, -1)))
     hlp = wx.MessageBox(prompt, title, style=wx.YES_NO | wx.CANCEL)
     return retval[hlp]


def ask_for_text(parent, title, caption):
    "present a dialog to get some text input from the user"
    result = ''
    with wx.TextEntryDialog(parent, caption, title) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetValue()
    return result


def call_dialog(obj):
    "show a modal dialog and return results"
    with obj.gui:
        while True:
            edt = obj.gui.ShowModal()
            # if edt in (wx.ID_SAVE, wx.ID_OK, wx.ID_APPLY):
            #     ok, dialog_data = obj.gui.on_ok()  # of direct obj.confirm() ?
            #     if ok:
            #         return True, dialog_data
            if edt == wx.ID_CANCEL:
                break
            ok, dialog_data = obj.gui.on_ok()  # of direct obj.confirm() ?
            if ok:
                return True, dialog_data
    return False, None


def show_dialog(obj):
    "show a non-mpdal dialog"
    with obj.gui:
        obj.gui.Show()


def ask_for_save_filename(parent, loc, mask):
    "stuur een dialoog om een bestandsnaam te vragen voor een nieuw bestand"
    # return qtw.QFileDialog.getSaveFileName(parent, "Save file as ...", loc, mask)[0]
    return ask_for_filename(parent, loc, mask, "Save file as ...", wx.FD_SAVE)


def ask_for_open_filename(parent, loc, mask):
    "stuur een dialoog om een bestandsnaam te vragen voor een bestaand bestand"
    # return qtw.QFileDialog.getOpenFileName(parent, "Choose a file", loc, mask)[0]
    return ask_for_filename(parent, loc, mask, "Choose a file", wx.FD_OPEN)


def ask_for_filename(parent, loc, mask, message, style):
    "stuur de bestandsnaamdialoog uit en retourneer het resultaat"
    if os.path.isfile(loc):
        dirname, filename = os.path.split(loc)
    else:
        dirname, filename = loc, ''
    with wx.FileDialog(parent, message=message, defaultDir=dirname, defaultFile=filename,
                       wildcard=mask, style=style) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            return dlg.GetPath()
    return ''


def build_mask(ftype):
    """build mask for FileDialog
    """
    text, filetypes = masks['all']
    all_mask = f"{text} ({filetypes[0]})|{filetypes[0]}"
    text, filetypes = masks[ftype]
    filetypes_text = ",".join(filetypes)
    if os.name == 'posix':
        filetypes_text = f'{filetypes_text},{filetypes_text.upper()}'
    extensions_text = filetypes_text.replace(',', ';')
    return f"{text} ({filetypes_text})|{extensions_text}" + '|' + all_mask


# def ask_for_save_filename(parent, text, loc, mask):
#     "stuur een dialoog om een bestandsnaam te vragen voor een nieuw bestand"
#     with wx.FileDialog(self, message="Save file as ...", defaultDir=loc, wildcard=mask,
#                        style=wx.FD_SAVE) as dlg:
#         if dlg.ShowModal() == wx.ID_OK:
#             return dlg.GetPath()
#     return ''
#
#
# def ask_for_open_filename(parent, text, loc, mask):
#     "stuur een dialoog om een bestandsnaam te vragen voor een bestaand bestand"
#     with wx.FileDialog(self, message="Choose a file", defaultDir=loc, wildcard=mask,
#                        style=wx.FD_OPEN) as dlg:
#         if dlg.ShowModal() == wx.ID_OK:
#             return dlg.GetPath()
#     return ''


class EditDialogGui(wx.Dialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, master, parent, title):
        self.master = master
        self.title = title
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        # mogelijk moet dit naar het afmaken van de display
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.Layout()

    def add_topline(self):
        "define a line at the top of the display"
        topline = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(topline, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        return topline

    def add_label(self, topline, text):
        "add some fixed text"
        lbl = wx.StaticText(self, label="element name:")
        topline.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)

    def add_textinput(self, topline, text, width):
        "add an input box of a given width abd optionally set its text"
        tb = wx.TextCtrl(self, size=(width, -1))
        tb.SetValue(text)
        topline.Add(tb, 0, wx.ALIGN_CENTER_VERTICAL)
        return tb

    def add_checkbox(self, topline, text, state):
        "add a checkbox and optionally set its state"
        cb = wx.CheckBox(self, label=text)
        cb.SetValue(state)
        topline.Add(cb, 0, wx.ALIGN_CENTER_VERTICAL)
        return cb

    def add_content_section(self):
        "add a container with a border around it"
        frm = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(frm, wx.VERTICAL)
        self.vbox.Add(sbox, 1, wx.ALL | wx.EXPAND, 5)
        self.frm = frm      # t.b.v. unittest
        return sbox

    def add_table_to_section(self, section, columndefs, attrs):
        "add an editable table to the content area"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        table = wxgrid.Grid(self)  # , -1)  # , size=(340, 120))
        table.CreateGrid(0, 2)
        table.SetRowLabelSize(19)
        for ix, cdef in enumerate(columndefs):
            table.SetColLabelValue(ix, cdef[0])
            table.SetColSize(ix, cdef[1])
        width = self.GetSize().GetWidth() - 10 - 102
        table.SetColSize(1, width)
        self.inactive_colour = wx.SystemSettings().GetColour(wx.SYS_COLOUR_GRAYTEXT)
        if attrs:
            for attr, value in attrs.items():
                table.AppendRows(1)
                row = table.GetNumberRows() - 1
                table.SetRowLabelValue(row, '')
                table.SetCellValue(row, 0, attr)
                table.SetCellValue(row, 1, value)
                if attr in ('style', 'styledata'):
                    for i in range(1):
                        table.SetReadOnly(row, i, True)
                        table.SetCellTextColour(row, i, self.inactive_colour)
        hbox.Add(table, 1, wx.EXPAND)
        section.Add(hbox, 1, wx.ALL | wx.EXPAND, 5)
        return table

    def add_buttons_to_section(self, section, buttondefs):
        "add a line of buttons to the content area"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        for text, callback in buttondefs:
            button = wx.Button(self, label=text)
            button.Bind(wx.EVT_BUTTON, callback)
            if text == self.master.style_text:
                self.style_button = button
            hbox.Add(button, 0, wx.EXPAND | wx.ALL, 1)
        section.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        self.check_changes = False

    def add_textinput_to_section(self, section, text, width, height):
        "add a multiline text input field"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        textbox = wx.TextCtrl(self, size=(width, height), style=wx.TE_MULTILINE)
        textbox.SetValue(text)
        hbox.Add(textbox, 1, wx.EXPAND | wx.ALL, 5)
        section.Add(hbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        return textbox

    def add_text_to_section(self, section, text):
        "add a line with text to the content area"
        lbl = wx.StaticText(self, label=text)
        section.Add(lbl, 0, wx.TOP, 10)

    def add_radiobutton_to_section(self, section, text, first, selected):
        "add a radiobutton on a line by itself to the content area"
        if not text:
            section.AddSpacer()
            return
        if first:
            radio = wx.RadioButton(self, label=text, style=wx.RB_GROUP)
        else:
            radio = wx.RadioButton(self, label=text)
        if selected:
            radio.SetValue(True)
        section.Add(radio, 0, wx.ALL, 2)
        return radio

    def add_buttons_to_bottom(self):
        "add a button strip with action buttons at the bottom"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(self, id=wx.ID_SAVE)
        button.Bind(wx.EVT_BUTTON, self.on_ok)
        hbox.Add(button, 0, wx.EXPAND | wx.ALL, 2)
        button = wx.Button(self, id=wx.ID_CANCEL)
        button.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox.Add(button, 0, wx.EXPAND | wx.ALL, 2)
        self.SetAffirmativeId(wx.ID_SAVE)
        self.vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)

    def set_focus_to(self, widget):
        "position for input"
        widget.SetFocus()

    # def on_add(self, event):
    #     "attribuut toevoegen"
    #     self.refresh()
    #     self.attr_table.AppendRows(1)
    #     row = self.attr_table.GetNumberRows() - 1
    #     self.attr_table.SetRowLabelValue(row, '')
    #     self.attr_table.SelectBlock(row, 0, row, 0)

    # def on_del(self, event):
    #     "attribuut verwijderen"
    #     self.refresh()
    #     rows = self.attr_table.GetSelectedRows()
    #     if rows:
    #         rows.reverse()
    #         for row in rows:
    #             self.attr_table.DeleteRows(row, 1)
    #     else:
    #         wx.MessageBox("Select a row by clicking on the row heading", 'Selection is empty',
    #                       wx.ICON_INFORMATION)

    # def on_style(self, event):
    #     "adjust style attributes"
    #     if self.check_changes:
    #         self.refresh()
    #         self.check_changes = False
    #         self.style_button.setText(self.master.style_text)
    #         return
    #     self.check_changes = True
    #     self.style_button.SetLabel('Chec&k Changes')
    #     tag = self.tag_text.GetValue()
    #     for row in range(self.attr_table.GetNumberRows()):
    #         if self.attr_table.GetCellValue(row, 0) == 'href':
    #             fname = self.attr_table.GetCellValue(row, 1)
    #             break
    #     else:
    #         fname = ''
    #     if self.master.is_stylesheet:
    #         self.master.parent.cssm.call_editor_for_stylesheet(fname)
    #         self.refresh()
    #         self.check_changes = False
    #     else:
    #         self.master.parent.cssm.call_editor(self, tag)

    # def refresh(self):
    #     "ververs het style / styledata element i.v.m. terugkeer uit css editor"
    #     if self.tag_text.GetValue() == 'link':
    #         return
    #     self.master.is_style_tag = self.tag_text.GetValue() == 'style'
    #     attrname = 'styledata' if self.master.is_style_tag else 'style'
    #     for row in range(self.attr_table.GetNumberRows()):
    #         if self.attr_table.GetCellValue(row, 0) == attrname:
    #             if attrname == 'style':
    #                 self.master.has_style = True
    #             self.attr_table.SetCellValue(row, 1, self.master.styledata)
    #             break
    #     else:  # new attribute
    #         self.attr_table.AppendRows(1)
    #         row = self.attr_table.GetNumberRows() - 1
    #         self.attr_table.SetRowLabelValue(row, '')
    #         self.attr_table.SetCellValue(row, 0, attrname)
    #         self.attr_table.SetReadOnly(row, 0, True)
    #         self.attr_table.SetCellTextColour(row, 0, self.inactive_colour)
    #         self.attr_table.SetCellValue(row, 1, self.master.styledata)
    #         self.attr_table.SetReadOnly(row, 1, True)
    #         self.attr_table.SetCellTextColour(row, 1, self.inactive_colour)
    #         self.style_button.SetLabel(analyze_element('', {attrname: ''})[2])
    #         if attrname == 'style':
    #             self.master.has_style = True
    #     self.master.old_styledata = self.master.styledata

    def get_radiobutton_state(self, field):
        "return the state of a radiobutton"
        return field.GetValue()

    def set_radiobutton_state(self, field, state):
        "set the state of a radiobutton"
        field.SetValue(state)

    def get_textinput_value(self, field):
        "return a textfield's contents"
        return field.GetValue()

    def get_textarea_contents(self, field):
        "return a multiline textfield's contents"
        return field.GetValue()

    def get_checkbox_state(self, field):
        "return the state of a checkbox"
        return field.GetValue()

    def set_button_text(self, btn, text):
        "change text on button"
        btn.SetLabel(text)

    def get_table_rowcount(self, field):
        "return the number of rows in a table"
        return field.GetNumberRows()

    def add_table_row(self, table, row):
        "add a row at the end of the table"
        table.AppendRows(1)

    def add_table_rowitem(self, table, row, col, text, editable=True):
        "add an item to the new row and set its text and editability"
        table.SetCellValue(row, col, text)
        if not editable:
            table.SetReadOnly(row, col, True)
            table.SetCellTextColour(row, col, self.inactive_colour)

    def delete_table_row(self, table, row):
        "delete a row from the table"
        table.DeleteRows(row, 1)

    def set_table_rowheader(self, table, row, text):
        "set an empty header for  a new table row"
        table.SetRowLabelValue(row - 1, '')

    def select_table_cell(self, table, row, col):
        "select a cell from the table (for editing)"
        table.SelectBlock(row, col, row, col)

    def get_selected_table_row(self, table):
        "return the selected table row"
        rows = table.GetSelectedRows()
        return rows[0] if rows else None

    def get_tableitem_text(self, table, row, col):
        "return the text of a tableitem at a specific location"
        return table.GetCellValue(row, col)

    def set_tableitem_text(self, table, row, col, text):
        "set the text for a tableitem at a specific location"
        table.SetCellValue(row, col, text)

    def on_cancel(self, event):
        "controle bij afbreken: css kan gewijzigd zijn"
        if hasattr(self.master, 'styledata'):
            if self.master.styledata != self.master.old_styledata:
                wx.MessageBox('Bijbehorende style data is gewijzigd', 'Let op', wx.ICON_WARNING)
                self.refresh()
                return
        self.EndModal(wx.ID_CANCEL)

    def on_ok(self):
        "doorgeven in dialoog gewijzigde waarden aan hoofdscherm"
        if hasattr(self.master, 'attr_table'):
            self.refresh()
        msg = self.master.confirm()
        if msg:
            wx.MessageBox(msg, self.title, wx.ICON_ERROR)
            return False
        return True


class SearchDialogGui(wx.Dialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title=""):
        super().__init__(parent, title=title)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)
        # sizer.SetSizeHints(self)
        self.Layout()

    def setup_container(self):
        "define the grid"
        gsizer = wx.GridBagSizer(4, 4)
        self.sizer.Add(gsizer, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.LEFT | wx.RIGHT, 8)
        return gsizer

    def add_title(self, gsizer, text, row, col):
        "add some text at the top (full width)"
        lbl = wx.StaticText(self, label=text)
        gsizer.Add(lbl, (row, col), (1, 3))

    def add_text(self, gsizer, text, row, col):
        "add some fixed text to a cell"
        lbl = wx.StaticText(self, label=text)
        gsizer.Add(lbl, (row, col), flag=wx.ALIGN_CENTER_VERTICAL)
        # vsizer = wx.BoxSizer(wx.VERTICAL)
        # hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # lbl_element = wx.StaticText(self, label="name: ")
        # hsizer.Add(lbl_element, flag=wx.ALIGN_CENTER_VERTICAL)

    def add_lineinput(self, gsizer, row, col, callback):
        "add a text input box to a cell"
        txt = wx.TextCtrl(self, size=(120, -1))
        txt.Bind(wx.EVT_TEXT, callback)
        # hsizer.Add(txt)
        # vsizer.Add(hsizer)
        # gsizer.Add(vsizer, (0, 1))
        gsizer.Add(txt, (row, col))
        return txt

    def add_checkbox(self, gsizer, text, row, col):
        "add a checkbox to a cell"
        cb = wx.CheckBox(self, text)
        gsizer.Add(cb, (row, col), (1, 3))
        return cb

    def add_description(self):
        "add search summary text"
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label='')
        hsizer.Add(lbl)
        self.sizer.Add(hsizer, 0, wx.LEFT | wx.RIGHT, 8)
        return lbl

    def add_buttons_to_bottom(self):
        "add some action buttons at the bottom of the display"
        # hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.ok_button = wx.Button(self, id=wx.ID_OK)
        # # self.SetAffirmativeId(wx.ID_OK)
        # # self.SetAffirmativeId(self.ok_button.GetId())
        # self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        # hsizer.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        # hsizer.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        # sizer.Add(hsizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
        #           wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)
        # buttons = self.CreateButtonSizer(wx.APPLY | wx.CLOSE)
        # self.SetAffirmativeId(wx.ID_APPLY)
        # self.SetEscapeId(wx.ID_CLOSE)
        buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.sizer.Add(buttons)


        # if self._parent.search_args:
        #     self.txt_element.SetValue(self._parent.search_args[0])
        #     self.txt_attr_name.SetValue(self._parent.search_args[1])
        #     self.txt_attr_val.SetValue(self._parent.search_args[2])
        #     self.txt_text.SetValue(self._parent.search_args[3])

    def set_lineinput_value(self, field, text):
        "set the value for a text input field"
        field.SetValue(text)

    def get_lineinput_value(self, field):
        "return the value of a text input field"
        return field.GetValue()

    def get_checkbox_state(self, field):
        "return the state of a checkbox"
        return field.GetValue()

    def set_focus_to(self, widget):
        "position for input"
        widget.SetFocus()

    def set_label_text(self, field, text):
        "update the value for a label field"
        field.SetLabel(text)

    def update_size(self):
        "adjust widget sizer after changing text contents"
        self.sizer.Fit()

    def on_ok(self):
        "confirm dialog and pass changed data to parent"
        return self.master.confirm()


class AddDialogGui(wx.Dialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, master, parent, title):
        self.master = master
        self.title = title
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        # mogelijk moet dit naar het afmaken van de display
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.Layout()

    def add_content_section(self):
        "add a container with a border around it"
        frm = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(frm, wx.VERTICAL)
        # self.vbox.Add(sbox, 1, wx.ALL | wx.EXPAND, 5)
        self.vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        grid = wx.GridBagSizer(4,4)
        sbox.Add(grid, 0, wx.ALL, 10)
        self.frm = frm   # alleen t.b.v. unittest
        return grid

    def add_text_to_section(self, grid, text, row, col):
        "add fixed text to a cell in the content area"
        lbl = wx.StaticText(self, label=text)
        grid.Add(lbl, (row, col), flag=wx.ALIGN_CENTER_VERTICAL)

    def add_textinput_to_section(self, grid, row, col, text='', width=0, callback=None):
        "add a text input to a cell in the content area"
        width = width or 250
        edit = wx.TextCtrl(self, size=(width, -1), value=text)
        if callback:
            edit.Bind(wx.EVT_TEXT, callback)
        grid.Add(edit, (row, col))
        return edit

    def add_button_line_to_section(self, grid, row, buttondefs):
        "add a line with one or more buttons to the content area"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        for text, callback in buttondefs:
            button = wx.Button(self, label=text)
            button.Bind(wx.EVT_BUTTON, callback)
            hbox.Add(button, 0, wx.EXPAND | wx.ALL, 2)
        grid.Add(hbox, (row, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

    def add_spinbox_to_section(self, grid, row, col, maxvalue=0, startvalue=0, callback=None):
        "add a spinbox to a cell in the content area"
        sb = wx.SpinCtrl(self)  # .pnl, -1, size = (40, -1))
        sb.SetMax(maxvalue)
        sb.SetValue(startvalue)
        if callback:
            sb.Bind(wx.EVT_SPINCTRL, callback)
        grid.Add(sb, (row, col))
        return sb

    def add_combobox_to_section(self, grid, row, col, values, callback=None):
        "add a combobox to a cell in the content area"
        select = wx.ComboBox(self, style=wx.CB_DROPDOWN, choices=values)
        # select.SetStringSelection(values[0])
        if callback:
            select.Bind(wx.EVT_COMBOBOX, callback)
        grid.Add(select, row, col)
        return select

    def add_checkbox_to_section(self, grid, row, col, text, checked=False, callback=None):
        "add a checkbox to a cell in the content area"
        cb = wx.CheckBox(self, label=text)
        if checked:
            cb.SetValue(True)
        if callback:
            cb.Bind(wx.EVT_CHECKBOX, callback)
        grid.Add(cb, (row, col), flag=wx.ALL, border=5)
        return cb

    def add_table_to_section(self, grid, row, initialrows, headers, callback=None):
        "add a full-width table to the content area"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        table = wxgrid.Grid(self, size=(340, 120))
        table.CreateGrid(initialrows, len(headers))
        for ix, text in enumerate(headers):
            table.SetColLabelValue(ix, text)
            # table.SetColSize(ix, 240)
        if callback:
            table.Bind(wxgrid.EVT_GRID_LABEL_LEFT_CLICK, callback)
            table.Bind(wxgrid.EVT_GRID_LABEL_LEFT_DCLICK, callback)
            table.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_CLICK, callback)
            table.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_DCLICK, callback)
        grid.Add(table, (row, 1), (1, 2), wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        return table

    def add_buttons_to_bottom(self, extra=()):
        "add a button strip with action buttons at the bottom"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, id=wx.ID_SAVE)
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        hbox.Add(ok_button, 0, wx.EXPAND | wx.ALL, 2)
        if extra:
            inline_button = wx.Button(self, label=extra[0])
            inline_button.Bind(wx.EVT_BUTTON, extra[1])
            hbox.Add(inline_button, 0, wx.EXPAND | wx.ALL, 2)
        cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox.Add(cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        self.SetAffirmativeId(wx.ID_SAVE)
        self.vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)

    def get_textinput_value(self, field):
        "return a textfield's contents"
        return field.GetValue()

    def set_textinput_value(self, field, value):
        "set a textfield's contents"
        return field.SetValue(value)

    def get_conbobox_text(self, cb):
        "return the selected text in a combobox"
        return cb.GetValue()
        #return cb.GetStringSelection()

    def get_spinbox_value(self, sb):
        "return the value of a spinbox"
        return sb.GetValue()

    def get_checkbox_state(self, cb):
        "return the state of a checkbox"
        return cb.IsChecked()

    def get_table_columncount(self, table):
        "return the number of columns in the table"
        return table.GetNumberCols()

    def get_table_rowcount(self, table):
        "return the number of rows in the table"
        return table.GetNumberRows()

    def get_tablecell_itemtext(self, table, row, col):
        "return the contents of a cell at a given position"
        return table.GetCellValue(row, col)

    def set_table_headers(self, table, headers, widths):
        "reset the column titles and widths "
        for ix, title in enumerate(headers):
            table.SetColLabelValue(ix, title)
        for ix, width in enumerate(widths):
            table.SetColSize(ix, width)

    def enable_table_header(self, table, value):
        "make table header (visible and) clickable"
        table.SetColLabelSize(24 if value else 0)

    def add_table_column(self, table, colno):
        "add a table column"
        table.InsertCols(colno, 1)

    def add_table_row(self, table, colno):
        "add a table row"
        table.AppendRows(1)
        table.SetRowLabelValue(colno, '')

    def remove_table_column(self, table, colno):
        "remove a table column"
        table.DeleteCols(colno)

    def remove_table_row(self, table, colno):
        "remove a table row"
        table.DeleteRows(colno)

    def get_table_column(self, *args):
        "return the column for which the header was clicked"
        evt = args[0]
        return evt.GetCol()

    def enable_widget(self, widget, value):
        "make a widget responsive or not"
        widget.Enable(value)

    def on_cancel(self, event):
        "controle bij afbreken: css kan gewijzigd zijn"
        self.EndModal(wx.ID_CANCEL)

    def on_ok(self):
        "doorgeven in dialoog gewijzigde waarden aan hoofdscherm"
        msg = self.master.confirm()
        if msg:
            wx.MessageBox(msg, self.title, wx.ICON_ERROR)
            return False
        return True


class ScrolledTextDialogGui(wx.Dialog):
    """dialoog voor het tonen van validatieoutput

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, master, parent, title):
        self.master = master
        super().__init__(parent, title=title, size=(600, 400))
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.Layout()

    def add_top_label(self, text):
        "add a message to the top of the display"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self)
        lbl.SetLabel(text)
        hbox.Add(lbl)
        self.vbox.Add(hbox)

    def add_text_area(self):
        "build the space for the text to display"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox.Add(text, 1, wx.EXPAND)
        self.vbox.Add(hbox)
        return text

    def add_bottom_buttons(self, buttondefs):
        "add one or more action buttons"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        first = True
        for text, callback in buttondefs:
            button = wx.Button(self, label=text)
            if first:
                self.SetAffirmativeId(button.GetId())
                first = False
            else:
                button.Bind(wx.EVT_BUTTON, callback)
            hbox.Add(button)
        self.vbox.Add(hbox)

    def set_textarea_contents(self, textfield, data):
        "transmit the text to display"
        textfield.SetValue(data)


class CodeViewDialogGui(wx.Dialog):
    """dialoog voor het tonen van de broncode

    create a window with a scintilla text widget and an ok button
    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.Layout()

    def add_top_message(self, text):
        "add a message to the top of the display"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label=text))
        self.vbox.Add(hbox)

    def add_content_area(self, data):
        "define the space for the main content"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wxstc.StyledTextCtrl(self)
        # self.setup_text()
        text.SetText(data)
        text.SetReadOnly(True)
        hbox.Add(text, 1, wx.EXPAND | wx.ALL)
        self.text = text   # alleen voor unittest
        self.vbox.Add(hbox)

    def add_bottom_button(self):
        "add an action button at the bottom of the display"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, label='&Done')
        self.SetAffirmativeId(ok_button.GetId())
        hbox.Add(ok_button)
        self.vbox.Add(hbox)

    def setup_text(self):
        "define the scintilla widget's properties"
        # # Set the default font
        # font = gui.QFont()
        # font.setFamily('Courier')
        # font.setFixedPitch(True)
        # font.setPointSize(10)
        # self.text.setFont(font)
        # self.text.setMarginsFont(font)

        # # Margin 0 is used for line numbers
        # fontmetrics = gui.QFontMetrics(font)
        # self.text.setMarginsFont(font)
        # self.text.setMarginWidth(0, fontmetrics.width("00000"))
        # self.text.setMarginLineNumbers(0, True)
        # self.text.setMarginsBackgroundColor(gui.QColor("#cccccc"))

        # # Enable brace matching, auto-indent, code-folding
        # self.text.setBraceMatching(sci.QsciScintilla.SloppyBraceMatch)
        # self.text.setAutoIndent(True)
        # self.text.setFolding(sci.QsciScintilla.PlainFoldStyle)

        # # Current line visible with special background color
        # self.text.setCaretLineVisible(True)
        # self.text.setCaretLineBackgroundColor(gui.QColor("#ffe4e4"))

        # # Set HTML lexer
        # lexer = sci.QsciLexerHTML()
        # lexer.setDefaultFont(font)
        # self.text.setLexer(lexer)
