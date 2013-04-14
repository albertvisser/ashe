Files in this directory
=======================

/:

htmleditor.py
    starter for the files in the package "ashe"
    (currently working with the wxPython version)

ashe/:

__init__.py
    (empty) package indicator
ashe_mixin.py
    GUI independent code
    imports shutil, BeautifulSoup and others
ashe_ppg.py
    GUI code, PocketPyGUI version
    imports ppygui, BeautifulSoup, ashe_mixin
ashe_qt.py
    GUI code, PyQt4 version
    imports QTGui, QTCore, QTWebkit, BeautifulSoup, ashe_mixin
ashe_tk.py
    GUI code, Tkinter version
    uses Gene Cash's Tree control for Tkinter
    imports Tkinter, Tree, mytkSimpleDialog, BeautifulSoup
    (not up-to-date with the others)
ashe_wx.py
    GUI code, wxPython version
    imports wx, wx.grid, wx.html, BeautifulSoup, ashe_mixin

ashe.ico
    my own application icon
how_it_works.txt
    description of methods used in the various modules (needs updating)

