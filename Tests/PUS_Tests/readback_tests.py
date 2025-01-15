"""Test used to set a scientific parameters in the datahub, and reading back the values to confirm correct functionality.
    The test uses SET messages defined in PUS_8_test with predefined values. After the SET messages are sent the GET messages are sent
    which request the DataHub the previously set parameter.
"""
import PUS_8_test
import serial
import codecs
from cobs import cobs
import signal
import sys
import struct
import time
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


def var_name(variable):
    return [name for name, value in locals().items() if value is variable][0]

try:
    for i, msg in enumerate(PUS_8_test.PUS_8_TC_SETs):
        spp_message = msg
        msg_len = len(spp_message)
        ser.write(spp_message)
        print("Sent ", var_name(msg))
        print(f"SENT: ", cobs.decode(spp_message[:-1]).hex())

 #       time.sleep(1)
        msg = PUS_8_test.PUS_8_TC_GETs[i]
        spp_message = msg
        msg_len = len(spp_message)
        ser.write(spp_message)
        print("Sent", var_name(msg))
        print(f"SENT: ", cobs.decode(spp_message[:-1]).hex())

        output = ser.read(256)
        print("RECEIVED: ", output.hex())
        output_dec = cobs.decode(output[:-1])
        print("AFTER COBS DECODE: ", output_dec.hex())
        spp_header = SPP_decode(output_dec)
        print(output_dec[6:-2].hex())
        print("")
except:
    pass
else:
    pass
