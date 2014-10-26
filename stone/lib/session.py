#-*- coding: utf-8 -*-


class Session():

    def init(self, user):
        self.user = user

    def get_user(self):
        return self.user

    def close(self):
        self.user = None

    def is_open(self):
        if self.user:
            return True
        else:
            return False
