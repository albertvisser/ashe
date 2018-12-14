"""wxPython versie van mijn op een treeview gebaseerde HTML-editor

custom dialogen
"""
import os
# import sys
import string
import wx
import wx.grid as wxgrid
# import wx.html as html
# from wx.lib.dialogs import ScrolledMessageDialog
import ashe.ashe_mixin as ed

## try:
    ## import cssedit.editor.csseditor_qt as csed
    ## cssedit_available = True
## except ImportError:
cssedit_available = False

DESKTOP = ed.DESKTOP
CMSTART = ed.CMSTART
ELSTART = ed.ELSTART
CMELSTART = ed.CMELSTART
DTDSTART = ed.DTDSTART
IMASK = "All files|*.*"
if os.name == "nt":
    HMASK = "HTML files (*.htm,*.html)|*.htm;*.html|All files (*.*)|*.*"
elif os.name == "posix":
    HMASK = "HTML files (*.htm,*.HTM,*.html,*.HTML)|*.htm;*.HTM;*.html;*.HTML|All files (*.*)|*.*"


class ElementDialog(wx.Dialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, parent, title='', tag=None, attrs=None):
        wx.Dialog.__init__(self, parent, -1, title=title,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.pnl = self
        self.parent = parent
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self.pnl, -1, "element name:")
        self.tag_text = wx.TextCtrl(self.pnl, -1, size=(150, -1))
        self.comment_button = wx.CheckBox(self.pnl, label='&Comment(ed)')
        iscomment = False
        if tag:
            x = tag.split(None, 1)
            if x[0] == CMSTART:
                iscomment = True
                x = x[1].split(None, 1)
            if x[0] == ELSTART:
                x = x[1].split(None, 1)
            self.tag_text.SetValue(x[0])
            ## self.tag_text.readonly=True
        self.comment_button.SetValue(iscomment)
        hbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.tag_text, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.comment_button, 0, wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        tbl = wxgrid.Grid(self.pnl, -1, size=(340, 120))
        tbl.CreateGrid(0, 2)
        tbl.SetColLabelValue(0, 'attribute')
        tbl.SetColLabelValue(1, 'value')
        tbl.SetColSize(1, tbl.Size[0] - 162)  # 178) # 160)   ## FIXME: werkt dit?
        if attrs:
            for attr, value in attrs.items():
                tbl.AppendRows(1)
                idx = tbl.GetNumberRows() - 1
                tbl.SetRowLabelValue(idx, '')
                tbl.SetCellValue(idx, 0, attr)
                tbl.SetCellValue(idx, 1, value)
        else:
            self.row = -1
        self.attr_table = tbl
        hbox.Add(self.attr_table, 1, wx.EXPAND)
        sbox.Add(hbox, 1, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self.pnl, label='&Add Attribute')
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_button = wx.Button(self.pnl, label='&Delete Selected')
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_del)
        hbox.Add(self.add_button, 0, wx.EXPAND | wx.ALL, 1)
        hbox.Add(self.delete_button, 0, wx.EXPAND | wx.ALL, 1)
        sbox.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        vbox.Add(sbox, 1, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)

        ## self.Bind(wx.EVT_SIZE, self.on_resize)
        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.tag_text.SetFocus()
        ## self.Show(True)

    ## def on_resize(self, evt=None):
        ## self.attr_table.SetColSize(1, self.attr_table.GetSize()[0] - 162) # 178) # 160)
        ## self.attr_table.ForceRefresh()

    def on_add(self, evt=None):
        "attribuut toevoegen"
        self.attr_table.AppendRows(1)
        idx = self.attr_table.GetNumberRows() - 1
        self.attr_table.SetRowLabelValue(idx, '')

    def on_del(self, evt=None):
        "attribuut verwijderen"
        rows = self.attr_table.GetSelectedRows()
        if rows:
            rows.reverse()
            for row in rows:
                self.attr_table.DeleteRows(row, 1)
        else:
            wx.MessageBox("Select a row by clicking on the row heading", 'Selection is empty',
                          wx.ICON_INFORMATION)

    def on_ok(self, evt=None):
        "controle bij OK aanklikken"
        tag = self.tag_text.GetValue()
        okay = True
        test = string.ascii_letters + string.digits
        for letter in tag:
            if letter not in test:
                okay = False
                wx.MessageBox('Illegal character(s) in tag name', self.parent.title, wx.ICON_ERROR)
                break
        if okay:
            evt.Skip()


