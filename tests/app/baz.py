from flask import Blueprint

bp = Blueprint('baz', __name__, url_prefix='/baz')


@bp.route('/foo')
def foo():
    return 'baz.foo response'


@bp.route('/bar')
def bar():
    return 'baz.bar response'
