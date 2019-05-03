"""wxPython versie van mijn op een treeview gebaseerde HTML-editor

custom dialogen
"""
import os
## import sys
import string
# import pathlib
import wx
import wx.grid as wxgrid
# import wx.html as html
# from wx.lib.dialogs import ScrolledMessageDialog
import wx.stc as wxstc
from ashe.shared import CMSTART, VAL_MESSAGE, analyze_element


class ElementDialog(wx.Dialog):
    """dialoog om (de attributen van) een element op te voeren of te wijzigen
    tevens kan worden aangegeven of het element "op commentaar gezet" moet zijn"""

    def __init__(self, parent, title='', tag='', attrs=None):
        self._parent = parent
        super().__init__(parent, -1, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        tagdata = analyze_element(tag, attrs)
        tag_text, iscomment, style_text, styledata, self.has_style, is_stylesheet = tagdata
        self.is_style_tag = tag_text == 'style'
        if self.is_style_tag or self.has_style:
            self._parent.editor.cssm.setup_flags(styledata, is_stylesheet)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label="element name:")
        self.tag_text = wx.TextCtrl(self, size=(150, -1))
        self.comment_button = wx.CheckBox(self, label='&Comment(ed)')
        self.is_stylesheet = False
        self.styledata = ''
        self.tag_text.SetValue(tag_text)
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
        width = self.attr_table.GetSize().GetWidth() - 162
        self.attr_table.SetColSize(1, width)  # 178) # 160)   ## FIXME: werkt dit?
        if attrs:
            for attr, value in attrs.items():
                self.attr_table.AppendRows(1)
                idx = self.attr_table.GetNumberRows() - 1
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
        self.style_button = wx.Button(self, label=style_text)
        if self._parent.editor.cssedit_available:
            self.style_button.Bind(wx.EVT_BUTTON, self.on_style)
        else:
            self.style_button.Disable(True)
        hbox.Add(self.add_button, 0, wx.EXPAND | wx.ALL, 1)
        hbox.Add(self.delete_button, 0, wx.EXPAND | wx.ALL, 1)
        hbox.Add(self.style_button, 0, wx.EXPAND | wx.ALL, 1)
        sbox.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        vbox.Add(sbox, 1, wx.ALL | wx.EXPAND, 5)

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
        tag = self.tag_text.GetValue()
        for row in range(self.attr_table.GetNumberRows()):
            if self.attr_table.GetCellValue(row, 0) == 'href':
                fname = self.attr_table.GetCellValue(row, 1)
        self._parent.editor.cssm.call_csseditor(tag, fname)

    def on_ok(self):
        "doorgeven in dialoog gewijzigde waarden aan hoofdscherm"
        # TODO: ensure no duplicate items are added
        tag = self.tag_text.GetValue()
        test = string.ascii_letters + string.digits
        for letter in tag:
            if letter not in test:
                wx.MessageBox('Illegal character(s) in tag name',
                              'Add an item', wx.ICON_ERROR)
                return False, ()
        commented = self.comment_button.GetValue()
        attrs = {}
        for i in range(self.attr_table.GetNumberRows()):
            try:
                name = self.attr_table.GetCellValue(i, 0)
                value = self.attr_table.GetCellValue(i, 1)
            except AttributeError:
                wx.MessageBox('Press enter on this item first',
                              'Add an item', wx.ICON_ERROR)
                return False, ()
            if name != 'style':
                attrs[name] = value
        if self.is_style_tag or self.has_style:
            self.styledata, attrs = self._parent.editor.cssm.check_if_modified(tag, attrs)
        return True, (tag, attrs, commented)


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
                self.comment_button.SetValue(True)
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
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
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
        commented = self.comment_button.IsChecked()
        tag = self.data_text.GetValue()
        return True, (tag, commented)


