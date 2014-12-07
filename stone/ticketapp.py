#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Utility import
import re
from threading import Thread, Event
from Queue import Queue, Empty
from datetime import datetime
from time import mktime, localtime, sleep
# intra-packages imports
from db import controlador
from lib import mailserver, session, utils, impresora, billetes
# Kivy related imports
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock, mainthread


#session
user_session = session.Session()


class ConfirmPopup(GridLayout):
    text = StringProperty()

    def __init__(self,**kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup,self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


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
                if self.scr_accept == 'profile':
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

    def options(self):
        '''Crea y accede a la pantalla de opciones'''
        if not self.manager.has_screen('opciones'):
            self.manager.add_widget(OptionScreen(name='opciones'))
        self.manager.current = 'opciones'

    def comprar(self):
        '''Crea y accede a la pantalla de compra de tickets'''
        if not self.manager.has_screen('compra_1'):
            self.manager.add_widget(Compra1Screen(name='compra_1'))
        self.manager.current = 'compra_1'

    def logout(self):
        '''Cierra la sesion, libera las pantallas que no se van a usar y
        vuelve a la pantalla principal'''
        user_session.close()
        if self.manager.has_screen('opciones'):
            self.manager.remove_widget(self.manager.get_screen('opciones'))
        if self.manager.has_screen('compra_1'):
            self.manager.remove_widget(self.manager.get_screen('compra_1'))
        if self.manager.has_screen('compra_2'):
            self.manager.remove_widget(self.manager.get_screen('compra_2'))

        self.manager.current = 'splash'


class OptionScreen(Screen):
    '''Pantalla de menu de usuario'''

    def anular(self):
        '''Crea y accede a la pantalla de anulación de tickets'''
        if not self.manager.has_screen('anular'):
            self.manager.add_widget(AnularScreen(name='anular'))
        self.manager.current = 'anular'

    def cargar(self):
        '''Crea y accede a la pantalla de carga de saldo'''
        self.user = user_session.get_user()
        if self.user['saldo'] >= 100:
            self.mensaje = "No puede cargar más de $ 100"
            WarningPopup().open()
        else:
            if not self.manager.has_screen('carga'):
                self.manager.add_widget(CargaScreen(name='carga'))
            self.manager.current = 'carga'
    def perfil(self):
        '''Crea y accede a la pantalla de perfil'''
        if not self.manager.has_screen('profile'):
            self.manager.add_widget(ProfileScreen(name='profile'))
        self.manager.current = 'profile'

    def cancel(self):
        '''Vuelve a la pantalla anterior'''
        if self.manager.has_screen('anular'):
            self.manager.remove_widget(self.manager.get_screen('anular'))
        if self.manager.has_screen('profile'):
            self.manager.remove_widget(self.manager.get_screen('profile'))
        if self.manager.has_screen('pass'):
            self.manager.remove_widget(self.manager.get_screen('pass'))
        self.manager.current = 'menu'


class Compra1Screen(Screen):

    def __init__(self, name=''):
        '''Pantalla para elegir los días de compra de tickets'''
        self.data = {}
        self.name = name
        self.cargar_datos()
        self.mensaje = StringProperty("")
        Screen.__init__(self)

    def update_datos(self):
        '''Actualiza los datos de la pantalla para plasmar cambios'''
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']
        self.ids.desde.text = self.data['dia']
        self.ids.hasta.text = ''

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de compra'''
        self.user = user_session.get_user()
        self.dias_desde = controlador.get_dias(self.user)
        self.dias_hasta = self.dias_desde[1:] + ['']
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$%.2f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        self.data['dia'] = self.dias_desde[0]
        self.importe = controlador.get_categoria_importe(self.user['id_categoria'])
        self.tickets_posibles = int(self.user['saldo'] / self.importe)
        self.data['posibles'] = str(self.tickets_posibles)

    def controlar_dias(self):
        '''
        Controla los días elegidos para que no hayan problemas de rango
        Retorna:
            None si el rango está mal.
            Una lista si el rango está bien o es un solo día.
        '''
        desde = self.dias_desde.index(self.ids.desde.text)
        if self.ids.hasta.text:
            hasta = self.dias_desde.index(self.ids.hasta.text)
            if desde < hasta:
                return self.dias_desde[desde:hasta + 1]
            elif desde == hasta:
                return [self.dias_desde[desde]]
            else:
                return None
        else:
            return [self.dias_desde[desde]]

    def medio_de_pago(self):
        dias = self.controlar_dias()
        if dias:
            if self.user['saldo'] >= self.importe:
                if len(dias) <= self.tickets_posibles:
                    titulo = "Paso 2: Confirmar Pago"
                    self.manager.add_widget(Compra3Screen(dias, titulo, name='compra_3'))
                    self.manager.current = 'compra_3'
                else:
                    faltante = (len(dias) * self.importe) - self.user['saldo']
                    print "faltante %d" % (faltante)
                    self.manager.add_widget(Compra2Screen(dias, faltante,
                                        self.user['saldo'], name='compra_2'))
                    self.manager.current = 'compra_2' 
            else:
                faltante = (len(dias) * self.importe) - self.user['saldo']
                self.manager.add_widget(Compra2Screen(dias, faltante,
                                        self.user['saldo'], name='compra_2'))
                self.manager.current = 'compra_2'
        else:
            self.mensaje = "La fecha DESDE debe ser menor a HASTA"
            WarningPopup().open()

    def cancel(self):
        '''Vuelve a una pantalla anterior'''
        self.manager.current = 'menu'

class Compra2Screen(Screen):

    def __init__(self, dias, faltante, saldo, name=''):
        '''Pantalla para comprar usando efectivo.'''
        self.data = {}
        self.name = name
        self.dias = dias
        self.saldo = saldo
        self.stop = Event()
        self.faltante = faltante
        self.cargar_datos()
        self.mensaje = StringProperty("")
        Screen.__init__(self)

    def update_datos(self):
        '''Actualiza los datos de la pantalla para plasmar cambios'''
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    @mainthread
    def update_ingreso(self, valor, disabled):
        self.ids.ingresado.text = "$ %s" %(valor)
        self.ids.btn_confirmar.disabled = disabled

    def leer_billetes(self, cola_billetes):
        while True:
            try:
                self.valor = cola_billetes.get(False)
            except Empty:
                continue
            if self.stop.is_set():
                return
            else:
                if self.valor:
                    self.update_ingreso(str(self.valor), False)
                else:
                    self.update_ingreso("", True)
            sleep(0.2)

    def cargar_billetes(self):
        Thread(target=self.stack, args=(self.cola_bool,)).start()
        sleep(1)
        self.update_ingreso("", True)
        self.faltante -= self.valor
        if self.faltante <= 0:
            self.ids.faltante.text = "0"
            if self.faltante:
                self.excedente = abs(self.faltante)
            else:
                self.excedente = 0
            self.comprar_tickets(self.excedente)
        else:
            self.ids.faltante.text = "%d" % self.faltante

    def comprar_tickets(self, excedente):
        '''
        Realiza la inserción de los tickets en la db y cambia a la
        siguiente pantalla.
        '''
        id_log = controlador.insert_log(self.user, 'comprar')
        controlador.insert_tickets(self.user, self.dias, id_log)
        controlador.update_saldo(self.user, self.saldo, 1)
        controlador.update_saldo(self.user, excedente, 0)
        self.update_datos()
        self.imprimir_todos()
        self.manager.current = 'menu'
        self.manager.remove_widget(self.manager.get_screen('compra_1'))
        self.manager.remove_widget(self.manager.get_screen('compra_2'))

    def imprimir_todos(self):
        id_log = controlador.insert_log(self.user, 'imprimir')
        for dia in self.dias:
            row = controlador.get_ticket(self.user, dia)
            id_ticket = row['id']
            fecha = row['fecha'].strftime('%d/%m/%Y')
            code = row['barcode']
            nom = self.data['nombre'].decode('utf8')
            dni = self.data['dni'].decode('utf8')
            cat = self.data['categoria'].decode('utf8')
            fac = self.data['facultad'].decode('utf8')
            unit = '03' # chequear db TODO
            ticket = str(id_ticket)
            print_thread = Thread(target=impresora.imprimir_ticket_alumno,
                    args=(nom, dni, fac, cat, code, unit, ticket, fecha))
            print_thread.start()
            controlador.insert_ticket_log(id_ticket, id_log)

    def stack(self, cola_bool):
        cola_bool.put(1)

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de compra'''
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = "$ 0.00"
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        cantidad = len(self.dias)
        self.data['cantidad'] = str(cantidad)
        importe = controlador.get_categoria_importe(self.user['id_categoria'])
        self.data['total'] = '$%.2f' % (importe * cantidad)
        self.total = importe * cantidad
        self.saldo = self.user['saldo']
        self.data['faltante'] = str(self.faltante)
        # Threads & Queue
        self.cola_bool = Queue()
        self.cola_stop = Queue()
        self.cola_billetes = Queue()
        self.valor = 0
        get_bill_thread = Thread(target=self.leer_billetes,
                                    args=(self.cola_billetes,))
        get_bill_thread.daemon = True
        get_bill_thread.start()
        status = {'security': 0, 'enable': 0, 'communication': 0, 'inhibit': 0}
        self.cola_estado = Queue()
        self.cola_estado.put(status)
        bill_thread = Thread(target=billetes.pool, args=(self.cola_billetes,
                                self.cola_bool, self.cola_stop, self.faltante,
                                self.cola_estado, 10))
        bill_thread.daemon = True
        bill_thread.start()

    def cancel(self):
        '''Vuelve a una pantalla anterior'''
        self.stop.set()
        self.cola_stop.put(self.stop.is_set())
        self.manager.current = 'compra_1'
        self.update_ingreso("", True)
        self.manager.remove_widget(self.manager.get_screen('compra_2'))


class Compra3Screen(Screen):

    def __init__(self, dias, titulo, name=''):
        '''Pantalla para confirmar e imprimir los tickets'''
        self.data = {}
        self.name = name
        self.dias = dias
        self.titulo = titulo
        self.cargar_datos()
        self.mensaje = StringProperty("")
        Screen.__init__(self)

    def update_datos(self):
        '''Actualiza los datos de la pantalla para plasmar cambios'''
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de compra'''
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$%.2f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        cantidad = len(self.dias)
        self.data['cantidad'] = str(cantidad)
        importe = controlador.get_categoria_importe(self.user['id_categoria'])
        self.data['total'] = '$%.2f' % (importe * cantidad)
        self.total = importe * cantidad
        self.saldo = self.user['saldo']
        self.data['titulo'] = self.titulo

    def confirmar_tickets(self):
        '''Confirma la compra y verifica que haya saldo suficiente.'''
        content = ConfirmPopup(text='Seguro deseas comprar?')
        content.bind(on_answer=self._on_answer)
        self.popup = Popup(title="Advertencia",
                                content=content,
                                size_hint=(None, None),
                                size=(400,400),
                                auto_dismiss= False)
        self.popup.open()

    def _on_answer(self, instance, answer):
        if answer:
            self.comprar_tickets()
        self.popup.dismiss()

    def check_hora(self, fecha, hora=11):
        '''Verifica que no se pueda anular un ticket despues de la hora'''
        ahora = datetime.now()
        fecha = datetime.strptime(fecha, '%d/%m/%Y')
        if fecha.year == ahora.year:
            if fecha.month == ahora.month and fecha.day == ahora.day:
                if ahora.hour >= hora:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

    def imprimir_todos(self):
        id_log = controlador.insert_log(self.user, 'imprimir')
        for dia in self.dias:
            row = controlador.get_ticket(self.user, dia)
            id_ticket = row['id']
            fecha = row['fecha'].strftime('%d/%m/%Y')
            code = row['barcode']
            nom = self.data['nombre'].decode('utf8')
            dni = self.data['dni'].decode('utf8')
            cat = self.data['categoria'].decode('utf8')
            fac = self.data['facultad'].decode('utf8')
            unit = '03' # chequear db TODO
            ticket = str(id_ticket)
            print_thread = Thread(target=impresora.imprimir_ticket_alumno,
                    args=(nom, dni, fac, cat, code, unit, ticket, fecha))
            print_thread.start()
            controlador.insert_ticket_log(id_ticket, id_log)

    def comprar_tickets(self):
        '''
        Realiza la inserción de los tickets en la db y cambia a la
        siguiente pantalla.
        '''
        id_log = controlador.insert_log(self.user, 'comprar')
        controlador.insert_tickets(self.user, self.dias, id_log)
        controlador.update_saldo(self.user, self.total, 1)
        self.update_datos()
        self.imprimir_todos()
        self.manager.current = 'menu'
        if self.manager.has_screen('compra_2'):
            self.manager.remove_widget(self.manager.get_screen('compra_2'))
        self.manager.remove_widget(self.manager.get_screen('compra_1'))
        self.manager.remove_widget(self.manager.get_screen('compra_3'))
        
    def cancel(self):
        '''Vuelve a una pantalla anterior'''
        self.manager.current = 'compra_1'
        self.manager.remove_widget(self.manager.get_screen('compra_3'))


class ProfileScreen(Screen):

    def __init__(self, name=''):
        '''Pantalla para ver/modificar el perfil del usuario'''
        self.data = {}
        self.name = name
        self.provincias = controlador.get_all_provincias()
        self.cargar_datos()
        Screen.__init__(self)

    def cambiar_pass(self):
        '''Llama a la pantalla de cambiar password'''
        if not self.manager.has_screen('pass'):
            self.manager.add_widget(PasswordScreen('profile', 'profile', 'pass'))
        self.manager.current = 'pass'

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de perfil'''
        try:
            user_session.update(controlador.get_usuario(self.data['dni']))
            self.user = user_session.get_user()
        except KeyError:
            self.user = user_session.get_user()
        self.provincias_nombre = sorted(self.provincias.keys())
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$ %.2f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['nombre'] = self.user['nombre']
        self.data['lu'] = self.user['lu']
        self.data['email'] = self.user['email']
        self.data['provincia'] = controlador.get_provincia(self.user['id_provincia'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']

    def update_datos(self):
        '''Actualiza los datos de la pantalla para plasmar cambios'''
        self.cargar_datos()
        self.ids.nombre.text = self.data['nombre']
        self.ids.lu.text = self.data['lu']
        self.ids.email.text = self.data['email']
        self.ids.provincia.text = self.data['provincia']
        self.ids.saldo.text = self.data['saldo']

    def update_profile(self):
        '''Actualiza el perfil con los cambios realizados por el usuario'''
        self.updata = {}
        self.updata['nombre'] = self.ids.nombre.text
        self.updata['lu'] = self.ids.lu.text
        self.updata['email'] = self.ids.email.text
        self.updata['id_provincia'] = self.provincias[self.ids.provincia.text]
        controlador.update_usuario(self.user, self.updata)
        controlador.insert_log(self.user, 'perfil')
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()

    def cancel(self):
        '''Vuelve a la pantalla anterior'''
        self.manager.current = 'opciones'

    def mailvalidator(self, email):
        '''Valida que el mail esté bien formado'''
        if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$",
                        email) != None:
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
        elif not self.ids.provincia.text:
            self.mensaje = u"Debe especificar una PROVINCIA"
            WarningPopup().open()
        else:
            self.mensaje = "Perfil actualizado correctamente"
            WarningPopup().open()
            self.update_profile()
            self.manager.current = 'opciones'


class AnularScreen(Screen):

    def __init__(self, name=''):
        '''Pantalla para anular los tickets del usuario'''
        self.data = {}
        self.name = name
        self.cargar_datos()
        self.mensaje = StringProperty("")
        Screen.__init__(self)

    def validar_anulacion(self):
        if self.ids.id_ticket.text:
            if not self.ids.id_ticket.text.isdigit():
                self.ids.id_ticket.text = ""
                self.ids.id_ticket.focus = True
                self.mensaje = "El código del ticket\r\n solo contiene números."
                WarningPopup().open()
            else:
                fecha = controlador.has_ticket(self.user, self.ids.id_ticket.text)
                if fecha:
                    return fecha
                else:
                    self.ids.id_ticket.text = ""
                    self.ids.id_ticket.focus = True
                    self.mensaje = "El código del ticket\r\n no es valido."
                    WarningPopup().open()
        else:
            self.ids.id_ticket.text = ""
            self.ids.id_ticket.focus = True
            self.mensaje = "El código del ticket\r\n no puede estar vacío."
            WarningPopup().open()

    def confirmacion(self):
        Window.release_all_keyboards()
        self.fecha = self.validar_anulacion()
        if self.fecha:
            content = ConfirmPopup(text='Seguro deseas anular el ticket\r\n del día %s?' %(self.fecha))
            content.bind(on_answer=self._on_answer)
            self.popup = Popup(title="Advertencia",
                                    content=content,
                                    size_hint=(None, None),
                                    size=(400,400),
                                    auto_dismiss= False)
            self.popup.open()

    def _on_answer(self, instance, answer):
        if answer:
            self.anular_ticket()
            self.ids.id_ticket.text = ""
        self.popup.dismiss()

    def anular_ticket(self):
        '''Anula el ticket de acuerdo al id ingresado'''
        id_ticket = int(self.ids.id_ticket.text)
        controlador.anular_ticket(id_ticket)
        id_log = controlador.insert_log(self.user, 'anular')
        controlador.insert_ticket_log(id_ticket, id_log)

    def update_datos(self):
        '''Actualiza los datos de la pantalla para plasmar cambios'''
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    def check_hora(self, fecha, hora=11):
        '''Verifica que no se pueda anular un ticket despues de la hora'''
        ahora = datetime.now()
        fecha = datetime.strptime(fecha, '%d/%m/%Y')
        if fecha.year == ahora.year:
            if fecha.month == ahora.month and fecha.day == ahora.day:
                if ahora.hour >= hora:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

    def cargar_datos(self):
        '''Carga los datos del usuario dentro de la pantalla de anulación'''
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$%.2f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['ruta_foto'] = self.user['ruta_foto']
            
    def cancel(self):
        '''Vuelve a una pantalla anterior'''
        self.manager.current = 'opciones'
        

class CargaScreen(Screen):

    def __init__(self, name=''):
        '''Pantalla para comprar usando efectivo.'''
        self.data = {}
        self.name = name
        self.stop = Event()
        self.cargar_datos()
        self.total = 0
        self.mensaje = StringProperty("")
        Screen.__init__(self)

    def update_datos(self):
        '''Actualiza los datos de la pantalla para plasmar cambios'''
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    @mainthread
    def update_ingreso(self, valor, disabled):
        self.ids.ingresado.text = "$ %s" %(valor)
        self.ids.btn_confirmar.disabled = disabled

    def leer_billetes(self, cola_billetes):
        while True:
            try:
                self.valor = cola_billetes.get(False)
            except Empty:
                continue
            if self.stop.is_set():
                return
            else:
                if self.valor:
                    self.update_ingreso(str(self.valor), False)
                else:
                    self.update_ingreso("", True)
            sleep(0.2)

    def cargar_billetes(self):
        Thread(target=self.stack, args=(self.cola_bool,)).start()
        sleep(0.5)
        self.update_ingreso("", True)
        self.cargar_saldo(self.valor)

    def cargar_saldo(self, excedente):
        '''
        Realiza la inserción de los tickets en la db y cambia a la
        siguiente pantalla.
        '''
        controlador.update_saldo(self.user, self.valor, 0)
        self.total += self.valor
        self.ids.total.text = "$ %.2f" %(self.total)
        self.update_datos()

    def stack(self, cola_bool):
        cola_bool.put(1)

    def cargar_datos(self):
        '''
        Carga los datos del usuario dentro de la pantalla de compra.
        Inicia las colas e hilos para manejar la maquina de billetes.
        '''
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = "$ %.2f" % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        # Threads & Queue
        self.cola_bool = Queue()
        self.cola_stop = Queue()
        self.cola_billetes = Queue()
        self.valor = 0
        get_bill_thread = Thread(target=self.leer_billetes,
                                    args=(self.cola_billetes,))
        get_bill_thread.daemon = True
        get_bill_thread.start()
        status = {'security': 0, 'enable': 0, 'communication': 0, 'inhibit': 0}
        self.cola_estado = Queue()
        self.cola_estado.put(status)
        bill_thread = Thread(target=billetes.pool, args=(self.cola_billetes,
                                self.cola_bool,
                                self.cola_stop, 100 - self.user['saldo'],
                                self.cola_estado, 10))
        bill_thread.daemon = True
        bill_thread.start()

    def cancel(self):
        '''Vuelve a una pantalla anterior'''
        if self.total:
            controlador.insert_log(self.user, 'cargar', str(self.total))
        self.stop.set()
        self.cola_stop.put(self.stop.is_set())
        self.manager.current = 'menu'
        self.manager.remove_widget(self.manager.get_screen('carga'))


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
                        user = user_session.get_user()
                        controlador.insert_log(user, 'ingresar')
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
        Thread(target=billetes.init).start()
        sm = ScreenManager(transition=WipeTransition())
        # Agregamos las pantallas fijas del sistema
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(FormScreen(name='formulario'))
        sm.add_widget(LoginScreen(name='login'))
        return sm


if __name__ == '__main__':
    TicketApp().run()
