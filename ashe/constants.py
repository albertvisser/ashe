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
masks = {'all': ('All files', ('*.*',)),
         'html': ('HTML files', ('*.htm', '*.html')),
         'css': ('CSS files', ('*.css',)),
         'image': ('Image files', ('*.gif', '*.ico', '*.jpg', '*.jpeg', '*.png', '*.xpm', '*.svg')),
         'video': ('Video files', ('*.mp4', '*.avi', '*.mpeg')),
         'audio': ('Audio files', ('*.mp3', '*.wav', '*.ogg'))}
