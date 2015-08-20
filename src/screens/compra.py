# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from threading import Thread, Event
from Queue import Queue, Empty
from lib import utils, billetes
from db import controlador
from src.settings import user_session, UNIDAD
from src.alerts import WarningPopup, ConfirmPopup
from bloqueo import BloqueoScreen
from time import sleep
from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread


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
            posibles = '\rNo hay días disponibles\r\n para la compra'
            self.ids.posibles.text = posibles
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
                    self.manager.add_widget(
                        Compra3Screen(dias, titulo, name='compra_3')
                    )
                    self.manager.current = 'compra_3'
                else:
                    self.manager.add_widget(
                        Compra2Screen(
                            dias,
                            self.user['saldo'],
                            name='compra_2'
                        )
                    )
                    self.manager.current = 'compra_2'
            else:
                self.manager.add_widget(
                    Compra2Screen(dias, self.user['saldo'], name='compra_2')
                )
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
        self.reserva, full, state = controlador.reservar_tickets(
            self.user, dias, id_log, UNIDAD
        )
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
        source = "../../images/billetes/%sp.jpg" % (valor)
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
        controlador.insert_log(
            user,
            'salir',
            UNIDAD,
            'Billete trabado - bloqueo'
        )
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
                categoria = self.data['categoria'].decode('utf8')
                ticket_data['categoria'] = categoria
                ticket_data['facultad'] = self.data['facultad'].decode('utf8')
                ticket_data['unidad'] = str(UNIDAD)
                mensaje = u"Gracias por usar el Comedor Universitario"
                ticket_data['mensaje'] = mensaje
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
        get_bill_thread = Thread(
            target=self.leer_billetes,
            args=(self.cola_billetes,)
        )
        get_bill_thread.daemon = True
        get_bill_thread.start()
        status = {'security': 0, 'enable': 0, 'communication': 0, 'inhibit': 0}
        self.cola_estado = Queue()
        self.cola_estado.put(status)
        bill_thread = Thread(
            target=billetes.pool,
            args=(
                self.cola_billetes,
                self.cola_bool,
                self.cola_stop,
                self.faltante,
                self.cola_estado, 8
            )
        )
        bill_thread.daemon = True
        bill_thread.start()

    def cancel(self):
        """Vuelve a una pantalla anterior"""
        self.stop.set()
        self.cola_stop.put(True)
        if self.total_parcial:
            total = self.total_parcial
            log = controlador.insert_log(
                self.user,
                'cargar',
                UNIDAD,
                str(self.total_parcial)
            )
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
                print_thread = Thread(
                    target=impresora.imprimir_ticket_carga,
                    args=(nom, dni, fac, cat, code, unit, log, msj, pco, sdo)
                )
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
        self.reserva, full, state = controlador.reservar_tickets(
            self.user, dias, id_log, UNIDAD
        )
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
        self.popup = Popup(
            title="Advertencia",
            content=content,
            size_hint=(None, None),
            size=(400, 400),
            auto_dismiss=False
        )
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
                categoria = self.data['categoria'].decode('utf8')
                ticket_data['categoria'] = categoria
                ticket_data['facultad'] = self.data['facultad'].decode('utf8')
                ticket_data['unidad'] = str(UNIDAD)
                mensaje = u"Gracias por usar el Comedor Universitario"
                ticket_data['mensaje'] = mensaje
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
                self.manager.add_widget(
                    ConfirmacionScreen(len(self.reserva), name='confirmacion')
                )
                self.manager.current = 'confirmacion'
                if self.manager.has_screen('compra_2'):
                    self.manager.remove_widget(
                        self.manager.get_screen('compra_2')
                    )
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

    def __init__(self, cantidad, **kwargs):
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
