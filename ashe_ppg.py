import os,sys,shutil,copy
import BeautifulSoup as bs
ELSTART = '<>'
DTDSTART = "<!DOCTYPE"
BL = "&nbsp;"
TITEL = "Albert's Simple HTML-editor"
HMASK = "HTML files (*.htm,*.html)|*.htm;*.html|All files (*.*)|*.*"
IMASK = "All files|*.*"

import ashe_mixin as ed
todo = """\
Bij saven volgt het volgende:
Traceback (most recent call last):
  File "\loewis\25\python\Modules\_ctypes\callbacks.c", line 206, in 'calling callback function'
  File "C:\Python25\lib\site-packages\ppygui\core.py", line 220, in globalWndProc
    handled, result = dispatcher.dispatch(hWnd, nMsg, wParam, lParam)
  File "C:\Python25\lib\site-packages\ppygui\core.py", line 469, in dispatch
    res = self.callback(event)
  File "ppygui_editor.py", line 663, in savexml
    self.savexmlas()
  File "ppygui_editor.py", line 671, in savexmlas
    self.savexmlfile(saveas=True)
  File "ppygui_editor.py", line 748, in savexmlfile
    expandnode(tag,root)
  File "ppygui_editor.py", line 731, in expandnode
    expandnode(el,sub)
  File "ppygui_editor.py", line 731, in expandnode
    expandnode(el,sub)
  File "ppygui_editor.py", line 725, in expandnode
    for att,val in dic:
TypeError: 'NoneType' object is not iterable
"""

if os.name == 'ce':
    import ppygui as gui
    DESKTOP = False
else:
    import ppygui.api as gui
    DESKTOP = True

