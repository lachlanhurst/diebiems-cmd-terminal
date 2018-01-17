#!/usr/bin/env python3

import argparse
import datetime
import serial.tools.list_ports
import signal
import sys
import time

from dbmscommand.interface import run_command, get_cells, get_status

def print_serial_connections():
    slist = serial.tools.list_ports.comports()
    for sc in slist:
        print(str(sc.device))

def print_command_output(serialport, command):
    #print(command)
    cmdout = run_command(serialport, command)
    print(cmdout)


def __record_filename(time, recordtype):
    return time.strftime("%Y-%m-%d-%H-%M-%S") + "_" + recordtype + ".csv"


def run_record(serialport, timestep):
    starttime = datetime.datetime.now()
    statusfilename = __record_filename(starttime, "status")
    cellsfilename = __record_filename(starttime, "cells")
    print("--- entering record mode ---")
    print("status will be written to " + statusfilename)
    print("cells will be written to " + cellsfilename)
    print()
    print("Press crtl-c to exit record mode at any time")
    print()

    fl = True
    while True:
        currenttime = datetime.datetime.now()
        totalseconds = (currenttime - starttime).total_seconds()
        timetuple = ('Time (sec)', "{:.1f}".format(totalseconds))

        status = get_status(serialport)
        status.insert(0, timetuple)
        cells = get_cells(serialport)
        cells.insert(0, timetuple)

        # both the status and cells file get opened and closed after each
        # poll, this way we don't care when a user exits.
        with open(statusfilename, "a") as statusfile:
            if fl:
                headerbits = [statusitem[0] for statusitem in status]
                header = ', '.join(headerbits)
                statusfile.write(header + '\n')
            valuebits = [statusitem[1] for statusitem in status]
            value = ', '.join(valuebits)
            statusfile.write(value + '\n')

        with open(cellsfilename, "a") as cellsfile:
            if fl:
                headerbits = [cellitem[0] for cellitem in cells]
                header = ', '.join(headerbits)
                cellsfile.write(header + '\n')
            valuebits = [cellitem[1] for cellitem in cells]
            value = ', '.join(valuebits)
            cellsfile.write(value + '\n')

        print('updated at time = ' + timetuple[1])
        fl = False
        time.sleep(timestep)


class HelpOnErrorArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

if __name__ == '__main__':

    # Make sure we can exit cleanly
    def handle_sigint(signal, frame):
        print("Exiting")
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
    parser.add_argument(
        "-r", "--record", action='store_true',
        help="Run in record mode. Periodically poll the BMS, " +
            "saving responses to CSV file.",
        required=False)
    parser.add_argument(
        "-rf", "--record-timestep", type=float, default=30,
        help="Time (seconds) between polling the BMS in record mode.",
        required=False)

    args = parser.parse_args()

    if args.list_serial:
        print_serial_connections()
        sys.exit(0)

    if args.serial_port is None:
        print("no serial port specified")
        sys.exit(1)

    if args.command is not None:
        print_command_output(args.serial_port, args.command)
        sys.exit(0)

    if args.record:
        run_record(args.serial_port, args.record_timestep)
        sys.exit(0)
