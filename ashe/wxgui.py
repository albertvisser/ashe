"""wxPython specifieke routines voor mijn op een treeview gebaseerde HTML-editor
"""
import os
import wx
import wx.grid as wxgrid
import wx.lib.mixins.treemixin as treemix
import wx.html2 as wxhtml  # webkit
import wx.stc as wxstc

from ashe.shared import ELSTART, masks


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
        # self.top = self.tree.AddRoot(fname)
        top = self.tree.AddRoot(fname)
        self.top = self.tree.AppendItem(top, os.path.abspath(fname))

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
                menuitem = wx.MenuItem(menu, wx.ID_ANY, item[0], item[2])
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

    def meld(self, text):
        """notify about some information"""
        wx.MessageBox(text, self.editor.title, parent=self)

    def ensure_item_visible(self, item):
        """make sure we can see the item
        """
        self.tree.EnsureVisible(item)


class VisualTree(treemix.DragAndDrop, wx.TreeCtrl):
    """tree representation of HTML
    """
    def __init__(self, parent):  # , size):
        self._parent = parent.Parent
        super().__init__(parent)  # , size=size)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_leftdclick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

    def on_leftdclick(self, evt):
        "start edit bij dubbelklikken tenzij op filenaam"
        item = self.HitTest(evt.GetPosition())[0]
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
        """check for context menu key
        """
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
    # retval = dict(zip((wx.ID_YES, wx.ID_NO, wx.ID_CANCEL), (1, 0, -1)))
    retval = dict(zip((wx.YES, wx.NO, wx.CANCEL), (1, 0, -1)))
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
            ok = obj.gui.refresh_if_necessary(edt)
            if ok:
                if edt == wx.ID_CANCEL:
                    break
                msg = obj.confirm()
                if msg:
                    wx.MessageBox(msg, 'HTMLEdit', wx.ICON_WARNING)
                else:
                    return True, obj.parent.dialog_data
    return False, None


def show_dialog(obj):
    "show a non-mpdal dialog"
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
        lbl = wx.StaticText(self, label=text)
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
        # width = self.GetSize().GetWidth() - 10 - 102
        # table.SetColSize(1, width)
        self.inactive_colour = wx.SystemSettings().GetColour(wx.SYS_COLOUR_GRAYTEXT)
        if attrs:
            for attr, value in attrs.items():
                table.AppendRows(1)
                row = table.GetNumberRows() - 1
                table.SetRowLabelValue(row, '')
                table.SetCellValue(row, 0, attr)
                table.SetCellValue(row, 1, value)
                if attr in ('style', 'styledata'):
                    for i in range(2):
                        table.SetReadOnly(row, i, True)
                        table.SetCellTextColour(row, i, self.inactive_colour)
        hbox.Add(table, 1, wx.EXPAND)
        section.Add(hbox, 1, wx.ALL | wx.EXPAND, 5)
        return table

    def add_buttons_to_section(self, section, buttondefs):
        "add a line of buttons to the content area"
        result = []
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        for text, callback in buttondefs:
            button = wx.Button(self, label=text)
            button.Bind(wx.EVT_BUTTON, callback)
            if text == self.master.style_text:
                result.append(button)
            hbox.Add(button, 0, wx.EXPAND | wx.ALL, 1)
        section.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        self.check_changes = False
        return result

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
            section.AddSpacer(5)
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
        # button.Bind(wx.EVT_BUTTON, self.on_ok)
        hbox.Add(button, 0, wx.EXPAND | wx.ALL, 2)
        button = wx.Button(self, id=wx.ID_CANCEL)
        # button.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox.Add(button, 0, wx.EXPAND | wx.ALL, 2)
        self.SetAffirmativeId(wx.ID_SAVE)
        self.vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL
                      | wx.ALIGN_CENTER_VERTICAL, 20)

    def set_focus_to(self, widget):
        "position for input"
        widget.SetFocus()

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
        table.SetRowLabelValue(row, text)

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

    def refresh_if_necessary(self, edt):
        "dialog-specific result handling"
        if edt == wx.ID_CANCEL and hasattr(self.master, 'styledata'):
            if self.master.styledata != self.master.old_styledata:
                wx.MessageBox('Bijbehorende style data is gewijzigd', 'Let op', wx.ICON_WARNING)
                self.master.refresh()
                return False
        if edt == wx.ID_OK and hasattr(self.master, 'attr_table'):
            self.master.refresh()
        return True


