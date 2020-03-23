"""PyQt5 versie van mijn op een treeview gebaseerde HTML-editor

custom dialogen
"""
import os
## import sys
import string
# import pathlib
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import PyQt5.Qsci as sci  # scintilla
from ashe.shared import CMSTART, VAL_MESSAGE, analyze_element


class ElementDialog(qtw.QDialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, parent, title='', tag='', attrs=None):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self._parent.appicon)
        tagdata = analyze_element(tag, attrs)
        tag_text, iscomment, style_text, styledata, self.has_style, is_stylesheet = tagdata
        self.is_style_tag = tag_text == 'style'
        if self.is_style_tag or self.has_style:
            self._parent.editor.cssm.setup_flags(styledata, is_stylesheet)
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        lbl = qtw.QLabel("element name:", self)
        self.tag_text = qtw.QLineEdit(self)
        self.tag_text.setMinimumWidth(250)
        self.comment_button = qtw.QCheckBox('&Comment(ed)', self)
        self.is_stylesheet = False
        self.styledata = ''
        self.tag_text.setText(tag_text)
        if iscomment:
            self.comment_button.toggle()
        hbox.addWidget(lbl)
        hbox.addWidget(self.tag_text)
        hbox.addWidget(self.comment_button)
        vbox.addLayout(hbox)

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)

        box = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        self.attr_table = qtw.QTableWidget(self)
        self.attr_table.setColumnCount(2)
        self.attr_table.setHorizontalHeaderLabels(['attribute', 'value'])
        hdr = self.attr_table.horizontalHeader()
        hdr.resizeSection(0, 102)
        hdr.resizeSection(1, 152)
        hdr.setStretchLastSection(True)
        self.attr_table.verticalHeader().setVisible(False)
        self.attr_table.setTabKeyNavigation(False)
        if attrs:
            for attr, value in attrs.items():
                idx = self.attr_table.rowCount()
                self.attr_table.insertRow(idx)
                item = qtw.QTableWidgetItem(attr)
                self.attr_table.setItem(idx, 0, item)
                if attr == 'style':
                    item.setFlags(item.flags() & (not core.Qt.ItemIsEditable))
                item = qtw.QTableWidgetItem(value)
                self.attr_table.setItem(idx, 1, item)
                if attr == 'style':
                    item.setFlags(item.flags() & (not core.Qt.ItemIsEditable))
        else:
            self.row = -1
        hbox.addWidget(self.attr_table)
        box.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.add_button = qtw.QPushButton('&Add Attribute', self)
        self.add_button.clicked.connect(self.on_add)
        self.delete_button = qtw.QPushButton('&Delete Selected', self)
        self.delete_button.clicked.connect(self.on_del)
        self.style_button = qtw.QPushButton(style_text, self)
        if self._parent.editor.cssedit_available:
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

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        vbox.addLayout(hbox)
        hbox.addStretch()

        self.setLayout(vbox)

    def on_add(self):
        "attribuut toevoegen"
        self.attr_table.setFocus()
        idx = self.attr_table.rowCount()
        self.attr_table.insertRow(idx)
        self.attr_table.setCurrentCell(idx, 0)

    def on_del(self):
        "attribuut verwijderen"
        row = self.attr_table.currentRow()
        if row or row == 0:
            self.attr_table.removeRow(row)
        else:
            qtw.QMessageBox.information(self, 'Delete attribute',
                                        "press Enter on this item first")

    def on_style(self):
        "adjust style attributes"
        tag = self.tag_text.text()
        fname = ''
        test = self.attr_table.findItems('href', core.Qt.MatchFixedString)
        for item in test:
            col = self.attr_table.column(item)
            row = self.attr_table.row(item)
            if col == 0:
                fname = self.attr_table.item(row, 1).text()
        # FIXME: dit werkt(e) niet voor een inline style
        self._parent.editor.cssm.call_editor(tag, fname, self._parent.app)

    def accept(self):
        "controle bij OK aanklikken"
        # TODO: ensure no duplicate items are added
        tag = str(self.tag_text.text())
        test = string.ascii_letters + string.digits
        for letter in tag:
            if letter not in test:
                qtw.QMessageBox.information(self, self._parent.editor.title,
                                            'Illegal character(s) in tag name')
                break
        commented = self.comment_button.checkState()
        attrs = {}
        for i in range(self.attr_table.rowCount()):
            try:
                name = str(self.attr_table.item(i, 0).text())
                value = str(self.attr_table.item(i, 1).text())
            except AttributeError:
                qtw.QMessageBox.information(self, 'Add an element',
                                            'Press enter on this item first')
                return
            if name != 'style':
                attrs[name] = value
        if self.is_style_tag or self.has_style:
            self.styledata, attrs = self._parent.editor.cssm.check_if_modified(tag, attrs)
        self._parent.dialog_data = tag, attrs, commented
        super().accept()


