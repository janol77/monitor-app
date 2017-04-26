import importlib
import copy

def principal_menu():
    from app.login import (
        admin,
        editor,
        user as u
    )
    permisions = [
        # {'inventory': {'create': editor, 'list': u}},
        {'servers': {'create': editor, 'list': u}},
        # {'services': {'create': editor, 'list': u}},
        {'user': admin}]
    menu = []
    for item in permisions:
        for m, ele in item.items():
            module_obj = importlib.import_module('app.modules.' + m)
            config = copy.deepcopy(module_obj.config)
            if type(ele) is not dict:
                if not ele.can():
                    continue
                menu.append(config)
                continue
            for submenu, permision in ele.items():
                if not permision.can():
                    del config['menu'][submenu]
                    continue
            if not config['menu']:
                continue
            menu.append(config)
    return menu
