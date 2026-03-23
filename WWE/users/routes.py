from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from WWE.models import User
from WWE.extensions import db, bcrypt
import os, secrets
from WWE.form import UpdateAccountForm, LoginForm, RegisterForm

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/')
@login_required
def index():
  return render_template('users/index.html', title='User Page')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    query = db.select(User).where(User.username==username)
    user = db.session.scalar(query)
    if user:
      flash('Username is already exists!', 'warning')
      return redirect(url_for('users.register'))
    else:
      query = db.select(User).where(User.email==email)
      user = db.session.scalar(query)
      if user:
        flash('Email is already exists!', 'warning')
        return redirect(url_for('users.register'))
      else:
        if password == confirm_password:
          pwd_hash = bcrypt.generate_password_hash(password=password).decode('utf-8')
          user = User(username=username, email=email, password=pwd_hash)
          db.session.add(user)
          db.session.commit()
          flash('Register successful!', 'success')
          return redirect(url_for('users.login'))
        else:
          flash('Your password not match!', 'warning')
          return redirect(url_for('users.register'))
  return render_template('users/register.html', title='Register Page')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.username == form.username.data)
        )

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('core.index'))
        else:
            flash('Login failed. Check username and password', 'danger')

    return render_template('users/login.html', title='Login Page', form=form)

@users_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('core.index'))

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  user = current_user
  if request.method == 'POST':
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    if len(firstname)>0 and len(lastname)>0:
      user.firstname = firstname
      user.lastname = lastname
      db.session.add(user)
      db.session.commit()
      flash('Update profile successful!', 'success')
      return redirect(url_for('users.profile'))
    
  return render_template('users/profile.html', 
                         title='Profile Page',
                         user=user)

@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  if request.method == 'POST':
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')

    user = current_user

    if not bcrypt.check_password_hash(user.password, old_password):
      flash('Old password is not correct!', 'warning')
      return redirect(url_for('users.change_password'))
    
    if new_password != confirm_new_password:
      flash('New password and confirm password do not match!', 'warning')
      return redirect(url_for('users.change_password'))
    
    pwd_hash = bcrypt.generate_password_hash(password=new_password).decode('utf-8')
    user.password = pwd_hash
    db.session.add(user)
    db.session.commit()
    
    flash('Change password successful!', 'success')
    return redirect(url_for('users.profile'))

  return render_template('users/change_password.html', title='Change Password Page')