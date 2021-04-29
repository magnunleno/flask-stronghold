#!/usr/bin/env python
# encoding: utf-8

from flask_stronghold import stronghold_exempt


def test_exempt_decorator_add_exempt_flag(stronghold):
    @stronghold_exempt
    def func():
        ...

    assert hasattr(func, '_IS_STRONGHOLD_EXEMPT') is True
    assert func._IS_STRONGHOLD_EXEMPT is True
