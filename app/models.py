from . import db
from . import  login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import  UserMixin,AnonymousUserMixin
from datetime import datetime
import hashlib
from flask import request
class Permission:
    AI_Recommend=0x01
    GasData_Analysis=0x02
    GasData_Management=0x04
    Moderate_EmployeeInfo=0x08
    Administrator=0x80
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    permissions=db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>'%self.name
    @staticmethod
    def insert_roles():
        roles = {
            'Customer': Permission.AI_Recommend,
            'Employee': Permission.GasData_Analysis |
                          Permission.GasData_Management,
            'Administrator': 0xff
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()
class User(UserMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    email=db.Column(db.String(64), unique=True, index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash=db.Column(db.String(128))
    name=db.Column(db.String(64))
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
    imagefiles= db.relationship('ImageFile', backref='user', lazy='dynamic', cascade="all, delete-orphan",
                    passive_deletes=True)
    portraits = db.relationship('Portrait', backref='user', lazy='dynamic', cascade="all, delete-orphan",
                    passive_deletes=True)
    def __repr__(self):
        return '<User %r>' % self.username
    def can(self,permissions):
        return self.role is not None and \
               (self.role.permissions&permissions)==permissions
    def is_administrator(self):
        return self.can(Permission.Administrator)
    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)
    @property
    def password(self):
        raise ArithmeticError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    def is_administrator(self):
        return False
login_manager.anonymous_user=AnonymousUser
class ImageFile(db.Model):
    __tablename__='imagefiles'
    id=db.Column(db.Integer,primary_key=True)
    image_name=db.Column(db.String(30),index=True)
    image=db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'))
    portraits = db.relationship('Portrait', backref='imagefile', lazy='dynamic', cascade="all, delete-orphan",
                                passive_deletes=True)
class Portrait(db.Model):
    __tablename__='portraits'
    p_id=db.Column(db.Integer,db.ForeignKey('imagefiles.id',ondelete='CASCADE'),primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
    image_name = db.Column(db.String(30), index=True)
    image = db.Column(db.LargeBinary)
class Customer(db.Model):
    __tablename__='customers'
    id=db.Column(db.Integer,primary_key=True)
    year_avg_use=db.Column(db.Integer)
    high_usage_rate=db.Column(db.DECIMAL(5,3))
    capacity=db.Column(db.DECIMAL(5,3))
    replace_thing=db.Column(db.Integer)
    grow_rate=db.Column(db.DECIMAL(5,3))
class Gasconsumption(db.Model):
    __tablename__='gasconsumption'
    id = db.Column(db.Integer, primary_key=True)
    sales_well = db.Column(db.Integer)
    gas_sales=db.Column(db.DECIMAL(5,1))
    district_GDP=db.Column(db.DECIMAL(5,1))
    population=db.Column(db.Integer)
    month_avg_income=db.Column(db.DECIMAL(6,1))
    gas_price=db.Column(db.DECIMAL(5,2))
    liquid_price=db.Column(db.DECIMAL(5,2))
class GasconsumptionTest(db.Model):
    __tablename__='gasconsumptiontest'
    id = db.Column(db.Integer, primary_key=True)
    gas_sales=db.Column(db.DECIMAL(5,1))
    district_GDP=db.Column(db.DECIMAL(5,1))
    population=db.Column(db.Integer)
    month_avg_income=db.Column(db.DECIMAL(6,1))
    gas_price=db.Column(db.DECIMAL(5,2))
    liquid_price=db.Column(db.DECIMAL(5,2))
class ConsumptionUseCase(db.Model):
    __tablename__='consumptionusecase'
    id=db.Column(db.Integer,primary_key=True)
    month_avg_use=db.Column(db.Integer)
    family_numbers=db.Column(db.Integer)
    month_avg_income=db.Column(db.Integer)
    place=db.Column(db.String(30), index=True)
class GasPredictionSale(db.Model):
    __tablename__ ='gaspredictionsale'
    id = db.Column(db.Integer, primary_key=True)
    gas_sales = db.Column(db.Integer)
    sales_well=db.Column(db.Integer)

