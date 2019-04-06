"""wxPython versie van mijn op een treeview gebaseerde HTML-editor

custom dialogen
"""
import os
## import sys
import string
import pathlib
import wx
import wx.grid as wxgrid
# import wx.html as html
# from wx.lib.dialogs import ScrolledMessageDialog
from ashe.constants import CMSTART, ELSTART
try:
    import cssedit.editor.csseditor_qt as csed
    cssedit_available = True
except ImportError:
    cssedit_available = False

IMASK = "All files (*.*)|*.*"
if os.name == "nt":
    HMASK = "HTML files (*.htm,*.html)|*.htm;*.html|" + IMASK
    CMASK = "CSS files (*.css)|*.css|" + IMASK
elif os.name == "posix":
    HMASK = "HTML files (*.htm,*.HTM,*.html,*.HTML)|*.htm;*.HTM;*.html;*.HTML|" + IMASK
    CMASK = "CSS files (*.css,*.CSS)|*.css;*.CSS|" + IMASK


class ElementDialog(wx.Dialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, parent, title='', tag=None, attrs=None):
        self._parent = parent
        super().__init__(parent, -1, title=title,
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label="element name:")
        self.tag_text = wx.TextCtrl(self, size=(150, -1))
        self.tag_text.setMinimumWidth(250)
        self.comment_button = wx.CheckBox(self, label='&Comment(ed)')
        is_style_tag = self.is_stylesheet = has_style = False
        self.styledata = self.old_styledata = ''
        iscomment = False
        if tag:
            x = tag.split(None, 1)
            if x[0] == CMSTART:
                iscomment = True
                x = x[1].split(None, 1)
            if x[0] == ELSTART:
                x = x[1].split(None, 1)
            self.tag_text.setValue(x[0])
            origtag = x[0]
            is_style_tag = (origtag == 'style')
        self.comment_button.SetValue(iscomment)
        hbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.tag_text, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.comment_button, 0, wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.attr_table = wxgrid.Grid(self, -1, size=(340, 120))
        self.attr_table.CreateGrid(0, 2)
        self.attr_table.SetColLabelValue(0, 'attribute')
        self.attr_table.SetColLabelValue(1, 'value')
        self.attr_table.SetColSize(1, tbl.Size[0] - 162)  # 178) # 160)   ## FIXME: werkt dit?
        if attrs:
            for attr, value in attrs.items():
                if attr == 'styledata':
                    self.old_styledata = value
                    continue
                elif origtag == 'link' and attr == 'rel' and value == 'stylesheet':
                    self.is_stylesheet = True
                elif attr == 'style':
                    has_style = True
                    self.old_styledata = value
                self.attr_table.AppendRows(1)
                idx = tbl.GetNumberRows() - 1
                self.attr_table.SetRowLabelValue(idx, '')
                self.attr_table.SetCellValue(idx, 0, attr)
                ## if attr == 'style':
                    ## item.setFlags(item.flags() & (not core.Qt.ItemIsEditable))
                self.attr_table.SetCellValue(idx, 1, value)
                ## if attr == 'style':
                    ## item.setFlags(item.flags() & (not core.Qt.ItemIsEditable))
        else:
            self.row = -1
        hbox.Add(self.attr_table, 1, wx.EXPAND)
        sbox.Add(hbox, 1, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self, label='&Add Attribute')
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_button = wx.Button(self, label='&Delete Selected')
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_del)
        if is_style_tag:
            text = '&Edit styles'
        elif self.is_stylesheet:
            text = '&Edit linked stylesheet'
        elif has_style:
            text = '&Edit inline style'
        else:
            text = '&Add inline style'
        self.style_button = wx.Button(self, label=text)
        if cssedit_available:
            self.style_button.Bind(wx.EVT_BUTTON, self.on_style)
        else:
            self.style_button.setDisabled(True)
        hbox.Add(self.add_button, 0, wx.EXPAND | wx.ALL, 1)
        hbox.Add(self.delete_button, 0, wx.EXPAND | wx.ALL, 1)
        hbox.Add(self.style_button, 0, wx.EXPAND | wx.ALL, 1)
        sbox.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        vbox.Add(sbox, 1, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, label='&Save')
        self.ok_button.Bind(wx.EVT_BUTTON, self.accept)
        self.SetAffirmativeId(wx.ID_SAVE)
        self.cancel_button = wx.Button(self, label='&Cancel')
        self.cancel_button.Bind(wx.EVT_BUTTON, self.reject)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.tag_text.SetFocus()

    def on_add(self):
        "attribuut toevoegen"
        self.attr_table.AppendRows(1)
        idx = self.attr_table.GetNumberRows() - 1
        self.attr_table.SetRowLabelValue(idx, '')

    def on_del(self):
        "attribuut verwijderen"
        rows = self.attr_table.GetSelectedRows()
        if rows:
            rows.reverse()
            for row in rows:
                self.attr_table.DeleteRows(row, 1)
        else:
            wx.MessageBox("Select a row by clicking on the row heading", 'Selection is empty',
                          wx.ICON_INFORMATION)

    def on_style(self):
        "adjust style attributes"
        return
        #FIXME - mogelijk probleem: cssedit heeft alleen nog maar een QT versie volgens mij
        tag = self.tag_text.GetValue()
        if not self.is_stylesheet:
            css = csed.MainWindow(self, app=self._parent.app)     # calling the editor
            # with this dialog as parent should make sure we get the css back as an attribute
            if tag == 'style':
                css.open(text=self.old_styledata)
            else:
                css.open(tag=tag, text=self.old_styledata)
            css.setWindowModality(core.Qt.ApplicationModal)
            css.show()  # sets self.styledata right before closing
            return
        print("started cssedit main window")
        mld = fname = ''
        test = self.attr_table.findItems('href', core.Qt.MatchFixedString)
        for item in test:
            col = self.attr_table.column(item)
            row = self.attr_table.row(item)
            if col == 0:
                fname = self.attr_table.item(row, 1).text()
        print('got filename:', fname)
        if not fname:
            mld = 'Please enter a link address first'
        elif fname.startswith('/'):
            mld = "Cannot determine file system location of stylesheet file"
        else:
            if fname.startswith('http'):
                h_fname = os.path.join('/tmp', 'ashe_{}'.format(os.path.basename(fname)))
                os.system('wget {} -O {}'.format(fname, h_fname))    # TODO: use subprocess?
                fname = h_fname
            else:
                h_fname = fname
                xmlfn_path = pathlib.Path(self._parent.editor.xmlfn)
                while h_fname.startswith('../'):
                    h_fname = h_fname[3:]
                    xmlfn_path = xmlfn_path.parent
                fname = str(xmlfn_path / h_fname)
            print('constructed filename:', fname)
            try:
                css = csed.MainWindow(app=self._parent.app)
                css.open(filename=fname)
            except Exception as e:
                mld = str(e)
            else:
                css.setWindowModality(core.Qt.ApplicationModal)
                css.show()
        if mld:
            qtw.QMessageBox.information(self, self._parent.editor.title, mld)

    def on_ok(self):
        "doorgeven in dialoog gewijzigde waarden aan hoofdscherm"
        # TODO: ensure no duplicate items are added
        tag = self.tag_text.GetValue()
        okay = True
        test = string.ascii_letters + string.digits
        for letter in tag:
            if letter not in test:
                ok = False
                wx.MessageBox('Illegal character(s) in tag name',
                              'Add an item', wx.ICON_ERROR)
                return
        commented = self.comment_button.checkState()
        attrs = {}
        for i in range(self.attr_table.GetNumberRows()):
            try:
                name = self.attr_table.GetCellValue(i, 0)
                value = self.attr_table.GetCellValue(i, 1)
            except AttributeError:
                wx.MessageBox('Press enter on this item first',
                              'Add an item', wx.ICON_ERROR)
                return
            if name != 'style':
                attrs[name] = value
        try:
            self.styledata = self.styledata.decode()
        except AttributeError:
            pass
        if self.styledata != self.old_styledata:
            self.old_styledata = self.styledata
        if tag == 'style':
            attrs['styledata'] = self.old_styledata
        else:
            if self.old_styledata:
                attrs['style'] = self.old_styledata
        return tag, attrs, commented


