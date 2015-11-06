# -*- coding: utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from smtplib import SMTP
from tg import config
from tg import request

try:
    import turbomail
except ImportError:
    turbomail = None

try:
    from tgext.mailer import Message as message, Attachment
    from tgext.mailer import get_mailer
except ImportError:
    message = None

def get_reset_password_form():
    reset_password_config = config['_pluggable_resetpassword_config']
    reset_password_form = reset_password_config.get('reset_password_form_instance')
    if not reset_password_form:
        form_path = reset_password_config.get('reset_password_form', 'resetpassword.lib.forms.ResetPasswordForm')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        reset_password_form = reset_password_config['reset_password_form_instance'] = form_class()

    return reset_password_form


def get_new_password_form():
    reset_password_config = config['_pluggable_resetpassword_config']

    new_password_form = reset_password_config.get('new_password_form_instance')
    if not new_password_form:
        form_path = reset_password_config.get('new_password_form', 'resetpassword.lib.forms.NewPasswordForm')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        new_password_form = reset_password_config['new_password_form_instance'] = form_class()

    return new_password_form


def _plain_send_mail(sender, recipient, subject, body):
    header_charset = 'ISO-8859-1'
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            body.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break

    sender_name, sender_addr = parseaddr(sender)
    recipient_name, recipient_addr = parseaddr(recipient)

    sender_name = str(Header(unicode(sender_name), header_charset))
    recipient_name = str(Header(unicode(recipient_name), header_charset))

    sender_addr = sender_addr.encode('ascii')
    recipient_addr = recipient_addr.encode('ascii')

    msg = MIMEText(body.encode(body_charset), 'plain', body_charset)
    msg['From'] = formataddr((sender_name, sender_addr))
    msg['To'] = formataddr((recipient_name, recipient_addr))
    msg['Subject'] = Header(unicode(subject), header_charset)

    smtp = SMTP(config.get('resetpassword.smtp_host', 'localhost'), int(config.get('resetpassword.smtp_port', 0)))
    if config.get('resetpassword.smtp_login'):
        try:
            smtp.starttls()
        except:
            pass
        smtp.login(config.get('resetpassword.smtp_login'), config.get('resetpassword.smtp_passwd'))
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.quit()


def send_email(to_addr, sender, subject, body, rich=None):
    # Using turbomail if it exists, 'dumb' method otherwise
    if turbomail and config.get('mail.on'):
        msg = turbomail.Message(sender, to_addr, subject,  encoding='utf-8')
        msg.plain = body
        if rich:
            msg.rich = rich
        turbomail.enqueue(msg)
    # Using tgext.mailer pluggable if it exists, 'dumb' method otherwise
    elif message:
        mailer = get_mailer(request)
        message_to_send = message(
            subject=subject,
            sender=sender,
            recipients=[to_addr],
            body=body,
            html=rich or None
        )

        if config.get('tm.enabled', False):
            mailer.send(message_to_send)
        else:
            mailer.send_immediately(message_to_send)
    else:
        _plain_send_mail(sender, to_addr, subject, body)
