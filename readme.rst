Albert's Simple HTML Editor (ASHE)
==================================

I'm not sure what came first, the discovery a tree widget for Tkinter
or the nice idea to write a tree-based xml-editor to use on my PDA,
but since wxPython for PocketPyCE 2.5 ate up most of my memory I had to build one
using Tk, with the added bonus that I could use it on the PC as well.
So I wrote one that more or less worked, and lost interest.

Along came PocketPyGui. After some playing with it I felt ready to tackle the
(sparsely documented) tree widget and so I turned my Tkinter code into PPygui code,
slowly falling more in love with this toolkit.

But somehow I couldn't run the Tkinter version on Windows anymore (maybe because I
reinstalled without the tree widget). Of course I could run it using an emulator,
but I wanted a real Windows app so i decided to build a wxPython version as well.

Along the way I decided to go for a HTML editor based on the same code,
and try a hand at building a way to turn various programs for various gui toolkits
into one program "plugging in" the gui code depending on the toolkit available -
or in this case having gui-dependent versions importing the gui-independent common
stuff because that seemed a bit less contrived at the time.

The HTML editor contains some HTML-specific functions like adding a dtd, link, image, list or
table, and presents a non-css preview alongside the tree.
In the HTML menu there are also options for validating the html, and viewing the code in
pretty-printed format.

Requirements
............

- Python
- BeautifulSoup
- wxPython for the current GUI version
- Tkinter and Gene Cash's Tree module for an older GUI version
- PocketPyGUI for a PocketPC version
