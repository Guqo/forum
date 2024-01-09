from flask_appbuilder import IndexView, expose, ModelView
from flask_appbuilder.baseviews import BaseModelView
from flask_appbuilder.models.sqla.filters import FilterEqual
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_login import current_user
from .models import Thread


class MyIndexView(IndexView, BaseModelView):
    datamodel = SQLAInterface(Thread)

    @expose('/')
    def index(self):
        # Zkontrolujte, zda je uživatel přihlášen a má potřebná oprávnění
        if current_user.is_authenticated and self.appbuilder.sm.has_access('can_list', 'ThreadModelView'):
            (_, user_threads) = self.datamodel.query(filters=self.datamodel.get_filters().add_filter('user_id', FilterEqual, current_user.id))
            # Předání článků do šablony
            return self.render_template('index.html', threads=user_threads, can_list=True)
        else:
            # Uživatel není přihlášen nebo nemá oprávnění, zobrazte pouze informační hlášení
            return self.render_template('index.html', message="Prosím přihlaste se pro zobrazení vašich chatů.")

