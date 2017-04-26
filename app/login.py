# -*- coding: utf-8 -*-
from flask import (
    current_app,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
    g
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from flask_principal import (
    Principal,
    Identity,
    AnonymousIdentity,
    identity_changed,
    identity_loaded,
    RoleNeed,
    ActionNeed,
    Permission
)
from urlparse import urlparse, parse_qs
from werkzeug import check_password_hash

login_manager = LoginManager()
principals = Principal()
auth = Blueprint('auth', __name__)

# Needs
be_admin = RoleNeed('admin')
be_editor = RoleNeed('editor')
to_view = ActionNeed('viewer')

# Permissions
user = Permission(to_view)
user.description = "Viewer permissions"
editor = Permission(be_editor)
editor.description = "Editor's permissions"
admin = Permission(be_admin)
admin.description = "Admin's permissions"


@login_manager.user_loader
def load_user(user_id):
    "New class."
    from modules.user.models import User
    user = User.objects.filter(id=user_id).first()
    return user


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('auth.login'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/login?next=' + request.path)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    # import pdb;pdb.set_trace()
    from modules.user.forms import LoginForm
    from modules.user.models import User
    errors = {}
    form = LoginForm()
    if form.validate_on_submit():
        users = User.objects.filter(email=form.email.data)
        user = users.first()
        if user:
            if not user.active:
                flash("Cuenta Desactivada", "info")
                return redirect("/auth/login")
            elif check_password_hash(user.password, form.password.data):
                login_user(user, remember=False)
                # Tell Flask-Principal the identity changed
                identity = Identity(user.rol)
                identity_changed.send(current_app._get_current_object(), identity=identity)
                flash("Logeado Correctamente", "success")
                o = urlparse(request.referrer)
                query = parse_qs(o.query)
                if 'next' in query:
                    _next = query['next'][0]
                    return redirect(_next)
                else:
                    return redirect(url_for("index"))
        flash("Credenciales invalidas", "error")

    return render_template("auth/login.html", form=form)
