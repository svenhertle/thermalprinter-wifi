#!/usr/bin/env python

import argparse
import math
import sys

from datetime import datetime
from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError


def center(text, width=32):
    if len(text) < width:
        padding = math.floor((width - len(text)) / 2)
        return " " * padding + text


# argparse
parser = argparse.ArgumentParser()
parser.add_argument("ssid")
parser.add_argument("psk")
args = parser.parse_args()

# init printer
try:
    p = Usb(0x0416, 0x5011, 0)
    p.profile = "TM-T88III"
except USBNotFoundError:
    print("USB printer not found")
    sys.exit(1)

while True:
    p.text("\n")

    p.text(center(args.ssid) + "\n")
    p.qr("WIFI:S:{};T:WPA;P:{};;".format(args.ssid, args.psk), size=12)
    p.text(center(args.psk) + "\n")

    p.cut()

    print("Continue?")
    try:
        input()
    except KeyboardInterrupt:
        print("Bye")
        sys.exit(0)
