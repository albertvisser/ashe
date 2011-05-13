Files in this directory
=======================

/:

htmleditor.py
    starter for the files in the package "ashe"
    (only ppg and wx work though)

ashe/:

__init__.py
    (empty) package indicator
ashe_mixin.py
    GUI independent code
    imports BeautifulSoup
ashe_ppg.py
    GUI code, PocketPyGUI version
    imports shutil, copy, ppygui, BeautifulSoup, ashe_mixin
ashe_tk.py
    GUI code, Tkinter version
    uses Gene Cash's Tree control for Tkinter
    imports Tkinter, Tree, mytkSimpleDialog, BeautifulSoup
    (not up-to-date with the others)
ashe_wx.py
    GUI code, wxPython version
    imports shutil, copy, wx, wx.grid, BeautifulSoup, ashe_mixin

ashe.ico
    my own application icon
how_it_works.txt
    description of methods used in the various modules

extra files not in distribution/source control:
-----------------------------------------------

history.txt
    description of how this stuff came to be
mytkSimpleDialog.py
    tkSimpleDialog with some cosmetic changes that couldn't be passed
    normally
    intended to be placed in lib/site-packages