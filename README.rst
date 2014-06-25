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

Some options are available that can be set on ``.ini``
configuration file for your application.
At least one option is required to make activation emails
work:

    * **resetpassword.email_sender** -> Outgoing mails sender

If you are not using *TurboMail* a few more configuration
options must be set to make activation email work:

    * **resetpassword.smtp_host** -> SMTP server to use to send emails

    * **resetpassword.smtp_port** -> SMTP server port

    * **resetpassword.smtp_login** -> Login for authentication on SMTP server

    * **resetpassword.smtp_passwd** -> Password for authentication on SMTP server

Plugin Options
---------------------

When plugging ``tgapp-resetpassword`` the following options
can be passed to the plug call:

    * **reset_password.reset_password_form** -> Full python path of the form class to use for Reset Password form. By default *resetpassword.lib.forms.ResetPasswordForm* is used.

    * **reset_password.new_password_form** -> Full python path of the form class to use for New Password form. By default *registration.lib.forms.NewPasswordForm* is used.

Available Hooks
----------------------

resetpassword makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

    * resetpassword.on_request(user, email_data, reset_link)
    * resetpassword.before_render_change_password_template(user, deserialized_data)

Exposed Templates
--------------------

The templates used by resetpassword and that can be replaced with
*tgext.pluggable.replace_template* are:

    * resetpassword.templates.index -> Page with password reset request form

    * resetpassword.templates.change_password -> Page with change password request