class SearchDialogGui(wx.Dialog):
    """Dialog to get search arguments
    """
    def __init__(self, master, parent, title=""):
        self.master = master
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

    def add_lineinput(self, gsizer, row, col, callback):
        "add a text input box to a cell"
        txt = wx.TextCtrl(self, size=(120, -1))
        txt.Bind(wx.EVT_TEXT, callback)
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
        buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.sizer.Add(buttons)

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
        self.sizer.Fit(self)

    def refresh_if_necessary(self, *args):
        "dialog-specific result handling"
        return True


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
        grid = wx.GridBagSizer(4, 4)
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
        result = []
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        for text, callback in buttondefs:
            button = wx.Button(self, label=text)
            button.Bind(wx.EVT_BUTTON, callback)
            hbox.Add(button, 0, wx.EXPAND | wx.ALL, 2)
            result.append(button)
        grid.Add(hbox, (row, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)
        return result

    def add_spinbox_to_section(self, grid, row, col, maxvalue=0, startvalue=0, callback=None):
        "add a spinbox to a cell in the content area"
        sb = wx.SpinCtrl(self)  # .pnl, -1, size = (40, -1))
        if maxvalue:
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
        grid.Add(select, (row, col))
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
        table = wxgrid.Grid(self)  # , size=(340, 120))
        table.CreateGrid(initialrows, len(headers))
        for ix, text in enumerate(headers):
            table.SetColLabelValue(ix, text)
            # table.SetColSize(ix, 240)
        table.SetRowLabelSize(12)
        table.SetRowLabelValue(0, '')
        if callback:
            table.Bind(wxgrid.EVT_GRID_LABEL_LEFT_CLICK, callback)
            table.Bind(wxgrid.EVT_GRID_LABEL_LEFT_DCLICK, callback)
            table.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_CLICK, callback)
            table.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_DCLICK, callback)
        grid.Add(table, (row, 0), (1, 2), wx.EXPAND)  # | wx.LEFT | wx.RIGHT | wx.TOP, 3)
        return table

    def add_buttons_to_bottom(self, extra=()):
        "add a button strip with action buttons at the bottom"
        buttons = []
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, id=wx.ID_SAVE)
        # ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        hbox.Add(ok_button, 0, wx.EXPAND | wx.ALL, 2)
        if extra:
            inline_button = wx.Button(self, label=extra[0])
            inline_button.Bind(wx.EVT_BUTTON, extra[1])
            hbox.Add(inline_button, 0, wx.EXPAND | wx.ALL, 2)
            buttons.append(inline_button)
        cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        # cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox.Add(cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        self.SetAffirmativeId(wx.ID_SAVE)
        self.vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL
                      | wx.ALIGN_CENTER_VERTICAL, 20)
        return buttons

    def set_focus_to(self, widget):
        "position for input"
        widget.SetFocus()

    def get_textinput_value(self, field):
        "return a textfield's contents"
        return field.GetValue()

    def set_textinput_value(self, field, value):
        "set a textfield's contents"
        return field.SetValue(value)

    def get_combobox_text(self, cb):
        "return the selected text in a combobox"
        return cb.GetValue()
        # return cb.GetStringSelection()

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

    def refresh_if_necessary(self, *args):
        "dialog-specific result handling"
        return True


class ScrolledTextDialogGui(wx.Dialog):
    """dialoog voor het tonen van validatieoutput

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        # self.vbox.Fit(self)
        # self.vbox.SetSizeHints(self)
        # self.SetMinSize((600, 600))
        self.Layout()

    def add_top_label(self, text):
        "add a message to the top of the display"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self)
        lbl.SetLabel(text)
        hbox.Add(lbl, 0, wx.LEFT, 10)
        self.vbox.Add(hbox)

    def add_text_area(self):
        "build the space for the text to display"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox.Add(text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.vbox.Add(hbox, 1, wx.EXPAND)
        return text

    def add_bottom_buttons(self, buttondefs):
        "add one or more action buttons"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        first = True
        for text, callback in buttondefs:
            button = wx.Button(self, label=text)
            if first:
                self.SetAffirmativeId(button.GetId())
                first = False
            else:
                button.Bind(wx.EVT_BUTTON, callback)
            hbox.Add(button)
        hbox.AddStretchSpacer()
        self.vbox.Add(hbox, 0, wx.ALIGN_CENTER)

    def set_textarea_contents(self, textfield, data):
        "transmit the text to display"
        textfield.SetValue(data)

    def close(self, *args):
        "dialoog afsluiten"
        self.Close()


class CodeViewDialogGui(wx.Dialog):
    """dialoog voor het tonen van de broncode

    create a window with a scintilla text widget and an ok button
    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.SetMinSize((800, 600))
        self.Layout()

    def add_top_message(self, text):
        "add a message to the top of the display"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label=text), 1, wx.LEFT, 10)
        self.vbox.Add(hbox)

    def add_content_area(self, data):
        "define the space for the main content"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wxstc.StyledTextCtrl(self)
        # self.setup_text()
        text.SetText(data)
        text.SetReadOnly(True)
        hbox.Add(text, 1, wx.EXPAND | wx.ALL, 10)
        self.text = text   # alleen voor unittest
        self.vbox.Add(hbox, 1, wx.EXPAND)

    def add_bottom_button(self):
        "add an action button at the bottom of the display"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # hbox.AddStretchSpacer()
        ok_button = wx.Button(self, label='&Done')
        self.SetAffirmativeId(ok_button.GetId())
        hbox.Add(ok_button)  # , flag=wx.ALIGN_CENTRE)
        # hbox.AddStretchSpacer()
        self.vbox.Add(hbox, 0, wx.ALIGN_CENTER)

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
