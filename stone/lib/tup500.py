#-*- coding: utf-8 -*-

from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE


class Tup500():

    def __init__(self, port='/dev/ttyS0'):
        self.ser = Serial()
        self.ser.port = port
        self.ser.baudrate = 38400
        self.ser.bytesize = EIGHTBITS
        self.ser.parity = PARITY_NONE
        self.ser.stopbits = STOPBITS_ONE
        self.ser.dsrdtr = True

    def connect(self):
        try:
            self.ser.open()
        except Exception, e:
            print "error open serial port: " + str(e)

    def is_connected(self):
        return self.ser.isOpen()

    def disconnect(self):
        if self.is_connected():
            self.ser.close()

    def in_waiting(self):
        return self.ser.inWaiting()

    def flush_io(self):
        self.ser.flushInput()
        self.ser.flushOutput();

    def send(self, bytelist):
         self.ser.write(bytelist)

    def recipe(self, byte_amount=1):
        out = ''
        while self.in_waiting() > 0:
            out += self.ser.read(byte_amount)
        if out:
            return out.encode('hex')
        else:
            return 'Null'
