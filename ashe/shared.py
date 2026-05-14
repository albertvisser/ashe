"""Constants for HTML editor
"""
import pathlib

ICO = str(pathlib.Path(__file__).parent / "ashe.ico")
TITEL = "Albert's Simple HTML-editor"
CMSTART = "<!>"
ELSTART = '<>'
DTDSTART = "DOCTYPE"
# IFSTART = '!IF'     # IE support misschien kan dit een keer echt weg
BL = "&nbsp;"
VAL_MESSAGE = ("Validation results are for the file on disk\n"
               "some errors/warnings may already have been corrected by BeautifulSoup\n"
               "(you'll know when they don't show up in the tree or text view\n"
               " or when you save the file in memory back to disk)")
masks = {'all': ('All files', ('*.*',)),
         'html': ('HTML files', ('*.htm', '*.html')),
         'css': ('CSS files', ('*.css',)),
         'image': ('Image files', ('*.gif', '*.ico', '*.jpg', '*.jpeg', '*.png', '*.xpm', '*.svg')),
         'video': ('Video files', ('*.mp4', '*.avi', '*.mpeg')),
         'audio': ('Audio files', ('*.mp3', '*.wav', '*.ogg'))}


def get_dtd_menu_texts(has_dtd):
    """determine text to update dtd menu with
    """
    # how to use in gui.<xx>.py:
    #    def adjust_dtd_nemu(self):
    #        label, helpstr = shared.get_dtd_menu_texts(self.dtdmenu.has_dtd)
    textdict = {'label': '{} &DTD', 'help': '{} the Document Type Declaration'}
    replacements = {True: 'Remove', False: 'Add'}
    return [textdict[key].format(replacements[has_dtd]) for key in ('label', 'help')]
