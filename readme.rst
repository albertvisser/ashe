Albert's Simple HTML Editor (ASHE)
==================================

This HTML editor is based on the premiss that editing a HTML document is better done
via the tree structure than via the text, on account of not having the tags cloud
the contents.

The editor also contains some HTML-specific functions like adding a dtd, link,
image, video or audio element, list or table,
and presents a simple preview alongside the tree.
In the HTML menu there are also options for validating the html,
and viewing the code in pretty-printed format.


Usage
-----

Basically you call ``htmleditor.py`` in the top directory.
You can provide a file name to indicate the file you'll be working with.

For ease of work, I've configured my file manager to be able to call the editor
on the file selected.


Requirements
............

- Python
- BeautifulSoup
- PyQt4 for the current GUI version
- wxPython for the previous GUI version (doesn't work with Python 3)
- Tkinter and Gene Cash's Tree module for an older GUI version
- PocketPyGUI for a PocketPC version