class TextDialog(qtw.QDialog):
    """dialoog om een tekst element op te voeren of aan te passen
    biedt tevens de mogelijkheid de tekst "op commentaar" te zetten"""

    def __init__(self, parent, title='', text=None):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        self.comment_button = qtw.QCheckBox('&Comment(ed)', self)
        if text is None:
            text = ''
        else:
            if text.startswith(CMSTART):
                self.comment_button.toggle()
                try:
                    dummy, text = text.split(None, 1)
                except ValueError:
                    text = ""
        hbox.addWidget(self.comment_button)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.data_text = qtw.QTextEdit(self)
        self.data_text.resize(340, 175)
        self.data_text.setText(text)
        hbox.addWidget(self.data_text)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.data_text.setFocus()

    def accept(self):
        "pass changed data to parent"
        self._parent.dialog_data = (str(self.data_text.toPlainText()),
                                    self.comment_button.checkState())
        super().accept()


class SearchDialog(qtw.QDialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self._parent = parent

        self.cb_element = qtw.QLabel('Element', self)
        lbl_element = qtw.QLabel("name:", self)
        self.txt_element = qtw.QLineEdit(self)
        self.txt_element.textChanged.connect(self.set_search)

        self.cb_attr = qtw.QLabel('Attribute', self)
        lbl_attr_name = qtw.QLabel("name:", self)
        self.txt_attr_name = qtw.QLineEdit(self)
        self.txt_attr_name.textChanged.connect(self.set_search)
        lbl_attr_val = qtw.QLabel("value:", self)
        self.txt_attr_val = qtw.QLineEdit(self)
        self.txt_attr_val.textChanged.connect(self.set_search)

        self.cb_text = qtw.QLabel('Text', self)
        lbl_text = qtw.QLabel("value:", self)
        self.txt_text = qtw.QLineEdit(self)
        self.txt_text.textChanged.connect(self.set_search)

        self.lbl_search = qtw.QLabel('', self)

        self.btn_ok = qtw.QPushButton('&Ok', self)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_ok.setDefault(True)
        self.btn_cancel = qtw.QPushButton('&Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)

        sizer = qtw.QVBoxLayout()

        gsizer = qtw.QGridLayout()

        gsizer.addWidget(self.cb_element, 0, 0)
        vsizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(lbl_element)
        hsizer.addWidget(self.txt_element)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 0, 1)

        vsizer = qtw.QVBoxLayout()
        vsizer.addSpacing(5)
        vsizer.addWidget(self.cb_attr)
        vsizer.addStretch()
        gsizer.addLayout(vsizer, 1, 0)
        vsizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(lbl_attr_name)
        hsizer.addWidget(self.txt_attr_name)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(lbl_attr_val)
        hsizer.addWidget(self.txt_attr_val)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 1, 1)

        gsizer.addWidget(self.cb_text, 2, 0)
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(lbl_text)
        hsizer.addWidget(self.txt_text)
        gsizer.addLayout(hsizer, 2, 1)
        sizer.addLayout(gsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(self.lbl_search)
        sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
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
        out = self._parent.editor.build_search_spec(self.txt_element.text(),
                                                    self.txt_attr_name.text(),
                                                    self.txt_attr_val.text(),
                                                    self.txt_text.text(), '')
        self.lbl_search.setText(out)
        self.search_specs = out

    def accept(self):
        """confirm dialog and pass changed data to parent"""
        ele = str(self.txt_element.text())
        attr_name = str(self.txt_attr_name.text())
        attr_val = str(self.txt_attr_val.text())
        text = str(self.txt_text.text())
        if not any((ele, attr_name, attr_val, text)):
            qtw.QMessageBox.information(self, self._parent.title, 'Please'
                                        ' enter search criteria or press cancel')
            self.txt_element.setFocus()
            return

        # self._parent.search_args = (ele, attr_name, attr_val, text)
        # self._parent.search_specs = self.search_specs
        self._parent.dralog_data = ((ele, attr_name, attr_val, text), self.search_specs)
        super().accept()


class DtdDialog(qtw.QDialog):
    """dialoog om het toe te voegen dtd te selecteren
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle("Add DTD")
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        vsbox = qtw.QVBoxLayout()

        hsbox = qtw.QHBoxLayout()
        lbl = qtw.QLabel("Select document type:", self)
        hsbox.addWidget(lbl)
        vsbox.addLayout(hsbox, 0)

        hsbox = qtw.QHBoxLayout()
        vhsbox = qtw.QVBoxLayout()
        first = True
        button_groups = []
        self.dtd_list = []
        for idx, x in enumerate(self._parent.editor.dtdlist):
            if not x[0]:
                vhsbox.addSpacing(8)
                continue
            if first:
                grp = qtw.QButtonGroup()
                button_groups.append(grp)
                first = False
            radio = qtw.QRadioButton(x[0], self)
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

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def accept(self):
        "pass changed data to parent"
        for caption, dtd, radio in self.dtd_list:
            if radio and radio.isChecked():
                self._parent.dialog_data = dtd
                break
        super().accept()


class CssDialog(qtw.QDialog):
    """dialoog om een stylesheet toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        self.styledata = ''
        super().__init__(parent)
        self.setWindowTitle('Add Stylesheet')
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        gbox = qtw.QGridLayout()

        gbox.addWidget(qtw.QLabel("link to stylesheet:", self), 0, 0)
        self.link_text = qtw.QLineEdit("http://", self)
        gbox.addWidget(self.link_text, 0, 1)

        self.choose_button = qtw.QPushButton('&Browse', self)
        self.choose_button.clicked.connect(self.kies)
        box = qtw.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, 1, 0, 1, 2)

        gbox.addWidget(qtw.QLabel("for media type(s):", self), 2, 0)
        self.text_text = qtw.QLineEdit(self)
        gbox.addWidget(self.text_text, 2, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.inline_button = qtw.QPushButton('&Add inline', self)
        self.inline_button.clicked.connect(self.on_inline)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
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
        loc = self._parent.editor.xmlfn or os.getcwd()
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc,
                                                   self._parent.build_mask('css'))
        if fnaam:
            self.link_text.setText(fnaam)

    def on_inline(self):
        "voegt een 'style' tag in"
        self._parent.dialog_data = self._parent.editor.cssm.call_from_inline(self._parent,
                                                                             self.text_text.text())

    def accept(self):
        """bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad
        maar eerst kijken of dit geen inline stylesheet betreft """
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


