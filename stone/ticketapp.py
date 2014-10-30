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
    '''Ventana Popup para mostrar los mensajes'''
    pass


class PasswordScreen(Screen):
    
    def __init__(self, screen_accept, screen_cancel, name):
    '''Pantalla para cambiar el password actual'''
        self.scr_accept = screen_accept
        self.scr_cancel = screen_cancel
        self.mensaje = StringProperty("")
        self.name = name
        Screen.__init__(self)

    def validar(self, screen):
        '''Valida las entradas y llama al metodo que cambia el password'''
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
                self.manager.current = self.scr_accept
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
        self.manager.current = self.scr_cancel

    def clear(self):
        '''Limpia los campos de texto y libera el teclado virtual'''
        self.ids.old_pass.text = ''
        self.ids.new_pass.text = ''
        self.ids.re_new_pass.text = ''
        Window.release_all_keyboards()

    def cambiar_pass(self, user):
        '''Chequea que el password ingresado sea igual al almacenado y revisa
        que los password nuevos coincidan. Si es así, actualiza el password
        del usuario.'''
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
    '''Pantalla de menu de usuario'''

    def profile(self):
        '''Crea y accede a la pantalla de perfil'''
        self.manager.add_widget(ProfileScreen(name='profile'))
        self.manager.current = 'profile'

    def logout(self):
        '''Cierra la sesion, libera las pantallas que no se van a usar y
        vuelve a la pantalla principal'''
        user_session.close()
        self.manager.remove_widget(self.manager.get_screen('profile'))
        self.manager.remove_widget(self.manager.get_screen('pass'))
        self.manager.current = 'splash'


class ProfileScreen(Screen):

    def __init__(self, name=''):
        '''Pantalla para ver/modificar el perfil del usuario'''
        self.data = {}
        self.name = name
        self.user = user_session.get_user()
        self.cargar_datos()
        Screen.__init__(self)

    def cambiar_pass(self):
        '''Llama a la pantalla de cambiar password'''
        self.manager.add_widget(PasswordScreen('profile', 'profile', 'pass'))

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de perfil'''
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = str(self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['nombre'] = self.user['nombre']
        self.data['lu'] = self.user['lu']
        self.data['email'] = self.user['email']
        self.data['provincia'] = controlador.get_provincia(self.user['id_provincia'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])

    def cancel(self):
        self.manager.current = 'menu'

    def mailvalidator(self, email):
        '''Valida que el mail esté bien formado'''
        if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
            return 1
        return 0

    def validar(self):
        '''Valida las entradas de texto y actualiza el perfil de usuario si
         todo esta bien.'''
        if not self.ids.nombre.text:
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
            self.mensaje = u"Su EMAIL está mal formado.\r\n\r\n Recuerde que este mail se usa\r\n para confirmaciones."
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
            self.mensaje = "Perfil actualizado correctamente"
            WarningPopup().open()
            self.manager.current = 'menu'
        

class SplashScreen(Screen):
    '''Pantalla de acceso - Pantalla principal'''
    pass


class FormScreen(Screen):
    '''Pantalla de registro del sistema'''
    facultades = controlador.get_all_facultades()
    provincias = controlador.get_all_provincias()
    facultades_nombre = sorted(facultades.keys())
    provincias_nombre = sorted(provincias.keys())
    
    def mailvalidator(self, email):
        '''Valida que el mail esté bien formado'''
        if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
            return 1
        return 0

    mensaje = StringProperty("")
    def validar(self):
        '''Valida las entradas de texto y manda a registrar al usuario
        si todo esta bien.'''
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
        '''Limpia los campos de texto y libera el teclado virtual'''
        self.ids.dni.text = ""
        self.ids.nombre.text = ""
        self.ids.lu.text = ""
        self.ids.mail.text = ""
        self.ids.facultad.text = ""
        self.ids.provincia.text = ""
        Window.release_all_keyboards()

    def registrar_usuario(self):
        '''Registra los usuarios de acuerdo a lo ingresado en el formulario.
        Llamando a los metodos insert_usuario y a send_mail'''
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
        data['id_categoria'] = controlador.get_categoria_id('Regular')
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
    '''Pantalla para ingresar al sistema'''
    mensaje = StringProperty("")
    def validar(self):
        '''Valida las entradas y chequea en la base de datos por el par
        dni - password'''
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
                        self.manager.add_widget(PasswordScreen('menu', 'splash', 'pass'))
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
        '''Limpia los campos de texto y libera el teclado virtual'''
        self.ids.dni.text = ""
        self.ids.passw.text = ""
        Window.release_all_keyboards()

    def validar_login(self, dni, password):
        '''Revisa el password de acuerdo al dni ingresado y devuelve los
        siguientes estados:
            0: No existe el dni o no coincide con el password
            1: Existe el usuario y está activo(ingresar)
            2: Existe el usuario pero no confirmó su registro(cambiar pass)
            3: Existe el usuario pero esta inactivo(cancelar ingreso)'''
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
        '''compara el pass ingresado con el pass de la db'''
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
        # Limpiamos la pantalla y le ponemos color blanco
        Window.clearcolor = (1, 1, 1, 1)
        Window.clear()
        # Creamos el screen manager con la WipeTransition
        sm = ScreenManager(transition=WipeTransition())
        # Agregamos las pantallas fijas del sistema
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(FormScreen(name='formulario'))
        sm.add_widget(LoginScreen(name='login'))
        return sm


if __name__ == '__main__':
    TicketApp().run()
