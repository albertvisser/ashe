"""PyQt specifieke routines voor mijn op een treeview gebaseerde HTML-editor
"""
import os
import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
import PyQt6.QtWebEngineWidgets as webeng
import PyQt6.Qsci as qsc  # scintilla

from ashe.shared import masks


class EditorGui(qtw.QMainWindow):
    "Main GUI"

    def __init__(self, editor, title, icon):
        # self.parent = parent
        self.editor = editor
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        # if err:
        #     show_message(self, TITEL, err)
        #     return

        self.dialog_data = {}
        # self.search_args = []
        self.setWindowTitle(title)
        self.appicon = gui.QIcon(icon)
        self.setWindowIcon(self.appicon)
        self.resize(1200, 900)

    def create_menu(self):
        """build application menu
        """
        menu_bar = self.menuBar()
        self.contextmenu_items = []
        for menu_text, data in self.editor.get_menulist():
            menu = qtw.QMenu(menu_text, self)
            for item in data:
                if len(item) == 1:
                    menu.addSeparator()
                    continue
                menuitem_text, hotkey, modifiers, status_text, callback = item[:5]
                if 'A' in modifiers:
                    hotkey = f"Alt+{hotkey}"
                if 'C' in modifiers:
                    hotkey = f"Ctrl+{hotkey}"
                if 'S' in modifiers:
                    hotkey = f"Shift+{hotkey}"
                act = gui.QAction(menuitem_text, self)
                menu.addAction(act)
                act.setStatusTip(status_text)
                act.setShortcut(hotkey)
                act.triggered.connect(callback)
                if menuitem_text.startswith('Advance selection'):
                    act.setCheckable(True)
                    self.adv_menu = act
                elif menu_text == '&View':
                    self.contextmenu_items.append(('A', act))
                elif menuitem_text == 'Add &DTD':
                    self.dtd_menu = act
                elif menuitem_text == 'Add &Stylesheet':
                    self.css_menu = act
                # if menu_text in ('&Edit', '&Search', '&HTML'):
                #     self.contextmenu_items.append(('M', menu))
                # moet bovenstaande IF niet ook uitgesprongen?
                # nu krijg je voor elke action het hele menu geappend, hoeft toch maar één keer?
            if menu_text == '&View':
                self.contextmenu_items.append(('', ''))
            elif menu_text in ('&Edit', '&Search', '&HTML'):
                self.contextmenu_items.append(('M', menu))
            menu_bar.addMenu(menu)

    def create_splitter(self):
        "create main window"
        self.pnl = qtw.QSplitter(self)
        self.setCentralWidget(self.pnl)

    def create_tree_on_left(self):
        "create treeview for editing"
        self.tree = VisualTree(self)
        self.tree.headerItem().setHidden(True)
        self.pnl.addWidget(self.tree)

    def create_preview_on_right(self):
        "create html view"
        # self.html = webkit.QWebView(self.pnl)  # , -1,
        self.html = webeng.QWebEngineView(self.pnl)
        self.pnl.addWidget(self.html)

    def create_statusbar_at_bottom(self):
        "create area for status messages"
        self.sb = self.statusBar()

    def finalize_display(self):
        "finish off screen creation"
        self.tree.resize(500, 100)
        self.pnl.setSizes([300, 900])
        self.tree.setFocus()
        self.adv_menu.setChecked(True)
        self.show()

    def go(self):
        """show the screen
        """
        sys.exit(self.app.exec())

    def get_screen_title(self):
        "retrieve the screen's title"
        return self.windowTitle()

    def set_screen_title(self, title):
        "change the screen's title"
        self.setWindowTitle(title)

    @staticmethod
    def get_element_text(node):
        "return text in visual tree for this element"
        return node.text(0)

    @staticmethod
    def get_element_parent(node):
        "return parent in visual tree for this element"
        return node.parent()

    @staticmethod
    def get_element_parentpos(item):
        "return parent and position under parent in visual tree for this element"
        parent = item.parent()
        return parent, parent.indexOfChild(item)

    @staticmethod
    def get_element_data(node):
        "return attributes or inline text stored with this element"
        return node.data(0, core.Qt.ItemDataRole.UserRole)

    @staticmethod
    def get_element_children(node):
        "return iterator over children in visual tree for this element"
        count = node.childCount()
        # return (node.child(idx) for idx in range(count))
        return [node.child(idx) for idx in range(count)]

    @staticmethod
    def set_element_text(node, text):
        "change text in visual tree for this element"
        node.setText(0, text)

    @staticmethod
    def set_element_data(node, data):
        "change stored attrs or inline text for this element"
        node.setData(0, core.Qt.ItemDataRole.UserRole, data)

    @staticmethod
    def addtreeitem(node, naam, data, index=-1):
        """itemnaam en -data toevoegen aan de interne tree
        default is achteraan onder node, anders index meegeven
        geeft referentie naar treeitem terug
        """
        newnode = qtw.QTreeWidgetItem()
        newnode.setText(0, naam)  # self.tree.AppendItem(node, naam)
        # data is ofwel leeg, ofwel een string, ofwel een dictionary
        newnode.setData(0, core.Qt.ItemDataRole.UserRole, data)  # self.tree.SetPyData(newnode, data)
        if index == -1:
            node.addChild(newnode)
        else:
            node.insertChild(index, newnode)
        return newnode

    def addtreetop(self, fname, titel):
        """titel en root item in tree instellen"""
        self.setWindowTitle(titel)
        self.tree.clear()
        self.top = qtw.QTreeWidgetItem()
        self.top.setText(0, fname)
        self.tree.addTopLevelItem(self.top)  # AddRoot(titel)

    def get_selected_item(self):
        """geef het in de tree geselecteerde item terug
        """
        return self.tree.currentItem()

    def set_selected_item(self, item):
        """stel het in de tree geselecteerde item in
        """
        self.tree.setCurrentItem(item)

    def init_tree(self, message):
        "toolkit specifieke zaken van tree instellen"
        self.tree.setCurrentItem(self.top)
        self.adv_menu.setChecked(True)
        self.show_statusbar_message(message)

    def show_statusbar_message(self, text):
        """toon tekst in de statusbar
        """
        self.sb.showMessage(text)

    def adjust_dtd_menu(self):
        "set text for dtd menu option"
        if self.editor.has_dtd:
            self.dtd_menu.setText('Remove &DTD')
            self.dtd_menu.setStatusTip('Remove the document type declaration')
        else:
            self.dtd_menu.setText('Add &DTD')
            self.dtd_menu.setStatusTip('Add a document type description')

    def popup_menu(self, arg=None):
        'build/show context menu'
        if arg is None:
            return
        # get type of node
        menu = qtw.QMenu()
        for itemtype, item in self.contextmenu_items:
            if itemtype == 'A':
                menu.addAction(item)
            elif itemtype == 'M':
                menu.addMenu(item)
            else:
                menu.addSeparator()
        # determine location of popup
        popup_location = self.tree.visualItemRect(arg).bottomRight()
        menu.exec(self.tree.mapToGlobal(popup_location))

    def keyReleaseEvent(self, event):
        "reimplemented event handler"
        skip = self.on_keyup(event)
        if not skip:
            super().keyReleaseEvent(event)

    def on_keyup(self, ev):
        "determine if key event needs to be skipped"
        ky = ev.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top and ky == core.Qt.Key.Key_Menu:
            self.popup_menu(item)
            skip = True
        return skip

    def ask_how_to_continue(self, title, text):
        """vraag of de wijzigingen moet worden opgeslagen
        """
        title = title or self._parent.title
        return ask_yesnocancel(self, text, title)

    @staticmethod
    def set_item_expanded(item, state):
        """show item's children
        """
        item.setExpanded(state)

    def expand(self):
        "toolkit specifieke voortzetting van gelijknamige editor methode"
        def expand_all(item):
            "recursively expand items"
            all_results = []
            for ix in range(item.childCount()):
                sub = item.child(ix)
                sub.setExpanded(True)
                all_results.append(sub)
                result = expand_all(sub)
                if result:
                    all_results.extend(result)
            return all_results
        item = self.tree.currentItem()
        self.tree.expandItem(item)
        results = expand_all(item)
        self.tree.resizeColumnToContents(0)
        self.tree.scrollToItem(results[-1])

    def collapse(self):
        "toolkit specifieke voortzetting van gelijknamige editor methode"
        def collapse_all(item):
            "recursively collapse items"
            for ix in range(item.childCount()):
                sub = item.child(ix)
                collapse_all(sub)
                sub.setExpanded(False)
        item = self.tree.currentItem()
        collapse_all(item)
        self.tree.collapseItem(item)
        self.tree.resizeColumnToContents(0)

    def get_adv_sel_setting(self):
        "callback for menu option"
        return self.adv_menu.isChecked()

    def refresh_preview(self, soup):
        "toolkit specifieke implementatie van gelijknamige editor methode"
        # print(os.path.abspath(self.editor.xmlfn))
        self.html.setHtml(str(soup).replace('%SOUP-ENCODING%', 'utf-8'),
                          baseUrl=core.QUrl.fromLocalFile(os.path.abspath(self.editor.xmlfn)))
        self.tree.setFocus()

    def do_delete_item(self, item):
        """remove element from tree
        """
        parent = item.parent()
        ix = parent.indexOfChild(item)
        if ix > 0:
            ix -= 1
            prev = parent.child(ix)
        else:
            prev = parent
            if prev == self.editor.root:
                prev = parent.child(ix + 1)
        parent.removeChild(item)
        return prev

    def meld(self, text):
        """notify about some information"""
        qtw.QMessageBox.information(self, self.editor.title, text)

    def ensure_item_visible(self, item):
        """make sure we can see the item
        """
        self.tree.scrollToItem(item)


