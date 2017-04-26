from flask import Blueprint

user = Blueprint('user', __name__)
config = {}
config['name'] = "Usuarios"
config['menu'] = {'list': {'link': 'user.list', 'name': 'Lista'},
                  'create': {'link': 'user.create', 'name': 'Crear'}}

from controllers import *


def get_config():
	return config
