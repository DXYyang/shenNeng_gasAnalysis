from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user
from . import  auth
from ..models import User,Role
from .forms import  LoginForm,RegistrationForm
from .. import db
@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return  redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码无效！')
    return render_template('auth/login.html',form=form)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经登出.')
    return redirect(url_for('main.index'))
@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        role=Role.query.filter_by(name=form.role.data).first()
        user=User(email=form.email.data,
                  username=form.username.data,
                  password=form.password.data,
                  role=role)
        db.session.add(user)
        flash('你现在可以登录了.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

