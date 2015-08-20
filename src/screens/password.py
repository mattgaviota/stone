#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from lib import utils
from db import controlador
from src.settings import user_session, UNIDAD
from src.alerts import WarningPopup
from kivy.uix.screenmanager import Screen


class PasswordScreen(Screen):

    def __init__(self, screen_accept, screen_cancel, name):
        """Pantalla para cambiar el password actual"""
        self.scr_accept = screen_accept
        self.scr_cancel = screen_cancel
        self.data = {}
        self.data['fondo'] = controlador.get_images('fondo')
        self.data['aside'] = controlador.get_images('aside')
        self.data['footer'] = controlador.get_images('footer')
        self.cargar_datos()
        self.name = name
        Screen.__init__(self)

    def cargar_datos(self):
        """Carga los datos del usuario dentro de la pantalla de anulación"""
        try:
            user_session.update(controlador.get_usuario(self.data['dni']))
            self.user = user_session.get_user()
        except KeyError:
            self.user = user_session.get_user()
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$ %.0f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(
                                                    self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(
                                                    self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']

    def validar(self):
        """Valida las entradas y llama al metodo que cambia el password"""
        if not self.ids.old_pass.text:
            mensaje = u"Debe ingresar el password actual"
            self.ids.old_pass.focus = True
            WarningPopup(mensaje).open()
        elif not self.ids.new_pass.text:
            mensaje = u"Debe ingresar el password nuevo"
            self.ids.new_pass.focus = True
            WarningPopup(mensaje).open()
        elif not self.ids.re_new_pass.text:
            mensaje = u"Debe repetir el password nuevo"
            self.ids.re_new_pass.focus = True
            WarningPopup(mensaje).open()
        else:
            user = user_session.get_user()
            response = self.cambiar_pass(user)
            if response == 1:
                mensaje = u"Su password se actualizo correctamente"
                WarningPopup(mensaje).open()
                self.clear()
                self.manager.current = self.scr_accept
                if self.scr_accept == 'profile':
                    controlador.insert_log(user, 'perfil', UNIDAD)
                user_session.close()
                self.manager.remove_widget(self.manager.get_screen('pass'))
            elif response == 2:
                mensaje = u"\rEL password actual\r\n no coincide con el almacenado"
                WarningPopup(mensaje).open()
                self.clear()
            elif response == 3:
                mensaje = u"\rEl password actual\r\n no debe superar los 15 caracteres\r\n y no puede contener símbolos extraños."
                WarningPopup(mensaje).open()
                self.clear()
            else:
                mensaje = u"El password nuevo no coincide"
                WarningPopup(mensaje).open()
                self.clear()


    def cancel(self):
        """
        Limpia los campos y regresa a la pantalla scr_cancel.
        Si el usuario no esta activo cierra la sesión.
        """
        self.clear()
        user = user_session.get_user()
        if user['estado'] == 1:
            user_session.close()
        self.manager.current = self.scr_cancel

    def clear(self):
        """Limpia los campos de texto y libera el teclado virtual"""
        self.ids.old_pass.text = ''
        self.ids.new_pass.text = ''
        self.ids.re_new_pass.text = ''
        self.ids.old_pass.focus = True
        Window.release_all_keyboards()

    def check_pass(self, new_pass):
        """
        Chequea que los caracteres de la contraseña esten dentro del grupo y
        que la longitud no exceda los 15 caracteres.
        """
        caracteres = "abcdefghijklmnopqrstuvywxzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890#$%&?.-_"
        if len(new_pass) <= 64:
            for char in new_pass:
                if char not in caracteres:
                    return 0
            return 1
        else:
            return 0

    def cambiar_pass(self, user):
        """Chequea que el password ingresado sea igual al almacenado y revisa
        que los password nuevos coincidan. Si es así, actualiza el password
        del usuario."""
        old_pass = utils.md5_pass(self.ids.old_pass.text)
        pass_db = user['password']
        pass_db = pass_db[4:-4] # control interno
        new_pass = self.ids.new_pass.text
        re_new_pass = self.ids.re_new_pass.text
        if self.check_pass(new_pass):
            if new_pass == re_new_pass:
                if pass_db == old_pass:
                    tmp = utils.ofuscar_pass(new_pass)
                    controlador.update_pass(user, tmp)
                    if user['estado'] == 1: # si no está activo se lo activa
                        controlador.update_estado(user, 2)
                    return 1
                else:
                    return 2
            else:
                return 0
        else:
            return 3
