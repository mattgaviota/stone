#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
# Utility import
from threading import Thread
# intra-packages imports
from db import controlador
from src.settings import UNIDAD
from lib import billetes
# screens
from src.screens.splash import SplashScreen
from src.screens.menu import MenuScreen
from src.screens.form import FormScreen
from src.screens.login import LoginScreen
from src.screens.ayuda import AyudaScreen
from src.screens.control import ControlScreen
# Kivy related imports
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, WipeTransition


class TicketApp(App):

    def build(self):
        # Cargamos el archivo con la interfaz
        Builder.load_file('kv/ticket.kv')
        # Creamos el screen manager con la WipeTransition
        sm = ScreenManager(transition=WipeTransition())
        # Agregamos las pantallas fijas del sistema
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(FormScreen(name='formulario'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AyudaScreen(name='ayuda'))
        sm.add_widget(ControlScreen(name='menu_control'))
        return sm


if __name__ == '__main__':
    controlador.insert_log({'dni': '222'}, 'iniciar', UNIDAD, 'Pre Inicio')
    init_thread = Thread(target=billetes.init)
    init_thread.daemon = True
    init_thread.start()
    TicketApp().run()
