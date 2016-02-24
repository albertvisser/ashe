# -*- coding: utf-8 -*-

"""
PyQt4 versie van mijn op een treeview gebaseerde HTML-editor
custom dialogen
"""

import os
import sys
import string
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import PyQt4.Qsci as sci # scintilla
import ashe.ashe_mixin as ed

try:
    import cssedit.editor.csseditor_qt as csed
    cssedit_available = True
except ImportError:
    cssedit_available = False

PPATH = os.path.split(__file__)[0]
CMSTART = ed.CMSTART
ELSTART = ed.ELSTART
CMELSTART = ed.CMELSTART
DTDSTART = ed.DTDSTART
IFSTART = ed.IFSTART
IMASK = "All files (*.*)"
if os.name == "nt":
    HMASK = "HTML files (*.htm *.html);;" + IMASK
elif os.name == "posix":
    HMASK = "HTML files (*.htm *.HTM *.html *.HTML);;" + IMASK

class ElementDialog(gui.QDialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, parent, title='', tag=None, attrs=None):
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        self._parent = parent
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        lbl = gui.QLabel("element name:", self)
        self.tag_text = gui.QLineEdit(self)
        self.tag_text.setMinimumWidth(250)
        self.comment_button = gui.QCheckBox('&Comment(ed)', self)
        ## is_comment = False
        is_style_tag = self.is_stylesheet = has_style = False
        self.styledata = self.old_styledata = ''
        if tag:
            x = tag.split(None, 1)
            if x[0] == CMSTART:
                ## is_comment = True
                self.comment_button.toggle()
                x = x[1].split(None, 1)
            if x[0] == ELSTART:
                x = x[1].split(None, 1)
            self.tag_text.setText(x[0])
            origtag = x[0]
            is_style_tag = (origtag == 'style')
            ## self.tag_text.readonly=True
        hbox.addWidget(lbl)
        hbox.addWidget(self.tag_text)
        hbox.addWidget(self.comment_button)
        vbox.addLayout(hbox)

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)

        box = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        self.attr_table = gui.QTableWidget(self)
        ## self.attr_table.resize(540, 340)
        self.attr_table.setColumnCount(2)
        self.attr_table.setHorizontalHeaderLabels(['attribute', 'value']) # alleen zo te wijzigen
        hdr = self.attr_table.horizontalHeader()
        ## hdr.setMinimumSectionSize(340)
        hdr.resizeSection(0, 102)
        hdr.resizeSection(1, 152)
        hdr.setStretchLastSection(True)
        self.attr_table.verticalHeader().setVisible(False)
        self.attr_table.setTabKeyNavigation(False)
        ## self.attr_table.SetColSize(1, tbl.Size[0] - 162) # 178) # 160)
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
                idx = self.attr_table.rowCount()
                self.attr_table.insertRow(idx)
                item = gui.QTableWidgetItem(attr)
                self.attr_table.setItem(idx, 0, item)
                if attr == 'style':
                    item.setFlags(item.flags() & (not core.Qt.ItemIsEditable))
                item = gui.QTableWidgetItem(value)
                self.attr_table.setItem(idx, 1, item)
                if attr == 'style':
                    item.setFlags(item.flags() & (not core.Qt.ItemIsEditable))
        else:
            self.row = -1
        ## hbox.addStretch()
        hbox.addWidget(self.attr_table)
        ## hbox.addStretch()
        box.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        self.add_button = gui.QPushButton('&Add Attribute', self)
        self.add_button.clicked.connect(self.on_add)
        self.delete_button = gui.QPushButton('&Delete Selected', self)
        self.delete_button.clicked.connect(self.on_del)
        if is_style_tag:
            text = '&Edit styles'
        elif self.is_stylesheet:
            text = '&Edit linked stylesheet'
        elif has_style:
            text = '&Edit inline style'
        else:
            text = '&Add inline style'
        self.style_button = gui.QPushButton(text, self)
        if cssedit_available:
            self.style_button.clicked.connect(self.on_style)
        else:
            self.style_button.setDisabled(True)
        hbox.addStretch()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.style_button)
        hbox.addStretch()
        box.addLayout(hbox)

        sbox.setLayout(box)

        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        vbox.addLayout(hbox)
        hbox.addStretch()

        self.setLayout(vbox)

    ## def on_resize(self, evt=None):
        ## self.attr_table.SetColSize(1, self.attr_table.GetSize()[0] - 162) # 178) # 160)
        ## self.attr_table.ForceRefresh()

    def on_add(self, evt=None):
        "attribuut toevoegen"
        self.attr_table.setFocus()
        idx = self.attr_table.rowCount()
        self.attr_table.insertRow(idx)
        self.attr_table.setCurrentCell(idx, 0)

    def on_del(self, evt=None):
        "attribuut verwijderen"
        row = self.attr_table.currentRow()
        if row or row == 0:
            self.attr_table.removeRow(row)
        else:
            gui.QMessageBox.information(self, 'Delete attribute',
                "press Enter on this item first")

    def on_style(self, evt=None):
        tag = self.tag_text.text()
        if not self.is_stylesheet:
            css = csed.MainWindow(self) # call the editor with this dialog as parent should
                                        # make sure we get the css back as an attribute
            if tag =='style':
                css.open(text=self.old_styledata)
            else:
                css.open(tag=tag, text=self.old_styledata)
            css.setWindowModality(core.Qt.ApplicationModal)
            css.show() # sets self.styledata right before closing
            return
        css = csed.MainWindow()
        mld = fname = ''
        test = self.attr_table.findItems('href', core.Qt.MatchFixedString)
        for item in test:
            col = self.attr_table.column(item)
            row = self.attr_table.row(item)
            if col == 0:
                fname = self.attr_table.item(row, 1).text()
        if not fname:
            mld = 'Please enter a link address first'
        else:
            if fname.startswith('http'):
                h_fname = os.path.join('/tmp', 'ashe_{}'.format(
                    os.path.basename(fname)))
                os.system('wget {} -O {}'.format(fname, h_fname))    # TODO
                fname = h_fname
            else:
                h_fname = fname
                xmlfn_path = os.path.dirname(self._parent.xmlfn)
                while h_fname.startswith('../'):
                    h_fname = h_fname[3:]
                    xmlfn_path = os.path.dirname(xmlfn_path)
                fname = os.path.join(xmlfn_path, h_fname)
            try:
                css.open(filename=fname)
            except BaseException as e:
                mld = str(e)
            else:
                css.setWindowModality(core.Qt.ApplicationModal)
                css.show()
        if mld: gui.QMessageBox.information(self, 'Htmledit', mld)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        "controle bij OK aanklikken"
        # TODO: ensure no duplicate items are added
        tag = str(self.tag_text.text())
        okay = True
        test = string.ascii_letters + string.digits
        for letter in tag:
            if letter not in test:
                okay = False
                gui.QMessageBox.information(self, self._parent.title,
                    'Illegal character(s) in tag name')
                break
        commented = self.comment_button.checkState()
        attrs = {}
        for i in range(self.attr_table.rowCount()):
            try:
                name = str(self.attr_table.item(i, 0).text())
                value = str(self.attr_table.item(i, 1).text())
            except AttributeError:
                gui.QMessageBox.information(self, 'Add an element',
                    'Press enter on this item first')
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
        self._parent.dialog_data = tag, attrs, commented
        gui.QDialog.done(self, gui.QDialog.Accepted)

