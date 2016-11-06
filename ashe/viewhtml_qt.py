import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import PyQt5.QtWebKitWidgets as webkit

class HtmlView(qtw.QMainWindow):

    def __init__(self, parent=None):

        super().__init__()
        self.resize(1020, 900)
        self.html = webkit.QWebView(self)
        self.setCentralWidget(self.html)

    def keyPressEvent(self, event):
        """event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key_Escape:
            self.close()

    def show_html(self, data):

        self.html.setHtml(data)

    def show_html_from_path(self, pathname):

        with open(pathname, encoding="utf-8") as _in:
            html = _in.read()
        self.setWindowTitle("View HTML: {}".format(pathname))
        self.html.setHtml(html)

    def show_html_from_url(self, url):

        self.html.load(url)


def main(path):
    app = qtw.QApplication(sys.argv)
    frm = HtmlView()
    frm.show_html_from_path(path)
    frm.show()
    sys.exit(app.exec_())