class TextDialog(wx.Dialog):
    """dialoog om een tekst element op te voeren of aan te passen
    biedt tevens de mogelijkheid de tekst "op commentaar" te zetten"""

    def __init__(self, parent, title='', text=None):
        self._parent = parent
        super().__init__(parent, title=title,
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.comment_button = wx.CheckBox(self, label='&Comment(ed)')
        if text is None:
            text = ''
        else:
            if text.startswith(CMSTART):
                self.comment_button.toggle()
                dummy, text = text.split(None, 1)
        hbox.Add(self.comment_button, 0, wx.EXPAND | wx.ALL, 1)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.data_text = wx.TextCtrl(self, -1, size=(340, 175), style=wx.TE_MULTILINE)
        self.data_text.SetValue(text)
        hbox.Add(self.data_text, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        # self.ok_button.Bind(wx.EVT_BUTTON, self.accept)
        # self.ok_button.setDefault(True)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        # self.cancel_button.Bind(wx.EVT_BUTTON, self.reject)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)
        self.sizer = vbox
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.data_text.SetFocus()

    def on_ok(self):
        "doorgeven in dialoog gewijzigde waarden aan hoofdscherm"
        commented = self.comment_button.checkState()
        tag = self.data_text.GetValue()
        return txt, commented


class SearchDialog(wx.Dialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title=""):
        return
        super().__init__(parent)
        self.setWindowTitle(title)
        self._parent = parent

        self.cb_element = wx.StaticText('Element', self)
        lbl_element = wx.StaticText("name:", self)
        self.txt_element = wx.TextCtrl(self)
        self.txt_element.textChanged.connect(self.set_search)

        self.cb_attr = wx.StaticText('Attribute', self)
        lbl_attr_name = wx.StaticText("name:", self)
        self.txt_attr_name = wx.TextCtrl(self)
        self.txt_attr_name.textChanged.connect(self.set_search)
        lbl_attr_val = wx.StaticText("value:", self)
        self.txt_attr_val = wx.TextCtrl(self)
        self.txt_attr_val.textChanged.connect(self.set_search)

        self.cb_text = wx.StaticText('Text', self)
        lbl_text = wx.StaticText("value:", self)
        self.txt_text = wx.TextCtrl(self)
        self.txt_text.textChanged.connect(self.set_search)

        self.lbl_search = wx.StaticText('', self)

        self.btn_ok = wx.Button('&Ok', self)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.accept)
        self.btn_ok.setDefault(True)
        self.btn_cancel = wx.Button('&Cancel', self)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.reject)

        sizer = wx.BoxSizer(wx.VERTICAL)

        gsizer = qtw.QGridLayout()

        gsizer.addWidget(self.cb_element, 0, 0)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.addWidget(lbl_element)
        hsizer.addWidget(self.txt_element)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 0, 1)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.addSpacing(5)
        vsizer.addWidget(self.cb_attr)
        vsizer.addStretch()
        gsizer.addLayout(vsizer, 1, 0)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.addWidget(lbl_attr_name)
        hsizer.addWidget(self.txt_attr_name)
        vsizer.addLayout(hsizer)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.addWidget(lbl_attr_val)
        hsizer.addWidget(self.txt_attr_val)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 1, 1)

        gsizer.addWidget(self.cb_text, 2, 0)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.addWidget(lbl_text)
        hsizer.addWidget(self.txt_text)
        gsizer.addLayout(hsizer, 2, 1)
        sizer.addLayout(gsizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.addWidget(self.lbl_search)
        sizer.addLayout(hsizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.addStretch()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)

        if self._parent.search_args:
            self.txt_element.setText(self._parent.search_args[0])
            self.txt_attr_name.setText(self._parent.search_args[1])
            self.txt_attr_val.setText(self._parent.search_args[2])
            self.txt_text.setText(self._parent.search_args[3])

    def set_search(self):
        """build text describing search action"""
        return
        out = ''
        ele = self.txt_element.text()
        attr_name = self.txt_attr_name.text()
        attr_val = self.txt_attr_val.text()
        text = self.txt_text.text()
        attr = ''
        if ele:
            ele = '\n an element named `{}`'.format(ele)
        if attr_name or attr_val:
            attr = '\n an attribute'
            if attr_name:
                attr += ' named `{}`'.format(attr_name)
            if attr_val:
                attr += '\n that has value `{}`'.format(attr_val)
            if ele:
                attr = '\n with' + attr[1:]
        if text:
            out = 'search for text'
            if ele:
                out += '\n under' + ele[1:]
            elif attr:
                out += '\n under an element\n with'
            if attr:
                out += attr
        elif ele:
            out = 'search for' + ele
            if attr:
                out += attr
        elif attr:
            out = 'search for' + attr
        self.lbl_search.setText(out)

    def on_ok(self):
        """confirm dialog and pass changed data to parent"""
        ele = str(self.txt_element.GetValue())
        attr_name = str(self.txt_attr_name.GetValue())
        attr_val = str(self.txt_attr_val.GetValue())
        text = str(self.txt_text.GetValue())
        if not any((ele, attr_name, attr_val, text)):
            wx.MessageBox('Please enter search criteria or press cancel',
                          self._parent.editor.title, self)
            self.txt_element.setFocus()
            return

        return (ele, attr_name, attr_val, text)


class DtdDialog(wx.Dialog):
    """dialoog om het toe te voegen dtd te selecteren
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent, title="Add DTD")
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        lbl = wx.StaticText(self, label="Select document type:")
        hbox.Add(lbl, 0, wx.TOP, 10)
        sbox.Add(hbox, 0)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        first = True
        button_groups = []
        self.dtd_list = []
        for idx, x in enumerate(self._parent.editor.dtdlist):
            if not x[0]:
                hbox.Add(vbox2)
                sbox.Add(hbox, 0, wx.ALL, 10)
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                vbox2 = wx.BoxSizer(wx.VERTICAL)
                continue
            if first:
                radio = wx.RadioButton(self, -1, x[0], style=wx.RB_GROUP)
                first = False
            else:
                radio = wx.RadioButton(self, -1, x[0])
            # if idx == 4:
            #     radio.setChecked(True)
            x.append(radio)
            vbox2.Add(radio, 0, wx.ALL, 2)
            # self.dtd_list.append((x[0], x[1], radio))
        hbox.Add(vbox2)
        sbox.Add(hbox, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(sbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.IS_SAVE)
        self.SetAffirmativeId(wx.ID_SAVE)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()

    def accept(self):
        """pass changed data to parent
        """
        # for caption, dtd, radio in self.dtd_list:
        #     if radio and radio.isChecked():
        #         self._parent.dialog_data = dtd
        #         break
        # super().accept()


class CssDialog(wx.Dialog):
    """dialoog om een stylesheet toe te voegen
    """
    def __init__(self, parent):
        return
        self._parent = parent
        self.styledata = ''
        super().__init__(parent)
        self.setWindowTitle('Add Stylesheet')
        self.setWindowIcon(self._parent.appicon)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        gbox = qtw.QGridLayout()

        gbox.addWidget(wx.StaticText("link to stylesheet:", self), 0, 0)
        self.link_text = wx.TextCtrl("http://", self)
        gbox.addWidget(self.link_text, 0, 1)

        self.choose_button = wx.Button('&Browse', self)
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, 1, 0, 1, 2)

        gbox.addWidget(wx.StaticText("for media type(s):", self), 2, 0)
        self.text_text = wx.TextCtrl(self)
        gbox.addWidget(self.text_text, 2, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button('&Save', self)
        self.ok_button.Bind(wx.EVT_BUTTON, self.accept)
        self.ok_button.setDefault(True)
        self.inline_button = wx.Button('&Add inline', self)
        self.inline_button.Bind(wx.EVT_BUTTON, self.on_inline)
        self.cancel_button = wx.Button('&Cancel', self)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.inline_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.link_text.setFocus()

    def kies(self):
        "methode om het te linken document te selecteren"
        return
        loc = self._parent.editor.xmlfn or os.getcwd()
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc, CMASK)
        if fnaam:
            self.link_text.setText(fnaam)

    def accept(self):
        """bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad
        maar eerst kijken of dit geen inline stylesheet betreft """
        return
        # TODO: wat als er zowel styledata als een linkadres is?
        if self.styledata:
            self._parent.dialog_data = {"cssdata": self.styledata.decode()}
            super().accept()
            return
        link = str(self.link_text.text())
        if link in ('', 'http://'):
            qtw.QMessageBox.information(self, self.parent().title, "bestandsnaam opgeven"
                                        " of inline stylesheet definiëren s.v.p")
            return
        try:
            link = self._parent.editor.convert_link(link, self._parent.editor.xmlfn)
        except ValueError as msg:
            qtw.QMessageBox.information(self, self._parent.title, msg)
            return
        self._parent.dialog_data = {"rel": 'stylesheet',
                                    "href": link,
                                    "type": 'text/css'}
        test = str(self.text_text.text())
        if test:
            self._parent.dialog_data["media"] = test
        super().accept()

    def on_inline(self):
        "voegt een 'style' tag in"
        return
        self._parent.dialog_data = {"type": 'text/css'}
        test = str(self.text_text.text())
        if test:
            self._parent.dialog_data["media"] = test
        css = csed.MainWindow(self, self._parent.app)
        css.open(text="")
        css.setWindowModality(core.Qt.ApplicationModal)
        css.show()


class LinkDialog(wx.Dialog):
    """dialoog om een link element toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent, title='Add Link')
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = qtw.QGridLayout()
        lbl = wx.StaticText(self, label="descriptive title:")
        gbox.addWidget(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.title_text = wx.TextCtrl(self, -1, size=(250, -1))
        gbox.Add(self.title_text, (0, 1))

        lbl = wx.StaticText(self, label="link to document:")
        gbox.Add(lbl, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self, size=(250, -1), value="http://")
        self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (1, 1))

        self.choose_button = wx.Button(self, label='&Browse')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (2, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText(self, label="link text:")
        gbox.Add(lbl, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.text_text = wx.TextCtrl(self, size=(250, -1))
        self.text_text.Bind(wx.EVT_TEXT, self.set_text)
        gbox.Add(self.text_text, (3, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.title_text.SetFocus()

    def kies(self):
        "methode om het te linken document te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        with wx.FileDialog(self, message="Choose a file", defaultDir=loc,
                           wildcard=HMASK, style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.link_text.SetValue(dlg.GetPath())

    def set_text(self, chgtext):
        'indien leeg title tekst gelijk maken aan link adres'
        if evt.EventObject == self.link_text:
            linktxt = self.link_text.GetValue()
            if self.text_text.GetValue() == self.linktxt:
                self.text_text.SetValue(linktxt)
                self.linktxt = linktxt
        elif self.text_text.GetValue() == "":
            self.linktxt = ""

    def on_ok(self, evt=None):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        txt = str(self.text_text.text())
        if not txt:
            wx.MessageBox("link opgeven of cancel kiezen s.v.p", self.parent.title)
            # hlp = qtw.QMessageBox.question(self, 'Add Link',
            #                                "Link text is empty - are you sure?",
            #                                qtw.QMessageBox.Yes | qtw.QMessageBox.No,
            #                                defaultButton=qtw.QMessageBox.Yes)
            # if hlp == qtw.QMessageBox.No:
            #     return
            return
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            self.parent.meld(msg)
            return
        self._parent.dialog_data = [txt, {"href": link,
                                          "title": str(self.title_text.text())}]
        super().accept()


class ImageDialog(wx.Dialog):
    """dialoog om een image toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent, title='Add Image')
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)

        lbl = wx.StaticText(self, -1, "descriptive title:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.title_text = wx.TextCtrl(self, -1, size=(250, -1))
        gbox.Add(self.title_text, (0, 1))

        lbl = wx.StaticText(self, -1, "link to image:")
        gbox.Add(lbl, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self, -1, size=(250, -1), value="http://")
        self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (1, 1))

        self.choose_button = wx.Button(self, -1, 'Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (2, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText(self, -1, "alternate text:")
        gbox.Add(lbl, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.alt_text = wx.TextCtrl(self, -1, size=(250, -1))
        self.alt_text.Bind(wx.EVT_TEXT, self.set_text)
        gbox.Add(self.alt_text, (3, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.title_text.SetFocus()

    def kies(self):
        "methode om het te linken image te selecteren"
        with wx.FileDialog(self, message="Choose a file", defaultDir=os.getcwd(),
                           wildcard=IMASK, style=wx.OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.link_text.SetValue(dlg.GetPath())

    def set_text(self, evt=None):
        'indien leeg link tekst gelijk maken aan link adres'
        if evt.EventObject == self.link_text:
            linktxt = self.link_text.GetValue()
            if self.alt_text.GetValue() == self.linktxt:
                self.alt_text.SetValue(linktxt)
                self.linktxt = linktxt
        elif self.alt_text.GetValue() == "":
            self.linktxt = ""

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            wx.MessageBox.information(self._parent.title, msg, self)
            return
        self._parent.dialog_data = {"src": link,
                                    "alt": str(self.alt_text.text()),
                                    "title": str(self.title_text.text())}


class VideoDialog(wx.Dialog):
    """dialoog om een video element toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        initialwidth, initialheight = 400, 200
        maxwidth, maxheight = 2400, 1200
        super().__init__(parent, title='Add Video')
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)

        lbl = wx.StaticText(self, -1, "link to video:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self, -1, size=(250, -1), value="http://")
        self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (0, 1))

        self.choose_button = wx.Button(self, -1, 'Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (1, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText("height of video window:", self)
        self.hig_text = wx.SpinCtrl(self)  # .pnl, -1, size = (40, -1))
        self.hig_text.SetMax(maxheight)
        self.hig_text.SetValue(initialheight)
        self.hig_text.Bind(wx.EVT_SPINCTRL, self.on_text)
        gbox.Add(self.hig_text, (2, 1))

        lbl = wx.StaticText("width of video window:", self)
        self.wid_text = wx.SpinCtrl(self)  # .pnl, -1, size = (40, -1))
        self.wid_text.SetMax(maxwidth)
        self.wid_text.SetValue(initialwidth)
        self.wid_text.Bind(wx.EVT_SPINCTRL, self.on_text)
        gbox.Add(self.wid_text, (3, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.title_text.SetFocus()

    def kies(self):
        "methode om het te linken element te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        mask = '*.mp4 *.avi *.mpeg'  # TODO: add other types
        if os.name == "posix":
            mask += ' ' + mask.upper()
        mask = "Video files ({});;{}".format(mask, IMASK)
        with wx.FileDialog(self, message="Choose a file", defaultDir=os.getcwd(),
                           wildcard=IMASK, style=wx.OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.link_text.SetValue(dlg.GetPath())

    def on_text(self, number=None):
        "controle bij invullen/aanpassen hoogte/breedte"
        try:
            int(number)  # self.rows_text.value())
        except ValueError:
            wx.MessageBox.information(self._parent.title, 'Number must be numeric integer',
                                      self)
            return

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            wx.MessageBox.information(self._parent.title, msg, self)
            return
        self._parent.dialog_data = {"src": link,
                                    "height": str(self.hig_text.text()),
                                    "width": str(self.wid_text.text())}


class AudioDialog(wx.Dialog):
    'dialoog om een audio element toe te voegen'

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent, title='Add Audio')
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)

        lbl = wx.StaticText("link to audio fragment:", self)
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self, -1, size=(250, -1), value="http://")
        self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (0, 1))

        self.choose_button = wx.Button(self, -1, 'Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (1, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.title_text.SetFocus()

    def kies(self):
        "methode om het te linken element te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        mask = '*.mp3 *.wav *.ogg'  # TODO: add other types
        if os.name == "posix":
            mask += ' ' + mask.upper()
        mask = "Audio files ({});;{}".format(mask, IMASK)
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
        if fnaam:
            self.link_text.setText(fnaam)

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            qtw.QMessageBox.information(self, self._parent.title, msg)
            return
        self._parent.dialog_data = {"src": link}
        super().accept()


class ListDialog(wx.Dialog):
    """dialoog om een list toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        self.items = []
        self.dataitems = []
        initialrows = 1
        super().__init__(parent, title='Add a list',
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        tbox = wx.FlexGridSizer(2, 2, 2, 2)
        lbl = wx.StaticText(self, -1, "choose type of list:")

        self.type_select = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN,
                                       choices=["unordered", "ordered", "definition"])
        self.type_select.SetStringSelection("unordered")
        self.type_select.Bind(wx.EVT_COMBOBOX, self.on_type)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.type_select)

        lbl = wx.StaticText(self, -1, "initial number of items:")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.rows_text = wx.SpinCtrl(self)
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_rows)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.rows_text)  # hbox)
        sbox.Add(tbox, 0, wx.ALL, 5)

        self.list_table = wxgrid.Grid(self, -1, size=(340, 120))
        self.list_table.CreateGrid(0, 1)
        self.list_table.SetColLabelValue(0, 'list item')
        self.list_table.SetColSize(0, 240)
        sbox.Add(self.list_table, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(sbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.type_select.SetFocus()

    def on_type(self, evt=None):  # , selectedindex=None):
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

    def on_rows(self, evt=None):  # , number=None):
        "controle en actie bij invullen/aanpassen aantal regels"
        try:
            cur_rows = int(self.rows_text.GetValue())
        except ValueError:
            wx.MessageBox.information('Number must be numeric integer', self._parent.title,
                                      self)
            return
        num_rows = self.list_table.GetNumberRows()
        if num_rows > cur_rows:
            for idx in range(num_rows - 1, cur_rows - 1, -1):
                self.list_table.DeleteRows(idx)
        elif cur_rows > num_rows:
            for idx in range(num_rows, cur_rows):
                self.list_table.AppendRows(1)
                self.list_table.SetRowLabelValue(idx, '')

    def on_ok(self):
        """bij OK: de opgebouwde list via self.dialog_data doorgeven
        aan het mainwindow
        """
        list_type = str(self.type_select.currentText()[0]) + "l"
        list_data = []
        for row in range(self.list_table.rowCount()):
            try:
                list_item = [str(self.list_table.item(row, 0).text())]
            except AttributeError:
                self._parent.meld('Graag nog even het laatste item bevestigen (...)')
                return
            if list_type == "dl":
                try:
                    list_item.append(str(self.list_table.item(row, 1).text()))
                except AttributeError:
                    self._parent.meld('Graag nog even het laatste item bevestigen (...)')
                    return
            list_data.append(list_item)
        self._parent.dialog_data = list_type, list_data


class TableDialog(wx.Dialog):
    "dialoog om een tabel toe te voegen"

    def __init__(self, parent):
        self._parent = parent
        self.headings = ['']
        initialcols, initialrows = 1, 1
        super().__init__(parent, title='Add a table'
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self.pnl, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        tbox = wx.FlexGridSizer(3, 2, 2, 2)

        lbl = wx.StaticText(self.pnl, -1, "summary (description):")
        tbox.Add(lbl)
        self.title_text = wx.TextCtrl(self.pnl, -1, size=(250, -1))
        tbox.Add(self.title_text)

        # self.rows_text.setValue(initialrows)
        lbl = wx.StaticText(self.pnl, -1, "initial number of rows:")
        self.rows_text = wx.SpinCtrl(self.pnl, -1)
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_rows)
        self.rows_text.Bind(wx.EVT_TEXT, self.on_rows)
        tbox.Add(lbl)
        tbox.Add(self.rows_text)

        # self.cols_text.setValue(initialcols)
        lbl = wx.StaticText(self.pnl, -1, "initial number of columns:")
        self.cols_text = wx.SpinCtrl(self.pnl)
        self.cols_text.Bind(wx.EVT_SPINCTRL, self.on_cols)
        self.cols_text.Bind(wx.EVT_TEXT, self.on_cols)
        tbox.Add(lbl)
        tbox.Add(self.cols_text)
        sbox.Add(tbox, 0, wx.ALL, 5)

        self.show_titles = wx.CheckBox('Show Titles')
        self.show_titles.setChecked(True)
        self.show_titles.stateChanged.connect(self.on_check)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.addWidget(self.show_titles)
        gbox.addLayout(hbox, 3, 1)

        # self.table_table.setRowCount(initialrows)     # de eerste rij is voor de kolomtitels
        # self.table_table.setColumnCount(initialcols)  # de eerste rij is voor de rijtitels
        # self.table_table.setHorizontalHeaderLabels(self.headings)
        # self.hdr = self.table_table.horizontalHeader()
        # self.table_table.verticalHeader().setVisible(False)
        # self.hdr.setSectionsClickable(True)
        # self.hdr.sectionBind(wx.EVT_BUTTON, self.on_title)
        self.table_table = wxgrid.Grid(self.pnl, -1, size=(340, 120))
        self.table_table.CreateGrid(0, 0)
        self.table_table.Bind(wxgrid.EVT_GRID_LABEL_LEFT_CLICK, self.on_title)
        self.table_table.Bind(wxgrid.EVT_GRID_LABEL_LEFT_DCLICK, self.on_title)
        self.table_table.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_title)
        self.table_table.Bind(wxgrid.EVT_GRID_LABEL_RIGHT_DCLICK, self.on_title)
        sbox.Add(self.table_table, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(sbox, 1, wx.EXPAND | wx.ALL, 20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 20)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.title_text.SetFocus()

    def on_rows(self, evt=None):  # , number=None):
        "controle en actie bij opgeven aantal regels"
        try:
            cur_rows = int(self.rows_text.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer', self.parent.title)
            return
        num_rows = self.table_table.GetNumberRows()
        if num_rows > cur_rows:
            for idx in range(num_rows - 1, cur_rows - 1, -1):
                self.table_table.DeleteRows(idx)
        elif cur_rows > num_rows:
            for idx in range(num_rows, cur_rows):
                self.table_table.AppendRows(1)
                self.table_table.SetRowLabelValue(idx, '')

    def on_cols(self, evt=None):  # , number=None):
        "controle en actie bij opgeven aantal kolommen"
        try:
            cur_cols = int(self.cols_text.GetValue())
        except ValueError:
            wx.MessageBox('Number must be numeric integer', self.parent.title)
            return
        num_cols = self.table_table.GetNumberCols()
        if num_cols > cur_cols:
            for idx in range(num_cols - 1, cur_cols - 1, -1):
                self.table_table.DeleteCols(idx)
                # self.headings.pop()
        elif cur_cols > num_cols:
            for idx in range(num_cols, cur_cols):
                # self.headings.append('')
                # self.table_table.setHorizontalHeaderLabels(self.headings)
                self.table_table.AppendCols(1)
                self.table_table.SetColLabelValue(idx, '')

    def on_check(self, number=None):
        "callback for show titles checkbox"
        # self.hdr.setVisible(bool(number))

    def on_title(self, evt=None):
        "opgeven titel bij klikken op kolomheader mogelijk maken"
        if not evt:
            return
        col = evt.GetCol()
        if col < 0:
            return
        with wx.TextEntryDialog(self, 'Enter a title for this column:',
                                self.parent.title) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.table_table.SetColLabelValue(col, dlg.GetValue())

    def on_ok(self):
        """bij OK: de opgebouwde tabel via self.dialog_data doorgeven
        aan het mainwindow
        """
        rows = self.table_table.rowCount()
        cols = self.table_table.columnCount()
        summary = str(self.title_text.text())
        items = []
        for row in range(rows):
            rowitems = []
            for col in range(cols):
                try:
                    rowitems.append(str(self.table_table.item(row, col).text()))
                except AttributeError:
                    self._parent.meld('Graag nog even het laatste item bevestigen (...)')
                    return
            items.append(rowitems)
        self._parent.dialog_data = (summary, self.show_titles.isChecked(),
                                    self.headings, items)
        super().accept()


class ScrolledTextDialog(wx.Dialog):
    """dialoog voor het tonen van validatieoutput

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title='', data='', htmlfile='', fromdisk=False,
                 size=(600, 400)):
        # self._parent = parent
        self.htmlfile = htmlfile
        super().__init__(parent, title=title)
        self.resize(size[0], size[1])
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.message = wx.StaticText(self)
        if fromdisk:
            self.message.setText("\n".join((
                "Validation results are for the file on disk",
                "some errors/warnings may already have been corrected by "
                "BeautifulSoup",
                "(you'll know when they don't show up inthe tree or text view",
                " ozr when you save the file in memory back to disk)")))
        hbox.addWidget(self.message)
        vbox.addLayout(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.TextCtrl(self)
        text.setReadOnly(True)
        hbox.addWidget(text)
        vbox.addLayout(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button('&Done', self)
        ok_button.Bind(wx.EVT_BUTTON, self.close)
        ok_button.setDefault(True)
        if htmlfile:
            show_button = wx.Button('&View submitted source', self)
            show_button.Bind(wx.EVT_BUTTON, self.show_source)
        hbox.addStretch()
        hbox.addWidget(ok_button)
        if htmlfile:
            hbox.addWidget(show_button)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        if htmlfile:
            data = parent.editor.do_validate(htmlfile)
        if data:
            text.setPlainText(data)

    def show_source(self):
        "start viewing html source"
        with open(self.htmlfile) as f_in:
            data = ''.join([x for x in f_in])
        if data:
            dlg = CodeViewDialog(self, "Submitted source", data=data)
            dlg.show()


class CodeViewDialog(wx.Dialog):
    """dialoog voor het tonen van de broncode

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title='', caption='', data='', size=(600, 400)):
        "create a window with a scintilla text widget and an ok button"
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        # self.setWindowIcon(self._parent.appicon)
        self.resize(size[0], size[1])
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.addWidget(wx.StaticText(caption, self))
        vbox.addLayout(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = sci.QsciScintilla(self)
        self.setup_text()
        self.text.setText(data)
        self.text.setReadOnly(True)
        hbox.addWidget(self.text)
        vbox.addLayout(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button('&Done', self)
        ok_button.Bind(wx.EVT_BUTTON, self.close)
        ok_button.setDefault(True)
        hbox.addStretch()
        hbox.addWidget(ok_button)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def setup_text(self):
        "define the scintilla widget's properties"
        # Set the default font
        font = gui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.text.setFont(font)
        self.text.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = gui.QFontMetrics(font)
        self.text.setMarginsFont(font)
        self.text.setMarginWidth(0, fontmetrics.width("00000"))
        self.text.setMarginLineNumbers(0, True)
        self.text.setMarginsBackgroundColor(gui.QColor("#cccccc"))

        # Enable brace matching, auto-indent, code-folding
        self.text.setBraceMatching(sci.QsciScintilla.SloppyBraceMatch)
        self.text.setAutoIndent(True)
        self.text.setFolding(sci.QsciScintilla.PlainFoldStyle)

        # Current line visible with special background color
        self.text.setCaretLineVisible(True)
        self.text.setCaretLineBackgroundColor(gui.QColor("#ffe4e4"))

        # Set HTML lexer
        lexer = sci.QsciLexerHTML()
        lexer.setDefaultFont(font)
        self.text.setLexer(lexer)
