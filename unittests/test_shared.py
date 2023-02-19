import pytest
import ashe.shared as testee

def test_analyze_element(monkeypatch, capsys):
    assert testee.analyze_element('', {}) == ('', False, 'Add &inline style', '', False, False)
    assert testee.analyze_element('x', {'y': 'z'}) == ('x', False, 'Add &inline style', '', False,
                                                       False)
    assert testee.analyze_element('<> x', {}) == ('x', False, 'Add &inline style', '', False, False)
    assert testee.analyze_element('<!> <> x', {}) == ('x', True, 'Add &inline style', '', False,
                                                      False)
    assert testee.analyze_element('<!> x', {}) == ('x', True, 'Add &inline style', '', False, False)
    assert testee.analyze_element('link', {'rel': 'stylesheet'}) == ('link', False,
                                                                     '&Edit linked stylesheet',
                                                                     '', False, True)
    assert testee.analyze_element('x', {'style': 'y'}) == ('x', False, '&Edit inline style', 'y',
                                                          True, False)
    assert testee.analyze_element('style', {}) == ('style', False, '&Edit styles', '', False, False)
    assert testee.analyze_element('style', {'styledata': 'y'}) == ('style', False, '&Edit styles',
                                                                   'y', True, False)

def test_get_dtdmenu_texts(monkeypatch, capsys):
    # nog kijken hoe dit in de gui modules gebruikt moet worden om hardgecodeerde teksten te
    # vervangen
    assert testee.get_dtd_menu_texts(True) == ['Remove &DTD', 'Remove the Document Type Declaration']
    assert testee.get_dtd_menu_texts(False) == ['Add &DTD', 'Add the Document Type Declaration']
