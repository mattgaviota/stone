# -*- coding: utf-8 -*-
# Autor: Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html
#
# states
NOT_SENT = 0
SENDING = 1
SENT = 2

# Command codes
SYNC = 'FC'
LNG_5 = '05'
LNG_6 = '06'
LNG_7 = '07'
# Operation command
RESET = '40'
STACK_1 = '41'
STACK_2 = '42'
RETURN = '43'
HOLD = '44'
WAIT = '45'
# ACK
ACK = '50'
# Setting Command
ENABLE = 'C0'
SECURITY = 'C1'
COMMUNICATION = 'C2'
INHIBIT = 'C3'
DIRECTION = 'C4'
OPTIONAL = 'C5'
# Setting status request
REQ_STATUS = '11'
REQ_ENABLE = '80'
REQ_SECURITY = '81'
REQ_COMMUNICATION = '82'
REQ_INHIBIT = '83'
REQ_DIRECTION = '84'
REQ_OPTIONAL = '85'
REQ_VERSION = '88'
REQ_BOOT = '89'
REQ_CURRENCY = '8A'

# denominations to accept
BVU_ACCEPT_1 = 0x01
BVU_ACCEPT_5 = 0x04
BVU_ACCEPT_10 = 0x08
BVU_ACCEPT_20 = 0x10
BVU_ACCEPT_50 = 0x20
BVU_ACCEPT_100 = 0x40

# denominations accepted
BILL_VALUE = {
    '62': 2,
    '63': 5,
    '64': 10,
    '65': 20,
    '66': 50,
    '67': 100
    }

# generic denomination codes
BVU_ESCROW_61 = 0x61
BVU_ESCROW_62 = 0x62
BVU_ESCROW_63 = 0x63
BVU_ESCROW_64 = 0x64
BVU_ESCROW_65 = 0x65
BVU_ESCROW_66 = 0x66
BVU_ESCROW_67 = 0x67
BVU_ESCROW_68 = 0x68
BVU_ESCROW_69 = 0x69
BVU_ESCROW_6A = 0x6A
BVU_ESCROW_6B = 0x6B
BVU_ESCROW_6C = 0x6C
BVU_ESCROW_6D = 0x6D
BVU_ESCROW_6E = 0x6E
BVU_ESCROW_6F = 0x6F

# accepted directions
BVU_DIRECTION_A = '01'
BVU_DIRECTION_B = '02'
BVU_DIRECTION_C = '03'
BVU_DIRECTION_D = '04'

#  failure codes ID003
FAILURE_DATA = {
    'a2': 'Stack motor failure',
    'a5': 'Transport(feed) motor speed failure',
    'a6': 'Transport(feed) motor failure',
    'a8': 'Selenoid failure',
    'a9': 'PB unit failure',
    'ab': 'Cash box not ready',
    'af': 'Validator head remove',
    'b0': 'BOOT ROM failure',
    'b1': 'External ROM failure',
    'b2': 'RAM failure',
    'b3': 'External ROM writing failure'
    }

# failure codes ICB
BVU_FAILURE_ICB_02 = 0x02
BVU_FAILURE_ICB_03 = 0x03
BVU_FAILURE_ICB_04 = 0x04
BVU_FAILURE_ICB_07 = 0x07
BVU_FAILURE_ICB_08 = 0x08
BVU_FAILURE_ICB_09 = 0x09

# Status Results
STATUS_RESULT = {
    '11': 'IDLING',
    '12': 'ACCEPTING',
    '13': 'ESCROW',
    '14': 'STACKING',
    '15': 'VEND_VALID',
    '16': 'STACKED',
    '17': 'REJECTING',
    '18': 'RETURNING',
    '19': 'HOLDING',
    '1a': 'DISABLED',
    '1b': 'INITIALIZING',
    '40': 'POWER UP',
    '41': 'POWER UP BILL IN ACCEPTOR',
    '42': 'POWER UP BILL IN STACKER',
    '43': 'STACKER FULL',
    '44': 'STACKER OPEN',
    '45': 'JAM IN ACCEPTOR',
    '46': 'JAM IN STACKER',
    '47': 'PAUSE',
    '48': 'CHEATED',
    '49': 'FAILURE',
    '4a': 'COMMUNICATION ERROR',
    '50': 'ACK'
    }

# REJECTING DATA

REJECT_DATA = {
    '71': 'Insertion error',
    '72': 'Mug error',
    '73': 'Return action due to residual bills',
    '74': 'Calibration / magnification error',
    '75': 'Conveying error',
    '76': 'Discrimination error for bill denomination',
    '77': 'Photo pattern error',
    '78': 'Photo level error',
    '79': 'Return by INHIBIT: error of insertion direction',
    '7a': 'None',
    '7b': 'Operation error',
    '7c': 'Return action due to residual bills',
    '7d': 'Lenght error',
    '7e': 'Photo pattern error',
    '7f': 'True bill feature error'
    }
# COMMUNICATION ERRORS
DCB_ERROR = 0x01
PORT_ALREADY_OPENED = 0x02
PORT_SETTINGS_FAILED = 0x03
INVALID_PORT = 0x04
ERROR_CE_BREAK = 0x05
ERROR_CE_FRAME = 0x06
ERROR_CE_IOE = 0x07
ERROR_CE_MODE = 0x08
ERROR_CE_OVERRUN = 0x09
ERROR_CE_RXOVER = 0x0A
ERROR_CE_RXPARITY = 0x0B
ERROR_CE_TXFULL = 0x0C
RXTIME_OUT = 0x0D
CRC_ERROR = 0x0E
