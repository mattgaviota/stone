#-*- coding: utf-8 -*-
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


class GrupalesScreen(Screen):

    def __init__(self, **kwargs):
        """ Pantalla para reimprimir tickets de cierre antiguos. """
        super(GrupalesScreen, self).__init__(**kwargs)
        self.cargar_datos()

    def cargar_datos(self):
        """ Carga los datos de los días. """
        self.categorias = controlador.get_categorias()
        self.unidades = controlador.get_all_facultades()
        self.ids.year.values = ['2015', '2016', '2017', '2018', '2019']
        self.ids.mes.values = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',\
                    'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',\
                     'Noviembre', 'Diciembre']
        self.ids.dia.values = [str(i) for i in range(1, 32)]
        self.ids.categorias.values = sorted(self.categorias.keys())
        self.ids.categorias.text = 'Regular'
        date = datetime.today()
        self.ids.year.text = str(date.year)
        self.ids.mes.text = self.ids.mes.values[date.month - 1]
        self.ids.dia.text = str(date.day)

    def confirmacion(self):
        content = ConfirmPopup(
                    text='\rSeguro deseas comprar el \r\n ticket grupal?')
        content.bind(on_answer=self._on_answer)
        self.popup = Popup(title="Advertencia",
                                content=content,
                                size_hint=(None, None),
                                size=(400,400),
                                auto_dismiss= False)
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
        cant = int(self.ids.cantidad.text)
        delegacion = self.ids.delegacion.text
        recibo = self.ids.recibo.text
        cat = (self.categorias[self.ids.categorias.text],
                                                    self.ids.categorias.text)
        try:
            date = datetime(year, mes, dia)
            if date >= datetime.now():
                self.print_ticket_grupal(cant, delegacion, cat, date, recibo)
            else:
                mensaje = u"Fecha Inválida"
                WarningPopup(mensaje).open()
        except ValueError:
            mensaje = u"Fecha Inválida"
            WarningPopup(mensaje).open()

    def print_ticket_grupal(self, cant, delegacion, cat, date, recibo):
        """
        Imprime el ticket grupal para el día(date), para la delegación
        dada y la cantidad solicitada.
        """
        user = user_session.get_user()
        id_log = controlador.insert_log(user, 'comprar_grupal', UNIDAD)
        ticket_grupal = controlador.comprar_ticket_grupal(cant, delegacion,
                                                    cat, date, recibo, id_log)
        row = controlador.get_ticket_grupal_by_id(ticket_grupal)
        id_log = controlador.insert_log(user, 'imprimir_grupal', UNIDAD)
        controlador.insert_ticket_log(ticket_grupal, id_log)
        print_thread = Thread(target=impresora.imprimir_ticket_grupal,
                            args=(
                                user['nombre'],
                                user['dni'],
                                row['id'],
                                UNIDAD,
                                row['fecha'].strftime('%d/%m/%Y'),
                                row['cantidad'],
                                row['barcode'],
                                row['importe'],
                                row['delegacion'],
                                row['recibo']
                            )
                        )
        print_thread.start()
        Window.release_all_keyboards()
        self.cancel()

    def cancel(self):
        """Vuelve a la pantalla anterior"""
        self.manager.current = 'servicios'
        self.manager.remove_widget(self.manager.get_screen('grupales'))
