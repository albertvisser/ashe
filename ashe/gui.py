"""importeer de gui classes vanuit een bepaalde toolkit-specifieke module
"""
from .toolkit import toolkit
if toolkit == 'qt':
    import ashe.qtgui as gui
elif toolkit == 'wx':
    import ashe.wxgui as gui
else:
    raise ImportError('onbekende GUI toolkit')
