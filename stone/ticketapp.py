#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Utility import
import re
from threading import Thread
# intra-packages imports
from db import controlador
from lib import mailserver, session, utils
# Kivy related imports
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

#session
user_session = session.Session()


class WarningPopup(Popup):
    pass


class PasswordScreen(Screen):

    mensaje = StringProperty("")

    def validar(self):
        if not self.ids.old_pass.text:
            self.mensaje = u"Debe ingresar el password actual"
            self.ids.old_pass.focus = True
            WarningPopup().open()
        elif not self.ids.new_pass.text:
            self.mensaje = u"Debe ingresar el password nuevo"
            self.ids.new_pass.focus = True
            WarningPopup().open()
        elif not self.ids.re_new_pass.text:
            self.mensaje = u"Debe repetir el password nuevo"
            self.ids.re_new_pass.focus = True
            WarningPopup().open()
        else:
            user = user_session.get_user()
            response = self.cambiar_pass(user)
            if response == 1:
                self.mensaje = u"Su password se actualizo correctamente"
                WarningPopup().open()
                self.clear()
                self.manager.current = 'menu'
            elif response == 2:
                self.mensaje = u"EL password actual\r\n no coincide con el almacenado"
                WarningPopup().open()
                self.clear()
            else:
                self.mensaje = u"El password nuevo no coincide"
                WarningPopup().open()
                self.clear()

    def cancel(self):
        self.clear()
        user_session.close()
        self.manager.current = 'splash'

    def clear(self):
        self.ids.old_pass.text = ''
        self.ids.new_pass.text = ''
        self.ids.re_new_pass.text = ''
        Window.release_all_keyboards()

    def cambiar_pass(self, user):
        old_pass = utils.md5_pass(self.ids.old_pass.text)
        pass_db = user['password']
        pass_db = pass_db[4:-4] # control interno
        new_pass = self.ids.new_pass.text
        re_new_pass = self.ids.re_new_pass.text
        if new_pass == re_new_pass:
            if pass_db == old_pass:
                tmp = utils.ofuscar_pass(new_pass)
                controlador.update_pass(user, tmp)
                if user['estado'] != 1:
                    controlador.update_estado(user, 1)
                return 1
            else:
                return 2
        else:
            return 0


class MenuScreen(Screen):

    def logout(self):
        user_session.close()
        self.manager.current = 'splash'


class SplashScreen(Screen):
    pass


class FormScreen(Screen):

    facultades = controlador.get_all_facultades()
    provincias = controlador.get_all_provincias()
    facultades_nombre = sorted(facultades.keys())
    provincias_nombre = sorted(provincias.keys())
    
    def mailvalidator(self, email):
        if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
            return 1
        return 0

    mensaje = StringProperty("")
    def validar(self):
        if self.ids.dni.text:
            if not self.ids.dni.text.isdigit():
                self.mensaje = u"Su DNI solo puede contenter números"
                self.ids.dni.text = ""
                self.ids.dni.focus = True
                WarningPopup().open()
            elif not self.ids.nombre.text:
                self.mensaje = u"Su NOMBRE no puede estar vacío"
                self.ids.nombre.focus = True
                WarningPopup().open()
            elif not self.ids.lu.text:
                self.mensaje = u"Su LU no puede estar vacía"
                self.ids.lu.focus = True
                WarningPopup().open()
            elif not self.ids.lu.text.isdigit():
                self.mensaje = u"Su LU solo puede contenter números"
                self.ids.lu.text = ""
                self.ids.lu.focus = True
                WarningPopup().open()
            elif not self.ids.mail.text:
                self.mensaje = u"Su EMAIL no puede estar vacío"
                self.ids.mail.focus = True
                WarningPopup().open()
            elif not self.mailvalidator(self.ids.mail.text):
                self.mensaje = u"Su EMAIL está mal formado.\r\n\r\n Recuerde que este mail se usará\r\n para confirmar su registro."
                self.ids.mail.text = ""
                self.ids.mail.focus = True
                WarningPopup().open()
            elif not self.ids.facultad.text:
                self.mensaje = u"Debe especificar una FACULTAD"
                WarningPopup().open()
            elif not self.ids.provincia.text:
                self.mensaje = u"Debe especificar una PROVINCIA"
                WarningPopup().open()
            else:
                self.registrar_usuario()
                self.clear()
                self.manager.current = 'splash'
        else:
            self.mensaje = u"Su DNI no puede estar vacío"
            self.ids.dni.focus = True
            WarningPopup().open()

    def clear(self):
        self.ids.dni.text = ""
        self.ids.nombre.text = ""
        self.ids.lu.text = ""
        self.ids.mail.text = ""
        self.ids.facultad.text = ""
        self.ids.provincia.text = ""
        Window.release_all_keyboards()

    def registrar_usuario(self):
        data = {}
        data['dni'] = self.ids.dni.text
        data['nombre'] = self.ids.nombre.text
        data['lu'] = self.ids.lu.text
        data['email'] = self.ids.mail.text
        data['id_facultad'] = self.facultades[self.ids.facultad.text]
        data['id_provincia'] = self.provincias[self.ids.provincia.text]
        password = utils.generar_pass()
        data['password'] = utils.ofuscar_pass(password)
        data['estado'] = 2
        data['id_perfil'] = controlador.get_perfil('Alumno')
        data['id_categoria'] = controlador.get_categoria('Regular')
        # insertamos el usuario en la db
        db_thread = Thread(target=controlador.insert_usuario, args=(data,))
        db_thread.start()
        # Enviamos el mail de confirmación
        mail_thread = Thread(target=mailserver.send_mail, args=(data['nombre'], data['email'], password))
        mail_thread.start()
        self.mensaje = "Gracias por registrarte!!\r\n\r\n Comprueba tu mail\r\n para completar el registro"
        WarningPopup().open()

    def cancel(self):
        self.clear()
        self.manager.current = 'splash'


