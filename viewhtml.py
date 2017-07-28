#! /usr/bin/env python3
"""View HTML file on filesystem

usage: python(3) viewhtml.py <filename>
"""
import sys
## from ashe.viewhtml_qt4 import main
from ashe.viewhtml_qt import main

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1]:
        print(__doc__)
    else:
        main(sys.argv[1])
