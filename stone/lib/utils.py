#-*- coding: utf-8 -*-

from md5 import md5
import random
# funciones útiles

def generar_pass(longitud=10):
    caracteres = "abcdefghijklmnopqrstuvywxzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890#$%&?."
    password = ''.join(random.sample(caracteres, longitud))
    return password

def ofuscar_pass(password):
    tmp = md5(password).hexdigest()
    code = generar_pass(8)
    tmp = code[:4] + tmp + code[4:]
    return tmp

def md5_pass(password):
    return md5(password).hexdigest()

def aclarar_pass(password):
    return password[4:-4]
