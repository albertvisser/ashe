Albert's Simple HTML Editor (ASHE)
==================================

This HTML editor is based on the premisse that editing a HTML document is better done
via the tree structure than via the text, on account of not having the tags cloud
the contents.

The editor also contains some HTML-specific functions like adding a dtd, link,
image, video or audio element, list or table,
and presents a simple preview alongside the tree.
In the HTML menu there are options for adding specific constructs, validating the html,
and viewing the code in pretty-printed format.


Usage
-----

Basically you call ``htmleditor.py`` in the top directory.
You can provide a file name to indicate the file you'll be working with.

For ease of work, I've configured my file manager to be able to call the editor
on the file selected.

Also included is a simple HTML previewer that can be started by calling ``viewhtml.py`` in the top directory

Requirements
............

- Python
- BeautifulSoup (and lxml)
- PyQt(5, including QtWebEngine) or wxPython (4, including wxhtml2)
