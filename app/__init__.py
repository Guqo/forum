import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.menu import Menu
from flask_jwt_extended import JWTManager

from .indexview import MyIndexView
from .secview import MyAuthDBView, MySecurityManager

app = Flask(__name__)
app.config.from_object("config")
app.config['FAB_LOGGING_LEVEL'] = 'DEBUG'
app.config['FAB_LOGGING_FORMAT'] = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
app.config['JWT_SECRET_KEY'] = 'ForumSphereSecretKey12345'  # Použijte bezpečný klíč
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Povolte použití cookies pro ukládání tokenů
app.config['JWT_COOKIE_SECURE'] = False  # Nastavte na True v produkčním prostředí s HTTPS
app.config['JWT_COOKIE_SAMESITE'] = None
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

jwt = JWTManager(app)

db = SQLA(app)

appbuilder = AppBuilder(
    app,
    db.session,
    # security_manager_class=MySecurityManager,
    indexview=MyIndexView,
    menu=Menu(reverse=False),
)

from . import views, api