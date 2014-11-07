#-*- coding: utf-8 -*-

from printer import Printer

def imprimir_ticket_alumno(nom, dni, fac, cat, code, unit, ticket):
    printer = Printer()
    tup = printer.get_tup()
    msj = u"Gracias por usar el Comedor Universitario"
    if tup.is_connected():
        printer.print_ticket_alumno(nom, dni, fac, cat, code, unit, ticket, msj)
    tup.disconnect()
