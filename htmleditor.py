import sys
## from ashe_ppg import MainGui
## from ashe_tk import MainGui - NB werkt niet op deze manier
from ashe_wx import MainGui

def main(args):
    x = MainGui(args)

if __name__ == '__main__':
    main(sys.argv)
