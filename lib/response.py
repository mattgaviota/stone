# -*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
from constant import *


class Response():

    def __init__(self):
        return None

    def get_escrow(self, answer):
        data = answer[6:-4]
        escrow = BILL_VALUE[data]
        return escrow

    def show_response(self, answer, opt):
        if opt in (RESET, STACK_1, STACK_2, HOLD, WAIT, RETURN):
            resp = answer[4:6]
            if resp == '50':
                respuesta = 'Valid ACK'
            else:
                respuesta = 'Invalid command'
            mensaje = 'Answer: '
        elif opt == REQ_STATUS:
            mensaje = 'Status: '
            resp = answer[4:6]
            if resp in ('13', '17', '49'):
                respuesta = self.resolve_data(resp, answer[6:-4])
            else:
                respuesta = STATUS_RESULT[resp]
        else:
            resp = answer[4:6]
            if resp == '4b':
                respuesta = 'Invalid command'
            elif resp == '4a':
                respuesta = 'Communication error'
            else:
                respuesta = self.resolve_data(resp, answer[6:-4])
            mensaje = ''

        print mensaje + respuesta

    def resolve_data(self, resp, data):
        if resp == '13':
            return '%s: %d pesos' % (STATUS_RESULT[resp], BILL_VALUE[data])
        elif resp == '83':
            return 'Inhibit: %s' % (bool(int(data, 16)),)
        elif resp == '17':
            return '%s: %s' % (STATUS_RESULT[resp], REJECT_DATA[data])
        elif resp == '49':
            return '%s: %s' % (STATUS_RESULT[resp], FAILURE_DATA[data])
        elif resp == '88':
            return self.resolve_version(data)
        elif resp == '89':
            return 'BOOT Version: ' + data.decode('hex')
        elif resp == '8a':
            return self.resolve_currency(data)
        else:
            return 'Echo back: ' + data

    def resolve_version(self, data):
        data_ascii = data.decode('hex')
        mc = data_ascii[0]
        cc = data_ascii[2:5]
        mn = data_ascii[6:9]
        st = data_ascii[10:12]
        it = data_ascii[13:21]
        sv = data_ascii[21:28]
        date = data_ascii[29:36]
        respuesta = """
            Version
            =======

            Machine code:     %s
            Country code:     %s
            Model number:     %s
            Stacker type:     %s
            Interface type:   %s
            Software version: %s
            Date:             %s
        """ % (mc, cc, mn, st, it, sv, date)
        return respuesta

    def resolve_currency(self, data):
        bill_2 = data[8:10]
        currency_2 = data[10:16]
        bill_5 = data[16:18]
        currency_5 = data[18:24]
        bill_10 = data[24:26]
        currency_10 = data[26:32]
        bill_20 = data[32:34]
        currency_20 = data[34:40]
        bill_50 = data[40:42]
        currency_50 = data[42:48]
        bill_100 = data[48:50]
        currency_100 = data[50:56]
        respuesta = """
            Currency
            ========

            Escrow    Country code    Denomination
            ------    ------------    ------------
              %s           %s              %s
              %s           %s              %s
              %s           %s              %s
              %s           %s              %s
              %s           %s              %s
              %s           %s              %s
        """ % (bill_2, currency_2[:2], int(currency_2[2:4], 16),
               bill_5, currency_5[:2], int(currency_5[2:4], 16),
               bill_10, currency_10[:2], int(currency_10[2:4], 16),
               bill_20, currency_20[:2], int(currency_20[2:4], 16),
               bill_50, currency_50[:2], int(currency_50[2:4], 16),
               bill_100, currency_100[:2], int(currency_100[2:4], 16)
               )
        return respuesta
