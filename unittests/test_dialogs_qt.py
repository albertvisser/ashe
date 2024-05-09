"""unittests for ./ashe/dialogs_qt.py
"""
from ashe import dialogs_qt as testee


class TestElementDialog:
    """unittest for dialogs_qt.ElementDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ElementDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ElementDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ElementDialog, '__init__', mock_init)
        testobj = testee.ElementDialog()
        assert capsys.readouterr().out == 'called ElementDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ElementDialog.__init__
        """
        testobj = testee.ElementDialog(parent, title='', tag='', attrs=None)
        assert capsys.readouterr().out == ("")

    def _test_on_add(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_add
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_add() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_del(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_del
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_del() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_style(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_style
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_style() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh(self, monkeypatch, capsys):
        """unittest for ElementDialog.refresh
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_reject(self, monkeypatch, capsys):
        """unittest for ElementDialog.reject
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.reject() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for ElementDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestTextDialog:
    """unittest for dialogs_qt.TextDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.TextDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__ with args', args)
        monkeypatch.setattr(testee.TextDialog, '__init__', mock_init)
        testobj = testee.TextDialog()
        assert capsys.readouterr().out == 'called TextDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for TextDialog.__init__
        """
        testobj = testee.TextDialog(parent, title='', text=None, show_commented=True)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for TextDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSearchDialog:
    """unittest for dialogs_qt.SearchDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.SearchDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SearchDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SearchDialog, '__init__', mock_init)
        testobj = testee.SearchDialog()
        assert capsys.readouterr().out == 'called SearchDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SearchDialog.__init__
        """
        testobj = testee.SearchDialog(parent, title="", replace=False)
        assert capsys.readouterr().out == ("")

    def _test_set_search(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_search
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_search() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SearchDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestDtdDialog:
    """unittest for dialogs_qt.DtdDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.DtdDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called DtdDialog.__init__ with args', args)
        monkeypatch.setattr(testee.DtdDialog, '__init__', mock_init)
        testobj = testee.DtdDialog()
        assert capsys.readouterr().out == 'called DtdDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for DtdDialog.__init__
        """
        testobj = testee.DtdDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for DtdDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestCssDialog:
    """unittest for dialogs_qt.CssDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.CssDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CssDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CssDialog, '__init__', mock_init)
        testobj = testee.CssDialog()
        assert capsys.readouterr().out == 'called CssDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CssDialog.__init__
        """
        testobj = testee.CssDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_kies(self, monkeypatch, capsys):
        """unittest for CssDialog.kies
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.kies() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_nieuw(self, monkeypatch, capsys):
        """unittest for CssDialog.nieuw
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.nieuw(evt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_edit(self, monkeypatch, capsys):
        """unittest for CssDialog.edit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.edit(evt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_select_file(self, monkeypatch, capsys):
        """unittest for CssDialog.select_file
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_file(create=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_inline(self, monkeypatch, capsys):
        """unittest for CssDialog.on_inline
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_inline() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for CssDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestLinkDialog:
    """unittest for dialogs_qt.LinkDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.LinkDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LinkDialog.__init__ with args', args)
        monkeypatch.setattr(testee.LinkDialog, '__init__', mock_init)
        testobj = testee.LinkDialog()
        assert capsys.readouterr().out == 'called LinkDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for LinkDialog.__init__
        """
        testobj = testee.LinkDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_kies(self, monkeypatch, capsys):
        """unittest for LinkDialog.kies
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.kies() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_ltext(self, monkeypatch, capsys):
        """unittest for LinkDialog.set_ltext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_ltext(chgtext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_ttext(self, monkeypatch, capsys):
        """unittest for LinkDialog.set_ttext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_ttext(chgtext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for LinkDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestImageDialog:
    """unittest for dialogs_qt.ImageDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ImageDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ImageDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ImageDialog, '__init__', mock_init)
        testobj = testee.ImageDialog()
        assert capsys.readouterr().out == 'called ImageDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ImageDialog.__init__
        """
        testobj = testee.ImageDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_kies(self, monkeypatch, capsys):
        """unittest for ImageDialog.kies
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.kies() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_ltext(self, monkeypatch, capsys):
        """unittest for ImageDialog.set_ltext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_ltext(chgtext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_ttext(self, monkeypatch, capsys):
        """unittest for ImageDialog.set_ttext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_ttext(chgtext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for ImageDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestVideoDialog:
    """unittest for dialogs_qt.VideoDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.VideoDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called VideoDialog.__init__ with args', args)
        monkeypatch.setattr(testee.VideoDialog, '__init__', mock_init)
        testobj = testee.VideoDialog()
        assert capsys.readouterr().out == 'called VideoDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for VideoDialog.__init__
        """
        testobj = testee.VideoDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_kies(self, monkeypatch, capsys):
        """unittest for VideoDialog.kies
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.kies() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_text(self, monkeypatch, capsys):
        """unittest for VideoDialog.on_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_text(number=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for VideoDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestAudioDialog:
    """unittest for dialogs_qt.AudioDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.AudioDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called AudioDialog.__init__ with args', args)
        monkeypatch.setattr(testee.AudioDialog, '__init__', mock_init)
        testobj = testee.AudioDialog()
        assert capsys.readouterr().out == 'called AudioDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for AudioDialog.__init__
        """
        testobj = testee.AudioDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_kies(self, monkeypatch, capsys):
        """unittest for AudioDialog.kies
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.kies() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for AudioDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestListDialog:
    """unittest for dialogs_qt.ListDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ListDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ListDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ListDialog, '__init__', mock_init)
        testobj = testee.ListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ListDialog.__init__
        """
        testobj = testee.ListDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_on_type(self, monkeypatch, capsys):
        """unittest for ListDialog.on_type
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_type() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_rows(self, monkeypatch, capsys):
        """unittest for ListDialog.on_rows
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_rows() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for ListDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestTableDialog:
    """unittest for dialogs_qt.TableDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.TableDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TableDialog.__init__ with args', args)
        monkeypatch.setattr(testee.TableDialog, '__init__', mock_init)
        testobj = testee.TableDialog()
        assert capsys.readouterr().out == 'called TableDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for TableDialog.__init__
        """
        testobj = testee.TableDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_on_rows(self, monkeypatch, capsys):
        """unittest for TableDialog.on_rows
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_rows() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_cols(self, monkeypatch, capsys):
        """unittest for TableDialog.on_cols
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_cols() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_check(self, monkeypatch, capsys):
        """unittest for TableDialog.on_check
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_check(number=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_title(self, monkeypatch, capsys):
        """unittest for TableDialog.on_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_title(col) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for TableDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestScrolledTextDialog:
    """unittest for dialogs_qt.ScrolledTextDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ScrolledTextDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ScrolledTextDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ScrolledTextDialog, '__init__', mock_init)
        testobj = testee.ScrolledTextDialog()
        assert capsys.readouterr().out == 'called ScrolledTextDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialog.__init__
        """
        testobj = testee.ScrolledTextDialog(parent, title='', data='', htmlfile='', fromdisk=False,
        assert capsys.readouterr().out == ("")

    def _test_show_source(self, monkeypatch, capsys):
        """unittest for ScrolledTextDialog.show_source
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_source() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestCodeViewDialog:
    """unittest for dialogs_qt.CodeViewDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.CodeViewDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CodeViewDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CodeViewDialog, '__init__', mock_init)
        testobj = testee.CodeViewDialog()
        assert capsys.readouterr().out == 'called CodeViewDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CodeViewDialog.__init__
        """
        testobj = testee.CodeViewDialog(parent, title='', caption='', data='', size=(600, 400))
        assert capsys.readouterr().out == ("")

    def _test_setup_text(self, monkeypatch, capsys):
        """unittest for CodeViewDialog.setup_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_text() == "expected_result"
        assert capsys.readouterr().out == ("")
