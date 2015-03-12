#-*- coding: utf-8 -*-

from time import sleep
from printer import Printer

def imprimir_ticket_alumno(nom, dni, fac, cat, code, unit, tkt, date, msj):
    '''Imprime el ticket de alumnos'''
    printer = Printer()
    printer.print_ticket_alumno(nom, dni, fac, cat, code, unit, tkt, date, msj)
    sleep(1)
    printer.disconnect()

def imprimir_ticket_cierre(nom, tkt, unit, hora, bills, total, code):
    '''Imprime el ticket de cierre'''
    printer = Printer()
    printer.print_ticket_cierre(nom, tkt, unit, hora, bills, total, code)
    sleep(1)
    printer.disconnect()

def imprimir_ticket_carga(nom, dni, fac, cat, code, unit, log, msj, pco):
    '''Imprime el ticket de carga'''
    printer = Printer()
    printer.print_ticket_carga(nom, dni, fac, cat, code, unit, log, msj, pco)
    sleep(1)
    printer.disconnect()

def check_status():
    '''Chequea el estado de la impresora'''
    #printer = Printer()
    #state = printer.get_status()
    #if state != 1:
        #state = printer.get_status()
    #return state
    #printer.disconnect()
    return 1
