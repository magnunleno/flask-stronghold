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

from typing import Union, TYPE_CHECKING

from flask import request, abort
from flask.wrappers import Request

from flask_stronghold.utils import is_view_func_public

if TYPE_CHECKING:
    from flask_stronghold import Stronghold


class StrongholdRequestHandler(object):
    def __init__(self, stronghold: 'Stronghold'):
        '''
        Initialized the StrongholdRequestHandler storing the reference to
        the Stronghold instance.
        '''
        self.stronghold = stronghold

    def match_public_rule(self, endpoint: str) -> bool:
        '''
        Checks if any stronghold regex rules match the given endpoint name.
        '''
        for rule in self.stronghold._rules:
            if rule.match(endpoint):
                return True
        return False

    def handle_request(self) -> Union[None, object, str]:
        '''
        Handles the current request and deals with Stronghold public setting
        and order of precedence:
         - Is view authentication exempt?
         - Is blueprint registered as public?
         - Is endpoint registered as public?
         - Is there any regex rule that matches the endpoint name?

         If none of the above answers as true, the handler calls the
         Stronghold._user_callback to determine if we have an authenticated
         user or not.
        '''
        view = self.stronghold.app.view_functions[request.endpoint]

        if is_view_func_public(view):
            return

        if request.blueprint in self.stronghold._blueprints:
            return

        if request.endpoint in self.stronghold._endpoints:
            return

        if self.match_public_rule(request.endpoint):
            return

        user = self.stronghold._get_user_callback(request) \
            if self.stronghold._get_user_callback \
            else None

        if not user:
            return self.stronghold._unauthorized_handler(request)


def default_unauthorized_handler(request: Request) -> None:
    '''Dummy unauthorized handler that raises an 401 error.'''
    abort(401)
