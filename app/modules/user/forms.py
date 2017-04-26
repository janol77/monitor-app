# -*- coding: utf-8 -*-
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form
# , RecaptchaField
from app.libs.validators import UniqueValidator
from models import User
# Import Form elements such as TextField and BooleanField (optional)
from wtforms import (
    TextField,
    PasswordField,
    SelectField,
    ValidationError,
    HiddenField,
    BooleanField
)

# Import Form validators
from wtforms.validators import(
    Required,
    Email,
    Length,
    DataRequired,
    EqualTo
)


# Define the login form (WTForms)

# def password_check(form, field):
#     print field.data
#     size = len(field.data)
#     if size > 6 and size > 8:
#         raise ValidationError(u'La contraseña debe \
#          tener entre 6 y 8 carácteres')
#     if field.data != form.confirm.data:
#         raise ValidationError(u'Las contraseñas deben coincidir')

rol_choices = [('admin', 'Administrador'),
               ('editor', 'Editor'),
               ('viewer', 'Lectura')]
state_choices = [('confirm', 'Confirmar Correo'),
                 ('confirmed', 'Correo Confirmado'),
                 ('reset', u'Cambio de Contraseña'),
                 ('email_reset', u'Cambio de Correo')]


class UserForm(Form):
    email = TextField(u'Correo Electrónico', [
        Email(message=u"El Correo Electronico no es Válido"),
        Required(message=u'Debe ingresar un correo electrónico'),
        UniqueValidator(User,
                        'email',
                        u'El Correo ya se utilizó para otra cuenta')])
    name = TextField('Nombre',
                     [Length(max=25),
                      Required(message='Debe ingresar un Nombre')])
    active = BooleanField('Activo')
    rol = SelectField('Rol',
                      [Required(message='Debe seleccionar el Rol')],
                      choices=rol_choices,
                      coerce=unicode,
                      default='viewer')


class PasswordForm(Form):
    password = PasswordField(u'Nueva Contraseña', [
        Length(max=8,
               min=6,
               message=u'La contraseña debe tener entre 6 y 8 carácteres'),
        DataRequired(message=u'Debe ingresar una contraseña válida'),
        EqualTo('confirm', message=u'Las contraseñas deben coincidir')],
        render_kw={"placeholder": u"Ingrese Nueva Password"})
    confirm = PasswordField(u'Repita Contraseña',
      render_kw={"placeholder": u"Confirme Nueva Password"})
    id = HiddenField('id')
    code = HiddenField('code')


class EditUserForm(Form):
    email = TextField(u'Correo Electrónico', [
        Email(message=u"El Correo Electronico no es Válido"),
        Required(message=u'Debe ingresar un correo electrónico'),
        UniqueValidator(User,
                        'email',
                        u'El Correo ya se utilizó para otra cuenta')])
    name = TextField('Nombre',
                     [Length(max=25),
                      Required(message='Debe ingresar un Nombre')])
    active = BooleanField('Activo')
    rol = SelectField('Rol',
                      [Required(message='Debe seleccionar el Rol')],
                      choices=rol_choices,
                      coerce=unicode)
    password = PasswordField(u'Nueva Contraseña')
    confirm = PasswordField(u'Repita Contraseña')
    id = HiddenField('id')

    def validate_password(form, field):
        size = len(field.data)
        if size > 0:
            if size < 6 or size > 8:
                raise ValidationError(u'La contraseña debe \
                 tener entre 6 y 8 carácteres')
        if field.data != form.confirm.data:
            raise ValidationError(u'Las contraseñas deben coincidir')


class LoginForm(Form):
    email = TextField(u'Correo Electrónico', [
        Email(message=u"El Correo Electronico no es Válido"),
        Required(message=u'Debe ingresar un correo electrónico')],
        render_kw={"placeholder": u"Ingrese su Email"})
    password = PasswordField(u'Contraseña', [
        DataRequired(message=u'Debe ingresar una contraseña válida')],
        render_kw={"placeholder": u"Contraseña"})
