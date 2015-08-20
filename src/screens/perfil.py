# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
import re
from db import controlador
from src.settings import user_session, UNIDAD
from src.alerts import WarningPopup
from password import PasswordScreen
from kivy.uix.screenmanager import Screen


class ProfileScreen(Screen):

    def __init__(self, **kwargs):
        """Pantalla para ver/modificar el perfil del usuario"""
        self.data = {}
        self.provincias = controlador.get_all_provincias()
        self.cargar_datos()
        super(ProfileScreen, self).__init__(**kwargs)

    def cambiar_pass(self):
        """Llama a la pantalla de cambiar password"""
        if not self.manager.has_screen('pass'):
            self.manager.add_widget(
                PasswordScreen('profile', 'profile', 'pass')
            )
        self.manager.current = 'pass'

    def cargar_datos(self):
        """Carga los datos del usuario dentro de la pantalla de perfil"""
        try:
            user_session.update(controlador.get_usuario(self.data['dni']))
            self.user = user_session.get_user()
        except KeyError:
            self.user = user_session.get_user()
        self.provincias_nombre = sorted(self.provincias.keys())
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$ %.0f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(
                                                    self.user['id_categoria'])
        self.data['nombre'] = self.user['nombre']
        self.data['email'] = self.user['email']
        self.data['provincia'] = controlador.get_provincia(
                                                    self.user['id_provincia'])
        self.data['facultad'] = controlador.get_facultad(
                                                    self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']

    def update_datos(self):
        """Actualiza los datos de la pantalla para plasmar cambios"""
        self.cargar_datos()
        self.ids.nombre.text = self.data['nombre']
        self.ids.email.text = self.data['email']
        self.ids.provincia.text = self.data['provincia']
        self.ids.saldo.text = self.data['saldo']

    def update_profile(self):
        """Actualiza el perfil con los cambios realizados por el usuario"""
        self.updata = {}
        self.updata['nombre'] = self.ids.nombre.text
        self.updata['email'] = self.ids.email.text
        self.updata['id_provincia'] = self.provincias[self.ids.provincia.text]
        controlador.update_usuario(self.user, self.updata)
        controlador.insert_log(self.user, 'perfil', UNIDAD)
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()

    def cancel(self):
        """Vuelve a la pantalla anterior"""
        self.manager.current = 'opciones'

    def mailvalidator(self, email):
        """Valida que el mail esté bien formado"""
        if re.match(
            "^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$",
            email
        ) != None:
            return 1
        return 0

    def validar(self):
        """Valida las entradas de texto y actualiza el perfil de usuario si
         todo esta bien."""
        if not self.ids.nombre.text:
            mensaje = u"Su NOMBRE no puede estar vacío"
            self.ids.nombre.focus = True
            WarningPopup(mensaje).open()
        elif len(self.ids.nombre.text) >= 45:
            mensaje = u"\rSu NOMBRE no puede tener\r\n más de 45 caracteres."
            self.ids.nombre.text = ""
            self.ids.nombre.focus = True
            WarningPopup(mensaje).open()
        elif not self.ids.email.text:
            mensaje = u"Su EMAIL no puede estar vacío"
            self.ids.email.focus = True
            WarningPopup(mensaje).open()
        elif len(self.ids.email.text) >= 64:
            mensaje = u"\rSu EMAIL no puede tener\r\n más de 64 caracteres."
            self.ids.email.text = ""
            self.ids.email.focus = True
            WarningPopup(mensaje).open()
        elif not self.mailvalidator(self.ids.email.text):
            mensaje = u"Su EMAIL está mal formado."
            self.ids.email.text = ""
            self.ids.email.focus = True
            WarningPopup(mensaje).open()
        elif not self.ids.provincia.text:
            mensaje = u"Debe especificar una PROVINCIA"
            WarningPopup(mensaje).open()
        else:
            mensaje = "Perfil actualizado correctamente"
            WarningPopup(mensaje).open()
            self.update_profile()
            self.manager.current = 'opciones'
