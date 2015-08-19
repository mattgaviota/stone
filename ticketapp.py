#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html

# Utility import
from threading import Thread, Event
from Queue import Queue, Empty
from datetime import datetime
from time import sleep, time
from os import system
# intra-packages imports
from db import controlador
from lib import session, utils, impresora, billetes
from src.alerts import WarningPopup, ConfirmPopup
from src.settings import UNIDAD
## screens
from src.screens.splash import SplashScreen
from src.screens.login import LoginScreen
from src.screens.ayuda import AyudaScreen
from src.screens.form import FormScreen
from src.screens.control import ControlScreen
# Kivy related imports
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.clock import mainthread


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


class MenuScreen(Screen):
    """Pantalla de menu de usuario"""

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

    def options(self):
        """Crea y accede a la pantalla de opciones"""
        if not self.manager.has_screen('opciones'):
            self.manager.add_widget(OptionScreen(name='opciones'))
        self.manager.current = 'opciones'

    def comprar(self):
        """
        Crea y accede a la pantalla de compra de tickets siempre y cuando
        haya papel en la impresora.
        """
        estado = impresora.check_status()
        if estado == 1:
            controlador.update_estado_maquina(UNIDAD, 1)
            if not self.manager.has_screen('compra_1'):
                self.manager.add_widget(Compra1Screen(name='compra_1'))
            self.manager.current = 'compra_1'
        elif estado == 2:
            controlador.update_estado_maquina(UNIDAD, 4)
            mensaje = u"\rLa maquina no tiene papel.\r\n Disculpe las molestias"
            WarningPopup(mensaje).open()
        else:
            controlador.update_estado_maquina(UNIDAD, 2)
            mensaje = u"\rLa impresora está desconectada.\r\n Disculpe las molestias"
            WarningPopup(mensaje).open()

    def logout(self):
        """Cierra la sesion, libera las pantallas que no se van a usar y
        vuelve a la pantalla principal"""
        user = user_session.get_user()
        controlador.insert_log(user, 'salir', UNIDAD)
        controlador.update_activo(user, 0)
        user_session.close()
        if self.manager.has_screen('opciones'):
            self.manager.remove_widget(self.manager.get_screen('opciones'))
        if self.manager.has_screen('compra_1'):
            self.manager.remove_widget(self.manager.get_screen('compra_1'))
        if self.manager.has_screen('compra_2'):
            self.manager.remove_widget(self.manager.get_screen('compra_2'))
        self.manager.current = 'splash'


class OptionScreen(Screen):
    """Pantalla de opciones de usuario"""

    def anular(self):
        """Crea y accede a la pantalla de anulación de tickets"""
        if not self.manager.has_screen('anular'):
            self.manager.add_widget(AnularScreen(name='anular'))
        self.manager.current = 'anular'

    def cargar(self):
        """Crea y accede a la pantalla de carga de saldo"""
        self.user = user_session.get_user()
        if self.user['saldo'] >= 100:
            mensaje = "No puede cargar más de $ 100"
            WarningPopup(mensaje).open()
        else:
            if not self.manager.has_screen('carga'):
                self.manager.add_widget(CargaScreen(name='carga'))
            self.manager.current = 'carga'

    def perfil(self):
        """Crea y accede a la pantalla de perfil"""
        if not self.manager.has_screen('profile'):
            self.manager.add_widget(ProfileScreen(name='profile'))
        self.manager.current = 'profile'

    def cancel(self):
        """Vuelve a la pantalla anterior"""
        if self.manager.has_screen('anular'):
            self.manager.remove_widget(self.manager.get_screen('anular'))
        if self.manager.has_screen('profile'):
            self.manager.remove_widget(self.manager.get_screen('profile'))
        if self.manager.has_screen('pass'):
            self.manager.remove_widget(self.manager.get_screen('pass'))
        self.manager.current = 'menu'


