# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from threading import Thread
from datetime import datetime
from db import controlador
from lib import impresora
from src.settings import user_session, UNIDAD
from src.alerts import ConfirmPopup, WarningPopup
from kivy.uix.screenmanager import Screen


class CierreScreen(Screen):

    def __init__(self, **kwargs):
        """ Pantalla para reimprimir tickets de cierre antiguos. """
        super(CierreScreen, self).__init__(**kwargs)
        self.cargar_datos()

    def cargar_datos(self):
        """ Carga los datos de los días. """
        self.unidades = controlador.get_all_facultades()
        self.ids.year.values = ['2015', '2016', '2017', '2018', '2019']
        self.ids.mes.values = [
            'Enero', 'Febrero', 'Marzo', 'Abril',
            'Mayo', 'Junio', 'Julio', 'Agosto',
            'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        self.ids.dia.values = [str(i) for i in range(1, 32)]
        self.ids.unidad.values = sorted(self.unidades.keys())
        self.ids.unidad.text = controlador.get_ubicacion(UNIDAD)
        date = datetime.today()
        self.ids.year.text = str(date.year)
        self.ids.mes.text = self.ids.mes.values[date.month - 1]
        self.ids.dia.text = str(date.day)

    def confirmacion(self):
        self.popup = ConfirmPopup(
            text='\rSeguro deseas imprimir el \r\n ticket de cierre?'
        )
        self.popup.bind(on_answer=self._on_answer)
        self.popup.open()

    def _on_answer(self, instance, answer):
        if answer:
            self.check_fecha()
        self.popup.dismiss()

    def check_fecha(self):
        """ Verifica que la fecha sea correcta y menor o igual a la actual. """
        year = int(self.ids.year.text)
        mes = self.ids.mes.values.index(self.ids.mes.text) + 1
        dia = int(self.ids.dia.text)
        unidad = controlador.get_maquina_ubicacion(
            self.unidades[self.ids.unidad.text]
        )
        try:
            date = datetime(year, mes, dia)
            if date <= datetime.now():
                self.print_ticket_cierre(unidad, date)
            else:
                mensaje = u"Fecha Inválida"
                WarningPopup(mensaje).open()
        except ValueError:
            mensaje = u"Fecha Inválida"
            WarningPopup(mensaje).open()

    def print_ticket_cierre(self, unidad, date):
        """ Imprime el ticket de cierre de la unidad y del día(date) dado """
        total, bills = controlador.get_total(unidad, date)
        user = user_session.get_user()
        desc = 'Control - Cierre de la maquina %d del dia %s' % (
            unidad, date.strftime('%d/%m/%Y')
        )
        id_log = controlador.insert_log(user, 'retiro', unidad, desc)
        id_ticket = controlador.get_id_ticket_cierre(unidad, date)
        if not id_ticket:
            id_ticket = controlador.insert_ticket_cierre(
                id_log, total, unidad
            )
        ticket = controlador.get_ticket_cierre(id_ticket)
        hora = controlador.get_hora_inicio(unidad, date)
        print_thread = Thread(
            target=impresora.imprimir_ticket_cierre,
            args=(
                user['nombre'],
                id_ticket,
                unidad,
                hora,
                bills,
                total,
                ticket['barcode'],
                date.strftime('%d/%m/%Y')
            )
        )
        print_thread.start()

    def cancel(self):
        """Vuelve a la pantalla anterior"""
        self.manager.current = 'servicios'
        self.manager.remove_widget(self.manager.get_screen('cierre'))
