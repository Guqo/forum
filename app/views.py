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
from .models import Group, Category, Thread, Comment, Reply, ForumUser

log = logging.getLogger(__name__)


def fill_group():
    try:
        db.session.add(Group(name="Moderator"))
        db.session.commit()
    except Exception:
        db.session.rollback()

def fill_category():
    try:
        db.session.add(Category(name="Math"))
        db.session.add(Category(name="History"))
        db.session.add(Category(name="English"))
        db.session.commit()
    except Exception:
        db.session.rollback()


class GroupModelView(ModelView):
    datamodel = SQLAInterface(Group)


class ForumUserModelView(ModelView):
    datamodel = SQLAInterface(ForumUser)


class ThreadModelView(ModelView):
    datamodel = SQLAInterface(Thread)

    label_columns = {"title": "Titulek", "content": "Obsah", "like": "Obliba",
                     "user": "Autor", "category": "Kategorie", "created_at": "Vytvořeno"}
    list_columns = ["title", "created_at", "user", "category"]

    base_order = ("created_at", "desc")

    show_fieldsets = [
        ("Vlákno", {"fields": ["title", "user"]}),
        (
            "Podrobné informace",
            {
                "fields": [
                    "created_at",
                    "category",
                    "like",
                    "content",
                ],
                "expanded": False,
            },
        ),
    ]

    add_fieldsets = [
        ("Vlákno", {"fields": ["title", "user"]}),
        (
            "Podrobné informace",
            {
                "fields": [
                    "created_at",
                    "category",
                    "like",
                    "content",
                ],
                "expanded": False,
            },
        ),
    ]

    edit_fieldsets = [
        ("Vlákno", {"fields": ["title", "user"]}),
        (
            "Podrobné informace",
            {
                "fields": [
                    "created_at",
                    "category",
                    "like",
                    "content",
                ],
                "expanded": False,
            },
        ),
    ]

    @action(
        "muldelete",
        "Delete",
        Markup("<p>Delete all Really?</p><p>Ok then...</p>"),
        "fa-rocket",
    )
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

    label_columns = {"title": "Titulek", "content": "Obsah", "like": "Like",
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


class MyView(BaseView):

    default_view = "method1"

    @expose("/method1/")
    @has_access
    def method1(self):
        # do something with param1
        # and return to previous page or index
        return "Hello"

    @expose("/method2/<string:param1>")
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = "Goodbye %s" % (param1)
        return param1

    @expose("/method3/<string:param1>")
    @has_access
    def method3(self, param1):
        # do something with param1
        # and render template with param
        param1 = "Goodbye %s" % (param1)
        return self.render_template("method3.html", param1=param1)


class MyThreadCreateView(BaseView):
    default_view = "create"

    @expose('/create/', methods=['POST'])
    @has_access  # Zajišťuje, že pouze oprávnění uživatelé mohou vytvářet články
    def create(self):
        try:
            # Získání dat z AJAXového požadavku
            data = request.form
            # Přidejte zde další pole a validaci

            # Vytvoření a uložení nového článku
            thread = Thread()
            thread.title = data.get('title')
            thread.content = data.get('content')
            thread.user_id = data.get('user_id')
            thread.category_id = data.get('category_id')
            # Nastavte další atributy článku
            db.session.add(thread)
            db.session.commit()

            # Odpověď pro AJAXový požadavek
            return jsonify(status="success", message="Článek byl úspěšně vytvořen.")
        except Exception as e:
            # V případě chyby vrátíte chybovou zprávu
            return jsonify(status="error", message=str(e))


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
    MyThreadCreateView, "Create thread"
)

appbuilder.add_view(MyView(), "Method1", category="My View")
# appbuilder.add_view(
#     MyView(), "Method2", href='/myview/method2/jonh', category='My View'
# )
# Use add link instead there is no need to create MyView twice.
appbuilder.add_link("Method2", href="/myview/method2/jonh", category="My View")
appbuilder.add_link("Method3", href="/myview/method3/jonh", category="My View")

log.info("F.A.B. Version: %s", appbuilder.version)