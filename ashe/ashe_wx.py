"wxPython versie van een op een treeview gebaseerde HTML-editor"

import os
import sys
import shutil
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

class PreviewDialog(wx.Dialog):
    "dialoog waarin de gerenderde html getoond wordt"

    def __init__(self, parent):
        "html aanmaken/opslaan in een tijdelijk html file en dit renderen"
        self.parent = parent
        dsp = wx.Display().GetClientArea()
        high = dsp.height if dsp.height < 800 else 800
        wide = dsp.width if dsp.width < 1024 else 1024
        ## print "preview: ", dsp.top, dsp.left, wi, hi
        wx.Dialog.__init__(self, parent, title = 'Preview HTML',
            pos = (dsp.top, dsp.left), size=(wide, high),
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER ,
            ) #,action=("Cancel", self.on_cancel))
        self.pnl = self # wx.Panel(self, -1)

        self.parent.maakhtml()
        self.data_file = "tempfile.html"
        with open(self.data_file,"w") as f_out:
            f_out.write(str(self.parent.soup))


        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15, 15, 15, 15))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.html = html.HtmlWindow(self.pnl, -1, # size = (600, 680)
            size = (wide, high - 30)
            ) #, zoom_level = 0)
        if "gtk2" in wx.PlatformInfo:
            self.html.SetStandardFonts()

        self.html.LoadPage(self.data_file)
        ## x, y = self.html.GetPosition()
        ## w, h = self.html.GetSize()
        ## wm, hm = self.html.GetMaxSize()
        ## print "size:", x, y, w, h, wm, hm
        hbox.Add(self.html, 1) #, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 1)

        ## hbox = wx.BoxSizer(wx.HORIZONTAL)
        ## self.ok_button = wx.Button(self.pnl, id = wx.ID_OK)
        ## hbox.Add(self.ok_button, 0, wx.ALL, 2)
        ## vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

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
        self.pnl = self # wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL) # ,border=(15, 15, 15, 15))

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self.pnl, -1, "Select document type:")
        hbox.Add(lbl, 0, wx.TOP, 10)
        sbox.Add(hbox, 0) # , wx.LEFT|wx.RIGHT, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        for i, x in enumerate(self.dtd_list[:3]):
            if i == 0:
                radio = wx.RadioButton(self.pnl, -1, x[0], style = wx.RB_GROUP)
            else:
                radio = wx.RadioButton(self.pnl, -1, x[0])
            x.append(radio)
            vbox2.Add(radio, 0, wx.ALL, 2)
        hbox.Add(vbox2) # , 0, wx.TOP, 15)
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
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE) # label='Save')
        self.SetAffirmativeId(wx.ID_SAVE)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL) #label='Cancel')
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
        self.pnl = self # wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15, 15, 15, 15))

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
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE) # label='Save')
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL) #label='Cancel')
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
            print "link adres:", link
            if not link.startswith('http://'):
                if self.parent.xmlfn:
                    whereami = self.parent.xmlfn
                else:
                    whereami = os.path.join(os.getcwd(),'index.html')
                print "whereamI:", whereami
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
        self.pnl = self # wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15, 15, 15, 15))

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
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE) # label='Save')
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL) #label='Cancel')
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
            ) #,action=("Cancel", self.on_cancel))
        self.pnl = self # wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15, 15, 15, 15))

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        ## tsizer = wx.TBox(2, 2,border=(2, 2, 20, 2),spacing_x=2,spacing_y=2)
        tbox = wx.FlexGridSizer(2, 2, 2, 2)  # rows, cols, vgap, hgap
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
        #~ self.rows_text = wx.TextCtrl(self.pnl, -1,size=(20, -1))
        self.rows_text = wx.SpinCtrl(self.pnl, -1, size = (40, -1))
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_text)
        #~ self.rows_text.Bind(wx.EVT_TEXT, self.on_text)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.rows_text) ## hbox)
        sbox.Add(tbox, 0, wx.ALL, 5)

        #~ hbox = wx.BoxSizer(wx.HORIZONTAL)
        tbl = wxgrid.Grid(self.pnl, -1, size = (340, 120))
        tbl.CreateGrid(0, 1)
        tbl.SetColLabelValue(0, 'list item')
        tbl.SetColSize(0, 240)
        self.list_table = tbl
        sbox.Add(self.list_table, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(sbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE) # label='Save')
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL) #label='Cancel')
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
                ## print idx
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
            ) #,action=("Cancel", self.on_cancel))
        self.pnl = self # wx.Panel(self, -1)
        self.headings = []
        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15, 15, 15, 15))

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        ## tbox = wx.TBox(2, 2,border=(2, 2, 20, 2),spacing_x=2,spacing_y=2)
        tbox = wx.FlexGridSizer(3, 2, 2, 2)  # rows, cols, vgap, hgap

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
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE) # label='Save')
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL) #label='Cancel')
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
        ## print "Elementdialog:", tag, attrs
        wx.Dialog.__init__(self, parent, -1, title = title,
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            ) # action=("Cancel", self.on_cancel))
        self.pnl = self # wx.Panel(self, -1)
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
        ## tbl.bind(selchanged=self.on_sel)
        self.attr_table = tbl
        hbox.Add(self.attr_table, 1, wx.EXPAND)
        sbox.Add(hbox, 1, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self.pnl, label = '&Add Attribute')
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_button = wx.Button(self.pnl, label = '&Delete Selected')
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_del)
        ## self.comment_button.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_comment)
        hbox.Add(self.add_button, 0, wx.EXPAND | wx.ALL, 1)
        hbox.Add(self.delete_button, 0, wx.EXPAND | wx.ALL, 1)
        sbox.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1) # , wx.EXPAND|wx.ALL,5)
        vbox.Add(sbox, 1, wx.ALL | wx.EXPAND, 5) # , wx.LEFT | wx.RIGHT , 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE) # label='Save')
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL) #label='Cancel')
        ## self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
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
            ) #,action=("Cancel", self.on_cancel))
        self.pnl = self # wx.Panel(self, -1)
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
        self.ok_button = wx.Button(self.pnl, id = wx.ID_SAVE) # label='Save')
        self.cancel_button = wx.Button(self.pnl, id = wx.ID_CANCEL) #label='Cancel')
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
        wide = dsp.width if dsp.width < 620 else 620
        ## print "main: ", dsp.top, dsp.left, wi, hi
        wx.Frame.__init__(self, parent, _id,
            pos = (dsp.top, dsp.left),
            size = (wide, high)
            )
        self.SetIcon(wx.Icon(os.path.join(PPATH,"ashe.ico"), wx.BITMAP_TYPE_ICO))

        menu_bar = wx.MenuBar()

        self.filemenu = wx.Menu()
        self.FM_NEW = wx.NewId()
        self.FM_OPN = wx.NewId()
        self.FM_SAV = wx.NewId()
        self.FM_SAS = wx.NewId()
        self.FM_ROP = wx.NewId()
        self.FM_PVW = wx.NewId()
        self.FM_XIT = wx.NewId()

        self.filemenu.Append(self.FM_NEW, "&New      Ctrl-N")
        self.filemenu.Append(self.FM_OPN, "&Open     Ctrl-O")
        self.filemenu.Append(self.FM_SAV, '&Save     Ctrl-S')
        self.filemenu.Append(self.FM_SAS, 'Save &As  Shift-Ctrl-S')
        self.filemenu.Append(self.FM_ROP, '&Revert   Ctrl-R')
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.FM_PVW, 'Pre&view')
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.FM_XIT, 'E&xit     Ctrl-Q, Alt-F4')
        menu_bar.Append(self.filemenu, "&File")

        self.viewmenu = wx.Menu()
        self.VW_EXP = wx.NewId()
        self.VW_CLP = wx.NewId()
        self.viewmenu.Append(self.VW_EXP, "Expand All (sub)Levels    Ctrl +")
        self.viewmenu.Append(self.VW_CLP, "Collapse All (sub)Levels  Ctrl -")
        menu_bar.Append(self.viewmenu, "&View")

        self.editmenu = wx.Menu()
        self.EM_EDT = wx.NewId()
        self.EM_CUT = wx.NewId()
        self.EM_CPY = wx.NewId()
        self.EM_PB = wx.NewId()
        self.EM_PA = wx.NewId()
        self.EM_PU = wx.NewId()
        self.EM_IT = wx.NewId()
        self.EM_IB = wx.NewId()
        self.EM_IA = wx.NewId()
        self.EM_IU = wx.NewId()
        self.EM_DEL = wx.NewId()
        self.editmenu.Append(self.EM_EDT,
            "Edit                    F2")
        self.editmenu.AppendSeparator()
        self.editmenu.Append(self.EM_CUT,
            "Cut                     Ctrl-X")
        self.editmenu.Append(self.EM_CPY,
            "Copy                    Ctrl-C")
        self.pastebeforeitem = self.editmenu.Append(self.EM_PB,
            "Paste Before            Shft-Ctrl-V")
        self.pasteafteritem = self.editmenu.Append(self.EM_PA,
            "Paste After             Alt-Ctrl-V")
        self.pastebelowitem = self.editmenu.Append(self.EM_PU,
            "Paste Under             Ctrl-V")
        self.editmenu.AppendSeparator()
        self.editmenu.Append(self.EM_DEL,
            "Delete                  Del")
        self.editmenu.Append(self.EM_IT,
            "Insert Text (under)     Ctrl-Ins")
        self.editmenu.Append(self.EM_IB,
            'Insert Element Before   Shft-Ins')
        self.editmenu.Append(self.EM_IA,
            'Insert Element After    Alt-Ins')
        self.editmenu.Append(self.EM_IU,
            'Insert Element Under    Ins')
        ## self.pastebeforeitem.title = "Nothing to Paste"
        ## self.pastebeforeitem.enable(False)
        ## self.pasteafteritem.title = " "
        ## self.pasteafteritem.enable(False)
        ## self.pastebelowitem.title = " "
        ## self.pastebelowitem.enable(False)
        menu_bar.Append(self.editmenu, "&Edit")

        # self.helpmenu.append('About', callback = self.about)
        self.htmlmenu = wx.Menu()
        self.HM_DTD = wx.NewId()
        self.HM_LNK = wx.NewId()
        self.HM_IMG = wx.NewId()
        self.HM_LST = wx.NewId()
        self.HM_TBL = wx.NewId()
        self.dtdmenu = self.htmlmenu.Append(self.HM_DTD, "Add DTD")
        self.htmlmenu.Append(self.HM_LNK, "Create link (under)")
        self.htmlmenu.Append(self.HM_IMG, "Add image (under)")
        self.htmlmenu.Append(self.HM_LST, "Add list (under)")
        self.htmlmenu.Append(self.HM_TBL, "Add table (under)")
        menu_bar.Append(self.htmlmenu, "&HTML")
        self.SetMenuBar(menu_bar)

        self.Connect(self.FM_NEW, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.newxml)
        self.Connect(self.FM_OPN, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.openxml)
        self.Connect(self.FM_SAV, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.savexml)
        self.Connect(self.FM_SAS, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.savexmlas)
        self.Connect(self.FM_ROP, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.reopenxml)
        self.Connect(self.FM_PVW, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.preview)
        self.Connect(self.FM_XIT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.quit)
        self.Connect(self.VW_EXP, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.expand   )
        self.Connect(self.VW_CLP, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.collapse )
        self.Connect(self.EM_EDT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.edit     )
        self.Connect(self.EM_CUT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.cut      )
        self.Connect(self.EM_CPY, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.copy     )
        self.Connect(self.EM_DEL, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.delete   )
        self.Connect(self.EM_PB , -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.paste    )
        self.Connect(self.EM_PA , -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.paste_aft)
        self.Connect(self.EM_PU , -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.paste_blw)
        self.Connect(self.EM_IT , -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.add_text )
        self.Connect(self.EM_IB , -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.insert   )
        self.Connect(self.EM_IA , -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.ins_aft  )
        self.Connect(self.EM_IU , -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.ins_chld )
        self.Connect(self.HM_DTD, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.add_dtd  )
        self.Connect(self.HM_LNK, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.add_link )
        self.Connect(self.HM_IMG, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.add_image)
        self.Connect(self.HM_LST, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.add_list )
        self.Connect(self.HM_TBL, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.add_table)

        self.pnl = wx.Panel(self, -1)

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
        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

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

        ed.EditorMixin.init_fn(self)

    def check_tree(self):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)"""
        ## print "check_tree aangeroepen"
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
            ed.EditorMixin.newxml(self)

    def openxml(self, evt = None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna een html bestand kiezen"""
        if self.check_tree() != wx.CANCEL:
            ed.EditorMixin.openxml(self)

    def preview(self, evt = None):
        "toon preview dialoog"
        edt = PreviewDialog(self)
        edt.ShowModal()
        edt.Destroy()

    def savexmlas(self, evt = None):
        """vraag bestand om html op te slaan
        bestand opslaan en naam in titel en root element zetten"""
        dname, fname = os.path.split(self.xmlfn)
        dlg = wx.FileDialog(
            self, message = "Save file as ...",
            defaultDir = dname,
            defaultFile = fname,
            wildcard = HMASK,
            style = wx.SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.xmlfn = dlg.GetPath()
            self.savexmlfile(saveas = True)
            self.tree.SetItemText(self.top, self.xmlfn)
            self.SetTitle(" - ".join((os.path.split(self.xmlfn)[-1], TITEL)))
        dlg.Destroy()

    def about(self, evt = None):
        "toon programma info"
        ed.EditorMixin.about(self)
        wx.MessageBox(self.abouttext, self.title, wx.OK | wx.ICON_INFORMATION)

    def openfile(self):
        """vraag bestand om te openen
        controleer of het geparsed kan worden"""
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir = os.getcwd(),
            wildcard = HMASK,
            style = wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            pname = dlg.GetPath()
            if not ed.EditorMixin.openfile(self, pname):
                dlg = wx.MessageBox(self.title, 'html parsing error',
                               wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
        dlg.Destroy()

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

    def savexmlfile(self, saveas = False):
        "open file en schrijf html erheen"
        if not saveas:
            try:
                shutil.copyfile(self.xmlfn, self.xmlfn + '.bak')
            except IOError as mld:
                wx.MessageBox(mld, self.title, wx.OK | wx.ICON_ERROR)
        self.maakhtml()
        try:
            with open(self.xmlfn,"w") as f_out:
                f_out.write(str(self.soup))
            self.tree_dirty = False
        except IOError as err:
            dlg = wx.MessageBox(self.title, err, wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def maakhtml(self):
        "interne tree omzetten in BeautifulSoup object"
        def expandnode(node, root, data, commented = False):
            "tree item (node) met inhoud (data) toevoegen aan BS node (root)"
            ## print data, commented
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
                            ## print "before:", elm, text, data
                            expandnode(elm, sub, data, is_comment)
                            ## print "after:", sub
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
        self.soup = bs.BeautifulSoup()
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

    ## def on_bdown(self, ev=None):
        ## if wx.recon_context(self.tree, ev):
            ## self.item = self.tree.selection
            ## if self.item == self.top:
                ## wx.context_menu(self, ev, self.filemenu)
            ## elif self.item is not None:
                ## wx.context_menu(self, ev, self.editmenu)
            ## else:
                ## wx.Message.ok(self.title,'You need to select a tree item first')
                ## #menu.append()
        ## else:
            ## ev.skip()

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
        if item and item != self.top:
            self.tree.SelectItem(item)
            data = self.tree.GetItemText(item)
            menu = wx.Menu()
            menu.Append(self.VW_EXP, "Expand All (sub)Levels")
            menu.Append(self.VW_CLP, "Collapse All (sub)Levels")
            edit_menu = wx.Menu()
            edit_menu.Append(self.EM_EDT, "Edit")
            edit_menu.AppendSeparator()
            edit_menu.Append(self.EM_CUT, "Cut")
            edit_menu.Append(self.EM_CPY, "Copy")
            edit_menu.Append(self.EM_PB, "Paste Before")
            edit_menu.Append(self.EM_PA, "Paste After")
            if data.startswith(ELSTART):
                edit_menu.Append(self.EM_PU, "Paste Under")
            edit_menu.AppendSeparator()
            edit_menu.Append(self.EM_DEL, "Delete")
            if data.startswith(ELSTART):
                edit_menu.Append(self.EM_IT, "Insert Text (under)")
            edit_menu.Append(self.EM_IB, 'Insert Element Before')
            edit_menu.Append(self.EM_IA, 'Insert Element After')
            if data.startswith(ELSTART):
                edit_menu.Append(self.EM_IU, 'Insert Eledit_menuent Under')
            menu.AppendMenu(-1, "Edit", edit_menu)
            html_menu = wx.Menu()
            html_menu.Append(self.HM_DTD, "Add DTD")
            if data.startswith(ELSTART):
                html_menu.Append(self.HM_LNK, "Create link (under)")
                html_menu.Append(self.HM_IMG, "Add image (under)")
                html_menu.Append(self.HM_LST, "Add list (under)")
                html_menu.Append(self.HM_TBL, "Add table (under)")
            menu.AppendMenu(-1, "HTML", html_menu)
            self.PopupMenu(menu)
            ## print "klaar met menu"
            menu.Destroy()
        ## pass

    def on_key(self, event):
        """afhandeling toetscombinaties"""
        ## pass # for now
        skip = True
        keycode = event.GetKeyCode()
        mods = event.GetModifiers()
        win = event.GetEventObject()
        if keycode == wx.WXK_INSERT and win == self.tree:
            if mods == wx.MOD_CONTROL:
                self.add_text()
            elif mods == wx.MOD_SHIFT:
                self.insert()
            elif mods == wx.MOD_ALT:
                self.ins_aft()
            else:
                self.ins_chld()
        elif keycode == ord("V"):
            if mods == wx.MOD_CONTROL:
                self.paste_blw()
            elif mods == wx.MOD_CONTROL | wx.MOD_SHIFT:
                self.paste()
            elif mods == wx.MOD_CONTROL | wx.MOD_ALT:
                self.paste_aft()
        elif keycode == ord("S"):
            if mods == wx.MOD_CONTROL:
                self.savexml()
            elif mods == wx.MOD_CONTROL | wx.MOD_SHIFT:
                self.savexmlas()
        elif mods == wx.MOD_CONTROL:
            if keycode == ord("O"):
                self.openxml()
            elif keycode == ord("N"):
                self.newxml()
            elif keycode == ord("R"):
                self.reopenxml()
            elif keycode == ord("Q"):
                self.quit()
            elif keycode == ord("X") and win == self.tree:
                self.cut()
            elif keycode == ord("C") and win == self.tree:
                self.copy()
            elif keycode == ord("+") and win == self.tree:
                self.expand()
            elif keycode == ord("-") and win == self.tree:
                self.collapse()
        ## elif keycode == wx.WXK_F1:
            ## self.help_page()
        elif keycode == wx.WXK_F2: # and win == self.tree:
            self.edit()
        elif keycode == wx.WXK_DELETE and win == self.tree:
            self.delete()
        ## elif keycode == wx.WXK_ESCAPE:
            ## self.afsl()
        if event and skip:
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
        ## print "edit:", data
        if data.startswith(ELSTART) or data.startswith(CMELSTART):
            attrdict = self.tree.GetItemData(self.item).GetData()
            was_commented = data.startswith(CMSTART)
            ## print "element attrs:", attrdict
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
                ## print self.tree.GetItemText(self.item)
                ## print "voor:", self.tree.GetItemData(self.item).GetData()
                self.tree.SetPyData(self.item, attrs)
                ## print "na:", self.tree.GetItemData(self.item).GetData()
                if commented != was_commented:
                    comment_out(self.item, commented)
                self.tree_dirty = True
        else:
            txt = CMSTART + " " if data.startswith(CMSTART) else ""
            data = self.tree.GetItemData(self.item).GetData()
            ## print "text:", txt, data
            edt = TextDialog(self, title='Edit Text', text = txt + data)
            if edt.ShowModal() == wx.ID_SAVE:
                txt = edt.data_text.GetValue()
                self.tree.SetItemText(self.item, ed.getshortname(txt,
                    edt.comment_button.GetValue()))
                self.tree.SetPyData(self.item, txt)
                self.tree_dirty = True
        edt.Destroy()

    def copy(self, evt = None, cut = False, retain = True):
        "start copy/cut/delete actie"
        def push_el(elm, result):
            "subitem(s) toevoegen aan copy buffer"
            ## print "start: ",result
            text = self.tree.GetItemText(elm)
            data = self.tree.GetItemPyData(elm)
            atrlist = []
            ## print "before looping over contents:",text,y
            if text.startswith(ELSTART):
                node, pos = self.tree.GetFirstChild(elm)
                while node.IsOk():
                    ## print "\tbefore going down:",y
                    x = push_el(node, atrlist)
                    ## print "\t", self.tree.GetItemText(x), z
                    ## print y
                    ## y.append(z) # geeft die ellipsis aan het eind - is blijkbaar ook niet nodig
                    ## print "\tafter going down: ",y
                    node, pos = self.tree.GetNextChild(elm, pos)
            ## print "after  looping over contents: ",text,y
            result.append((text, data, atrlist))
            ## print "end:  ",result
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
                ## print "copy: get_them", self.cut_el
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
            try:
                if self.cut_txt.startswith(DTDSTART):
                    self.has_dtd = False
            except AttributeError:
            ## except ValueError:
                pass
        ## self.pastebeforeitem.text="Paste Before"
        ## self.pastebeforeitem.enable(True)
        ## self.pasteafteritem.text="Paste After"
        ## self.pasteafteritem.enable(True)
        ## self.pastebelowitem.text ="Paste Under"
        ## self.pastebelowitem.enable(True)

    def paste(self, evt = None, before = True, below = False):
        "start paste actie"
        def zetzeronder(node, elm, pos = -1):
            "paste copy buffer into tree"
            ## print "zetzeronder", pos
            ## print node
            ## print el
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
        #if self.cut:
        #    self.pastebeforeitem.set_text = "Nothing to Paste"
        #    self.pastebeforeitem.enable(False)
        #    self.pasteafteritem.set_text = " "
        #    self.pasteafteritem.enable(False)
        #    self.pastebelowitem.set_text = " "
        #    self.pastebelowitem.enable(False)
        if self.cut_txt:
            item = ed.getshortname(self.cut_txt)
            data = self.cut_txt
            if below:
                node = self.tree.AppendItem(self.item, item)
                self.tree.SetPyData(self.item, data)
                ## i = len(node)
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
            ## print "paste element"
            ## print node
            ## print self.cut_el
            zetzeronder(node, self.cut_el[0], idx)
        self.tree_dirty = True

    def add_text(self, evt = None):
        "tekst toevoegen onder huidige element"
        if DESKTOP and not self.checkselection():
            return
        if not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't insert below text", self.title)
            return
        edt = TextDialog(self, title="New Text")
        if edt.ShowModal() == wx.ID_SAVE:
            txt = edt.data_text.GetValue()
            new_item = self.tree.AppendItem(self.item, ed.getshortname(txt,
                edt.comment_button.GetValue()))
            self.tree.SetPyData(new_item, txt)
            # om te testen:
            ## text = self.tree.GetItemText(new_item)
            ## data = self.tree.GetItemPyData(new_item)
            ## print text,data
            self.tree_dirty = True
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
            print "under comment:", under_comment
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
                print "commented, under_comment:", commented, under_comment
                text = ed.getelname(tag, data, commented or under_comment)
                print text
                item = self.tree.AppendItem(self.item, text)
                self.tree.SetPyData(item, data)
            else:
                parent = self.tree.GetItemParent(self.item)
                text = self.tree.GetItemText(parent)
                under_comment = text.startswith(CMSTART)
                print "commented, under_comment:", commented, under_comment
                text = ed.getelname(tag, data, commented or under_comment)
                item = self.item if not before else self.tree.GetPrevSibling(self.item)
                node = self.tree.InsertItem(parent, item, text)
                self.tree.SetPyData(node, data)
            self.tree_dirty = True
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
        edt.Destroy()

def main_gui(args):
    "start main GUI"
    app = wx.App(redirect = True, filename = "ashe.log")
    if len(args) > 1:
        frm = MainFrame(None, -1, fname = args[1])
    else:
        frm = MainFrame(None, -1)
    app.MainLoop()

if __name__ == "__main__":
    print sys.argv
    main_gui(sys.argv)
