from flask import Flask
from flask_appbuilder import ModelView, SQLA, IndexView
from models import db, Thread, Comment, Reply
from . import app, db
from flask_appbuilder.models.sqla.interface import SQLAInterface

#  class ThreadV(ModelView):
#      datamodel = SQLAInterface(Thread)
#      list_template = 'index.html'
#      list_columns = ['column1', 'column2', 'column3']

# app.add_view(ThreadV, "Thread List", icon="fa-folder-open-o", category="My Models")

# class ThreadCreate(ModelView):
#     datamodel = SQLAInterface(Thread)
#     list_template = 'create_thread_form.html'

# app.add_view(ThreadCreate, "Thread Create Form", icon="fa-folder-open-o", category="My Models")

class SkupinyModelView(ModelView):
    datamodel = db

class UzivatelModelView(ModelView):
    datamodel = db

class CategoryModelView(ModelView):
    datamodel = db

class ThreadModelView(ModelView):
    datamodel = db

class CommentModelView(ModelView):
    datamodel = db

class ReplyModelView(ModelView):
    datamodel = db

app.add_view_no_menu(SkupinyModelView)
app.add_view_no_menu(UzivatelModelView)
app.add_view_no_menu(CategoryModelView)
app.add_view_no_menu(ThreadModelView)
app.add_view_no_menu(CommentModelView)
app.add_view_no_menu(ReplyModelView)