class PreviewDialog(gui.Dialog):
    def __init__(self,data):
        print data
        gui.Dialog.__init__(self,title="Preview",action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        self.html = gui.Html(self) #, zoom_level = 0)
        self.bclose = gui.Button(self, "Quit")
        self.bclose.bind(clicked=self.on_cancel)
        self.html.value = data
        sizer = gui.VBox(border=(5,5,5,5))
        sizer.add(self.html, 1)
        sizer2 = gui.HBox(spacing=5)
        #sizer2.add(gui.Spacer(0, 0), 1)
        #sizer2.add(self.bopen, 1)
        sizer2.add(self.bclose, 1)
        sizer.add(sizer2)
        self.sizer = sizer

    def on_cancel(self,ev=None):
        self.end('cancel')

class DTDDialog(gui.Dialog):
    def __init__(self):
        gui.Dialog.__init__(self,title="Add DTD",action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        self.rbgDTD = gui.RadioGroup()
        vsizer = gui.VBox(border=(15,15,15,15))
        hsizer = gui.HBox()
        lblLink = gui.Label(self, "Select document type:")
        hsizer.add(lblLink)
        vsizer.add(hsizer)
        spc = gui.Spacer(y=5)
        vsizer.add(spc)
        hsizer = gui.HBox()
        spc = gui.Spacer(x=20)
        hsizer.add(spc)
        vsizer2 = gui.VBox()
        self.rbH41S = gui.RadioButton(self,title='HTML 4.1 Strict',
            value = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
            group=self.rbgDTD)
        self.rbH41T = gui.RadioButton(self,title='HTML 4.1 Transitional',
            value = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
            group=self.rbgDTD)
        self.rbH41F = gui.RadioButton(self,title='HTML 4.1 Frameset',
            value = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">',
            group=self.rbgDTD)
        vsizer2.add(self.rbH41S)
        vsizer2.add(self.rbH41T)
        vsizer2.add(self.rbH41F)
        hsizer.add(vsizer2)
        vsizer.add(hsizer)
        spc = gui.Spacer(y=10)
        vsizer.add(spc)
        hsizer = gui.HBox()
        spc = gui.Spacer(x=20)
        hsizer.add(spc)
        vsizer2 = gui.VBox()
        self.rbX10S = gui.RadioButton(self,title='XHTML 1.0 Strict',
            value = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
            group=self.rbgDTD)
        self.rbX10T = gui.RadioButton(self,title='XHTML 1.0 Transitional',
            value = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
            group=self.rbgDTD)
        self.rbX10F = gui.RadioButton(self,title='XHTML 1.0 Frameset',
            value = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">',
            group=self.rbgDTD)
        vsizer2.add(self.rbX10S)
        vsizer2.add(self.rbX10T)
        vsizer2.add(self.rbX10F)
        hsizer.add(vsizer2)
        vsizer.add(hsizer)
        spc = gui.Spacer()
        vsizer.add(spc)
        hsizer = gui.HBox()
        self.bOk = gui.Button(self,title='Save',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        vsizer.add(hsizer)
        self.sizer = vsizer

    def on_ok(self,ev=None):
        self._parent.data = {"dtd": self.rbgDTD.value}
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')

class LinkDialog(gui.Dialog):
    def __init__(self):
        gui.Dialog.__init__(self,title='Add Link',action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        vsizer = gui.VBox(border=(15,15,15,15))

        hsizer = gui.HBox()
        lblLink = gui.Label(self, "link to document:")
        hsizer.add(lblLink)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        spc = gui.Spacer(x=20,y=-1)
        self.txtLink = gui.Edit(self)
        self.bKies = gui.Button(self,title='Search',action=self.kies)
        hsizer.add(spc)
        hsizer.add(self.txtLink)
        hsizer.add(self.bKies)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        lblTitle = gui.Label(self, "descriptive title:")
        hsizer.add(lblTitle)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        spc = gui.Spacer(x=20,y=-1)
        self.txtTitle = gui.Edit(self)
        hsizer.add(spc)
        hsizer.add(self.txtTitle)
        vsizer.add(hsizer)

        spc = gui.Spacer(x=-1,y=5)
        vsizer.add(spc)

        hsizer = gui.HBox()
        self.bOk = gui.Button(self,title='Save',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        vsizer.add(hsizer)

        self.sizer = vsizer

    def kies(self,ev=None):
        h = gui.FileDialog.open(wildcards={"HTML files (*.html,*.htm)": "*.html;*.htm"})
        if h:
            self.txtLink.set_text(h)

    def on_ok(self,ev=None):
        link = self.txtLink.get_text()
        if not link:
            gui.Message.ok("","link opgeven of cancel kiezen s.v.p")
            return
        self._parent.data = {
            "href": link,
            "title": self.txtTitle.get_text()
            }
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')

class ImageDialog(gui.Dialog):
    def __init__(self):
        gui.Dialog.__init__(self,title='Add Image',action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        vsizer = gui.VBox(border=(15,15,15,15))

        hsizer = gui.HBox()
        lblLink = gui.Label(self, "link to image:")
        hsizer.add(lblLink)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        spc = gui.Spacer(x=20,y=-1)
        self.txtLink = gui.Edit(self)
        self.bKies = gui.Button(self,title='Search',action=self.kies)
        hsizer.add(spc)
        hsizer.add(self.txtLink)
        hsizer.add(self.bKies)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        lblTitle = gui.Label(self, "descriptive title:")
        hsizer.add(lblTitle)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        spc = gui.Spacer(x=20,y=-1)
        self.txtTitle = gui.Edit(self)
        hsizer.add(spc)
        hsizer.add(self.txtTitle)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        lblAlt = gui.Label(self, "alternate text:")
        hsizer.add(lblAlt)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        spc = gui.Spacer(x=20,y=-1)
        self.txtAlt = gui.Edit(self)
        hsizer.add(spc)
        hsizer.add(self.txtAlt)
        vsizer.add(hsizer)

        spc = gui.Spacer(x=-1,y=5)
        vsizer.add(spc)

        hsizer = gui.HBox()
        self.bOk = gui.Button(self,title='Save',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        vsizer.add(hsizer)

        self.sizer = vsizer

    def kies(self,ev=None):
        h = gui.FileDialog.open(wildcards={"all files": "*.*"}) #  {"image files": "*.html"})
        if h:
            self.txtLink.set_text(h)

    def on_ok(self,ev=None):
        link = self.txtLink.get_text()# probeer het opgegeven pad relatief te maken t.o.v. het huidige
        if not link:
            gui.Message.ok("","link opgeven of cancel kiezen s.v.p")
            return
        self._parent.data = {
            "src": link,
            "alt": self.txtAlt.get_text(),
            "title": self.txtTitle.get_text()
            }
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')

class ListDialog(gui.Dialog):
    def __init__(self):
        gui.Dialog.__init__(self,title='Add List',action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        self.items = []
        self.dataitems = []
        vsizer = gui.VBox(border=(15,15,15,15))

        tsizer = gui.TBox(2,2,border=(2,2,20,2),spacing_x=2,spacing_y=2)
        lblType = gui.Label(self, "choose type of list:")
        self.cmbType = gui.Combo(self,style="list",choices=[
            "unordered",
            "ordered",
            "definition",
            ])
        self.cmbType.selection = 0
        self.cmbType.bind(selchanged=self.on_type)
        tsizer.add(lblType)
        tsizer.add(self.cmbType)

        lblNr = gui.Label(self, "initial number of items:")
        hsizer = gui.HBox()
        ## self.txtNr = gui.Edit(self,style="number")
        self.txtNr = gui.Spin(self,value=1)
        self.txtNr.bind(update=self.on_ud)
        ## spc = gui.Spacer(x=20,y=-1)
        tsizer.add(lblNr)
        hsizer.add(self.txtNr)
        ## hsizer.add(spc)
        tsizer.add(hsizer)
        vsizer.add(tsizer)

        spc = gui.Spacer(x=-1,y=5)
        vsizer.add(spc)

        hsizer = gui.HBox()
        lblText = gui.Label(self, "enter text for list item:")
        hsizer.add(lblText)
        vsizer.add(hsizer)

        hsizer = gui.HBox(spacing=2)
        ## spc = gui.Spacer(x=20,y=-1)
        self.txtText = gui.Edit(self,pos=(-1,-1,5,-1))
        self.txtData = gui.Edit(self)
        ## hsizer.add(spc)
        hsizer.add(self.txtText,1)
        hsizer.add(self.txtData,4)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        self.bNext = gui.Button(self,title='Next item',action=self.on_next)
        hsizer.add(self.bNext)
        vsizer.add(hsizer)

        spc = gui.Spacer(x=-1,y=5)
        vsizer.add(spc)

        hsizer = gui.HBox()
        self.lbList = gui.List(self)
        ## self.tblList.columns.set(0,width=160)
        hsizer.add(self.lbList)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        self.bOk = gui.Button(self,title='Save',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        vsizer.add(hsizer)

        self.sizer = vsizer
        self.txtText.hide()

    def on_ud(self,ev=None):
        print self.txtNr.value,
        print self.txtNr.get_value(),
        print self.txtNr._ud._get_pos(),
        self.txtNr._buddy.select_all()
        print self.txtNr._buddy.selected_text

    def on_type(self,ev=None):
        s = self.cmbType.get_text()
        if s[0] == "d":
            self.txtText.show()
        else:
            self.txtText.hide()
        self.update()

    def on_next(self,ev=None):
        text = self.txtData.get_text()
        if self.cmbType.get_text()[0] == "d":
            text = ": ".join((self.txtText.get_text(),text))
        self.lbList.append(text)
        if self.lbList.count == self.txtNr.value: # int(self.txtNr.get_text()):
            gui.Message.ok('','No more items available')
            self.bNext.disable()

    def on_ok(self,ev=None):
        self._parent.data = {}
        type = self.cmbType.get_text()[0] + "l"
        self._parent.data['type'] = type
        self._parent.data['type'] = type
        if type == "dl":
            self._parent.data['itemtype'] = "dt"
            self._parent.data['datatype'] = "dd"
            self._parent.data["items"] = []
            self._parent.data["dataitems"] = []
            for x in self.lbList:
                txt = x.split(": ")
                self._parent.data["items"].append(txt[0])
                self._parent.data["dataitems"].append(txt[1])
        else:
            self._parent.data['itemtype'] = "li"
            self._parent.data["items"] = [x for x in self.lbList]
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')

class TableDialog(gui.Dialog):
    def __init__(self):
        gui.Dialog.__init__(self,title='Add Table',action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        self.headings = []
        vsizer = gui.VBox(border=(15,15,15,15))

        tsizer = gui.TBox(2,2,border=(2,2,20,2),spacing_x=2,spacing_y=2)
        lblRows = gui.Label(self, "initial number of rows:")
        self.txtRows = gui.Spin(self,value=1)
        tsizer.add(lblRows)
        tsizer.add(self.txtRows)

        lblCols = gui.Label(self, "initial number of columns:")
        self.txtCols = gui.Spin(self,value=1)
        tsizer.add(lblCols)
        tsizer.add(self.txtCols)
        vsizer.add(tsizer)

        spc = gui.Spacer(x=-1,y=5)
        vsizer.add(spc)

        hsizer = gui.HBox()
        lblHead = gui.Label(self, "enter text for column heading:")
        hsizer.add(lblHead)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        ## spc = gui.Spacer(x=20,y=-1)
        self.txtHead = gui.Edit(self)
        ## hsizer.add(spc)
        hsizer.add(self.txtHead)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        self.bNext = gui.Button(self,title='Next heading',action=self.on_next)
        hsizer.add(self.bNext)
        vsizer.add(hsizer)

        spc = gui.Spacer(x=-1,y=5)
        vsizer.add(spc)

        hsizer = gui.HBox()
        self.lbHeadings = gui.List(self)
        ## self.tblList.columns.set(0,width=160)
        hsizer.add(self.lbHeadings)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        self.bOk = gui.Button(self,title='Save',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        vsizer.add(hsizer)

        self.sizer = vsizer

    def on_next(self,ev=None):
        self.lbHeadings.append(self.txtHead.get_text())
        if self.lbHeadings.count == self.txtCols.value:
            gui.Message.ok('','No more headings available')
            self.bNext.disable()

    def on_ok(self,ev=None):
        self.headings = []
        self._parent.data = {
            "cols": int(self.txtCols.value),
            "rows": int(self.txtRows.value),
            "head": [x for x in self.lbHeadings]
        }
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')


class ElementDialog(gui.Dialog):
    def __init__(self,title='',tag=None,attrs=None):
        gui.Dialog.__init__(self,title,action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        vsizer = gui.VBox()
        hsizer = gui.HBox()
        lblName = gui.Label(self, "element name:")
        self.txtTag = gui.Edit(self)
        if tag:
            ## self.txtTag.text=tag[3:] # dit komt uit versie 2_4
            self.txtTag.text=tag.split()[1] # dit was de verbetering(?) hier
            ## self.txtTag.readonly=True
        hsizer.add(lblName)
        hsizer.add(self.txtTag)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        vsizer2 = gui.VBox(border=(2,2,2,2))
        hsizer2 = gui.HBox()
        tbl = gui.Table(self,columns=['attribute','value'])
        tbl.columns.set(1,width=160)
        if attrs:
            self.row = 0
            for attr,value in attrs.items():
                tbl.rows.append([attr,value])
        else:
            self.row = -1
        tbl.bind(selchanged=self.on_sel)
        self.tblAttr = tbl
        hsizer2.add(self.tblAttr)
        vsizer2.add(hsizer2)
        hsizer2 = gui.HBox()
        self.bEdit = gui.Button(self,title='Edit selected',action=self.on_edit)
        self.bDel = gui.Button(self,title='Delete selected',action=self.on_del)
        hsizer2.add(self.bEdit)
        hsizer2.add(self.bDel)
        vsizer2.add(hsizer2)
        hsizer.add(vsizer2)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        vsizer2 = gui.VBox(border=(2,2,2,2))
        hsizer2 = gui.HBox()
        lblAttnam = gui.Label(self, "Attribute name:")
        self.txtAttnam = gui.Edit(self)
        hsizer2.add(lblAttnam)
        hsizer2.add(self.txtAttnam)
        vsizer2.add(hsizer2)
        hsizer2 = gui.HBox()
        lblAttval = gui.Label(self, "Attribute value:")
        self.txtAttval = gui.Edit(self)
        hsizer2.add(lblAttval)
        hsizer2.add(self.txtAttval)
        vsizer2.add(hsizer2)
        hsizer2 = gui.HBox()
        self.bAttOk = gui.Button(self,title='Add/Apply Edit',action=self.on_attok)
        hsizer2.add(self.bAttOk)
        vsizer2.add(hsizer2)
        hsizer.add(vsizer2)
        vsizer.add(hsizer)

        hsizer = gui.HBox()
        self.bOk = gui.Button(self,title='Save',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        vsizer.add(hsizer)

        self.sizer = vsizer

    def on_sel(self,ev):
        self.row = ev.get_index()

    def on_edit(self,ev=None):
        if self.row >= 0:
            self.txtAttnam.set_text(self.tblAttr[self.row,0])
            self.txtAttval.set_text(self.tblAttr[self.row,1])

    def on_del(self,ev=None):
        if self.row >= 0:
            self.tblAttr.rows.__delitem__(self.row)

    def on_attok(self,ev=None):
        # voeg toe/wijzig de geselecteerde regel i de tabel
        nam = self.txtAttnam.get_text()
        val = self.txtAttval.get_text()
        done = False
        for x in range(len(self.tblAttr.rows)):
            if self.tblAttr[x,0] == nam:
                self.tblAttr[x,1] = val
                done = True
                break
        if not done:
            self.tblAttr.rows.append([nam,val])

    def on_ok(self,ev=None):
        self._parent.data = {}
        self._parent.data['tag'] = self.txtTag.get_text()
        attrs = {}
        for x in range(len(self.tblAttr.rows)):
            attrs[self.tblAttr[x,0]] = self.tblAttr[x,1]
        self._parent.data['attrs'] = attrs
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')


class TextDialog(gui.Dialog):
    def __init__(self,title='',text=None):
        if text is None:
            text = ''
        gui.Dialog.__init__(self,title,action=("Cancel", self.on_cancel))
        self.sippref = gui.SIPPref(self)
        vsizer = gui.VBox()
        hsizer = gui.HBox()
        self.txtData = gui.Edit(self,text=text, multiline=True, line_wrap=True)
        hsizer.add(self.txtData)
        vsizer.add(hsizer)
        hsizer = gui.HBox()
        self.bOk = gui.Button(self,title='Ok',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        vsizer.add(hsizer)
        self.sizer = vsizer

    def on_ok(self,ev=None):
        self._parent.data = {}
        self.txtData.select_all()
        self._parent.data = self.txtData.selected_text
        self.end('ok')

    def on_cancel(self,ev=None):
        self.end('cancel')

class MainFrame(gui.CeFrame,ed.editormixin):
    def __init__(self,fn=''):
        self.title = "Albert's Simple HTML Editor"
        gui.CeFrame.__init__(self,
            title=self.title,
            action=("About", self.about),
            menu="Menu"
            )
        self.xmlfn = fn
        self.sipp = gui.SIPPref(self)
        self.tree = gui.Tree(self)

        self.filemenu = gui.PopupMenu()
        self.filemenu.append("New",callback=self.newxml)
        self.filemenu.append("Open",callback=self.openxml)
        self.filemenu.append('Save', callback = self.savexml)
        self.filemenu.append('Save As', callback = self.savexmlas)
        self.filemenu.append_separator()
        self.filemenu.append('Preview', callback = self.preview)
        self.filemenu.append_separator()
        self.filemenu.append('Exit', callback = self.quit)
        self.viewmenu = gui.PopupMenu()
        self.viewmenu.append("Expand All (sub)Levels", callback = self.expand)
        self.viewmenu.append("Collapse All (sub)Levels", callback = self.collapse)
        self.editmenu = gui.PopupMenu()
        self.editmenu.append("Edit", callback = self.edit)
        self.editmenu.append_separator()
        self.editmenu.append("Cut", callback = self.cut)
        self.editmenu.append("Copy", callback = self.copy)
        self.pastebeforeitem = self.editmenu.append("Paste Before", callback = self.paste)
        self.pasteafteritem = self.editmenu.append("Paste After", callback = self.paste_aft)
        self.pastebelowitem = self.editmenu.append("Paste Under", callback = self.paste_blw)
        self.editmenu.append_separator()
        self.editmenu.append("Insert Text (under)",callback=self.add_text)
        self.editmenu.append('Insert Element Before', callback=self.insert)
        self.editmenu.append('Insert Element After', callback=self.ins_aft)
        self.editmenu.append('Insert Element Under', callback=self.ins_chld)
        self.pastebeforeitem.title = "Nothing to Paste"
        self.pastebeforeitem.enable(False)
        self.pasteafteritem.title = " "
        self.pasteafteritem.enable(False)
        self.pastebelowitem.title = " "
        self.pastebelowitem.enable(False)
        ## self.helpmenu.append('About', callback = self.about)
        self.htmlmenu = gui.PopupMenu()
        self.dtdmenu = self.htmlmenu.append("Add DTD",callback=self.add_dtd)
        self.htmlmenu.append("Create link (under)",callback=self.add_link)
        self.htmlmenu.append("Add image (under)",callback=self.add_image)
        self.htmlmenu.append("Add list (under)",callback=self.add_list)
        self.htmlmenu.append("Add table (under)",callback=self.add_table)
        sizer = gui.VBox(border=(2,2,2,2), spacing=2)
        sizer.add(self.tree)
        self.sizer = sizer

        ed.editormixin.init_fn(self)

        # context menu doesn't work in PC version, cb_menu doesn't in WM2003
        if DESKTOP:
            self.cb_menu.append_menu("Document",self.filemenu)
            self.cb_menu.append_menu("View",self.viewmenu)
            self.cb_menu.append_menu("Edit",self.editmenu)
            self.cb_menu.append_menu("Html",self.htmlmenu)
        else:
            self.tree.bind(lbdown=self.on_bdown)
            self.editmenu.append_menu("View",self.viewmenu)
            self.editmenu.append_menu("Html",self.htmlmenu)

    def quit(self,ev=None):
        self.destroy()

    def preview(self,ev=None):
        self.maakhtml()
        edt = PreviewDialog(self.bs)
        edt.popup(self)

    def savexmlas(self,ev=None):
        h = gui.FileDialog.save(filename=self.xmlfn,wildcards={"HTML files": "*.html"})
        if h is not None:
            self.xmlfn = h
            self.savexmlfile(saveas=True)
            self.tree.roots[0].text = self.xmlfn

    def about(self,ev=None):
        ed.editormixin.about(self)
        gui.Message.ok(self.title,self.abouttext)

    def openfile(self):
        h = gui.FileDialog.open(wildcards={"HTML files": "*.html"})
        if h:
            if not ed.editormixin.openfile(self,h):
                h = gui.Message.ok(self.title,'html parsing error')

    def addtreeitem(self,node,naam,data):
        return node.append(naam,data)

    def addtreetop(self,fn,titel):
        self.title = titel
        self.top = self.tree.add_root(fn)

    def init_tree(self,name=''):
        self.tree.delete_all()
        ed.editormixin.init_tree(self,name)

    def savexmlfile(self,saveas=False):
        if not saveas:
            try:
                shutil.copyfile(self.xmlfn,self.xmlfn + '.bak')
            except IOError,mld:
                gui.msgBox(self,title,mld)
        self.maakhtml()
        f = open(self.xmlfn,"w")
        f.write(str(self.bs))
        f.close()

    def maakhtml(self):
        def expandnode(node,root):
            print node.get_text()
            try:
                for att in node.data:
                    root[att] = node.data[att] # val # TypeError: list indices must be integers
                ## dic = node.get_data() # versie 2.4a
            except TypeError:
                pass
            ## else:
                ## for att in dic: # verstie 2.4a
                    ## root[att] = dic[att] # versie 2.4a
                ## ## for att,val in dic: # vanuit verste 2.4
                    ## ## root[att] = val # vanuit versie 2.4
            for el in reversed(node):
                text = el.text
                data = el.data
                if text.startswith(ELSTART):
                ## if el.text.startswith(ELSTART): versie 2.4a
                    sub = bs.Tag(self.bs,el.text.split()[1])
                    root.insert(0,sub)
                    expandnode(el,sub)
                else:
                    # dit levert fouten op bij het gebruiken van diacrieten
                    ## sub = bs.NavigableString(escape(data))
                    ## root.insert(0,sub)
                    # dit niet maar er wordt niet correct gecodeerd
                    ## root.insert(0,escape(data))
                    # misschien dat dit het doet
                    sub = bs.NavigableString(data.decode("latin-1"))
                    root.insert(0,data.decode("latin-1")) # sub)
                    ## sub = bs.NavigableString(el.data) # versie 2.4a
                    ## root.insert(0,sub) # versie 2.4a
        self.bs = bs.BeautifulSoup()
        for tag in self.tree.roots[0]:
            if not tag.text.startswith(ELSTART):
                sub = bs.Declaration(tag.data)
            else:
                root = bs.Tag(self.bs, tag.text.split(None,1)[1])
                self.bs.insert(0,root)
                expandnode(tag,root)

    def on_bdown(self, ev=None):
        if gui.recon_context(self.tree, ev):
            self.item = self.tree.selection
            if self.item == self.top:
                gui.context_menu(self, ev, self.filemenu)
            elif self.item is not None:
                gui.context_menu(self, ev, self.editmenu)
            else:
                gui.Message.ok(self.title,'You need to select a tree item first')
                #menu.append()
        else:
            ev.skip()

    def checkselection(self):
        sel = True
        self.item = self.tree.selection
        if self.item is None or self.item == self.top:
            gui.Message.ok(self.title,'You need to select an element or text first')
        return sel

    def expand(self,ev=None):
        def expand_sub(node):
            node.expand()
            for sub in node:
                expand_sub(sub)
        sel = self.tree.selection
        if not sel:
            expand_sub(self.top)
        else:
            expand_sub(sel)

    def collapse(self,ev=None):
        def collapse_sub(node):
            for sub in node:
                collapse_sub(sub)
            node.collapse()
        sel = self.tree.selection
        if not sel:
            collapse_sub(self.top)
        else:
            collapse_sub(sel)

    def edit(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        data = self.item.get_text()
        if data.startswith(ELSTART):
            attrdict = self.item.get_data()
            edt = ElementDialog(title='Edit an element',tag=data,attrs=attrdict)
            if edt.popup(self) == 'ok':
                if self.data["tag"] != data:
                    self.item.set_text(getelname(self.data["tag"],self.data["attrs"]))
                print self.data["attrs"]
                self.item.set_data(self.data["attrs"])
        else:
            data = self.item.get_data()
            ## data = {'item': self.item, 'name': nam, 'value': val}
            edt = TextDialog(title='Edit Text',text=data)
            if edt.popup(self) == 'ok':
                self.item.set_text(getshortname(self.data))
                self.item.set_data(self.data)

    def copy(self, ev=None, cut=False):
        def push_el(el,result):
            text = el.get_text()
            data = el.get_data()
            y = []
            if text.startswith(ELSTART):
                for x in el:
                    y = push_el(x,y)
            result.append((text,data,y))
            return result
        if DESKTOP and not self.checkselection():
            return
        text = self.item.get_text()
        data = self.item.get_data()
        try:
            if data.startswith(DTDSTART):
                if cut:
                    gui.Message.ok(self.title,'The DTD cannot be *paste*d, only *add*ed from the menu')
                else:
                    gui.Message.ok(self.title,"You can't *copy* the DTD, only *cut* it")
                    return
        except:
            pass
        txt = 'cut' if cut else 'copy'
        if data == self.rt:
            gui.Message.ok(self.title,"Can't %s the root" % txt)
            return
        if text.startswith(ELSTART):
            self.cut_el = []
            self.cut_el = push_el(self.item,self.cut_el)
            #print "copy: get_them", self.cut_el
            self.cut_txt = None
        else:
            self.cut_el = None
            self.cut_txt = data
        if cut:
            self.item.remove()
            try:
                if self.cut_txt.startswith(DTDSTART):
                    self.hasDTD = False
            except:
                pass
        self.pastebeforeitem.text="Paste Before"
        self.pastebeforeitem.enable(True)
        self.pasteafteritem.text="Paste After"
        self.pasteafteritem.enable(True)
        self.pastebelowitem.text ="Paste Under"
        self.pastebelowitem.enable(True)

    def paste(self, ev=None,before=True,below=False):
        if DESKTOP and not self.checkselection():
            return
        data = self.item.get_data()
        if below and not self.item.get_text().startswith(ELSTART):
            gui.Message.ok(self.title,"Can't paste below text")
            return
        if data == self.rt:
            if before:
                gui.Message.ok(self.title,"Can't paste before the root")
                return
            else:
                gui.Message.ok(self.title,"Pasting as first element below root")
                below = True
        #if self.cut:
        #    self.pastebeforeitem.set_text = "Nothing to Paste"
        #    self.pastebeforeitem.enable(False)
        #    self.pasteafteritem.set_text = " "
        #    self.pasteafteritem.enable(False)
        #    self.pastebelowitem.set_text = " "
        #    self.pastebelowitem.enable(False)
        if self.cut_txt:
            item = getshortname(self.cut_txt)
            data = self.cut_txt
            if below:
                node = self.item.append(item,data)
                i = len(node)
            else:
                add_to = self.item.get_parent()
                added = False
                for i,x in enumerate(add_to):
                    if x == self.item:
                        if not before:
                            i += 1
                        node = add_to.insert(i,item,data)
                        added = True
                        break
                if not added:
                    node = add_to.append(item,data)
        else:
            # I'd like to manipulate a complete treeitem (with subtree) here but I don't know how
            def zetzeronder(node,el,pos=-1):
                if pos == -1:
                    subnode = node.append(el[0],el[1])
                else:
                    subnode = node.insert(i,el[0],el[1])
                for x in el[2]:
                    zetzeronder(subnode,x)
            if below:
                node = self.item
                i = -1
            else:
                node = self.item.get_parent()
                for i,x in enumerate(node):
                    if x == self.item:
                        if not before: i += 1
                        break
                if i > len(node): i = -1
            zetzeronder(node,self.cut_el[0],i)

    def add_text(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = TextDialog("New Text")
        if edt.popup(self) == 'ok':
            self.item.append(getshortname(self.data),self.data)

    def insert(self, ev=None,before=True,below=False):
        if DESKTOP and not self.checkselection():
            return
        current = self.item
        parent = self.item.get_parent()
        edt = ElementDialog("New element")
        if edt.popup(self) == 'ok':
            data = self.data['attrs']
            text = getelname(self.data['tag'],data)
            if below:
                current.append(text,data)
            else:
                for i,x in enumerate(parent):
                    print i,x,x.get_text()
                    if x == self.item:
                        i = i if before else i+1
                        print i
                        parent.insert(i,text,data)
                        break

    def add_dtd(self,ev=None):
        edt = DTDDialog()
        if edt.popup(self) == 'ok':
            dtd = self.data["dtd"]
            self.top.insert(0,getshortname(dtd),data=dtd)
            self.hasDTD = True

    def add_link(self,ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = LinkDialog()
        if edt.popup(self) == 'ok':
            self.data["href"] = getrelativepath(self.data["href"],self.xmlfn),
            self.item.append('<> a',data=self.data) #.items())

    def add_image(self,ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = ImageDialog()
        if edt.popup(self) == 'ok':
            self.data["src"] = getrelativepath(self.data["src"],self.xmlfn),
            self.item.append('<> img',data=self.data) #.items())

    def add_list(self,ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = ListDialog()
        if edt.popup(self) == 'ok':
            new_item = self.item.append('<> ' + self.data['type'])
            for i,data in enumerate(self.data["items"]):
                new_data = new_item.append('<> ' + self.data['itemtype'])
                new_data.append(getshortname(data),data=data)
                if "datatype" in self.data:
                    new_data = new_item.append('<> ' + self.data['datatype'])
                    text = self.data["dataitems"][i]
                    new_data.append(getshortname(text),data=text)

    def add_table(self,ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = TableDialog()
        if edt.popup(self) == 'ok':
            new_item = self.item.append('<> table')
            if "head" in self.data:
                new_row = new_item.append('<> tr')
                for row in range(self.data["cols"]):
                    new_head = new_row.append('<> th')
                    try:
                        head = self.data["head"][row]
                    except IndexError:
                        new_head.append(BL,data=BL)
                    else:
                        new_head.append(getshortname(head),data=head)
            for row in range(self.data["rows"]):
                new_row = new_item.append('<> tr')
                for col in range(self.data["cols"]):
                    new_cell = new_row.append('<> td')
                    new_cell.append(BL,data=BL)

class MainGui(object):
    def __init__(self,args):
        if len(args) > 1:
            app = gui.Application(MainFrame(args[1]))
        else:
            app = gui.Application(MainFrame())
        app.run()

if __name__ == "__main__":
    ## print getelname("a",{"name": 'Hello', "snork": "hahaha"})
    ## print getshortname("Hee hallo")
    x = MainGui(sys.argv)
