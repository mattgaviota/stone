#-*- coding: utf-8 -*-

from threading import Thread
from Queue import Empty
from message import Message
from ivizion import Ivizion
from constant import *
from response import Response
from time import time, sleep


# Función para controlar los billetes que se ingresan
# en progreso...

class Manager():

    def __init__(self):
        self.ivizion = Ivizion()
        if not self.ivizion.is_connected():
            self.ivizion.connect()
        self.message = Message()
        self.response = Response()

    def send_command(self, lng=LNG_5, cmd=RESET, data1='', data2=''):
        self.message.update_message(lng=lng, cmd=cmd, data1=data1, data2=data2)
        msg = self.message.get_message()
        self.ivizion.send(msg)

    def get_status(self):
        self.message.update_message()
        msg = self.message.get_message()
        self.ivizion.send(msg)
        answer = self.ivizion.recipe()
        return answer[4:6]

    def show_status(self):
        self.message.update_message()
        msg = self.message.get_message()
        self.ivizion.send(msg)
        answer = self.ivizion.recipe()
        self.response.show_response(answer, REQ_STATUS)

    def get_escrow(self):
        self.message.update_message()
        msg = self.message.get_message()
        self.ivizion.send(msg)
        answer = self.ivizion.recipe()
        return self.response.get_escrow(answer)

def init():
    manager = Manager()
    sleep(0.2)
    if manager.ivizion.is_connected():
        resp = manager.get_status()
        if resp in ('40', '41', '42'):
            manager.send_command()
            sleep(3)


def pool(cola_billetes, cola_bool, cola_stop, a_ingresar,
            cola_estado, timeout):
    manager = Manager()
    total = 0
    stackbill = 0
    resp = manager.get_status()
    try:
        status = cola_estado.get(False)
    except Empty:
        status = None
    while manager.ivizion.is_connected():
        if resp in ('1b', '11', '1a'):
            if status['security'] == NOT_SENT:
                status['security'] = SENDING
                manager.send_command(LNG_7, SECURITY, '00', '00')
            elif status['enable'] == NOT_SENT:
                status['enable'] = SENDING
                manager.send_command(LNG_7, ENABLE, '00', '00')
            elif status['communication'] == NOT_SENT:
                status['communication'] = SENDING
                manager.send_command(LNG_6, COMMUNICATION, '00', '')
            elif status['inhibit'] == NOT_SENT:
                status['inhibit'] = SENDING
                manager.send_command(LNG_6, INHIBIT, '00', '')
            else:
                resp = manager.get_status()
            resp = manager.get_status()
        elif resp in ['14', '15']: # stacking and vend_valid
            manager.send_command(cmd=ACK) # send ack response to vend valid
            resp = manager.get_status()
            manager.send_command(cmd=INHIBIT, data1='01')
        elif resp == '16': # stacked
            resp = manager.get_status() # status request
        elif resp == '19': # added to keep holding
            elapsed_time = time()
            if int(elapsed_time - sent_time) >= timeout:
                if stackbill == 1:
                    manager.send_command(cmd=STACK_1) # stack 1
                    total += valor
                    sleep(0.1)
                    timeout = 10
                    stackbill = 0
                    valor = 0
                elif stackbill == 2:
                    manager.send_command(cmd=STACK_2) # stack 2
                    total += valor
                    sleep(0.1)
                    timeout = 10
                    stackbill = 0
                    valor = 0
                elif stackbill == 0:
                    cola_billetes.put(0)
                    manager.send_command(cmd=RETURN) # return bill
                    sleep(0.1)
                    timeout = 10
                    valor = 0
                else:
                    resp = manager.get_status() # else ask for status
            else:
                manager.send_command(cmd=HOLD)
        elif resp == '4a': # communication error
            resp = manager.get_status() # status request
        else:
            resp = manager.get_status()


        if resp == '13':
            valor = manager.get_escrow()
            sent_time = time()
            cola_billetes.put(valor)
            manager.send_command(cmd=HOLD)
        else:
            if total >= a_ingresar:
                manager.send_command(LNG_6, INHIBIT, '01', '')
                manager.ivizion.disconnect()
                return
            else:
                try:
                    stop_data = cola_stop.get(False)
                except Empty:
                    stop_data = False
                if stop_data:
                    manager.send_command(LNG_6, INHIBIT, '01', '')
                    manager.ivizion.disconnect()
                    return
                else:
                    try:
                        band = cola_bool.get(False)
                    except Empty:
                        band = 0
                    if band:
                        stackbill = 1
                        timeout = 0
                    else:
                        resp = manager.get_status()
        resp = manager.get_status()
        sleep(0.2)
