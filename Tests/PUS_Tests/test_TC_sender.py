"""Used to test that the uC is generating correct message to the FPGA when setting parameters through PUS 8 service."""
import PUS_8_test
import serial
import codecs
from cobs import cobs
import signal
import sys
import struct
from SPP_PUS_test import *

ser = serial.Serial('COM3', 115200, timeout=1)

def signal_handler(sig, frame):
    ser.close()
    sys.exit(0)

def pad_msg(msg, pad_to):
    msg_len = len(msg)
    diff = pad_to - msg_len
    for i in range(0, diff):
        msg += b'\x00'
    return msg


signal.signal(signal.SIGINT, signal_handler)



try:
    for i, msg in enumerate(PUS_8_test.PUS_8_TCs):
        spp_message = msg
        msg_len = len(spp_message)
        ser.write(spp_message)
        print(f"Sent Message ({msg_len})")

        output = ser.read(256)
        correct = PUS_8_test.response[i] == output
        print("Correct RESP: ", correct)
        print("EXPECTED: ", PUS_8_test.response[i].hex())
        print("RECEIVED: ", output.hex())
except:
    pass
else:
    pass



