# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref
from tg.caching import cached_property
from tgext.pluggable import primary_key, app_model


DeclarativeBase = declarative_base()

class ResetPasswordRequest(DeclarativeBase):
    __tablename__ = 'resetpassword_requests'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey(primary_key(app_model.User)))
    user = relation(app_model.User, backref=backref('resetpassword_requests'))
    request_date = Column(DateTime, nullable=False, default=datetime.utcnow(), index=True)
    reset_link = Column(Unicode(150), nullable=False, index=True)

    @cached_property
    def request_email(self):
        return self.user.email_address