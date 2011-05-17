import sys
## from ashe_ppg import MainGui
## from ashe_tk import MainGui - NB werkt niet op deze manier
from ashe.ashe_wx import main_gui

def main(args):
    x = main_gui(args)

if __name__ == '__main__':
    main(sys.argv)
