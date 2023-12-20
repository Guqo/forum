from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship, declarative_base, create_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
from flask_appbuilder.security.sqla.models import User

import logging

from app import app

mysql_connection_string = 'mysql://admin:AdminadminAdmin@localhost/sys'
# engine = create_engine(mysql_connection_string, echo=True)
# Base = declarative_base()

# Session = sessionmaker(bind=engine)
# session = Session()
db = SQLAlchemy(app)
# app['SQLALCHEMY_DATABASE_URI'] = mysql_connection_string


class Skupiny(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def repr(self):
        return self.name

skupiny_data = ['Superuzivatel', 'Moderator', 'Uzivatel']


def load_skupiny():
    for skupiny_name in skupiny_data:
        skupiny = Skupiny(name=skupiny_name)
        #db.session.add(skupiny)
    #db.session.commit()

load_skupiny()

# class MyUser(User):
#     __tablename__ = 'my_user'
#     id = Column(Integer, ForeignKey('ab_user.id'), primary_key=True)
#     uzivatel = relationship('Uzivatel', back_populates='my_user')
#     uzivatel = relationship('Uzivatel', primaryjoin='MyUser.id == Uzivatel.id')


class Uzivatel(db.Model):
    __tablename__ = 'uzivatel'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    skupiny_id = Column(Integer, ForeignKey('skupiny.id'))
    skupiny = relationship('Skupiny')
    # my_user = relationship('MyUser')

# MyUser.uzivatel = relationship('Uzivatel', back_populates='my_user')
# Uzivatel.my_user = relationship('MyUser', back_populates='uzivatel')

# class MyUser(User):
#     __tablename__ = 'my_user'
#     id = Column(Integer, primary_key=True)
#     uzivatel = relationship('Uzivatel')

# class Uzivatel(db.Model):
#     __tablename__ = 'uzivatel'
#     id = Column(Integer, primary_key=True)
#     my_user_id = Column(Integer, ForeignKey('my_user.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def repr(self):
        return self.name

categories_data = ['Maths', 'History', 'English']

def load_categories():
    for name in categories_data:
        category = Category(name=name)
        #db.session.add(category)
    #db.session.commit()

load_categories()

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    like = db.Column(db.Integer, autoincrement=True)
    uzivatel_id = db.Column(db.Integer, ForeignKey('uzivatel.id'))
    category_id = db.Column(db.Integer, ForeignKey('category.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    uzivatel = relationship('Uzivatel')
    category = relationship('Category')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    uzivatel_id = db.Column(db.Integer, ForeignKey('uzivatel.id'))
    thread_id = db.Column(db.Integer, ForeignKey('thread.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    Uzivatel = relationship('Uzivatel')
    thread = relationship('Thread')

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    uzivatel_id = db.Column(db.Integer, ForeignKey('uzivatel.id'))
    comment_id = db.Column(db.Integer, ForeignKey('comment.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    Uzivatel = relationship('Uzivatel')
    comment = relationship('Comment')

# query_result = session.query(Uzivatel).filter_by(name='John Doe').first()
# print("Query Result:", query_result)

# Add the instance to the database session
#db.session.add(new_data)

# Commit the changes to the database
#db.session.commit()

db.create_all()
    
log = logging.getLogger(__name__)

################## get role Admin ####################
# role_admin = app.sm.find_role(app.sm.auth_role_admin)
# if role_admin is None:
#     log.error('Error: please run \'flask fab create-admin\' before loading data!')
#     exit(1)

# ############# configuring role engineers #############
# role_moderator = app.sm.find_role('mods')
# if role_moderator is None:
#     app.sm.add_role('mods')
#     role_moderator = app.sm.find_role('mods')

# for pv in role_admin.permissions:
#     if ('Thread' in pv.__repr__() or \
#         'Comment' in pv.__repr__() or \
#         'Reply' in pv.__repr__() \
#        ) and not ( \
#         'add' in pv.__repr__() or \
#         'delete' in pv.__repr__() or \
#         'edit' in pv.__repr__() or \
#         'post' in pv.__repr__() or \
#         'show' in pv.__repr__() \
#         ):
#         app.sm.add_permission_role(role_moderator, pv)
#     if 'Task Progress' in pv.__repr__() or \
#        'TaskProgressModelView' in pv.__repr__() or \
#        'MyPassword' in pv.__repr__() or \
#        'mypassword' in pv.__repr__() or \
#        ('userinfo' in pv.__repr__() and 'userinfoedit' not in pv.__repr__()) or \
#        ('UserInfo' in pv.__repr__() and 'UserInfoEdit' not in pv.__repr__()):
#         app.sm.add_permission_role(role_moderator, pv)

# ############### configuring role public ##############
# role_poster = app.sm.find_role('posters')
# if role_poster is None:
#     app.sm.add_role('posters')
#     role_poster = app.sm.find_role('posters')

# for pv in role_admin.permissions:
#     if ('Task Progress' in pv.__repr__() or \
#         'TaskProgressModelView' in pv.__repr__() or
#         'Tasks Projects' in pv.__repr__() \
#         ) and not ( \
#         'add' in pv.__repr__() or \
#         'delete' in pv.__repr__() or \
#         'edit' in pv.__repr__() or \
#         'post' in pv.__repr__() or \
#         'show' in pv.__repr__()):
#         app.sm.add_permission_role(role_poster, pv)