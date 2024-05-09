"""unittests for ./ashe/gui_qt.py
"""
from ashe import gui_qt as testee


class TestVisualTree:
    """unittest for gui_qt.VisualTree
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.VisualTree object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called VisualTree.__init__ with args', args)
        monkeypatch.setattr(testee.VisualTree, '__init__', mock_init)
        testobj = testee.VisualTree()
        assert capsys.readouterr().out == 'called VisualTree.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for VisualTree.__init__
        """
        testobj = testee.VisualTree(parent)
        assert capsys.readouterr().out == ("")

    def _test_mouseDoubleClickEvent(self, monkeypatch, capsys):
        """unittest for VisualTree.mouseDoubleClickEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mouseDoubleClickEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for VisualTree.mouseReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mouseReleaseEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_dropEvent(self, monkeypatch, capsys):
        """unittest for VisualTree.dropEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.dropEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")


class TestEditorGui:
    """unittest for gui_qt.EditorGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.EditorGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditorGui.__init__ with args', args)
        monkeypatch.setattr(testee.EditorGui, '__init__', mock_init)
        testobj = testee.EditorGui()
        assert capsys.readouterr().out == 'called EditorGui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for EditorGui.__init__
        """
        testobj = testee.EditorGui(parent=None, editor=None, err=None, icon=None)
        assert capsys.readouterr().out == ("")

    def _test_go(self, monkeypatch, capsys):
        """unittest for EditorGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_menu(self, monkeypatch, capsys):
        """unittest for EditorGui.setup_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_menu() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_screen_title(self, monkeypatch, capsys):
        """unittest for EditorGui.get_screen_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_screen_title() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_screen_title(self, monkeypatch, capsys):
        """unittest for EditorGui.set_screen_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_screen_title(title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_element_text(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_element_text(node) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_element_parent(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_parent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_element_parent(node) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_element_parentpos(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_parentpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_element_parentpos(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_element_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_element_data(node) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_element_children(self, monkeypatch, capsys):
        """unittest for EditorGui.get_element_children
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_element_children(node) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_element_text(self, monkeypatch, capsys):
        """unittest for EditorGui.set_element_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_element_text(node, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_element_data(self, monkeypatch, capsys):
        """unittest for EditorGui.set_element_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_element_data(node, data) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_addtreeitem(self, monkeypatch, capsys):
        """unittest for EditorGui.addtreeitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.addtreeitem(node, naam, data, index=-1) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_addtreetop(self, monkeypatch, capsys):
        """unittest for EditorGui.addtreetop
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.addtreetop(fname, titel) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_item(self, monkeypatch, capsys):
        """unittest for EditorGui.get_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_selected_item(self, monkeypatch, capsys):
        """unittest for EditorGui.set_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_selected_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_tree(self, monkeypatch, capsys):
        """unittest for EditorGui.init_tree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_tree(message) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_statusbar_message(self, monkeypatch, capsys):
        """unittest for EditorGui.show_statusbar_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_statusbar_message(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_adjust_dtd_menu(self, monkeypatch, capsys):
        """unittest for EditorGui.adjust_dtd_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.adjust_dtd_menu() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_popup_menu(self, monkeypatch, capsys):
        """unittest for EditorGui.popup_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.popup_menu(arg=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for EditorGui.keyReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.keyReleaseEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_keyup(self, monkeypatch, capsys):
        """unittest for EditorGui.on_keyup
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_keyup(ev=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ask_how_to_continue(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_how_to_continue
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_how_to_continue(title, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_mask(self, monkeypatch, capsys):
        """unittest for EditorGui.build_mask
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_mask(ftype) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ask_for_open_filename(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_for_open_filename
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_for_open_filename() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ask_for_save_filename(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_for_save_filename
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_for_save_filename() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for EditorGui.set_item_expanded
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_item_expanded(item, state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_expand(self, monkeypatch, capsys):
        """unittest for EditorGui.expand
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.expand() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_collapse(self, monkeypatch, capsys):
        """unittest for EditorGui.collapse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.collapse() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_adv_sel_setting(self, monkeypatch, capsys):
        """unittest for EditorGui.get_adv_sel_setting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_adv_sel_setting() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh_preview(self, monkeypatch, capsys):
        """unittest for EditorGui.refresh_preview
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh_preview(soup) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_call_dialog(self, monkeypatch, capsys):
        """unittest for EditorGui.call_dialog
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.call_dialog(obj) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_edit_element(self, monkeypatch, capsys):
        """unittest for EditorGui.do_edit_element
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_edit_element(tagdata, attrdict) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_add_element(self, monkeypatch, capsys):
        """unittest for EditorGui.do_add_element
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_add_element(where) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_edit_textvalue(self, monkeypatch, capsys):
        """unittest for EditorGui.do_edit_textvalue
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_edit_textvalue(textdata) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_add_textvalue(self, monkeypatch, capsys):
        """unittest for EditorGui.do_add_textvalue
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_add_textvalue() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_delete_item(self, monkeypatch, capsys):
        """unittest for EditorGui.do_delete_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_delete_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_search_args(self, monkeypatch, capsys):
        """unittest for EditorGui.get_search_args
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_search_args(replace=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_meld(self, monkeypatch, capsys):
        """unittest for EditorGui.meld
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.meld(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_meld_fout(self, monkeypatch, capsys):
        """unittest for EditorGui.meld_fout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.meld_fout(text, abort=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ask_yesnocancel(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_yesnocancel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_yesnocancel(prompt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ask_for_text(self, monkeypatch, capsys):
        """unittest for EditorGui.ask_for_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_for_text(prompt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ensure_item_visible(self, monkeypatch, capsys):
        """unittest for EditorGui.ensure_item_visible
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ensure_item_visible(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_dtd(self, monkeypatch, capsys):
        """unittest for EditorGui.get_dtd
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_dtd() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_css_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_css_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_css_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_link_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_link_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_link_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_image_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_image_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_image_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_video_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_video_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_video_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_audio_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_audio_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_audio_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_list_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_list_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_table_data(self, monkeypatch, capsys):
        """unittest for EditorGui.get_table_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_table_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_validate(self, monkeypatch, capsys):
        """unittest for EditorGui.validate
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.validate(htmlfile, fromdisk) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_code(self, monkeypatch, capsys):
        """unittest for EditorGui.show_code
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_code(title, caption, data) == "expected_result"
        assert capsys.readouterr().out == ("")
