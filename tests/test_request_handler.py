#!/usr/bin/env python
# encoding: utf-8

import pytest

from flask import url_for


VIEWS = ['home', 'about', 'manage']


@pytest.mark.parametrize('view_name', VIEWS)
def test_stronghold_handler_is_active_and_blocking(
    stronghold, client, mocker, view_name,
):
    spy = mocker.spy(stronghold._request_handler, 'handle_request')
    assert spy.call_count == 0

    resp = client.get(url_for(view_name))
    assert spy.call_count == 1
    assert resp.status_code == 401


@pytest.mark.parametrize('view_name', VIEWS)
def test_stronghold_handler_is_calling_get_user_callback_and_blocking(
    stronghold_with_user_callback, client, mocker, view_name
):
    spy = mocker.spy(stronghold_with_user_callback, '_get_user_callback')
    resp = client.get(url_for(view_name))
    assert resp.status_code == 401
    assert spy.call_count == 1


def test_stronghold_handler_allows_logged_user_requests(
    stronghold_with_user_callback, client,
):
    resp = client.get(url_for('home'), headers={"Authorization": "123"})
    assert resp.status_code == 200
    assert resp.get_data().decode() == 'home response'
