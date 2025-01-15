"""Test used to verify the functionality of toggling On/Off the periodic generation of specific housekeeping reports."""
import PUS_3_test
import serial
from cobs import cobs
import signal
import sys
from SPP_PUS_test import *

print("PUS 3 HK_toggle_periodic")

ser = serial.Serial('COM3', 115200, timeout=1)

def signal_handler(sig, frame):
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    msg_full = PUS_3_test.HK_DIS_PERIODIC_FPGA_COBS
    print("SENT: ", cobs.decode(msg_full[:-1]).hex())
    ser.write(msg_full)
except:
    pass
else:
    pass