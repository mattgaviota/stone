# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from time import time
from lib import utils
from db import controlador
from src.settings import user_session, UNIDAD
from src.alerts import WarningPopup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


class BloqueoScreen(Screen):

    def validar(self):
        """Valida las entradas y chequea en la base de datos por el par
        dni - password"""
        if self.ids.dni.text:
            if not self.ids.dni.text.isdigit():
                self.ids.dni.text = ""
                self.ids.dni.focus = True
                mensaje = u"Su DNI solo puede contenter números"
                WarningPopup(mensaje).open()
            elif len(self.ids.dni.text) >= 10:
                mensaje = u"\rSu DNI no puede tener\r\n más de 10 caracteres."
                self.ids.dni.focus = True
                WarningPopup(mensaje).open()
            elif not self.ids.passw.text:
                mensaje = u"Su PASSWORD no puede estar vacío"
                self.ids.passw.focus = True
                WarningPopup(mensaje).open()
            elif len(self.ids.passw.text) >= 64:
                mensaje = u"\rSu PASSWORD no puede tener\r\n"
                mensaje += u"más de 64 caracteres."
                self.ids.passw.focus = True
                WarningPopup(mensaje).open()
            else:
                dni = self.ids.dni.text
                password = self.ids.passw.text
                login = self.validar_login(dni, password)
                if login:
                    self.clear()
                    user_session.init(controlador.get_usuario(dni), time())
                    user = user_session.get_user()
                    controlador.insert_log(
                        user,
                        'ingresar',
                        UNIDAD,
                        'control - desbloqueo'
                    )
                    self.manager.current = 'menu_control'
                    self.manager.remove_widget(
                        self.manager.get_screen('bloqueo')
                    )
                else:
                    self.ids.passw.text = ""
                    mensaje = u"DNI o PASSWORD incorrecto"
                    WarningPopup(mensaje).open()
        else:
            mensaje = u"Su DNI no puede estar vacío"
            self.ids.dni.focus = True
            WarningPopup(mensaje).open()

    def validar_login(self, dni, password):
        """Revisa el password de acuerdo al dni ingresado y devuelve los
        siguientes estados:
            0: No existe el dni o no coincide con el password
            1: Existe el usuario pero no confirmó su registro(cambiar pass)
            2: Existe el usuario y está registrado(ingresar)
            3: Existe el usuario pero esta suspendido(cancelar ingreso)
            6: Existe el usuario y es de control(pantalla de control)"""
        user = controlador.get_usuario(dni)
        if user:
            if self.comparar_pass(password, user):
                if user['id_perfil'] in [3, 5]:  # usuario administrativo
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0

    def comparar_pass(self, password, user):
        """compara el pass ingresado con el pass de la db"""
        pass_ingresado = utils.md5_pass(password)
        pass_db = utils.aclarar_pass(user['password'])  # control interno
        if pass_ingresado == pass_db:
            return 1
        else:
            return 0

    def clear(self):
        """Limpia los campos de texto y libera el teclado virtual"""
        self.ids.dni.text = ""
        self.ids.passw.text = ""
        Window.release_all_keyboards()
