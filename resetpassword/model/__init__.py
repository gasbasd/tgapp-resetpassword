# -*- coding: utf-8 -*-
import logging
import tg
from tgext.pluggable import PluggableSession

log = logging.getLogger('tgapp-resetpassword')

DBSession = PluggableSession()


def init_model(app_session):
    DBSession.configure(app_session)


class PluggableSproxProvider(object):
    def __init__(self):
        self._provider = None

    def _configure_provider(self):
        if tg.config.get('use_sqlalchemy', False):
            log.info('Configuring resetpassword for SQLAlchemy')
            from sprox.sa.provider import SAORMProvider
            self._provider = SAORMProvider(session=DBSession)
        elif tg.config.get('use_ming', False):
            log.info('Configuring resetpassword for Ming')
            from sprox.mg.provider import MingProvider
            self._provider = MingProvider(DBSession)
        else:
            raise ValueError('resetpassword should be used with sqlalchemy or ming')

    def __getattr__(self, item):
        if self._provider is None:
            self._configure_provider()
        return getattr(self._provider, item)

provider = PluggableSproxProvider()