class VisualTree(qtw.QTreeWidget):
    """tree representation of HTML
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.setDragDropMode(self.DragDropMode.InternalMove)
        self.setDropIndicatorShown(True)

    def mouseDoubleClickEvent(self, event):
        "reimplemented event handler"
        # item = self.itemAt(event.x(), event.y())
        item = self.itemAt(event.position().toPoint())
        if (item and item != self._parent.top
                and item.text(0).startswith(self._parent.editor.constants['ELSTART'])
                and item.childCount() == 0):
            self._parent.editor.edit()
            return
        super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        "reimplemented event handler"
        if event.button() == core.Qt.MouseButton.RightButton:
            # xc, yc = event.x(), event.y()
            # item = self.itemAt(xc, yc)
            item = self.itemAt(event.position().toPoint())
            if item and item != self._parent.top:
                self.setCurrentItem(item)
                self._parent.popup_menu(item)
                return
        super().mouseReleaseEvent(event)

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        item = self.itemAt(event.position().toPoint())
        if not item or not item.text(0).startswith(self._parent.editor.constants['ELSTART']):
            show_message(self._parent, 'HtmlEditor', 'Can only drop on element')
            return
        dragitem = self.selectedItems()[0]
        super().dropEvent(event)
        dropitem = dragitem.parent()
        self.setCurrentItem(dragitem)
        dropitem.setExpanded(True)
        self._parent.editor.mark_dirty(True)
        self._parent.editor.refresh_preview()
        # CodeViewDialog(self, title, caption, data).gui.show()


def show_message(parent, title, message):
    "show a message to the user"
    qtw.QMessageBox.information(parent, title, message)


def ask_yesnocancel(parent, prompt, title):
    """stelt een vraag en retourneert het antwoord

    1 = Yes, 0 = No, -1 = Cancel
    """
    retval = dict(zip((qtw.QMessageBox.StandardButton.Yes, qtw.QMessageBox.StandardButton.No,
                       qtw.QMessageBox.StandardButton.Cancel), (1, 0, -1)))
    hlp = qtw.QMessageBox.question(parent, title, prompt, qtw.QMessageBox.StandardButton.Yes
                                   | qtw.QMessageBox.StandardButton.No
                                   | qtw.QMessageBox.StandardButton.Cancel,
                                   defaultButton=qtw.QMessageBox.StandardButton.Yes)
    return retval[hlp]


def ask_for_text(parent, title, caption):
    "present a dialog to get some text input from the user"
    txt, ok = qtw.QInputDialog.getText(parent, title, caption)
    if ok:
        return txt
    return ''


def call_dialog(obj):
    "show a modal dialog and return results"
    edt = obj.gui.exec()
    if edt == qtw.QDialog.DialogCode.Accepted:
        return True, obj.parent.dialog_data
    return False, None


def show_dialog(obj):
    "show a nonmodal dialog"
    # print('called show_dialog with arg', obj)
    # breakpoint()
    obj.gui.show()


def ask_for_save_filename(parent, loc, mask):
    "stuur een dialoog om een bestandsnaam te vragen voor een nieuw bestand"
    return qtw.QFileDialog.getSaveFileName(parent, "Save file as ...", loc, mask)[0]


def ask_for_open_filename(parent, loc, mask):
    "stuur een dialoog om een bestandsnaam te vragen voor een bestaand bestand"
    return qtw.QFileDialog.getOpenFileName(parent, "Choose a file", loc, mask)[0]


def build_mask(ftype):
    """build mask for FileDialog
    """
    text, filetypes = masks['all']
    all_mask = f"{text} ({filetypes[0]})"
    text, filetypes = masks[ftype]
    filetypes_text = " ".join(filetypes)
    if os.name == 'posix':
        filetypes_text = f'{filetypes_text} {filetypes_text.upper()}'
    return f"{text} ({filetypes_text})" + ';;' + all_mask


class EditDialogGui(qtw.QDialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, master, parent, title):
        self.master = master
        self.title = title
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_topline(self):
        "define a line at the top of the display"
        topline = qtw.QHBoxLayout()
        self.vbox.addLayout(topline)
        return topline

    def add_label(self, topline, text):
        "add some fixed text"
        lbl = qtw.QLabel(text, self)
        topline.addWidget(lbl)

    def add_textinput(self, topline, text, width):
        "add an input box of a given width abd optionally set its text"
        tb = qtw.QLineEdit(self)
        tb.setMinimumWidth(width)
        tb.setText(text)
        topline.addWidget(tb)
        return tb

    def add_checkbox(self, topline, text, state):
        "add a checkbox and optionally set its state"
        cb = qtw.QCheckBox(text, self)
        if state:
            cb.toggle()
        topline.addWidget(cb)
        return cb

    def add_content_section(self):
        "add a container with a border around it"
        frm = qtw.QFrame()
        frm.setFrameStyle(qtw.QFrame.Shape.Box)
        box = qtw.QVBoxLayout()
        frm.setLayout(box)
        self.vbox.addWidget(frm)
        return box

    def add_table_to_section(self, section, columndefs, attrs):
        "add an editable table to the content area"
        hbox = qtw.QHBoxLayout()
        table = qtw.QTableWidget(self)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels([x[0] for x in columndefs])
        hdr = table.horizontalHeader()
        for ix, cdef in enumerate(columndefs):
            hdr.resizeSection(ix, cdef[1])
        hdr.setStretchLastSection(True)
        # table.verticalHeader().setVisible(False)
        table.setTabKeyNavigation(False)
        if attrs:
            for attr, value in attrs.items():
                row = table.rowCount()
                table.insertRow(row)
                table.setVerticalHeaderItem(row, qtw.QTableWidgetItem('  '))
                item = qtw.QTableWidgetItem(attr)
                table.setItem(row, 0, item)
                if attr in ('style', 'styledata'):
                    item.setFlags(item.flags() & ~core.Qt.ItemFlag.ItemIsEditable)
                item = qtw.QTableWidgetItem(value)
                table.setItem(row, 1, item)
                if attr in ('style', 'styledata'):
                    item.setFlags(item.flags() & ~core.Qt.ItemFlag.ItemIsEditable)
        hbox.addWidget(table)
        section.addLayout(hbox)
        return table

    def add_buttons_to_section(self, section, buttondefs):
        "add a line of buttons to the content area"
        result = []
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
            if text == self.master.style_text:
                result.append(btn)
        hbox.addStretch()
        section.addLayout(hbox)
        self.check_changes = False
        return result

    def add_textinput_to_section(self, section, text, width, height):
        "add a multiline text input field to the content area"
        hbox = qtw.QHBoxLayout()
        textbox = qtw.QTextEdit(self)
        textbox.resize(width, height)
        textbox.setText(text)
        hbox.addWidget(textbox)
        section.addLayout(hbox)
        return textbox

    def add_text_to_section(self, section, text):
        "add a line with text to the content area"
        section.addWidget(qtw.QLabel("Select document type:", self))

    def add_radiobutton_to_section(self, section, text, first, selected):
        "add a radiobutton on a line by itself to the content area"
        if not text:
            section.addSpacing(8)
            return
        if first:
            self.grp = qtw.QButtonGroup()
        radio = qtw.QRadioButton(text, self)
        if selected:
            radio.setChecked(True)
        self.grp.addButton(radio)
        section.addWidget(radio)
        return radio

    def add_buttons_to_bottom(self):
        "add a button strip with action buttons at the bottom"
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        ok_button = qtw.QPushButton('&Save', self)
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton('&Cancel', self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def set_focus_to(self, widget):
        "position for input"
        widget.setFocus()

    def get_radiobutton_state(self, rb):
        "return the state of a radiobutton"
        return rb.isChecked()

    def set_radiobutton_state(self, rb, state):
        "set the state of a radiobutton"
        rb.setChecked(state)

    def get_textinput_value(self, field):
        "return a textfield's contents"
        return field.text()

    def get_textarea_contents(self, field):
        "return a multiline textfield's contents"
        return field.toPlainText()

    def get_checkbox_state(self, field):
        "return the state od a checkbox"
        return field.isChecked()

    def set_button_text(self, btn, text):
        "change text on button"
        btn.setText(text)

    def get_table_rowcount(self, table):
        "return the number of rows in a table"
        return table.rowCount()

    def add_table_row(self, table, row):
        "add a row at the end of the table"
        table.insertRow(row)

    def add_table_rowitem(self, table, row, col, text, editable=True):
        "add an item to the new row and set its text and editability"
        item = qtw.QTableWidgetItem(text)
        table.setItem(row, col, item)
        if not editable:
            # item.setFlags(item.flags() & (not core.Qt.ItemFlag.ItemIsEditable))
            item.setFlags(item.flags() & ~core.Qt.ItemFlag.ItemIsEditable)

    def delete_table_row(self, table, row):
        "delete a row from the table"
        table.removeRow(row)

    def set_table_rowheader(self, table, row, text):
        "set an empty header for a new table row"
        table.setVerticalHeaderItem(row, qtw.QTableWidgetItem('  '))

    def select_table_cell(self, table, row, col):
        "select a cell from the table (for editing)"
        table.setCurrentCell(row, col)

    def get_selected_table_row(self, table):
        "return the selected table row"
        return table.currentRow()

    def get_tableitem_text(self, table, row, col):
        "return the text of a tableitem at a specific location"
        return table.item(row, col).text()

    def set_tableitem_text(self, table, row, col, text):
        "set the text for a tableitem at a specific location"
        table.item(row, col).setText(text)

    def reject(self):
        "controle bij afbreken: css data kan gewijzigd zijn"
        if hasattr(self.master, 'styledata'):
            if self.master.styledata != self.master.old_styledata:
                # breakpoint()
                qtw.QMessageBox.information(self, 'Let op', "bijbehorende style data is gewijzigd")
                self.master.refresh()
                return
        super().reject()

    def accept(self):
        "controle bij OK aanklikken"
        if hasattr(self.master, 'attr_table'):
            self.master.refresh()
        msg = self.master.confirm()
        if msg:
            qtw.QMessageBox.information(self, self.title, msg)
            return
        super().accept()


class SearchDialogGui(qtw.QDialog):
    """Dialog to get search arguments
    """
    def __init__(self, master, parent, title=""):
        self.master = master
        super().__init__(parent)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.setLayout(self.sizer)

    def setup_container(self):
        "define the grid"
        gsizer = qtw.QGridLayout()
        self.sizer.addLayout(gsizer)
        return gsizer

    def add_title(self, gsizer, text, row, col):
        "add some text at the top"
        gsizer.addWidget(qtw.QLabel(text, self), row, col, 1, 3)

    def add_text(self, gsizer, text, row, col):
        "add some fixed text to a cell"
        gsizer.addWidget(qtw.QLabel(text, self), row, col)

    def add_lineinput(self, gsizer, row, col, callback):
        "add a text input box to a cell"
        txt = qtw.QLineEdit(self)
        # height = txt.size().height()
        # txt.setMinimumHeight(height)
        txt.textChanged.connect(callback)
        gsizer.addWidget(txt, row, col)
        return txt

    def add_checkbox(self, gsizer, text, row, col):
        "add a checkbox to a cell"
        cb = qtw.QCheckBox(text, self)
        gsizer.addWidget(cb, 5, 3, 1, 3)
        return cb

    def add_description(self):
        "add search summary text"
        hsizer = qtw.QHBoxLayout()
        lbl = qtw.QLabel('', self)
        hsizer.addWidget(lbl)
        self.sizer.addLayout(hsizer)
        lbl.setWordWrap(True)
        return lbl

    def add_buttons_to_bottom(self):
        "add some action buttons at the bottom of the display"
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        btn = qtw.QPushButton('&Ok', self)
        btn.clicked.connect(self.accept)
        btn.setDefault(True)
        hsizer.addWidget(btn)
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.reject)
        hsizer.addWidget(btn)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def set_lineinput_value(self, field, text):
        "set the value for a text input field"
        field.setText(text)

    def get_lineinput_value(self, field):
        "return the value of a text input field"
        return field.text()

    def get_checkbox_state(self, field):
        "return the state od a checkbox"
        return field.isChecked()

    def set_focus_to(self, widget):
        "position for input"
        widget.setFocus()

    def set_label_text(self, field, text):
        "update the value for a label field"
        field.setText(text)

    def update_size(self):
        "adjust widget sizer after changing text contents"
        # self.sizer.update()

    def accept(self):
        """confirm dialog and pass changed data to parent"""
        msg = self.master.confirm()
        if msg:
            qtw.QMessageBox.information(self, self.master.title, msg)
            widget = self.txt_element_replace if 'replace' in msg else self.txt_element
            self.set_focus_to(widget)
        else:
            super().accept()


class AddDialogGui(qtw.QDialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""
    def __init__(self, master, parent, title):
        self.master = master
        self.title = title
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_content_section(self):
        "add a container with a border around it"
        frm = qtw.QFrame()
        frm.setFrameStyle(qtw.QFrame.Shape.Box)
        # grid = qtw.QVBoxLayout()
        grid = qtw.QGridLayout()
        frm.setLayout(grid)
        self.vbox.addWidget(frm)
        return grid

    def add_text_to_section(self, grid, text, row, col):
        "add fixed text to a cell in the content area"
        grid.addWidget(qtw.QLabel(text, self), row, col)

    def add_textinput_to_section(self, grid, row, col, text='', width=0, callback=None):
        "add a text input to a cell in the content area"
        edit = qtw.QLineEdit(text, self)
        if width:
            edit.setMinimumWidth(width)
        if callback:
            edit.textChanged.connect(callback)
        grid.addWidget(edit, row, col)
        return edit

    def add_button_line_to_section(self, grid, row, buttondefs):
        "add a line with one or more buttons to the content area"
        result = []
        box = qtw.QHBoxLayout()
        box.addStretch()
        for text, callback in buttondefs:
            button = qtw.QPushButton(text, self)
            button.clicked.connect(callback)
            box.addWidget(button)
            result.append(button)
        box.addStretch()
        grid.addLayout(box, row, 0, 1, 2)
        return result

    def add_spinbox_to_section(self, grid, row, col, maxvalue=0, startvalue=0, callback=None):
        "add a spinbox to a cell in the content area"
        hbox = qtw.QHBoxLayout()
        sb = qtw.QSpinBox(self)  # .pnl, -1, size = (40, -1))
        if maxvalue:
            sb.setMaximum(maxvalue)
        sb.setValue(startvalue)
        if callback:
            sb.valueChanged.connect(callback)
        hbox.addWidget(sb)
        hbox.addStretch()
        grid.addLayout(hbox, row, col)
        return sb

    def add_combobox_to_section(self, grid, row, col, values, callback=None):
        "add a combobox to a cell in the content area"
        select = qtw.QComboBox(self)
        select.addItems(values)
        if callback:
            select.activated.connect(callback)
        grid.addWidget(select, row, col)
        return select

    def add_checkbox_to_section(self, grid, row, col, text, checked=False, callback=None):
        "add a checkbox to a cell in the content area"
        cb = qtw.QCheckBox(text, self)
        if checked:
            cb.setChecked(checked)
        if callback:
            cb.stateChanged.connect(callback)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(cb)
        grid.addLayout(hbox, row, col)
        return cb

    def add_table_to_section(self, grid, row, initialrows, headers, callback=None):
        "add a full-width table to the content area"
        # breakpoint()
        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(1)  # addStretch()
        table = qtw.QTableWidget(self)
        table.setRowCount(initialrows)
        table.setColumnCount(len(headers))
        hdr = table.horizontalHeader()
        hdr.setStretchLastSection(True)
        # hdr.resizeSection(0, 252)
        if callback:
            hdr.setSectionsClickable(True)
            hdr.sectionClicked.connect(callback)
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        hbox.addWidget(table)
        hbox.addSpacing(1)  # addStretch()
        grid.addLayout(hbox, row, 0, 1, 2)
        return table

    def add_buttons_to_bottom(self, extra=()):
        "add a button strip with action buttons at the bottom"
        buttons = []
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        ok_button = qtw.QPushButton('&Save', self)
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        hbox.addWidget(ok_button)
        if extra:
            inline_button = qtw.QPushButton(extra[0], self)
            inline_button.clicked.connect(extra[1])
            hbox.addWidget(inline_button)
            buttons.append(inline_button)
        cancel_button = qtw.QPushButton('&Cancel', self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch()
        self.vbox.addLayout(hbox)
        return buttons

    def set_focus_to(self, widget):
        "position for input"
        widget.setFocus()

    def get_textinput_value(self, field):
        "return a textfield's contents"
        return field.text()

    def set_textinput_value(self, field, value):
        "set a textfield's contents"
        return field.setText(value)

    def get_combobox_text(self, cb):
        "return the selected text in a combobox"
        return cb.currentText()

    def get_spinbox_value(self, sb):
        "return the value of a spinbox"
        return sb.value()

    def get_checkbox_state(self, cb):
        "return the state of a checkbox"
        return cb.isChecked()

    def get_table_columncount(self, table):
        "return the number of columns in the table"
        return table.columnCount()

    def get_table_rowcount(self, table):
        "return the number of rows in the table"
        return table.rowCount()

    def get_tablecell_itemtext(self, table, row, col):
        "return the contents of a cell at a given position"
        return table.item(row, col).text()

    def set_table_headers(self, table, headers, widths):
        "reset the column titles and widths "
        table.setHorizontalHeaderLabels(headers)
        hdr = table.horizontalHeader()
        for ix, section in enumerate(widths):
            hdr.resizeSection(ix, section)

    def enable_table_header(self, table, value):
        "make table header (visible and) clickable"
        hdr = table.horizontalHeader()
        hdr.setVisible(value)

    def add_table_column(self, table, colno):
        "add a table column"
        table.insertColumn(colno)

    def add_table_row(self, table, rowno):
        "add a table row"
        table.insertRow(rowno)

    def remove_table_column(self, table, colno):
        "remove a table column"
        table.removeColumn(colno)

    def remove_table_row(self, table, rowno):
        "remove a table row"
        table.removeRow(rowno)

    def get_table_column(self, *args):
        "return the column for which the header was clicked"
        # simply return the number that's passed in from table.header.sectionClicked
        return args[0]

    def enable_widget(self, widget, value):
        "make a widget responsive or not"
        widget.setEnabled(value)

    def accept(self):
        "controle bij OK aanklikken"
        msg = self.master.confirm()
        if msg:
            qtw.QMessageBox.information(self, self.title, msg)
            return
        super().accept()


class ScrolledTextDialogGui(qtw.QDialog):
    """dialoog voor het tonen van validatieoutput

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        self.resize(800, 600)

    def add_top_label(self, text):
        "add a message to the top of the display"
        hbox = qtw.QHBoxLayout()
        lbl = qtw.QLabel(self)
        lbl.setText(text)
        hbox.addWidget(lbl)
        self.vbox.addLayout(hbox)

    def add_text_area(self):
        "build the space for the text to display"
        hbox = qtw.QHBoxLayout()
        text = qtw.QTextEdit(self)
        text.setReadOnly(True)
        hbox.addWidget(text)
        self.vbox.addLayout(hbox)
        return text

    def add_bottom_buttons(self, buttondefs):
        "add one or more action buttons"
        # breakpoint()
        print('called ScrolledTextDialogGui.add_bottom_buttons with arg', buttondefs)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        # first = True
        for text, callback in buttondefs:
            button = qtw.QPushButton(text, self)
            print(f'called clicked.connect with arg {callback} on button {button} with text {text}')
            button.clicked.connect(callback)
            # if first:
            #     button.setDefault(True)
            #     first = False
            hbox.addWidget(button)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def set_textarea_contents(self, textfield, data):
        "transmit the text to display"
        textfield.setPlainText(data)


