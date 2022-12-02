"""simple program to show html page without opening a web browser - PyQt5 version
"""
import sys
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import PyQt5.QtWebEngineWidgets as webeng


class HtmlView(qtw.QMainWindow):
    """Show HTML from various sources
    """
    def __init__(self):
        super().__init__()
        self.resize(1020, 900)
        self.html = webeng.QWebEngineView(self)
        self.setCentralWidget(self.html)

    def keyPressEvent(self, event):
        """event handler voor toetsaanslagen
        """
        if event.key() == core.Qt.Key_Escape:
            self.close()

    def show_html(self, data):
        """start viewer with source
        """
        self.html.setHtml(data)

    def show_html_from_path(self, pathname):
        """start viewer with filename
        """
        with open(pathname, encoding="utf-8") as _in:
            html = _in.read()
        self.setWindowTitle("View HTML: {}".format(pathname))
        self.html.setHtml(html)

    def show_html_from_url(self, url):
        """start viewer with URL
        """
        self.html.load(url)


def main(path):
    "main function"
    app = qtw.QApplication(sys.argv)
    frm = HtmlView()
    frm.show_html_from_path(path)
    frm.show()
    sys.exit(app.exec_())