class TextDialog(gui.QDialog):
    """dialoog om een tekst element op te voeren of aan te passen
    biedt tevens de mogelijkheid de tekst "op commentaar" te zetten"""

    def __init__(self, parent, title='', text=None):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        self.comment_button = gui.QCheckBox('&Comment(ed)', self)
        ## self.comment_button.setCheckState(iscomment)
        ## iscomment = False
        if text is None:
            text = ''
        else:
            if text.startswith(CMSTART):
                ## iscomment = True
                self.comment_button.toggle()
                dummy, text = text.split(None, 1)
        hbox.addWidget(self.comment_button)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        self.data_text = gui.QTextEdit(self)
        self.data_text.resize(340, 175)
        self.data_text.setText(text)
        hbox.addWidget(self.data_text)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.data_text.setFocus()

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        self._parent.dialog_data = (
            str(self.data_text.toPlainText()),
            self.comment_button.checkState(),
            )
        gui.QDialog.done(self, gui.QDialog.Accepted)

class DtdDialog(gui.QDialog):
    "dialoog om het toe te voegen dtd te selecteren"

    def __init__(self, parent):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle("Add DTD")
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        vsbox = gui.QVBoxLayout()

        hsbox = gui.QHBoxLayout()
        lbl = gui.QLabel("Select document type:", self)
        hsbox.addWidget(lbl)
        vsbox.addLayout(hsbox, 0)

        hsbox = gui.QHBoxLayout()
        vhsbox = gui.QVBoxLayout()
        first = True
        button_groups = []
        self.dtd_list = []
        for idx, x in enumerate(ed.dtdlist):
            if not x[0]:
                vhsbox.addSpacing(8) #  = gui.QVBoxLayout()
                continue
            if first:
                grp = gui.QButtonGroup()
                button_groups.append(grp)
                first = False
            radio = gui.QRadioButton(x[0], self)
            if idx == 4:
                radio.setChecked(True)
            self.dtd_list.append((x[0], x[1], radio))
            grp.addButton(radio)
            vhsbox.addWidget(radio)
        hsbox.addLayout(vhsbox)
        vsbox.addLayout(hsbox)

        sbox.setLayout(vsbox)
        hbox.addWidget(sbox)
        vbox.addLayout(hbox)

        ## hbox = gui.QDialog.ButtonBoxlayout()
        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        for cap, dtd, radio in self.dtd_list:
            if radio and radio.isChecked():
                self._parent.dialog_data = dtd
                break
        gui.QDialog.done(self, gui.QDialog.Accepted)

