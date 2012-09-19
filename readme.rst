Albert's Simple HTML Editor (ASHE)
==================================

I'm not sure what came first, the discovery a tree widget for Tkinter
or the nice idea to write a tree-based xml-editor to use on my PDA,
but since wxPython for PocketPyCE 2.5 ate up most of my memory I had to build one
using Tk, with the added bonus that I could use it on the PC as well.
So I wrote one that more or less worked, and lost interest.

Along came PocketPyGui. After some playing with it I felt ready to tackle the
(sparsely documented) tree widget and so I turned my Tkinter code into Ppygui code,
slowly falling more in love with this toolkit.

But somehow I couldn't run it on Windows anymore (except when using an emulator,
but I wanted a real Windows app) so i decided to build a wxPython version as well.

Along the way I decided to go for a html editor based on the same code,
and try a hand at building a way to turn various programs for various gui toolkits
into one program "plugging in" the gui code depending on the toolkit available.

Requirements
............

- Python
- BeautifulSoup
- wxPython for the current GUI version
- Tkinter and Gene Cash's Tree module for an older GUI version
- PocketPyGUI for a PocketPC version
