#!/usr/bin/env python
# encoding: utf-8

import pytest

from flask import url_for


VIEWS = [
    'home', 'about', 'manage', 'baz.foo', 'baz.bar', 'qux.foo', 'qux.bar',
]


def test_flas_app_in_testing_mode(app):
    assert app.config.get('TESTING') is True


@pytest.mark.parametrize('view_name', VIEWS)
def test_app_public_views(client, view_name):
    resp = client.get(url_for(view_name))
    assert resp.status_code == 200
    assert resp.get_data().decode() == f'{view_name} response'
