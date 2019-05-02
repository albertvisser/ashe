"""simple program to show html page without opening a web browser - wxPhoenix version
"""
import os
import wx
import wx.html2 as wxhtml


class HtmlView(wx.Frame):
    """Show HTML from various sources
    """
    def __init__(self):
        super().__init__(parent=None, size=(1020, 900))
        self.html = wxhtml.WebView.New(self)
        # dit werkt niet
        # self.Bind(wx.EVT_KEY_UP, self.on_key)
        # en dit werkt ook niet
        # menuitem = wx.MenuItem(None, text='exit')
        # accel=wx.AcceleratorEntry(cmd=menuitem.GetId())
        # if accel.FromString('Escape'):
        #     self.SetAcceleratorTable(wx.AcceleratorTable([accel]))

    def on_key(self, event):
        """event handler voor toetsaanslagen
        """
        print('in on_key')
        if event.GetKeyCode() == wx.WXK_ESCAPE:  # of event.getUnicodeKey()
            self.close()

    def show_html(self, data):
        """start viewer with source
        """
        self.html.SetPage(data)

    def show_html_from_path(self, pathname):
        """start viewer with filename
        """
        fullpath = os.path.abspath(pathname)
        self.SetTitle("View HTML: {}".format(fullpath))
        self.html.LoadURL('file://' + fullpath)

    def show_html_from_url(self, url):
        """start viewer with URL
        """
        self.html.LoadURL(url)


def main(path):
    "main function"
    app = wx.App()
    frm = HtmlView()
    frm.show_html_from_path(path)
    frm.Show(True)
    app.MainLoop()
