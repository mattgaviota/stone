# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from datetime import datetime
from db import controlador
from src.settings import user_session, UNIDAD
from src.alerts import WarningPopup, ConfirmPopup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


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
                fecha = controlador.has_ticket(
                    self.user,
                    self.ids.id_ticket.text
                )
                hora_max = controlador.get_hora_anulacion()
                if fecha:
                    codigo = self.check_hora(fecha, hora_max)
                    if codigo == 1:
                        return fecha.strftime('%d/%m/%Y')  # anular
                    elif codigo == 0:
                        self.ids.id_ticket.text = ""
                        self.ids.id_ticket.focus = True
                        mensaje = "\rNo puede anular un ticket\r\n"
                        mensaje += "despues de las %d hs." % (hora_max)
                        WarningPopup(mensaje).open()
                        return 0  # nada
                    else:
                        self.ticket_vencido()
                        self.ids.id_ticket.text = ""
                        self.ids.id_ticket.focus = True
                        mensaje = "\rNo puede anular un ticket\r\n despues"
                        mensaje += "de la fecha\r\n de servicio.\r\n\r\n"
                        mensaje += "Su ticket se venció."
                        WarningPopup(mensaje).open()
                        return 0  # vencer
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
            self.popup = ConfirmPopup(
                text='\rSeguro deseas anular el ticket\r\n del día %s?' %
                (self.fecha)
            )
            self.popup.bind(on_answer=self._on_answer)
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
            return 1  # Ok (anular)
        elif ahora.date() > fecha.date():
            return 2  # Fecha anterior al día de hoy(vencer).
        else:
            if hora <= ahora.hour < 15:
                return 0  # Hora invalida para anular (Nada)
            elif ahora.hour < hora:
                return 1  # Ok (anular)
            else:
                return 2  # Hora posterior al permitido.(vencer)

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
