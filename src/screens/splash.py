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
        self.update_label(tickets_disponibles)

    def update_label(self, tickets):
        """Actualiza el cartel con los tickets disponibles para el día."""
        self.disponibles = u"Tickets disponibles para hoy : %s" % (tickets)
        self.ids.disponibles.text = self.disponibles

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