class SearchDialog(wx.Dialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title=""):
        self._parent = parent
        super().__init__(parent, title=title)
        sizer = wx.BoxSizer(wx.VERTICAL)

        gsizer = wx.GridBagSizer(4, 4)
        self.cb_element = wx.StaticText(self, label='Element')
        gsizer.Add(self.cb_element, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_element = wx.StaticText(self, label="name: ")
        hsizer.Add(lbl_element, flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_element = wx.TextCtrl(self, size=(120, -1))
        self.txt_element.Bind(wx.EVT_TEXT, self.set_search)
        hsizer.Add(self.txt_element)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (0, 1))

        self.cb_attr = wx.StaticText(self, label='Attribute ')
        gsizer.Add(self.cb_attr, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_attr_name = wx.StaticText(self, label="name: ")
        hsizer.Add(lbl_attr_name, flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_attr_name = wx.TextCtrl(self, size=(120, -1))
        self.txt_attr_name.Bind(wx.EVT_TEXT, self.set_search)
        hsizer.Add(self.txt_attr_name)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (1, 1))

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_attr_val = wx.StaticText(self, label="value: ")
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer.Add(lbl_attr_val, flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_attr_val = wx.TextCtrl(self, size=(120, -1))
        self.txt_attr_val.Bind(wx.EVT_TEXT, self.set_search)
        hsizer.Add(self.txt_attr_val)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (2, 1))

        self.cb_text = wx.StaticText(self, label='Text')
        gsizer.Add(self.cb_text, (3, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_text = wx.StaticText(self, label="value: ")
        hsizer.Add(lbl_text, flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_text = wx.TextCtrl(self, size=(120, -1))
        self.txt_text.Bind(wx.EVT_TEXT, self.set_search)
        hsizer.Add(self.txt_text)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (3, 1))

        sizer.Add(gsizer, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.LEFT | wx.RIGHT, 8)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_search = wx.StaticText(self, label='')
        hsizer.Add(self.lbl_search)
        sizer.Add(hsizer, 0, wx.LEFT | wx.RIGHT, 8)

        # hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.ok_button = wx.Button(self, id=wx.ID_OK)
        # # self.SetAffirmativeId(wx.ID_OK)
        # # self.SetAffirmativeId(self.ok_button.GetId())
        # self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        # hsizer.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        # hsizer.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        # sizer.Add(hsizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
        #           wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)
        # buttons = self.CreateButtonSizer(wx.APPLY | wx.CLOSE)
        # self.SetAffirmativeId(wx.ID_APPLY)
        # self.SetEscapeId(wx.ID_CLOSE)
        buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(buttons)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        # sizer.SetSizeHints(self)
        self.Layout()

        if self._parent.search_args:
            self.txt_element.SetValue(self._parent.search_args[0])
            self.txt_attr_name.SetValue(self._parent.search_args[1])
            self.txt_attr_val.SetValue(self._parent.search_args[2])
            self.txt_text.SetValue(self._parent.search_args[3])

    def set_search(self, event):
        """build text describing search action"""
        out = self._parent.editor.build_search_spec(self.txt_element.GetValue(),
                                                    self.txt_attr_name.GetValue(),
                                                    self.txt_attr_val.GetValue(),
                                                    self.txt_text.GetValue(),
                                                    '')
        self.lbl_search.SetLabel(out)
        self.search_specs = out
        self.Fit()

    def on_ok(self):
        """confirm dialog and pass changed data to parent"""
        ele = str(self.txt_element.GetValue())
        attr_name = str(self.txt_attr_name.GetValue())
        attr_val = str(self.txt_attr_val.GetValue())
        text = str(self.txt_text.GetValue())
        if not any((ele, attr_name, attr_val, text)):
            self._parent.meld('Please enter search criteria or press cancel')
            self.resend = True
            return False, ()
        return True, ((ele, attr_name, attr_val, text), self.search_specs)


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
            if idx == 4:
                radio.SetValue(True)
            vbox2.Add(radio, 0, wx.ALL, 2)
            self.dtd_list.append((x[0], x[1], radio))
        hbox.Add(vbox2)
        sbox.Add(hbox, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(sbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_OK)
        # self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        # self.SetAffirmativeId(wx.ID_SAVE)
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

    def on_ok(self):
        """pass changed data to parent
        """
        for caption, dtd, radio in self.dtd_list:
            if radio and radio.GetValue():
                return True, dtd
        return False, None


class CssDialog(wx.Dialog):
    """dialoog om een stylesheet toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        self.styledata = ''
        super().__init__(parent, title='Add Stylesheet')
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)
        lbl = wx.StaticText(self, label="link to stylesheet:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self, size=(250, -1), value="http://")
        gbox.Add(self.link_text, (0, 1))

        self.choose_button = wx.Button(self, label='&Browse')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (1, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText(self, label="for media type(s):")
        gbox.Add(lbl, (2, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.text_text = wx.TextCtrl(self)
        gbox.Add(self.text_text, (2, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
        self.inline_button = wx.Button(self, label='&Add inline')
        self.inline_button.Bind(wx.EVT_BUTTON, self.on_inline)
        self.cancel_button = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)
        hbox.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.inline_button, 0, wx.EXPAND | wx.ALL, 2)
        hbox.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(hbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM |
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 15)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.link_text.SetFocus()

    def kies(self, evt):
        "methode om het te linken document te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        with wx.FileDialog(self, message="Choose a file", defaultDir=loc,
                           wildcard=self._parent.build_mask('css'), style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.link_text.SetValue(dlg.GetPath())

    def on_inline(self, event=None):
        "voegt een 'style' tag in"
        self._parent.dialog_data = self._parent.editor.cssm.call_from_inline(self._parent,
                                                                             self.text_text.GetValue())

    def on_ok(self):
        """bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad
        maar eerst kijken of dit geen inline stylesheet betreft """
        # TODO: wat als er zowel styledata als een linkadres is?
        if self.styledata:
            return True, {"cssdata": self.styledata.decode()}
        link = str(self.link_text.GetValue())
        if link in ('', 'http://'):
            self._parent.meld("bestandsnaam opgeven of inline stylesheet definiëren s.v.p")
            return False, {}
        try:
            link = self._parent.editor.convert_link(link, self._parent.editor.xmlfn)
        except ValueError as msg:
            self._parent.meld(msg)
            return False, {}
        dialog_data = {"rel": 'stylesheet', "href": link, "type": 'text/css'}
        test = self.text_text.GetValue()
        if test:
            dialog_data["media"] = test
        return True, dialog_data


class LinkDialog(wx.Dialog):
    """dialoog om een link element toe te voegen
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent, title='Add Link')
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)
        lbl = wx.StaticText(self, label="descriptive title:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
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

    def kies(self, evt):
        "methode om het te linken document te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        with wx.FileDialog(self, message="Choose a file", defaultDir=loc,
                           wildcard=self._parent.build_mask('html'), style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.link_text.SetValue(dlg.GetPath())

    def set_text(self, evt):
        'indien leeg title tekst gelijk maken aan link adres'
        if evt.EventObject == self.link_text:
            linktxt = self.link_text.GetValue()
            if self.text_text.GetValue() == self.linktxt:
                self.text_text.SetValue(linktxt)
                self.linktxt = linktxt
        elif self.text_text.GetValue() == "":
            self.linktxt = ""

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        txt = str(self.text_text.GetValue())
        if not txt:
            self.parent.meld("link opgeven of cancel kiezen s.v.p")
            return False, {}
        try:
            link = self._parent.editor.convert_link(self.link_text.GetValue(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            self.parent.meld(msg)
            return False, ()
        return True, (txt, {"href": link, "title": self.title_text.GetValue()})


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
        # self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
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

    def kies(self, evt):
        "methode om het te linken image te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        # mask = '*.gif *.jpg *.png'
        # if os.name == "posix":
        #     mask += ' ' + mask.upper()
        # mask = "Image files ({});;{}".format(mask, IMASK)
        with wx.FileDialog(self, message="Choose a file", defaultDir=loc,
                           wildcard=self._parent.build_mask('image'), style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.link_text.SetValue(dlg.GetPath())

    def set_text(self, evt):
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
            link = self._parent.editor.convert_link(self.link_text.GetValue(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            self._parent.meld(msg)
            return False, {}
        return True, {"src": link, "alt": str(self.alt_text.GetValue()),
                      "title": str(self.title_text.GetValue())}


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

        lbl = wx.StaticText(self, label="link to video:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self, size=(250, -1), value="http://")
        # self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (0, 1))

        self.choose_button = wx.Button(self, label='Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (1, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        lbl = wx.StaticText(self, label="height of video window:")
        gbox.Add(lbl, (2, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.hig_text = wx.SpinCtrl(self)  # .pnl, -1, size = (40, -1))
        self.hig_text.SetMax(maxheight)
        self.hig_text.SetValue(initialheight)
        self.hig_text.Bind(wx.EVT_SPINCTRL, self.on_text)
        gbox.Add(self.hig_text, (2, 1))

        lbl = wx.StaticText(self, label="width of video window:")
        gbox.Add(lbl, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.wid_text = wx.SpinCtrl(self)  # .pnl, -1, size = (40, -1))
        self.wid_text.SetMax(maxwidth)
        self.wid_text.SetValue(initialwidth)
        self.wid_text.Bind(wx.EVT_SPINCTRL, self.on_text)
        gbox.Add(self.wid_text, (3, 1))

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
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
        self.link_text.SetFocus()

    def kies(self, evt):
        "methode om het te linken element te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        with wx.FileDialog(self, message="Choose a file", defaultDir=loc,
                           wildcard=self._parent.build_mask('video'), style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.link_text.SetValue(dlg.GetPath())

    def on_text(self, evt):  # number=None):
        "controle bij invullen/aanpassen hoogte/breedte"
        try:
            # int(number)  # self.rows_text.value())
            _ = int(evt.EventObject.GetValue())
        except ValueError:
            self._parent.meld('Number must be numeric integer')
            return

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.convert_link(self.link_text.GetValue(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            self._parent.meld(msg)
            return False, {}
        return True, {"src": link,
                      "height": str(self.hig_text.GetValue()),
                      "width": str(self.wid_text.GetValue())}


class AudioDialog(wx.Dialog):
    'dialoog om een audio element toe te voegen'

    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent, title='Add Audio')
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self, -1)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        gbox = wx.GridBagSizer(4, 4)

        lbl = wx.StaticText(self, label="link to audio fragment:")
        gbox.Add(lbl, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        self.link_text = wx.TextCtrl(self, size=(250, -1), value="http://")
        # self.link_text.Bind(wx.EVT_TEXT, self.set_text)
        self.linktxt = ""
        gbox.Add(self.link_text, (0, 1))

        self.choose_button = wx.Button(self, label='Search')
        self.choose_button.Bind(wx.EVT_BUTTON, self.kies)
        gbox.Add(self.choose_button, (1, 0), (1, 2), wx.ALIGN_CENTER_HORIZONTAL)

        sbox.Add(gbox, 0, wx.ALL, 10)
        vbox.Add(sbox, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, id=wx.ID_SAVE)
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
        self.link_text.SetFocus()

    def kies(self, evt):
        "methode om het te linken element te selecteren"
        loc = self._parent.editor.xmlfn or os.getcwd()
        with wx.FileDialog(self, message="Choose a file", defaultDir=loc,
                           wildcard=self._parent.build_mask('audio'), style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.link_text.SetValue(dlg.GetPath())

    def on_ok(self):
        "bij OK: het geselecteerde (absolute) pad omzetten in een relatief pad"
        try:
            link = self._parent.editor.convert_link(self.link_text.GetValue(),
                                                    self._parent.editor.xmlfn)
        except ValueError as msg:
            self._parent.meld(msg)
            return False, {}
        return True, {"src": link}


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

        box = wx.StaticBox(self)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)

        tbox = wx.FlexGridSizer(2, 2, 2, 2)
        lbl = wx.StaticText(self, label="choose type of list:")

        self.type_select = wx.ComboBox(self, style=wx.CB_DROPDOWN,
                                       choices=["unordered", "ordered", "definition"])
        self.type_select.SetStringSelection("unordered")
        self.type_select.Bind(wx.EVT_COMBOBOX, self.on_type)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.type_select)

        lbl = wx.StaticText(self, label="initial number of items:")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.rows_text = wx.SpinCtrl(self)
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_rows)
        self.rows_text.Bind(wx.EVT_TEXT, self.on_rows)
        self.rows_text.SetValue(initialrows)
        tbox.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        tbox.Add(self.rows_text)  # hbox)
        sbox.Add(tbox, 0, wx.ALL, 5)

        self.list_table = wxgrid.Grid(self, size=(340, 120))
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
            self._parent.meld('Number must be numeric integer')
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
        list_type = str(self.type_select.GetStringSelection()[0]) + "l"
        list_data = []
        for row in range(self.list_table.GetNumberRows()):
            # try:
            list_item = [self.list_table.GetCellValue(row, 0)]
            # except AttributeError:
            #     self._parent.meld('Graag nog even het laatste item bevestigen (...)')
            #     return False, ()
            if list_type == "dl":
                # try:
                list_item.append(self.list_table.GetCellValue(row, 1))
                # except AttributeError:
                #     self._parent.meld('Graag nog even het laatste item bevestigen (...)')
                #     return False, ()
            list_data.append(list_item)
        return True, (list_type, list_data)


class TableDialog(wx.Dialog):
    "dialoog om een tabel toe te voegen"

    def __init__(self, parent):
        self._parent = parent
        self.headings = []
        initialcols, initialrows = 1, 1
        super().__init__(parent, title='Add a table',
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        vbox = wx.BoxSizer(wx.VERTICAL)

        box = wx.StaticBox(self)
        sbox = wx.StaticBoxSizer(box, wx.VERTICAL)
        tbox = wx.FlexGridSizer(3, 2, 2, 2)

        lbl = wx.StaticText(self, label="summary (description):")
        tbox.Add(lbl)
        self.title_text = wx.TextCtrl(self, size=(250, -1))
        tbox.Add(self.title_text, wx.ALIGN_CENTER_VERTICAL)

        # self.rows_text.setValue(initialrows)
        lbl = wx.StaticText(self, label="initial number of rows:")
        self.rows_text = wx.SpinCtrl(self)
        self.rows_text.Bind(wx.EVT_SPINCTRL, self.on_rows)
        self.rows_text.Bind(wx.EVT_TEXT, self.on_rows)
        self.rows_text.SetValue(initialrows)
        tbox.Add(lbl)
        tbox.Add(self.rows_text, wx.ALIGN_CENTER_VERTICAL)

        # self.cols_text.setValue(initialcols)
        lbl = wx.StaticText(self, label="initial number of columns:")
        self.cols_text = wx.SpinCtrl(self)
        self.cols_text.Bind(wx.EVT_SPINCTRL, self.on_cols)
        self.cols_text.Bind(wx.EVT_TEXT, self.on_cols)
        self.cols_text.SetValue(initialcols)
        tbox.Add(lbl)
        tbox.Add(self.cols_text, wx.ALIGN_CENTER_VERTICAL)
        sbox.Add(tbox, 0, wx.ALL, 5)

        self.show_titles = wx.CheckBox(self, label='Show Titles')
        self.show_titles.SetValue(True)
        self.show_titles.Bind(wx.EVT_CHECKBOX, self.on_check)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.show_titles)
        sbox.Add(hbox, 0, wx.ALL, 5)

        # self.table_table.setRowCount(initialrows)     # de eerste rij is voor de kolomtitels
        # self.table_table.setColumnCount(initialcols)  # de eerste rij is voor de rijtitels
        # self.table_table.setHorizontalHeaderLabels(self.headings)
        # self.hdr = self.table_table.horizontalHeader()
        # self.table_table.verticalHeader().setVisible(False)
        # self.hdr.setSectionsClickable(True)
        # self.hdr.sectionBind(wx.EVT_BUTTON, self.on_title)
        self.table_table = wxgrid.Grid(self, -1, size=(340, 120))
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
            self.parent.meld('Number must be numeric integer')
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
            self.parent.meld('Number must be numeric integer')
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
                                self._parent.editor.title) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.table_table.SetColLabelValue(col, dlg.GetValue())

    def on_ok(self):
        """bij OK: de opgebouwde tabel via self.dialog_data doorgeven
        aan het mainwindow
        """
        rows = self.table_table.GetNumberRows()
        cols = self.table_table.GetNumberCols()
        summary = str(self.title_text.GetValue())
        for col in range(cols):
            self.headings.append(self.table_table.GetColLabelValue(col))
        items = []
        for row in range(rows):
            rowitems = []
            for col in range(cols):
                # try:
                rowitems.append(self.table_table.GetCellValue(row, col))
                # except AttributeError:
                #     self._parent.meld('Graag nog even het laatste item bevestigen (...)')
                #     return False, ()
            items.append(rowitems)
        return True, (summary, self.show_titles.GetValue(), self.headings, items)


class ScrolledTextDialog(wx.Dialog):
    """dialoog voor het tonen van validatieoutput

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title='', data='', htmlfile='', fromdisk=False, size=(600, 400)):
        # self._parent = parent
        self.htmlfile = htmlfile
        super().__init__(parent, title=title, size=size)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.message = wx.StaticText(self)
        if fromdisk:
            self.message.SetLabel(VAL_MESSAGE)
        hbox.Add(self.message)
        vbox.Add(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY, size=size)
        hbox.Add(text)
        vbox.Add(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, label='&Done')
        # ok_button.Bind(wx.EVT_BUTTON, self.Destroy)
        self.SetAffirmativeId(ok_button.GetId())
        if htmlfile:
            show_button = wx.Button(self, label='&View submitted source')
            show_button.Bind(wx.EVT_BUTTON, self.show_source)
        hbox.Add(ok_button)
        if htmlfile:
            hbox.Add(show_button)
        vbox.Add(hbox)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        if htmlfile:
            data = parent.editor.do_validate(htmlfile)
        if data:
            text.SetValue(data)

    def show_source(self, event):
        "start viewing html source"
        with open(self.htmlfile) as f_in:
            data = ''.join([x for x in f_in])
        if data:
            dlg = CodeViewDialog(self, "Submitted source", data=data)
            dlg.ShowModal()


class CodeViewDialog(wx.Dialog):
    """dialoog voor het tonen van de broncode

    aanroepen met show() om openhouden tijdens aanpassen mogelijk te maken
    """
    def __init__(self, parent, title='', caption='', data='', size=(600, 400)):
        "create a window with a scintilla text widget and an ok button"
        self._parent = parent
        super().__init__(parent, title=title, size=size)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label=caption))
        vbox.Add(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wxstc.StyledTextCtrl(self, size=size)
        # self.setup_text()
        self.text.SetText(data)
        self.text.SetReadOnly(True)
        hbox.Add(self.text)
        vbox.Add(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, label='&Done')
        self.SetAffirmativeId(ok_button.GetId())
        hbox.Add(ok_button)
        vbox.Add(hbox)

        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()

    def setup_text(self):
        "define the scintilla widget's properties"
        # # Set the default font
        # font = gui.QFont()
        # font.setFamily('Courier')
        # font.setFixedPitch(True)
        # font.setPointSize(10)
        # self.text.setFont(font)
        # self.text.setMarginsFont(font)

        # # Margin 0 is used for line numbers
        # fontmetrics = gui.QFontMetrics(font)
        # self.text.setMarginsFont(font)
        # self.text.setMarginWidth(0, fontmetrics.width("00000"))
        # self.text.setMarginLineNumbers(0, True)
        # self.text.setMarginsBackgroundColor(gui.QColor("#cccccc"))

        # # Enable brace matching, auto-indent, code-folding
        # self.text.setBraceMatching(sci.QsciScintilla.SloppyBraceMatch)
        # self.text.setAutoIndent(True)
        # self.text.setFolding(sci.QsciScintilla.PlainFoldStyle)

        # # Current line visible with special background color
        # self.text.setCaretLineVisible(True)
        # self.text.setCaretLineBackgroundColor(gui.QColor("#ffe4e4"))

        # # Set HTML lexer
        # lexer = sci.QsciLexerHTML()
        # lexer.setDefaultFont(font)
        # self.text.setLexer(lexer)
