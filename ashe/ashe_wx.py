import os,sys,shutil,copy
import BeautifulSoup as bs
ELSTART = '<>'
DTDSTART = "<!DOCTYPE"
BL = "&nbsp;"
TITEL = "Albert's Simple HTML-editor"
HMASK = "HTML files (*.htm,*.html)|*.htm;*.html|All files (*.*)|*.*"
IMASK = "All files|*.*"
PPATH = os.path.split(__file__)[0]

import ashe_mixin as ed
if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True
import wx
import wx.grid as wxgrid
import wx.html as  html

class PreviewDialog(wx.Dialog):
    def __init__(self,parent):
        self.parent = parent
        wx.Dialog.__init__(self,parent,title='Preview HTML',size=(1024,800),
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER ,
            ) #,action=("Cancel", self.on_cancel))
        self.pnl = wx.Panel(self,-1)

        self.parent.maakhtml()
        self.data_file = "tempfile.html"
        f = open(self.data_file,"w")
        f.write(str(self.parent.bs))
        f.close()

        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15,15,15,15))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.html = html.HtmlWindow(self.pnl,-1,size=(1024,768)) #, zoom_level = 0)
        ## self.html.SetRelatedFrame(self, "%s")
        self.html.LoadPage(self.data_file)
        hbox.Add(self.html,1) #,wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox,1)

        ## hbox = wx.BoxSizer(wx.HORIZONTAL)
        ## self.bOk = wx.Button(self.pnl,id=wx.ID_OK)
        ## hbox.Add(self.bOk,0,wx.ALL, 2)
        ## vbox.Add(hbox,0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

class DTDDialog(wx.Dialog):
    # AttributeError: 'module' object has no attribute 'RadioGroup'
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,title="Add DTD") # ,action=("Cancel", self.on_cancel))
        self.pnl = wx.Panel(self,-1)
        self.rbgDTD = [
            ['HTML 4.1 Strict',       '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'],
            ['HTML 4.1 Transitional', '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'],
            ['HTML 4.1 Frameset',     '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">'],
            ['XHTML 1.0 Strict',      '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'],
            ['XHTML 1.0 Transitional','<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'],
            ['XHTML 1.0 Frameset',    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'],
            ]
        vbox = wx.BoxSizer(wx.VERTICAL) # ,border=(15,15,15,15))

        box = wx.StaticBox(self.pnl,-1)
        sbox = wx.StaticBoxSizer(box,wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lblLink = wx.StaticText(self.pnl,-1, "Select document type:")
        hbox.Add(lblLink,0,wx.TOP,10)
        sbox.Add(hbox,0) # ,wx.LEFT|wx.RIGHT,10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        for i,x in enumerate(self.rbgDTD[:3]):
            if i == 0:
                rb = wx.RadioButton(self.pnl,-1,x[0],style = wx.RB_GROUP)
            else:
                rb = wx.RadioButton(self.pnl,-1,x[0])
            x.append(rb)
            vbox2.Add(rb,0,wx.ALL,2)
        hbox.Add(vbox2) # ,0,wx.TOP,15)
        sbox.Add(hbox,0,wx.ALL,10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        for x in self.rbgDTD[3:]:
            rb = wx.RadioButton(self.pnl,-1,x[0])
            x.append(rb)
            vbox2.Add(rb,0,wx.ALL,2)
        hbox.Add(vbox2)
        sbox.Add(hbox,1,wx.EXPAND | wx.ALL,10)
        vbox.Add(sbox,1,wx.EXPAND | wx.LEFT | wx.RIGHT,15)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE) # label='Save')
        self.SetAffirmativeId(wx.ID_SAVE)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL) #label='Cancel')
        hbox.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,5)
        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

class LinkDialog(wx.Dialog):
    # AttributeError: type object 'FileDialog' has no attribute 'open'
    def __init__(self,parent):
        self.parent = parent
        wx.Dialog.__init__(self,parent,title='Add Link') #,action=("Cancel", self.on_cancel))
        self.pnl = wx.Panel(self,-1)
        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15,15,15,15))

        box = wx.StaticBox(self.pnl,-1)
        sbox = wx.StaticBoxSizer(box,wx.VERTICAL)
        gbox = wx.GridBagSizer(4,4)
        lblLink = wx.StaticText(self.pnl,-1, "link to document:")
        gbox.Add(lblLink,(0,0),(1,1),wx.ALIGN_CENTER_VERTICAL)
        self.txtLink = wx.TextCtrl(self.pnl,-1,size=(250,-1),value="http://")
        gbox.Add(self.txtLink,(0,1))

        self.bKies = wx.Button(self.pnl,-1,'Search')
        self.bKies.Bind(wx.EVT_BUTTON,self.kies)
        gbox.Add(self.bKies,(1,0),(1,2),wx.ALIGN_CENTER_HORIZONTAL)

        lblTitle = wx.StaticText(self.pnl,-1, "descriptive title:")
        gbox.Add(lblTitle,(2,0),(1,1),wx.ALIGN_CENTER_VERTICAL)
        self.txtTitle = wx.TextCtrl(self.pnl,-1,size=(250,-1))
        gbox.Add(self.txtTitle,(2,1))

        sbox.Add(gbox,0,wx.ALL,10)
        vbox.Add(sbox,0,wx.ALL,15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE) # label='Save')
        self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL) #label='Cancel')
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,2)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

    def kies(self,ev=None):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            wildcard=HMASK,
            style=wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            h = dlg.GetPath()
            self.txtLink.SetValue(h)
        dlg.Destroy()

    def on_ok(self,ev=None):
        link = self.txtLink.GetValue()
        if link:
            link = ed.getrelativepath(link,self.parent.xmlfn)
            if not link:
                wx.MessageBox('Impossible to make this local link relative',self.parent.title)
            else:
                self.link = link
                ev.Skip()
        else:
            wx.MessageBox("link opgeven of cancel kiezen s.v.p",'')

