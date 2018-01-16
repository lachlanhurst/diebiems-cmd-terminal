#
# Module includes code to call serial functions of the DieBieMS
#

import pyvesc
import serial
import time

from dbmscommand.commands import GetTerminalPrint, SetTerminalCmd
from dbmscommand.util import read_all

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
