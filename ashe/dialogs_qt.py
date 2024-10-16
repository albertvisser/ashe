"""PyQt5 versie van mijn op een treeview gebaseerde HTML-editor

custom dialogen
"""
import os
## import sys
import string
# import pathlib
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
import PyQt6.Qsci as sci  # scintilla
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
        tag_text, iscomment, self.style_text = tagdata[:3]
        self.styledata, self.has_style, self.is_stylesheet = tagdata[3:]
        self.csseditor_called = False
        self.old_styledata = self.styledata
        self.is_style_tag = tag_text == 'style'
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        lbl = qtw.QLabel("element name:", self)
        self.tag_text = qtw.QLineEdit(self)
        self.tag_text.setMinimumWidth(250)
        self.comment_button = qtw.QCheckBox('&Comment(ed)', self)
        self.tag_text.setText(tag_text)
        if iscomment:
            self.comment_button.toggle()
        hbox.addWidget(lbl)
        hbox.addWidget(self.tag_text)
        hbox.addWidget(self.comment_button)
        vbox.addLayout(hbox)

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)

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
                row = self.attr_table.rowCount()
                self.attr_table.insertRow(row)
                item = qtw.QTableWidgetItem(attr)
                self.attr_table.setItem(row, 0, item)
                if attr in ('style', 'styledata'):
                    item.setFlags(item.flags() & ~core.Qt.ItemFlag.ItemIsEditable)
                item = qtw.QTableWidgetItem(value)
                self.attr_table.setItem(row, 1, item)
                if attr in ('style', 'styledata'):
                    item.setFlags(item.flags() & ~core.Qt.ItemFlag.ItemIsEditable)
        hbox.addWidget(self.attr_table)
        box.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.add_button = qtw.QPushButton('&Add Attribute', self)
        self.add_button.clicked.connect(self.on_add)
        self.delete_button = qtw.QPushButton('&Delete Selected', self)
        self.delete_button.clicked.connect(self.on_del)
        self.check_changes = False
        self.style_button = qtw.QPushButton(self.style_text, self)
        self.style_button.clicked.connect(self.on_style)
        # self.refresh_button = qtw.QPushButton('&Refresh', self)
        # self.refresh_button.clicked.connect(self.refresh)
        # self.refresh_button.setDisabled(True)
        hbox.addStretch()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.style_button)
        # hbox.addWidget(self.refresh_button)
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
        self.refresh()
        self.attr_table.setFocus()
        row = self.attr_table.rowCount()
        self.attr_table.insertRow(row)
        self.attr_table.setCurrentCell(row, 0)

    def on_del(self):
        "attribuut verwijderen"
        self.refresh()
        row = self.attr_table.currentRow()
        if row or row == 0:
            if self.attr_table.item(row, 0).text() == 'style':
                self.has_style = False
            self.attr_table.removeRow(row)
        else:
            qtw.QMessageBox.information(self, 'Delete attribute',
                                        "press Enter on this item first")

    def on_style(self):
        "adjust style attributes"
        if self.check_changes:
            self.refresh()
            self.check_changes = False
            self.style_button.setText(self.style_text)
            return
        self.check_changes = True
        self.style_button.setText('Chec&k Changes')
        tag = self.tag_text.text()
        fname = ''
        test = self.attr_table.findItems('href', core.Qt.MatchFlag.MatchFixedString)
        for item in test:
            col = self.attr_table.column(item)
            row = self.attr_table.row(item)
            if col == 0:
                fname = self.attr_table.item(row, 1).text()
        if self.is_stylesheet:
            self._parent.editor.cssm.call_editor_for_stylesheet(fname)
            self.refresh()
            self.check_changes = False
        else:
            self._parent.editor.cssm.call_editor(self, tag)

    def refresh(self):
        "ververs het style / styledata element i.v.m. terugkeer uit css editor"
        if self.tag_text.text() == 'link':
            return
        self.is_style_tag = self.tag_text.text() == 'style'
        attrname = 'styledata' if self.is_style_tag else 'style'
        self.has_style = not self.is_style_tag
        # klopt de voorgaande regel wel? Is wel equivalent met hoe het eerder stond volgens mij
        # maar zet has_style ook aan als we een nieuwe (lege) style definiëren
        # in on_del wordt has_style uitgezet als de style regel wordt verwijderd dus lijkt te kloppen
        for row in range(self.attr_table.rowCount()):
            # if self.attr_table.item(row, 0).text() in ('style', 'styledata'):
            if self.attr_table.item(row, 0).text() == attrname:
                self.attr_table.item(row, 1).setText(str(self.styledata))
                break
        else:
            row = self.attr_table.rowCount()
            self.attr_table.insertRow(row)
            item = qtw.QTableWidgetItem(attrname)
            self.attr_table.setItem(row, 0, item)
            # item.setFlags(item.flags() & (not core.Qt.ItemFlag.ItemIsEditable))
            item.setFlags(item.flags() & ~core.Qt.ItemFlag.ItemIsEditable)
            item = qtw.QTableWidgetItem(self.styledata)
            self.attr_table.setItem(row, 1, item)
            # item.setFlags(item.flags() & (not core.Qt.ItemFlag.ItemIsEditable))
            item.setFlags(item.flags() & ~core.Qt.ItemFlag.ItemIsEditable)
            self.style_button.setText(analyze_element('', {attrname: ''})[2])
        self.old_styledata = self.styledata

    def reject(self):
        "controle bij afbreken: css data kan gewijzigd zijn"
        if self.styledata != self.old_styledata:
            qtw.QMessageBox.information(self, 'Let op', "bijbehorende style data is gewijzigd")
            self.refresh()
        else:
            super().reject()

    def accept(self):
        "controle bij OK aanklikken"
        self.refresh()
        add_title = 'Add an element'
        tag = self.tag_text.text()
        test = string.ascii_letters + string.digits
        for letter in tag:
            if letter not in test:
                qtw.QMessageBox.information(self, add_title, 'Illegal character(s) in tag name')
                return
        commented = self.comment_button.isChecked()  # checkState()
        attrs = {}
        for i in range(self.attr_table.rowCount()):
            try:
                name = self.attr_table.item(i, 0).text()
                value = self.attr_table.item(i, 1).text()
            except AttributeError:
                qtw.QMessageBox.information(self, add_title, 'Press enter on this item first')
                return
            if name in attrs:
                qtw.QMessageBox.information(self, add_title, 'Duplicate attributes, please merge')
                return
            if name not in ('styledata', 'style'):
                attrs[name] = value
        # hoeft dit nog als ik die refresh doe?
        attrname = 'styledata' if self.is_style_tag else 'style' if self.has_style else ''
        if attrname:
            attrs[attrname] = self.styledata
        self._parent.dialog_data = tag, attrs, commented
        super().accept()