class LoginScreen(Screen):
    
    mensaje = StringProperty("")
    def validar(self):
        if self.ids.dni.text:
            if not self.ids.dni.text.isdigit():
                self.mensaje = u"Su DNI solo puede contenter números"
                WarningPopup().open()
                self.ids.dni.text = ""
                self.ids.dni.focus = True
            elif not self.ids.passw.text:
                self.mensaje = u"Su PASSWORD no puede estar vacío"
                self.ids.passw.focus = True
                WarningPopup().open()
            else:
                dni = self.ids.dni.text
                password = self.ids.passw.text
                login = self.validar_login(dni, password)
                if login:
                    if login == 1:
                        self.clear()
                        user_session.init(controlador.get_usuario(dni))
                        self.manager.current = 'menu'
                    elif login == 2:
                        self.clear()
                        user_session.init(controlador.get_usuario(dni))
                        self.manager.current = 'pass'
                    else:
                        self.clear()
                        self.mensaje = u"Su cuenta esta inactiva\r\n Contacte a un administrador"
                        WarningPopup().open()
                else:
                    self.clear()
                    self.mensaje = u"DNI o PASSWORD incorrecto"
                    WarningPopup().open()
        else:
            self.mensaje = u"Su DNI no puede estar vacío"
            self.ids.dni.focus = True
            WarningPopup().open()

    def clear(self):
        self.ids.dni.text = ""
        self.ids.passw.text = ""
        Window.release_all_keyboards()

    def validar_login(self, dni, password):
        user = controlador.get_usuario(dni)
        if user:
            if self.comparar_pass(password, user):
                if user['estado'] == 2: # estado wait / login & cambiar pass
                    return 2
                elif user['estado'] == 1: # estado activo / login & menu
                    return 1
                else: # estado inactivo / cancel
                    return 3
            else:
                return 0
        else:
            return 0

    def comparar_pass(self, password, user):
        pass_ingresado = utils.md5_pass(password)
        pass_db = utils.aclarar_pass(user['password']) # control interno
        if pass_ingresado == pass_db:
            return 1
        else:
            return 0

    def cancel(self):
        self.clear()
        self.manager.current = 'splash'

class TicketApp(App):

    def build(self):
        # Create the screen manager
        Window.clearcolor = (1, 1, 1, 1)
        Window.clear()
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(FormScreen(name='formulario'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(PasswordScreen(name='pass'))
        return sm


if __name__ == '__main__':
    TicketApp().run()
