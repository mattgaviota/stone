#-*- coding: utf-8 -*-

from md5 import md5
import random
# funciones útiles para el sistema

def generar_pass(longitud=10):
    '''Genera un password aleatorio de longitud de caracteres'''
    caracteres = "abcdefghijklmnopqrstuvywxzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890#$%&?."
    password = ''.join(random.sample(caracteres, longitud))
    return password

def ofuscar_pass(password):
    '''ofusca el password en md5 para su posterior almacenado'''
    tmp = md5(password).hexdigest()
    code = generar_pass(8)
    tmp = code[:4] + tmp + code[4:]
    return tmp

def md5_pass(password):
    '''Retorna el md5 hexadecimal del parametro password'''
    return md5(password).hexdigest()

def aclarar_pass(password):
    '''Hace el proceso inverso de ofuscar_pass'''
    return password[4:-4]
