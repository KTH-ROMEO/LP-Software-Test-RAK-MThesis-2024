'''
This script generates 256 sweep table set commands directed to either the FRAM or FPGA (FRAM_target or FPGA_target).
The table is select with table_id. For the FRAM this goes from 0 - 7, for the FPGA this is 0 - 1.
The actual values are just shifted and offset loop iterators just to have different values in each step.

All of the SET commands ar sent, afterwards all of the GET (readback) commands are sent and the response is
collected after each GET command. After collecting all of the responses they are check for correct data.
The python serial libary is kind of wierd and some times the timing can lead to infinite wait times.

For a test that will not freeze the time.sleep in both the SET and GET message loops can be made longer, 
but this will considerably increase the testing time. The current values were found empirically and work
99% of the time.
'''
import PUS_8_test
import serial
import codecs
from cobs import cobs
import signal
import sys
import struct
import time
#from SPP_PUS_test import *

ser = serial.Serial('COM3', 115200, timeout=1)
def signal_handler(sig, frame):
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

steps_levels : list[tuple[int, int]] = []

table_id = 0x07
set_msgs : list[bytes] = []

get_msgs : list[bytes] = []

resp_data: list[bytes] = []

FPGA_target = 0x00
FRAM_target = 0x01

nof_steps = 256

for i in range(nof_steps):
    set_value: int = (i << 6) + 7
    
    set_value_0 : int = set_value & 0xFF
    set_value_1 : int = (set_value >> 8) & 0xFF

    set_step_id: int = i
    get_step_id : int = set_step_id
    steps_levels.append((set_step_id, set_value))

    set_table_id : int = table_id
    get_table_id : int = set_table_id

    SET_VL_SWM_FRAM : list[int] = [0xAB, 0x04, 0x01, set_table_id,  0x02, set_step_id , 0x03, set_value_0 , set_value_1, 0x08, FRAM_target]
    GET_VL_SWM_FRAM : list[int] = [0xA1, 0x03, 0x01, get_table_id,  0x02, get_step_id,                                   0x08, FRAM_target]
    #print(SET_VL_SWM_FRAM.hex())
    #print('[{}]'.format(', '.join(hex(x) for x in SET_VL_SWM_FRAM)))
    set_pus81msg : bytes = PUS_8_test.get_PUS_8_TC(bytearray(SET_VL_SWM_FRAM))
    get_pus81msg : bytes = PUS_8_test.get_PUS_8_TC(bytearray(GET_VL_SWM_FRAM))

    set_msgs.append(set_pus81msg)
    get_msgs.append(get_pus81msg)


#print(set_msgs)
#print(get_msgs)
#print(steps_levels)

error_cnt = 0

ser.reset_output_buffer()
ser.reset_input_buffer()
only_get = False
only_send = False

try:
    if not only_get:
        print("Sending SET messages...")
        for i, msg in enumerate(set_msgs):
            ser.reset_output_buffer()
            spp_message = msg
            msg_len = len(spp_message)
            time.sleep(0.05)
            ser.write(spp_message)
            print(f"SENT: ", cobs.decode(spp_message[:-1]).hex())

 #       time.sleep(1)
    if not only_send:
        print("Sending GET messages and reading responses...")
        for i, msg in enumerate(get_msgs):
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            spp_message = msg
            msg_len = len(spp_message)
            ser.write(spp_message)

            time.sleep(0.1)
            output = ser.read(ser.in_waiting)

            output_dec = cobs.decode(output[:-1])
            resp_data.append(output_dec[6:-2])
            print(f"Response to GET: {output_dec.hex()}")


        for i, resp_msg in enumerate(resp_data):
            if len(resp_msg) == 0:
                continue
            step_level = steps_levels[i]

            recv_msg_id = resp_msg[0]
            if recv_msg_id != 0xA1:
                print(f"ERROR: GET msg id does not match response msg id! {recv_msg_id}")
                error_cnt += 1

            recv_table_id = resp_msg[1]
            if recv_table_id != table_id:
                print(f"ERROR: GET table id does not match response table id! {recv_table_id} {table_id}")
                error_cnt += 1

            recv_step_id = resp_msg[2]
            if recv_step_id != step_level[0]:
                print(f"ERROR: GET step id does not match response step id! {recv_step_id} {step_level[0]}")
                error_cnt += 1

            recv_voltage_int : int = (resp_msg[4] << 8) | resp_msg[3]
            if recv_voltage_int != step_level[1]:
                print(f"ERROR: SET Voltage does not match response voltage ! {recv_voltage_int} {step_level[1]}")
                error_cnt += 1

            print(f"RECV ({recv_step_id}, {recv_voltage_int}) == SET {step_level}")

        print(f"Errors: {error_cnt}")

except:
    pass
else:
    pass