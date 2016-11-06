usage = """\
usage: python(3) viewhtml.py <filename>             view HTML file on filesystem
"""
## from ashe.viewhtml_qt import main
from ashe.viewhtml_qt5 import main

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1]:
        print(usage)
    else:
        main(sys.argv[1])
