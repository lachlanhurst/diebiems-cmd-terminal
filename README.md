# DieBieMS command terminal
The DieBieMS is an open source/open hardware Battery Management System (BMS) originally developed for electric skateboards. A BMS helps ensure multi-cell battery packs are charged correctly; extending the life of a battery pack, and improving safety. The DieBieMS can be configured to support a range of battery pack configurations and cell chemistries. For more details see the [DieBieMS repositories](https://github.com/DieBieEngineering/DieBieMS/).

*The command line tool in this repository supports sending terminal commands to the DieBieMS via a USB based serial interface.*

The DieBieMS implements a subset of the serial interface used by the [VESC](https://github.com/vedderb/bldc) speed controller, allowing a number of existing applications and libraries a simple means of communication. This tool makes use of the [PyVESC library](https://github.com/LiamBindle/PyVESC) for communication with the DieBieMS.

## Setup

### Dependencies
The following process assumes the following dependencies have been installed.
- [Python 3.4+](https://www.python.org/)
- [virtualenv](https://virtualenv.pypa.io)

Note: virtualenv is a nice to have, not really a dependency but the following install process makes use of this tool...

### Install

Clone the project

    git clone https://github.com/lachlanhurst/diebiems-cmd-terminal.git
    cd diebiems-cmd-terminal

Create a fresh python virtual environment making sure python 3 is used.

    virtualenv -p python3 venv

Activate the virtual environment (to deactivate later type `deactivate` at the cmd prompt). Note: this process differs for Linux/MacOS and Windows.

Windows:

    venv/bin/activate

Linux / MacOS:

    source venv/bin/activate

Install dependencies as listed in `requirements.txt` needed for this app to run. As we've activated the virtualenv these will be installed into the venv folder (and not into your system python).

    pip install -r requirements.txt

That's it!

## Usage
