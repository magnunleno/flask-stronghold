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


import warnings

from flask import current_app
from typing import TYPE_CHECKING, Callable

from flask_stronghold import handlers, config

if TYPE_CHECKING:
    from wsgiref.types import WSGIApplication


class Stronghold(object):
    '''
    This is the main class, it's responsible for loading settings, adding
    handlers and callbacks.
    '''
    def __init__(self, app: 'WSGIApplication' = None):
        '''Stronghold class initializer.'''
        self.app = None

        self._get_user_callback = None
        self._unauthorized_handler = None

        self._rules = []
        self._endpoints = []
        self._blueprints = []

        if app is not None:  # pragma: no cover
            self.init_app(app)

    def setup_app(self, app: 'WSGIApplication') -> None:  # pragma: no cover
        '''
        This method has been deprecated. Please use Stronghold.init_app
        instead.
        '''
        warnings.warn(
            'Warning setup_app is deprecated. Please use init_app.',
            DeprecationWarning,
        )
        self.init_app(app)

    def init_app(self, app: 'WSGIApplication') -> None:
        '''
        Here the extension is initialized and registered in the 'extensions'
        dictionary in the current Flask app instance.
        '''
        self.app = app

        if not hasattr(self.app, 'extensions'):  # pragma: no cover
            self.app.extensions = {}

        self.app.extensions['stronghold'] = self

        self._load_settings()
        self._register_handlers()

    def _load_settings(self) -> None:
        '''
        Query and set all Flask-Stronghold settings.

        This method should not be called anywhere else other then
        Stronghold.init_app.
        '''
        self._rules = config.get_public_rules(current_app)
        self._endpoints = config.get_public_endpoints(current_app)
        self._blueprints = config.get_public_blueprints(current_app)

    def _register_handlers(self) -> None:
        '''
        Register StrongholdRequestHandler in them current Flask app and the
        default unauthorized handler, if no other was provided before.

        This method should not be called anywhere else other then
        Stronghold.init_app.
        '''
        self._request_handler = handlers.StrongholdRequestHandler(self)
        self.app.before_request(lambda: self._request_handler.handle_request())

        if self._unauthorized_handler is None:  # pragma: no cover
            self.unauthorized_handler(handlers.default_unauthorized_handler)

    def user_callback(self, callback: Callable) -> None:
        '''
        Defines the user callback used by Flask-Stronghold to determine if
        a user is authenticated or not.
        '''
        self._get_user_callback = callback

    def unauthorized_handler(self, callback: Callable) -> None:
        '''
        Defines the unauthorized handler used by Flask-Stronghold when a view
        is access by an unauthenticated user.
        '''
        self._unauthorized_handler = callback
