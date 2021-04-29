from flask import Blueprint

bp = Blueprint('qux', __name__, url_prefix='/qux')


@bp.route('/foo')
def foo():
    return 'qux.foo response'


@bp.route('/bar')
def bar():
    return 'qux.bar response'