class CssDialog(gui.QDialog):
    "dialoog om een stylesheet toe te voegen"

    def __init__(self, parent):
        self._parent = parent
        self.styledata = ''
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle('Add Stylesheet')
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        gbox = gui.QGridLayout() # gui.QGridBagSizer(4, 4)

        gbox.addWidget(gui.QLabel("link to stylesheet:", self), 0, 0)
        self.link_text = gui.QLineEdit("http://", self)
        gbox.addWidget(self.link_text, 0, 1)

        self.choose_button = gui.QPushButton('Search', self)
        self.choose_button.clicked.connect(self.kies)
        box = gui.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, 1, 0, 1, 2)

        gbox.addWidget(gui.QLabel("for media type(s):", self), 2, 0)
        self.text_text = gui.QLineEdit(self)
        gbox.addWidget(self.text_text, 2, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.inline_button = gui.QPushButton('&Add inline', self)
        self.connect(self.inline_button, core.SIGNAL('clicked()'), self.on_inline)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.inline_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.link_text.setFocus()

    def kies(self, evt=None):
        "methode om het te linken document te selecteren"
        if self._parent.xmlfn:
            loc = os.path.dirname(self._parent.xmlfn)
        else:
            loc = os.getcwd()
        if os.name == "nt":
            mask = "CSS files (*.css)"
        elif os.name == "posix":
            mask = "CSS files (*.css *.CSS)"
        fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
        if fnaam:
            self.link_text.setText(fnaam)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        """bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad
        maar eerst kijken of dit geen inline stylesheet betreft """
        # TODO: wat als er zowel styledata als een linkadres is?
        if self.styledata:
            self._parent.dialog_data = {"cssdata": self.styledata.decode()}
            gui.QDialog.done(self, gui.QDialog.Accepted)
            return
        link = str(self.link_text.text())
        if link in ('', 'http://'):
            gui.QMessageBox.information(self, self.parent().title,
                "bestandsnaam opgeven of inline stylesheet definiëren s.v.p")
            ## gui.QDialog.done(self, gui.QDialog.Rejected)
            return
        if not link.startswith('http://'):
            link = os.path.abspath(link)
            if self._parent.xmlfn:
                whereami = os.path.abspath(self._parent.xmlfn)
            else:
                whereami = os.path.join(os.getcwd(),'index.html')
            link = ed.getrelativepath(link, whereami)
        if not link:
            gui.QMessageBox.information(self, self.parent().title,
                'Unable to make this local link relative')
        else:
            self.link = link
        self._parent.dialog_data = {
            "rel": 'stylesheet',
            "href": link,
            "type": 'text/css',
            }
        test = str(self.text_text.text())
        if test:
            self._parent.dialog_data["media"] = test
        gui.QDialog.done(self, gui.QDialog.Accepted)

    def on_inline(self):
        "voegt een 'style' tag in"
        self._parent.dialog_data = {
            "type": 'text/css',
            }
        test = str(self.text_text.text())
        if test:
            self._parent.dialog_data["media"] = test
        css = csed.MainWindow(self)
        css.open(text="")
        css.setWindowModality(core.Qt.ApplicationModal)
        css.show()

class LinkDialog(gui.QDialog):
    "dialoog om een link element toe te voegen"

    def __init__(self, parent):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle('Add Link')
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        gbox = gui.QGridLayout() # gui.QGridBagSizer(4, 4)
        gbox.addWidget(gui.QLabel("descriptive title:", self), 0, 0)
        self.title_text = gui.QLineEdit(self)
        self.title_text.setMinimumWidth(250)
        gbox.addWidget(self.title_text, 0, 1)

        gbox.addWidget(gui.QLabel("link to document:", self), 1, 0)
        self.link_text = gui.QLineEdit("http://", self)
        self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, 1, 1)

        self.choose_button = gui.QPushButton('Search', self)
        self.choose_button.clicked.connect(self.kies)
        box = gui.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, 2, 0, 1, 2)

        gbox.addWidget(gui.QLabel("link text:", self), 3, 0)
        self.text_text = gui.QLineEdit(self)
        self.text_text.textChanged.connect(self.set_ttext)
        gbox.addWidget(self.text_text, 3, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.title_text.setFocus()

    def kies(self, evt=None):
        "methode om het te linken document te selecteren"
        if self._parent.xmlfn:
            loc = os.path.dirname(self._parent.xmlfn)
        else:
            loc = os.getcwd()
        fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", loc,
            HMASK)
        if fnaam:
            self.link_text.setText(fnaam)

    def set_ltext(self, chgtext):
        'indien leeg title tekst gelijk maken aan link adres'
        linktxt = str(chgtext)
        if self.title_text.text() == self.linktxt:
            self.title_text.setText(linktxt)
            self.linktxt = linktxt

    def set_ttext(self, chgtext):
        if str(chgtext) == "":
            self.linktxt = ""

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        link = str(self.link_text.text())
        if link:
            if not link.startswith('http://'):
                link = os.path.abspath(link)
                if self._parent.xmlfn:
                    whereami = os.path.abspath(self._parent.xmlfn)
                else:
                    whereami = os.path.join(os.getcwd(),'index.html')
                link = ed.getrelativepath(link, whereami)
            if not link:
                gui.QMessageBox.information('Unable to make this local link relative',
                    self.parent.title)
            else:
                self.link = link
            txt = str(self.text_text.text())
            data = {
                "href": link,
                "title": str(self.title_text.text())
                }
            self._parent.dialog_data = txt, data
        else:
            gui.QMessageBox.information("link opgeven of cancel kiezen s.v.p",'')
            return
        gui.QDialog.done(self, gui.QDialog.Accepted)

