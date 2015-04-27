#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
from time import sleep, strftime, localtime
from printer import Printer

def imprimir_ticket_alumno(nom, dni, fac, cat, code, unit, tkt, date, msj,
                                                                         sdo):
    '''Imprime el ticket de alumnos'''
    printer = Printer()
    printer.print_ticket_alumno(nom, dni, fac, cat, code, unit, tkt, date, msj,
                                                                        sdo)
    sleep(1)
    printer.disconnect()

def imprimir_tickets_alumno(*lista_tickets):
    '''Imprime una lista de tickets de un alumno'''
    printer = Printer()
    for ticket in lista_tickets:
        printer.print_ticket_alumno(ticket['nom'], ticket['dni'],
                                    ticket['fac'], ticket['cat'],
                                    ticket['code'], ticket['unit'],
                                    ticket['ticket'], ticket['fecha'],
                                    ticket['msj'], ticket['saldo'])
        sleep(0.5)
    printer.disconnect()

def imprimir_ticket_cierre(nom, tkt, unit, hora, bills, total, code,
                                        dia=strftime("%d/%m/%Y", localtime())):
    '''Imprime el ticket de cierre'''
    printer = Printer()
    printer.print_ticket_cierre(nom, tkt, unit, hora, bills, total, code, dia)
    sleep(1)
    printer.disconnect()

def imprimir_ticket_carga(nom, dni, fac, cat, code, unit, log, msj, pco, sdo):
    '''Imprime el ticket de carga'''
    printer = Printer()
    printer.print_ticket_carga(nom, dni, fac, cat, code, unit, log, msj, pco,
                                                                         sdo)
    sleep(1)
    printer.disconnect()

def cortar():
    printer = Printer()
    printer.feed_and_full_cut()
    printer.disconnect()

def check_status():
    '''Chequea el estado de la impresora'''
    printer = Printer()
    state = printer.get_status()
    if state != 1:
        state = printer.get_status()
    return state
    printer.disconnect()
