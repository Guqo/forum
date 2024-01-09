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


# class ForumUser(Model, UserExtensionMixin):
#     group_id = Column(Integer, ForeignKey('group.id'))
#     group = relationship('Group')
#
#     def __repr__(self):
#         return self.username

class ForumUser(User):
    __tablename__ = 'ab_user'


class Thread(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    like = Column(Integer)
    user_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user = relationship('ForumUser')
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return self.title


class Comment(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user = relationship('ForumUser')
    thread_id = Column(Integer, ForeignKey('thread.id'))
    thread = relationship('Thread')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return self.content


class Reply(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user = relationship('ForumUser')
    comment_id = Column(Integer, ForeignKey('comment.id'))
    comment = relationship('Comment')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return self.content