class CodeViewDialogGui(qtw.QDialog):
    """dialoog voor het tonen van de broncode

    create a window with a scintilla text widget and an ok button
    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title):
        # print('called CodeviewDialogGui')
        super().__init__(parent)
        self.setWindowTitle(title)
        # self.setWindowIcon(self._parent.appicon)
        self.vbox = qtw.QVBoxLayout()
        self.resize(800, 600)
        self.setLayout(self.vbox)

    def add_top_message(self, text):
        "add a message to the top of the display"
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(text, self))
        self.vbox.addLayout(hbox)

    def add_content_area(self, data):
        "define the space for the main content"
        hbox = qtw.QHBoxLayout()
        text = qsc.QsciScintilla(self)
        self.setup_text(text)
        text.setText(data)
        text.setReadOnly(True)
        hbox.addWidget(text)
        self.vbox.addLayout(hbox)
        return text  # alleen t.b.v. unittest

    def add_bottom_button(self):
        "add an action button at the bottom of the display"
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        button = qtw.QPushButton('&Done', self)
        button.clicked.connect(self.close)
        # button.setDefault(True)
        button.setFocus()
        hbox.addWidget(button)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def setup_text(self, textfield):
        "define the scintilla widget's properties"
        # Set the default font
        font = gui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        textfield.setFont(font)
        textfield.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = gui.QFontMetrics(font)
        textfield.setMarginsFont(font)
        textfield.setMarginWidth(0, fontmetrics.horizontalAdvance("00000"))
        textfield.setMarginLineNumbers(0, True)
        textfield.setMarginsBackgroundColor(gui.QColor("#cccccc"))

        # Enable brace matching, auto-indent, code-folding
        textfield.setBraceMatching(qsc.QsciScintilla.BraceMatch.SloppyBraceMatch)
        textfield.setAutoIndent(True)
        textfield.setFolding(qsc.QsciScintilla.FoldStyle.PlainFoldStyle)

        # Current line visible with special background color
        textfield.setCaretLineVisible(True)
        textfield.setCaretLineBackgroundColor(gui.QColor("#ffe4e4"))

        # Set HTML lexer
        lexer = qsc.QsciLexerHTML()
        lexer.setDefaultFont(font)
        textfield.setLexer(lexer)
        return font  # alleen t.b.v. unitttest
