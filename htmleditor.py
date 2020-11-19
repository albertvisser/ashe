#! /usr/bin/env python3
"""Albert's simple HTML editor: tree-based with live preview
new and improved version
"""
import sys
from ashe.base import Editor


def main(args):
    "main function"
    Editor(args)


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else ''
    main(arg)
