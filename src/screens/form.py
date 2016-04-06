# -*- coding: utf-8 -*-
"""Modulo para registrar usuarios. Con su pantalla correspondiente"""
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
import re
from threading import Thread
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from db import controlador
from lib import mailserver, utils
from src.alerts import WarningPopup
from src.settings import UNIDAD


def mailvalidator(email):
    """Valida que el mail esté bien formado"""
    if re.match(
            "^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$",
            email
    ) is not None:
        return 1
    return 0


def chequear_alumno(libu, dni):
    """
    Chequea los datos ingresados para ver que correspondan con un alumno.
    Retorna 1 -> Si los datos están bien y tiene 2 o más materias.
    Retorna 2 -> Si los datos están bien pero no tiene 2 o más materias.
    Retorna 0 -> Si los datos no se corresponden con un alumno.
    """
    id_alumno = controlador.get_alumno(libu, dni)
    if id_alumno:
        if controlador.get_materias(id_alumno) >= 2:
            return 1
        else:
            return 2
    else:
        return 0


class FormScreen(Screen):
    """Pantalla de registro del sistema"""

    def __init__(self, **kwargs):
        self.facultades = controlador.get_all_facultades()
        self.provincias = controlador.get_all_provincias()
        self.facultades_nombre = sorted(self.facultades.keys())
        self.provincias_nombre = sorted(self.provincias.keys())
        self.datos = {}
        self.datos['aside'] = controlador.get_images('aside')
        self.datos['footer'] = controlador.get_images('footer')

        super(FormScreen, self).__init__(**kwargs)
        self.ids.provincia.text = 'Salta'

    def validar(self):
        """Valida las entradas de texto y manda a registrar al usuario
        si todo esta bien."""
        if self.ids.dni.text:
            if not self.ids.dni.text.isdigit():
                mensaje = u"Su DNI solo puede contenter números"
                self.ids.dni.text = ""
                self.ids.dni.focus = True
                WarningPopup(mensaje).open()
            elif len(self.ids.dni.text) >= 10:
                mensaje = u"\rSu DNI no puede tener\r\n más de 10 caracteres."
                self.ids.dni.text = ""
                self.ids.dni.focus = True
                WarningPopup(mensaje).open()
            elif not self.ids.nombre.text:
                mensaje = u"Su NOMBRE no puede estar vacío"
                self.ids.nombre.focus = True
                WarningPopup(mensaje).open()
            elif len(self.ids.nombre.text) >= 45:
                msje = u"\rSu NOMBRE no puede tener\r\n más de 45 caracteres."
                self.ids.nombre.text = ""
                self.ids.nombre.focus = True
                WarningPopup(msje).open()
            elif not self.ids.lu.text:
                mensaje = u"Su LU no puede estar vacía"
                self.ids.lu.focus = True
                WarningPopup(mensaje).open()
            elif not self.ids.lu.text.isdigit():
                mensaje = u"Su LU solo puede contenter números"
                self.ids.lu.text = ""
                self.ids.lu.focus = True
                WarningPopup(mensaje).open()
            elif len(self.ids.lu.text) >= 8:
                mensaje = u"\rSu LU no puede tener\r\n más de 8 caracteres."
                self.ids.lu.text = ""
                self.ids.lu.focus = True
                WarningPopup(mensaje).open()
            elif not self.ids.mail.text:
                mensaje = u"Su EMAIL no puede estar vacío"
                self.ids.mail.focus = True
                WarningPopup(mensaje).open()
            elif len(self.ids.mail.text) >= 64:
                msje = u"\rSu EMAIL no puede tener\r\n más de 64 caracteres."
                self.ids.mail.text = ""
                self.ids.mail.focus = True
                WarningPopup(msje).open()
            elif not mailvalidator(self.ids.mail.text):
                mensaje = u"\rSu EMAIL está mal formado.\r\n Recuerde que este"
                mensaje += u" mail se usará\r\n para confirmar su registro."
                self.ids.mail.text = ""
                self.ids.mail.focus = True
                WarningPopup(mensaje).open()
            elif not self.ids.facultad.text:
                mensaje = u"Debe especificar una FACULTAD"
                WarningPopup(mensaje).open()
            elif not self.ids.provincia.text:
                mensaje = u"Debe especificar una PROVINCIA"
                WarningPopup(mensaje).open()
            else:
                if utils.internet_on():
                    chequeo = chequear_alumno(
                        self.ids.lu.text, self.ids.dni.text
                    )
                    if chequeo == 1:
                        self.registrar_usuario()
                        self.clear()
                        self.manager.current = 'splash'
                    elif chequeo == 2:
                        self.registrar_usuario(0)
                        self.clear()
                        self.manager.current = 'splash'
                    else:
                        mensaje = u"Su DNI o LU es incorrecto"
                        WarningPopup(mensaje).open()
                else:
                    msje = u"\rInternet no disponible\r\n Intente más tarde."
                    WarningPopup(msje).open()
        else:
            mensaje = u"Su DNI no puede estar vacío"
            self.ids.dni.focus = True
            WarningPopup(mensaje).open()

    def clear(self):
        """Limpia los campos de texto y libera el teclado virtual"""
        self.ids.dni.text = ""
        self.ids.nombre.text = ""
        self.ids.lu.text = ""
        self.ids.mail.text = ""
        self.ids.facultad.text = ""
        self.ids.provincia.text = ""
        Window.release_all_keyboards()

    def registrar_usuario(self, estado=1):
        """Registra los usuarios de acuerdo a lo ingresado en el formulario.
        Llamando a los metodos insert_usuario y a send_mail"""
        user = controlador.get_usuario(self.ids.dni.text)
        if not user:
            data = {}
            data['dni'] = self.ids.dni.text
            data['nombre'] = self.ids.nombre.text
            data['lu'] = self.ids.lu.text
            data['email'] = self.ids.mail.text
            data['id_facultad'] = self.facultades[self.ids.facultad.text]
            data['id_provincia'] = self.provincias[self.ids.provincia.text]
            password = utils.generar_pass()
            data['password'] = utils.ofuscar_pass(password)
            data['estado'] = estado  # 0 bloqueado / 1 registrado
            data['id_perfil'] = controlador.get_perfil('Alumno')
            data['id_categoria'] = controlador.get_categoria_id('Regular')
            # insertamos el usuario en la db
            controlador.insert_usuario(data, UNIDAD)
            # Enviamos el mail de confirmación
            datos_mail = controlador.get_configuracion()
            mail_thread = Thread(
                target=mailserver.send_mail,
                args=(data['nombre'], data['email'], password, datos_mail)
            )
            mail_thread.start()
            mensaje = "\rGracias por registrarte!!\r\n\r\n"
            mensaje += "Comprueba tu mail\r\n para completar el registro"
            WarningPopup(mensaje).open()
        else:
            mensaje = "Ya existe un usario con ese DNI"
            WarningPopup(mensaje).open()

    def cancel(self):
        """Vuelve a la pantalla anterior."""
        self.clear()
        self.manager.current = 'splash'
