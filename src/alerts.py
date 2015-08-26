# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html

from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty


class ConfirmPopup(Popup):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


class WarningPopup(Popup):
    """Ventana Popup para mostrar los mensajes"""
    def __init__(self, mensaje, **kwargs):
        self.mensaje = mensaje
        super(WarningPopup, self).__init__(**kwargs)