class ImageDialog(wx.Dialog):
    # AttributeError: type object 'FileDialog' has no attribute 'open'
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,title='Add Image') #,action=("Cancel", self.on_cancel))
        self.parent = parent
        self.pnl = wx.Panel(self,-1)
        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15,15,15,15))

        box = wx.StaticBox(self.pnl,-1)
        sbox = wx.StaticBoxSizer(box,wx.VERTICAL)
        gbox = wx.GridBagSizer(4,4)
        lblLink = wx.StaticText(self.pnl,-1, "link to image:")
        gbox.Add(lblLink,(0,0),(1,1),wx.ALIGN_CENTER_VERTICAL)
        self.txtLink = wx.TextCtrl(self.pnl,-1,size=(250,-1),value="http://")
        gbox.Add(self.txtLink,(0,1))

        self.bKies = wx.Button(self.pnl,-1,'Search')
        self.bKies.Bind(wx.EVT_BUTTON,self.kies)
        gbox.Add(self.bKies,(1,0),(1,2),wx.ALIGN_CENTER_HORIZONTAL)

        lblTitle = wx.StaticText(self.pnl,-1, "descriptive title:")
        gbox.Add(lblTitle,(2,0),(1,1),wx.ALIGN_CENTER_VERTICAL)
        self.txtTitle = wx.TextCtrl(self.pnl,-1,size=(250,-1))
        gbox.Add(self.txtTitle,(2,1))

        lblAlt = wx.StaticText(self.pnl,-1, "alternate text:")
        gbox.Add(lblAlt,(3,0),(1,1),wx.ALIGN_CENTER_VERTICAL)
        self.txtAlt = wx.TextCtrl(self.pnl,-1,size=(250,-1))
        gbox.Add(self.txtAlt,(3,1))

        sbox.Add(gbox,0,wx.ALL,10)
        vbox.Add(sbox,0,wx.ALL,15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE) # label='Save')
        self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL) #label='Cancel')
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,2)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

    def kies(self,ev=None):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            wildcard=IMASK,
            style=wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            h = dlg.GetPath()
            self.txtLink.SetValue(h)
        dlg.Destroy()

    def on_ok(self,ev=None):
        link = self.txtLink.GetValue()# probeer het opgegeven pad relatief te maken t.o.v. het huidige
        if link:
            link = ed.getrelativepath(link,self.parent.xmlfn)
            if not link:
                wx.MessageBox('Impossible to make this local link relative',self.parent.title)
            else:
                self.link = link
                ev.Skip()
        else:
            wx.Message.ok("","image link opgeven of cancel kiezen s.v.p")

