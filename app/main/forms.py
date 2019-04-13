from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField,ValidationError,FileField
from wtforms.validators import  DataRequired,Length,Email,Regexp
from ..models import User,Role
class upForm(Form):
    name = StringField('照片名称')
    file = FileField('照片')
    submit = SubmitField('提交')
class EditProfileForm(Form):
    name=StringField('真名',validators=[Length(0,64)])
    location=StringField('地址',validators=[Length(0,64)])
    about_me=TextAreaField('关于我')
    submit=SubmitField('上传')
class SearchForm(Form):
    search=StringField('',validators=[Length(0,64)])
    submit=SubmitField('搜索')
class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         'Usernames must have only letters,'
                                                                                         'numbers,dots or underscores')])
    role=SelectField('角色',coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')
    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name)for role in Role.query.order_by(Role.name).all()]
        self.user=user
    def validate_username(self,field):
        if field.data!=self.user.username and \
            User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用.')
    def validate_email(self,field):
        if field.data!=self.user.email and \
            User.query.filter_by(email=field.data).first():
            raise  ValidationError('邮箱已被注册.')
class KMeansForm(Form):
    KMeans=StringField('输入分类的类数',validators=[DataRequired(),Regexp('^[1-9][0-9]*$',0,'输入数字必须为大于0的整数')])
class LogicPredictionForm(Form):
    file = FileField('上传要预测的数据')
class Intel_consumptionForm(Form):
    family_numbers=StringField('家庭人数',validators=[DataRequired(),Regexp('^[1-9][0-9]*$',0,'输入数字必须为大于0的整数')])
    avg_month_income=StringField('个人平均工资',validators=[DataRequired(),Regexp('^[1-9][0-9]*$',0,'输入数字必须为大于0的整数')])
    submit = SubmitField('燃气用量推荐')
class Review_sentimentForm(Form):
    Review = StringField('输入一条评论', validators=[Length(0, 64)])
class GasProblemDistributionForm(Form):
    KMeans=StringField('输入分类的类数',validators=[DataRequired(),Regexp('^[1-9][0-9]*$',0,'输入数字必须为大于0的整数')])

