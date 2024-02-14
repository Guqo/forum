import logging

from flask import redirect, request, jsonify, flash, make_response, app
from flask_appbuilder import ModelView, action, BaseView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.views import AuthDBView
from flask_appbuilder.widgets import ListWidget
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_login import current_user
from markupsafe import Markup

from . import appbuilder, db
from .models import Group, Category, Thread, ForumUser

log = logging.getLogger(__name__)

# přidá do model Category roli Moderator
def fill_group():
    try:
        db.session.add(Group(name="Moderator"))
        db.session.commit()
    except Exception:
        db.session.rollback()

#přidá kategorie do atributu modelu Thread
def fill_category():
    try:
        # Přidání kategorií
        db.session.add(Category(name="Sci-fi"))
        db.session.add(Category(name="Horror"))
        db.session.add(Category(name="Comedy"))
        # Odeslání do databáze
        db.session.commit()
        # Pokud při 'try' dojde k chybě provede se 'rollback'
        # a vrátí databázi do původního stavu
    except Exception:
        db.session.rollback()

class GroupModelView(ModelView):
    datamodel = SQLAInterface(Group)


class ForumUserModelView(ModelView):
    datamodel = SQLAInterface(ForumUser)

#definice classy ThreadModelView, přidání řádků na vyplnění informací do databáze
class ThreadModelView(ModelView):
    datamodel = SQLAInterface(Thread)
    label_columns = {"title": "Titulek", "content": "Obsah",
                     "user": "Autor", "category": "Kategorie", "created_at": "Vytvořeno"}
    list_columns = ["title", "category", "user", "created_at"]
    base_order = ("created_at", "desc")
    show_fieldsets = [
        ("Vlákno", {"fields": ["title", "category", "content", "user", "created_at"]})]
    add_fieldsets = [
        ("Vlákno", {"fields": ["title", "category", "content"]})]
    edit_fieldsets = [
        ("Vlákno", {"fields": ["title", "category", "content", "user", "created_at"]})]
    def pre_add(self, item):
        item.user = db.session.query(ForumUser).filter_by(id=current_user.id).one_or_none()
        super(ThreadModelView, self).pre_add(item)


    @action(
        "muldelete",
        "Delete",
        Markup("<p>Delete all Really?</p><p>Ok then...</p>"),
        "fa-rocket",
    )
# funkce umožňující vymazání více článků naráz
    def muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())
    
    # Filtrování článků tak, aby uživatelé viděli jen své
    def get_query(self):
        return self.session.query(self.model).filter(self.model.user_id == current_user.id)



class ThreadListWidget(ListWidget):
    template = "appbuilder/general/widgets/threadlist.html"


class ThreadListWidgetOverride(ListWidget):
    template = "appbuilder/general/widgets/threadlistoverride.html"


class ThreadModelViewPublic(ModelView):
    datamodel = SQLAInterface(Thread)

    # user = thread.user_id = data.get('user_id')

    label_columns = {"title": "Titulek", "content": "Obsah",
                     "user": "Autor", "category": "Kategorie", "created_at": "Vytvořeno"}
    list_columns = ["title", "created_at", "user", "category"]
    base_order = ("created_at", "desc")
    list_template = "threadlist.html"
    list_widget = ThreadListWidgetOverride
    extra_args = {"widget_arg": "WIDGET"}


class CategoryModelView(ModelView):
    datamodel = SQLAInterface(Category)
    related_views = [ThreadModelView]

    def __init__(self, **kwargs):
        super(ModelView, self).__init__(**kwargs)
        self.list_title = "Seznam kategorií"
# classa umožňující vytvoření Threadu a přidání do databáze, příkaz umožňující aby Thread viděli jen přihlášení uživatelé
class MyThreadCreateView(BaseView):
    default_view = "create"

    @expose('/create/', methods=['POST'])
    @has_access  # Zajistuje, ze pouze opravneni uzivatele mohou vytvaret clanky
    def create(self):
            # Získání dat z AJAXového požadavku
            data = request.form

            # Vytvoreni a ulozeni noveho clanku
            thread = Thread()
            thread.title = data.get('title')
            thread.content = data.get('content')
            thread.user_id = data.get('user_id')
            thread.category_id = data.get('category_id')
            # Odeslani do databaze
            db.session.add(thread)
            db.session.commit()
            return redirect(self.appbuilder.get_url_for_index())

db.create_all()
fill_group()
fill_category()

appbuilder.add_view(
    GroupModelView,
    "Groups",
    icon="fa-folder-open-o",
    category="Admin Forum",
    category_icon="fa-envelope",
)

appbuilder.add_view(
    CategoryModelView,
    "Categories",
    icon="fa-envelope",
    category="Admin Forum"
)

appbuilder.add_view(
    ForumUserModelView,
    "ForumUsers",
    icon="fa-envelope",
    category="Admin Forum"
)

appbuilder.add_view(
    ThreadModelView,
    "Threads",
    icon="fa-envelope",
    category="Admin Forum"
)

appbuilder.add_view(
    ThreadModelViewPublic, "Threads", icon="fa-envelope", category="Public"
)

appbuilder.add_view(
    MyThreadCreateView, ""
)

log.info("F.A.B. Version: %s", appbuilder.version)