class ListDialog(wx.Dialog):
    # AttributeError: 'module' object has no attribute 'Combo'
    def __init__(self,parent):
        self.items = []
        self.dataitems = []
        wx.Dialog.__init__(self,parent,title='Add List') #,action=("Cancel", self.on_cancel))
        self.pnl = wx.Panel(self,-1)
        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15,15,15,15))

        box = wx.StaticBox(self.pnl,-1)
        sbox = wx.StaticBoxSizer(box,wx.VERTICAL)

        ## tsizer = wx.TBox(2,2,border=(2,2,20,2),spacing_x=2,spacing_y=2)
        tbox = wx.FlexGridSizer(2, 2, 2, 2)  # rows, cols, vgap, hgap
        lblType = wx.StaticText(self.pnl,-1, "choose type of list:")
        self.cmbType = wx.ComboBox(self.pnl,-1,style=wx.CB_DROPDOWN,choices=[
            "unordered",
            "ordered",
            "definition",
            ])
        self.cmbType.SetStringSelection("unordered")
        self.cmbType.Bind(wx.EVT_COMBOBOX,self.on_type)
        tbox.Add(lblType,0,wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.cmbType)

        lblNr = wx.StaticText(self.pnl,-1, "initial number of items:")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        #~ self.txtNr = wx.TextCtrl(self.pnl,-1,size=(20,-1))
        self.txtNr = wx.SpinCtrl(self.pnl,-1,size=(40,-1))
        self.txtNr.Bind(wx.EVT_SPINCTRL,self.on_text)
        #~ self.txtNr.Bind(wx.EVT_TEXT,self.on_text)
        tbox.Add(lblNr,0,wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.txtNr) ## hbox)
        sbox.Add(tbox,0,wx.ALL,5)

        #~ hbox = wx.BoxSizer(wx.HORIZONTAL)
        tbl = wxgrid.Grid(self.pnl,-1,size=(340,120))
        tbl.CreateGrid(0,1)
        tbl.SetColLabelValue(0,'list item')
        tbl.SetColSize(0,240)
        self.tblList = tbl
        sbox.Add(self.tblList,0,wx.ALL,2)
        vbox.Add(sbox,0,wx.LEFT,20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE) # label='Save')
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL) #label='Cancel')
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,2)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

    def on_type(self,ev=None):
        s = self.cmbType.GetValue()
        nt = self.tblList.GetNumberCols()
        if s[0] == "d" and nt == 1:
                self.tblList.InsertCols(0,1)
                self.tblList.SetColLabelValue(0,'term')
                self.tblList.SetColSize(0,80)
                self.tblList.SetColLabelValue(1,'description')
                self.tblList.SetColSize(1,160)

        elif s[0] != "d" and nt == 2:
                self.tblList.DeleteCols(0)
                self.tblList.SetColLabelValue(0,'list item')
                self.tblList.SetColSize(0,240)

    def on_text(self,ev=None):
        try:
            num = int(self.txtNr.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer','')
            return
        nt = self.tblList.GetNumberRows()
        if nt > num:
            for ix in xrange(nt-1,num-1,-1):
                ## print ix
                self.tblList.DeleteRows(ix)
        elif num > nt:
            for ix in xrange(nt,num):
                self.tblList.AppendRows(1)
                self.tblList.SetRowLabelValue(ix,'')

class TableDialog(wx.Dialog):
    #
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,title='Add Table') #,action=("Cancel", self.on_cancel))
        self.pnl = wx.Panel(self,-1)
        self.headings = []
        vbox = wx.BoxSizer(wx.VERTICAL) # border=(15,15,15,15))

        box = wx.StaticBox(self.pnl,-1)
        sbox = wx.StaticBoxSizer(box,wx.VERTICAL)

        ## tbox = wx.TBox(2,2,border=(2,2,20,2),spacing_x=2,spacing_y=2)
        tbox = wx.FlexGridSizer(2, 2, 2, 2)  # rows, cols, vgap, hgap
        lblRows = wx.StaticText(self.pnl,-1, "initial number of rows:")
        ## self.txtRows = wx.TextCtrl(self.pnl,-1)
        self.txtRows = wx.SpinCtrl(self.pnl,-1,size=(40,-1))
        self.txtRows.Bind(wx.EVT_SPINCTRL,self.on_rows)
        self.txtRows.Bind(wx.EVT_TEXT,self.on_rows)
        tbox.Add(lblRows)
        tbox.Add(self.txtRows)

        lblCols = wx.StaticText(self.pnl,-1, "initial number of columns:")
        ## self.txtCols = wx.TextCtrl(self.pnl,-1)
        self.txtCols = wx.SpinCtrl(self.pnl,-1,size=(40,-1))
        self.txtCols.Bind(wx.EVT_SPINCTRL,self.on_cols)
        self.txtCols.Bind(wx.EVT_TEXT,self.on_cols)
        tbox.Add(lblCols)
        tbox.Add(self.txtCols)
        sbox.Add(tbox,0,wx.ALL,5)

        tbl = wxgrid.Grid(self.pnl,-1,size=(340,120))
        tbl.CreateGrid(0,0)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_LEFT_CLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_LEFT_DCLICK, self.on_title)
        tbl.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_DCLICK, self.on_title)
        self.tblTable = tbl
        sbox.Add(self.tblTable,0,wx.ALL,2)
        vbox.Add(sbox,0,wx.LEFT,20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE) # label='Save')
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL) #label='Cancel')
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,2)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

    def on_rows(self,ev=None):
        try:
            num = int(self.txtRows.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer','')
            return
        nt = self.tblTable.GetNumberRows()
        if nt > num:
            for ix in xrange(nt-1,num-1,-1):
                ## print ix
                self.tblTable.DeleteRows(ix)
        elif num > nt:
            for ix in xrange(nt,num):
                self.tblTable.AppendRows(1)
                self.tblTable.SetRowLabelValue(ix,'')

    def on_cols(self,ev=None):
        try:
            num = int(self.txtCols.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer','')
            return
        nt = self.tblTable.GetNumberCols()
        if nt > num:
            for ix in xrange(nt-1,num-1,-1):
                ## print ix
                self.tblTable.DeleteCols(ix)
        elif num > nt:
            for ix in xrange(nt,num):
                self.tblTable.AppendCols(1)
                self.tblTable.SetColLabelValue(ix,'')

    def on_title(self,ev=None):
        if ev:
            col,row = ev.GetCol(),ev.GetRow()
            if col < 0:
                return
            dlg = wx.TextEntryDialog(
                self, 'Enter a title for this column:',
                '')
            if dlg.ShowModal() == wx.ID_OK:
                self.tblTable.SetColLabelValue(col,dlg.GetValue())
            dlg.Destroy()

class ElementDialog(wx.Dialog):
    def __init__(self,parent,title='',tag=None,attrs=None):
        wx.Dialog.__init__(self,parent,-1,title=title) # action=("Cancel", self.on_cancel))
        self.pnl = wx.Panel(self,-1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lblName = wx.StaticText(self.pnl,-1, "element name:")
        self.txtTag = wx.TextCtrl(self.pnl,-1)
        if tag:
            self.txtTag.SetValue(tag.split()[1])
            ## self.txtTag.readonly=True
        hbox.Add(lblName,0,wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.txtTag,0,wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(hbox,0,wx.LEFT,20)

        box = wx.StaticBox(self.pnl,-1)
        sbox = wx.StaticBoxSizer(box,wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        tbl = wxgrid.Grid(self.pnl,-1,size=(340,120))
        tbl.CreateGrid(0,2)
        tbl.SetColLabelValue(0,'attribute')
        tbl.SetColLabelValue(1,'value')
        tbl.SetColSize(1,160)
        if attrs:
            for attr,value in attrs.items():
                tbl.AppendRows(1)
                ix = tbl.GetNumberRows() - 1
                tbl.SetRowLabelValue(ix,'')
                tbl.SetCellValue(ix,0,attr)
                tbl.SetCellValue(ix,1,value)
        else:
            self.row = -1
        ## tbl.bind(selchanged=self.on_sel)
        self.tblAttr = tbl
        hbox.Add(self.tblAttr)
        sbox.Add(hbox) # ,1,wx.EXPAND|wx.ALL,5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bAdd = wx.Button(self.pnl,label='Add Attribute')
        self.bAdd.Bind(wx.EVT_BUTTON,self.on_add)
        self.bDel = wx.Button(self.pnl,label='Delete Selected')
        self.bDel.Bind(wx.EVT_BUTTON,self.on_del)
        hbox.Add(self.bAdd,0,wx.EXPAND | wx.ALL, 1)
        hbox.Add(self.bDel,0,wx.EXPAND | wx.ALL, 1)
        sbox.Add(hbox,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,1) # ,wx.EXPAND|wx.ALL,5)
        vbox.Add(sbox,0,wx.LEFT,20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE) # label='Save')
        ## self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL) #label='Cancel')
        ## self.bCancel.Bind(wx.EVT_BUTTON,self.on_cancel)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,2)

        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()
        ## self.Show(True)

    def on_add(self,ev=None):
        self.tblAttr.AppendRows(1)
        ix = self.tblAttr.GetNumberRows() - 1
        self.tblAttr.SetRowLabelValue(ix,'')

    def on_del(self,ev=None):
        s = self.tblAttr.GetSelectedRows()
        if s:
            s.reverse()
            for ix in s:
                self.tblAttr.DeleteRows(ix,1)
        else:
            wx.MessageBox("Select a row by clicking on the row heading",'Selection is empty',wx.ICON_INFORMATION)

class TextDialog(wx.Dialog):
    def __init__(self,parent,title='',text=None):
        if text is None:
            text = ''
        wx.Dialog.__init__(self,parent,-1,title) #,action=("Cancel", self.on_cancel))
        self.pnl = wx.Panel(self,-1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.txtData = wx.TextCtrl(self.pnl,-1, size=(340,175), style=wx.TE_MULTILINE)
        self.txtData.SetValue(text)
        hbox.Add(self.txtData,1,wx.EXPAND | wx.ALL,5)
        vbox.Add(hbox,0,wx.LEFT,20)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE) # label='Save')
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL) #label='Cancel')
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,2)
        self.sizer = vbox
        self.pnl.SetSizer(vbox)
        self.pnl.SetAutoLayout(True)
        vbox.Fit(self.pnl)
        vbox.SetSizeHints(self.pnl)
        self.pnl.Layout()

class MainFrame(wx.Frame,ed.editormixin):
    def __init__(self,parent,id,fn=''):
        self.parent = parent
        self.title = "(untitled) - Albert's Simple HTML Editor"
        self.xmlfn = fn
        wx.Frame.__init__(self, parent, id,
            pos=(2,2),
            size=(620,900)
            )
        self.SetIcon(wx.Icon(os.path.join(PPATH,"ashe.ico"),wx.BITMAP_TYPE_ICO))

        menuBar = wx.MenuBar()

        self.filemenu = wx.Menu()
        self.FM_NEW = wx.NewId()
        self.FM_OPN = wx.NewId()
        self.FM_SAV = wx.NewId()
        self.FM_SAS = wx.NewId()
        self.FM_PVW = wx.NewId()
        self.FM_XIT = wx.NewId()

        self.filemenu.Append(self.FM_NEW,"&New")
        self.filemenu.Append(self.FM_OPN,"&Open")
        self.filemenu.Append(self.FM_SAV,'&Save')
        self.filemenu.Append(self.FM_SAS,'Save &As')
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.FM_PVW,'Pre&view')
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.FM_XIT,'E&xit')
        menuBar.Append(self.filemenu, "&File")

        self.viewmenu = wx.Menu()
        self.VW_EXP = wx.NewId()
        self.VW_CLP = wx.NewId()
        self.viewmenu.Append(self.VW_EXP,"Expand All (sub)Levels")
        self.viewmenu.Append(self.VW_CLP,"Collapse All (sub)Levels")
        menuBar.Append(self.viewmenu, "&View")

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
        self.editmenu.Append(self.EM_EDT,"Edit")
        self.editmenu.AppendSeparator()
        self.editmenu.Append(self.EM_CUT,"Cut")
        self.editmenu.Append(self.EM_CPY,"Copy")
        self.pastebeforeitem = self.editmenu.Append(self.EM_PB,"Paste Before")
        self.pasteafteritem = self.editmenu.Append(self.EM_PA,"Paste After")
        self.pastebelowitem = self.editmenu.Append(self.EM_PU,"Paste Under")
        self.editmenu.AppendSeparator()
        self.editmenu.Append(self.EM_DEL,"Delete")
        self.editmenu.Append(self.EM_IT,"Insert Text (under)")
        self.editmenu.Append(self.EM_IB,'Insert Element Before')
        self.editmenu.Append(self.EM_IA,'Insert Element After')
        self.editmenu.Append(self.EM_IU,'Insert Element Under')
        ## self.pastebeforeitem.title = "Nothing to Paste"
        ## self.pastebeforeitem.enable(False)
        ## self.pasteafteritem.title = " "
        ## self.pasteafteritem.enable(False)
        ## self.pastebelowitem.title = " "
        ## self.pastebelowitem.enable(False)
        menuBar.Append(self.editmenu, "&Edit")

        # self.helpmenu.append('About', callback = self.about)
        self.htmlmenu = wx.Menu()
        self.HM_DTD = wx.NewId()
        self.HM_LNK = wx.NewId()
        self.HM_IMG = wx.NewId()
        self.HM_LST = wx.NewId()
        self.HM_TBL = wx.NewId()
        self.dtdmenu = self.htmlmenu.Append(self.HM_DTD,"Add DTD")
        self.htmlmenu.Append(self.HM_LNK,"Create link (under)")
        self.htmlmenu.Append(self.HM_IMG,"Add image (under)")
        self.htmlmenu.Append(self.HM_LST,"Add list (under)")
        self.htmlmenu.Append(self.HM_TBL,"Add table (under)")
        menuBar.Append(self.htmlmenu, "&HTML")
        self.SetMenuBar(menuBar)

        self.Connect(self.FM_NEW,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.newxml)
        self.Connect(self.FM_OPN,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.openxml)
        self.Connect(self.FM_SAV,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.savexml)
        self.Connect(self.FM_SAS,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.savexmlas)
        self.Connect(self.FM_PVW,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.preview)
        self.Connect(self.FM_XIT,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.quit)
        self.Connect(self.VW_EXP,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.expand   )
        self.Connect(self.VW_CLP,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.collapse )
        self.Connect(self.EM_EDT,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.edit     )
        self.Connect(self.EM_CUT,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.cut      )
        self.Connect(self.EM_CPY,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.copy     )
        self.Connect(self.EM_DEL,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.delete   )
        self.Connect(self.EM_PB ,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.paste    )
        self.Connect(self.EM_PA ,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.paste_aft)
        self.Connect(self.EM_PU ,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.paste_blw)
        self.Connect(self.EM_IT ,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.add_text )
        self.Connect(self.EM_IB ,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.insert   )
        self.Connect(self.EM_IA ,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.ins_aft  )
        self.Connect(self.EM_IU ,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.ins_chld )
        self.Connect(self.HM_DTD,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.add_dtd  )
        self.Connect(self.HM_LNK,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.add_link )
        self.Connect(self.HM_IMG,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.add_image)
        self.Connect(self.HM_LST,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.add_list )
        self.Connect(self.HM_TBL,-1,wx.wxEVT_COMMAND_MENU_SELECTED,self.add_table)

        self.pnl = wx.Panel(self,-1)

        self.tree = wx.TreeCtrl(self.pnl,-1)
        ## isz = (16,16)
        ## il = wx.ImageList(isz[0], isz[1])
        ## fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        ## fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        ## fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        ## self.tree.SetImageList(il)
        ## self.il = il
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDClick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        ## self.tree.Bind(wx.EVT_CONTEXT_MENU, self.onContextMenu)

        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.tree,1,wx.EXPAND)
        sizer0.Add(sizer1,1,wx.EXPAND)

        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)

        ed.editormixin.init_fn(self)

    def quit(self,ev=None):
        if self.check_tree() != wx.CANCEL:
            self.Close()

    def preview(self,ev=None):
        edt = PreviewDialog(self)
        h = edt.ShowModal()
        edt.Destroy()

    def check_tree(self):
        print "check_tree aangeroepen"
        if self.tree_dirty:
            h = wx.MessageBox("XML data has been modified - save before continuing?",
                self.title,
                style = wx.YES_NO | wx.CANCEL)
            if h == wx.ID_YES:
                self.savexml()
            return h

    def newxml(self, ev=None):
        if self.check_tree() != wx.CANCEL:
            ed.editormixin.newxml(self)

    def openxml(self, ev=None):
        if self.check_tree() != wx.CANCEL:
            ed.editormixin.openxml(self)

    def savexmlas(self,ev=None):
        d,f = os.path.split(self.xmlfn) # AttributeError: 'module' object has no attribute 'split'
        dlg = wx.FileDialog(
            self, message="Save file as ...",
            defaultDir=d,
            defaultFile=f,
            wildcard=HMASK,
            style=wx.SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.xmlfn = dlg.GetPath()
            self.savexmlfile(saveas=True)
            self.tree.SetItemText(self.top,self.xmlfn)
            self.SetTitle(" - ".join((os.path.split(titel)[-1],TITEL)))
        dlg.Destroy()

    def about(self,ev=None):
        ed.editormixin.about(self)
        wx.MessageBox(self.abouttext,self.title,wx.OK|wx.ICON_INFORMATION)

    def openfile(self):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            wildcard=HMASK,
            style=wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            h = dlg.GetPath()
            if not ed.editormixin.openfile(self,h):
                dlg = wx.MessageBox(self.title,'html parsing error',
                               wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
        dlg.Destroy()

    def addtreeitem(self,node,naam,data):
        rr = self.tree.AppendItem(node,naam)
        self.tree.SetPyData(rr,data)
        return rr

    def addtreetop(self,fn,titel):
        self.SetTitle(titel)
        self.top = self.tree.AddRoot(fn)

    def init_tree(self,name=''):
        self.tree.DeleteAllItems()
        ed.editormixin.init_tree(self,name)
        if DESKTOP:
            self.tree.SelectItem(self.top)

    def savexmlfile(self,saveas=False):
        if not saveas:
            try:
                shutil.copyfile(self.xmlfn,self.xmlfn + '.bak')
            except IOError,mld:
                wx.MessageBox(mld,self.title,wx.OK|wx.ICON_ERROR)
        self.maakhtml()
        f = open(self.xmlfn,"w")
        f.write(str(self.bs))
        f.close()
        self.tree_dirty = False


    def maakhtml(self):
        def expandnode(node,root,data):
            try:
                for att in data:
                    root[att] = data[att]
            except TypeError:
                pass
            el,c = self.tree.GetFirstChild(node)
            while el.IsOk():
                text = self.tree.GetItemText(el)
                data = self.tree.GetItemPyData(el)
                if text.startswith(ELSTART):
                    sub = bs.Tag(self.bs,text.split(None,2)[1])
                    root.append(sub) # insert(0,sub)
                    expandnode(el,sub,data)
                else:
                    # dit levert fouten op bij het gebruiken van diacrieten
                    ## sub = bs.NavigableString(.ed.escape(data))
                    ## root.append(sub) # insert(0,sub)
                    # dit niet maar er wordt niet correct gecodeerd
                    ## root.append(ed.escape(data))
                    # misschien dat dit het doet
                    sub = bs.NavigableString(data.decode("latin-1"))
                    root.append(data.decode("latin-1")) # insert(0,sub)
                el,c = self.tree.GetNextChild(node,c)

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
        self.bs = bs.BeautifulSoup()
        tag,c = self.tree.GetFirstChild(self.top)
        while tag.IsOk():
            text = self.tree.GetItemText(tag)
            data = self.tree.GetItemPyData(tag)
            if not text.startswith(ELSTART):
                sub = bs.Declaration(data)
            else:
                root = bs.Tag(self.bs, text.split(None,2)[1])
                self.bs.insert(0,root)
                expandnode(tag,root,data)
            tag,c = self.tree.GetNextChild(self.top,c)

    def onLeftDClick(self,ev=None):
        pt = ev.GetPosition();
        item, flags = self.tree.HitTest(pt)
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
        ev.Skip()

    def OnRightDown(self, ev=None):
        pt = ev.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item and item != self.top:
            self.tree.SelectItem(item)
            menu = wx.Menu()
            menu.Append(self.VW_EXP,"Expand All (sub)Levels")
            menu.Append(self.VW_CLP,"Collapse All (sub)Levels")
            em = wx.Menu()
            em.Append(self.EM_EDT,"Edit")
            em.AppendSeparator()
            em.Append(self.EM_CUT,"Cut")
            em.Append(self.EM_CPY,"Copy")
            em.Append(self.EM_PB,"Paste Before")
            em.Append(self.EM_PA,"Paste After")
            em.Append(self.EM_PU,"Paste Under")
            em.AppendSeparator()
            em.Append(self.EM_DEL,"Delete")
            em.Append(self.EM_IT,"Insert Text (under)")
            em.Append(self.EM_IB,'Insert Element Before')
            em.Append(self.EM_IA,'Insert Element After')
            em.Append(self.EM_IU,'Insert Element Under')
            menu.AppendMenu(-1, "Edit", em)
            hm = wx.Menu()
            hm.Append(self.HM_DTD,"Add DTD")
            hm.Append(self.HM_LNK,"Create link (under)")
            hm.Append(self.HM_IMG,"Add image (under)")
            hm.Append(self.HM_LST,"Add list (under)")
            hm.Append(self.HM_TBL,"Add table (under)")
            menu.AppendMenu(-1, "HTML", hm)
            self.PopupMenu(menu)
            ## print "klaar met menu"
            menu.Destroy()
        ## pass

    def checkselection(self):
        sel = True
        self.item = self.tree.Selection
        if self.item is None or self.item == self.top:
            wx.MessageBox('You need to select an element or text first',self.title)
            sel = False
        return sel

    def expand(self,ev=None):
        item = self.tree.Selection
        if item:
            self.tree.ExpandAllChildren(item)

    def collapse(self,ev=None):
        item = self.tree.Selection
        if item:
            self.tree.CollapseAllChildren(item)

    def edit(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemText(self.item)
        if data.startswith(ELSTART):
            attrdict = self.tree.GetItemData(self.item).GetData()
            #~ print attrdict
            edt = ElementDialog(self,title='Edit an element',tag=data,attrs=attrdict)
            if edt.ShowModal() == wx.ID_SAVE:
                tag = edt.txtTag.GetValue()
                attrs = {}
                for i in range(edt.tblAttr.GetNumberRows()):
                    attrs[edt.tblAttr.GetCellValue(i,0)] = edt.tblAttr.GetCellValue(i,1)
                if tag != data or attrs != attrdict:
                    self.tree.SetItemText(self.item,ed.getelname(tag,attrs))
                self.tree.SetPyData(self.item,attrs)
                self.tree_dirty = True
        else:
            data = self.tree.GetItemData(self.item).GetData()
            ## data = {'item': self.item, 'name': nam, 'value': val}
            edt = TextDialog(self,title='Edit Text',text=data)
            if edt.ShowModal() == wx.ID_SAVE:
                txt = edt.txtData.GetValue()
                self.tree.SetItemText(self.item,ed.getshortname(txt))
                self.tree.SetPyData(self.item,txt)
                self.tree_dirty = True
        edt.Destroy()

    def copy(self, ev=None, cut=False, retain=True):
        def push_el(el,result):
            ## print "start: ",result
            text = self.tree.GetItemText(el)
            data = self.tree.GetItemPyData(el)
            y = []
            ## print "before looping over contents:",text,y
            if text.startswith(ELSTART):
                x,c = self.tree.GetFirstChild(el)
                while x.IsOk():
                    ## print "\tbefore going down:",y
                    z = push_el(x,y)
                    ## print "\t",self.tree.GetItemText(x),z
                    ## print y
                    ## y.append(z) # geeft die ellipsis aan het eind - is blijkbaar ook niet nodig
                    ## print "\tafter going down: ",y
                    x,c = self.tree.GetNextChild(el,c)
            ## print "after  looping over contents: ",text,y
            result.append((text,data,y))
            ## print "end:  ",result
            return result
        if DESKTOP and not self.checkselection():
            return
        text = self.tree.GetItemText(self.item)
        data = self.tree.GetItemPyData(self.item)
        txt = 'cut' if cut else 'copy'
        if data == self.rt:
            wx.MessageBox("Can't %s the root" % txt,self.title)
            return
        if retain:
            if text.startswith(ELSTART):
                self.cut_el = []
                self.cut_el = push_el(self.item,self.cut_el)
                ## print "copy: get_them", self.cut_el
                self.cut_txt = None
            else:
                if data.startswith(DTDSTART):
                    if cut:
                        wx.MessageBox('The DTD cannot be *paste*d, only *add*ed from the menu','Warning',wx.ICON_INFORMATION)
                    else:
                        wx.MessageBox("You can't *copy* the DTD, only *cut* it",'Error',wx.ICON_ERROR)
                        return
                self.cut_el = None
                self.cut_txt = data
        if cut:
            self.tree.Delete(self.item)
            self.tree_dirty = True
            try:
                if self.cut_txt.startswith(DTDSTART):
                    self.hasDTD = False
            except:
                pass
        ## self.pastebeforeitem.text="Paste Before"
        ## self.pastebeforeitem.enable(True)
        ## self.pasteafteritem.text="Paste After"
        ## self.pasteafteritem.enable(True)
        ## self.pastebelowitem.text ="Paste Under"
        ## self.pastebelowitem.enable(True)

    def paste(self, ev=None,before=True,below=False):
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemPyData(self.item)
        if below and not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't paste below text",self.title)
            return
        if data == self.rt:
            if before:
                wx.MessageBox("Can't paste before the root",self.title)
                return
            else:
                wx.MessageBox("Pasting as first element below root",self.title)
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
                node = self.tree.AppendItem(self.item,item)
                self.tree.SetPyData(self.item,data)
                ## i = len(node)
            else:
                add_to = self.tree.GetItemParent(self.item)
                added = False
                x,c = self.tree.GetFirstChild(add_to)
                for i in range(self.tree.GetChildrenCount(add_to)):
                    if x == self.item:
                        if not before:
                            i += 1
                        node = self.tree.InsertItemBefore(add_to,i,item)
                        self.tree.SetPyData(node,data)
                        added = True
                        break
                    x,c = self.tree.GetNextChild(add_to,c)
                if not added:
                    node = self.tree.AppendItem(add_to,item)
                    self.tree.SetPyData(node,data)
        else:
            # I'd like to manipulate a complete treeitem (with subtree) here but I don't know how
            def zetzeronder(node,el,pos=-1):
                ## print "zetzeronder", pos
                ## print node
                ## print el
                if pos == -1:
                    subnode = self.tree.AppendItem(node,el[0])
                    self.tree.SetPyData(subnode,el[1])
                else:
                    subnode = self.tree.InsertItemBefore(node,pos,el[0])
                    self.tree.SetPyData(subnode,el[1])
                for x in el[2]:
                    zetzeronder(subnode,x)
            if below:
                node = self.item
                i = -1
            else:
                node = self.tree.GetItemParent(self.item)
                x,c = self.tree.GetFirstChild(node)
                cnt = self.tree.GetChildrenCount(node)
                for i in range(cnt):
                    if x == self.item:
                        if not before: i += 1
                        break
                    x,c = self.tree.GetNextChild(node,c)
                if i == cnt: i -= 1
            ## print "paste element"
            ## print node
            ## print self.cut_el
            zetzeronder(node,self.cut_el[0],i)
        self.tree_dirty = True

    def add_text(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = TextDialog(self,title="New Text")
        if edt.ShowModal() == wx.ID_SAVE:
            txt = edt.txtData.GetValue()
            new_item = self.tree.AppendItem(self.item,ed.getshortname(txt))
            self.tree.SetPyData(new_item,txt)
            # om te testen:
            ## text = self.tree.GetItemText(new_item)
            ## data = self.tree.GetItemPyData(new_item)
            ## print text,data
            self.tree_dirty = True
        edt.Destroy()

    def insert(self, ev=None,before=True,below=False):
        if DESKTOP and not self.checkselection():
            return
        edt = ElementDialog(self,title="New element")
        if edt.ShowModal() == wx.ID_SAVE:
            tag = edt.txtTag.GetValue()
            attrs = {}
            for i in range(edt.tblAttr.GetNumberRows()):
                attrs[edt.tblAttr.GetCellValue(i,0)] = edt.tblAttr.GetCellValue(i,1)
            data = attrs
            text = ed.getelname(tag,data)
            if below:
                self.tree.AppendItem(self.item,text)
                self.tree.SetPyData(self.item,data)
            else:
                parent = self.tree.GetItemParent(self.item)
                item = self.item if not before else self.tree.GetPrevSibling(self.item)
                node = self.tree.InsertItem(parent,item,text)
                self.tree.SetPyData(node,data)
            self.tree_dirty = True
        edt.Destroy()

    def add_dtd(self,ev=None):
        edt = DTDDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            for cap,dtd,rb in edt.rbgDTD:
                h = rb.GetValue()
                if h:
                    rr = self.tree.InsertItemBefore(self.top,0,ed.getshortname(dtd))
                    self.tree.SetPyData(rr,dtd)
                    self.hasDTD = True
                    self.tree_dirty = True
                    break
        edt.Destroy()

    def add_link(self,ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = LinkDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            self.data = {
                "href": edt.link,
                "title": edt.txtTitle.GetValue()
                }
            rr = self.tree.AppendItem(self.item,'<> a')
            self.tree.SetPyData(rr,self.data)
            self.tree_dirty = True
        edt.Destroy()

    def add_image(self,ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = ImageDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            self.data = {
                "src": edt.link,
                "alt": edt.txtAlt.GetValue(),
                "title": edt.txtTitle.GetValue()
                }
            rr = self.tree.AppendItem(self.item,'<> img')
            self.tree.SetPyData(rr,self.data)
            self.tree_dirty = True
        edt.Destroy()

    def add_list(self,ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = ListDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            self.data = {}
            type = edt.cmbType.GetValue()[0] + "l"
            itemtype = "dt" if type == "dl" else "li"
            new_item = self.tree.AppendItem(self.item,' '.join((ELSTART,type)))

            for row in range(edt.tblList.GetNumberRows()):
                new_data = self.tree.AppendItem(new_item,' '.join((ELSTART,itemtype)))
                data = edt.tblList.GetCellValue(row,0)
                rr = self.tree.AppendItem(new_data,ed.getshortname(data))
                self.tree.SetPyData(rr,data)
                if type == "dl":
                    new_data = self.tree.AppendItem(new_item,'<> dd')
                    data = edt.tblList.GetCellValue(row,1)
                    rr = self.tree.AppendItem(new_data,ed.getshortname(data))
                    self.tree.SetPyData(rr,data)

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

    def add_table(self,ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = TableDialog(self)
        if edt.ShowModal() == wx.ID_SAVE:
            cols = edt.tblTable.GetNumberCols() #int(edt.txtCols.GetValue())
            rows = edt.tblTable.GetNumberRows() #int(edt.txtRows.GetValue())
            new_item = self.tree.AppendItem(self.item,'<> table')
            new_row = self.tree.AppendItem(new_item,'<> tr')
            for col in range(cols):
                new_head = self.tree.AppendItem(new_row,'<> th')
                # try:
                head = edt.tblTable.GetColLabelValue(col) # edt.headings[col]
                # except IndexError:
                if not head:
                    rr = self.tree.AppendItem(new_head,BL)
                    self.tree.SetPyData(rr,BL)
                else:
                    rr = self.tree.AppendItem(new_head,ed.getshortname(head))
                    self.tree.SetPyData(rr,head)
            for row in range(rows):
                new_row = self.tree.AppendItem(new_item,'<> tr')
                for col in range(cols):
                    new_cell = self.tree.AppendItem(new_row,'<> td')
                    text = edt.tblTable.GetCellValue(row,col)
                    rr = self.tree.AppendItem(new_cell,ed.getshortname(text)) # BL)
                    self.tree.SetPyData(rr, text) # BL)
            self.tree_dirty = True
        edt.Destroy()

class MainGui(object):
    def __init__(self,args):
        app = wx.App(redirect=True,filename="ashe.log")
        if len(args) > 1:
            frm = MainFrame(None, -1, fn=args[1])
        else:
            frm = MainFrame(None, -1)
        app.MainLoop()

if __name__ == "__main__":
    print sys.argv
    MainGui(sys.argv)
