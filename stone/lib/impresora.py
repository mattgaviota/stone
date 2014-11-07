#-*- coding: utf-8 -*-

from time import sleep
from printer import Printer

def imprimir_ticket_alumno(nom, dni, fac, cat, code, unit, ticket, fecha):
    printer = Printer()
    tup = printer.get_tup()
    msj = u"Gracias por usar el Comedor Universitario"
    printer.print_ticket_alumno(nom, dni, fac, cat, code, unit, ticket,
                                                                    fecha, msj)
    sleep(1)
    tup.disconnect()
