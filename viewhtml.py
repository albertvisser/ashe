#! /usr/bin/env python3
usage = """\
usage: python(3) viewhtml.py <filename>             view HTML file on filesystem
"""
import sys
## from ashe.viewhtml_qt4 import main
from ashe.viewhtml_qt import main

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1]:
        print(usage)
    else:
        main(sys.argv[1])
