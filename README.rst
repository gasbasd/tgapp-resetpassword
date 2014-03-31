About resetpassword
-------------------------

resetpassword is a Pluggable application for TurboGears2 that
permits to change user password or reset it when lost.

Installing
-------------------------------

resetpassword can be installed both from pypi or from bitbucket::

    pip install tgapp-resetpassword

should just work for most of the users

Plugging resetpassword
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with resetpassword::

    plug(base_config, 'resetpassword')

You will be able to access the plugged application at
*http://localhost:8080/resetpassword*.

Available Hooks
----------------------

resetpassword makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

    * resetpassword.on_request(user, email_data, reset_link)

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

    * resetpassword.templates.index -> Page with password reset request form

    * resetpassword.templates.change_password -> Page with change password request
