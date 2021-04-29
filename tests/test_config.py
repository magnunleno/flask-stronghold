#!/usr/bin/env python
# encoding: utf-8

import re
import pytest


@pytest.mark.options(STRONGHOLD_PUBLIC_BLUEPRINTS=['foo', 'bar'])
def test_blueprint_config_loading(stronghold, client):
    assert stronghold._blueprints == ['foo', 'bar']


@pytest.mark.options(STRONGHOLD_PUBLIC_BLUEPRINTS=['foo', 123])
def test_blueprint_config_loading_ignore_non_string(stronghold, client):
    assert stronghold._blueprints == ['foo']


@pytest.mark.options(STRONGHOLD_PUBLIC_ENDPOINTS=['foo.bar', 'foo.baz'])
def test_endpoint_config_loading(stronghold, client):
    assert stronghold._endpoints == ['foo.bar', 'foo.baz']


@pytest.mark.options(STRONGHOLD_PUBLIC_ENDPOINTS=['foo.bar', 123])
def test_endpoint_config_loading_ignore_non_string(stronghold, client):
    assert stronghold._endpoints == ['foo.bar']


@pytest.mark.options(STRONGHOLD_PUBLIC_RULES=['^foo\\..*', '.*\\.public'])
def test_rule_config_loading(stronghold, client):
    assert stronghold._rules == [
        re.compile('^foo\\..*'), re.compile('.*\\.public')
    ]


@pytest.mark.options(STRONGHOLD_PUBLIC_RULES=['.*\\.public', 123])
def test_rule_config_loading_ignore_non_string(stronghold, client):
    assert stronghold._rules == [re.compile('.*\\.public')]


@pytest.mark.options(
    STRONGHOLD_PUBLIC_RULES=['.*\\.public'],
    STRONGHOLD_PUBLIC_ENDPOINTS=['foo.bar'],
    STRONGHOLD_PUBLIC_BLUEPRINTS=['baz'],
)
def test_endpoint_blueprint_and_rule_config_loading(stronghold, client):
    assert stronghold._rules == [re.compile('.*\\.public')]
    assert stronghold._endpoints == ['foo.bar']
    assert stronghold._blueprints == ['baz']
