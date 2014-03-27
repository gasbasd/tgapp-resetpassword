# -*- coding: utf-8 -*-
"""Main Controller"""
from datetime import datetime
from itsdangerous import URLSafeSerializer
from resetpassword.lib import get_reset_password_form, send_email, get_new_password_form

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from resetpassword.lib.i18n import p_ as _, lp_ as l_
from resetpassword import model
import tg
from tgext.pluggable import app_model


class RootController(TGController):
    @expose('genshi:resetpassword.templates.index')
    def index(self, **kw):
        return dict(reset_password_form=get_reset_password_form(), action=self.mount_point+'/reset_request')

    @expose()
    @validate(get_reset_password_form(), error_handler=index)
    def reset_request(self, **kw):
        user = model.provider.get_obj(app_model.User, params=dict(email_address=kw['email_address']))
        password_frag = user.password[0:4]
        serializer = URLSafeSerializer(tg.config['beaker.session.secret'])
        request_date = datetime.strptime(datetime.utcnow().strftime('%m/%d/%Y %H:%M'), '%m/%d/%Y %H:%M')
        serialized_data = serializer.dumps(dict(request_date=request_date.strftime('%m/%d/%Y %H:%M'),
                                                email_address=kw['email_address'], password_frag=password_frag))
        password_reset_link = tg.url(self.mount_point + "/change_password/", params=dict(data=serialized_data), qualified=True)
        reset_password_config = tg.config.get('_pluggable_resetpassword_config')
        mail_body = reset_password_config.get('mail_body', _('''
We've received a request to reset the password for this account. Please click this link to reset your password:
%(password_reset_link)s
If you no longer wish to make the above change, or if you did not initiate this request, please disregard and/or delete this e-mail.
'''))
        if '%(password_reset_link)s' not in mail_body:
            mail_body += '\n \n %(password_reset_link)s'

        email_data = {'sender': tg.config['resetpassword.email_sender'],
                      'subject': reset_password_config.get('mail_subject', _('Password reset request')),
                      'body': mail_body,
                      'rich': reset_password_config.get('mail_rich', '')}

        hooks = tg.config['hooks'].get('resetpassword.on_request', [])
        for func in hooks:
            func(user, email_data, password_reset_link)

        email_data['body'] = email_data['body'] % dict(password_reset_link=password_reset_link)
        email_data['rich'] = email_data['rich'] % dict(password_reset_link=password_reset_link)

        send_email(user.email_address, **email_data)
        if model.provider.get_obj(model.ResetPasswordRequest, params=dict(user_id=user._id)):
            model.provider.delete(model.ResetPasswordRequest, params=dict(user_id=user._id))
        model.provider.create(model.ResetPasswordRequest, dict(user=user,
                                                               request_date=request_date,
                                                               reset_link=password_reset_link))
        flash(_('Password reset request sent'))
        return redirect(self.mount_point)

    @expose('genshi:resetpassword.templates.change_password')
    def change_password(self, **kw):
        serializer = URLSafeSerializer(tg.config['beaker.session.secret'])
        deserialized_data = serializer.loads(kw['data'])
        request_date = datetime.strptime(deserialized_data['request_date'], '%m/%d/%Y %H:%M')
        user = model.provider.get_obj(app_model.User, params=dict(email_address=deserialized_data['email_address']))
        password_frag = user.password[0:4]
        reset_request = model.provider.get_obj(model.ResetPasswordRequest,
                                               params=dict(user_id=user._id))
        if abs((datetime.now() - reset_request.request_date).days) > 1:
            flash('Password reset request timed out', 'error')
            return redirect(self.mount_point)
        if password_frag == deserialized_data['password_frag'] and request_date == reset_request.request_date \
                                                               and reset_request.user == user:
            return dict(new_password_form=get_new_password_form(),
                        form_data=dict(email_address=user.email_address), action=self.mount_point+'/save_password')
        flash(_('Invalid password reset request'), 'error')
        return redirect(self.mount_point)


    @expose()
    @validate(get_new_password_form(), error_handler=change_password)
    def save_password(self, **kw):
        user = model.provider.get_obj(app_model.User, params=dict(email_address=kw['email_address']))
        user.password = kw['password']
        model.provider.delete(model.ResetPasswordRequest, params=dict(user_id=user._id))
        flash(_('Password changed successfully'))
        return redirect(self.mount_point)
