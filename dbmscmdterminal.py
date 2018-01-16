#!/usr/bin/env python3

import argparse
import serial.tools.list_ports
import signal
import sys

from dbmscommand.interface import run_command

def print_serial_connections():
    slist = serial.tools.list_ports.comports()
    for sc in slist:
        print(str(sc.device))

def print_command_output(serialport, command):
    #print(command)
    cmdout = run_command(serialport, command)
    print(cmdout)

class HelpOnErrorArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

if __name__ == '__main__':

    # Make sure we can exit cleanly
    def handle_sigint(signal, frame):
        print("Received interrupt")
        sys.exit(0)
    signal.signal(signal.SIGINT, handle_sigint)

    # setup the command line parser
    parser = HelpOnErrorArgumentParser(
        description='Command line terminal tool for the DieBieMS',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-l", "--list-serial", action='store_true', help="List available serial connections",
        required=False)
    parser.add_argument(
        "-sp", "--serial-port", default=None, help="Serial port the BMS is connected to",
        required=False)
    parser.add_argument(
        "-c", "--command", default=None, help="Terminal command to run",
        required=False)

    args = parser.parse_args()

    if args.list_serial:
        print_serial_connections()
        sys.exit(0)

    if args.serial_port is None:
        print("no serial port specified")
        sys.exit(1)

    if args.command is None:
        print("no command specified")
        sys.exit(1)



    print_command_output(args.serial_port, args.command)
