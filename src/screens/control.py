# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
import os
from db import controlador
from src.settings import user_session, UNIDAD
from src.alerts import ConfirmPopup
from service import ServiceScreen
from kivy.uix.screenmanager import Screen


class ControlScreen(Screen):
    """Pantalla de menú de control"""

    def iniciar(self):
        """Accede a la pantalla principal del sistema"""
        user = user_session.get_user()
        hora = controlador.get_hora_inicio(UNIDAD)
        retiro = controlador.get_log(UNIDAD, 'retiro')
        if not hora:
            controlador.insert_log(user, 'iniciar', UNIDAD, '1er control')
        else:
            controlador.insert_log(user, 'iniciar', UNIDAD, 'control')
        user_session.close()
        self.manager.current = 'splash'

    def servicios(self):
        """Crea y accede a la pantalla de servicios"""
        if not self.manager.has_screen('servicios'):
            self.manager.add_widget(ServiceScreen(name='servicios'))  # TODO
        self.manager.current = 'servicios'

    def confirmacion_apagar(self):
        content = ConfirmPopup(
                    text='\rSeguro deseas salir y apagar\r\n la maquina?')
        content.bind(on_answer=self._on_answer_apagar)
        self.popup = Popup(
            title="Advertencia",
            content=content,
            size_hint=(None, None),
            size=(400, 400),
            auto_dismiss=False
        )
        self.popup.open()

    def _on_answer_apagar(self, instance, answer):
        if answer:
            self.apagar()
        self.popup.dismiss()

    def confirmacion_reiniciar(self):
        content = ConfirmPopup(
                    text='\rSeguro deseas salir y reiniciar\r\n la maquina?')
        content.bind(on_answer=self._on_answer_reiniciar)
        self.popup = Popup(
            title="Advertencia",
            content=content,
            size_hint=(None, None),
            size=(400, 400),
            auto_dismiss=False
        )
        self.popup.open()

    def _on_answer_reiniciar(self, instance, answer):
        if answer:
            self.reiniciar()
        self.popup.dismiss()

    def reiniciar(self):
        """Cierra la sesion y apaga la maquina"""
        user = user_session.get_user()
        controlador.insert_log(user, 'apagar', UNIDAD, 'Control - reinicio')
        user_session.close()
        controlador.update_all_activos()
        os.system("/sbin/shutdown -r now")

    def apagar(self):
        """Cierra la sesion y apaga la maquina"""
        user = user_session.get_user()
        controlador.insert_log(user, 'apagar', UNIDAD, 'Control')
        user_session.close()
        controlador.update_all_activos()
        os.system("/sbin/shutdown -h now")
