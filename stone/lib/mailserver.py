#-*- coding: utf-8 -*-

import smtplib
import json
from db import controlador
from os import path
from email.MIMEText import MIMEText
from email.Encoders import encode_base64


def send_mail(name, mail_to, code):
    '''Envia un email a la direccion mail_to con el name y el code de acuerdo
    un mensaje almacenado en la DB usando smtplib'''
    data = controlador.get_configuracion()
    print data
    
    mail_from = data['email']
    mail_pass = data['password']
    
    # Construimos el mensaje simple
    mensaje_crudo = data['mensaje_email']
    mensaje_crudo = mensaje_crudo.replace('<nombre>', name)
    mensaje_crudo = mensaje_crudo.replace('<password>', code)
    mensaje = MIMEText(mensaje_crudo, data['email_type'], data['charset'])
    mensaje['From'] = mail_from
    mensaje['To'] = mail_to
    mensaje['Subject'] = data['asunto']
    # Establecemos conexion con el servidor smtp y enviamos el mensaje
    try:
        smtpserver = smtplib.SMTP(data['smtp'], data['puerto'])
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
