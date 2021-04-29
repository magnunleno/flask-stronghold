#!/usr/bin/env python
# encoding: utf-8

import pytest

from flask import url_for


RULES_CONFIG = ['^home$', '^about$', '^.*\\.foo$']
PUBLIC_ENDPOINT_VIEWS = ['home', 'about', 'baz.foo', 'qux.foo']
PRIVATE_ENDPOINT_VIEWS = ['manage', 'baz.bar', 'qux.bar']
ALL_ENDPOINT_VIEWS = PUBLIC_ENDPOINT_VIEWS + PRIVATE_ENDPOINT_VIEWS


@pytest.mark.options(STRONGHOLD_PUBLIC_RULES=RULES_CONFIG)
@pytest.mark.parametrize('view_name', PUBLIC_ENDPOINT_VIEWS)
def test_configured_rules_are_visible(stronghold, client, view_name):
    resp = client.get(url_for(view_name))
    assert resp.status_code == 200
    assert resp.get_data().decode() == f'{view_name} response'


@pytest.mark.options(STRONGHOLD_PUBLIC_RULES=RULES_CONFIG)
@pytest.mark.parametrize('view_name', PRIVATE_ENDPOINT_VIEWS)
def test_configured_rules_are_not_visible(stronghold, client, view_name):
    resp = client.get(url_for(view_name))
    assert resp.status_code == 401
    assert resp.get_data().decode() != f'{view_name} response'


@pytest.mark.options(STRONGHOLD_PUBLIC_RULES=RULES_CONFIG)
@pytest.mark.parametrize('view_name', ALL_ENDPOINT_VIEWS)
def test_configured_rules_are_visible_for_logged_user(
    stronghold_with_user_callback, client, view_name,
):
    resp = client.get(url_for(view_name), headers={"Authorization": "123"})
    assert resp.status_code == 200
    assert resp.get_data().decode() == f'{view_name} response'