class ImageDialog(gui.QDialog):
    'dialoog om een image toe te voegen'

    def __init__(self, parent):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle('Add Image')
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        gbox = gui.QGridLayout() # gui.QGridBagSizer(4, 4)
        gbox.addWidget(gui.QLabel("descriptive title:", self), 0, 0)
        self.title_text = gui.QLineEdit(self)
        self.title_text.setMinimumWidth(250)
        gbox.addWidget(self.title_text, 0, 1)

        gbox.addWidget(gui.QLabel("link to image:", self), 1, 0)
        self.link_text = gui.QLineEdit("http://", self)
        self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, 1, 1)

        self.choose_button = gui.QPushButton('Search', self)
        self.choose_button.clicked.connect(self.kies)
        box = gui.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, 2, 0, 1, 2)

        gbox.addWidget(gui.QLabel("alternate text:", self), 3, 0)
        self.alt_text = gui.QLineEdit(self)
        self.alt_text.textChanged.connect(self.set_ttext)
        gbox.addWidget(self.alt_text, 3, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.title_text.setFocus()

    def kies(self, evt=None):
        "methode om het te linken image te selecteren"
        if self._parent.xmlfn:
            loc = os.path.dirname(self._parent.xmlfn)
        else:
            loc = os.getcwd()
        mask = '*.png *.jpg *.gif *.jpeg *.ico *.xpm *.svg'
        ## if os.name == "nt":
            ## mask = "Image files (*.htm *.html);;" + IMASK
        ## elif os.name == "posix":
        if os.name == "posix":
            mask += ' ' + mask.upper()
        mask = "Image files ({});;{}".format(mask, IMASK)
        fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
        if fnaam:
            self.link_text.setText(fnaam)

    def set_ltext(self, chgtext):
        'indien leeg link tekst gelijk maken aan link adres'
        linktxt = str(chgtext)
        if str(self.alt_text.text()) == self.linktxt:
            self.alt_text.setText(linktxt)
            self.linktxt = linktxt

    def set_ttext(self, chgtext):
        if str(chgtext) == "":
            self.linktxt = ""

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        link = str(self.link_text.text())
        if link:
            if not link.startswith('http://'):
                link = os.path.abspath(link)
                if self._parent.xmlfn:
                    whereami = os.path.abspath(self._parent.xmlfn)
                else:
                    whereami = os.path.join(os.getcwd(),'index.html')
                link = ed.getrelativepath(link, whereami)
            if not link:
                gui.QMessageBox.information('Unable to make this local link relative',
                    self.parent.title)
            else:
                self.link = link
            self._parent.dialog_data = {
                    "src": link,
                    "alt": str(self.alt_text.text()),
                    "title": str(self.title_text.text())
                    }
        else:
            gui.QMessageBox.information("image link opgeven of cancel kiezen s.v.p",'')
            return
        gui.QDialog.done(self, gui.QDialog.Accepted)

class VideoDialog(gui.QDialog):
    'dialoog om een video element toe te voegen'

    def __init__(self, parent):
        self._parent = parent
        initialwidth, initialheight = 400, 200
        maxwidth, maxheight = 2400, 1200
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle('Add Video')
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        gbox = gui.QGridLayout() # gui.QGridBagSizer(4, 4)

        row = 0
        gbox.addWidget(gui.QLabel("link to video:", self), row, 0)
        self.link_text = gui.QLineEdit("http://", self)
        ## self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, row, 1)

        row += 1
        self.choose_button = gui.QPushButton('Search', self)
        self.choose_button.clicked.connect(self.kies)
        box = gui.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, row, 0, 1, 2)

        row += 1
        gbox.addWidget(gui.QLabel("height of video window:", self), row, 0)
        self.hig_text = gui.QSpinBox(self) #.pnl, -1, size = (40, -1))
        self.hig_text.setMaximum(maxheight)
        self.hig_text.setValue(initialheight)
        self.hig_text.valueChanged.connect(self.on_text)
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.hig_text)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        gbox.addWidget(gui.QLabel("width  of video window:", self), row, 0)
        self.wid_text = gui.QSpinBox(self) #.pnl, -1, size = (40, -1))
        self.wid_text.setMaximum(maxwidth)
        self.wid_text.setValue(initialwidth)
        self.wid_text.valueChanged.connect(self.on_text)
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.wid_text)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.link_text.setFocus()

    def kies(self, evt=None):
        "methode om het te linken element te selecteren"
        if self._parent.xmlfn:
            loc = os.path.dirname(self._parent.xmlfn)
        else:
            loc = os.getcwd()
        mask = '*.mp4 *.avi *.mpeg' # TODO: add other types
        ## if os.name == "nt":
            ## mask = "Image files (*.htm *.html);;" + IMASK
        ## elif os.name == "posix":
        if os.name == "posix":
            mask += ' ' + mask.upper()
        mask = "Video files ({});;{}".format(mask, IMASK)
        fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
        if fnaam:
            self.link_text.setText(fnaam)

    def on_text(self, number=None):
        "controle bij invullen/aanpassen hoogte/breedte"
        try:
            num = int(number) # self.rows_text.value())
        except ValueError:
            gui.QMessageBox.information(self, self.title,
                'Number must be numeric integer','')
            return

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        link = str(self.link_text.text())
        if link:
            if not link.startswith('http://'):
                link = os.path.abspath(link)
                if self._parent.xmlfn:
                    whereami = os.path.abspath(self._parent.xmlfn)
                else:
                    whereami = os.path.join(os.getcwd(),'index.html')
                link = ed.getrelativepath(link, whereami)
            if not link:
                gui.QMessageBox.information('Unable to make this local link relative',
                    self.parent.title)
            else:
                self.link = link
            self._parent.dialog_data = {
                    "src": link,
                    "height": str(self.hig_text.text()),
                    "width": str(self.wid_text.text())
                    }
        else:
            gui.QMessageBox.information("link naar video opgeven of cancel kiezen s.v.p",'')
            return
        gui.QDialog.done(self, gui.QDialog.Accepted)

