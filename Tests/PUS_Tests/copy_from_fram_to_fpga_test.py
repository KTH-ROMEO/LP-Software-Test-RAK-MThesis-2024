'''
This script sets a full sweep table to FRAM, then sends a copy command to copy the table from FRAM to the FPGA, then sends GET requests
to get data from the FPGA to check if the copy has worked successfully.
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

ser = serial.Serial('COM3', 115200)
def signal_handler(sig, frame):
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

steps_levels : list[tuple[int, int]] = []

table_id = 0x01
set_msgs : list[bytes] = []

get_msgs : list[bytes] = []

resp_data: list[bytes] = []

FPGA_target = 0x00
FRAM_target = 0x01

COPY_TABLE_FRAM_TO_FPGA                       = [0xE0, 0x02, 0x01,  0x01,  0x09, 0x01]
copy_pus81msg = PUS_8_test.get_PUS_8_TC(bytearray(COPY_TABLE_FRAM_TO_FPGA))

for i in range(256):
    set_value: int = (i << 3) + 16
    
    set_value_0 : int = set_value & 0xFF
    set_value_1 : int = (set_value >> 8) & 0xFF

    set_step_id: int = i
    get_step_id : int = set_step_id
    steps_levels.append((set_step_id, set_value))

    set_table_id : int = table_id
    get_table_id : int = set_table_id

    SET_VL_SWM_FRAM : list[int] = [0xAB, 0x04, 0x01, set_table_id,  0x02, set_step_id , 0x03, set_value_0 , set_value_1, 0x08, FRAM_target]
    GET_VL_SWM_FRAM : list[int] = [0xA1, 0x03, 0x01, get_table_id,  0x02, get_step_id,                                   0x08, FPGA_target]
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

try:
    if not only_get:
        print("Sending SET messages to FRAM...")
        for i, msg in enumerate(set_msgs):
            ser.reset_output_buffer()
            spp_message = msg
            msg_len = len(spp_message)
            time.sleep(0.05)
            print(cobs.decode(spp_message[:-1]).hex() )
            ser.write(spp_message)


    time.sleep(0.2)
    print("Sending COPY FRAM -> FPGA command...")
    ser.write(copy_pus81msg)
    time.sleep(0.5)




    print("Sending GET messages to FPGA and reading responses...")
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
   

    print(resp_data)
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