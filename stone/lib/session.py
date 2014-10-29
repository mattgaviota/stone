#-*- coding: utf-8 -*-


class Session():

    def init(self, user):
        '''Clase para el manejo de la sesion del usuario'''
        self.user = user

    def get_user(self):
        '''devuelve el usuario actual'''
        return self.user

    def close(self):
        '''cierra la sesion'''
        self.user = None

    def is_open(self):
        '''Devuelve verdadero si la sesion está activa'''
        if self.user:
            return True
        else:
            return False
