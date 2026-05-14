"""unittests for ./ashe/shared.py
"""
import ashe.shared as testee

def test_get_dtdmenu_texts():
    """unittest for shared.get_dtdmenu_texts
    """
    # nog kijken hoe dit in de gui modules gebruikt moet worden om hardgecodeerde teksten te
    # vervangen
    assert testee.get_dtd_menu_texts(True) == ['Remove &DTD', 'Remove the Document Type Declaration']
    assert testee.get_dtd_menu_texts(False) == ['Add &DTD', 'Add the Document Type Declaration']
