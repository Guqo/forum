from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship, declarative_base, create_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy

from app import app

# mysql_connection_string = 'mysql://admin:AdminadminAdmin@localhost/sys'
# engine = create_engine(mysql_connection_string, echo=True)
# Base = declarative_base()

# Session = sessionmaker(bind=engine)
# session = Session()
db = SQLAlchemy(app)
# app['SQLALCHEMY_DATABASE_URI'] = mysql_connection_string


class Skupiny(Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def repr(self):
        return self.name

skupiny_data = ['Admin', 'Moderator', 'Uzivatel']

def load_skupiny():
    for skupiny_name in skupiny_data:
        skupiny = Skupiny(name=skupiny_name)
    #     session.add(skupiny)
    # session.commit()

load_skupiny()

class Uzivatel(Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    skupiny_id = db.Column(db.Integer, ForeignKey('skupiny.id'))
    skupiny = relationship('Skupiny')

class Category(Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def repr(self):
        return self.name

categories_data = ['Maths', 'History', 'English']

def load_categories():
    for name in categories_data:
        category = Category(name=name)
    #     session.add(category)
    # session.commit()

load_categories()

class Thread(Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    like = db.Column(db.Integer, autoincrement=True)
    uzivatel_id = db.Column(db.Integer, ForeignKey('uzivatel.id'))
    category_id = db.Column(db.Integer, ForeignKey('category.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    uzivatel = relationship('Uzivatel')
    category = relationship('Category')

class Comment(Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    uzivatel_id = db.Column(db.Integer, ForeignKey('uzivatel.id'))
    thread_id = db.Column(db.Integer, ForeignKey('thread.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    Uzivatel = relationship('Uzivatel')
    thread = relationship('Thread')

class Reply(Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    uzivatel_id = db.Column(db.Integer, ForeignKey('uzivatel.id'))
    comment_id = db.Column(db.Integer, ForeignKey('comment.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())
    Uzivatel = relationship('Uzivatel')
    comment = relationship('Comment')


# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# query_result = session.query(Uzivatel).filter_by(name='John Doe').first()
# print("Query Result:", query_result)