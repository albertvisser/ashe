"""importeer de gui classes vanuit een bepaalde toolkit-specifieke module
"""
from .toolkit import toolkit
if toolkit == 'qt':
    import ashe.gui_qt as gui
elif toolkit == 'wx':
    import ashe.gui_wx as gui

