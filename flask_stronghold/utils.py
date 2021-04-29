#!/usr/bin/env python
# encoding: utf-8
#
# Flask-Stronghold
# -----------
# A simple Flask extension that makes all of your app's routes require login
# by default.
#
# :copyright: (c) 2021 by Magnun Leno.
# :license: MIT/X11, see LICENSE for more details.

from typing import Callable


def is_view_func_public(view: Callable) -> bool:
    '''
    Returns whether or not the given Flask view has the
    _IS_STRONGHOLD_EXEMPT flag.
    '''
    return getattr(view, "_IS_STRONGHOLD_EXEMPT", False)


def set_view_func_public(view: Callable) -> None:
    '''Set the _IS_STRONGHOLD_EXEMPT flag in a given Flask view.'''
    setattr(view, "_IS_STRONGHOLD_EXEMPT", True)
