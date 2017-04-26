"""Controller of inventory."""
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify
from flask_login import login_required

import re
# Import the database object from the main app module
import json

from forms import ServerForm, type_choices

# Import module models (i.e. User)
from models import Server

# Define the blueprint: 'auth', set its url prefix: url/auth
from . import servers, config
# from inventory import principal_menu
from app.modules import principal_menu
from app.login import admin, editor, user as viewer


@servers.route('/', methods=['GET'])
@servers.route('/list', methods=['GET', 'POST'])
@login_required
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
        total = Server.objects.filter(deleted=False).count()
        if search:
            keys = Server._fields.keys()
            keys.remove('id')
            params = [{'deleted': False}]
            regex = re.compile('.*%s.*' % search)
            for key in keys:
                params.append({key: regex})
            try:
                result = Server.objects.filter(__raw__={"$or": params}) \
                                       .limit(length) \
                                       .skip(start)
                count = Server.objects.filter(__raw__={"$or": params}) \
                                      .count()
            except Exception as e:
                print e
        else:
            try:
                result = Server.objects.filter(deleted=False) \
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
    return render_template("servers/list.html",
                           menu=principal_menu(),
                           config=config,
                           type_choices=dict(type_choices))


@servers.route('/create', methods=['GET', 'POST'])
@editor.require(http_exception=403)
@login_required
def create():
    """Create Method."""
    form = ServerForm(request.form)
    if form.validate_on_submit():
        obj = Server()
        form.populate_obj(obj)
        obj.deleted = False
        Server.objects.insert(obj)
        flash("Servidor creado", "success")
        return redirect(url_for("servers.list"))
    return render_template("servers/create.html",
                           action="create",
                           form=form,
                           menu=principal_menu(),
                           config=config)


@servers.route('/edit/<string:key>', methods=['GET', 'POST'])
@editor.require(http_exception=403)
@login_required
def edit(key):
    """Edit Method."""
    try:
        element = Server.objects.filter(deleted=False,
                                        id=key).first()
    except Exception:
        flash("Servidor No encontrado", "error")
        return redirect(url_for("servers.list"))
    if request.method == 'GET':
        form = ServerForm(request.form, element)
        return render_template("servers/create.html",
                               action="edit",
                               form=form,
                               menu=principal_menu(),
                               config=config)
    else:
        form = ServerForm(request.form)
        if form.validate_on_submit():
            element.update(**form.data)
            flash("Servidor Actualizado", "success")
            return redirect(url_for("servers.list"))
        return render_template("servers/create.html",
                               action="edit",
                               form=form,
                               menu=principal_menu(),
                               config=config)


@servers.route('/view/<string:key>', methods=['GET'])
@login_required
def view(key):
    """Edit Method."""
    try:
        element = Server.objects.filter(deleted=False,
                                        id=key).first()
    except Exception:
        flash("Servidor No encontrado", "error")
        return redirect(url_for("servers.list"))
    form = ServerForm(request.form, element)
    return render_template("servers/create.html",
                           action="view",
                           form=form,
                           menu=principal_menu(),
                           config=config)


@servers.route('/delete/<string:key>', methods=['GET'])
@editor.require(http_exception=403)
@login_required
def delete(key):
    """Delete Method."""
    try:
        element = Server.objects.filter(deleted=False,
                                        id=key).first()
    except Exception:
        flash("Servidor No encontrado", "error")
        return redirect(url_for("servers.list"))
    element.update(deleted=True)
    flash("Servidor Eliminado", "success")
    return redirect(url_for("servers.list"))


@servers.route('/export/<string:type>', methods=['GET'])
@servers.route('/export/<string:type>/<string:key>', methods=['GET'])
@login_required
def export(type='xls', key=None):
    """Export Method."""
    pass
