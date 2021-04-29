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

import re

from typing import List, Pattern, TYPE_CHECKING

if TYPE_CHECKING:
    from wsgiref.types import WSGIApplication

DEFAULTS = {
    'STRONGHOLD_PUBLIC_RULES': [],
    'STRONGHOLD_PUBLIC_ENDPOINTS': [],
    'STRONGHOLD_PUBLIC_BLUEPRINTS': [],
}


def get_public_rules(app: 'WSGIApplication') -> List[Pattern]:
    '''
    Query the config key STRONGHOLD_PUBLIC_RULES in the Flask app and return
    a list of compiled regex pattern.
    '''
    CONFIG_KEY = 'STRONGHOLD_PUBLIC_RULES'
    opts = app.config.get(CONFIG_KEY, DEFAULTS[CONFIG_KEY].copy())
    return [
        re.compile(pattern) for pattern in opts if isinstance(pattern, str)
    ]


def get_public_blueprints(app: 'WSGIApplication') -> List[str]:
    '''
    Query the config key STRONGHOLD_PUBLIC_BLUEPRINTS in the Flask app and
    return a list of strings containing then 'public' blueprint names.
    '''
    CONFIG_KEY = 'STRONGHOLD_PUBLIC_BLUEPRINTS'
    opts = app.config.get(CONFIG_KEY, DEFAULTS[CONFIG_KEY].copy())
    return [name for name in opts if isinstance(name, str)]


def get_public_endpoints(app: 'WSGIApplication') -> List[str]:
    '''
    Query the config key STRONGHOLD_PUBLIC_ENDPOINTS in the Flask app and
    return a list of strings containing then 'public' endpoint names.
    '''
    CONFIG_KEY = 'STRONGHOLD_PUBLIC_ENDPOINTS'
    opts = app.config.get(CONFIG_KEY, DEFAULTS[CONFIG_KEY].copy())
    return [name for name in opts if isinstance(name, str)]
