#!/usr/bin/env python
# encoding: utf-8

from flask import url_for, redirect


VIEWS = ['home', 'about', 'manage']
CUSTOM_MESSAGE = "You're not authorized to view this page!"


def redirect_unauthorized_handler(request):
    return redirect(url_for('about'))


def html_page_unauthorized_handler(request):
    return CUSTOM_MESSAGE, 401


def test_stronghold_default_unauthorized_handler_initialized(
    stronghold, client
):
    handler = stronghold._unauthorized_handler
    assert handler is not None
    assert handler.__name__ == 'default_unauthorized_handler'


def test_stronghold_unauthorized_handler_is_called(
    stronghold, client, mocker,
):
    spy = mocker.spy(stronghold, '_unauthorized_handler')
    resp = client.get(url_for('home'))
    assert spy.call_count == 1
    assert resp.status_code == 401


def test_stronghold_unauthorized_handler_is_not_called(
    stronghold_with_user_callback, client, mocker,
):
    spy = mocker.spy(stronghold_with_user_callback, '_unauthorized_handler')
    resp = client.get(url_for('home'), headers={"Authorization": "123"})
    assert resp.status_code == 200
    assert spy.call_count == 0


def test_stronghold_custom_unauthorized_handler_is_set(stronghold, client):
    stronghold.unauthorized_handler(redirect_unauthorized_handler)
    assert stronghold._unauthorized_handler is not None
    assert stronghold._unauthorized_handler == redirect_unauthorized_handler


def test_stronghold_custom_unauthorized_handler_is_called(
    stronghold, client, mocker,
):
    mock = mocker.MagicMock(side_effect=redirect_unauthorized_handler)
    stronghold.unauthorized_handler(mock)
    resp = client.get(url_for('home'))
    assert mock.call_count == 1
    assert resp.status_code == 302
    assert resp.location == 'http://localhost/about'


def test_stronghold_html_page_response(stronghold, client, mocker):
    mock = mocker.MagicMock(side_effect=html_page_unauthorized_handler)
    stronghold.unauthorized_handler(mock)
    resp = client.get(url_for('home'))
    assert mock.call_count == 1
    assert resp.status_code == 401
    assert CUSTOM_MESSAGE == resp.get_data().decode()
