#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2015
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
from db import controlador
from kivy.uix.screenmanager import Screen


class AyudaScreen(Screen):

    def __init__(self, **kwargs):
        """Pantalla para mostrar la ayuda"""
        self.data = {}
        self.cargar_datos()
        super(AyudaScreen, self).__init__(**kwargs)

    def cargar_datos(self):
        """Carga los datos de los videos dentro de la pantalla de ayuda."""
        self.data['titulo'] = 'Ningún video cargado'
        self.playlist = controlador.get_videos()

    def play(self, source):
        """Reproduce el video del playlist correspondiente al source."""
        self.ids.player.play = False
        self.ids.titulo.text = self.playlist[source][1]
        self.ids.player.source = self.playlist[source][0]
        self.ids.player.play = True

    def cancel(self):
        """Vuelve a una pantalla anterior"""
        self.manager.current = 'splash'
