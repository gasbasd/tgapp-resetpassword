import functools
from tgext.pluggable import i18n

__all__ = ['p_', 'lp_', 'np_', 'lnp_']

p_ = functools.partial(i18n.ugettext, "resetpassword")
lp_ = functools.partial(i18n.lazy_ugettext, "resetpassword")

np_ = functools.partial(i18n.ungettext, "resetpassword")
lnp_ = functools.partial(i18n.lazy_ungettext, "resetpassword")