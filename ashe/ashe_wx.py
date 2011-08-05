"wxPython versie van een op een treeview gebaseerde HTML-editor"

import os
import sys
import string
import wx
import wx.grid as wxgrid
import wx.html as  html
import ashe_mixin as ed
import BeautifulSoup as bs

PPATH = os.path.split(__file__)[0]
HMASK = "HTML files (*.htm,*.html)|*.htm;*.html|All files (*.*)|*.*"
IMASK = "All files|*.*"
DESKTOP = ed.DESKTOP
CMSTART = ed.CMSTART
ELSTART = ed.ELSTART
CMELSTART = ed.CMELSTART
DTDSTART = ed.DTDSTART
BL = ed.BL
TITEL = ed.TITEL

class DTDDialog(wx.Dialog):
    "dialoog om het toe te voegen dtd te selecteren"
    dtd_list = [
        ['HTML 4.1 Strict',
        """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">"""],
        ['HTML 4.1 Transitional',
        """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">"""],
        ['HTML 4.1 Frameset',
        """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
        "http://www.w3.org/TR/html4/frameset.dtd">"""],
        ['XHTML 1.0 Strict',
        """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">"""],
        ['XHTML 1.0 Transitional',
        """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">"""],
        ['XHTML 1.0 Frameset',
        """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">"""],
            ]

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
        for i, x in enumerate(self.dtd_list[:3]):
            if i == 0:
                radio = wx.RadioButton(self.pnl, -1, x[0], style = wx.RB_GROUP)
            else:
                radio = wx.RadioButton(self.pnl, -1, x[0])
            x.append(radio)
            vbox2.Add(radio, 0, wx.ALL, 2)
        hbox.Add(vbox2)
        sbox.Add(hbox, 0, wx.ALL, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        for x in self.dtd_list[3:]:
            radio = wx.RadioButton(self.pnl, -1, x[0])
            x.append(radio)
            vbox2.Add(radio, 0, wx.ALL, 2)
        hbox.Add(vbox2)
        sbox.Add(hbox, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(sbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE)
        self.SetAffirmativeId(wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
            wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)
        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

class LinkDialog(wx.Dialog):
    "dialoog om een link element toe te voegen"

    def __init__(self, parent):
        self.parent = parent
        wx.Dialog.__init__(self, parent, title = 'Add Link')
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)

        lbl = wx.StaticText(self.pnl, -1, "descriptive title:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.title_text = wx.TextCtrl(self.pnl, -1, size = (250, -1))
        gbox.Add(self.title_text, (0, 1))

        lbl = wx.StaticText(self.pnl, -1, "link to document:")
        gbox.Add(lbl, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self.pnl, -1, size = (250, -1), value = "http://")
        self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (1, 1))

        self.choose_button = wx.Button(self.pnl, -1,'Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (2, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText(self.pnl, -1, "link text:")
        gbox.Add(lbl, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.text_text = wx.TextCtrl(self.pnl, -1, size = (250, -1))
        self.text_text.Bind(wx.EVT_TEXT, self.set_text)
        gbox.Add(self.text_text, (3, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL)
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

    def kies(self, evt = None):
        "methode om het te linken document te selecteren"
        dlg = wx.FileDialog(
            self, message = "Choose a file",
            defaultDir = os.getcwd(), wildcard = HMASK, style = wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.link_text.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_ok(self, evt = None):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        link = self.link_text.GetValue()
        if link:
            if not link.startswith('http://'):
                if self.parent.xmlfn:
                    whereami = self.parent.xmlfn
                else:
                    whereami = os.path.join(os.getcwd(),'index.html')
                link = ed.getrelativepath(link, whereami)
            if not link:
                wx.MessageBox('Impossible to make this local link relative',
                    self.parent.title)
            else:
                self.link = link
                evt.Skip()
        else:
            wx.MessageBox("link opgeven of cancel kiezen s.v.p",'')

    def set_text(self, evt = None):
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
        wx.Dialog.__init__(self, parent, title = 'Add Image')
        self.parent = parent
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)

        lbl = wx.StaticText(self.pnl, -1, "descriptive title:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.title_text = wx.TextCtrl(self.pnl, -1, size = (250, -1))
        gbox.Add(self.title_text, (0, 1))

        lbl = wx.StaticText(self.pnl, -1, "link to image:")
        gbox.Add(lbl, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self.pnl, -1, size = (250, -1), value = "http://")
        self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (1, 1))

        self.choose_button = wx.Button(self.pnl, -1, 'Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (2, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText(self.pnl, -1, "alternate text:")
        gbox.Add(lbl, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.alt_text = wx.TextCtrl(self.pnl, -1, size = (250, -1))
        self.alt_text.Bind(wx.EVT_TEXT, self.set_text)
        gbox.Add(self.alt_text, (3, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL)
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

    def kies(self, evt = None):
        "methode om het te linken image te selecteren"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), wildcard=IMASK, style = wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.link_text.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_ok(self, evt = None):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        link = self.link_text.GetValue()
        if link:
            if not link.startswith('http://'):
                if self.parent.xmlfn:
                    whereami = self.parent.xmlfn
                else:
                    whereami = os.path.join(os.getcwd(),'index.html')
                link = ed.getrelativepath(link, whereami)
            if not link:
                wx.MessageBox('Impossible to make this local link relative',
                    self.parent.title)
            else:
                self.link = link
                evt.Skip()
        else:
            wx.MessageBox("image link opgeven of cancel kiezen s.v.p", self.parent.title)

    def set_text(self, evt = None):
        'indien leeg link tekst gelijk maken aan link adres'
        if evt.EventObject == self.link_text:
            linktxt = self.link_text.GetValue()
            if self.alt_text.GetValue() == self.linktxt:
                self.alt_text.SetValue(linktxt)
                self.linktxt = linktxt
        elif self.alt_text.GetValue() == "":
            self.linktxt = ""

class ListDialog(wx.Dialog):
    'dialoog om een list toe te voegen'

    def __init__(self, parent):
        self.items = []
        self.dataitems = []
        wx.Dialog.__init__(self, parent, title = 'Add List',
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER ,
            )
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        tbox = wx.FlexGridSizer(2, 2, 2, 2)
        lbl = wx.StaticText(self.pnl, -1, "choose type of list:")
        self.type_select = wx.ComboBox(self.pnl, -1, style = wx.CB_DROPDOWN, choices = [
            "unordered",
            "ordered",
            "definition",
            ])
        self.type_select.SetStringSelection("unordered")
        self.type_select.Bind(wx.EVT_COMBOBOX, self.on_type)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.type_select)

        lbl = wx.StaticText(self.pnl, -1, "initial number of items:")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.rows_text = wx.SpinCtrl(self.pnl, -1, size = (40, -1))
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_text)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.rows_text) ## hbox)
        sbox.Add(tbox, 0, wx.ALL, 5)

        tbl = wxgrid.Grid(self.pnl, -1, size = (340, 120))
        tbl.CreateGrid(0, 1)
        tbl.SetColLabelValue(0, 'list item')
        tbl.SetColSize(0, 240)
        self.list_table = tbl
        sbox.Add(self.list_table, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(sbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL)
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

    def on_type(self, evt = None):
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

    def on_text(self, evt = None):
        "controle en actie bij invullen/aanpassen aantal regels"
        try:
            cur_rows = int(self.rows_text.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer','')
            return
        num_rows = self.list_table.GetNumberRows()
        if num_rows > cur_rows:
            for idx in xrange(num_rows-1, cur_rows-1, -1):
                self.list_table.DeleteRows(idx)
        elif cur_rows > num_rows:
            for idx in xrange(num_rows, cur_rows):
                self.list_table.AppendRows(1)
                self.list_table.SetRowLabelValue(idx, '')

class TableDialog(wx.Dialog):
    "dialoog om een tabel toe te voegen"

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, title = 'Add Table',
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER ,
            )
        self.pnl = self
        self.headings = []
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        tbox = wx.FlexGridSizer(3, 2, 2, 2)

        lbl = wx.StaticText(self.pnl, -1, "summary (description):")
        tbox.Add(lbl)
        self.title_text = wx.TextCtrl(self.pnl, -1, size = (250, -1))
        tbox.Add(self.title_text)

        lbl = wx.StaticText(self.pnl, -1, "initial number of rows:")
        ## self.rows_text = wx.TextCtrl(self.pnl, -1)
        self.rows_text = wx.SpinCtrl(self.pnl, -1, size = (40, -1))
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_rows)
        self.rows_text.Bind(wx.EVT_TEXT, self.on_rows)
        tbox.Add(lbl)
        tbox.Add(self.rows_text)

        lbl = wx.StaticText(self.pnl, -1, "initial number of columns:")
        ## self.cols_text = wx.TextCtrl(self.pnl, -1)
        self.cols_text = wx.SpinCtrl(self.pnl, -1, size = (40, -1))
        self.cols_text.Bind(wx.EVT_SPINCTRL, self.on_cols)
        self.cols_text.Bind(wx.EVT_TEXT, self.on_cols)
        tbox.Add(lbl)
        tbox.Add(self.cols_text)
        sbox.Add(tbox, 0, wx.ALL, 5)

        tbl = wxgrid.Grid(self.pnl, -1, size = (340, 120))
        tbl.CreateGrid(0, 0)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_LEFT_CLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_LEFT_DCLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_DCLICK, self.on_title)
        self.table_table = tbl
        sbox.Add(self.table_table, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(sbox, 1, wx.EXPAND | wx.ALL, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
            wx.ALIGN_CENTER_HORIZONTAL, 20)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.title_text.SetFocus()

    def on_rows(self, evt = None):
        "controle en actie bij opgeven aantal regels"
        try:
            cur_rows = int(self.rows_text.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer', '')
            return
        num_rows = self.table_table.GetNumberRows()
        if num_rows > cur_rows:
            for idx in xrange(num_rows-1, cur_rows-1, -1):
                ## prinum_rows idx
                self.table_table.DeleteRows(idx)
        elif cur_rows > num_rows:
            for idx in xrange(num_rows, cur_rows):
                self.table_table.AppendRows(1)
                self.table_table.SetRowLabelValue(idx, '')

    def on_cols(self, evt = None):
        "controle en actie bij opgeven aantal kolommen"
        try:
            cur_cols = int(self.cols_text.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer', '')
            return
        num_cols = self.table_table.GetNumberCols()
        if num_cols > cur_cols:
            for idx in xrange(num_cols-1, cur_cols-1, -1):
                ## prinum_cols idx
                self.table_table.DeleteCols(idx)
        elif cur_cols > num_cols:
            for idx in xrange(num_cols, cur_cols):
                self.table_table.AppendCols(1)
                self.table_table.SetColLabelValue(idx,'')

    def on_title(self, evt = None):
        "opgeven titel bij klikken op kolomheader mogelijk maken"
        if evt:
            col = evt.GetCol()
            if col < 0:
                return
            dlg = wx.TextEntryDialog(
                self, 'Enter a title for this column:',
                '')
            if dlg.ShowModal() == wx.ID_OK:
                self.table_table.SetColLabelValue(col, dlg.GetValue())
            dlg.Destroy()

class ElementDialog(wx.Dialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, parent, title = '', tag = None, attrs = None):
        wx.Dialog.__init__(self, parent, -1, title = title,
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            )
        self.pnl = self
        self.parent = parent
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self.pnl, -1, "element name:")
        self.tag_text = wx.TextCtrl(self.pnl, -1)
        self.comment_button = wx.CheckBox(self.pnl, label = '&Comment(ed)')
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
        tbl.SetColSize(1, 160)
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
        self.add_button = wx.Button(self.pnl, label = '&Add Attribute')
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_button = wx.Button(self.pnl, label = '&Delete Selected')
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_del)
        hbox.Add(self.add_button, 0, wx.EXPAND | wx.ALL, 1)
        hbox.Add(self.delete_button, 0, wx.EXPAND | wx.ALL, 1)
        sbox.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        vbox.Add(sbox, 1, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL)
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
        self.tag_text.SetFocus()
        ## self.Show(True)

    def on_add(self, evt = None):
        "attribuut toevoegen"
        self.attr_table.AppendRows(1)
        idx = self.attr_table.GetNumberRows() - 1
        self.attr_table.SetRowLabelValue(idx, '')

    def on_del(self, evt = None):
        "attribuut verwijderen"
        rows = self.attr_table.GetSelectedRows()
        if rows:
            rows.reverse()
            for row in rows:
                self.attr_table.DeleteRows(row, 1)
        else:
            wx.MessageBox("Select a row by clicking on the row heading",
                'Selection is empty', wx.ICON_INFORMATION)

    def on_ok(self, evt = None):
        "controle bij OK aanklikken"
        tag = self.tag_text.GetValue()
        okay = True
        test = string.ascii_letters + string.digits
        for letter in tag:
            if letter not in test:
                okay = False
                wx.MessageBox('Illegal character(s) in tag name',
                    self.parent.title, wx.ICON_ERROR)
                break
        if okay:
            evt.Skip()

class TextDialog(wx.Dialog):
    """dialoog om een tekst element op te voeren of aan te passen
    biedt tevens de mogelijkheid de tekst "op commentaar" te zetten"""

    def __init__(self, parent, title = '', text = None):
        iscomment = False
        if text is None:
            text = ''
        else:
            if text.startswith(CMSTART):
                iscomment = True
                dummy, text = text.split(None, 1)
        wx.Dialog.__init__(self, parent, -1, title,
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER ,
            )
        self.pnl = self
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.comment_button = wx.CheckBox(self.pnl, label = '&Comment(ed)')
        self.comment_button.SetValue(iscomment)
        hbox.Add(self.comment_button, 0, wx.EXPAND | wx.ALL, 1)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.data_text = wx.TextCtrl(self.pnl, -1, size=(340, 175), style = wx.TE_MULTILINE)
        self.data_text.SetValue(text)
        hbox.Add(self.data_text, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL)
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

class MainFrame(wx.Frame, ed.EditorMixin):
    "Main GUI"

    def __init__(self, parent, _id, fname = ''):
        self.parent = parent
        self.title = "(untitled) - Albert's Simple HTML Editor"
        self.xmlfn = fname
        ## if fn:
            ## self.xmlfn = os.path.abspath(fn)
        ## else:
            ## self.xmlfn = ''
        dsp = wx.Display().GetClientArea()
        high = dsp.height if dsp.height < 900 else 900
        wide = dsp.width if dsp.width < 1020 else 1020
        wx.Frame.__init__(self, parent, _id,
            pos = (dsp.top, dsp.left),
            size = (wide, high)
            )
        self.SetIcon(wx.Icon(os.path.join(PPATH,"ashe.ico"), wx.BITMAP_TYPE_ICO))

        self.setup_menu()

        self.pnl = wx.SplitterWindow(self, -1, style=wx.NO_3D)
        self.pnl.SetMinimumPaneSize (1)

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

        self.html = html.HtmlWindow(self.pnl, -1,
            ## size = (wide, high - 30)
            )
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

        ed.EditorMixin.getsoup(self, fname)
        self.refresh_preview()

    def setup_menu(self):
        self.menulist = (
            '&File', (
                ('&New', 'N', 'C', "Start a new HTML document", self.newxml),
                ('&Open', 'O', 'C', "Open an existing HTML document", self.openxml),
                ('&Save', 'S', 'C', "Save the current document", self.savexml),
                ('Save &As', 'S', 'SC', "Save the current document under a different name",
                    self.savexmlas),
                ('&Revert', 'R', 'C', "Discard all changes since the last save", self.reopenxml),
                ('sep1', ),
                ('E&xit', 'Q', 'C', 'Quit the application', self.quit),
                ),
                ), (
            '&View', (
                ('Expand All (sub)Levels', '+', 'C', "Show what's beneath the current element",
                    self.expand, True),
                ('Collapse All (sub)Levels', '-', 'C', "Hide what's beneath the current element",
                    self.collapse, True),
                ),
                ), (
            '&Edit', (
                ('Edit', 'F2', '', 'Modify the element/text and/or its attributes', self.edit),
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
                ('Add DTD', '', '', 'Add a document type description', self.add_dtd),
                ('Create link (under)', '', '', 'Add a link', self.add_link),
                ('Add image (under)', '', '', 'Include an image', self.add_image),
                ('Add list (under)', '', '', 'Create a list', self.add_list),
                ('Add table (under)', '', '', 'Create a table', self.add_table),
                ),
                )
        self.menu_id = {}
        menu_bar = wx.MenuBar()
        for menu_text, data in self.menulist:
            menu = wx.Menu()
            for item in data:
                if len(item) > 1:
                    menuitem_text, hotkey, modifiers, status_text, callback = item[:5]
                    if 'A' in modifiers:
                        hotkey = "-".join(("Alt",hotkey))
                    if 'C' in modifiers:
                        hotkey = "-".join(("Ctrl",hotkey))
                    if 'S' in modifiers:
                        hotkey = "-".join(("Shift",hotkey))
                    self.menu_id[menuitem_text] = wx.NewId()
                    caption = menuitem_text.ljust(40) + hotkey
                    menu.Append(self.menu_id[menuitem_text], caption, status_text)
                    self.Connect(self.menu_id[menuitem_text], -1, wx.wxEVT_COMMAND_MENU_SELECTED,
                        callback)
                else:
                    menu.AppendSeparator()
            menu_bar.Append(menu, menu_text)
        self.SetMenuBar(menu_bar)

    def check_tree(self):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)"""
        if self.tree_dirty:
            hlp = wx.MessageBox("HTML data has been modified - save before continuing?",
                self.title,
                style = wx.YES_NO | wx.CANCEL)
            if hlp == wx.ID_YES:
                self.savexml()
            return hlp

    def quit(self, evt = None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna afsluiten"""
        if self.check_tree() != wx.CANCEL:
            self.Close()

    def newxml(self, evt = None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna nieuwe html aanmaken"""
        if self.check_tree() != wx.CANCEL:
            try:
                ed.EditorMixin.getsoup(self, fname = None)
                self.sb.SetStatusText("started new document")
                self.refresh_preview()
            except Exception as err:
                dlg = wx.MessageBox(self.title, err, wx.OK | wx.INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()

    def openxml(self, evt = None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna een html bestand kiezen"""
        if self.check_tree() != wx.CANCEL:
            loc = os.path.dirname(self.xmlfn) if self.xmlfn else os.getcwd()
            dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir = loc,
                wildcard = HMASK,
                style = wx.OPEN
                )
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    ed.EditorMixin.getsoup(self, fname = dlg.GetPath())
                    self.sb.SetStatusText("loaded {}".format(self.xmlfn))
                    self.refresh_preview()
                except Exception as err:
                    dlg.Destroy()
                    dlg = wx.MessageBox(str(err), self.title, wx.OK) # | wx.INFORMATION)
                    dlg.ShowModal()
                    dlg.Destroy()

    def savexml(self, evt = None):
        "save html to file"
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.data2soup()
            try:
                self.soup2file()
            except IOError as err:
                dlg = wx.MessageBox(self.title, err, wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                return
            self.sb.SetStatusText("saved {}".format(self.xmlfn))

    def savexmlas(self, evt = None):
        """vraag bestand om html op te slaan
        bestand opslaan en naam in titel en root element zetten"""
        if self.xmlfn:
            dname, fname = os.path.split(self.xmlfn)
        else:
            dname = os.getcwd()
            fname = ""
        dlg = wx.FileDialog(
            self, message = "Save file as ...",
            defaultDir = dname,
            defaultFile = fname,
            wildcard = HMASK,
            style = wx.SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.xmlfn = dlg.GetPath()
            self.data2soup()
            try:
                self.soup2file(saveas = True)
            except IOError as err:
                dlg.Destroy()
                dlg = wx.MessageBox(self.title, err, wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                return
            self.tree.SetItemText(self.top, self.xmlfn)
            self.SetTitle(" - ".join((os.path.basename(self.xmlfn), TITEL)))
            self.sb.SetStatusText("saved as {}".format(self.xmlfn))
        dlg.Destroy()

    def reopenxml(self, evt = None):
        """onvoorwaardelijk html bestand opnieuw laden"""
        try:
            ed.EditorMixin.getsoup(self, fname = self.xmlfn)
            self.sb.SetStatusText("reloaded {}".format(self.xmlfn))
            self.refresh_preview()
        except Exception as err:
            dlg = wx.MessageBox(self.title, err, wx.OK | wx.INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def refresh_preview(self):
        self.data2soup()
        self.data_file = "tempfile.html"
        with open(self.data_file,"w") as f_out:
            f_out.write(str(self.soup).replace('%SOUP-ENCODING%','utf-8'))
        self.html.LoadPage(self.data_file)
        self.tree.SetFocus()

    def about(self, evt = None):
        "toon programma info"
        abouttext = ed.EditorMixin.about(self)
        wx.MessageBox(abouttext, self.title, wx.OK | wx.ICON_INFORMATION)

    def addtreeitem(self, node, naam, data):
        """itemnaam en -data toevoegen aan de interne tree
        referentie naar treeitem teruggeven"""
        newnode = self.tree.AppendItem(node, naam)
        self.tree.SetPyData(newnode, data)
        return newnode

    def addtreetop(self, fname, titel):
        """titel en root item in tree instellen"""
        self.SetTitle(titel)
        self.top = self.tree.AddRoot(fname)

    def init_tree(self, name = ''):
        "nieuwe tree initialiseren"
        self.tree.DeleteAllItems()
        ed.EditorMixin.init_tree(self, name)
        if DESKTOP:
            self.tree.SelectItem(self.top)

    def data2soup(self):
        "interne tree omzetten in BeautifulSoup object"
        def expandnode(node, root, data, commented = False):
            "tree item (node) met inhoud (data) toevoegen aan BS node (root)"
            try:
                for att in data:
                    root[att] = data[att]
            except TypeError:
                pass
            elm, pos = self.tree.GetFirstChild(node)
            while elm.IsOk():
                text = self.tree.GetItemText(elm)
                data = self.tree.GetItemPyData(elm)
                if text.startswith(ELSTART) or text.startswith(CMELSTART):
                    if text.startswith(CMSTART):
                        text = text.split(None, 1)[1]
                        if not commented:
                            is_comment = True
                            soup = bs.BeautifulSoup()
                            sub = bs.Tag(soup, text.split()[1])
                            expandnode(elm, sub, data, is_comment)
                            sub = bs.Comment(str(sub).decode("latin-1"))
                        else:
                            is_comment = False
                            sub = bs.Tag(self.soup, text.split()[1])
                    else:
                        is_comment = False
                        sub = bs.Tag(self.soup, text.split()[1])
                    root.append(sub) # insert(0,sub)
                    if not is_comment:
                        expandnode(elm, sub, data, commented)
                else:
                    # dit levert fouten op bij het gebruiken van diacrieten
                    ## sub = bs.NavigableString(.ed.escape(data))
                    ## root.append(sub) # insert(0,sub)
                    # dit niet maar er wordt niet correct gecodeerd
                    ## root.append(ed.escape(data))
                    # misschien dat dit het doet
                    sub = bs.NavigableString(data.decode("latin-1"))
                    if text.startswith(CMSTART) and not commented:
                        sub = bs.Comment(data.decode("latin-1"))
                    root.append(sub) # data.decode("latin-1")) # insert(0,sub)
                elm, pos = self.tree.GetNextChild(node, pos)
        print self.root.originalEncoding
        self.soup = bs.BeautifulSoup(fromEncoding="") # self.root.originalEncoding)
        tag, pos = self.tree.GetFirstChild(self.top)
        while tag.IsOk():
            text = self.tree.GetItemText(tag)
            data = self.tree.GetItemPyData(tag)
            if text.startswith(ELSTART):
                ## sub = bs.Declaration(data)
            ## else:
                root = bs.Tag(self.soup, text.split(None, 2)[1])
                self.soup.insert(0, root)
                expandnode(tag, root, data)
            tag, pos = self.tree.GetNextChild(self.top, pos)

    def on_leftdclick(self, evt = None):
        "start edit bij dubbelklikken tenzij op filenaam"
        item, flags = self.tree.HitTest(evt.GetPosition())
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

    def on_rightdown(self, evt = None):
        "context menu bij rechtsklikken"
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and item != self.top: # != self.top:
            self.contextmenu(item)

    def contextmenu(self, item, pos = None):
        'we should be getting a menu now'
        self.tree.SelectItem(item)
        data = self.tree.GetItemText(item)
        menu = wx.Menu()
        for menu_item in self.menulist[1][1]:
            menu.Append(self.menu_id[menu_item[0]], menu_item[0])
        for menu_text, data in self.menulist[2:4]:
            submenu = wx.Menu()
            for item in data:
                if len(item) == 1:
                    submenu.AppendSeparator()
                elif len(item) < 6 or data.startswith(ELSTART):
                    submenu.Append(self.menu_id[item[0]], item[0])
            menu.AppendMenu(-1, menu_text, submenu)
        if pos:
            self.PopupMenu(menu, pos = pos)
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
            'SA': wx.MOD_SHIFT | wx.MOD_ALT,}
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
                self.contextmenu(item, pos = pos)
                return
        for menu, data in self.menulist:
            for submenu in data:
                if len(submenu) < 2 or submenu[1] == '':
                    continue
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
                else:
                    go_on = False
                if go_on and mods != mods_ok[submenu[2]]:
                    go_on = False
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

    def expand(self, evt = None):
        "expandeer tree vanaf huidige item"
        item = self.tree.Selection
        if item:
            self.tree.ExpandAllChildren(item)

    def collapse(self, evt = None):
        "collapse huidige item en daaronder"
        item = self.tree.Selection
        if item:
            self.tree.CollapseAllChildren(item)

    def edit(self, evt = None):
        "start edit m.b.v. dialoog"
        def comment_out(node, commented):
            "subitem(s) (ook) op commentaar zetten"
            subnode, pos = self.tree.GetFirstChild(node)
            while subnode.IsOk():
                txt = self.tree.GetItemText(subnode)
                if commented:
                    if not txt.startswith(CMSTART):
                        self.tree.SetItemText(subnode, " ".join((CMSTART, txt)))
                else:
                    if txt.startswith(CMSTART):
                        self.tree.SetItemText(subnode, txt.split(None, 1)[1])
                comment_out(subnode, commented)
                subnode, pos = self.tree.GetNextChild(node, pos)
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemText(self.item)
        if data.startswith(ELSTART) or data.startswith(CMELSTART):
            attrdict = self.tree.GetItemData(self.item).GetData()
            was_commented = data.startswith(CMSTART)
            edt = ElementDialog(self, title = 'Edit an element', tag = data,
                attrs = attrdict)
            if edt.ShowModal() == wx.ID_SAVE:
                tag = edt.tag_text.GetValue()
                commented = edt.comment_button.GetValue()
                attrs = {}
                for i in range(edt.attr_table.GetNumberRows()):
                    attrs[edt.attr_table.GetCellValue(i, 0)] = edt.attr_table.GetCellValue(i, 1)
                if tag != data or attrs != attrdict:
                    self.tree.SetItemText(self.item, ed.getelname(tag, attrs,
                        commented))
                self.tree.SetPyData(self.item, attrs)
                if commented != was_commented:
                    comment_out(self.item, commented)
        else:
            txt = CMSTART + " " if data.startswith(CMSTART) else ""
            data = self.tree.GetItemData(self.item).GetData()
            edt = TextDialog(self, title='Edit Text', text = txt + data)
            if edt.ShowModal() == wx.ID_SAVE:
                txt = edt.data_text.GetValue()
                self.tree.SetItemText(self.item, ed.getshortname(txt,
                    edt.comment_button.GetValue()))
                self.tree.SetPyData(self.item, txt)
        self.tree_dirty = True
        self.refresh_preview()
        edt.Destroy()

    def copy(self, evt = None, cut = False, retain = True):
        "start copy/cut/delete actie"
        def push_el(elm, result):
            "subitem(s) toevoegen aan copy buffer"
            text = self.tree.GetItemText(elm)
            data = self.tree.GetItemPyData(elm)
            atrlist = []
            if text.startswith(ELSTART):
                node, pos = self.tree.GetFirstChild(elm)
                while node.IsOk():
                    x = push_el(node, atrlist)
                    node, pos = self.tree.GetNextChild(elm, pos)
            result.append((text, data, atrlist))
            return result
        if DESKTOP and not self.checkselection():
            return
        text = self.tree.GetItemText(self.item)
        data = self.tree.GetItemPyData(self.item)
        txt = 'cut' if cut else 'copy'
        if data == self.root:
            wx.MessageBox("Can't %s the root" % txt, self.title)
            return
        if retain:
            if text.startswith(ELSTART):
                self.cut_el = []
                self.cut_el = push_el(self.item, self.cut_el)
                self.cut_txt = None
            else:
                if data.startswith(DTDSTART):
                    if cut:
                        wx.MessageBox(
                            'The DTD cannot be *paste*d, only *add*ed from the menu',
                            'Warning',
                            wx.ICON_INFORMATION
                            )
                    else:
                        wx.MessageBox(
                            "You can't *copy* the DTD, only *cut* it",
                            'Error',
                            wx.ICON_ERROR
                            )
                        return
                self.cut_el = None
                self.cut_txt = data
        if cut:
            self.tree.Delete(self.item)
            self.tree_dirty = True
            self.refresh_preview()
            try:
                if self.cut_txt.startswith(DTDSTART):
                    self.has_dtd = False
            except AttributeError:
                pass

    def paste(self, evt = None, before = True, below = False):
        "start paste actie"
        def zetzeronder(node, elm, pos = -1):
            "paste copy buffer into tree"
            if pos == -1:
                subnode = self.tree.AppendItem(node, elm[0])
                self.tree.SetPyData(subnode, elm[1])
            else:
                subnode = self.tree.InsertItemBefore(node, pos, elm[0])
                self.tree.SetPyData(subnode, elm[1])
            for item in elm[2]:
                zetzeronder(subnode, item)
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemPyData(self.item)
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
                self.tree.SetPyData(node, data)
            else:
                add_to = self.tree.GetItemParent(self.item)
                added = False
                chld, pos = self.tree.GetFirstChild(add_to)
                for idx in range(self.tree.GetChildrenCount(add_to)):
                    if chld == self.item:
                        if not before:
                            idx += 1
                        node = self.tree.InsertItemBefore(add_to, idx, item)
                        self.tree.SetPyData(node, data)
                        added = True
                        break
                    chld, pos = self.tree.GetNextChild(add_to, pos)
                if not added:
                    node = self.tree.AppendItem(add_to, item)
                    self.tree.SetPyData(node, data)
        else:
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
            zetzeronder(node, self.cut_el[0], idx)
        self.tree_dirty = True
        self.refresh_preview()

    def add_text(self, evt = None, before = True, below = False):
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
            self.tree.SetPyData(new_item, txt)
            self.tree_dirty = True
            self.refresh_preview()
            self.tree.Expand(self.item)
        edt.Destroy()

    def insert(self, evt = None, before = True, below = False):
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
                self.tree.SetPyData(item, data)
                self.tree.Expand(self.item)
            else:
                parent = self.tree.GetItemParent(self.item)
                text = self.tree.GetItemText(parent)
                under_comment = text.startswith(CMSTART)
                text = ed.getelname(tag, data, commented or under_comment)
                item = self.item if not before else self.tree.GetPrevSibling(self.item)
                node = self.tree.InsertItem(parent, item, text)
                self.tree.SetPyData(node, data)
            self.tree_dirty = True
            self.refresh_preview()
        edt.Destroy()

    def add_dtd(self, evt = None):
        "start toevoegen dtd m.b.v. dialoog"
        edt = DTDDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            for cap, dtd, radio in edt.dtd_list:
                if radio.GetValue():
                    node = self.tree.InsertItemBefore(self.top, 0, ed.getshortname(dtd))
                    self.tree.SetPyData(node, dtd)
                    self.has_dtd = True
                    self.tree_dirty = True
                    self.refresh_preview()
                    break
        edt.Destroy()

    def add_link(self, evt = None):
        "start toevoegen link m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't do this below text", self.title)
            return
        edt = LinkDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            data = {
                "href": edt.link,
                "title": edt.title_text.GetValue()
                }
            node = self.tree.AppendItem(self.item, ed.getelname('a', data))
            self.tree.SetPyData(node, data)
            txt = edt.text_text.GetValue()
            new_item = self.tree.AppendItem(node, ed.getshortname(txt))
            self.tree.SetPyData(new_item, txt)
            self.tree_dirty = True
            self.refresh_preview()
        edt.Destroy()

    def add_image(self, evt = None):
        "start toevoegen image m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't do this below text", self.title)
            return
        edt = ImageDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            data = {
                "src": edt.link,
                "alt": edt.alt_text.GetValue(),
                "title": edt.title_text.GetValue()
                }
            node = self.tree.AppendItem(self.item, ed.getelname('img', data))
            self.tree.SetPyData(node, data)
            self.tree_dirty = True
            self.refresh_preview()
        edt.Destroy()

    def add_list(self, evt = None):
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
                self.tree.SetPyData(node, data)
                if type == "dl":
                    new_item = self.tree.AppendItem(new_subitem, ed.getelname('dd'))
                    data = edt.list_table.GetCellValue(row, 1)
                    node = self.tree.AppendItem(new_item, ed.getshortname(data))
                    self.tree.SetPyData(node, data)

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
            self.tree_dirty = True
            self.refresh_preview()
        edt.Destroy()

    def add_table(self, evt = None):
        "start toevoegen tabel m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't do this below text", self.title)
            return
        edt = TableDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            cols = edt.table_table.GetNumberCols() #int(edt.cols_text.GetValue())
            rows = edt.table_table.GetNumberRows() #int(edt.rows_text.GetValue())
            data = {"summary": edt.title_text.GetValue()}
            new_item = self.tree.AppendItem(self.item, ed.getelname('table', data))
            self.tree.SetPyData(new_item, data)
            new_row = self.tree.AppendItem(new_item, ed.getelname('tr'))
            for col in range(cols):
                new_head = self.tree.AppendItem(new_row, ed.getelname('th'))
                # try:
                head = edt.table_table.GetColLabelValue(col) # edt.headings[col]
                # except IndexError:
                if not head:
                    node = self.tree.AppendItem(new_head, ed.getshortname(BL))
                    self.tree.SetPyData(node, BL)
                else:
                    node = self.tree.AppendItem(new_head, ed.getshortname(head))
                    self.tree.SetPyData(node, head)
            for row in range(rows):
                new_row = self.tree.AppendItem(new_item, ed.getelname('tr'))
                for col in range(cols):
                    new_cell = self.tree.AppendItem(new_row, ed.getelname('td'))
                    text = edt.table_table.GetCellValue(row, col)
                    node = self.tree.AppendItem(new_cell, ed.getshortname(text))
                    self.tree.SetPyData(node, text)
            self.tree_dirty = True
            self.refresh_preview()
        edt.Destroy()

def main_gui(args):
    "start main GUI"
    fname = ''
    if len(args) > 1:
        fname = args[1]
        ## if len(args) > 2:
            ## print args[2]
        if not os.path.exists(fname):
            ## fname = os.path.join(args[2], args[1])
            print('Kan file niet openen, geef s.v.p. een absoluut pad op\n')
    app = wx.App(redirect = True, filename = "ashe.log")
    print "\n-- new entry --\n"
    if fname:
        frm = MainFrame(None, -1, fname = fname)
    else:
        frm = MainFrame(None, -1)
    app.MainLoop()

if __name__ == "__main__":
    main_gui(sys.argv)
