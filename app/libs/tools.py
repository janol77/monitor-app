# -*- coding: utf-8 -*-
"""Tools file."""
from flask import current_app
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import string
import random


mails = [{
    'subject': 'SMTP HTML e-mail test',
    'message': 'Test Email'},
    {'subject': u'Confirmaci&oacute;n de Correo',
     'message': u"""
Confirme el correo en el siguiente link para activar la cuenta
<a href="%s">%s</a>
"""}
]


def sendmail(receivers=[], _type=0, url=None, code=None, _id=None):
    """Send email using postfix."""
    target = current_app.config["SMTPTARGET"]
    smtpsender = current_app.config["SMTPDEFAULTSENDER"]
    subject = mails[_type]['subject']
    message = mails[_type]['message']
    if not receivers:
        return False
    receivers_list = []
    r_text = []
    for r in receivers:
        r_text.append("%s <%s>" % (r['name'], r['email']))
        receivers_list.append(r['email'])
    receivers_text = ','.join(r_text)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = "Openvita.com <mail>"
    msg['To'] = receivers_text
    text = "SMTP HTML e-mail test"
    html = text
    if _type == 1:
        url = url_generator(code=code, url=url, _id=_id)
        text = "Confirmation link %s" % (url)
        html = message % (url, url)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    try:
        smtpobj = smtplib.SMTP(target)
        smtpobj.sendmail(smtpsender, receivers_list, msg.as_string())
        return True
    except smtplib.SMTPException:
        print "Error: unable to send email."


def code_generator(size=30, hexdigits=True):
    """Generar codigo aleatorio."""
    chars = string.digits
    if hexdigits:
        chars = string.hexdigits
    return ''.join(random.choice(chars) for _ in range(size))


def url_generator(code=None, _id=None, url=None):
    """Url Generator."""
    if url is None or code is None or _id is None:
        return "http://www.openvita.com"
    path = '/user/%s/activate/%s' % (_id, code)
    return url + path