class AudioDialog(gui.QDialog):
    'dialoog om een audio element toe te voegen'

    def __init__(self, parent):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle('Add Audio')
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        gbox = gui.QGridLayout() # gui.QGridBagSizer(4, 4)

        row = 0
        gbox.addWidget(gui.QLabel("link to audio fragment:", self), row, 0)
        self.link_text = gui.QLineEdit("http://", self)
        ## self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, row, 1)

        row += 1
        self.choose_button = gui.QPushButton('Search', self)
        self.choose_button.clicked.connect(self.kies)
        box = gui.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, row, 0, 1, 2)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.link_text.setFocus()

    def kies(self, evt=None):
        "methode om het te linken element te selecteren"
        if self._parent.xmlfn:
            loc = os.path.dirname(self._parent.xmlfn)
        else:
            loc = os.getcwd()
        mask = '*.mp3 *.wav *.ogg' # TODO: add other types
        ## if os.name == "nt":
            ## mask = "Image files (*.htm *.html);;" + IMASK
        ## elif os.name == "posix":
        if os.name == "posix":
            mask += ' ' + mask.upper()
        mask = "Audio files ({});;{}".format(mask, IMASK)
        fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
        if fnaam:
            self.link_text.setText(fnaam)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        link = str(self.link_text.text())
        if link:
            if not link.startswith('http://'):
                link = os.path.abspath(link)
                if self._parent.xmlfn:
                    whereami = os.path.abspath(self._parent.xmlfn)
                else:
                    whereami = os.path.join(os.getcwd(),'index.html')
                link = ed.getrelativepath(link, whereami)
            if not link:
                gui.QMessageBox.information('Unable to make this local link relative',
                    self.parent.title)
            else:
                self.link = link
            self._parent.dialog_data = {
                    "src": link,
                    }
        else:
            gui.QMessageBox.information("link naar audio opgeven of cancel kiezen s.v.p",'')
            return
        gui.QDialog.done(self, gui.QDialog.Accepted)

