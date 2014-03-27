# -*- coding: utf-8 -*-
from datetime import datetime
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from resetpassword.model import DBSession
from ming import schema as s
from tg.caching import cached_property
from tgext.pluggable import app_model


class ResetPasswordRequest(MappedClass):
    class __mongometa__:
        name = 'resetpassword_requests'
        session = DBSession
        indexes = []

    _id = FieldProperty(s.ObjectId)
    user_id = ForeignIdProperty(app_model.User)
    user = RelationProperty('User')
    request_date = FieldProperty(s.DateTime, if_missing=datetime.utcnow())
    reset_link = FieldProperty(s.String, required=True)

    @cached_property
    def uid(self):
        # Provided for seamless compatibility with SQLAlchemy
        return str(self._id)

    @cached_property
    def request_email(self):
        return self.user.email_address