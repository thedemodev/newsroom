from flask_mail import Message
from flask import current_app, render_template


def send_email(to, subject, text_body, html_body):
    """
    Sends the email
    :param to: List of recipients
    :param subject: Subject text
    :param text_body: Text Body
    :param html_body: Html Body
    :return:
    """
    msg = Message(subject=subject, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=to)
    msg.body = text_body
    msg.html = html_body
    app = current_app._get_current_object()
    app.mail.send(msg)


def send_validate_account_email(user_name, user_email, token):
    """
    Forms and sends validation email
    :param user_name: Name of the user
    :param user_email: Email address
    :param token: token string
    :return:
    """
    app_name = current_app.config['SITE_NAME']
    url = '{}/validate/{}'.format(current_app.config['CLIENT_URL'], token)
    hours = current_app.config['VALIDATE_ACCOUNT_TOKEN_TIME_TO_LIVE'] * 24

    subject = '{} account created'.format(app_name)
    text_body = render_template('account_created_email.txt', app_name=app_name, name=user_name, expires=hours, url=url)
    html_body = render_template('account_created_email.html', app_name=app_name, name=user_name, expires=hours, url=url)

    send_email(to=[user_email], subject=subject, text_body=text_body, html_body=html_body)


def send_reset_password_email(user_name, user_email, token):
    """
    Forms and sends reset password email
    :param user_name: Name of the user
    :param user_email: Email address
    :param token: token string
    :return:
    """
    app_name = current_app.config['SITE_NAME']
    url = '{}/reset_password/{}'.format(current_app.config['CLIENT_URL'], token)
    hours = current_app.config['RESET_PASSWORD_TOKEN_TIME_TO_LIVE'] * 24

    subject = '{} password reset'.format(app_name)
    text_body = render_template('reset_password_email.txt', app_name=app_name, name=user_name,
                                email=user_email, expires=hours, url=url)
    html_body = render_template('reset_password_email.html', app_name=app_name, name=user_name,
                                email=user_email, expires=hours, url=url)

    send_email(to=[user_email], subject=subject, text_body=text_body, html_body=html_body)