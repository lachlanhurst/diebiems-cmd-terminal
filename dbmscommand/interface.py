#
# Module includes code to call serial functions of the DieBieMS
#

import pyvesc
import re
import serial
import time

from dbmscommand.commands import GetTerminalPrint, SetTerminalCmd
from dbmscommand.util import read_all

# fields with names in this list will not have their values stripped of
# non-numeric characters
known_nonnumeric_fields = [
    "Operational state",
    "Discharge enabled",
    "Charge enabled"
]


# Parses the DieBieMS text response format into a list of tuples.
# Each tuple contains value label and value as strings
def _parse_cellslikeresponse(responsestring):
    lines = responsestring.splitlines()

    nondecimal = re.compile(r'[^\d.]+')

    cellsdata = []

    for line in lines:
        if line.startswith('---') and line.endswith('---'):
            # then it's the header or footer
            continue

        labelandvalue = line.split(':')
        label = labelandvalue[0].strip()
        value = labelandvalue[1].strip()
        if label not in known_nonnumeric_fields:
            value = nondecimal.sub('', value) # remove the V char

        cellsdata.append((label, value))

    return cellsdata


def get_cells(serialport):
    response = run_command(serialport, "cells")
    return _parse_cellslikeresponse(response)


def get_status(serialport):
    response = run_command(serialport, "status")
    return _parse_cellslikeresponse(response)


def run_command(serialport, command):

    with serial.Serial(serialport, baudrate=115200, timeout=0.2) as ser:

        # Encode the command as per vesc spec and write to serial port
        ser.write(pyvesc.encode(SetTerminalCmd(command)))

        # read all bytes available from serial port
        bytedata = read_all(ser)

        # VESC data comes in frames, we need to decode each frame and append
        # together.
        fullresponse = ''
        consumed = 0
        fl = True
        while consumed < len(bytedata):
            (response, consumed) = pyvesc.decode(bytedata)

            # strip the bytes already decoded from the serial data
            bytedata = bytedata[consumed:]
            if fl:
                fl = False
                fullresponse = response.message
            else:
                fullresponse = fullresponse + '\n' + response.message

        return fullresponse
