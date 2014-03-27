# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate

from resetpassword.lib.i18n import p_ as _, lp_ as l_
from resetpassword import model
from resetpassword.model import DBSession

class RootController(TGController):
    @expose('resetpassword.templates.index')
    def index(self):
        sample = DBSession.query(model.Sample).first()
        flash(_("Hello World!"))
        return dict(sample=sample)
