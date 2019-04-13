from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField
from wtforms.validators import  DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User
class LoginForm(Form):
    email=StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()])
    password=PasswordField('密码',validators=[DataRequired()])
    remember_me=BooleanField('保持登录状态')
    submit=SubmitField('登录')
class RegistrationForm(Form):
    email=StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()])
    username=StringField('用户名',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                                                   'Usernames must have only letters,'
                                                                                   'numbers,dots or underscores')])
    password=PasswordField('密码',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')])
    password2=PasswordField('再次确认密码',validators=[DataRequired()])
    role = SelectField('用户角色', validators=[DataRequired()],
                         choices=[('Customer', '客户'), ('Employee', '普通员工'), ('Administrator', '管理员')])
    submit=SubmitField('注册')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise  ValidationError('邮箱已被注册！')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册！')