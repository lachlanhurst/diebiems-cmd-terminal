#
# PyVESC messages specific to the DieBieMS
#

from pyvesc.messages.base import VESCMessage

# send a terminal command to the BMS
class SetTerminalCmd(metaclass=VESCMessage):
    id = 20

    fields = [
            ('command', 's')
    ]

# response to sent terminal command
class GetTerminalPrint(metaclass=VESCMessage):
    id = 21

    fields = [
            ('message', 's')
    ]
