from flask import Flask
from flask_appbuilder import ModelView, SQLA, IndexView
from . import app, db
from flask_appbuilder.models.sqla.interface import SQLAInterface

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