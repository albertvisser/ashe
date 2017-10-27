# -*- coding: utf-8 -*-
"""PyQt5 versie van mijn op een treeview gebaseerde HTML-editor
custom dialogen
"""
import os
## import sys
import string
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import PyQt5.Qsci as sci  # scintilla
import ashe.ashe_mixin as ed

try:
    import cssedit.editor.csseditor_qt as csed
    cssedit_available = True
except ImportError:
    cssedit_available = False

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


class ElementDialog(qtw.QDialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, parent, title='', tag=None, attrs=None):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        lbl = qtw.QLabel("element name:", self)
        self.tag_text = qtw.QLineEdit(self)
        self.tag_text.setMinimumWidth(250)
        self.comment_button = qtw.QCheckBox('&Comment(ed)', self)
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

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)

        box = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        self.attr_table = qtw.QTableWidget(self)
        ## self.attr_table.resize(540, 340)
        self.attr_table.setColumnCount(2)
        self.attr_table.setHorizontalHeaderLabels(['attribute', 'value'])
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
        ## hbox.addStretch()
        hbox.addWidget(self.attr_table)
        ## hbox.addStretch()
        box.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.add_button = qtw.QPushButton('&Add Attribute', self)
        self.add_button.clicked.connect(self.on_add)
        self.delete_button = qtw.QPushButton('&Delete Selected', self)
        self.delete_button.clicked.connect(self.on_del)
        if is_style_tag:
            text = '&Edit styles'
        elif self.is_stylesheet:
            text = '&Edit linked stylesheet'
        elif has_style:
            text = '&Edit inline style'
        else:
            text = '&Add inline style'
        self.style_button = qtw.QPushButton(text, self)
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

    ## def on_resize(self, evt=None):
        ## self.attr_table.SetColSize(1, self.attr_table.GetSize()[0] - 162) # 178) # 160)
        ## self.attr_table.ForceRefresh()

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
                ## h_fname = str(pathlib.Path('/tmp') / 'ashe_{}'.format(
                    ## pathlib.Path(fname).name))
                os.system('wget {} -O {}'.format(fname, h_fname))    # TODO
                fname = h_fname
            else:
                h_fname = fname
                ## xmlfn_path = os.path.dirname(self._parent.xmlfn)
                xmlfn_path = pathlib.Path(self._parent.xmlfn)
                while h_fname.startswith('../'):
                    h_fname = h_fname[3:]
                    ## xmlfn_path = os.path.dirname(xmlfn_path)
                    xmlfn_path = xmlfn_path.parent
                ## fname = os.path.join(xmlfn_path, h_fname)
                fname = str(xmlfn_path / h_fname)
            print('constructed filename:', fname)
            try:
                css = csed.MainWindow(app=self._parent.app)
                css.open(filename=fname)
            except Exception as e:
                mld = str(e)
                ## css.close()
            else:
                css.setWindowModality(core.Qt.ApplicationModal)
                css.show()
        if mld:
            qtw.QMessageBox.information(self, self._parent.title, mld)

    def accept(self):
        "controle bij OK aanklikken"
        # TODO: ensure no duplicate items are added
        tag = str(self.tag_text.text())
        ## okay = True
        test = string.ascii_letters + string.digits
        for letter in tag:
            if letter not in test:
                ## okay = False
                qtw.QMessageBox.information(self, self._parent.title,
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
        for idx, x in enumerate(ed.dtdlist):
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

        ## hbox = qtw.QDialog.ButtonBoxlayout()
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

        self.choose_button = qtw.QPushButton('Search', self)
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
        ## if self._parent.xmlfn:
            ## loc = os.path.dirname(self._parent.xmlfn)
        ## else:
            ## loc = os.getcwd()
        loc = self._parent.xmlfn or os.getcwd()
        ## if os.name == "nt":
            ## mask = "CSS files (*.css)"
        ## elif os.name == "posix":
            ## mask = "CSS files (*.css *.CSS)"
        mask = HMASK.replace('html', 'css').replace('HTML', 'CSS')
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
        if fnaam:
            self.link_text.setText(fnaam)

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
        ## if not link.startswith('http://'):
            ## link = os.path.abspath(link)
            ## if self._parent.xmlfn:
                ## whereami = os.path.abspath(self._parent.xmlfn)
            ## else:
                ## whereami = os.path.join(os.getcwd(), 'index.html')
            ## link = ed.getrelativepath(link, whereami)
        ## if not link:
            ## qtw.QMessageBox.information(self, self.parent().title,
                                        ## 'Unable to make this local link relative')
        ## else:
            ## self.link = link
        try:
            link = ed.convert_link(link)
        except ed.ConversionError:
            qtw.QMessageBox.information(self, self._parent.title,msg)
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
        self._parent.dialog_data = {"type": 'text/css'}
        test = str(self.text_text.text())
        if test:
            self._parent.dialog_data["media"] = test
        css = csed.MainWindow(self)
        css.open(text="")
        css.setWindowModality(core.Qt.ApplicationModal)
        css.show()


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
        gbox.addWidget(qtw.QLabel("descriptive title:", self), 0, 0)
        self.title_text = qtw.QLineEdit(self)
        self.title_text.setMinimumWidth(250)
        gbox.addWidget(self.title_text, 0, 1)

        gbox.addWidget(qtw.QLabel("link to document:", self), 1, 0)
        self.link_text = qtw.QLineEdit("http://", self)
        self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, 1, 1)

        self.choose_button = qtw.QPushButton('Search', self)
        self.choose_button.clicked.connect(self.kies)
        box = qtw.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, 2, 0, 1, 2)

        gbox.addWidget(qtw.QLabel("link text:", self), 3, 0)
        self.text_text = qtw.QLineEdit(self)
        self.text_text.textChanged.connect(self.set_ttext)
        gbox.addWidget(self.text_text, 3, 1)

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

    def kies(self):
        "methode om het te linken document te selecteren"
        ## if self._parent.xmlfn:
            ## loc = os.path.dirname(self._parent.xmlfn)
        ## else:
            ## loc = os.getcwd()
        loc = self._parent.xmlfn or os.getcwd()
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc, HMASK)
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
        ## link = str(self.link_text.text())
        ## if link:
            ## if not link.startswith('http://'):
                ## link = os.path.abspath(link)
                ## if self._parent.xmlfn:
                    ## whereami = os.path.abspath(self._parent.xmlfn)
                ## else:
                    ## whereami = os.path.join(os.getcwd(), 'index.html')
                ## link = ed.getrelativepath(link, whereami)
            ## if not link:
                ## qtw.QMessageBox.information(self, self._parent.title,
                                            ## 'Unable to make this local link relative')
            ## else:
                ## self.link = link
            ## txt = str(self.text_text.text())
            ## data = {"href": link,
                    ## "title": str(self.title_text.text())}
            ## self._parent.dialog_data = txt, data
        ## else:
            ## qtw.QMessageBox.information(self, self._parent.title,
                                        ## "link opgeven of cancel kiezen s.v.p")
            ## return
        txt = str(self.text_text.text())
        if not txt:
            hlp = qtw.QMessageBox.question(self, 'Add Link',
                                           "Link text is empty - are you sure?",
                                           qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                                           defaultButton=qtw.QMessageBox.Yes)
            if hlp == qtw.QMessageBox.No:
                return
        try:
            link = ed.convert_link(self.link_text.text(), self._parent.xmlfn)
        except ed.ConversionError as msg:
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
        gbox.addWidget(qtw.QLabel("descriptive title:", self), 0, 0)
        self.title_text = qtw.QLineEdit(self)
        self.title_text.setMinimumWidth(250)
        gbox.addWidget(self.title_text, 0, 1)

        gbox.addWidget(qtw.QLabel("link to image:", self), 1, 0)
        self.link_text = qtw.QLineEdit("http://", self)
        self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, 1, 1)

        self.choose_button = qtw.QPushButton('Search', self)
        self.choose_button.clicked.connect(self.kies)
        box = qtw.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addStretch()
        gbox.addLayout(box, 2, 0, 1, 2)

        gbox.addWidget(qtw.QLabel("alternate text:", self), 3, 0)
        self.alt_text = qtw.QLineEdit(self)
        self.alt_text.textChanged.connect(self.set_ttext)
        gbox.addWidget(self.alt_text, 3, 1)

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

    def kies(self):
        "methode om het te linken image te selecteren"
        ## if self._parent.xmlfn:
            ## loc = os.path.dirname(self._parent.xmlfn)
        ## else:
            ## loc = os.getcwd()
        loc = self._parent.xmlfn or os.getcwd()
        mask = '*.png *.jpg *.gif *.jpeg *.ico *.xpm *.svg'
        ## if os.name == "nt":
            ## mask = "Image files (*.htm *.html);;" + IMASK
        ## elif os.name == "posix":
        if os.name == "posix":
            mask += ' ' + mask.upper()
        mask = "Image files ({});;{}".format(mask, IMASK)
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
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
        ## link = str(self.link_text.text())
        ## if link:
            ## if not link.startswith('http://'):
                ## link = os.path.abspath(link)
                ## if self._parent.xmlfn:
                    ## whereami = os.path.abspath(self._parent.xmlfn)
                ## else:
                    ## whereami = os.path.join(os.getcwd(), 'index.html')
                ## link = ed.getrelativepath(link, whereami)
            ## if not link:
                ## qtw.QMessageBox.information(self, self._parent.title,
                                            ## 'Unable to make this local link relative')
            ## else:
                ## self.link = link
            ## self._parent.dialog_data = {"src": link,
                                        ## "alt": str(self.alt_text.text()),
                                        ## "title": str(self.title_text.text())}
        ## else:
            ## qtw.QMessageBox.information(self, self._parent.title,
                                        ## "image link opgeven of cancel kiezen s.v.p")
            ## return
        try:
            link = ed.convert_link(self.link_text.text(), self._parent.xmlfn)
        except ed.ConversionError:
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
        ## self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, row, 1)

        row += 1
        self.choose_button = qtw.QPushButton('Search', self)
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
        ## if self._parent.xmlfn:
            ## loc = os.path.dirname(self._parent.xmlfn)
        ## else:
            ## loc = os.getcwd()
        loc = self._parent.xmlfn or os.getcwd()
        mask = '*.mp4 *.avi *.mpeg'  # TODO: add other types
        ## if os.name == "nt":
            ## mask = "Image files (*.htm *.html);;" + IMASK
        ## elif os.name == "posix":
        if os.name == "posix":
            mask += ' ' + mask.upper()
        mask = "Video files ({});;{}".format(mask, IMASK)
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
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
        ## link = str(self.link_text.text())
        ## if link:
            ## if not link.startswith('http://'):
                ## link = os.path.abspath(link)
                ## if self._parent.xmlfn:
                    ## whereami = os.path.abspath(self._parent.xmlfn)
                ## else:
                    ## whereami = os.path.join(os.getcwd(), 'index.html')
                ## link = ed.getrelativepath(link, whereami)
            ## if not link:
                ## qtw.QMessageBox.information(self, self._parent.title,
                                            ## 'Unable to make this local link relative')
            ## else:
                ## self.link = link
            ## self._parent.dialog_data = {"src": link,
                                        ## "height": str(self.hig_text.text()),
                                        ## "width": str(self.wid_text.text())}
        ## else:
            ## qtw.QMessageBox.information(self, self._parent.title,
                                        ## "link naar video opgeven of cancel kiezen s.v.p")
            ## return
        try:
            link = ed.convert_link(self.link_text.text(), self._parent.xmlfn)
        except ed.ConversionError:
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
        ## self.link_text.textChanged.connect(self.set_ltext)
        self.linktxt = ""
        gbox.addWidget(self.link_text, row, 1)

        row += 1
        self.choose_button = qtw.QPushButton('Search', self)
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
        ## if self._parent.xmlfn:
            ## loc = os.path.dirname(self._parent.xmlfn)
        ## else:
            ## loc = os.getcwd()
        loc = self._parent.xmlfn or os.getcwd()
        mask = '*.mp3 *.wav *.ogg'  # TODO: add other types
        ## if os.name == "nt":
            ## mask = "Image files (*.htm *.html);;" + IMASK
        ## elif os.name == "posix":
        if os.name == "posix":
            mask += ' ' + mask.upper()
        mask = "Audio files ({});;{}".format(mask, IMASK)
        fnaam, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", loc, mask)
        if fnaam:
            self.link_text.setText(fnaam)

    def accept(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        ## link = str(self.link_text.text())
        ## if link:
            ## if not link.startswith('http://'):
                ## link = os.path.abspath(link)
                ## if self._parent.xmlfn:
                    ## whereami = os.path.abspath(self._parent.xmlfn)
                ## else:
                    ## whereami = os.path.join(os.getcwd(), 'index.html')
                ## link = ed.getrelativepath(link, whereami)
            ## if not link:
                ## qtw.QMessageBox.information(self, self._parent.title,
                                            ## 'Unable to make this local link relative')
            ## else:
                ## self.link = link
            ## self._parent.dialog_data = {"src": link}
        ## else:
            ## qtw.QMessageBox.information(self, self._parent.title,
                                        ## "link naar audio opgeven of cancel kiezen s.v.p")
            ## return
        try:
            link = ed.convert_link(self.link_text.text(), self._parent.xmlfn)
        except ed.ConversionError:
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
        ## self.type_select.setCurrentIndex(0) # SetStringSelection("unordered")
        self.type_select.activated.connect(self.on_type)
        tbox.addWidget(self.type_select, 0, 1)

        tbox.addWidget(qtw.QLabel("initial number of items:", self), 1, 0)
        self.rows_text = qtw.QSpinBox(self)  # .pnl, -1, size = (40, -1))
        self.rows_text.valueChanged.connect(self.on_text)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.rows_text)
        hbox.addStretch()
        tbox.addLayout(hbox, 1, 1)
        vsbox.addLayout(tbox)

        tbl = qtw.QTableWidget(self)
        tbl.setColumnCount(1)
        tbl.setHorizontalHeaderLabels(['list item'])
        hdr = tbl.horizontalHeader()
        hdr.resizeSection(0, 252)
        tbl.verticalHeader().setVisible(False)
        ## tbl.SetColSize(0, 240)
        self.list_table = tbl
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

    def on_text(self):  # , number=None):
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
                ## self.list_table.SetRowLabelValue(idx, '')

    def accept(self):
        """bij OK: de opgebouwde list via self.dialog_data doorgeven
        aan het mainwindow
        """
        list_type = str(self.type_select.currentText()[0]) + "l"
        list_data = []
        for row in range(self.list_table.rowCount()):
            list_item = [str(self.list_table.item(row, 0).text())]
            if list_type == "dl":
                list_item.append(str(self.list_table.item(row, 1).text()))
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
        ## hbox.addStretch()
        hbox.addWidget(self.show_titles)
        ## hbox.addStretch()
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
        ## hbox.addStretch()
        hbox.addWidget(self.table_table)
        ## hbox.addStretch()
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
                ## self.table_table.itemAt(idx, 0).setBackgroundColor(core.Qt.darkGray)
                ## self.table_table.SetRowLabelValue(idx, '')

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
                ## self.table_table.SetColLabelValue(idx,'')

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
                rowitems.append(str(self.table_table.item(row, col).text()))
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
        self._parent = parent
        self.htmlfile = htmlfile
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self._parent.appicon)
        self.resize(size[0], size[1])
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        self.message = qtw.QLabel(self)
        if fromdisk:
            self.message.setText("\n".join((
                "Validation results are for the file on disk",
                "some errors/warnings may already have been corrected by "
                "BeautifulSoup",
                "(you'll know when they don't show up inthe tree or text view",
                " or when you save the file in memory back to disk)")))
        hbox.addWidget(self.message)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        text = qtw.QTextEdit(self)
        text.setReadOnly(True)
        hbox.addWidget(text)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        ok_button = qtw.QPushButton('&Ok', self)
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
            data = ed.EditorMixin.validate(self, htmlfile)
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
        self.setWindowIcon(self._parent._parent.appicon)
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
        ok_button = qtw.QPushButton('&Ok', self)
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
