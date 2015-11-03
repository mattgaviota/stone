# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from lib.utils import internet_on
from db import controlador
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock


class SplashScreen(Screen):

    def __init__(self, **kwargs):
        """Pantalla de acceso - Pantalla principal"""
        self.disponibles = StringProperty()
        super(SplashScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_disponibles, 60)

    def update_disponibles(self, dt):
        """
        Revisa la cantidad de tickets disponibles y llama a la función que
        muestra el cartel.
        """
        tickets_disponibles = controlador.get_tickets_disponibles()
        self.update_labels(tickets_disponibles)

    def update_labels(self, tickets):
        """Actualiza el cartel con los tickets disponibles para la semana."""
        self.ids.dia1.text = tickets['dia1'][0]
        self.ids.dia2.text = tickets['dia2'][0]
        self.ids.dia3.text = tickets['dia3'][0]
        self.ids.dia4.text = tickets['dia4'][0]
        self.ids.dia5.text = tickets['dia5'][0]
        self.ids.fecha_dia1.text = tickets['dia1'][1]
        self.ids.fecha_dia2.text = tickets['dia2'][1]
        self.ids.fecha_dia3.text = tickets['dia3'][1]
        self.ids.fecha_dia4.text = tickets['dia4'][1]
        self.ids.fecha_dia5.text = tickets['dia5'][1]
        self.ids.cant_dia1.text = tickets['dia1'][2]
        self.ids.cant_dia2.text = tickets['dia2'][2]
        self.ids.cant_dia3.text = tickets['dia3'][2]
        self.ids.cant_dia4.text = tickets['dia4'][2]
        self.ids.cant_dia5.text = tickets['dia5'][2]

    def login(self):
        """ Ingresa a la pantalla de login """
        self.manager.current = "login"

    def registro(self):
        """ Ingresa a la pantalla de registro si hay internet. """
        if internet_on():
            self.manager.current = "formulario"
        else:
            msje = u"\rInternet sin conexión\r\n Intente nuevamente."
            WarningPopup(msje).open()
