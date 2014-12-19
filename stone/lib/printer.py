#!/usr/bin/env python
# -*- coding: utf-8 -*-

# las páginas se refieren al archivo comandos de impresora en la carpeta doc/

from tup500 import Tup500
from time import sleep, strftime, localtime, mktime


class Printer():

    def __init__(self):
        self.tup = Tup500()
        self.tup.connect()

    def get_tup(self):
        return self.tup

    def to_int(self, lststr, base=16):
        lst = []
        for item in lststr:
            lst.append(int(item, base))
        return lst

    def print_ticket_cierre(self, administrador):
        unidad = '03'
        ticket = '000346'
        operacion = '0000012346'
        # Header
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '01']))) # center alignment pag 50
        self.tup.send(bytearray(self.to_int(['1b', '1c', '70', '01', '00']))) # print logo pag 59
        self.tup.send(bytearray("\r\n"))
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '00']))) # left alignment pag 50
        self.tup.send(bytearray(self.to_int(['1b', '44', '22', '00']))) # Set Horizontal tab pag 48
        dia = strftime("%d/%m/%Y", localtime())
        self.tup.send(bytearray("Fecha %s" % (dia)))
        hora = strftime("%H:%M", localtime())
        self.tup.send(bytearray(" \x09 Hora %s\r\n" % (hora)))
        self.tup.send(bytearray(self.to_int(['1b', '44', '20', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("Nro Cierre: %s" % (ticket))) 
        self.tup.send(bytearray(" \x09 Terminal: %s\r\n" % (unidad)))
        self.tup.send(bytearray("----------------------------------------------\r\n\r\n"))
        # end Header
        # Body
        u_becados = 20
        u_regulares = 15
        u_gratis = 5
        a_becados = 10
        a_regulares = 8
        a_gratis = 2
        coin_10 = 15
        coin_25 = 8
        coin_50 = 4
        coin_1 = 11
        coin_2 = 1
        bill_2 = 13
        bill_5 = 6
        bill_10 = 3
        bill_20 = 2
        bill_50 = 1
        bill_100 = 0
        self.tup.send(bytearray(u"\x1b\x34Administrador:\x1b\x35 %s\r\n\r\n" % (administrador), 'cp850'))
        self.tup.send(bytearray(self.to_int(['1b', '44', '04', '12', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray(self.to_int(['1b', '45']))) # Set emphasys
        self.tup.send(bytearray("\x1b\x2d\x01Usuarios\x1b\x2d\x00\r\n\r\n"))
        self.tup.send(bytearray(" Tipo \x09 Cantidad \x09 Total \r\n\r\n"))
        self.tup.send(bytearray(self.to_int(['1b', '44', '04', '14', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray(" Becados \x09 %d \x09 $ %.2f \r\n" % (u_becados, u_becados)))
        self.tup.send(bytearray(" Regulares \x09 %d \x09 $ %.2f \r\n" % (u_regulares, u_regulares * 5)))
        self.tup.send(bytearray(" Gratuitos  \x09 %d \x09 $ 0.00 \r\n\r\n" % (u_gratis)))
        self.tup.send(bytearray("\x1b\x2d\x01Anulados\x1b\x2d\x00\r\n\r\n"))
        self.tup.send(bytearray(" Becados \x09 %d \x09 $ %.2f \r\n" % (a_becados, a_becados)))
        self.tup.send(bytearray(" Regulares \x09 %d \x09 $ %.2f \r\n" % (a_regulares, a_regulares * 5)))
        self.tup.send(bytearray(" Gratuitos  \x09 %d \x09 $ 0.00 \r\n\r\n" % (a_gratis)))
        self.tup.send(bytearray("----------------------------------------------\r\n\r\n"))
        self.tup.send(bytearray(self.to_int(['1b', '44', '04', '12', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("\x1b\x2d\x01Monedas\x1b\x2d\x00\r\n\r\n"))
        self.tup.send(bytearray(" Valor \x09 Cantidad \x09 Total \r\n\r\n"))
        self.tup.send(bytearray(self.to_int(['1b', '44', '04', '14', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray(" 10 cvos. \x09 %d \x09 $ %.2f \r\n" % (coin_10, coin_10 * 0.10)))
        self.tup.send(bytearray(" 25 cvos. \x09 %d \x09 $ %.2f \r\n" % (coin_25, coin_25 * 0.25)))
        self.tup.send(bytearray(" 50 cvos.  \x09 %d \x09 $ %.2f \r\n" % (coin_50, coin_50 * 0.5)))
        self.tup.send(bytearray(" 1 peso  \x09 %d \x09 $ %.2f \r\n" % (coin_1, coin_1)))
        self.tup.send(bytearray(" 2 pesos  \x09 %d \x09 $ %.2f \r\n\r\n" % (coin_2, coin_2 * 2)))
        self.tup.send(bytearray(self.to_int(['1b', '44', '04', '12', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("\x1b\x2d\x01Billetes\x1b\x2d\x00\r\n\r\n"))
        self.tup.send(bytearray(" Valor \x09 Cantidad \x09 Total \r\n\r\n"))
        self.tup.send(bytearray(self.to_int(['1b', '44', '04', '14', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray(" 2 pesos \x09 %d \x09 $ %.2f \r\n" % (bill_2, bill_2 * 2)))
        self.tup.send(bytearray(" 5 pesos \x09 %d \x09 $ %.2f \r\n" % (bill_5, bill_5 * 5)))
        self.tup.send(bytearray(" 10 pesos  \x09 %d \x09 $ %.2f \r\n" % (bill_10, bill_10 * 10)))
        self.tup.send(bytearray(" 20 pesos  \x09 %d \x09 $ %.2f \r\n" % (bill_20, bill_20 * 20)))
        self.tup.send(bytearray(" 50 pesos  \x09 %d \x09 $ %.2f \r\n" % (bill_50, bill_50 * 50)))
        self.tup.send(bytearray(" 100 pesos  \x09 %d \x09 $ %.2f \r\n\r\n" % (bill_100, bill_100 * 100)))
        self.tup.send(bytearray("----------------------------------------------\r\n\r\n"))
        self.tup.send(bytearray(self.to_int(['1b', '46']))) # Cancel emphasys
        self.tup.send(bytearray(self.to_int(['1b', '44', '10', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("Total Usuarios \x09"))
        total_usuarios = u_becados + u_regulares * 5
        self.tup.send(bytearray(" \x09 $ %.2f \r\n" % (total_usuarios)))
        self.tup.send(bytearray("Total Anulados \x09"))
        total_anulados = a_becados + a_regulares * 5
        self.tup.send(bytearray(" \x09 $ %.2f \r\n\r\n" % (total_anulados)))
        self.tup.send(bytearray(self.to_int(['1b', '44', '8', '16', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray(self.to_int(['1b', '69', '01', '01']))) # Character expansion
        self.tup.send(bytearray("\x1b\x34Total\x1b\x35 \x09"))
        total = total_usuarios + total_anulados
        self.tup.send(bytearray(" \x09 $ %.2f\r\n\r\n" % (total)))
        self.tup.send(bytearray(self.to_int(['1b', '69', '00', '00']))) # Cancel Character expansion
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '01']))) # center alignment pag 50
        # end Body
        # Footer
        dia = int(mktime(localtime()))
        self.tup.send(bytearray(self.to_int(['1b', '62', '06', '02', '02']))) # Barcode pag 61
        self.tup.send(bytearray(" %d%s\x1e\r\n" % (dia, operacion))) # Barcode pag 61
        # end Footer
        self.tup.send(bytearray(self.to_int(['1b', '64', '02']))) # paper fed and full cut page 63
    
    
    def print_ticket_alumno(self, alumno, dni, facultad, categoria,
                                code, unit, id_ticket, fecha, mensaje):
        unidad = unit
        ticket = id_ticket
        # Header
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '01']))) # center alignment pag 50
        self.tup.send(bytearray(self.to_int(['1b', '1c', '70', '01', '00']))) # print logo pag 59
        self.tup.send(bytearray("\r\n"))
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '00']))) # left alignment pag 50
        self.tup.send(bytearray(self.to_int(['1b', '44', '22', '00']))) # Set Horizontal tab pag 48
        dia = strftime("%d/%m/%Y", localtime())
        self.tup.send(bytearray("Fecha %s" % (dia)))
        hora = strftime("%H:%M", localtime())
        self.tup.send(bytearray(" \x09 Hora %s\r\n" % (hora)))
        self.tup.send(bytearray(self.to_int(['1b', '44', '20', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("Nro ticket: %s" % (ticket))) 
        self.tup.send(bytearray(" \x09 Terminal: %s\r\n" % (unidad), 'cp850'))
        self.tup.send(bytearray("---------------------------------------------\r\n\r\n"))
        # end Header
        # Body
        self.tup.send(bytearray("\x1b\x34Fecha de Servicio: %s\x1b\x35\r\n\r\n" %(fecha)))
        self.tup.send(bytearray(self.to_int(['1b', '45']))) # Set emphasys
        self.tup.send(bytearray(u"Alumno: %s\r\n" %(alumno), 'cp850'))
        self.tup.send(bytearray(u"DNI: %s\r\n" %(dni), 'cp850'))
        self.tup.send(bytearray(u"Facultad: %s\r\n" % (facultad), 'cp850'))
        self.tup.send(bytearray(u"Categoria: %s\r\n\r\n" % (categoria), 'cp850'))
        self.tup.send(bytearray(self.to_int(['1b', '46']))) # Cancel emphasys
        if categoria == u"Regular":
            precio = 5
            precio_escrito = u"cinco"
        elif categoria == u"Becado":
            precio = 1
            precio_escrito = u"uno"
        elif categoria == u"Gratuito":
            precio = 0
            precio_escrito = u"cero"
        else:
            precio = u"None"
        self.tup.send(bytearray(self.to_int(['1b', '44', '10', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("Importe \x09"))
        self.tup.send(bytearray(" \x09 \x1b\x34$ %.2f\x1b\x35\r\n" % (precio)))
        self.tup.send(bytearray(u"Total pesos %s\r\n" % (precio_escrito), 'cp850'))
        self.tup.send(bytearray("---------------------------------------------\r\n\r\n"))
        # end Body
        # Footer
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '01']))) # center alignment pag 50
        self.tup.send(bytearray(u"%s \r\n" % (mensaje), 'cp850'))
        self.tup.send(bytearray(self.to_int(['1b', '62', '06', '02', '02']))) # Barcode pag 61
        self.tup.send(bytearray(" %s\x1e\r\n" % (code))) # Barcode pag 61
        # end Footer
        self.tup.send(bytearray(self.to_int(['1b', '64', '02']))) # paper fed and full cut page 63
