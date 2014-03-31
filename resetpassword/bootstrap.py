# -*- coding: utf-8 -*-
"""Setup the resetpassword application"""
from __future__ import print_function

from resetpassword import model
from tgext.pluggable import app_model


def bootstrap(command, conf, vars):
    print('Bootstrapping resetpassword...')
