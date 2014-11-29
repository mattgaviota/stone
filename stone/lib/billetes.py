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
    if manager.ivizion.is_connected():
        resp = manager.get_status()
        if resp in ('40', '41', '42'):
            manager.send_command()
            sleep(3)


def pool(cola_billetes, cola_bool, cola_stop, a_ingresar, cola_estado, time):
    manager = Manager()
    total = 0
    resp = manager.get_status()
    while True: #manager.ivizion.is_connected():
        print 'entrando al ciclo'
        print 'respuesta: ' + resp
        if resp in ('1b', '11', '1a'):
            status = cola_estado.get()
            print status
            print 'entrando por 1b 11 1a'
            print status['security']
            if status['security'] == NOT_SENT:
                print 'entrando por securitystatus'
                status['security'] = SENDING
                print status['security']
                print status
                cola_estado.put(status)
                manager.send_command(LNG_7, SECURITY, '00', '00')
            elif status['enable'] == NOT_SENT:
                print 'entrando por enablestatus'
                status['enable'] = SENDING
                print status
                cola_estado.put(status)
                manager.send_command(LNG_7, ENABLE, '00', '00')
            elif status['communication'] == NOT_SENT:
                print 'entrando por communicationstatus'
                status['communication'] = SENDING
                print status
                cola_estado.put(status)
                manager.send_command(LNG_6, COMMUNICATION, '00', '')
            elif status['inhibit'] == NOT_SENT:
                print 'entrando por inhibitstatus'
                status['inhibit'] = SENDING
                print status
                cola_estado.put(status)
                manager.send_command(LNG_6, INHIBIT, '00', '')
            else:
                print 'entrando por else de 1b 11 1a'
                resp = manager.get_status()
            print 'saliendo de 1b 11 1a'
            resp = manager.get_status()
        elif resp == '13':
            print 'entrando por 13'
            valor = manager.get_escrow()
            sent_time = time()
            cola_billetes.put(valor)
            manager.send_command(cmd=HOLD)
        elif resp in ['14', '15']: # stacking and vend_valid
            print 'entrando por 14 15'
            manager.send_command(cmd=ACK) # send ack response to vend valid
            resp = manager.get_status()
            manager.send_command(cmd=INHIBIT, data1='01')
        elif resp == '16': # stacked
            print 'entrando por 16'
            resp = manager.get_status() # status request
        elif resp == '19': # added to keep holding
            print 'entrando por 19'
            elapsed_time = time()
            if int(elapsed_time - sent_time) >= time:
                if stackbill == 1:
                    manager.send_command(cmd=STACK_1) # stack 1
                    total += valor
                    time = 15
                elif stackbill == 2:
                    manager.send_command(cmd=STACK_2) # stack 2
                    total += valor
                    time = 15
                elif stackbill == 0:
                    manager.send_command(cmd=RETURN) # return bill
                else:
                    resp = manager.get_status() # else ask for status
            else:
                manager.send_command(cmd=HOLD)
        elif resp == '4a': # communication error
            print 'entrando por 4a'
            resp = manager.get_status() # status request
        else:
            resp = manager.get_status()


        print 'entrando al control'
        if total >= a_ingresar:
            print 'entrando a total > ingresar'
            cola_billetes.task_done()
            manager.send_command(LNG_6, INHIBIT, '01', '')
            manager.ivizion.disconnect()
            return
        else:
            print 'entrando a preguntar por stop'
            try:
                print "obteniendo de la cola_stop"
                stop = cola_stop.get()
            except Empty:
                print "cola_stop vacia"
                stop = False
            print stop
            if stop:
                print "entrando a stop"
                manager.send_command(LNG_6, INHIBIT, '01', '')
                manager.ivizion.disconnect()
                print "saliendo de pool"
                return
            else:
                print "entrando a preguntar por band"
                try:
                    print "obteniendo de la cola_bool"
                    band = cola_bool.get()
                except Empty:
                    print "cola_bool vacia"
                    band = False
                if band:
                    print 'entrando a band'
                    stackbill = 1
                    time = 1
                    cola_bool.task_done()
                else:
                    print 'entrando por else, get status'
                    resp = manager.get_status()
        print 'saliendo del ciclo'
        sleep(1)