class Compra1Screen(Screen):

    def __init__(self, **kwargs):
        """Pantalla para elegir los días de compra de tickets"""
        self.data = {}
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$ %.0f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(
                                                    self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(
                                                    self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        super(Compra1Screen, self).__init__(**kwargs)
        self.cargar_datos()

    def update_datos(self):
        """Actualiza los datos de la pantalla para plasmar cambios"""
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.user = user_session.get_user()
        self.cargar_datos()
        self.data['saldo'] = '$ %.0f' % (self.user['saldo'])
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']
        self.ids.desde.text = self.data['dia']
        self.ids.hasta.text = self.dias_hasta[0]

    def cargar_datos(self):
        """Carga los datos del usuario dentro de la pantalla de compra"""
        limite = controlador.get_categoria_limite(self.user['id_categoria'])
        self.dias_desde, self.d_name = controlador.get_dias(self.user, limite)
        if not self.dias_desde:
            self.dias_hasta = [u"Solo para este día"]
            self.ids.desde.values = []
            self.ids.hasta.values = []
            self.data['dia'] = ''
            self.ids.desde.text = self.data['dia']
            self.ids.posibles.text = '\rNo hay días disponibles\r\n para la compra'
            self.ids.btn_next.disabled = True
        else:
            self.ids.desde.values = self.d_name
            self.dias_hasta = [u"Solo para este día"] + self.d_name[1:]
            self.ids.hasta.values = self.dias_hasta
            self.ids.hasta.text = self.dias_hasta[0]
            self.data['dia'] = self.d_name[0]
            self.ids.desde.text = self.data['dia']
            self.importe = controlador.get_categoria_importe(
                                                    self.user['id_categoria'])
            if self.importe:
                self.tickets_posibles = int(self.user['saldo'] / self.importe)
            else:
                self.tickets_posibles = limite - controlador.get_count_tickets(
                                                                    self.user)
            self.ids.posibles.text = str(self.tickets_posibles)

    def controlar_dias(self):
        """
        Controla los días elegidos para que no hayan problemas de rango
        Retorna:
            None si el rango está mal.
            Una lista si el rango está bien o es un solo día.
        """
        desde = self.d_name.index(self.ids.desde.text)
        if self.ids.hasta.text:
            if self.ids.hasta.text != u"Solo para este día":
                hasta = self.d_name.index(self.ids.hasta.text)
                if desde < hasta:
                    return self.dias_desde[desde:hasta + 1]
                elif desde == hasta:
                    return [self.dias_desde[desde]]
                else:
                    return None
            else:
                return [self.dias_desde[desde]]
        else:
            return [self.dias_desde[desde]]

    def medio_de_pago(self):
        """
        Función que se ejecuta al presionar continuar. Decide en base al saldo
        disponible a que pantalla saltar.
        Si el saldo es mayor al importe necesario para realizar la compra va a
        la pantalla de confirmación.
        Si el saldo es menor o insuficiente para realizar la compra va a la
        pantalla de ingreso de billetes.
        """
        sleep(1)
        dias = self.controlar_dias()
        if dias:
            if self.user['saldo'] >= self.importe:
                if len(dias) <= self.tickets_posibles:
                    titulo = "Paso 2: Confirmar Pago"
                    self.manager.add_widget(Compra3Screen(dias, titulo,
                                                            name='compra_3'))
                    self.manager.current = 'compra_3'
                else:
                    self.manager.add_widget(Compra2Screen(dias,
                                        self.user['saldo'], name='compra_2'))
                    self.manager.current = 'compra_2'
            else:
                self.manager.add_widget(Compra2Screen(dias,
                                        self.user['saldo'], name='compra_2'))
                self.manager.current = 'compra_2'
        else:
            mensaje = "La fecha DESDE debe ser menor a HASTA"
            WarningPopup(mensaje).open()

    def cancel(self):
        """Vuelve a una pantalla anterior"""
        self.manager.current = 'menu'
        self.manager.remove_widget(self.manager.get_screen('compra_1'))

class Compra2Screen(Screen):

    def __init__(self, dias, saldo, **kwargs):
        """Pantalla para comprar usando efectivo."""
        self.user = user_session.get_user()
        id_log = controlador.insert_log(self.user, 'reservar', UNIDAD)
        self.reserva, full, state = controlador.reservar_tickets(self.user,
                                                        dias, id_log, UNIDAD)
        self.data = {}
        self.saldo = saldo
        self.stop = Event()
        importe = controlador.get_categoria_importe(self.user['id_categoria'])
        self.faltante = (len(self.reserva) * importe) - saldo
        self.total_parcial = 0
        self.bandera = True
        self.cargar_datos()
        self.cargar_threads()
        if state:
            if full:
                for dia in full:
                    mensaje = "\rNo se pudo reservar: \r\n\t%s" % (
                                                    dia.strftime('%d/%m/%Y'))
                    WarningPopup(mensaje).open()
        else:
            mensaje = "\rHubo un error al reservar \r\nIntente nuevamente"
            WarningPopup(mensaje).open()
            self.cancel()
        super(Compra2Screen, self).__init__(**kwargs)

    def update_datos(self):
        """Actualiza los datos de la pantalla para plasmar cambios"""
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.user = user_session.get_user()
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']
        self.total_parcial = 0

    @mainthread
    def update_ingreso(self, valor, disabled):
        """
        Muestra la imagen del billete ingresado y habilita el botón de
        confirmación.
        """
        source = "./images/billetes/%sp.jpg" % (valor)
        self.ids.ingresado.source = source
        self.ids.btn_confirmar.disabled = disabled

    def leer_billetes(self, cola_billetes):
        """
        Inicia el proceso de lectura de billetes. Cuando detecta un billete
        actualiza la pantalla para mostrar lo ingresado y permite que el
        billete se cargue en la maquina.
        """
        while True:
            try:
                self.valor = cola_billetes.get(False)
            except Empty:
                continue
            if self.stop.is_set():
                return
            else:
                if self.valor:
                    if self.valor == -1:
                        self.billete_trabado()
                        sleep(1)
                    else:
                        self.update_ingreso(str(self.valor), False)
                else:
                    self.update_ingreso("no", True)
            sleep(0.1)

    @mainthread
    def bloquear(self):
        self.manager.add_widget(BloqueoScreen(name='bloqueo'))
        self.manager.current = 'bloqueo'

    def billete_trabado(self):
        """ Registra los billetes trabados. """
        self.update_ingreso("jam", True)
        controlador.insert_log(self.user, 'jam', UNIDAD)
        self.stop.set()
        self.cola_stop.put(True)
        user = user_session.get_user()
        controlador.insert_log(user, 'salir', UNIDAD,
                                                'Billete trabado - bloqueo')
        controlador.update_activo(user, 0)
        user_session.close()
        sleep(2)
        self.bloquear()

    def cargar_billetes(self):
        """
        Inicia el hilo que se encarga de almacenar el billete en la maquina.
        Comprueba el dinero faltante.
        """
        Thread(target=self.stack, args=(self.cola_bool,)).start()
        sleep(1)
        self.update_ingreso("no", True)
        id_maquina = UNIDAD
        controlador.insert_billete(self.user, self.valor, id_maquina)
        self.total_parcial += self.valor
        self.faltante -= self.valor
        if self.faltante <= 0:
            self.update_ingreso("no", True)
            sleep(0.5)
            self.ids.faltante.text = "0"
            if self.faltante:
                self.excedente = abs(self.faltante)
            else:
                self.excedente = 0
            self.comprar_tickets(self.excedente)
        else:
            self.ids.faltante.text = "$ %d" % self.faltante
        self.update_ingreso("no", True)

    def comprar_tickets(self, excedente):
        """
        Realiza la inserción de los tickets en la db y cambia a la
        siguiente pantalla.
        """
        if self.bandera:
            id_log = controlador.insert_log(self.user, 'comprar', UNIDAD)
            if id_log:
                self.bandera = False
                controlador.comprar_tickets(self.reserva, id_log)
                controlador.update_saldo(self.user, self.saldo, 1)
                if excedente:
                    controlador.insert_log(
                        self.user,
                        'cargar',
                        UNIDAD,
                        str(excedente)
                    )
                    controlador.update_saldo(self.user, excedente, 0)
                self.update_datos()
                self.imprimir_todos()
                self.manager.add_widget(
                    ConfirmacionScreen(
                        len(self.reserva),
                        name='confirmacion'
                    )
                )
                self.manager.current = 'confirmacion'
                self.manager.remove_widget(self.manager.get_screen('compra_1'))
                self.manager.remove_widget(self.manager.get_screen('compra_2'))
                self.total_parcial = 0
            else:
                self.cancel()

    def imprimir_todos(self):
        """
        Imprime todos los tickets que se hayan comprado.
        """
        id_log = controlador.insert_log(self.user, 'imprimir', UNIDAD)
        ticket_list = []
        for ticket, id_dia in self.reserva:
            row = None
            ticket_data = {}
            row = controlador.get_ticket_by_id(ticket)
            if row:
                id_ticket = row['id']
                ticket_data['fecha'] = row['fecha'].strftime('%d/%m/%Y')
                ticket_data['code'] = row['barcode']
                ticket_data['nombre'] = self.data['nombre'].decode('utf8')
                ticket_data['dni'] = self.data['dni'].decode('utf8')
                ticket_data['categoria'] = self.data['categoria'].decode('utf8')
                ticket_data['facultad'] = self.data['facultad'].decode('utf8')
                ticket_data['unidad'] = str(UNIDAD)
                ticket_data['mensaje'] = u"Gracias por usar el Comedor Universitario"
                ticket_data['ticket'] = str(id_ticket)
                ticket_data['saldo'] = self.user['saldo']
                controlador.insert_ticket_log(id_ticket, id_log)
                ticket_list.append(ticket_data)

        print_thread = Thread(
            target=impresora.imprimir_tickets_alumno,
            args=ticket_list
        )
        print_thread.start()

    def stack(self, cola_bool):
        """Envía la orden para almacenar el billete en la lectora."""
        cola_bool.put(1)

    def cargar_datos(self):
        """Carga los datos del usuario dentro de la pantalla de compra"""
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = "$ %.0f" % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(
                                                    self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(
                                                    self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        cantidad = len(self.reserva)
        self.data['cantidad'] = str(cantidad)
        importe = controlador.get_categoria_importe(self.user['id_categoria'])
        self.data['total'] = '$ %.0f' % (importe * cantidad)
        self.total = importe * cantidad
        self.saldo = self.user['saldo']
        self.data['faltante'] = "$ %.0f" % (self.faltante)

    def cargar_threads(self):
        """
        Carga e inicia los hilos que manejan la maquina verificadora de
        billetes.
        """
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
                                self.cola_estado, 8))
        bill_thread.daemon = True
        bill_thread.start()

    def cancel(self):
        """Vuelve a una pantalla anterior"""
        self.stop.set()
        self.cola_stop.put(True)
        if self.total_parcial:
            total = self.total_parcial
            log = controlador.insert_log(self.user, 'cargar', UNIDAD,
                                                        str(self.total_parcial))
            controlador.update_saldo(self.user, self.total_parcial, 0)
            self.update_datos()
            if impresora.check_status() == 1:
                log = str(log)
                nom = self.data['nombre'].decode('utf8')
                dni = self.data['dni'].decode('utf8')
                cat = self.data['categoria'].decode('utf8')
                fac = self.data['facultad'].decode('utf8')
                unit = str(UNIDAD)
                fecha = str(int(time()))
                pco = total
                code = fecha + '0' * (10 - len(log)) + log
                msj = u"Gracias por usar el Comedor Universitario"
                sdo = self.user['saldo']
                print_thread = Thread(target=impresora.imprimir_ticket_carga,
                    args=(nom, dni, fac, cat, code, unit, log, msj, pco, sdo))
                print_thread.start()
        controlador.cancelar_tickets(self.reserva)
        self.manager.current = 'compra_1'
        self.update_ingreso("", True)
        self.manager.remove_widget(self.manager.get_screen('compra_2'))


class Compra3Screen(Screen):

    def __init__(self, dias, titulo, **kwargs):
        """Pantalla para confirmar e imprimir los tickets"""
        self.user = user_session.get_user()
        id_log = controlador.insert_log(self.user, 'reservar', UNIDAD)
        self.reserva, full, state = controlador.reservar_tickets(self.user,
                                                        dias, id_log, UNIDAD)
        if state:
            if full:
                for dia in full:
                    mensaje = "\rNo se pudo reservar: \r\n\t%s" % (
                                                    dia.strftime('%d/%m/%Y'))
                    WarningPopup(mensaje).open()
        else:
            mensaje = "\rHubo un error al reservar \r\nIntente nuevamente"
            WarningPopup(mensaje).open()
            self.cancel()
        self.bandera = True
        self.data = {}
        self.dias = dias
        self.titulo = titulo
        self.cargar_datos()
        super(Compra3Screen, self).__init__(**kwargs)

    def update_datos(self):
        """Actualiza los datos de la pantalla para plasmar cambios"""
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.user = user_session.get_user()
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    def cargar_datos(self):
        """Carga los datos del usuario dentro de la pantalla de compra"""
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$ %.0f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(
                                                    self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(
                                                    self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        cantidad = len(self.reserva)
        self.data['cantidad'] = str(cantidad)
        importe = controlador.get_categoria_importe(self.user['id_categoria'])
        self.data['total'] = '$ %.0f' % (importe * cantidad)
        self.total = importe * cantidad
        self.saldo = self.user['saldo']
        self.data['titulo'] = self.titulo

    def confirmar_tickets(self):
        """Confirma la compra y verifica que haya saldo suficiente."""
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

    def imprimir_todos(self):
        """
        Imprime todos los tickets que se hayan comprado.
        """
        id_log = controlador.insert_log(self.user, 'imprimir', UNIDAD)
        ticket_list = []
        for ticket, id_dia in self.reserva:
            row = None
            ticket_data = {}
            row = controlador.get_ticket_by_id(ticket)
            if row:
                id_ticket = row['id']
                ticket_data['fecha'] = row['fecha'].strftime('%d/%m/%Y')
                ticket_data['code'] = row['barcode']
                ticket_data['nombre'] = self.data['nombre'].decode('utf8')
                ticket_data['dni'] = self.data['dni'].decode('utf8')
                ticket_data['categoria'] = self.data['categoria'].decode('utf8')
                ticket_data['facultad'] = self.data['facultad'].decode('utf8')
                ticket_data['unidad'] = str(UNIDAD)
                ticket_data['mensaje'] = u"Gracias por usar el Comedor Universitario"
                ticket_data['ticket'] = str(id_ticket)
                ticket_data['saldo'] = self.user['saldo']
                controlador.insert_ticket_log(id_ticket, id_log)
                ticket_list.append(ticket_data)

        print_thread = Thread(
            target=impresora.imprimir_tickets_alumno,
            args=ticket_list
        )
        print_thread.start()

    def comprar_tickets(self):
        """
        Realiza la inserción de los tickets en la db y cambia a la
        siguiente pantalla.
        """
        if self.bandera:
            id_log = controlador.insert_log(self.user, 'comprar', UNIDAD)
            if id_log:
                self.bandera = False
                controlador.comprar_tickets(self.reserva, id_log)
                controlador.update_saldo(self.user, self.total, 1)
                self.update_datos()
                self.imprimir_todos()
                self.manager.add_widget(ConfirmacionScreen(len(self.reserva),
                                                            name='confirmacion'))
                self.manager.current = 'confirmacion'
                if self.manager.has_screen('compra_2'):
                    self.manager.remove_widget(self.manager.get_screen('compra_2'))
                self.manager.remove_widget(self.manager.get_screen('compra_1'))
                self.manager.remove_widget(self.manager.get_screen('compra_3'))
            else:
                self.cancel()


    def cancel(self):
        """Vuelve a una pantalla anterior"""
        controlador.cancelar_tickets(self.reserva)
        self.manager.current = 'compra_1'
        self.manager.remove_widget(self.manager.get_screen('compra_3'))


class ConfirmacionScreen(Screen):
    """ Pantalla para mostrar una confirmación de compra """

    def __init__ (self, cantidad, **kwargs):
        self.cantidad = cantidad
        self.data = {}
        self.cargar_datos()
        super(ConfirmacionScreen, self).__init__(**kwargs)

    def cargar_datos(self):
        """Carga los datos del usuario dentro de la pantalla de compra"""
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = "$ %.0f" % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(
                                                    self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(
                                                    self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']
        self.data['cantidad'] = str(self.cantidad)
        self.saldo = self.user['saldo']

    def update_datos(self):
        """Actualiza los datos de la pantalla para plasmar cambios"""
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    def cancel(self):
        """Regresa a la pantalla principal"""
        self.manager.current = 'menu'
        self.manager.remove_widget(self.manager.get_screen('confirmacion'))




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
            self.manager.add_widget(PasswordScreen('profile', 'profile', 'pass'))
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
        if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$",
                        email) != None:
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
            mensaje = u"\rSu EMAIL está mal formado.\r\n Recuerde que este mail se usa\r\n para confirmaciones."
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


class AnularScreen(Screen):

    def __init__(self, **kwargs):
        """Pantalla para anular los tickets del usuario"""
        self.data = {}
        self.cargar_datos()
        super(AnularScreen, self).__init__(**kwargs)

    def validar_anulacion(self):
        """Verifica que el numero ingresado corresponda a un ticket valido
        para el usuario y que sea antes de la hora máxima permitida."""
        if self.ids.id_ticket.text:
            if not self.ids.id_ticket.text.isdigit():
                self.ids.id_ticket.text = ""
                self.ids.id_ticket.focus = True
                mensaje = "\rEl código del ticket\r\n solo tiene números."
                WarningPopup(mensaje).open()
            else:
                fecha = controlador.has_ticket(self.user,
                                                    self.ids.id_ticket.text)
                hora_max = controlador.get_hora_anulacion()
                if fecha:
                    codigo = self.check_hora(fecha, hora_max)
                    if codigo == 1:
                        return fecha.strftime('%d/%m/%Y') # anular
                    elif codigo == 0:
                        self.ids.id_ticket.text = ""
                        self.ids.id_ticket.focus = True
                        mensaje = "\rNo puede anular un ticket\r\n despues de las %d hs." % (hora_max)
                        WarningPopup(mensaje).open()
                        return 0 # nada
                    else:
                        self.ticket_vencido()
                        self.ids.id_ticket.text = ""
                        self.ids.id_ticket.focus = True
                        mensaje = "\rNo puede anular un ticket\r\n despues de la fecha\r\n de servicio.\r\n\r\n Su ticket se venció."
                        WarningPopup(mensaje).open()
                        return 0 # vencer
                else:
                    self.ids.id_ticket.text = ""
                    self.ids.id_ticket.focus = True
                    mensaje = "El código del ticket\r\n no es valido."
                    WarningPopup(mensaje).open()
        else:
            self.ids.id_ticket.text = ""
            self.ids.id_ticket.focus = True
            mensaje = "\rEl código del ticket\r\n no puede estar vacío."
            WarningPopup(mensaje).open()

    def confirmacion(self):
        Window.release_all_keyboards()
        self.fecha = self.validar_anulacion()
        if self.fecha:
            content = ConfirmPopup(
                    text='\rSeguro deseas anular el ticket\r\n del día %s?' %
                    (self.fecha))
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

    def ticket_vencido(self):
        """ Anula el ticket vencido poniendo el estado vencido. """
        id_ticket = int(self.ids.id_ticket.text)
        controlador.update_ticket(id_ticket, self.user, UNIDAD, 4)

    def anular_ticket(self):
        """Anula el ticket de acuerdo al id ingresado"""
        id_ticket = int(self.ids.id_ticket.text)
        controlador.anular_ticket(id_ticket, self.user, UNIDAD)
        self.update_datos()

    def update_datos(self):
        """Actualiza los datos de la pantalla para plasmar cambios"""
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    def check_hora(self, fecha, hora):
        """Verifica que no se pueda anular un ticket despues de la hora"""
        ahora = datetime.now()
        if ahora.date() < fecha.date():
            return 1 # Ok (anular)
        elif ahora.date() > fecha.date():
            return 2 # Fecha anterior al día de hoy(vencer).
        else:
            if hora <= ahora.hour < 15:
                return 0 # Hora invalida para anular (Nada)
            elif ahora.hour < hora:
                return 1 # Ok (anular)
            else:
                return 2 # Hora posterior al permitido.(vencer)

    def cargar_datos(self):
        """Carga los datos del usuario dentro de la pantalla de anulación"""
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = '$%.0f' % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(
                                                    self.user['id_categoria'])
        self.data['ruta_foto'] = self.user['ruta_foto']

    def cancel(self):
        """Vuelve a una pantalla anterior"""
        self.manager.current = 'opciones'


class CargaScreen(Screen):

    def __init__(self, **kwargs):
        """Pantalla para comprar usando efectivo."""
        self.data = {}
        self.stop = Event()
        self.cargar_datos()
        self.cargar_threads()
        self.total = 0
        super(CargaScreen, self).__init__(**kwargs)

    def update_datos(self):
        """Actualiza los datos de la pantalla para plasmar cambios"""
        user_session.update(controlador.get_usuario(self.data['dni']))
        self.cargar_datos()
        self.ids.saldo.text = self.data['saldo']
        self.ids.nombre.text = self.data['nombre']

    @mainthread
    def update_ingreso(self, valor, disabled):
        """
        Muestra la imagen del billete ingresado y habilita el botón de
        confirmación.
        """
        source = "./images/billetes/%sp.jpg" % (valor)
        self.ids.ingresado.source = source
        self.ids.btn_confirmar.disabled = disabled

    def leer_billetes(self, cola_billetes):
        """
        Inicia el proceso de lectura de billetes. Cuando detecta un billete
        actualiza la pantalla para mostrar lo ingresado y permite que el
        billete se cargue en la maquina.
        """
        while True:
            try:
                self.valor = cola_billetes.get(False)
            except Empty:
                continue
            if self.stop.is_set():
                return
            else:
                if self.valor:
                    if self.valor == -1:
                        self.billete_trabado()
                        sleep(1)
                    else:
                        if self.user['saldo'] + self.valor > 100:
                            Thread(target=self.stack,
                                        args=(self.cola_bool, 2)).start()
                            mensaje = "No puede cargar mas de $ 100"
                            WarningPopup(mensaje).open()
                        else:
                            self.update_ingreso(str(self.valor), False)
                else:
                    self.update_ingreso("no", True)
            sleep(0.1)

    @mainthread
    def bloquear(self):
        self.manager.add_widget(BloqueoScreen(name='bloqueo'))
        self.manager.current = 'bloqueo'

    def billete_trabado(self):
        """ Registra los billetes trabados. """
        self.update_ingreso("jam", True)
        controlador.insert_log(self.user, 'jam', UNIDAD)
        self.stop.set()
        self.cola_stop.put(True)
        user = user_session.get_user()
        controlador.insert_log(user, 'salir', UNIDAD,
                                                'Billete trabado - bloqueo')
        controlador.update_activo(user, 0)
        user_session.close()
        sleep(2)
        self.bloquear()

    def cargar_billetes(self):
        """
        Inicia el hilo que se encarga de almacenar el billete en la maquina
        una vez que se presiona el boton de confirmar.
        """
        Thread(target=self.stack, args=(self.cola_bool, 1)).start()
        sleep(1)
        self.update_ingreso("", True)
        id_maquina = UNIDAD
        controlador.insert_billete(self.user, self.valor, id_maquina)
        self.cargar_saldo()

    def cargar_saldo(self):
        """
        Actualiza el saldo de acuerdo a los billetes que vayan ingresando.
        """
        controlador.update_saldo(self.user, self.valor, 0)
        self.total += self.valor
        self.update_datos()

    def stack(self, cola_bool, value):
        """Envía la orden para almacenar el billete en la lectora."""
        cola_bool.put(value)

    def cargar_datos(self):
        """
        Carga los datos del usuario dentro de la pantalla de carga.
        """
        self.user = user_session.get_user()
        self.data['nombre'] = self.user['nombre']
        self.data['dni'] = self.user['dni']
        self.data['saldo'] = "$ %.0f" % (self.user['saldo'])
        self.data['categoria'] = controlador.get_categoria_nombre(
                                                    self.user['id_categoria'])
        self.data['facultad'] = controlador.get_facultad(
                                                    self.user['id_facultad'])
        self.data['ruta_foto'] = self.user['ruta_foto']

    def cargar_threads(self):
        """
        Carga e inicia los hilos que manejan la maquina verificadora de
        billetes.
        """
        self.cola_bool = Queue()
        self.cola_stop = Queue()
        self.cola_billetes = Queue()
        self.valor = 0
        get_bill_thread = Thread(target=self.leer_billetes,
                                    args=(self.cola_billetes,))
        get_bill_thread.daemon = True
        get_bill_thread.start()
        saldo_maximo = controlador.get_saldo_maximo()
        status = {'security': 0, 'enable': 0, 'communication': 0, 'inhibit': 0}
        self.cola_estado = Queue()
        self.cola_estado.put(status)
        bill_thread = Thread(target=billetes.pool, args=(self.cola_billetes,
                                self.cola_bool, self.cola_stop,
                                saldo_maximo - self.user['saldo'],
                                self.cola_estado, 8))
        bill_thread.daemon = True
        bill_thread.start()

    def cancel(self):
        """Vuelve a una pantalla anterior"""
        if self.total:
            if impresora.check_status() == 1:
                log = controlador.insert_log(self.user, 'cargar', UNIDAD,
                                                            str(self.total))
                log = str(log)
                nombre = self.data['nombre'].decode('utf8')
                dni = self.data['dni'].decode('utf8')
                categoria = self.data['categoria'].decode('utf8')
                facultad = self.data['facultad'].decode('utf8')
                unidad = str(UNIDAD)
                fecha = str(int(time()))
                total = self.total
                code = fecha + '0' * (10 - len(log)) + log
                mensaje = u"Gracias por usar el Comedor Universitario"
                saldo = self.user['saldo']
                print_thread = Thread(
                    target=impresora.imprimir_ticket_carga,
                    args=(
                        nombre,
                        dni,
                        facultad,
                        categoria,
                        code,
                        unidad,
                        log,
                        mensaje,
                        total,
                        saldo
                    )
                )
                print_thread.start()
        self.stop.set()
        self.cola_stop.put(True)
        self.manager.current = 'menu'
        self.manager.remove_widget(self.manager.get_screen('carga'))


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
                mensaje = u"\rSu PASSWORD no puede tener\r\n más de 64 caracteres."
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
                    controlador.insert_log(user, 'ingresar', UNIDAD,
                                                        'control - desbloqueo')
                    self.manager.current = 'menu_control'
                    self.manager.remove_widget(self.manager.get_screen('bloqueo'))
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
                if user['id_perfil'] in [3, 5]: # usuario administrativo
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
        pass_db = utils.aclarar_pass(user['password']) # control interno
        if pass_ingresado == pass_db:
            return 1
        else:
            return 0

    def clear(self):
        """Limpia los campos de texto y libera el teclado virtual"""
        self.ids.dni.text = ""
        self.ids.passw.text = ""
        Window.release_all_keyboards()


class TicketApp(App):

    def build(self):
        Builder.load_file('kv/ticket.kv')
        # Creamos el screen manager con la WipeTransition
        sm = ScreenManager(transition=WipeTransition())
        # Agregamos las pantallas fijas del sistema
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(FormScreen(name='formulario'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AyudaScreen(name='ayuda'))
        sm.add_widget(ControlScreen(name='menu_control'))
        return sm


if __name__ == '__main__':
    controlador.insert_log({'dni': '222'}, 'iniciar', UNIDAD, 'Pre Inicio')
    init_thread = Thread(target=billetes.init)
    init_thread.daemon = True
    init_thread.start()
    TicketApp().run()
