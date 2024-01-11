from flask_appbuilder import ModelRestApi
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.filters import BaseFilter
from sqlalchemy import or_
from . import appbuilder, db
from .models import Thread, Category, ForumUser, Group


class GroupModelApi(ModelRestApi):
    resource_name = 'group'
    datamodel = SQLAInterface(Group)


class CategoryModelApi(ModelRestApi):
    resource_name = 'category'
    datamodel = SQLAInterface(Category)


class ThreadModelApi(ModelRestApi):
    resource_name = 'thread'
    datamodel = SQLAInterface(Thread)


appbuilder.add_api(GroupModelApi)
appbuilder.add_api(CategoryModelApi)
appbuilder.add_api(ThreadModelApi)

