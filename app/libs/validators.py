"""Validators class."""
# -*- coding: utf-8 -*-
from wtforms import ValidationError


class UniqueValidator(object):
    """Validador para chequear variables unicas."""

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'Existe otro Elemento con el mismo valor.'
        self.message = message

    def __call__(self, form, field):
        _id = None
        params = {self.field: field.data,
                  'deleted': False}
        existing = self.model.objects.filter(**params).first()
        if 'id' in form.data:
            _id = str(form.id.data)
        if existing and (_id is None or _id != str(existing.id)):
            raise ValidationError(self.message)
