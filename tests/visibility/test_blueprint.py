#!/usr/bin/env python
# encoding: utf-8

import pytest

from flask import url_for


BLUEPRINT_CONFIG = ['baz']
PUBLIC_BLUEPRINT_VIEWS = ['baz.foo', 'baz.bar']
PRIVATE_BLUEPRINT_VIEWS = ['home', 'about', 'manage', 'qux.foo', 'qux.bar']
ALL_BLUEPRINT_VIEWS = PUBLIC_BLUEPRINT_VIEWS + PRIVATE_BLUEPRINT_VIEWS


@pytest.mark.options(STRONGHOLD_PUBLIC_BLUEPRINTS=BLUEPRINT_CONFIG)
@pytest.mark.parametrize('view_name', PUBLIC_BLUEPRINT_VIEWS)
def test_configured_blueprints_are_visible(stronghold, client, view_name):
    resp = client.get(url_for(view_name))
    assert resp.status_code == 200
    assert resp.get_data().decode() == f'{view_name} response'


@pytest.mark.options(STRONGHOLD_PUBLIC_BLUEPRINTS=BLUEPRINT_CONFIG)
@pytest.mark.parametrize('view_name', PRIVATE_BLUEPRINT_VIEWS)
def test_configured_blueprints_are_not_visible(stronghold, client, view_name):
    resp = client.get(url_for(view_name))
    assert resp.status_code == 401
    assert resp.get_data().decode() != f'{view_name} response'


@pytest.mark.options(STRONGHOLD_PUBLIC_BLUEPRINTS=BLUEPRINT_CONFIG)
@pytest.mark.parametrize('view_name', ALL_BLUEPRINT_VIEWS)
def test_configured_blueprints_are_visible_for_logged_user(
    stronghold_with_user_callback, client, view_name,
):
    resp = client.get(url_for(view_name), headers={"Authorization": "123"})
    assert resp.status_code == 200
    assert resp.get_data().decode() == f'{view_name} response'
