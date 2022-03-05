import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def setup():
    parser = configparser.ConfigParser()
    parser.read("configEmailAlarm.cfg")

    email_user = parser['DEFAULT'].get('USER')
    email_pass = parser['DEFAULT'].get('PASS')
    server_smtp = parser['DEFAULT'].get('SMTP_SERVER')
    server_port = parser['DEFAULT'].getint('SMTP_PORT')
    timeout = parser['DEFAULT'].getfloat('TIMEOUT')

    return email_user, email_pass, server_smtp, server_port, timeout


def setup_and_send(receiver_email='', subject_line='', message_body=''):
    you = receiver_email
    message = message_body
    subject = subject_line
    text = message_body

    email_user, email_pass, server_smtp, server_port, timeout = setup()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = you

    html = f'''<strong>{ message } </strong><br>br<br>'''
    plain_version = MIMEText(text, 'plain')
    html_version = MIMEText(html, 'html')

    msg.attach(plain_version)
    # msg.attach(html_version)

    with smtplib.SMTP_SSL(server_smtp, server_port, timeout=timeout) as server:
        server.set_debuglevel(0)
        to_addrs = [you]
        server.login(email_user, email_pass)
        server.sendmail(email_user, to_addrs, msg.as_string())


def main(receiver_email='', subject_line='', message_body=''):
    if receiver_email:
        setup_and_send(receiver_email, subject_line, message_body)
    else:
        print('receiver_email is False.')


if __name__ == '__main__':
    main()
