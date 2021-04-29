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

from flask_stronghold.utils import set_view_func_public


def stronghold_exempt(view: Callable) -> Callable:
    '''
    Decorator that sets a view to be treated as 'authentication exempt'.
    '''
    set_view_func_public(view)
    return view
