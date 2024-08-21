# This Python file uses encoding: utf-8

from PyQt5.QtWidgets import QWidget


def find_child(ancestor, _type, name) -> QWidget:
    """
    Find a widget by searching for name amongst the descendant of ancestor

    Parameters
    ----------
    - ancestor: widget to amongst whose descendants we are searching
    - _type: type of the widget for which we are searching, e.g. QPushButton
    - name: name of the ancestor

    Returns
    -------
    QWidget

    Exceptions: raises exception when the widget is not found
    """
    child = ancestor.findChild(_type, name)

    if child is None:
        raise Exception(f'Could not find widget with name {name} of type {_type.__name__}')

    return child
