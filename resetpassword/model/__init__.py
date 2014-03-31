# -*- coding: utf-8 -*-
import logging
import tg
from tgext.pluggable import PluggableSession

log = logging.getLogger('tgapp-resetpassword')

DBSession = PluggableSession()
provider = None


def init_model(app_session):
    DBSession.configure(app_session)


def configure_models():
    global provider

    if tg.config.get('use_sqlalchemy', False):
        log.info('Configuring resetpassword for SQLAlchemy')
        from sprox.sa.provider import SAORMProvider
        provider = SAORMProvider(session=DBSession, engine=False)
    elif tg.config.get('use_ming', False):
        log.info('Configuring resetpassword for Ming')
        from sprox.mg.provider import MingProvider
        provider = MingProvider(DBSession)
    else:
        raise ValueError('resetpassword should be used with sqlalchemy or ming')


def configure_provider():
    if tg.config.get('use_sqlalchemy', False):
        provider.engine = DBSession.bind
