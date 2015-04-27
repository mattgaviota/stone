#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
from hashlib import md5
import random
import urllib2
# funciones útiles para el sistema

def generar_pass(longitud=10):
    '''Genera un password aleatorio de longitud de caracteres'''
    caracteres = "abcdefghijklmnopqrstuvywxzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890#$%&?.-_"
    password = ''.join(random.sample(caracteres, longitud))
    return password

def ofuscar_pass(password):
    '''ofusca el password en md5 para su posterior almacenado'''
    tmp = md5(password).hexdigest()
    code = ''.join(random.sample('abcdefABCDEF0123456789', 8))
    tmp = code[:4] + tmp + code[4:]
    return tmp

def md5_pass(password):
    '''Retorna el md5 hexadecimal del parametro password'''
    return md5(password).hexdigest()

def aclarar_pass(password):
    '''Hace el proceso inverso de ofuscar_pass'''
    return password[4:-4]

def internet_on():
    ''' Chequea la conexión a internet. Devuelve True si hay conexión y
    False en otro caso.'''
    try:
        response=urllib2.urlopen('http://74.125.228.100', timeout=3)
        return True
    except:
        pass
    return False
