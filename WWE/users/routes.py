from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from WWE.models import User
from WWE.extensions import db, bcrypt
import os, secrets
from WWE.forms import UpdateAccountForm, LoginForm, RegisterForm

users_bp = Blueprint('users', __name__, template_folder='templates', static_folder='static')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = db.session.scalar(db.select(User).where(User.username == username))
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('core.index'))  
        else:
            flash('Login failed. Check username and password', 'danger')

    return render_template('users/login.html', title='Login Page', form=form)


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Register successful!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register Page', form=form)


def save_avatar(form_avatar):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_avatar.filename)
    avatar_fn = random_hex + ext
    avatar_path = os.path.join(users_bp.root_path, 'static/img', avatar_fn)
    img = Image.open(form_avatar)
    img.thumbnail((256, 256))
    img.save(avatar_path)
    return avatar_fn


@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fullname.data = getattr(current_user, 'fullname', '')
    elif form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_avatar(form.avatar.data)
            current_user.avatar = avatar_file
        current_user.fullname = form.fullname.data
        db.session.commit()
        flash('Update profile successful!', 'success')
        return redirect(url_for('users.profile'))

    return render_template('users/profile.html', title='Profile Page', form=form, avatar_pic=current_user.avatar)


@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_pw = request.form.get('old_password')
        new_pw = request.form.get('new_password')
        if bcrypt.check_password_hash(current_user.password, old_pw):
            current_user.password = bcrypt.generate_password_hash(new_pw).decode('utf-8')
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Old password is incorrect', 'danger')

    return render_template('users/change_password.html', title='Change Password')