from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user
from . import  auth
from ..models import User,Role
from .forms import  LoginForm,RegistrationForm
from .. import db
from ..email import send_email
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
        db.session.commit()#提交数据库后才能赋予新用户id值，而确认令牌需要用到id，所以不能延后提交
        token=user.generate_confirmation_token()
        send_email(user.email,'Confirm Your Account','auth/email/confirm',
                   user=user,token=token)
        flash('一份确认邮件已经发送到你的邮箱，请查收！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('你已经确认了你的账号。谢谢！')
    else:
        flash('确认邮件已经无效或过期')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

