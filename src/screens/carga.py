#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from threading import Thread, Event
from Queue import Queue, Empty
from lib import billetes
from db import controlador
from src.settings import user_session, UNIDAD
from src.alerts import WarningPopup
from bloqueo import BloqueoScreen
from time import sleep
from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread


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