class ListDialog(gui.QDialog):
    'dialoog om een list toe te voegen'

    def __init__(self, parent):
        self._parent = parent
        self.items = []
        self.dataitems = []
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle('Add a list')
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        vsbox = gui.QVBoxLayout()
        tbox = gui.QGridLayout() # gui.QGridBagSizer(4, 4)
        tbox.addWidget(gui.QLabel("choose type of list:", self), 0, 0)
        self.type_select = gui.QComboBox(self)
        self.type_select.addItems(["unordered", "ordered", "definition",])
        ## self.type_select.setCurrentIndex(0) # SetStringSelection("unordered")
        self.type_select.activated.connect(self.on_type)
        tbox.addWidget(self.type_select, 0, 1)

        tbox.addWidget(gui.QLabel("initial number of items:", self), 1, 0)
        self.rows_text = gui.QSpinBox(self) #.pnl, -1, size = (40, -1))
        self.rows_text.valueChanged.connect(self.on_text)
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.rows_text)
        hbox.addStretch()
        tbox.addLayout(hbox, 1, 1)
        vsbox.addLayout(tbox)

        tbl = gui.QTableWidget(self) # wxgrid.Grid(self.pnl, -1, size = (340, 120))
        tbl.setColumnCount(1) # CreateGrid(0, 1)
        tbl.setHorizontalHeaderLabels(['list item'])
        hdr = tbl.horizontalHeader()
        hdr.resizeSection(0, 252)
        tbl.verticalHeader().setVisible(False)
        ## tbl.SetColSize(0, 240)
        self.list_table = tbl
        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.list_table)
        hbox.addStretch()
        vsbox.addLayout(hbox)
        sbox.setLayout(vsbox)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.connect(self.ok_button, core.SIGNAL('clicked()'), self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.connect(self.cancel_button, core.SIGNAL('clicked()'), self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.type_select.setFocus()

    def on_type(self, selectedindex=None):
        "geselecteerde list type toepassen"
        sel = self.type_select.currentText()
        numcols = self.list_table.columnCount()
        hdr = self.list_table.horizontalHeader()
        if sel[0] == "d" and numcols == 1:
            self.list_table.insertColumn(0)
            self.list_table.setHorizontalHeaderLabels(['term', 'description'])
            hdr.resizeSection(0, 102)
            hdr.resizeSection(1, 152)
            ## self.list_table.SetColLabelValue(0, 'term')
            ## self.list_table.SetColSize(0, 80)
            ## self.list_table.SetColLabelValue(1, 'description')
            ## self.list_table.SetColSize(1, 160)
        elif sel[0] != "d" and numcols == 2:
            self.list_table.removeColumn(0)
            self.list_table.setHorizontalHeaderLabels(['list item'])
            hdr.resizeSection(0, 254)
            ## self.list_table.SetColLabelValue(0, 'list item')
            ## self.list_table.SetColSize(0, 240)

    def on_text(self, number=None):
        "controle en actie bij invullen/aanpassen aantal regels"
        try:
            cur_rows = int(self.rows_text.value())
        except ValueError:
            gui.QMessageBox.information(self, self.title,
                'Number must be numeric integer','')
            return
        num_rows = self.list_table.rowCount()
        if num_rows > cur_rows:
            for idx in range(num_rows-1, cur_rows-1, -1):
                self.list_table.removeRow(idx)
        elif cur_rows > num_rows:
            for idx in range(num_rows, cur_rows):
                self.list_table.insertRow(idx)
                ## self.list_table.SetRowLabelValue(idx, '')

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        """bij OK: de opgebouwde list via self.dialog_data doorgeven
        aan het mainwindow
        """
        list_type = str(self.type_select.currentText()[0]) + "l"
        list_data = []
        for row in range(self.list_table.rowCount()):
            list_item = [str(self.list_table.item(row, 0).text()),]
            if list_type == "dl":
                list_item.append(str(self.list_table.item(row, 1).text()))
            list_data.append(list_item)
        self._parent.dialog_data = list_type, list_data
        gui.QDialog.done(self, gui.QDialog.Accepted)

class TableDialog(gui.QDialog):
    "dialoog om een tabel toe te voegen"

    def __init__(self, parent):
        self._parent = parent
        self.headings = ['',]
        initialcols, initialrows = 1, 1
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle('Add a table')
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        gbox = gui.QGridLayout() # gui.QGridBagSizer(4, 4)

        gbox.addWidget(gui.QLabel("summary (description):", self), 0, 0)
        self.title_text = gui.QLineEdit(self)
        self.title_text.setMinimumWidth(250)
        gbox.addWidget(self.title_text, 0, 1)

        gbox.addWidget(gui.QLabel("initial number of rows:", self), 1, 0)
        hbox = gui.QHBoxLayout()
        self.rows_text = gui.QSpinBox(self) #.pnl, -1, size = (40, -1))
        self.rows_text.setValue(initialrows)
        self.rows_text.valueChanged.connect(self.on_rows)
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.rows_text)
        hbox.addStretch()
        gbox.addLayout(hbox, 1, 1)

        gbox.addWidget(gui.QLabel("initial number of columns:", self), 2, 0)
        hbox = gui.QHBoxLayout()
        self.cols_text = gui.QSpinBox(self) #.pnl, -1, size = (40, -1))
        self.cols_text.setValue(initialcols)
        self.cols_text.valueChanged.connect(self.on_cols)
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.cols_text)
        hbox.addStretch()
        gbox.addLayout(hbox, 2, 1)

        self.show_titles = gui.QCheckBox('Show Titles')
        self.show_titles.setChecked(True)
        self.show_titles.stateChanged.connect(self.on_check)
        hbox = gui.QHBoxLayout()
        ## hbox.addStretch()
        hbox.addWidget(self.show_titles)
        ## hbox.addStretch()
        gbox.addLayout(hbox, 3, 1)

        self.table_table = gui.QTableWidget(self) # wxgrid.Grid(self.pnl, -1, size = (340, 120))
        self.table_table.setRowCount(initialrows) # de eerste rij is voor de kolomtitels
        self.table_table.setColumnCount(initialcols) # de eerste rij is voor de kolomtitels
        self.table_table.setHorizontalHeaderLabels(self.headings)
        self.hdr = self.table_table.horizontalHeader()
        self.table_table.verticalHeader().setVisible(False)
        self.hdr.setClickable(True)
        self.hdr.sectionClicked.connect(self.on_title)
        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.table_table)
        hbox.addStretch()
        gbox.addLayout(hbox, 4, 0, 1, 2)
        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        self.ok_button = gui.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.on_ok)
        self.ok_button.setDefault(True)
        self.cancel_button = gui.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.on_cancel)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.title_text.setFocus()

    def on_rows(self, number=None):
        "controle en actie bij opgeven aantal regels"
        try:
            cur_rows = int(self.rows_text.value())
        except ValueError:
            gui.QMessageBox.information(self, '',
                'Number must be numeric integer')
            return
        num_rows = self.table_table.rowCount()
        if num_rows > cur_rows:
            for idx in range(num_rows-1, cur_rows-1, -1):
                self.table_table.removeRow(idx)
        elif cur_rows > num_rows:
            for idx in range(num_rows, cur_rows):
                self.table_table.insertRow(idx)
                ## self.table_table.itemAt(idx, 0).setBackgroundColor(core.Qt.darkGray)
                ## self.table_table.SetRowLabelValue(idx, '')

    def on_cols(self, number=None):
        "controle en actie bij opgeven aantal kolommen"
        try:
            cur_cols = int(self.cols_text.value())
        except ValueError:
            gui.QMessageBox.information(self, '',
                'Number must be numeric integer')
            return
        num_cols = self.table_table.columnCount()
        if num_cols > cur_cols:
            for idx in range(num_cols-1, cur_cols-1, -1):
                self.table_table.removeColumn(idx)
                self.headings.pop()
        elif cur_cols > num_cols:
            for idx in range(num_cols, cur_cols):
                self.table_table.insertColumn(idx)
                self.headings.append('')
                self.table_table.setHorizontalHeaderLabels(self.headings)
                ## self.table_table.SetColLabelValue(idx,'')

    def on_check(self, number=None):
        self.hdr.setVisible(bool(number))

    def on_title(self, col):
        "opgeven titel bij klikken op kolomheader mogelijk maken"
        txt, ok = gui.QInputDialog.getText(self, 'Add a table',
            'Enter a title for this column:', gui.QLineEdit.Normal, "")
        if txt:
            self.headings[col] = txt
            self.table_table.setHorizontalHeaderLabels(self.headings)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

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
                rowitems.append(str(self.table_table.item(row, col).text()))
            items.append(rowitems)
        self._parent.dialog_data = (summary, self.show_titles.isChecked(),
            self.headings, items)
        gui.QDialog.done(self, gui.QDialog.Accepted)

