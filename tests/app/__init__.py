#!/usr/bin/env python
# encoding: utf-8

from flask import Flask


def home():
    return 'home response'


def about():
    return 'about response'


def manage():
    return 'manage response'


def create_app():
    app = Flask(__name__)
    app.testing = True

    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/about', 'about', about)
    app.add_url_rule('/manage', 'manage', manage)

    from . import baz
    from . import qux
    app.register_blueprint(baz.bp)
    app.register_blueprint(qux.bp)

    return app
