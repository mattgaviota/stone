#-*- coding: utf-8 -*-

import smtplib
import json
from os import path
from email.MIMEText import MIMEText
from email.Encoders import encode_base64


def send_mail(name, mail_to, code):
    # Cargamos el archivo de configuración
    file_path = path.join(path.split(path.abspath(path.dirname(__file__)))[0],
                'conf/mail.json')
    with open(file_path) as data_file:    
        data = json.load(data_file)

    mail_from = data['mail_from']
    mail_pass = data['pass']
    
    # Construimos el mensaje simple
    mensaje = MIMEText(data['message'] % (name, code), 'html', 'utf-8')
    mensaje['From'] = mail_from
    mensaje['To'] = mail_to
    mensaje['Subject'] = data['subject']
    # Establecemos conexion con el servidor smtp de gmail y enviamos el mensaje
    try:
        smtpserver = smtplib.SMTP(data['google_smtp'], data['port'])
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(mail_from, mail_pass)

        smtpserver.sendmail(mail_from, mail_to, mensaje.as_string())         
        smtpserver.close()
        return 1
    except Exception as e:
        print str(e)
        return 0
