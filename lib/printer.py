#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
# las páginas se refieren al archivo comandos de impresora en la carpeta doc/

from tup500 import Tup500
from time import sleep, strftime, localtime, mktime


class Printer():
    '''Clase que maneja la impresora'''
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

    def disconnect(self):
        self.tup.disconnect()

    def get_status(self):
        '''
        Obtiene el estado de la impresora y retorna un código.
            1 -> Online con papel
            2 -> Online sin papel
            3 -> Offline con algún error
        '''
        self.tup.send(bytearray(self.to_int(['1b', '06', '01'])))
        sleep(0.8)
        status = self.tup.recipe()
        offline = int(status[4:6], 16)
        error_mech = int(status[6:8], 16)
        error_jam = int(status[8:10], 16)
        paper = int(status[10:12], 16)
        if not offline:
            if not paper:
                return 1 # online y con papel
            else:
                if paper == 4:
                    return 2 # online y con papel por acabarse
                else:
                    return 2 # online y sin papel
        else:
            return 3 # offline y error
            #TODO especificación de error

    def print_ticket_cierre(self, user, id_ticket, unidad, inicio, bills,
                                                            total, code, dia):
        # Header
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '01']))) # center alignment pag 50
        self.tup.send(bytearray(self.to_int(['1b', '1c', '70', '01', '00']))) # print logo pag 59
        self.tup.send(bytearray("\r\n"))
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '00']))) # left alignment pag 50
        self.tup.send(bytearray(self.to_int(['1b', '44', '22', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("Fecha %s" % (dia)))
        hora = strftime("%H:%M", localtime())
        self.tup.send(bytearray(" \x09 Hora %s\r\n" % (hora)))
        self.tup.send(bytearray(self.to_int(['1b', '44', '20', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("Nro Cierre: %s" % (id_ticket))) 
        self.tup.send(bytearray(" \x09 Terminal: %d\r\n" % (unidad)))
        self.tup.send(bytearray("----------------------------------------------\r\n\r\n"))
        # end Header
        # Body
        bill_2 = bills[2]
        bill_5 = bills[5]
        bill_10 = bills[10]
        bill_20 = bills[20]
        bill_50 = bills[50]
        bill_100 = bills[100]
        self.tup.send(bytearray(u"\x1b\x34Administrador:\x1b\x35 %s\r\n\r\n" % (user), 'cp850'))
        self.tup.send(bytearray(u"\x1b\x34Hora de inicio:\x1b\x35 %s\r\n\r\n" % (inicio), 'cp850'))
        self.tup.send(bytearray(self.to_int(['1b', '44', '04', '12', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray(self.to_int(['1b', '45']))) # Set emphasys
        self.tup.send(bytearray("----------------------------------------------\r\n\r\n"))
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
        self.tup.send(bytearray(self.to_int(['1b', '44', '8', '16', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray(self.to_int(['1b', '69', '01', '01']))) # Character expansion
        self.tup.send(bytearray("\x1b\x34Total\x1b\x35 \x09"))
        self.tup.send(bytearray(" \x09 $ %.2f\r\n\r\n" % (total)))
        self.tup.send(bytearray(self.to_int(['1b', '69', '00', '00']))) # Cancel Character expansion
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '01']))) # center alignment pag 50
        # end Body
        # Footer
        dia = int(mktime(localtime()))
        self.tup.send(bytearray(self.to_int(['1b', '62', '06', '02', '02']))) # Barcode pag 61
        self.tup.send(bytearray(" %s\x1e\r\n" % (code))) # Barcode pag 61
        # end Footer
        self.tup.send(bytearray(self.to_int(['1b', '64', '02']))) # paper fed and full cut page 63
    
    
    def print_ticket_alumno(self, alumno, dni, facultad, categoria, code, 
                                        unidad, ticket, fecha, mensaje, saldo):
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
        self.tup.send(bytearray(u"Categoria: %s\r\n" % (categoria), 'cp850'))
        self.tup.send(bytearray("Saldo: $%d\r\n\r\n" % (saldo)))
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
            precio = -1
            precio_escrito = u"Null"
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
        self.tup.send(bytearray(self.to_int(['1b', '64', '03']))) # paper fed and full cut page 63

    def feed_and_full_cut(self):
        self.tup.send(bytearray(self.to_int(['1b', '64', '02']))) # paper fed and full cut page 63

    def print_ticket_carga(self, alumno, dni, facultad, categoria, code,
                                        unidad, log, mensaje, precio, saldo):
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
        self.tup.send(bytearray("Nro log: %s" % (log))) 
        self.tup.send(bytearray(" \x09 Terminal: %s\r\n" % (unidad), 'cp850'))
        self.tup.send(bytearray("---------------------------------------------\r\n\r\n"))
        # end Header
        # Body
        self.tup.send(bytearray("\x1b\x34Carga de Saldo\x1b\x35\r\n\r\n" ))
        self.tup.send(bytearray(self.to_int(['1b', '45']))) # Set emphasys
        self.tup.send(bytearray(u"Alumno: %s\r\n" %(alumno), 'cp850'))
        self.tup.send(bytearray(u"DNI: %s\r\n" %(dni), 'cp850'))
        self.tup.send(bytearray(u"Facultad: %s\r\n" % (facultad), 'cp850'))
        self.tup.send(bytearray(u"Categoria: %s\r\n\r\n" % (categoria), 'cp850'))
        self.tup.send(bytearray("Saldo: $%d\r\n\r\n" % (saldo)))
        self.tup.send(bytearray(self.to_int(['1b', '46']))) # Cancel emphasys
        self.tup.send(bytearray(self.to_int(['1b', '44', '10', '26', '00']))) # Set Horizontal tab pag 48
        self.tup.send(bytearray("Importe Cargado \x09"))
        self.tup.send(bytearray(" \x09 \x1b\x34$ %.2f\x1b\x35\r\n" % (precio)))
        self.tup.send(bytearray("---------------------------------------------\r\n\r\n"))
        # end Body
        # Footer
        self.tup.send(bytearray(self.to_int(['1b', '1d', '61', '01']))) # center alignment pag 50
        self.tup.send(bytearray(u"%s \r\n" % (mensaje), 'cp850'))
        self.tup.send(bytearray(self.to_int(['1b', '62', '06', '02', '02']))) # Barcode pag 61
        self.tup.send(bytearray(" %s\x1e\r\n" % (code))) # Barcode pag 61
        # end Footer
        self.tup.send(bytearray(self.to_int(['1b', '64', '02']))) # paper fed and full cut page 63