class ScrolledTextDialog(gui.QDialog):
    """dialoog voor het tonen van validatieoutput

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title='', data='', htmlfile='', fromdisk=False,
            size=(600, 400)):
        self._parent = parent
        self.htmlfile = htmlfile
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.resize(size[0], size[1])
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        self.message = gui.QLabel(self)
        if fromdisk:
            self.message.setText("\n".join((
                "Validation results are for the file on disk",
                "some errors/warnings may already have been corrected by "
                    "BeautifulSoup",
                "(you'll know when they don't show up inthe tree or text view",
                " or when you save the file in memory back to disk)")))
        hbox.addWidget(self.message)
        vbox.addLayout(hbox)
        hbox = gui.QHBoxLayout()
        text = gui.QTextEdit(self)
        text.setReadOnly(True)
        hbox.addWidget(text)
        vbox.addLayout(hbox)
        hbox = gui.QHBoxLayout()
        ok_button = gui.QPushButton('&Ok', self)
        ok_button.clicked.connect(self.close)
        ok_button.setDefault(True)
        if htmlfile:
            show_button = gui.QPushButton('&View submitted source', self)
            show_button.clicked.connect(self.show_source)
        hbox.addStretch()
        hbox.addWidget(ok_button)
        if htmlfile:
            hbox.addWidget(show_button)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        if htmlfile:
            data = ed.EditorMixin.validate(self, htmlfile)
        if data:
            text.setPlainText(data)

    def show_source(self, evt=None):
        with open(self.htmlfile) as f_in:
            data = ''.join([x for x in f_in])
        if data:
            dlg = CodeViewDialog(self, "Submitted source", data=data)
            dlg.show()

class CodeViewDialog(gui.QDialog):
    """dialoog voor het tonen van de broncode

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    ## ARROW_MARKER_NUM = 8

    def __init__(self, parent, title='', caption = '', data='', size=(600, 400)):
        "create a window with a scintilla text widget and an ok button"
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.resize(size[0], size[1])
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        hbox.addWidget(gui.QLabel(caption, self))
        vbox.addLayout(hbox)
        hbox = gui.QHBoxLayout()
        self.text = sci.QsciScintilla(self)
        self.setup_text()
        self.text.setText(data)
        self.text.setReadOnly(True)
        hbox.addWidget(self.text)
        vbox.addLayout(hbox)
        hbox = gui.QHBoxLayout()
        ok_button = gui.QPushButton('&Ok', self)
        ok_button.clicked.connect(self.close)
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

        ## # Clickable margin 1 for showing markers
        ## self.text.setMarginSensitivity(1, True)
        ## self.connect(self.text,
            ## core.SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),
            ## self.text.on_margin_clicked)
        ## self.text.markerDefine(sci.QsciScintilla.RightArrow,
            ## self.ARROW_MARKER_NUM)
        ## self.text.setMarkerBackgroundColor(gui.QColor("#ee1111"),
            ## self.ARROW_MARKER_NUM)

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

