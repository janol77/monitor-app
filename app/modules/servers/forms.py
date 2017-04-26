# -*- coding: utf-8 -*-
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form
# Import Form elements such as TextField and BooleanField (optional)
from wtforms import (
    TextField,
    TextAreaField,
    SelectField,
    BooleanField
)
# Import Form validators
from wtforms.validators import (
    Required,
    Length,
    Optional
)
# Define the login form (WTForms)
type_choices = [('desarrollo', 'Desarrollo'),
                ('produccion', u'Producción'),
                ('otro', 'Otro')]


class ServerForm(Form):
    name = TextField('Nombre',
                     [Required(message='Debe ingresar nombre del Servidor')])
    ip = TextField(u'Ip/Hostname',
                   [Required(
                    message='Debe ingresar la ip/hostname del servidor')])
    type_server = SelectField('Tipo',
                              [Required(message='Debe seleccionar el tipo')],
                              choices=type_choices,
                              coerce=unicode)
    description = TextAreaField(u'Descripción',
                                [Optional(),
                                 Length(max=200)])
