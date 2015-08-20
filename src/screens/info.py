# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from threading import Thread, Event
from Queue import Queue, Empty
from datetime import datetime
from time import sleep
from db import controlador
from lib import impresora, utils, billetes
from src.settings import user_session, UNIDAD, VERSION
from src.alerts import ConfirmPopup, WarningPopup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import mainthread


class InfoScreen(Screen):

    def __init__(self, **kwargs):
        """Pantalla para revisar la información referida a la maquina"""
        self.stop = Event()
        self.pressed = False
        super(InfoScreen, self).__init__(**kwargs)
        carga_thread = Thread(target=self.cargar_datos)
        carga_thread.daemon = True
        carga_thread.start()

    def cargar_datos(self):
        """Carga los datos de la maquina"""
        ubicacion = controlador.get_ubicacion(UNIDAD)
        self.ids.ubicacion.text = ubicacion
        self.ids.unidad.text = str(UNIDAD)
        self.ids.version.text = VERSION
        date = datetime.today()
        hora_inicio = controlador.get_hora_inicio(UNIDAD, date)
        hora_cierre = controlador.get_hora_cierre(UNIDAD, date)
        if hora_inicio:
            self.ids.hora_inicio.text = hora_inicio
        else:
            self.ids.hora_inicio.text = u"El sistema no ha iniciado"
        if hora_cierre:
            self.ids.hora_cierre.text = hora_cierre
        else:
            self.ids.hora_cierre.text = u"El sistema no ha cerrado"
        self.try_conexion()
        self.try_papel()

    def try_conexion(self):
        """Verifica la conexión con la BD e Internet"""
        self.ids.conexion.text = "probando..."
        sleep(0.5)
        try:
            categoria = controlador.get_categoria_id('Regular')
        except:
            categoria = None
        if utils.internet_on():
            if categoria:
                self.ids.conexion.text = u"\rBD On\r\nInternet On"
                controlador.update_estado_maquina(UNIDAD, 1)
            else:
                self.ids.conexion.text = u"\rBD Off\r\nInternet On"
                controlador.update_estado_maquina(UNIDAD, 5)
        else:
            if categoria:
                self.ids.conexion.text = u"\rBD On\r\nInternet Off"
                controlador.update_estado_maquina(UNIDAD, 1)
            else:
                self.ids.conexion.text = u"\rBD Off\r\nInternet On"
                controlador.update_estado_maquina(UNIDAD, 5)

    def try_papel(self):
        """Verifica el estado del papel en la maquina."""
        self.ids.papel.text = "probando..."
        sleep(0.5)
        estado = impresora.check_status()
        if estado == 1:
            self.ids.papel.text = u"\rImpresora Conectada\r\nPapel Ok"
            controlador.update_estado_maquina(UNIDAD, 1)
        elif estado == 2:
            self.ids.papel.text = u"\rImpresora Conectada\r\nSin Papel"
            controlador.update_estado_maquina(UNIDAD, 4)
        else:
            self.ids.papel.text = u"\rImpresora No Conectada"
            controlador.update_estado_maquina(UNIDAD, 2)

    @mainthread
    def update_ingreso(self, valor):
        """
        Muestra la imagen del billete ingresado y habilita el botón de
        confirmación.
        """
        source = "../../images/billetes/%sp.jpg" % (valor)
        self.ids.ingresado.source = source

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
                    self.update_ingreso(str(self.valor))
                else:
                    self.update_ingreso("no")
            sleep(0.1)

    def cargar_threads(self):
        """
        Carga e inicia los hilos que manejan la maquina verificadora de
        billetes.
        """
        self.cola_bool = Queue()
        self.cola_stop = Queue()
        self.cola_billetes = Queue()
        self.faltante = 100
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
                self.cola_estado,
                4
            )
        )
        bill_thread.daemon = True
        bill_thread.start()

    def try_billetes(self):
        """Activa la impresora para probar su funcionamiento"""
        if self.pressed:
            self.stop.set()
            self.cola_stop.put(True)
            self.pressed = False
            self.ids.try_billetes.state = 'normal'
            self.update_ingreso("no")
        else:
            self.pressed = True
            self.ids.try_billetes.state = 'down'
            self.cargar_threads()

    def cancel(self):
        """Vuelve a la pantalla anterior"""
        try:
            self.stop.set()
            self.cola_stop.put(True)
            self.pressed = False
        except AttributeError:
            pass
        self.manager.current = 'servicios'
