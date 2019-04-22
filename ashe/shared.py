"""Constants for HTML editor
"""
import pathlib

ICO = str(pathlib.Path(__file__).parent / "ashe.ico")
TITEL = "Albert's Simple HTML-editor"
CMSTART = "<!>"
ELSTART = '<>'
DTDSTART = "DOCTYPE"
IFSTART = '!IF'
BL = "&nbsp;"
VAL_MESSAGE = "\n".join(("Validation results are for the file on disk",
                         "some errors/warnings may already have been corrected by "
                         "BeautifulSoup",
                         "(you'll know when they don't show up in the tree or text view",
                         " or when you save the file in memory back to disk)"))
masks = {'all': ('All files', ('*.*',)),
         'html': ('HTML files', ('*.htm', '*.html')),
         'css': ('CSS files', ('*.css',)),
         'image': ('Image files', ('*.gif', '*.ico', '*.jpg', '*.jpeg', '*.png', '*.xpm', '*.svg')),
         'video': ('Video files', ('*.mp4', '*.avi', '*.mpeg')),
         'audio': ('Audio files', ('*.mp3', '*.wav', '*.ogg'))}


def analyze_element(tag, attrs):
    """setup text and such
    """
    old_styledata = ''
    is_stylesheet = has_style = iscomment = False
    if tag:
        x = tag.split(None, 1)
        if x[0] == CMSTART:
            iscomment = True
            x = x[1].split(None, 1)
        if x[0] == ELSTART:
            x = x[1].split(None, 1)
        tag = x[0]
    if attrs:
        for attr, value in attrs.items():
            if attr == 'styledata':
                old_styledata = value
                continue
            elif tag == 'link' and attr == 'rel' and value == 'stylesheet':
                is_stylesheet = True
            elif attr == 'style':
                has_style = True
                old_styledata = value
    if tag == 'style':  # is_style_tag:
        text = '&Edit styles'
    elif is_stylesheet:
        text = '&Edit linked stylesheet'
    elif has_style:
        text = '&Edit inline style'
    else:
        text = 'Add &inline style'
    return tag, iscomment, text, old_styledata, has_style, is_stylesheet
