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


__version__ = '0.1.0'


from .core import Stronghold
from .decorators import stronghold_exempt

__all__ = ['Stronghold', 'stronghold_exempt']
