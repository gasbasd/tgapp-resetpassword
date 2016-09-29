# -*- coding: utf-8 -*-
"""Main Controller"""
from datetime import datetime
from itsdangerous import URLSafeSerializer
from resetpassword.lib import get_reset_password_form, send_email, get_new_password_form

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import lazy_ugettext as l_, ugettext as _
from resetpassword import model
import tg
from tgext.pluggable import app_model, plug_url, plug_redirect


class RootController(TGController):
    @expose('resetpassword.templates.index')
    def index(self, **kw):
        return dict(reset_password_form=get_reset_password_form(), 
                    action=plug_url('resetpassword', '/reset_request'))

    @expose()
    @validate(get_reset_password_form(), error_handler=index)
    def reset_request(self, **kw):
        user = model.provider.query(app_model.User, filters=dict(email_address=kw['email_address']))[1][0]
        password_frag = user.password[0:4]
        secret = tg.config.get('session.secret', tg.config.get('beaker.session.secret'))
        serializer = URLSafeSerializer(secret)
        serialized_data = serializer.dumps(dict(request_date=datetime.utcnow().strftime('%m/%d/%Y %H:%M'),
                                                email_address=kw['email_address'], password_frag=password_frag))

        password_reset_link = tg.url(self.mount_point + "/change_password/", params=dict(data=serialized_data),
                                     qualified=True)
        reset_password_config = tg.config.get('_pluggable_resetpassword_config')
        mail_body = reset_password_config.get('mail_body', _('''
We've received a request to reset the password for this account. 
Please click this link to reset your password:

%(password_reset_link)s

If you no longer wish to make the above change, or if you did not initiate this request, please disregard and/or delete this e-mail.
'''))
        email_data = {'sender': tg.config['resetpassword.email_sender'],
                      'subject': reset_password_config.get('mail_subject', _('Password reset request')),
                      'body': mail_body,
                      'rich': reset_password_config.get('mail_rich', '')}

        tg.hooks.notify('resetpassword.on_request', args=(user, email_data, password_reset_link))

        email_data['body'] = email_data['body'] % dict(password_reset_link=password_reset_link)
        email_data['rich'] = email_data['rich'] % dict(password_reset_link=password_reset_link)

        send_email(user.email_address, **email_data)
        flash(_('Password reset request sent'))

        redirect_url = None
        redirect_url = tg.hooks.notify_with_value('resetpassword.before_redirect', redirect_url)
        if redirect_url:
            return redirect(redirect_url)

        return plug_redirect('resetpassword', '/')

    @expose('resetpassword.templates.change_password')
    def change_password(self, **kw):
        if kw.get('data') is None:
            flash(_('Invalid password reset request'), 'error')
            return plug_redirect('resetpassword', '/')
        
        secret = tg.config.get('session.secret', tg.config.get('beaker.session.secret'))
        serializer = URLSafeSerializer(secret)
        deserialized_data = serializer.loads(kw['data'])
        user = model.provider.query(app_model.User,
                                    filters=dict(email_address=deserialized_data['email_address']))[1][0]

        tg.hooks.notify('resetpassword.before_render_change_password_template', args=(user, deserialized_data))

        return dict(new_password_form=get_new_password_form(),
                    form_data=dict(data=kw['data']),
                    action=plug_url('resetpassword', '/save_password'))

    @expose()
    @validate(get_new_password_form(), error_handler=change_password)
    def save_password(self, **kw):
        secret = tg.config.get('session.secret', tg.config.get('beaker.session.secret'))
        serializer = URLSafeSerializer(secret)
        deserialized_data = serializer.loads(kw['data'])
        request_date = datetime.strptime(deserialized_data['request_date'], '%m/%d/%Y %H:%M')
        user = model.provider.query(app_model.User,
                                    filters=dict(email_address=deserialized_data['email_address']))[1][0]
        password_frag = user.password[0:4]
        if abs((datetime.now() - request_date).days) > 1:
            flash(_('Password reset request timed out'), 'error')
            return plug_redirect('resetpassword', '/')

        if password_frag != deserialized_data['password_frag']:
            flash(_('Invalid password reset request'), 'error')
            return plug_redirect('resetpassword', '/')

        user.password = kw['password']
        flash(_('Password changed successfully'))
        return redirect('/')
