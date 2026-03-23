from flask import Blueprint, render_template, request, flash, redirect, url_for
from WWE.extensions import db
from WWE.models import WWE, Type
from flask_login import login_required, current_user
from sqlalchemy import func

wwe_bp = Blueprint('wwe', __name__, template_folder='templates')

def parse_float(value, default=0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


@wwe_bp.route('/')
@login_required
def index():
    wwes = db.session.scalars(
        db.select(WWE).where(WWE.user_id == current_user.id)
    ).all()
    return render_template('wwe/index.html',
                           title='WWE Page',
                           wwes=wwes)


@wwe_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_wwe():
    wwe_types = db.session.scalars(db.select(Type)).all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        height = parse_float(request.form.get('height'))
        weight = parse_float(request.form.get('weight'))
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        type_ids = request.form.getlist('wwe_types')

        
        selected_types = [db.session.get(Type, int(id_str)) for id_str in type_ids if db.session.get(Type, int(id_str))]

        
        existing_wwe = db.session.scalar(
            db.select(WWE).where(func.lower(WWE.name) == name.lower())
        )
        if existing_wwe:
            flash(f'WWE Superstar "{name}" already exists!', 'warning')
            return redirect(url_for('wwe.new_wwe'))

       
        new_wwe = WWE(
            name=name,
            height=height,
            weight=weight,
            description=description,
            img_url=img_url,
            user_id=current_user.id,
            categories=selected_types
        )
        db.session.add(new_wwe)
        db.session.commit()

        flash('Add new WWE Superstar successful!', 'success')
        return redirect(url_for('wwe.index'))

    return render_template('wwe/new_superstars.html',
                           title='Add New Superstar',
                           wwe_types=wwe_types)

@wwe_bp.route("/wwe/<int:wwe_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_wwe(wwe_id):
    wwe_item = db.get_or_404(WWE, wwe_id)
    form = WWE.Form() 

    if form.validate_on_submit():
        wwe_item.name = form.name.data
        wwe_item.height = form.height.data
        wwe_item.weight = form.weight.data
        wwe_item.description = form.description.data
        
        wwe_item.types = form.types.data 
        
        db.session.commit()
        flash('อัปเดตข้อมูล Superstar เรียบร้อยแล้ว!', 'success')
        return redirect(url_for('wwe.wwe_detail', wwe_id=wwe_item.id))
    
    elif request.method == 'GET':
        
        form.name.data = wwe_item.name
        form.height.data = wwe_item.height
        form.weight.data = wwe_item.weight
        form.description.data = wwe_item.description
        form.types.data = wwe_item.types

    return render_template('add_wwe.html', title='Edit Superstar', form=form, legend='Edit Superstar')