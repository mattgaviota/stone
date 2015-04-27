#-*- coding: utf-8 -*-
#
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
from constant import *
from crckermit import CRC16Kermit

class Message():

    def __init__(self, sync=SYNC, lng=LNG_5, command=REQ_STATUS):
        self.message = bytearray(self.to_int([sync, lng, command, '0x27', '0x56']))
        self.sync = sync
        self.lng = lng
        self.command = command
        self.data1 = ''
        self.data2 = ''
        self.crcl = '0x27'
        self.crch  = '0x56'
        self.kermit = CRC16Kermit()

    def calculate_crc(self, band, lng, cmd, data1, data2):
        if band:
            crcl, crch = self.kermit.get_crc(self.sync + lng + cmd)
        else:
            if data2:
                crcl, crch = self.kermit.get_crc(self.sync + lng + cmd + data1 + data2)
            else:
                crcl, crch = self.kermit.get_crc(self.sync + lng + cmd + data1)
        self.crcl = crcl
        self.crch = crch

    def to_int(self, lststr, base=16):
        lst = []
        for item in lststr:
            lst.append(int(item, base))
        return lst

    def update_message(self, lng=LNG_5, cmd=REQ_STATUS, data1='', data2=''):
        if data1:
            self.calculate_crc(0, lng, cmd, data1, data2)
            if data2:
                self.message = bytearray(self.to_int([self.sync, lng, cmd, data1, data2, self.crcl, self.crch]))
            else:
                self.message = bytearray(self.to_int([self.sync, lng, cmd, data1, self.crcl, self.crch]))
        else:
            self.calculate_crc(1, lng, cmd, data1, data2)
            self.message = bytearray(self.to_int([self.sync, lng, cmd, self.crcl, self.crch]))

    def get_message(self):
        return self.message

    def set_message(self, command=REQ_STATUS):
        self.update_message(cmd=command)
