# coding=utf-8
from __future__ import unicode_literals
from tw2.core import EmailValidator, ValidationError
from resetpassword import model
from tgext.pluggable import app_model



class RegisteredUserValidator(EmailValidator):
    def _validate_python(self, value, state=None):
        if model.provider.get_obj(app_model.User, params=dict(email_address=value)) is None:
            raise ValidationError('User not found', self)


