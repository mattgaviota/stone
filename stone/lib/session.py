#-*- coding: utf-8 -*-


class Session():

    def init(self, user, time):
        '''Clase para el manejo de la sesion del usuario'''
        self.user = user
        self.init_time = time

    def get_user(self):
        '''Retorna el usuario logueado actual'''
        return self.user

    def get_init_time(self):
        '''Retorna la hora cuando se inició la sesión'''
        return self.init_time

    def update(self, user):
        '''Actualiza el usuario logueado actual'''
        self.user = user

    def close(self):
        '''cierra la sesion'''
        self.user = None

    def is_open(self):
        '''Devuelve verdadero si la sesion está activa'''
        if self.user:
            return True
        else:
            return False