class LinkDialog(qtw.QDialog):
    """dialoog om een link element toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle('Add Link')
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        gbox = qtw.QGridLayout()
        row = 0
        gbox.addWidget(qtw.QLabel("link to document:", self), row, 0)
        self.link_text = qtw.QLineEdit("http://", self)
        self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, row, 1)

        row += 1
        self.choose_button = qtw.QPushButton('&Browse', self)
        self.choose_button.clicked.connect(self.kies)
        box = qtw.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, row, 0, 1, 2)

        row += 1
        gbox.addWidget(qtw.QLabel("descriptive title:", self), row, 0)
        self.title_text = qtw.QLineEdit(self)
        self.title_text.setMinimumWidth(250)
        gbox.addWidget(self.title_text, row, 1)

        row += 1
        gbox.addWidget(qtw.QLabel("link text:", self), row, 0)
        self.text_text = qtw.QLineEdit(self)
        self.text_text.textChanged.connect(self.set_ttext)
        gbox.addWidget(self.text_text, row, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.link_text.setFocus()

    def kies(self):
        "methode om het te linken document te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc,
                                                   self._parent.build_mask('html'))
        if fnaam:
            self.link_text.setText(fnaam)

    def set_ltext(self, chgtext):
        'indien leeg title tekst gelijk maken aan link adres'
        linktxt = str(chgtext)
        if self.title_text.text() == self.linktxt:
            self.title_text.setText(linktxt)
            self.linktxt = linktxt

    def set_ttext(self, chgtext):
        "indien leeg link tekst leegmaken"
        if str(chgtext) == "":
            self.linktxt = ""

    def accept(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        txt = str(self.text_text.text())
        if not txt:
            hlp = qtw.QMessageBox.question(self, 'Add Link',
                                           "Link text is empty - are you sure?",
                                           qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                                           defaultButton=qtw.QMessageBox.Yes)
            if hlp == qtw.QMessageBox.No:
                return
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            qtw.QMessageBox.information(self, self._parent.title, msg)
            return
        self._parent.dialog_data = [txt, {"href": link,
                                          "title": str(self.title_text.text())}]
        super().accept()


class ImageDialog(qtw.QDialog):
    """dialoog om een image toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle('Add Image')
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        gbox = qtw.QGridLayout()
        row = 0
        gbox.addWidget(qtw.QLabel("link to image:", self), row, 0)
        self.link_text = qtw.QLineEdit("http://", self)
        self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, row, 1)

        row += 1
        self.choose_button = qtw.QPushButton('&Browse', self)
        self.choose_button.clicked.connect(self.kies)
        box = qtw.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, row, 0, 1, 2)

        row += 1
        gbox.addWidget(qtw.QLabel("descriptive title:", self), row, 0)
        self.title_text = qtw.QLineEdit(self)
        self.title_text.setMinimumWidth(250)
        gbox.addWidget(self.title_text, row, 1)

        row += 1
        gbox.addWidget(qtw.QLabel("alternate text:", self), row, 0)
        self.alt_text = qtw.QLineEdit(self)
        self.alt_text.textChanged.connect(self.set_ttext)
        gbox.addWidget(self.alt_text, row, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.link_text.setFocus()

    def kies(self):
        "methode om het te linken image te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc,
                                                   self._parent.build_mask('image'))
        if fnaam:
            self.link_text.setText(fnaam)

    def set_ltext(self, chgtext):
        'indien leeg link tekst gelijk maken aan link adres'
        linktxt = str(chgtext)
        if str(self.alt_text.text()) == self.linktxt:
            self.alt_text.setText(linktxt)
            self.linktxt = linktxt

    def set_ttext(self, chgtext):
        "indien leeg link tekst leegmaken"
        if str(chgtext) == "":
            self.linktxt = ""

    def accept(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            qtw.QMessageBox.information(self, self._parent.title, msg)
            return
        self._parent.dialog_data = {"src": link,
                                    "alt": str(self.alt_text.text()),
                                    "title": str(self.title_text.text())}
        super().accept()


class VideoDialog(qtw.QDialog):
    """dialoog om een video element toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        initialwidth, initialheight = 400, 200
        maxwidth, maxheight = 2400, 1200
        super().__init__(parent)
        self.setWindowTitle('Add Video')
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        gbox = qtw.QGridLayout()

        row = 0
        gbox.addWidget(qtw.QLabel("link to video:", self), row, 0)
        self.link_text = qtw.QLineEdit("http://", self)
        self.linktxt = ""
        gbox.addWidget(self.link_text, row, 1)

        row += 1
        self.choose_button = qtw.QPushButton('&Browse', self)
        self.choose_button.clicked.connect(self.kies)
        box = qtw.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, row, 0, 1, 2)

        row += 1
        gbox.addWidget(qtw.QLabel("height of video window:", self), row, 0)
        self.hig_text = qtw.QSpinBox(self)  # .pnl, -1, size = (40, -1))
        self.hig_text.setMaximum(maxheight)
        self.hig_text.setValue(initialheight)
        self.hig_text.valueChanged.connect(self.on_text)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.hig_text)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        row += 1
        gbox.addWidget(qtw.QLabel("width  of video window:", self), row, 0)
        self.wid_text = qtw.QSpinBox(self)  # .pnl, -1, size = (40, -1))
        self.wid_text.setMaximum(maxwidth)
        self.wid_text.setValue(initialwidth)
        self.wid_text.valueChanged.connect(self.on_text)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.wid_text)
        hbox.addStretch()
        gbox.addLayout(hbox, row, 1)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.link_text.setFocus()

    def kies(self):
        "methode om het te linken element te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc,
                                                   self._parent.build_mask('video'))
        if fnaam:
            self.link_text.setText(fnaam)

    def on_text(self, number=None):
        "controle bij invullen/aanpassen hoogte/breedte"
        try:
            int(number)  # self.rows_text.value())
        except ValueError:
            qtw.QMessageBox.information(self, self._parent.title,
                                        'Number must be numeric integer')
            return

    def accept(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.ed.convert_link(self.link_text.text(),
                                                       self._parent.editor.xmlfn)
        except ValueError as msg:
            qtw.QMessageBox.information(self, self._parent.title, msg)
            return
        self._parent.dialog_data = {"src": link,
                                    "height": str(self.hig_text.text()),
                                    "width": str(self.wid_text.text())}
        super().accept()


class AudioDialog(qtw.QDialog):
    'dialoog om een audio element toe te voegen'

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle('Add Audio')
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        gbox = qtw.QGridLayout()

        row = 0
        gbox.addWidget(qtw.QLabel("link to audio fragment:", self), row, 0)
        self.link_text = qtw.QLineEdit("http://", self)
        self.linktxt = ""
        gbox.addWidget(self.link_text, row, 1)

        row += 1
        self.choose_button = qtw.QPushButton('&Browse', self)
        self.choose_button.clicked.connect(self.kies)
        box = qtw.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, row, 0, 1, 2)

        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.link_text.setFocus()

    def kies(self):
        "methode om het te linken element te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc,
                                                   self._parent.build_mask('audio'))
        if fnaam:
            self.link_text.setText(fnaam)

    def accept(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            qtw.QMessageBox.information(self, self._parent.title, msg)
            return
        self._parent.dialog_data = {"src": link}
        super().accept()


class ListDialog(qtw.QDialog):
    """dialoog om een list toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        self.items = []
        self.dataitems = []
        initialrows = 1
        super().__init__(parent)
        self.setWindowTitle('Add a list')
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        vsbox = qtw.QVBoxLayout()
        tbox = qtw.QGridLayout()
        tbox.addWidget(qtw.QLabel("choose type of list:", self), 0, 0)
        self.type_select = qtw.QComboBox(self)
        self.type_select.addItems(["unordered", "ordered", "definition"])
        self.type_select.activated.connect(self.on_type)
        tbox.addWidget(self.type_select, 0, 1)

        tbox.addWidget(qtw.QLabel("initial number of items:", self), 1, 0)
        self.rows_text = qtw.QSpinBox(self)  # .pnl, -1, size = (40, -1))
        self.rows_text.setValue(initialrows)
        self.rows_text.valueChanged.connect(self.on_rows)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.rows_text)
        hbox.addStretch()
        tbox.addLayout(hbox, 1, 1)
        vsbox.addLayout(tbox)

        self.list_table = qtw.QTableWidget(self)
        self.list_table.setRowCount(initialrows)
        self.list_table.setColumnCount(1)
        self.list_table.setHorizontalHeaderLabels(['list item'])
        hdr = self.list_table.horizontalHeader()
        hdr.resizeSection(0, 252)
        self.list_table.verticalHeader().setVisible(False)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.list_table)
        hbox.addStretch()
        vsbox.addLayout(hbox)
        sbox.setLayout(vsbox)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.type_select.setFocus()

    def on_type(self):  # , selectedindex=None):
        "geselecteerde list type toepassen"
        sel = self.type_select.currentText()
        numcols = self.list_table.columnCount()
        hdr = self.list_table.horizontalHeader()
        if sel[0] == "d" and numcols == 1:
            self.list_table.insertColumn(0)
            self.list_table.setHorizontalHeaderLabels(['term', 'description'])
            hdr.resizeSection(0, 102)
            hdr.resizeSection(1, 152)
        elif sel[0] != "d" and numcols == 2:
            self.list_table.removeColumn(0)
            self.list_table.setHorizontalHeaderLabels(['list item'])
            hdr.resizeSection(0, 254)

    def on_rows(self):  # , number=None):
        "controle en actie bij invullen/aanpassen aantal regels"
        try:
            cur_rows = int(self.rows_text.value())
        except ValueError:
            qtw.QMessageBox.information(self, self._parent.title,
                                        'Number must be numeric integer')
            return
        num_rows = self.list_table.rowCount()
        if num_rows > cur_rows:
            for idx in range(num_rows - 1, cur_rows - 1, -1):
                self.list_table.removeRow(idx)
        elif cur_rows > num_rows:
            for idx in range(num_rows, cur_rows):
                self.list_table.insertRow(idx)

    def accept(self):
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
        super().accept()


