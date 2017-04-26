# -*- coding: utf-8 -*-
# Import flask dependencies
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    redirect,
    url_for,
    jsonify
)
from flask_login import login_required

import re
# Import the database object from the main app module
import json

from forms import (
    UserForm,
    EditUserForm,
    PasswordForm,
    rol_choices,
    state_choices
)
from libs.tools import sendmail

# Import module models (i.e. User)
from models import User

# Define the blueprint: 'auth', set its url prefix: url/auth
from . import user, config
from app.modules import principal_menu
from app.login import admin, user as view


# Set the route and accepted methods
@user.route('/', methods=['GET'])
@user.route('/list', methods=['GET', 'POST'])
@login_required
@admin.require(http_exception=403)
def list():
    """List Method."""
    if request.method == 'POST':
        data = json.loads(request.form.get("args"))
        draw = data['draw']
        length = data['length']
        start = data['start']
        search = data['search']['value']
        result = []
        response = {}
        count = 0
        total = User.objects.filter(deleted=False).count()
        keys = User._fields.keys()
        keys.remove('password')
        fields = keys[:]
        keys.remove('id')
        keys.remove('protected')
        if search:
            params = [{'deleted': False}]
            regex = re.compile('.*%s.*' % search)
            for key in keys:
                params.append({key: regex})
            try:
                result = User.objects.filter(__raw__={"$or": params}) \
                                     .only(*fields) \
                                     .limit(length) \
                                     .skip(start)
                count = User.objects.filter(__raw__={"$or": params}) \
                                    .count()
            except Exception as e:
                print e
        else:
            try:
                result = User.objects.filter(deleted=False) \
                                     .only(*fields) \
                                     .limit(length) \
                                     .skip(start)
                count = total
            except Exception as e:
                print e

        # order = int(request.form.get('order[0][column]'))
        # order_dir = request.form.get('order[0][dir]')
        response['draw'] = draw
        response["recordsTotal"] = total
        response["recordsFiltered"] = count
        response["data"] = result
        return jsonify(response)
    return render_template("user/list.html",
                           menu=principal_menu(),
                           config=config,
                           rol_choices=dict(rol_choices),
                           state_choices=dict(state_choices))


# Set the route and accepted methods
@user.route('/create', methods=['GET', 'POST'])
@login_required
@admin.require(http_exception=403)
def create():
    """Create Method."""
    form = UserForm(request.form)
    if form.validate_on_submit():
        obj = User()
        form.populate_obj(obj)
        obj.generate_code()
        obj.state = "confirm"
        new_user = User.objects.insert(obj)
        receivers = [{'email': obj.email, 'name': obj.name}]
        code = obj.code
        _id = str(new_user.id)
        url = request.referrer.split(request.path)[0]
        sm = sendmail(receivers, _type=1, code=code, _id=_id, url=url)
        if not sm:
            flash("Error enviando correo de confirmación", "error")
        else:
            flash("Un correo ha sido enviado a %s" % obj.email, "success")
            flash("Confirme el correo para activar cuenta", "info")
        return redirect(url_for("user.list"))
    return render_template("user/create.html",
                           action="create",
                           form=form,
                           menu=principal_menu(),
                           config=config)


@user.route('/edit/<string:key>', methods=['GET', 'POST'])
@login_required
@admin.require(http_exception=403)
def edit(key):
    """Edit Method."""
    try:
        element = User.objects.filter(deleted=False,
                                      id=key).first()
    except Exception:
        flash("Elemento No encontrado", "error")
        return redirect(url_for("user.list"))
    if request.method == 'GET':
        form = EditUserForm(request.form, element)
        return render_template("user/create.html",
                               action="edit",
                               form=form,
                               menu=principal_menu(),
                               config=config)
    form = EditUserForm(request.form)
    if form.validate_on_submit():
        email = element.email
        new_email = form.email.data
        form.populate_obj(element)
        if new_email == email:
            element.save()
            flash("Elemento Actualizado", "success")
            return redirect(url_for("user.list"))
        receivers = [{'email': element.email, 'name': element.name}]
        element.generate_code()
        element.state = "email_reset"
        code = element.code
        _id = str(element.id)
        url = request.referrer.split(request.path)[0]
        sm = sendmail(receivers, _type=1, code=code, _id=_id, url=url)
        if not sm:
            flash("Error enviando correo de confirmación", "error")
        else:
            flash("Un correo ha sido enviado a %s" % new_email, "success")
            flash("Confirme el correo para reactivar cuenta", "info")
        element.save()
        return redirect(url_for("user.list"))
    return render_template("user/create.html",
                           action="edit",
                           form=form,
                           menu=principal_menu(),
                           config=config)


@user.route('/view/<string:key>', methods=['GET'])
@login_required
@admin.require(http_exception=403)
def view(key):
    """View Method."""
    try:
        element = User.objects.filter(deleted=False,
                                      id=key).first()
    except Exception:
        flash("Elemento No encontrado", "error")
        return redirect(url_for("user.list"))
    form = EditUserForm(request.form, element)
    return render_template("user/create.html",
                           action="view",
                           form=form,
                           menu=principal_menu(),
                           config=config)


@user.route('/delete/<string:key>', methods=['GET'])
@login_required
@admin.require(http_exception=403)
def delete(key):
    """Delete Method."""
    try:
        element = User.objects.filter(deleted=False,
                                      id=key).first()
    except Exception:
        flash("Elemento No encontrado", "error")
        return redirect(url_for("user.list"))
    if not element.protected:
        element.update(deleted=True)
        flash("Elemento Eliminado", "success")
    else:
        flash("Elemento Protegido, no se puede eliminar", "info")
    return redirect(url_for("user.list"))


@user.route('/reset_password/<string:key>', methods=['GET'])
@login_required
@admin.require(http_exception=403)
def reset_password(key):
    """Reset Method."""
    try:
        element = User.objects.filter(deleted=False,
                                      id=key).first()
    except Exception:
        flash("Elemento No encontrado", "error")
        return redirect(url_for("user.list"))
    mail = element.email
    ##### Enviar correo para restablecer contraseña
    element.generate_code()
    element.state = "reset"
    element.save()
    flash("Un correo ha sido enviado a %s" % mail, "success")
    return redirect(url_for("user.list"))


@user.route('/<string:key>/activate/<string:token>', methods=['GET', 'POST'])
def activate(key, token):
    """Activate Method."""
    try:
        element = User.objects.filter(deleted=False,
                                      id=key,
                                      code=token).first()
    except Exception:
        flash("Usuario no Existe", "error")
        return redirect(url_for("index"))
    if element.state == 'confirmed':
        flash(u"Contraseña Actualizada Anteriormente", "info")
        return redirect(url_for('auth.login'))
    if element.state == "email_reset":
        element.state = "confirmed"
        element.save()
        flash(u"Correo Actualizado", "success")
        return redirect(url_for('auth.login'))
    form = PasswordForm(request.form, element)
    if request.method == 'GET':
        return render_template("auth/password.html",
                               form=form)
    if form.validate_on_submit():
        state = element.state
        password = form.password.data
        element.password = password
        element.generate_password()
        element.state = "confirmed"
        element.save()
        flash(u"Contraseña Actualizada", "success")
        if state == 'confirm':
            flash(u"Cuenta Activada", "info")
        return redirect(url_for('auth.login'))
    return render_template("auth/password.html",
                           form=form)
