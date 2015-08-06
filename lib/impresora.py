# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html

from time import sleep, strftime, localtime
from printer import Printer


def imprimir_ticket_alumno(
        nombre,
        dni,
        facultad,
        categoria,
        code,
        unidad,
        ticket,
        date,
        mensaje,
        saldo
        ):
    '''Imprime el ticket de alumnos'''
    printer = Printer()
    printer.print_ticket_alumno(
        nombre,
        dni,
        facultad,
        categoria,
        code,
        unidad,
        ticket,
        date,
        mensaje,
        saldo
    )
    sleep(1)
    printer.disconnect()


def imprimir_tickets_alumno(*lista_tickets):
    '''Imprime una lista de tickets de un alumno'''
    printer = Printer()
    for ticket in lista_tickets:
        printer.print_ticket_alumno(
            ticket['nombre'],
            ticket['dni'],
            ticket['facultad'],
            ticket['categoria'],
            ticket['code'],
            ticket['unidad'],
            ticket['ticket'],
            ticket['fecha'],
            ticket['mensaje'],
            ticket['saldo']
        )
        sleep(0.5)
    printer.disconnect()


def imprimir_ticket_cierre(
        nombre,
        ticket,
        unidad,
        hora,
        billetes,
        total,
        code,
        dia=strftime("%d/%m/%Y", localtime())
        ):
    '''Imprime el ticket de cierre'''
    printer = Printer()
    printer.print_ticket_cierre(
        nombre,
        ticket,
        unidad,
        hora,
        billetes,
        total,
        code,
        dia
    )
    sleep(1)
    printer.disconnect()


def imprimir_ticket_carga(
        nombre,
        dni,
        facultad,
        categoria,
        code,
        unidad,
        log,
        mensaje,
        total,
        saldo
        ):
    '''Imprime el ticket de carga'''
    printer = Printer()
    printer.print_ticket_carga(
        nombre,
        dni,
        facultad,
        categoria,
        code,
        unidad,
        log,
        mensaje,
        total,
        saldo
    )
    sleep(1)
    printer.disconnect()


def imprimir_ticket_grupal(
        nombre,
        dni,
        id_ticket,
        unidad,
        date,
        cantidad,
        codigo,
        importe,
        delegacion,
        recibo
        ):
    '''Imprime el ticket grupal'''
    printer = Printer()
    printer.print_ticket_grupal(
        nombre,
        dni,
        id_ticket,
        unidad,
        date,
        cantidad,
        codigo,
        importe,
        delegacion,
        recibo,
        'Gracias por usar el Comedor Universitario'
    )
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
