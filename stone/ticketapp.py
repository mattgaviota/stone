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

    def validar(self):
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
                controlador.insert_log(user, 'perfil')
                user_session.close()
                self.manager.remove_widget(self.manager.get_screen('pass'))
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

    def anular(self):
        '''Crea y accede a la pantalla de anulación de tickets'''
        if not self.manager.has_screen('anular'):
            self.manager.add_widget(AnularScreen(name='anular'))
        self.manager.current = 'anular'

    def profile(self):
        '''Crea y accede a la pantalla de perfil'''
        if not self.manager.has_screen('profile'):
            self.manager.add_widget(ProfileScreen(name='profile'))
        self.manager.current = 'profile'

    def logout(self):
        '''Cierra la sesion, libera las pantallas que no se van a usar y
        vuelve a la pantalla principal'''
        user_session.close()
        try:
            self.manager.remove_widget(self.manager.get_screen('anular'))
            self.manager.remove_widget(self.manager.get_screen('profile'))
            self.manager.remove_widget(self.manager.get_screen('pass'))
        except:
            pass
        self.manager.current = 'splash'


class AnularScreen(Screen):

    def __init__(self, name=''):
        '''Pantalla para anular los tickets del usuario'''
        self.data = {}
        self.name = name
        self.cargar_datos()
        Screen.__init__(self)

    def anular_ticket(self, row):
        id_ticket = self.data[row]['id']
        estado = self.data[row]['estado']
        if id_ticket and estado == 'Activo':
            controlador.anular_ticket(id_ticket)
            controlador.insert_log(self.user, 'anular')
            self.cargar_tickets()
            if row == 'rows0':
                self.ids.estado0.text = 'Anulado'
            elif row == 'rows1':
                self.ids.estado1.text = 'Anulado'
            elif row == 'rows2':
                self.ids.estado2.text = 'Anulado'
            elif row == 'rows3':
                self.ids.estado3.text = 'Anulado'
            else:
                self.ids.estado4.text = 'Anulado'
        
    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de anulación'''
        self.user = user_session.get_user()
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = str(self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.cargar_tickets()
        
    def cargar_tickets(self):    
        self.tickets = controlador.get_tickets(self.user)
        ticket_vacio = {'fecha': '', 'importe': '', 'estado': '', 'id': 0}
        i = 0
        for ticket in self.tickets:
            if ticket['estado']:
                ticket['estado'] = 'Activo'
            else:
                ticket['estado'] = 'Anulado'
            ticket['importe'] = '$%.2f' %(ticket['importe'])
            ticket['fecha'] = ticket['fecha'].strftime('%Y-%m-%d')
            self.data['rows%s' % (i)] = ticket
            i += 1
        faltantes = 5 - len(self.tickets)
        if faltantes:
            if faltantes == 1:
                self.data['rows4'] = ticket_vacio
            elif faltantes == 2:
                self.data['rows3'] = ticket_vacio
                self.data['rows4'] = ticket_vacio
            elif faltantes == 3:
                self.data['rows2'] = ticket_vacio
                self.data['rows3'] = ticket_vacio
                self.data['rows4'] = ticket_vacio
            elif faltantes == 4:
                self.data['rows1'] = ticket_vacio
                self.data['rows2'] = ticket_vacio
                self.data['rows3'] = ticket_vacio
                self.data['rows4'] = ticket_vacio
            else:
                self.data['rows0'] = ticket_vacio
                self.data['rows1'] = ticket_vacio
                self.data['rows2'] = ticket_vacio
                self.data['rows3'] = ticket_vacio
                self.data['rows4'] = ticket_vacio
            
    def cancel(self):
        self.manager.current = 'menu'


class ProfileScreen(Screen):

    def __init__(self, name=''):
        '''Pantalla para ver/modificar el perfil del usuario'''
        self.data = {}
        self.name = name
        self.facultades = controlador.get_all_facultades()
        self.provincias = controlador.get_all_provincias()
        self.cargar_datos()
        Screen.__init__(self)

    def cambiar_pass(self):
        '''Llama a la pantalla de cambiar password'''
        if not self.manager.has_screen('pass'):
            self.manager.add_widget(PasswordScreen('profile', 'profile', 'pass'))
        self.manager.current = 'pass'
        self.update_datos()

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de perfil'''
        self.user = user_session.get_user()
        self.facultades_nombre = sorted(self.facultades.keys())
        self.provincias_nombre = sorted(self.provincias.keys())
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = str(self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['nombre'] = self.user['nombre']
        self.data['lu'] = self.user['lu']
        self.data['email'] = self.user['email']
        self.data['provincia'] = controlador.get_provincia(self.user['id_provincia'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])

    def update_datos(self):
        self.ids.nombre.text = self.data['nombre']
        self.ids.lu.text = self.data['lu']
        self.ids.email.text = self.data['email']
        self.ids.facultad.text = self.data['facultad']
        self.ids.provincia.text = self.data['provincia']

    def update_profile(self):
        self.updata = {}
        self.updata['nombre'] = self.ids.nombre.text
        self.updata['lu'] = self.ids.lu.text
        self.updata['email'] = self.ids.email.text
        self.updata['id_provincia'] = self.provincias[self.ids.provincia.text]
        self.updata['id_facultad'] = self.facultades[self.ids.facultad.text]
        controlador.update_usuario(self.user, self.updata)
        controlador.insert_log(self.user, 'perfil')
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()

    def cancel(self):
        self.update_datos()
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
        elif not self.ids.email.text:
            self.mensaje = u"Su EMAIL no puede estar vacío"
            self.ids.email.focus = True
            WarningPopup().open()
        elif not self.mailvalidator(self.ids.email.text):
            self.mensaje = u"Su EMAIL está mal formado.\r\n\r\n Recuerde que este mail se usa\r\n para confirmaciones."
            self.ids.email.text = ""
            self.ids.email.focus = True
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
            update_thread = Thread(target=self.update_profile())
            update_thread.start()
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
        else:
            self.mensaje = "Ya existe un usario con ese DNI"
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
                        self.manager.add_widget(PasswordScreen('splash', 'splash', 'pass'))
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
