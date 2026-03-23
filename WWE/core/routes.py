from flask import Blueprint, render_template, request
from WWE.extensions import db
from WWE.models import WWE, Type

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    wwes = db.paginate(
        db.select(WWE),
        per_page=4,
        page=page )

    return render_template(
        'core/index.html',
        title='Home Page',
        wwes=wwes )

@core_bp.route('/<int:id>/detail')
def detail(id):
    wwe = db.session.get(WWE, id)

    return render_template(
        'core/wwe_detail.html',
        title='WWE Detail Page',
        wwe=wwe )