"""PyQt5 specifieke routines voor mijn op een treeview gebaseerde HTML-editor
"""
import os
import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
## import PyQt5.QtWebKit as webkit
import PyQt5.QtWebKitWidgets as webkit

from ashe.dialogs_qt import cssedit_available, HMASK, ElementDialog, \
    TextDialog, DtdDialog, CssDialog, LinkDialog, ImageDialog, VideoDialog, \
    AudioDialog, ListDialog, TableDialog, ScrolledTextDialog, CodeViewDialog, \
    SearchDialog



class VisualTree(qtw.QTreeWidget):
    """tree representation of HTML
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.InternalMove)
        self.setDropIndicatorShown(True)

    def mouseDoubleClickEvent(self, event):
        "reimplemented event handler"
        item = self.itemAt(event.x(), event.y())
        if item and item != self._parent.top:
            if str(item.text(0)).startswith(self._parent.editor.constants['ELSTART']) and \
                    item.childCount() == 0:
                self._parent.edit()
                return
        super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        "reimplemented event handler"
        if event.button() == core.Qt.RightButton:
            xc, yc = event.x(), event.y()
            item = self.itemAt(xc, yc)
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
        item = self.itemAt(event.pos())
        if not item or not item.text(0).startswith(self._parent.editor.constants['ELSTART']):
            self._parent.meld('Can only drop on element')
            return
        dragitem = self.selectedItems()[0]
        super().dropEvent(event)
        self._parent.tree_dirty = True
        dropitem = dragitem.parent()
        self.setCurrentItem(dragitem)
        dropitem.setExpanded(True)
        self._parent.refresh_preview()


class MainFrame(qtw.QMainWindow):
    "Main GUI"

    def __init__(self, parent=None, editor=None, err=None, icon=None):
        self.parent = parent
        self.editor = editor
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        if err:
            self.meld(err)
            return

        self.dialog_data = {}
        self.search_args = []
        self.appicon = gui.QIcon(icon)
        self.setWindowIcon(self.appicon)
        self.resize(1020, 900)

        self._setup_menu()
        self.in_contextmenu = False

        self.pnl = qtw.QSplitter(self)
        self.setCentralWidget(self.pnl)

        self.tree = VisualTree(self)
        self.tree.headerItem().setHidden(True)
        self.pnl.addWidget(self.tree)

        self.html = webkit.QWebView(self.pnl)  # , -1,
        self.pnl.addWidget(self.html)

        self.sb = self.statusBar()

        self.tree.resize(500, 100)
        self.tree.setFocus()

    def go(self):
        self.adv_menu.setChecked(True)
        self.show()
        err = self.editor.getsoup(self.editor.xmlfn) or ''
        if not err:
            self.editor.refresh_preview()
        sys.exit(self.app.exec_())

    def _setup_menu(self):
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
                    hotkey = "+".join(("Alt", hotkey))
                if 'C' in modifiers:
                    hotkey = "+".join(("Ctrl", hotkey))
                if 'S' in modifiers:
                    hotkey = "+".join(("Shift", hotkey))
                act = qtw.QAction(menuitem_text, self)
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
                    if not cssedit_available:
                        act.setDisabled(True)
                if menu_text in ('&Edit', '&HTML'):
                    self.contextmenu_items.append(('M', menu))
            if menu_text == '&View':
                self.contextmenu_items.append(('', ''))
            menu_bar.addMenu(menu)

    # def setfilenametooltip((self):
        # """bedoeld om de filename ook als tooltip te tonen, uit te voeren
        # aan het eind van new, open, save, saveas en reload"""
        # zie ticket 406 voor een overweging om dit helemaal achterwege te laten

    def mark_dirty(self, state):
        "update visual signs that the source was changed"
        title = str(self.windowTitle())
        test = ' - ' + self.editor.title
        test2 = '*' + test
        if state:
            if test2 not in title:
                title = title.replace(test, test2)
        else:
            title = title.replace(test2, test)
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
        "return attributes stored with this element"
        return node.data(0, core.Qt.UserRole)

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
        "change stored attrs for this element"""
        node.setData(0, core.Qt.UserRole, data)

    def addtreeitem(self, node, naam, data, index=-1):
        """itemnaam en -data toevoegen aan de interne tree
        default is achteraan onder node, anders index meegeven
        geeft referentie naar treeitem terug
        """
        newnode = qtw.QTreeWidgetItem()
        newnode.setText(0, naam)  # self.tree.AppendItem(node, naam)
        # data is ofwel leeg, ofwel een string, ofwel een dictionary
        newnode.setData(0, core.Qt.UserRole, data)  # self.tree.SetPyData(newnode, data)
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
        "toolkit specifieke voortzetting van gelijknamige editor methode"
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
        # get type of node
        menu = qtw.QMenu()
        for itemtype, item in self.contextmenu_items:
            if itemtype == 'A':
                act = menu.addAction(item)
                if item == self.css_menu:
                    if not cssedit_available:
                        act.setDisabled(True)
            elif itemtype == 'M':
                menu.addMenu(item)
            else:
                menu.addSeparator()
        y = self.tree.visualItemRect(arg).bottom()
        x = self.tree.visualItemRect(arg).left()
        popup_location = core.QPoint(int(x) + 200, y)
        self.in_contextmenu = True
        menu.exec_(self.tree.mapToGlobal(popup_location))
        self.in_contextmenu = False
        # del menu

    def keyReleaseEvent(self, event):
        "reimplemented event handler"
        skip = self.on_keyup(event)
        if not skip:
            super().keyReleaseEvent(event)

    def on_keyup(self, ev=None):
        "determine if key event needs to be skipped"
        ky = ev.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top:
            if ky == core.Qt.Key_Menu:
                self.popup_menu(item)
                skip = True
        return skip

    def ask_how_to_continue(self, title, text):
        """vraag of de wijzigingen moet worden opgeslagen
        keuze uitvoeren en teruggeven (i.v.m. eventueel gekozen Cancel)
        retourneert 1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((qtw.QMessageBox.Yes, qtw.QMessageBox.No, qtw.QMessageBox.Cancel),
                          (1, 0, -1)))
        hlp = qtw.QMessageBox.question(self, title, text, qtw.QMessageBox.Yes |
                                       qtw.QMessageBox.No | qtw.QMessageBox.Cancel,
                                       defaultButton=qtw.QMessageBox.Yes)
        return retval[hlp]

    def ask_for_open_filename(self):
        """open een dkialoog om te vragen welk file geladen moet worden
        """
        filename, _ = qtw.QFileDialog.getOpenFileName(self, "Choose a file",
                                                      self.editor.xmlfn or os.getcwd(), HMASK)
        return filename

    def ask_for_save_filename(self):
        """open een dialoog om te vragen onder welke naam de html moet worden opgeslagen
        """
        filename = qtw.QFileDialog.getSaveFileName(self, "Save file as ...",
                                                   self.editor.xmlfn or os.getcwd(), HMASK)
        print(filename)
        return filename

    def set_item_expanded(self, item, state):
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
        self.advance_selection_on_add = self.adv_menu.isChecked()

    def refresh_preview(self, soup):
        "toolkit specifieke voortzetting van gelijknamige editor methode"
        self.html.setHtml(str(soup).replace('%SOUP-ENCODING%', 'utf-8'))
        self.tree.setFocus()

    def call_dialog(self, obj):
        "send dialog and transmit results"
        edt = obj.exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        return False, None

    def do_edit_element(self, tagdata, attrdict):
        """show dialog for existing element"""
        obj = ElementDialog(self, title='Edit an element', tag=tagdata, attrs=attrdict)
        return self.call_dialog(obj)
        edt = ElementDialog(self, title='Edit an element', tag=tagdata, attrs=attrdict).exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def do_add_element(self, where):
        """show dialog for new element"""
        obj = ElementDialog(self, title="New element (insert {0})".format(where))
        return self.call_dialog(obj)
        edt = ElementDialog(self, title="New element (insert {0})".format(where)).exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def do_edit_textvalue(self, textdata):
        """show dialog for existing text"""
        return self.call_dialog(TextDialog(self, title='Edit Text', text=textdata))
        edt = TextDialog(self, title='Edit Text', text=textdata).exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def do_add_textvalue(self):
        """show dialog for new text"""
        return self.call_dialog(TextDialog(self, title="New Text"))
        edt = TextDialog(self, title="New Text").exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def ask_for_condition(self):
        "zet een IE conditie om het element heen"
        cond, ok = qtw.QInputDialog.getText(self, self.title, 'Enter the condition', text='')
        if ok:
            return cond
        return ''

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

    def get_search_args(self):
        """show search options dialog"""
        return self.call_dialog(SearchDialog(self, title='Search options'))
        edt = SearchDialog(self, title='Search options').exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.search_args
        else:
            return False, None

    def meld(self, text):
        """notify about some information"""
        self.in_dialog = True
        qtw.QMessageBox.information(self, self.editor.title, text)

    def meld_fout(self, text, abort=False):
        """notify about an error"""
        self.in_dialog = True
        qtw.QMessageBox.critical(self, self.title, text)
        if abort:
            self.quit()

    def ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((qtw.QMessageBox.Yes, qtw.QMessageBox.No,
                           qtw.QMessageBox.Cancel), (1, 0, -1)))
        self.in_dialog = True
        h = qtw.QMessageBox.question(
            self, self.title, prompt,
            qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel,
            defaultButton=qtw.QMessageBox.Yes)
        return retval[h]

    def ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        self.in_dialog = True
        data, ok = qtw.QInputDialog.getText(self, self.title, prompt, qtw.QLineEdit.Normal, "")
        return data, ok

    def ensure_item_visible(self, item):
        """make sure we can see the item
        """
        self.tree.scrollToItem(item)

    def get_dtd(self):
        """show dialog for dtd
        """
        return self.call_dialog(DtdDialog(self))
        edt = DtdDialog(self).exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def get_css_data(self):
        """show dialog for new style element
        """
        return self.call_dialog(CssDialog(self))
        edt = CssDialog(self).exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def get_link_data(self):
        """show dialog for new link element
        """
        return self.call_dialog(LinkDialog(self))
        edt = LinkDialog(self).exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def get_image_data(self):
        """show dialog for new image element
        """
        return self.call_dialog(ImageDialog(self))
        edt = ImageDialog(self).exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None

    def get_video_data(self):
        """show dialog for new video element
        """
        return self.call_dialog(VideoDialog(self))

    def get_audio_data(self):
        """show dialog for new audio element
        """
        return self.call_dialog(AudioDialog(self))

    def get_list_data(self):
        """show dialog for new list element
        """
        return self.call_dialog(ListDialog(self))

    def get_table_data(self):
        """show dialog for new table element
        """
        return self.call_dialog(TableDialog(self))

    def validate(self, htmlfile, fromdisk):
        "start validation"
        # deze dialoog is gecodeerd in de dialogs module maar moet het valideren daarbinnen wel
        # gebeuren?
        dlg = ScrolledTextDialog(self, "Validation output", htmlfile=htmlfile, fromdisk=fromdisk)
        dlg.show()

    def show_code(self, title, caption, data):
        "show dialog for view source"
        dlg = CodeViewDialog(self, title, caption, data)
        dlg.show()
