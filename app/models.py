from flask_appbuilder import Model
from flask_appbuilder.security.sqla.models import User, Role
from sqlalchemy import Column, Integer, ForeignKey, func, engine, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship


class Group(Role):
    __tablename__ = 'ab_role'


class Category(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return self.name

class ForumUser(User):
    __tablename__ = 'ab_user'


class Thread(Model):
    # Číslování (ID)
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Titulek
    title = Column(String(255), nullable=False)
    # Obsah
    content = Column(Text, nullable=False)
    # Vytvoření vztahu mezi aktuální tabulkou a tabulkou ab_user
    user_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    # Označení modelu ForumUser na user
    user = relationship('ForumUser')
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category')
    # Naplnění sloupce created_at aktuálním časem a datem
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return self.title
