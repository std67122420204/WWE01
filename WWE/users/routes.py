from flask import Blueprint, render_template, request, flash, redirect, url_for
from WWE.extensions import db
from WWE.models import WWE, Type, User
from flask_login import login_required, current_user

wwe_bp = Blueprint('wwe', __name__, template_folder='templates')


@wwe_bp.route('/')
@login_required
def index():
    
    query = db.select(WWE).where(WWE.user_id == current_user.id)
    wwes = db.session.scalars(query).all()
    return render_template('wwe/index.html', 
                           title='WWE Page',
                           wwes=wwes)


@wwe_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_wwe():
    
    types = db.session.scalars(db.select(Type)).all()

    if request.method == 'POST':
        name = request.form.get('name')
        height = request.form.get('height')
        weight = request.form.get('weight')
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        user_id = current_user.id
        type_ids = request.form.getlist('wwe_types')

       
        selected_types = [db.session.get(Type, int(id)) for id in type_ids]

        
        existing_wwe = db.session.scalar(db.select(WWE).where(WWE.name == name))
        if existing_wwe:
            flash(f'WWE: {name} already exists!', 'warning')
            return redirect(url_for('wwe.new_wwe'))

       
        new_wwe = WWE( name=name,
                       height=height,
                       weight=weight,
                       description=description,
                       img_url=img_url,
                       user_id=user_id,
                       types=selected_types)
        db.session.add(new_wwe)
        db.session.commit()
        flash('Add new WWE successful!', 'success')
        return redirect(url_for('wwe.index'))

    return render_template('wwe/new_wwe.html', 
                           title='New WWE Page',
                           types=types)