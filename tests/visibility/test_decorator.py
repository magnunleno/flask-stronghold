#!/usr/bin/env python
# encoding: utf-8

from flask import url_for

from flask_stronghold import stronghold_exempt


def test_custom_view_is_not_visible(stronghold, client):
    @stronghold.app.route('/custom_view')
    def custom_view():
        return 'custom view response'

    resp = client.get(url_for('custom_view'))
    assert resp.status_code == 401


def test_custom_view_is_now_exempt(stronghold, client):
    @stronghold_exempt
    @stronghold.app.route('/custom_view')
    def custom_view():
        return 'custom_view response'

    resp = client.get(url_for('custom_view'))
    assert resp.status_code == 200
    assert resp.get_data().decode() == 'custom_view response'
