# coding=utf-8

from __future__ import unicode_literals
from formencode.validators import FieldsMatch
from resetpassword.lib.validators import RegisteredUserValidator
from tw2.core import Validator

from tw2.forms import TableForm, HiddenField, PasswordField, SubmitButton, TextField
from tg.i18n import lazy_ugettext as l_


class NewPasswordForm(TableForm):
    data = HiddenField()
    password = PasswordField(label=l_('New password'), validator=Validator(required=True))
    password_confirm = PasswordField(label=l_('Confirm new password'), validator=Validator(required=True))
    validator = FieldsMatch('password', 'password_confirm')
    submit = SubmitButton(value=l_('Save new password'))


class ResetPasswordForm(TableForm):
    email_address = TextField(label=l_('Email address'), validator=RegisteredUserValidator(required=True))
    submit = SubmitButton(value=l_('Send Request'))
