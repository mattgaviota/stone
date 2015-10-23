#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
# las páginas se refieren al archivo comandos de impresora en la carpeta doc/

from tup500 import Tup500
from time import sleep, strftime, localtime


class Printer():
    '''Clase que maneja la impresora'''
    def __init__(self):
        self.tup = Tup500()
        self.tup.connect()
        self.style_codes = {
            'align-center': ['1b', '1d', '61', '01'],
            'align-left': ['1b', '1d', '61', '00'],
            'h-tab-22': ['1b', '44', '22', '00'],
            'h-tab-20': ['1b', '44', '20', '00'],
            'h-tab-8-16': ['1b', '44', '8', '16', '00'],
            'h-tab-10-26': ['1b', '44', '10', '26', '00'],
            'h-tab-12-26': ['1b', '44', '04', '12', '26', '00'],
            'h-tab-14-26': ['1b', '44', '04', '14', '26', '00'],
            'logo': ['1b', '1c', '70', '01', '00'],
            'set-em': ['1b', '45'],
            'unset-em': ['1b', '46'],
            'set-char-exp': ['1b', '69', '01', '01'],
            'unset-char-exp': ['1b', '69', '00', '00']
        }
        self.print_codes = {
            'h-line': "----------------------------------------------\r\n\r\n",
            'blank-line': "\r\n"
        }

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
        # error_mech = int(status[6:8], 16)
        # error_jam = int(status[8:10], 16)
        paper = int(status[10:12], 16)
        if not offline:
            if not paper:
                return 1  # online y con papel
            else:
                if paper == 4:
                    return 2  # online y con papel por acabarse
                else:
                    return 2  # online y sin papel
        else:
            return 3  # offline y error
            # TODO especificación de error

    def set_style(self, code):
        try:
            self.tup.send(bytearray(self.to_int(self.style_codes[code])))
        except KeyError:
            self.tup.send(bytearray(self.print_codes[code]))
        else:
            return None

    def print_header(
            self,
            id_ticket,
            unidad,
            mensaje,
            dia=strftime("%d/%m/%Y", localtime()),
            hora=strftime("%H:%M", localtime())
            ):
        self.set_style('align-center')
        self.set_style('logo')
        self.set_style('align-left')
        self.set_style('h-tab-22')
        self.tup.send(bytearray("Fecha %s" % (dia)))
        self.tup.send(bytearray(" \x09 Hora %s\r\n" % (hora)))
        self.set_style('h-tab-20')
        self.tup.send(bytearray("%s: %s" % (mensaje, id_ticket)))
        self.tup.send(bytearray(" \x09 Terminal: %d\r\n" % (unidad)))
        self.set_style('h-line')

    def print_footer(self, mensaje='', code=''):
        self.set_style('align-center')
        if mensaje:
            self.tup.send(bytearray(u"%s \r\n" % (mensaje), 'cp850'))
        self.print_barcode(code)

    def print_barcode(self, code):
        # Barcode pag 61
        self.tup.send(bytearray(self.to_int(['1b', '62', '06', '02', '02'])))
        self.tup.send(bytearray(" %s\x1e\r\n" % (code)))  # Barcode pag 61

    def feed_and_full_cut(self):
        # paper fed and full cut page 63
        self.tup.send(bytearray(self.to_int(['1b', '64', '02'])))

    def print_ticket_cierre(
            self,
            user,
            id_ticket,
            unidad,
            inicio,
            bills,
            total,
            code,
            dia
            ):
        # HEADER
        self.print_header(id_ticket, unidad, 'Nro Cierre', dia=dia)
        # BODY
        bill_2 = bills[2]
        bill_5 = bills[5]
        bill_10 = bills[10]
        bill_20 = bills[20]
        bill_50 = bills[50]
        bill_100 = bills[100]
        self.tup.send(
            bytearray(
                u"\x1b\x34Administrador:\x1b\x35 %s\r\n\r\n" % (user),
                'cp850'
            )
        )
        self.tup.send(
            bytearray(
                u"\x1b\x34Hora de inicio:\x1b\x35 %s\r\n\r\n" % (inicio),
                'cp850'
            )
        )
        self.set_style('h-tab-12-26')
        self.set_style('set-em')
        self.set_style('h-line')
        self.set_style('h-tab-12-26')
        self.tup.send(bytearray("\x1b\x2d\x01Billetes\x1b\x2d\x00\r\n\r\n"))
        self.tup.send(bytearray(" Valor \x09 Cantidad \x09 Total \r\n\r\n"))
        self.set_style('h-tab-14-26')
        self.tup.send(
            bytearray(
                " 2 pesos \x09 %d \x09 $ %.2f \r\n" % (bill_2, bill_2 * 2)
            )
        )
        self.tup.send(
            bytearray(
                " 5 pesos \x09 %d \x09 $ %.2f \r\n" % (bill_5, bill_5 * 5)
            )
        )
        self.tup.send(
            bytearray(
                " 10 pesos  \x09 %d \x09 $ %.2f \r\n" % (bill_10, bill_10 * 10)
            )
        )
        self.tup.send(
            bytearray(
                " 20 pesos  \x09 %d \x09 $ %.2f \r\n" % (bill_20, bill_20 * 20)
            )
        )
        self.tup.send(
            bytearray(
                " 50 pesos  \x09 %d \x09 $ %.2f \r\n" % (bill_50, bill_50 * 50)
            )
        )
        self.tup.send(
            bytearray(
                " 100 pesos  \x09 %d \x09 $ %.2f \r\n\r\n" % (
                    bill_100,
                    bill_100 * 100
                )
            )
        )
        self.set_style('h-line')
        self.set_style('unset-em')
        self.set_style('h-tab-8-16')
        self.set_style('set-char-exp')
        self.tup.send(bytearray("\x1b\x34Total\x1b\x35 \x09"))
        self.tup.send(bytearray(" \x09 $ %.2f\r\n\r\n" % (total)))
        self.set_style('unset-char-exp')
        self.set_style('align-center')
        # END BODY
        # FOOTER
        self.print_footer(code=code)
        # CUT
        self.feed_and_full_cut()

    def print_ticket_alumno(
            self,
            alumno,
            dni,
            facultad,
            categoria,
            code,
            unidad,
            ticket,
            fecha,
            mensaje,
            saldo
            ):
        # HEADER
        self.print_header(ticket, unidad, 'Nro ticket')
        # BODY
        self.tup.send(
            bytearray(
                "\x1b\x34Fecha de Servicio: %s\x1b\x35\r\n\r\n" % (fecha)
            )
        )
        self.set_style('set-em')
        self.tup.send(bytearray(u"Alumno: %s\r\n" % (alumno), 'cp850'))
        self.tup.send(bytearray(u"DNI: %s\r\n" % (dni), 'cp850'))
        self.tup.send(bytearray(u"Facultad: %s\r\n" % (facultad), 'cp850'))
        self.tup.send(bytearray(u"Categoria: %s\r\n" % (categoria), 'cp850'))
        self.tup.send(bytearray("Saldo: $%d\r\n\r\n" % (saldo)))
        self.set_style('unset-em')
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
        # Set Horizontal tab pag 48
        self.tup.send(bytearray(self.to_int(['1b', '44', '10', '26', '00'])))
        self.tup.send(bytearray("Importe \x09"))
        self.tup.send(bytearray(" \x09 \x1b\x34$ %.2f\x1b\x35\r\n" % (precio)))
        self.tup.send(
            bytearray(u"Total pesos %s\r\n" % (precio_escrito), 'cp850')
        )
        self.set_style('h-line')
        # END BODY
        # FOOTER
        self.print_footer(mensaje, code)
        # CUT
        self.feed_and_full_cut()

    def print_ticket_carga(
            self,
            alumno,
            dni,
            facultad,
            categoria,
            code,
            unidad,
            log,
            mensaje,
            precio,
            saldo
            ):
        # HEADER
        self.print_header(log, unidad, 'Nro log')
        # BODY
        self.tup.send(bytearray("\x1b\x34Carga de Saldo\x1b\x35\r\n\r\n"))
        self.set_style('set-em')
        self.tup.send(bytearray(u"Alumno: %s\r\n" % (alumno), 'cp850'))
        self.tup.send(bytearray(u"DNI: %s\r\n" % (dni), 'cp850'))
        self.tup.send(bytearray(u"Facultad: %s\r\n" % (facultad), 'cp850'))
        self.tup.send(
            bytearray(u"Categoria: %s\r\n\r\n" % (categoria), 'cp850')
        )
        self.tup.send(bytearray("Saldo: $%d\r\n\r\n" % (saldo)))
        self.set_style('unset-em')
        self.set_style('h-tab-10-26')
        self.tup.send(bytearray("Importe Cargado \x09"))
        self.tup.send(bytearray(" \x09 \x1b\x34$ %.2f\x1b\x35\r\n" % (precio)))
        self.set_style('h-line')
        # END BODY
        # FOOTER
        self.print_footer(mensaje, code)
        # CUT
        self.feed_and_full_cut()

    def print_ticket_grupal(
            self,
            usuario,
            dni,
            id_ticket,
            unidad,
            fecha,
            cantidad,
            code,
            importe,
            delegacion,
            recibo,
            mensaje
            ):
        self.print_header(id_ticket, unidad, 'Nro Ticket')
        # BODY
        self.tup.send(
            bytearray(
                "\x1b\x34Fecha de Servicio: %s\x1b\x35\r\n\r\n" % (fecha)
            )
        )
        self.tup.send(
            bytearray("\x1b\x34Delegacion: %s\x1b\x35\r\n\r\n" % (delegacion))
        )
        self.set_style('set-em')
        self.tup.send(bytearray(u"Usuario: %s\r\n" % (usuario), 'cp850'))
        self.tup.send(bytearray(u"DNI: %s\r\n" % (dni), 'cp850'))
        self.set_style('unset-em')
        self.set_style('h-tab-10-26')
        self.set_style('blank-line')
        self.tup.send(
            bytearray("\x1b\x34Nro de Recibo: %s\x1b\x35\r\n\r\n" % (recibo))
        )
        self.set_style('blank-line')
        self.set_style('blank-line')
        self.set_style('blank-line')
        self.tup.send(bytearray("Importe \x09"))
        self.tup.send(
            bytearray(" \x09 \x1b\x34$ %.2f\x1b\x35\r\n\r\n" % (importe))
        )
        self.tup.send(bytearray("Cantidad \x09"))
        self.tup.send(
            bytearray(" \x09 \x1b\x34 %d\x1b\x35\r\n\r\n" % (cantidad))
        )
        self.set_style('blank-line')
        self.tup.send(bytearray("Total \x09"))
        self.tup.send(bytearray(
            " \x09 \x1b\x34$ %.2f\x1b\x35\r\n" % (importe * cantidad)))
        self.set_style('h-line')
        # END BODY
        # FOOTER
        self.print_footer(mensaje, code)
        # CUT
        self.feed_and_full_cut()
