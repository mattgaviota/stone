#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from src.settings import user_session
from src.alerts import WarningPopup
from carga import CargaScreen
from anular import AnularScreen
from perfil import ProfileScreen
from kivy.uix.screenmanager import Screen


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