class TextDialog(wx.Dialog):
    """dialoog om een tekst element op te voeren of aan te passen
    biedt tevens de mogelijkheid de tekst "op commentaar" te zetten"""

    def __init__(self, parent, title='', text=None):
        iscomment = False
        if text is None:
            text = ''
        else:
            if text.startswith(CMSTART):
                iscomment = True
                dummy, text = text.split(None, 1)
        wx.Dialog.__init__(self, parent, -1, title,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.comment_button = wx.CheckBox(self.pnl, label='&Comment(ed)')
        self.comment_button.SetValue(iscomment)
        hbox.Add(self.comment_button, 0, wx.EXPAND | wx.ALL, 1)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.data_text = wx.TextCtrl(self.pnl, -1, size=(340, 175), style=wx.TE_MULTILINE)
        self.data_text.SetValue(text)
        hbox.Add(self.data_text, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)
        self.sizer = vbox
        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.data_text.SetFocus()


class SearchDialog(wx.Dialog):
    """Dialog to get search arguments
    """


class DtdDialog(wx.Dialog):
    "dialoog om het toe te voegen dtd te selecteren"
    dtd_list = ed.dtdlist

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add DTD")
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self.pnl, -1, "Select document type:")
        hbox.Add(lbl, 0, wx.TOP, 10)
        sbox.Add(hbox, 0)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        first = True
        for x in self.dtd_list:
            if not x[0]:
                hbox.Add(vbox2)
                sbox.Add(hbox, 0, wx.ALL, 10)
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                vbox2 = wx.BoxSizer(wx.VERTICAL)
                continue
            if first:
                radio = wx.RadioButton(self.pnl, -1, x[0], style=wx.RB_GROUP)
                first = False
            else:
                radio = wx.RadioButton(self.pnl, -1, x[0])
            x.append(radio)
            vbox2.Add(radio, 0, wx.ALL, 2)
        hbox.Add(vbox2)
        sbox.Add(hbox, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(sbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.SetAffirmativeId(wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id=wx.ID_CANCEL)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)
        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()


class CssDialog(wx.Dialog):
    """dialoog om een styleheet toe te voegen
    """


class LinkDialog(wx.Dialog):
    """Dialoog om een link element toe te voegen
    """
    def __init__(self, parent):
        self.parent = parent
        wx.Dialog.__init__(self, parent, title='Add Link')
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)

        lbl = wx.StaticText(self.pnl, -1, "descriptive title:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.title_text = wx.TextCtrl(self.pnl, -1, size=(250, -1))
        gbox.Add(self.title_text, (0, 1))

        lbl = wx.StaticText(self.pnl, -1, "link to document:")
        gbox.Add(lbl, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self.pnl, -1, size=(250, -1), value="http://")
        self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (1, 1))

        self.choose_button = wx.Button(self.pnl, -1, 'Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (2, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText(self.pnl, -1, "link text:")
        gbox.Add(lbl, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.text_text = wx.TextCtrl(self.pnl, -1, size=(250, -1))
        self.text_text.Bind(wx.EVT_TEXT, self.set_text)
        gbox.Add(self.text_text, (3, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.title_text.SetFocus()

    def kies(self, evt=None):
        "methode om het te linken document te selecteren"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=os.getcwd(),
                            wildcard=HMASK, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.link_text.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_ok(self, evt=None):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        link = self.link_text.GetValue()
        if link:
            if not link.startswith('http://') and not link.startswith('/'):
                if self.parent.xmlfn:
                    whereami = self.parent.xmlfn
                else:
                    whereami = os.path.join(os.getcwd(), 'index.html')
                link = ed.getrelativepath(link, whereami)
            if not link:
                wx.MessageBox('Impossible to make this local link relative',
                              self.parent.title)
            else:
                self.link = link
                evt.Skip()
        else:
            wx.MessageBox("link opgeven of cancel kiezen s.v.p", self.parent.title)

    def set_text(self, evt=None):
        'indien leeg link tekst gelijk maken aan link adres'
        if evt.EventObject == self.link_text:
            linktxt = self.link_text.GetValue()
            if self.text_text.GetValue() == self.linktxt:
                self.text_text.SetValue(linktxt)
                self.linktxt = linktxt
        elif self.text_text.GetValue() == "":
            self.linktxt = ""


class ImageDialog(wx.Dialog):
    'dialoog om een image toe te voegen'

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='Add Image')
        self.parent = parent
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)

        lbl = wx.StaticText(self.pnl, -1, "descriptive title:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.title_text = wx.TextCtrl(self.pnl, -1, size=(250, -1))
        gbox.Add(self.title_text, (0, 1))

        lbl = wx.StaticText(self.pnl, -1, "link to image:")
        gbox.Add(lbl, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self.pnl, -1, size=(250, -1), value="http://")
        self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (1, 1))

        self.choose_button = wx.Button(self.pnl, -1, 'Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (2, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText(self.pnl, -1, "alternate text:")
        gbox.Add(lbl, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.alt_text = wx.TextCtrl(self.pnl, -1, size=(250, -1))
        self.alt_text.Bind(wx.EVT_TEXT, self.set_text)
        gbox.Add(self.alt_text, (3, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.title_text.SetFocus()

    def kies(self, evt=None):
        "methode om het te linken image te selecteren"
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=os.getcwd(),
                            wildcard=IMASK, style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.link_text.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_ok(self, evt=None):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        link = self.link_text.GetValue()
        if link:
            if not link.startswith('http://') and not link.startswith('/'):
                if self.parent.xmlfn:
                    whereami = self.parent.xmlfn
                else:
                    whereami = os.path.join(os.getcwd(), 'index.html')
                link = ed.getrelativepath(link, whereami)
            if not link:
                wx.MessageBox('Impossible to make this local link relative', self.parent.title)
            else:
                self.link = link
                evt.Skip()
        else:
            wx.MessageBox("image link opgeven of cancel kiezen s.v.p", self.parent.title)

    def set_text(self, evt=None):
        'indien leeg link tekst gelijk maken aan link adres'
        if evt.EventObject == self.link_text:
            linktxt = self.link_text.GetValue()
            if self.alt_text.GetValue() == self.linktxt:
                self.alt_text.SetValue(linktxt)
                self.linktxt = linktxt
        elif self.alt_text.GetValue() == "":
            self.linktxt = ""


class VideoDialog(wx.Dialog):
    """Dialoog om een video element toe te voegen
    """


class AudioDialog(wx.Dialog):
    """Dialoog om een audio element toe te voegen
    """


class ListDialog(wx.Dialog):
    'dialoog om een list toe te voegen'

    def __init__(self, parent):
        self.items = []
        self.dataitems = []
        wx.Dialog.__init__(self, parent, title='Add List',
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        tbox = wx.FlexGridSizer(2, 2, 2, 2)
        lbl = wx.StaticText(self.pnl, -1, "choose type of list:")
        self.type_select = wx.ComboBox(self.pnl, -1, style=wx.CB_DROPDOWN, choices=["unordered",
                                                                                    "ordered",
                                                                                    "definition"])
        self.type_select.SetStringSelection("unordered")
        self.type_select.Bind(wx.EVT_COMBOBOX, self.on_type)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.type_select)

        lbl = wx.StaticText(self.pnl, -1, "initial number of items:")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.rows_text = wx.SpinCtrl(self.pnl)
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_text)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.rows_text)  # hbox)
        sbox.Add(tbox, 0, wx.ALL, 5)

        tbl = wxgrid.Grid(self.pnl, -1, size=(340, 120))
        tbl.CreateGrid(0, 1)
        tbl.SetColLabelValue(0, 'list item')
        tbl.SetColSize(0, 240)
        self.list_table = tbl
        sbox.Add(self.list_table, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(sbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.type_select.SetFocus()

    def on_type(self, evt=None):
        "geselecteerde list type toepassen"
        sel = self.type_select.GetValue()
        numcols = self.list_table.GetNumberCols()
        if sel[0] == "d" and numcols == 1:
            self.list_table.InsertCols(0, 1)
            self.list_table.SetColLabelValue(0, 'term')
            self.list_table.SetColSize(0, 80)
            self.list_table.SetColLabelValue(1, 'description')
            self.list_table.SetColSize(1, 160)
        elif sel[0] != "d" and numcols == 2:
            self.list_table.DeleteCols(0)
            self.list_table.SetColLabelValue(0, 'list item')
            self.list_table.SetColSize(0, 240)

    def on_text(self, evt=None):
        "controle en actie bij invullen/aanpassen aantal regels"
        try:
            cur_rows = int(self.rows_text.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer', self.parent.title)
            return
        num_rows = self.list_table.GetNumberRows()
        if num_rows > cur_rows:
            for idx in range(num_rows - 1, cur_rows - 1, -1):
                self.list_table.DeleteRows(idx)
        elif cur_rows > num_rows:
            for idx in range(num_rows, cur_rows):
                self.list_table.AppendRows(1)
                self.list_table.SetRowLabelValue(idx, '')


class TableDialog(wx.Dialog):
    "dialoog om een tabel toe te voegen"

    def __init__(self, parent):
        self.parent = parent
        wx.Dialog.__init__(self, parent, -1, title='Add Table',
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.pnl = self
        self.headings = []
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        tbox = wx.FlexGridSizer(3, 2, 2, 2)

        lbl = wx.StaticText(self.pnl, -1, "summary (description):")
        tbox.Add(lbl)
        self.title_text = wx.TextCtrl(self.pnl, -1, size=(250, -1))
        tbox.Add(self.title_text)

        lbl = wx.StaticText(self.pnl, -1, "initial number of rows:")
        ## self.rows_text = wx.TextCtrl(self.pnl, -1)
        self.rows_text = wx.SpinCtrl(self.pnl, -1)
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_rows)
        self.rows_text.Bind(wx.EVT_TEXT, self.on_rows)
        tbox.Add(lbl)
        tbox.Add(self.rows_text)

        lbl = wx.StaticText(self.pnl, -1, "initial number of columns:")
        ## self.cols_text = wx.TextCtrl(self.pnl, -1)
        self.cols_text = wx.SpinCtrl(self.pnl)
        self.cols_text.Bind(wx.EVT_SPINCTRL, self.on_cols)
        self.cols_text.Bind(wx.EVT_TEXT, self.on_cols)
        tbox.Add(lbl)
        tbox.Add(self.cols_text)
        sbox.Add(tbox, 0, wx.ALL, 5)

        tbl = wxgrid.Grid(self.pnl, -1, size=(340, 120))
        tbl.CreateGrid(0, 0)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_LEFT_CLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_LEFT_DCLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_DCLICK, self.on_title)
        self.table_table = tbl
        sbox.Add(self.table_table, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(sbox, 1, wx.EXPAND | wx.ALL, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 20)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.title_text.SetFocus()

    def on_rows(self, evt=None):
        "controle en actie bij opgeven aantal regels"
        try:
            cur_rows = int(self.rows_text.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer', self.parent.title)
            return
        num_rows = self.table_table.GetNumberRows()
        if num_rows > cur_rows:
            for idx in range(num_rows - 1, cur_rows - 1, -1):
                ## prinum_rows idx
                self.table_table.DeleteRows(idx)
        elif cur_rows > num_rows:
            for idx in range(num_rows, cur_rows):
                self.table_table.AppendRows(1)
                self.table_table.SetRowLabelValue(idx, '')

    def on_cols(self, evt=None):
        "controle en actie bij opgeven aantal kolommen"
        try:
            cur_cols = int(self.cols_text.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer', self.parent.title)
            return
        num_cols = self.table_table.GetNumberCols()
        if num_cols > cur_cols:
            for idx in range(num_cols - 1, cur_cols - 1, -1):
                ## prinum_cols idx
                self.table_table.DeleteCols(idx)
        elif cur_cols > num_cols:
            for idx in range(num_cols, cur_cols):
                self.table_table.AppendCols(1)
                self.table_table.SetColLabelValue(idx, '')

    def on_title(self, evt=None):
        "opgeven titel bij klikken op kolomheader mogelijk maken"
        if not evt:
            return
        col = evt.GetCol()
        if col < 0:
            return
        with wx.TextEntryDialog(self, 'Enter a title for this column:', self.parent.title) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.table_table.SetColLabelValue(col, dlg.GetValue())
        ## dlg.Destroy()


class ScrolledTextDialog(wx.Dialog):
    """dialoog voor het tonen van de validatieoutput
    """


class CodeViewDialog(wx.Dialog):
    """dialoog voor het tonen van de broncode
    """