class TextDialog(qtw.QDialog):
    """dialoog om een tekst element op te voeren of aan te passen
    biedt tevens de mogelijkheid de tekst "op commentaar" te zetten"""

    def __init__(self, parent, title='', text=None, show_commented=True):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self._parent.appicon)
        self.show_commented = show_commented
        vbox = qtw.QVBoxLayout()
        if show_commented:
            hbox = qtw.QHBoxLayout()
            self.comment_button = qtw.QCheckBox('&Comment(ed)', self)
            if text is None:
                text = ''
            elif text.startswith(CMSTART):
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
        commented = self.comment_button.checkState() if self.show_commented else False
        self._parent.dialog_data = (self.data_text.toPlainText(), commented)
        super().accept()


class SearchDialog(qtw.QDialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title="", replace=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self._parent = parent
        self.replace = replace

        self.txt_element = qtw.QLineEdit(self)
        self.txt_element.textChanged.connect(self.set_search)

        self.txt_attr_name = qtw.QLineEdit(self)
        self.txt_attr_name.textChanged.connect(self.set_search)
        self.txt_attr_val = qtw.QLineEdit(self)
        self.txt_attr_val.textChanged.connect(self.set_search)

        self.txt_text = qtw.QLineEdit(self)
        self.txt_text.textChanged.connect(self.set_search)

        if self.replace:
            self.txt_element_replace = qtw.QLineEdit(self)
            self.txt_element_replace.textChanged.connect(self.set_search)

            self.txt_attr_name_replace = qtw.QLineEdit(self)
            self.txt_attr_name_replace.textChanged.connect(self.set_search)
            self.txt_attr_val_replace = qtw.QLineEdit(self)
            self.txt_attr_val_replace.textChanged.connect(self.set_search)

            self.txt_text_replace = qtw.QLineEdit(self)
            self.txt_text_replace.textChanged.connect(self.set_search)

            self.cb_replace_all = qtw.QCheckBox('Replace All', self)

        self.lbl_search = qtw.QLabel('', self)

        self.btn_ok = qtw.QPushButton('&Ok', self)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_ok.setDefault(True)
        self.btn_cancel = qtw.QPushButton('&Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)

        sizer = qtw.QVBoxLayout()

        gsizer = qtw.QGridLayout()
        gsizer.addWidget(qtw.QLabel('Search for:', self), 0, 0, 1, 3)

        gsizer.addWidget(qtw.QLabel('Element', self), 1, 0)
        gsizer.addWidget(qtw.QLabel("name:", self), 1, 1)
        gsizer.addWidget(self.txt_element, 1, 2)

        gsizer.addWidget(qtw.QLabel('Attribute', self), 2, 0)
        gsizer.addWidget(qtw.QLabel("name:", self), 2, 1)
        gsizer.addWidget(self.txt_attr_name, 2, 2)
        gsizer.addWidget(qtw.QLabel("value:", self), 3, 1)
        gsizer.addWidget(self.txt_attr_val, 3, 2)

        gsizer.addWidget(qtw.QLabel('Text', self), 4, 0)
        gsizer.addWidget(qtw.QLabel("value:", self), 4, 1)
        gsizer.addWidget(self.txt_text, 4, 2)

        if replace:
            gsizer.addWidget(qtw.QLabel("Replace with:"), 0, 3, 1, 3)

            gsizer.addWidget(qtw.QLabel('Element', self), 1, 3)
            gsizer.addWidget(qtw.QLabel("name:", self), 1, 4)
            gsizer.addWidget(self.txt_element_replace, 1, 5)

            gsizer.addWidget(qtw.QLabel('Attribute', self), 2, 3)
            gsizer.addWidget(qtw.QLabel("name:", self), 2, 4)
            gsizer.addWidget(self.txt_attr_name_replace, 2, 5)
            gsizer.addWidget(qtw.QLabel("value:", self), 3, 4)
            gsizer.addWidget(self.txt_attr_val_replace, 3, 5)

            gsizer.addWidget(qtw.QLabel('Text', self), 4, 3)
            gsizer.addWidget(qtw.QLabel("value:", self), 4, 4)
            gsizer.addWidget(self.txt_text_replace, 4, 5)

            gsizer.addWidget(self.cb_replace_all, 5, 3, 1, 3)

        sizer.addLayout(gsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(self.lbl_search)
        sizer.addLayout(hsizer)
        self.lbl_search.setWordWrap(True)

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)

        if self._parent.editor.srchhlp.search_args:
            self.txt_element.setText(self._parent.editor.srchhlp.search_args[0])
            self.txt_attr_name.setText(self._parent.editor.srchhlp.search_args[1])
            self.txt_attr_val.setText(self._parent.editor.srchhlp.search_args[2])
            self.txt_text.setText(self._parent.editor.srchhlp.search_args[3])
        if replace and self._parent.editor.srchhlp.replace_args:
            self.txt_element_replace.setText(self._parent.editor.srchhlp.replace_args[0])
            self.txt_attr_name_replace.setText(self._parent.editor.srchhlp.replace_args[1])
            self.txt_attr_val_replace.setText(self._parent.editor.srchhlp.replace_args[2])
            self.txt_text_replace.setText(self._parent.editor.srchhlp.replace_args[3])

    def set_search(self):
        """build text describing search action"""
        replace = (self.txt_element_replace.text(),
                   self.txt_attr_name_replace.text(),
                   self.txt_attr_val_replace.text(),
                   self.txt_text_replace.text()) if self.replace else ()
        out = self._parent.editor.build_search_spec(self.txt_element.text(),
                                                    self.txt_attr_name.text(),
                                                    self.txt_attr_val.text(),
                                                    self.txt_text.text(), replace)
        self.lbl_search.setText(out)
        self.search_specs = out

    def accept(self):
        """confirm dialog and pass changed data to parent"""
        ele = str(self.txt_element.text())
        attr_name = str(self.txt_attr_name.text())
        attr_val = str(self.txt_attr_val.text())
        text = str(self.txt_text.text())
        if not any((ele, attr_name, attr_val, text)):
            qtw.QMessageBox.information(self, self._parent.editor.title, 'Please'
                                        ' enter search criteria or press cancel')
            self.txt_element.setFocus()
            return
        search_args = (ele, attr_name, attr_val, text)
        replace_args = ()
        if self.replace:
            ele = str(self.txt_element_replace.text())
            attr_name = str(self.txt_attr_name_replace.text())
            attr_val = str(self.txt_attr_val_replace.text())
            text = str(self.txt_text_replace.text())
            if not any((ele, attr_name, attr_val, text)):
                qtw.QMessageBox.information(self, self._parent.editor.title, 'Please'
                                            ' enter replacement criteria or press cancel')
                self.txt_element_replace.setFocus()
                return
            replace_args = (ele, attr_name, attr_val, text)

        # self._parent.search_args = (ele, attr_name, attr_val, text)
        # self._parent.search_specs = self.search_specs
        self._parent.dialog_data = (search_args, self.search_specs, replace_args)
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
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
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
            if self._parent.editor.dtdlist[idx][0] == 'HTML 5':
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
        # print('in CssDialog.__init__')
        self._parent = parent
        self.styledata = ''
        self.cssfilename = ''  # can be set from csseditor
        super().__init__(parent)
        self.setWindowTitle('Add Stylesheet')
        self.setWindowIcon(self._parent.appicon)
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
        gbox = qtw.QGridLayout()

        gbox.addWidget(qtw.QLabel("link to stylesheet:", self), 0, 0)
        self.link_text = qtw.QLineEdit("http://", self)
        gbox.addWidget(self.link_text, 0, 1)

        self.new_button = qtw.QPushButton('C&reate', self)
        self.new_button.clicked.connect(self.nieuw)
        self.choose_button = qtw.QPushButton('&Select', self)
        self.choose_button.clicked.connect(self.kies)
        self.edit_button = qtw.QPushButton('Select + &Edit', self)
        self.edit_button.clicked.connect(self.edit)
        box = qtw.QHBoxLayout()
        box.addStretch()
        box.addWidget(self.choose_button)
        box.addWidget(self.new_button)
        box.addWidget(self.edit_button)
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
        self.check_changes = False
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
        # print('in CssDialog.__init__: end of method')

    def kies(self):
        "methode om het te linken document te selecteren"
        self.select_file()

    def nieuw(self, evt):
        "methode om het te linken document te maken en automatisch te selecteren"
        fname = self.select_file(create=True)
        if not fname:
            return
        self._parent.editor.cssm.call_editor_for_stylesheet(fname, new_ok=True)

    def edit(self, evt):
        "methode om het te linken document van hieruit te wijzigen"
        fname = self.select_file()
        if not fname:
            return
        self._parent.editor.cssm.call_editor_for_stylesheet(fname)

    def select_file(self, create=False):
        "methode om het te linken document te selecteren"
        loc = self.link_text.text()
        if not loc or (loc.startswith('http') and '://' in loc):
            loc = os.path.dirname(self._parent.editor.xmlfn) or os.getcwd()
        text, mask = "Choose a file", self._parent.build_mask('css')
        if create:
            fnaam = qtw.QFileDialog.getSaveFileName(self, text, loc, mask)[0]
        else:
            fnaam = qtw.QFileDialog.getOpenFileName(self, text, loc, mask)[0]
        if fnaam:
            self.link_text.setText(fnaam)
        return fnaam

    def on_inline(self):
        "voegt een 'style' tag in"
        self._parent.editor.cssm.call_from_inline(self, '')
        # dit werkt niet, vandaar het dichtzetten van alles
        # styledata = self._parent.editor.cssm.call_from_inline(self._parent, '')
        # self._parent.dialog_data = {"type": 'text/css', 'cssdata': ''}  # styledata}
        # test = str(self.text_text.text())
        # if test:
        #     self._parent.dialog_data["media"] = test
        # super().accept()
        for widget in (self.link_text, self.new_button, self.edit_button, self.choose_button,
                       self.inline_button):
            widget.setDisabled(True)

    def accept(self):
        """bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad
        maar eerst kijken of dit geen inline stylesheet betreft """
        if self.styledata:
            self._parent.dialog_data = {"cssdata": self.styledata}
            super().accept()
            return
        if self.cssfilename:
            self.link_text.setText(self.cssfilename)  # moet nog relatief gemaakt worden
        link = self.link_text.text()
        if link in ('', 'http://'):
            self._parent.meld("bestandsnaam opgeven of inline stylesheet definiëren s.v.p")
            return
        try:
            link = self._parent.editor.convert_link(link, self._parent.editor.xmlfn)
        except ValueError as msg:
            self._parent.meld(str(msg))
            return
        self._parent.dialog_data = {"rel": 'stylesheet', "href": link, "type": 'text/css'}
        test = self.text_text.text()
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
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
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
        linktxt = chgtext
        if self.title_text.text() == self.linktxt:
            self.title_text.setText(linktxt)
            self.linktxt = linktxt

    def set_ttext(self, chgtext):
        "indien leeg link tekst leegmaken"
        if chgtext == "":
            self.linktxt = ""

    def accept(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        txt = str(self.text_text.text())
        if not txt:
            hlp = qtw.QMessageBox.question(self, 'Add Link',
                                           "Link text is empty - are you sure?",
                                           qtw.QMessageBox.StandardButton.Yes
                                           | qtw.QMessageBox.StandardButton.No,
                                           defaultButton=qtw.QMessageBox.StandardButton.Yes)
            if hlp == qtw.QMessageBox.StandardButton.No:
                return
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            self._parent.meld(str(msg))
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
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
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
        if self.alt_text.text() == self.linktxt:
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
            self._parent.meld(str(msg))
            return
        self._parent.dialog_data = {"src": link,
                                    "alt": self.alt_text.text(),
                                    "title": self.title_text.text()}
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
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
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

    def on_text(self, number):
        "controle bij invullen/aanpassen hoogte/breedte"
        try:
            int(number)  # self.rows_text.value())
        except ValueError:
            qtw.QMessageBox.information(self, self._parent.title,
                                        'Number must be numeric integer')

    def accept(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.convert_link(self.link_text.text(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            self._parent.meld(str(msg))
            return
        self._parent.dialog_data = {"src": link,
                                    "height": str(self.hig_text.value()),
                                    "width": str(self.wid_text.value())}
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
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
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
            self._parent.meld(str(msg))
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
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
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
        if sel[0] == "d" and numcols == len(['one_column']):
            self.list_table.insertColumn(0)
            self.list_table.setHorizontalHeaderLabels(['term', 'description'])
            hdr.resizeSection(0, 102)
            hdr.resizeSection(1, 152)
        elif sel[0] != "d" and numcols == len(['two', 'columns']):
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
        list_type = self.type_select.currentText()[0] + "l"
        list_data = []
        for row in range(self.list_table.rowCount()):
            try:
                list_item = [self.list_table.item(row, 0).text()]
            except AttributeError:
                self._parent.meld('Graag nog even het laatste item bevestigen (...)')
                return
            if list_type == "dl":
                try:
                    list_item.append(self.list_table.item(row, 1).text())
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
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
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
        txt, ok = qtw.QInputDialog.getText(self, 'Add a table', 'Enter a title for this column:',
                                           text="")
        if ok and txt:
            self.headings[col] = txt
            self.table_table.setHorizontalHeaderLabels(self.headings)

    def accept(self):
        """bij OK: de opgebouwde tabel via self.dialog_data doorgeven
        aan het mainwindow
        """
        rows = self.table_table.rowCount()
        cols = self.table_table.columnCount()
        summary = self.title_text.text()
        items = []
        for row in range(rows):
            rowitems = []
            for col in range(cols):
                try:
                    rowitems.append(self.table_table.item(row, col).text())
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
            data = ''.join(list(f_in))
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
        self.text.setMarginWidth(0, fontmetrics.horizontalAdvance("00000"))
        self.text.setMarginLineNumbers(0, True)
        self.text.setMarginsBackgroundColor(gui.QColor("#cccccc"))

        # Enable brace matching, auto-indent, code-folding
        self.text.setBraceMatching(sci.QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.text.setAutoIndent(True)
        self.text.setFolding(sci.QsciScintilla.FoldStyle.PlainFoldStyle)

        # Current line visible with special background color
        self.text.setCaretLineVisible(True)
        self.text.setCaretLineBackgroundColor(gui.QColor("#ffe4e4"))

        # Set HTML lexer
        lexer = sci.QsciLexerHTML()
        lexer.setDefaultFont(font)
        self.text.setLexer(lexer)
