from flask import Blueprint


servers = Blueprint('servers', __name__)
config = {}
config['name'] = "Servidores"
config['menu'] = {'list': {'link': 'servers.list', 'name': 'Lista'},
                  'create': {'link': 'servers.create', 'name': 'Crear'}}

from controllers import *


def get_config():
    return config
