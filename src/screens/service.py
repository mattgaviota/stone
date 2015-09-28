# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from threading import Thread
from time import time
from db import controlador
from lib import impresora
from src.settings import user_session, UNIDAD
from src.alerts import WarningPopup, ConfirmPopup
from cierre import CierreScreen
from grupales import GrupalesScreen
from anularGrupal import AnularGrupalScreen
from info import InfoScreen
from kivy.uix.screenmanager import Screen


class ServiceScreen(Screen):
    """Pantalla de servicio de control"""

    def imprimir(self):
        """imprime un ticket de control"""
        print_status = impresora.check_status()
        papel_disponible = controlador.get_papel_disponible()
        if ((print_status == 1) or
                (print_status == 2 and papel_disponible >= 1)
            ):
            user = user_session.get_user()
            controlador.insert_log(
                user,
                'imprimir',
                UNIDAD,
                'Ticket de prueba'
            )
            fecha = "dd/mm/aaaa"
            code = str(int(time())) + "0000000000"
            nom = user['nombre']
            dni = user['dni']
            cat = u"control"
            fac = u"Secretaría de Bienestar"
            msj = u"Ticket NO VALIDO"
            sdo = 0
            ticket = "XXX"
            print_thread = Thread(
                target=impresora.imprimir_ticket_alumno,
                args=(
                    nom,
                    dni,
                    fac,
                    cat,
                    code,
                    UNIDAD,
                    ticket,
                    fecha,
                    msj,
                    sdo
                )
            )
            print_thread.start()
        elif estado == 2:
            mensaje = u"No hay papel"
            WarningPopup(mensaje).open()
        else:
            mensaje = u"Impresora desconectada"
            WarningPopup(mensaje).open()

    def confirmacion(self):
        self.popup = ConfirmPopup(
            text='\rSeguro deseas retirar\r\n e imprimir el ticket de cierre?'
        )
        self.popup.bind(on_answer=self._on_answer)
        self.popup.open()

    def _on_answer(self, instance, answer):
        if answer:
            self.retirar()
        self.popup.dismiss()

    def retirar(self):
        """
        Controla que se pueda hacer un ticket de cierre para poder
        retirar el dinero.
        """
        user = user_session.get_user()
        retiro = controlador.get_log(UNIDAD, 'retiro')
        hora = controlador.get_hora_inicio(UNIDAD)
        if not retiro and hora:
            total, bills = controlador.get_total(UNIDAD)
            if total:
                desc = 'Control - 1er Cierre'
                id_log = controlador.insert_log(user, 'retiro', UNIDAD, desc)
                id_ticket = controlador.insert_ticket_cierre(
                    id_log, total, UNIDAD
                )
                ticket = controlador.get_ticket_cierre(id_ticket)
                hora = controlador.get_hora_inicio(UNIDAD)
                print_thread = Thread(  #TODO control papel
                    target=impresora.imprimir_ticket_cierre,
                    args=(
                        user['nombre'],
                        id_ticket,
                        UNIDAD,
                        hora,
                        bills,
                        total,
                        ticket['barcode']
                    )
                )
                print_thread.start()
            else:
                mensaje = u"No hay rergistros para hoy"
                WarningPopup(mensaje).open()
        elif retiro and hora:
            total, bills = controlador.get_total(UNIDAD)
            if total:
                desc = 'Control - Cierre'
                id_log = controlador.insert_log(user, 'retiro', UNIDAD, desc)
                total, bills = controlador.get_total(UNIDAD)
                id_ticket = controlador.get_id_ticket_cierre(UNIDAD)
                if not id_ticket:
                    id_ticket = controlador.insert_ticket_cierre(
                        id_log, total, UNIDAD
                    )
                ticket = controlador.get_ticket_cierre(id_ticket)
                hora = controlador.get_hora_inicio(UNIDAD)
                print_thread = Thread(
                    target=impresora.imprimir_ticket_cierre,
                    args=(
                        user['nombre'],
                        id_ticket,
                        UNIDAD,
                        hora,
                        bills,
                        total,
                        ticket['barcode']
                    )
                )
                print_thread.start()
            else:
                mensaje = u"No hay rergistros para hoy"
                WarningPopup(mensaje).open()
        else:
            msje = u"\rNo puede hacer cierre\r\n sin iniciar antes el sistema."
            WarningPopup(msje).open()

    def informacion(self):
        """
        Crea y accede a la pantalla de información del estado de la maquina.
        """
        if not self.manager.has_screen('info'):
            self.manager.add_widget(InfoScreen(name='info'))
        self.manager.current = 'info'

    def tickets_cierre(self):
        """
        Crea y accede a la pantalla de impresión de tickets de cierre.
        """
        if not self.manager.has_screen('cierre'):
            self.manager.add_widget(CierreScreen(name='cierre'))
        self.manager.current = 'cierre'

    def tickets_grupales(self):
        """
        Crea y accede a la pantalla de impresión de tickets grupales.
        """
        if not self.manager.has_screen('grupales'):
            self.manager.add_widget(GrupalesScreen(name='grupales'))
        self.manager.current = 'grupales'

    def anular_grupal(self):
        """
        Crea y accede a la pantalla de anulación de tickets grupales.
        """
        if not self.manager.has_screen('anular_grupal'):
            self.manager.add_widget(AnularGrupalScreen(name='anular_grupal'))
        self.manager.current = 'anular_grupal'

    def cancel(self):
        """Vuelve a la pantalla anterior"""
        self.manager.current = 'menu_control'
        self.manager.remove_widget(self.manager.get_screen('servicios'))
