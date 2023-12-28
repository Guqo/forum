import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder.security.sqla.models import User

"""
 Logging configuration
"""

app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:AdminadminAdmin@localhost/sys'  # SQLite for simplicity
db = SQLAlchemy(app)
login_manager = LoginManager(app)


appbuilder = AppBuilder(base_template='mybase.html')

app.config["AUTH_USER_MODEL"] = "models.MyUser"
app.config["AUTH_TYPE"] = 1

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views