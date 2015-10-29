# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from lib import impresora
from db import controlador
from src.settings import user_session, UNIDAD
from src.alerts import WarningPopup
from compra import Compra1Screen
from opciones import OptionScreen
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


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
            controlador.update_papel_disponible(UNIDAD, 2, 80)
            if not self.manager.has_screen('compra_1'):
                self.manager.add_widget(Compra1Screen(name='compra_1'))
            self.manager.current = 'compra_1'
        elif estado == 2:
            controlador.update_estado_maquina(UNIDAD, 4)
            if controlador.get_papel_disponible(UNIDAD) >= 5:
                if not self.manager.has_screen('compra_1'):
                    self.manager.add_widget(Compra1Screen(name='compra_1'))
                self.manager.current = 'compra_1'
            else:
                controlador.update_estado_maquina(UNIDAD, 2)
                mensaje = u"\rLa maquina no tiene papel."
                WarningPopup(mensaje).open()
        else:
            controlador.update_estado_maquina(UNIDAD, 5)
            mensaje = u"\rLa impresora está desconectada."
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
