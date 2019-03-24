#! /usr/bin/env python3
"""Albert's simple HTML editor: tree-based with live preview
adapted for use of wxPhoenix so please DO NOT COMMIT
"""
import sys
## from ashe_ppg import MainGui
## from ashe_tk import MainGui - NB werkt niet op deze manier
from ashe.ashe_wx import ashe_gui
## from ashe.ashe_qt4 import ashe_gui
## from ashe.ashe_qt import ashe_gui


def main(args):
    "main function"
    ashe_gui(args)

if __name__ == '__main__':
    main(sys.argv)
