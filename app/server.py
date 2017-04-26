"""Server."""
from flask_login import login_required
from db import db
from login import(
    principals,
    login_manager,
    user,
    to_view,
    be_editor,
    be_admin
)
from flask_principal import (
    identity_loaded
)
# Import flask and template operators
from flask import Flask, render_template, session
from flask_wtf.csrf import CsrfProtect
from modules import principal_menu
from datetime import timedelta
import os


def create_app(config="config.ini"):

    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(__name__)
    if os.path.exists(config):
        app.config.from_pyfile(config)
    else:
        print("The app does not have a config.ini file")
    # Define the WSGI application object
    db.init_app(app)
    # csrf protection
    login_manager.init_app(app)
    principals.init_app(app)
    csrf = CsrfProtect()
    csrf.init_app(app)
    # Register blueprint(s)
    # from modules.inventory import inventory as inventory_blueprint
    # app.register_blueprint(inventory_blueprint, url_prefix='/inventory')
    from modules.servers import servers as servers_blueprint
    app.register_blueprint(servers_blueprint, url_prefix='/servers')
    # from modules.services import services as services_blueprint
    # app.register_blueprint(services_blueprint, url_prefix='/services')
    from modules.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    from login import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route("/", methods=['GET'])
    @login_required
    @user.require(http_exception=403)
    def index():
        return render_template("index.html",
                               menu=principal_menu())

    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # Sample HTTP error handling
    @app.errorhandler(403)
    def access_denied(error):
        return render_template('403.html'), 403

    # Sample HTTP error handling
    @app.errorhandler(500)
    def server_full(error):
        return render_template('500.html'), 500

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)
        session.modified = True

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        needs = []

        if identity.id in ('viewer', 'editor', 'admin'):
            needs.append(to_view)

        if identity.id in ('editor', 'admin'):
            needs.append(be_editor)

        if identity.id == 'admin':
            needs.append(be_admin)

        for n in needs:
            identity.provides.add(n)

        # If the authenticated identity is :
        # - 'the_only user' she can sign in
        # - "the_only_editor" she can sign in and edit
        # - "the_only_admin" she can sign in , edit and administrate

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 5000),
            debug=app.config.get('DEBUG', False)
            )
