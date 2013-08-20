# -*- coding: utf-8 -*-

"PyQt4 versie van mijn op een treeview gebaseerde HTML-editor"

import os
import sys
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import PyQt4.QtWebKit as webkit
import ashe.ashe_mixin as ed
import bs4 as bs # BeautifulSoup as bs

PPATH = os.path.split(__file__)[0]
if os.name == "nt":
    HMASK = "HTML files (*.htm *.html);;All files (*.*)"
elif os.name == "posix":
    HMASK = "HTML files (*.htm *.HTM *.html *.HTML);;All files (*.*)"
IMASK = "All files (*.*)"
DESKTOP = ed.DESKTOP
CMSTART = ed.CMSTART
ELSTART = ed.ELSTART
CMELSTART = ed.CMELSTART
DTDSTART = ed.DTDSTART
BL = ed.BL
TITEL = ed.TITEL

def comment_out(node, commented):
    "subitem(s) (ook) op commentaar zetten"
    count = node.childCount()
    for idx in range(count):
        subnode = node.child(idx)
        txt = str(subnode.text(0))
        if commented:
            if not txt.startswith(CMSTART):
                subnode.setText(0, " ".join((CMSTART, txt)))
        else:
            if txt.startswith(CMSTART):
                subnode.setText(0, txt.split(None, 1)[1])
        comment_out(subnode, commented)

class DTDDialog(gui.QDialog):
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
        print(self.dtd_list)
        for cap, dtd, radio in self.dtd_list:
        ## for item in self.dtd_list:
            ## print item
            ## cap, dtd, radio = item
            if radio and radio.isChecked():
                self._parent.dialog_data = dtd
                break
        gui.QDialog.done(self, gui.QDialog.Accepted)

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
            if not link.startswith('http://') and not link.startswith('/'):
                if self._parent.xmlfn:
                    whereami = self._parent.xmlfn
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
        fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", loc,
            HMASK)
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
            if not link.startswith('http://') and not link.startswith('/'):
                if self._parent.xmlfn:
                    whereami = self._parent.xmlfn
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

        self.table_table = gui.QTableWidget(self) # wxgrid.Grid(self.pnl, -1, size = (340, 120))
        self.table_table.setRowCount(initialrows) # de eerste rij is voor de kolomtitels
        self.table_table.setColumnCount(initialcols) # de eerste rij is voor de kolomtitels
        self.table_table.setHorizontalHeaderLabels(self.headings)
        hdr = self.table_table.horizontalHeader()
        self.table_table.verticalHeader().setVisible(False)
        hdr.setClickable(True)
        hdr.sectionClicked.connect(self.on_title)
        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.table_table)
        hbox.addStretch()
        gbox.addLayout(hbox, 3, 0, 1, 2)
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
        self._parent.dialog_data = summary, self.headings, items
        gui.QDialog.done(self, gui.QDialog.Accepted)

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
        iscomment = False
        if tag:
            x = tag.split(None, 1)
            if x[0] == CMSTART:
                iscomment = True
                self.comment_button.toggle()
                x = x[1].split(None, 1)
            if x[0] == ELSTART:
                x = x[1].split(None, 1)
            self.tag_text.setText(x[0])
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
        self.attr_table.verticalHeader().setVisible(False)
        ## self.attr_table.SetColSize(1, tbl.Size[0] - 162) # 178) # 160)
        if attrs:
            for attr, value in attrs.items():
                idx = self.attr_table.rowCount()
                self.attr_table.insertRow(idx)
                item = gui.QTableWidgetItem(attr)
                self.attr_table.setItem(idx, 0, item)
                item = gui.QTableWidgetItem(value)
                self.attr_table.setItem(idx, 1, item)
        else:
            self.row = -1
        hbox.addStretch()
        hbox.addWidget(self.attr_table)
        hbox.addStretch()
        box.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        self.add_button = gui.QPushButton('&Add Attribute', self)
        self.add_button.clicked.connect(self.on_add)
        self.delete_button = gui.QPushButton('&Delete Selected', self)
        self.delete_button.clicked.connect(self.on_del)
        hbox.addStretch()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.delete_button)
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
        idx = self.attr_table.rowCount()
        self.attr_table.insertRow(idx)
        pos = self.attr_table.rowCount()
        item = gui.QTableWidgetItem('')
        self.attr_table.setItem(pos, 0, item)
        # onderstaande zaken werken niet om de focus op het nieuwe attribuut te krijgen
        ## self.attr_table.editItem(self.attr_table.item(pos, 0))
        ## self.attr_table.setCurrentItem(item)
        ## self.attr_table.setCurrentCell(pos, 0)
        self.attr_table.setFocus()

    def on_del(self, evt=None):
        "attribuut verwijderen"
        row = self.attr_table.currentRow()
        if row or row == 0:
            self.attr_table.removeRow(row)
        else:
            gui.QMessageBox.information(self, 'Delete attribute',
                "press Enter on this item first")

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        "controle bij OK aanklikken"
        tag = str(self.tag_text.text())
        okay = True
        test = ed.tagtest
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
            attrs[name] = value
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
        iscomment = False
        if text is None:
            text = ''
        else:
            if text.startswith(CMSTART):
                iscomment = True
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

