"""redirect om import in hoofdprogramma gui-agnostic te maken
"""
from .viewhtml_toolkit import toolkit
if toolkit == 'qt':
    from .viewhtml_qt import main
elif toolkit == 'wx':
    from .viewhtml_wx import main
else:
    raise ValueError('Invalid name specified for GUI toolkit')
