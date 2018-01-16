#!/usr/bin/env python3

import argparse
import serial.tools.list_ports
import signal
import sys


def print_serial_connections():
    slist = serial.tools.list_ports.comports()
    for sc in slist:
        print(str(sc.device))

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

    args = parser.parse_args()

    if args.list_serial:
        print_serial_connections()
        sys.exit(0)
