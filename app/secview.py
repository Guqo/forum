from flask import request, make_response, redirect
from flask_appbuilder import expose
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder.security.views import AuthDBView
from flask_jwt_extended import create_access_token, set_access_cookies


class MyAuthDBView(AuthDBView):

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = self.appbuilder.sm.auth_user_db(username, password)
            if user is not None:
                # Vytvoření JWT
                access_token = create_access_token(identity=username)

                # Nastavení JWT do cookies
                response = make_response(redirect('/'))
                set_access_cookies(response, access_token)
                print('cookies', response)
                return response
            else:
                return self.render_template(self.login_template,
                                            title=self.title,
                                            appbuilder=self.appbuilder,
                                            username=request.form.get('username'),
                                            openIdProviders=self.openid_providers)

        return super(MyAuthDBView, self).login()


class MySecurityManager(SecurityManager):
    authdbview = MyAuthDBView