class TableDialog(qtw.QDialog):
    "dialoog om een tabel toe te voegen"

    def __init__(self, parent):
        self._parent = parent
        self.headings = ['']
        initialcols, initialrows = 1, 1
        super().__init__(parent)
        self.setWindowTitle('Add a table')
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        gbox = qtw.QGridLayout()

        gbox.addWidget(qtw.QLabel("summary (description):", self), 0, 0)
        self.title_text = qtw.QLineEdit(self)
        self.title_text.setMinimumWidth(250)
        gbox.addWidget(self.title_text, 0, 1)

        gbox.addWidget(qtw.QLabel("initial number of rows:", self), 1, 0)
        hbox = qtw.QHBoxLayout()
        self.rows_text = qtw.QSpinBox(self)  # .pnl, -1, size = (40, -1))
        self.rows_text.setValue(initialrows)
        self.rows_text.valueChanged.connect(self.on_rows)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.rows_text)
        hbox.addStretch()
        gbox.addLayout(hbox, 1, 1)

        gbox.addWidget(qtw.QLabel("initial number of columns:", self), 2, 0)
        hbox = qtw.QHBoxLayout()
        self.cols_text = qtw.QSpinBox(self)  # .pnl, -1, size = (40, -1))
        self.cols_text.setValue(initialcols)
        self.cols_text.valueChanged.connect(self.on_cols)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.cols_text)
        hbox.addStretch()
        gbox.addLayout(hbox, 2, 1)

        self.show_titles = qtw.QCheckBox('Show Titles')
        self.show_titles.setChecked(True)
        self.show_titles.stateChanged.connect(self.on_check)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.show_titles)
        gbox.addLayout(hbox, 3, 1)

        self.table_table = qtw.QTableWidget(self)
        self.table_table.setRowCount(initialrows)     # de eerste rij is voor de kolomtitels
        self.table_table.setColumnCount(initialcols)  # de eerste rij is voor de rijtitels
        self.table_table.setHorizontalHeaderLabels(self.headings)
        self.hdr = self.table_table.horizontalHeader()
        self.table_table.verticalHeader().setVisible(False)
        self.hdr.setSectionsClickable(True)
        self.hdr.sectionClicked.connect(self.on_title)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.table_table)
        gbox.addLayout(hbox, 4, 0, 1, 2)
        sbox.setLayout(gbox)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        self.ok_button = qtw.QPushButton('&Save', self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.cancel_button = qtw.QPushButton('&Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        hbox.addStretch()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.title_text.setFocus()

    def on_rows(self):  # , number=None):
        "controle en actie bij opgeven aantal regels"
        try:
            cur_rows = int(self.rows_text.value())
        except ValueError:
            qtw.QMessageBox.information(self, self._parent.title,
                                        'Number must be numeric integer')
            return
        num_rows = self.table_table.rowCount()
        if num_rows > cur_rows:
            for idx in range(num_rows - 1, cur_rows - 1, -1):
                self.table_table.removeRow(idx)
        elif cur_rows > num_rows:
            for idx in range(num_rows, cur_rows):
                self.table_table.insertRow(idx)

    def on_cols(self):  # , number=None):
        "controle en actie bij opgeven aantal kolommen"
        try:
            cur_cols = int(self.cols_text.value())
        except ValueError:
            qtw.QMessageBox.information(self, self._parent.title,
                                        'Number must be numeric integer')
            return
        num_cols = self.table_table.columnCount()
        if num_cols > cur_cols:
            for idx in range(num_cols - 1, cur_cols - 1, -1):
                self.table_table.removeColumn(idx)
                self.headings.pop()
        elif cur_cols > num_cols:
            for idx in range(num_cols, cur_cols):
                self.table_table.insertColumn(idx)
                self.headings.append('')
                self.table_table.setHorizontalHeaderLabels(self.headings)

    def on_check(self, number=None):
        "callback for show titles checkbox"
        self.hdr.setVisible(bool(number))

    def on_title(self, col):
        "opgeven titel bij klikken op kolomheader mogelijk maken"
        txt, ok = qtw.QInputDialog.getText(self, 'Add a table',
                                           'Enter a title for this column:',
                                           qtw.QLineEdit.Normal, "")
        if txt and ok:
            self.headings[col] = txt
            self.table_table.setHorizontalHeaderLabels(self.headings)

    def accept(self):
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


class ScrolledTextDialog(qtw.QDialog):
    """dialoog voor het tonen van validatieoutput

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title='', data='', htmlfile='', fromdisk=False,
                 size=(600, 400)):
        # self._parent = parent
        self.htmlfile = htmlfile
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.resize(size[0], size[1])
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        self.message = qtw.QLabel(self)
        if fromdisk:
            self.message.setText(VAL_MESSAGE)
        hbox.addWidget(self.message)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        text = qtw.QTextEdit(self)
        text.setReadOnly(True)
        hbox.addWidget(text)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        ok_button = qtw.QPushButton('&Done', self)
        ok_button.clicked.connect(self.close)
        ok_button.setDefault(True)
        if htmlfile:
            show_button = qtw.QPushButton('&View submitted source', self)
            show_button.clicked.connect(self.show_source)
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


class CodeViewDialog(qtw.QDialog):
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
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(caption, self))
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        self.text = sci.QsciScintilla(self)
        self.setup_text()
        self.text.setText(data)
        self.text.setReadOnly(True)
        hbox.addWidget(self.text)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        ok_button = qtw.QPushButton('&Done', self)
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