class VisualTree(gui.QTreeWidget):
    def __init__(self, parent):
        self._parent = parent
        gui.QTreeWidget.__init__(self)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.InternalMove)
        self.setDropIndicatorShown(True)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.x(), event.y())
        if item and item != self._parent.top:
            if str(item.text(0)).startswith(ELSTART) and item.childCount() == 0:
                self._parent.edit()
                return
        gui.QTreeWidget.mouseDoubleClickEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == core.Qt.RightButton:
            xc, yc = event.x(), event.y()
            item = self.itemAt(xc, yc)
            if item and item != self._parent.top:
                self.setCurrentItem(item)
                menu = self._parent.contextmenu()
                menu.exec_(core.QPoint(xc, yc))
                return
        gui.QTreeWidget.mouseReleaseEvent(self, event)

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        dragitem = self.selectedItems()[0]
        gui.QTreeWidget.dropEvent(self, event)
        self._parent.tree_dirty = True
        dropitem = dragitem.parent()
        self.setCurrentItem(dragitem)
        dropitem.setExpanded(True)
        self._parent.refresh_preview()

class ScrolledTextDialog(gui.QDialog):
    """dialoog voor het tonen van validatieoutput

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title='', data='', size=(600, 400)):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.resize(size[0], size[1])
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        text = gui.QTextEdit(self)
        text.setPlainText(data)
        text.setReadOnly(True)
        hbox.addWidget(text)
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

class MainFrame(gui.QMainWindow, ed.EditorMixin):
    "Main GUI"

    def __init__(self, parent, _id, fname=''):
        self.parent = parent
        self.title = "(untitled) - Albert's Simple HTML Editor"
        self.xmlfn = fname
        ## if fn:
            ## self.xmlfn = os.path.abspath(fn)
        ## else:
            ## self.xmlfn = ''
        # bepaalt de bij het scherm passende hoogte en breedte
        # dsp = gui.QDisplay().GetClientArea()
        # high = dsp.height if dsp.height < 900 else 900
        # wide = dsp.width if dsp.width < 1020 else 1020
        gui.QMainWindow.__init__(self) #, parent, _id,
            # pos = (dsp.top, dsp.left),
            # size = (wide, high)
        self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        self.resize(1020, 900)

        self._setup_menu()
        act = gui.QAction(self)
        act.setShortcut(core.Qt.Key_Super_R)
        self.connect(act, core.SIGNAL('triggered()'), self.contextmenu)

        self.pnl = gui.QSplitter(self)
        ## self.pnl.moveSplitter(400, 1)
        self.setCentralWidget(self.pnl)

        self.tree = VisualTree(self)
        self.tree.setItemHidden(self.tree.headerItem(), True)
        self.pnl.addWidget(self.tree)

        self.html = webkit.QWebView(self.pnl) # , -1,
        self.pnl.addWidget(self.html)

        self.sb = self.statusBar()

        self.tree.resize(500, 100)
        self.tree.setFocus()
        # self.Bind(gui.QEVT_CLOSE, self.exit) reimplement self.closeEvent()

        ed.EditorMixin.getsoup(self, fname)
        self.adv_menu.setChecked(True)
        self.refresh_preview()

    def _setup_menu(self):
        self.menulist = (
            '&File', (
                ('&New', 'N', 'C', "Start a new HTML document", self.newxml),
                ('&Open', 'O', 'C', "Open an existing HTML document", self.openxml),
                ('&Save', 'S', 'C', "Save the current document", self.savexml),
                ('Save &As', 'S', 'SC',
                    "Save the current document under a different name",
                    self.savexmlas),
                ('&Revert', 'R', 'C', "Discard all changes since the last save",
                    self.reopenxml),
                ('sep1', ),
                ('E&xit', 'Q', 'C', 'Quit the application', self.close),
                ),
                ), (
            '&View', (
                ('E&xpand All (sub)Levels', '+', 'C',
                    "Show what's beneath the current element", self.expand, True),
                ('&Collapse All (sub)Levels', '-', 'C',
                    "Hide what's beneath the current element", self.collapse, True),
                ('sep1', ),
                ('Advance selection on add/insert', '', '',
                    "Move the selection to the added/pasted item",
                    self.advance_selection_onoff),
                ),
                ), (
            '&Edit', (
                ('Edit', 'F2', '', 'Modify the element/text and/or its attributes',
                    self.edit),
                ('Comment/Uncomment', '#', 'C', 'Comment (out) the current item and '
                    'everything below', self.comment),
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
                ('Add &DTD', '', '', 'Add a document type description', self.add_dtd),
                ('Create &link (under)', '', '', 'Add a link', self.add_link),
                ('Add i&mage (under)', '', '', 'Include an image', self.add_image),
                ('Add l&ist (under)', '', '', 'Create a list', self.add_list),
                ('Add &table (under)', '', '', 'Create a table', self.add_table),
                ('sep1', ),
                ('&Check syntax', '', '', 'Validate HTML with Tidy', self.validate),
                ),
                ), (
            "Help", (
                ('&About', '', '', 'Info about this application', self.about),
                ),
                )
        ## self.menu_id = {}
        menu_bar = self.menuBar()
        self.contextmenu_items = []
        for menu_text, data in self.menulist:
            menu = gui.QMenu(menu_text, self)
            for item in data:
                if len(item) == 1:
                    menu.addSeparator()
                    continue
                menuitem_text, hotkey, modifiers, status_text, callback = item[:5]
                if 'A' in modifiers:
                    hotkey = "+".join(("Alt",hotkey))
                if 'C' in modifiers:
                    hotkey = "+".join(("Ctrl",hotkey))
                if 'S' in modifiers:
                    hotkey = "+".join(("Shift",hotkey))
                ## self.menu_id[menuitem_text] = gui.QNewId()
                ## caption = menuitem_text.ljust(40) + hotkey
                act = gui.QAction(menuitem_text, self)
                menu.addAction(act)
                act.setStatusTip(status_text)
                act.setShortcut(hotkey)
                self.connect(act, core.SIGNAL('triggered()'), callback)
                if menuitem_text.startswith('Advance selection'):
                    act.setCheckable(True)
                    self.adv_menu = act
                elif menu_text == '&View':
                    self.contextmenu_items.append(('A', act))
                elif menuitem_text == 'Add &DTD':
                    self.dtd_menu = act
                if menu_text in ('&Edit', '&HTML'):
                    self.contextmenu_items.append(('M', menu))
            if menu_text == '&View':
                self.contextmenu_items.append(('', ''))
            menu_bar.addMenu(menu)

    def _check_tree(self):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)
        retourneert 1 = Yes, 0 = No, -1 = Cancel
        """
        if self.tree_dirty:
            retval = dict(zip((gui.QMessageBox.Yes, gui.QMessageBox.No,
                gui.QMessageBox.Cancel), (1, 0, -1)))
            hlp = gui.QMessageBox.question(self, self.title, "HTML data has been "
                "modified - save before continuing?",
                gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel,
                defaultButton = gui.QMessageBox.Yes)
            if hlp == gui.QMessageBox.Yes:
                self.savexml()
            return retval[hlp]

    def close(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna afsluiten"""
        if self._check_tree() != -1:
            gui.QMainWindow.close(self)

    def newxml(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna nieuwe html aanmaken"""
        if self._check_tree() != -1:
            try:
                ed.EditorMixin.getsoup(self, fname = None)
                self.adv_menu.setChecked(True)
                self.sb.showMessage("started new document")
                self.refresh_preview()
            except Exception as err:
                gui.QMessageBox.information(self, self.title, str(err))

    def openxml(self, evt=None):
        """kijken of er wijzigingen opgeslagen moeten worden
        daarna een html bestand kiezen"""
        if self._check_tree() != -1:
            loc = os.path.dirname(self.xmlfn) if self.xmlfn else os.getcwd()
            fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", loc,
                HMASK)
            if fnaam:
                ## try:
                    ed.EditorMixin.getsoup(self, fname=str(fnaam))
                    self.adv_menu.setChecked(True)
                    self.sb.showMessage("loaded {}".format(self.xmlfn))
                    self.refresh_preview()
                ## except Exception as err:
                    ## gui.QMessageBox.information(self, self.title, str(err))

    def savexml(self, evt=None):
        "save html to file"
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.data2soup()
            try:
                self.soup2file()
            except IOError as err:
                gui.QMessageBox.information(self, self.title, str(err))
                return
            self.sb.showMessage("saved {}".format(self.xmlfn))

    def savexmlas(self, evt=None):
        """vraag bestand om html op te slaan
        bestand opslaan en naam in titel en root element zetten"""
        name = gui.QFileDialog.getSaveFileName(self, "Save file as ...",
            self.xmlfn or os.getcwd(),
            HMASK)
        if name:
            self.xmlfn = str(name)
            self.data2soup()
            try:
                self.soup2file(saveas=True)
            except IOError as err:
                gui.QMessageBox.information(self, self.title, str(err))
                return
            self.top.setText(0, self.xmlfn)
            self.setWindowTitle(" - ".join((os.path.basename(self.xmlfn), TITEL)))
            self.sb.showMessage("saved as {}".format(self.xmlfn))

    def reopenxml(self, evt=None):
        """onvoorwaardelijk html bestand opnieuw laden"""
        try:
            ed.EditorMixin.getsoup(self, fname = self.xmlfn)
            self.adv_menu.setChecked(True)
            self.sb.showMessage("reloaded {}".format(self.xmlfn))
            self.refresh_preview()
        except Exception as err:
            gui.QMessageBox(self, self.title, str(err))

    def advance_selection_onoff(self, event=None):
        self.advance_selection_on_add = self.adv_menu.isChecked()

    def mark_dirty(self, state):
        ed.EditorMixin.mark_dirty(self, state)
        title = str(self.windowTitle())
        if state:
            if not title.endswith(' *'):
                title = title + ' *'
        else:
            title = title.rstrip(' *')
        self.setWindowTitle(title)

    def refresh_preview(self):
        self.data2soup()
        self.html.setHtml(str(self.soup).replace('%SOUP-ENCODING%','utf-8'))
        self.tree.setFocus()

    def about(self, evt=None):
        "toon programma info"
        abouttext = ed.EditorMixin.about(self)
        gui.QMessageBox.information(self, self.title, abouttext)

    def addtreeitem(self, node, naam, data):
        """itemnaam en -data toevoegen aan de interne tree
        referentie naar treeitem teruggeven"""
        newnode = gui.QTreeWidgetItem()
        newnode.setText(0, naam) # self.tree.AppendItem(node, naam)
        # data is ofwel leeg, ofwel een string, ofwel een dictionary
        newnode.setData(0, core.Qt.UserRole, data) # self.tree.SetPyData(newnode, data)
        node.addChild(newnode)
        return newnode

    def addtreetop(self, fname, titel):
        """titel en root item in tree instellen"""
        self.setWindowTitle(titel)
        self.top = gui.QTreeWidgetItem()
        self.top.setText(0, fname)
        self.tree.addTopLevelItem(self.top) # AddRoot(titel)

    def init_tree(self, name=''):
        "nieuwe tree initialiseren"
        self.tree.clear()
        ed.EditorMixin.init_tree(self, name)
        self.adjust_dtd_menu()
        if DESKTOP:
            self.tree.setCurrentItem(self.top)

    def data2soup(self):
        "interne tree omzetten in BeautifulSoup object"
        def expandnode(node, root, data, commented = False):
            "tree item (node) met inhoud (data) toevoegen aan BS node (root)"
            ## print data
            try:
                for att in data:
                    root[str(att)] = str(data[att])
            except TypeError:
                pass
            for ix in range(node.childCount()):
                elm = node.child(ix)
                text = str(elm.text(0))
                data = elm.data(0, core.Qt.UserRole)
                if sys.version < '3':
                    data = data.toPyObject()
                if text.startswith(ELSTART) or text.startswith(CMELSTART):
                    # data is een dict: leeg of een mapping van data op attributen
                    if text.startswith(CMSTART):
                        text = text.split(None, 1)[1]
                        if not commented:
                            is_comment = True
                            soup = bs.BeautifulSoup()
                            sub = soup.new_tag(text.split()[1])
                            expandnode(elm, sub, data, is_comment)
                            sub = bs.Comment(str(sub)) # .decode("utf-8")) niet voor Py3
                        else:
                            is_comment = False
                            sub = self.soup.new_tag(text.split()[1])
                    else:
                        is_comment = False
                        sub = self.soup.new_tag(text.split()[1])
                    root.append(sub) # insert(0,sub)
                    if not is_comment:
                        expandnode(elm, sub, data, commented)
                else:
                    sub = bs.NavigableString(str(data)) #.decode("utf-8")) niet voor Py3
                    if text.startswith(CMSTART) and not commented:
                        sub = bs.Comment(data) # .decode("utf-8")) niet voor Py3
                    root.append(sub) # data.decode("latin-1")) # insert(0,sub)
        self.soup = bs.BeautifulSoup() # self.root.originalEncoding)
        count = self.top.childCount()
        for ix in range(count):
            tag = self.top.child(ix)
            text = str(tag.text(0))
            ## print tag, text
            ## print text.split(None, 1)[1]
            ## print text.split(None, 2)[1]
            data = tag.data(0, core.Qt.UserRole)
            if sys.version < '3':
                data = data.toPyObject()
            if text.startswith(DTDSTART):
                root = bs.Declaration(str(data))
                self.soup.append(root)
            elif text.startswith(ELSTART):
                root = self.soup.new_tag(text.split(None, 2)[1])
                self.soup.append(root)
                expandnode(tag, root, data)

    def adjust_dtd_menu(self):
        if self.has_dtd:
            self.dtd_menu.setText('Remove &DTD')
            self.dtd_menu.setStatusTip('Remove the document type declaration')
        else:
            self.dtd_menu.setText('Add &DTD')
            self.dtd_menu.setStatusTip('Add a document type description')
        ## value = not self.has_dtd
        ## self.dtd_menu.Enable(value)

    def contextmenu(self, item=None, pos=None):
        'build/show context menu'
        menu = gui.QMenu()
        for itemtype, item in self.contextmenu_items:
            if itemtype == 'A':
                menu.addAction(item)
            elif itemtype == 'M':
                menu.addMenu(item)
            else:
                menu.addSeparator()
        return menu

    def checkselection(self):
        "controleer of er wel iets geselecteerd is (behalve de filenaam)"
        sel = True
        self.item = self.tree.currentItem()
        if self.item is None or self.item == self.top:
            gui.QMessageBox.information(self, self.title,
                'You need to select an element or text ''first')
            sel = False
        return sel

    def expand(self, evt=None):
        "expandeer tree vanaf huidige item"
        def expand_all(item):
            for ix in range(item.childCount()):
                sub = item.child(ix)
                sub.setExpanded(True)
                expand_all(sub)
        item = self.tree.currentItem()
        self.tree.expandItem(item)
        expand_all(item)

    def collapse(self, evt=None):
        "collapse huidige item en daaronder"
        def collapse_all(item):
            for ix in range(item.childCount()):
                sub = item.child(ix)
                collapse_all(sub)
                sub.setExpanded(False)
        item = self.tree.currentItem()
        collapse_all(item)
        self.tree.collapseItem(item)

    def comment(self, evt=None):
        "(un)comment zonder de edit dialoog"
        if DESKTOP and not self.checkselection():
            return
        tag = str(self.item.text(0))
        attrs = self.item.data(0, core.Qt.UserRole)
        if sys.version < '3':
            attrs = attrs.toPyObject()
        commented = tag.startswith(CMSTART)
        if commented:
            _, tag = tag.split(None, 1) # CMSTART eraf halen
        under_comment = str(self.item.parent().text(0)).startswith(CMELSTART)
        commented = not commented # het (un)commenten uitvoeren
        if under_comment:
            commented = True
        print("in comment:", tag, attrs)
        if tag.startswith(ELSTART):
            _, tag = tag.split(None, 1) # ELSTART eraf halen
            self.item.setText(0, ed.getelname(tag, attrs, commented))
            self.item.setData(0, core.Qt.UserRole, attrs)
            comment_out(self.item, commented)
        else:
            ## txt = CMSTART + " " + tag if commented else tag
            self.item.setText(0, ed.getshortname(tag, commented))
            self.item.setData(0, core.Qt.UserRole, tag)

    def edit(self, evt=None):
        "start edit m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        data = str(self.item.text(0))
        under_comment = str(self.item.parent().text(0)).startswith(CMELSTART)
        modified = False
        if data.startswith(ELSTART) or data.startswith(CMELSTART):
            attrdict = self.item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                attrdict = attrdict.toPyObject()
            was_commented = data.startswith(CMSTART)
            edt = ElementDialog(self, title = 'Edit an element', tag = data,
                attrs = attrdict).exec_()
            if edt == gui.QDialog.Accepted:
                modified = True
                tag, attrs, commented = self.dialog_data
                if under_comment:
                    commented = True
                print("in edit:", attrs)
                if tag != data or attrs != attrdict:
                    self.item.setText(0, ed.getelname(tag, attrs, commented))
                self.item.setData(0, core.Qt.UserRole, attrs)
                if commented != was_commented:
                    comment_out(self.item, commented)
        else:
            txt = CMSTART + " " if data.startswith(CMSTART) else ""
            data = self.item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                data = str(data.toPyObject())
            edt = TextDialog(self, title='Edit Text', text = txt + data).exec_()
            if edt == gui.QDialog.Accepted:
                modified = True
                txt, commented = self.dialog_data
                if under_comment:
                    commented = True
                self.item.setText(0, ed.getshortname(txt, commented))
                self.item.setData(0, core.Qt.UserRole, txt)
        if modified:
            self.mark_dirty(True)
            self.refresh_preview()

    def copy(self, evt=None, cut=False, retain=True):
        "start copy/cut/delete actie"
        def push_el(elm, result):
            "subitem(s) toevoegen aan copy buffer"
            text = str(elm.text(0))
            data = elm.data(0, core.Qt.UserRole)
            if sys.version < '3':
                data = data.toPyObject()
            atrlist = []
            if text.startswith(ELSTART):
                num = elm.childCount()
                for idx in range(num):
                    node = elm.child(idx)
                    x = push_el(node, atrlist)
            result.append((text, data, atrlist))
            return result
        if DESKTOP and not self.checkselection():
            return
        if self.item == self.root:
            gui.QMessageBox.information(self, self.title, "Can't %s the root" % txt)
            return
        text = str(self.item.text(0))
        data = self.item.data(0, core.Qt.UserRole)
        if sys.version < '3':
            data = data.toPyObject()
        txt = 'cut' if cut else 'copy'
        ## try:
        if str(data).startswith(DTDSTART):
            gui.QMessageBox.information(self, self.title,
                "use the HTML menu's DTD option")
            return
        if retain:
            if text.startswith(ELSTART):
                self.cut_el = []
                self.cut_el = push_el(self.item, self.cut_el)
                self.cut_txt = None
            else:
                self.cut_el = None
                self.cut_txt = data
        if cut:
            parent = self.item.parent()
            ix = parent.indexOfChild(self.item)
            if ix > 0:
                ix -= 1
                prev = parent.child(ix)
            else:
                prev = parent
                if prev == self.root:
                    prev = parent.child(ix+1)
            parent.removeChild(self.item)
            self.mark_dirty(True)
            self.tree.setCurrentItem(prev)
            self.refresh_preview()

    def paste(self, evt=None, before=True, below=False):
        "start paste actie"
        def zetzeronder(node, elm, pos = -1):
            "paste copy buffer into tree"
            subnode = gui.QTreeWidgetItem()
            subnode.setText(0, elm[0])
            subnode.setData(0, core.Qt.UserRole, elm[1])
            if pos == -1:
                node.addChild(subnode)
            else:
                node.insertChild(pos, subnode)
            for item in elm[2]:
                zetzeronder(subnode, item)
            return subnode
        if DESKTOP and not self.checkselection():
            return
        data = self.item.data(0, core.Qt.UserRole)
        if sys.version < '3':
            data = data.toPyObject()
        if below:
            text = str(self.item.text(0))
            if text.startswith(CMSTART):
                gui.QMessageBox.information(self, self.title, "Can't paste below comment")
                return
            if not text.startswith(ELSTART):
                gui.QMessageBox.information(self, self.title, "Can't paste below text")
                return
        if self.item == self.root:
            if before:
                gui.QMessageBox.information(self, self.title,
                    "Can't paste before the root")
                return
            else:
                gui.QMessageBox.information(self, self.title,
                    "Pasting as first element below root")
                below = True
        if self.cut_txt:
            item = ed.getshortname(self.cut_txt)
            data = self.cut_txt
            node = gui.QTreeWidgetItem()
            node.setText(0, item)
            node.setData(0, core.Qt.UserRole, data)
            if below:
                self.item.addChild(node)
            else:
                add_to = self.item.parent()
                idx = add_to.indexOfChild(self.item)
                if not before:
                    idx += 1
                if idx >= add_to.childCount():
                    add_to.addChild(node)
                else:
                    add_to.insertChild(idx, node)
            if self.advance_selection_on_add:
                self.tree.setCurrentItem(node)
        else:
            if below:
                add_to = self.item
                idx = -1
            else:
                add_to = self.item.parent()
                idx = add_to.indexOfChild(self.item)
                cnt = add_to.childCount()
                if not before:
                    idx += 1
                if idx == cnt:
                    idx -= 1
            new_item = zetzeronder(add_to, self.cut_el[0], idx)
            if self.advance_selection_on_add:
                self.tree.setCurrentItem(new_item)
        self.mark_dirty(True)
        self.refresh_preview()

    def add_text(self, evt=None, before=True, below=False):
        "tekst toevoegen onder huidige element"
        if DESKTOP and not self.checkselection():
            return
        if below and not str(self.item.text(0)).startswith(ELSTART):
            gui.MessageBox.information(self, self.title, "Can't add text below text")
            return
        edt = TextDialog(self, title="New Text").exec_()
        if edt == gui.QDialog.Accepted:
            txt, commented = self.dialog_data
            if below:
                text = str(self.item.text(0))
            else:
                parent = self.item.parent()
                text = str(parent.text(0))
            under_comment = text.startswith(CMSTART)
            text = ed.getshortname(txt, commented or under_comment)
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, text)
            new_item.setData(0, core.Qt.UserRole, txt)
            if below:
                self.item.addChild(new_item)
            else:
                ix = parent.indexOfChild(self.item)
                if not before:
                    ix += 1
                if ix >= parent.childCount():
                    parent.addChild(new_item)
                else:
                    parent.insertChild(ix, new_item)
            if self.advance_selection_on_add:
                self.tree.setCurrentItem(new_item)
            self.mark_dirty(True)
            self.refresh_preview()
            self.item.setExpanded(True)

    def insert(self, evt=None, before=True, below=False):
        "start invoeg actie"
        if DESKTOP and not self.checkselection():
            return
        if below:
            text = str(self.item.text(0))
            if text.startswith(CMSTART):
                gui.QMessageBox.information(self, self.title,
                    "Can't insert below comment")
                return
            if not text.startswith(ELSTART) and not text.startswith(CMELSTART):
                gui.QMessageBox.information(self, self.title,
                    "Can't insert below text")
                return
            under_comment = text.startswith(CMSTART)
            where = "under"
        elif before:
            where = "before"
        else:
            where = "after"
        edt = ElementDialog(self, title="New element (insert {0})".format(where)).exec_()
        if edt == gui.QDialog.Accepted:
            modified = True
            tag, attrs, commented = self.dialog_data
            if below:
                text = str(self.item.text(0))
            else:
                parent = self.item.parent()
                text = str(parent.text(0))
            under_comment = text.startswith(CMSTART)
            text = ed.getelname(tag, attrs, commented or under_comment)
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, text)
            new_item.setData(0, core.Qt.UserRole, attrs)

            if below:
                self.item.addChild(new_item)
            else:
                ix = parent.indexOfChild(self.item)
                if not before:
                    ix += 1
                if ix >= parent.childCount():
                    parent.addChild(new_item)
                else:
                    parent.insertChild(ix, new_item)
            if self.advance_selection_on_add:
                self.tree.setCurrentItem(new_item)
            self.mark_dirty(True)
            self.refresh_preview()
            self.item.setExpanded(True)

    def add_dtd(self, evt=None):
        "start toevoegen dtd m.b.v. dialoog"
        if self.has_dtd:
            self.top.removeChild(self.top.child(0))
            self.has_dtd = False
        else:
            edt = DTDDialog(self).exec_()
            if edt == gui.QDialog.Rejected:
                return
            node = gui.QTreeWidgetItem()
            self.top.insertChild(0, node)
            dtd = self.dialog_data
            node.setText(0, ed.getshortname(dtd))
            node.setData(0, core.Qt.UserRole, dtd.rstrip())
            self.has_dtd = True
        self.adjust_dtd_menu()
        self.mark_dirty(True)
        self.refresh_preview()
        self.tree.scrollToItem(self.top.child(0))

    def add_link(self, evt=None):
        "start toevoegen link m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox.information(self, self.title, "Can't do this below text")
            return
        edt = LinkDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            txt, data = self.dialog_data
            node = gui.QTreeWidgetItem()
            node.setText(0, ed.getelname('a', data))
            node.setData(0, core.Qt.UserRole, data)
            self.item.addChild(node)
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, ed.getshortname(txt))
            new_item.setData(0, core.Qt.UserRole, txt)
            node.addChild(new_item)
            self.mark_dirty(True)
            self.refresh_preview()

    def add_image(self, evt=None):
        "start toevoegen image m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox.information(self, self.title, "Can't do this below text")
            return
        edt = ImageDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            data = self.dialog_data
            node = gui.QTreeWidgetItem()
            node.setText(0, ed.getelname('a', data))
            node.setData(0, core.Qt.UserRole, data)
            self.item.addChild(node)
            self.mark_dirty(True)
            self.refresh_preview()

    def add_list(self, evt=None):
        "start toevoegen list m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox("Can't do this below text", self.title)
            return
        edt = ListDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            list_type, list_data = self.dialog_data
            itemtype = "dt" if list_type == "dl" else "li"
            new_item = gui.QTreeWidgetItem()
            self.item.addChild(new_item)
            new_item.setText(0, ed.getelname(list_type))

            for list_item in list_data:
                new_subitem = gui.QTreeWidgetItem()
                new_item.addChild(new_subitem)
                new_subitem.setText(0, ed.getelname(itemtype))
                data = list_item[0]
                node = gui.QTreeWidgetItem()
                new_subitem.addChild(node)
                node.setText(0, ed.getshortname(data))
                node.setData(0, core.Qt.UserRole, data)
                if list_type == "dl":
                    new_subitem = gui.QTreeWidgetItem()
                    new_item.addChild(new_subitem)
                    new_subitem.setText(0, ed.getelname('dd'))
                    data = list_item[1]
                    node = gui.QTreeWidgetItem()
                    new_subitem.addChild(node)
                    node.setText(0, ed.getshortname(data))
                    node.setData(0, core.Qt.UserRole, data)
            self.mark_dirty(True)
            self.refresh_preview()

    def add_table(self, evt=None):
        "start toevoegen tabel m.b.v. dialoog"
        if DESKTOP and not self.checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox("Can't do this below text", self.title)
            return
        edt = TableDialog(self).exec_()
        if edt == gui.QDialog.Accepted:
            summary, headers, items = self.dialog_data
            new_item = gui.QTreeWidgetItem()
            self.item.addChild(new_item)
            data = {'summary': summary}
            new_item.setText(0, ed.getelname('table', data))
            new_item.setData(0, core.Qt.UserRole, data)
            new_row = gui.QTreeWidgetItem()
            new_item.addChild(new_row)
            new_row.setText(0, ed.getelname('tr'))
            for head in headers:
                new_head = gui.QTreeWidgetItem()
                new_row.addChild(new_head)
                new_head.setText(0, ed.getelname('th'))
                node = gui.QTreeWidgetItem()
                new_head.addChild(node)
                text = head or BL
                node.setText(0, ed.getshortname(text))
                node.setData(0, core.Qt.UserRole, text)
            for rowitem in items:
                new_row = gui.QTreeWidgetItem()
                new_item.addChild(new_row)
                new_row.setText(0, ed.getelname('tr'))
                for cellitem in rowitem:
                    new_cell = gui.QTreeWidgetItem()
                    new_row.addChild(new_cell)
                    new_cell.setText(0, ed.getelname('td'))
                    text = cellitem
                    node = gui.QTreeWidgetItem()
                    new_cell.addChild(node)
                    node.setText(0, ed.getshortname(text))
                    node.setData(0, core.Qt.UserRole, text)
            self.mark_dirty(True)
            self.refresh_preview()

    def validate(self, evt=None):
        if self.tree_dirty or not self.xmlfn:
            htmlfile = '/tmp/ashe_check.html'
            fromdisk = False
            self.data2soup()
            with open(htmlfile, "w") as f_out:
                f_out.write(str(self.soup))
        else:
            htmlfile = self.xmlfn
            fromdisk = True
        data = ed.EditorMixin.validate(self, htmlfile, fromdisk)
        dlg = ScrolledTextDialog(self, "Validation output", data).show()

def ashe_gui(args):
    "start main GUI"
    fname = ''
    if len(args) > 1:
        fname = args[1]
        ## if len(args) > 2:
            ## print args[2]
        if not os.path.exists(fname):
            ## fname = os.path.join(args[2], args[1])
            print('Kan file niet openen, geef s.v.p. een absoluut pad op\n')
    app = gui.QApplication(sys.argv)
    ## (redirect = True, filename = "/home/albert/htmledit/ashe/ashe.log")
    ## print "\n-- new entry --\n"
    if fname:
        frm = MainFrame(None, -1, fname = fname)
    else:
        frm = MainFrame(None, -1)
    frm.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    ashe_gui(sys.argv)
