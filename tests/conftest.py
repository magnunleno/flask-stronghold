#!/usr/bin/env python
# encoding: utf-8


import pytest

from tests.app import create_app


@pytest.fixture(scope='function')
def app(request):
    flask_app = create_app()
    ctx = flask_app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return flask_app


@pytest.fixture(scope='function')
def stronghold(app):
    from flask_stronghold import Stronghold
    stronghold = Stronghold()
    stronghold.init_app(app)
    return stronghold


@pytest.fixture(scope='function')
def stronghold_with_user_callback(stronghold):
    @stronghold.user_callback
    def get_user_fixture(request):
        api_key = request.headers.get('Authorization')
        if api_key is None:
            return None
        return int(api_key)
    return stronghold
