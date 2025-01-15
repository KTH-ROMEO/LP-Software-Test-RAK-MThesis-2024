"""Contains definitions of Message Argument IDs, Preambles, Postambles for PUS 8 Service.
    The test message definitions are used by other scripts to conduct tests.

    Each test message has three versions, for example:
        EN_PROBE_CONST_BIAS_MODE - The test message in hex numbers.
        EN_PROBE_CONST_BIAS_MODE_COBS - The test message wrapped in SPP and PUS headers, COBS encoded. This version is sent to the DataHub
        EN_PROBE_CONST_BIAS_MODE_RES - Used only when testing if the Microcontroller code is generating the correct uC - FPGA messages from PUS 8 messages.
"""
import sys
from SPP_PUS_test import *


FPGA_PREAMBLE = b'\xB5\x43'
FPGA_POSTAMBLE = b'\x0A'

def get_correct_result(data):
    correct_response = FPGA_PREAMBLE
    for i in range(len(data)):
        correct_response += (data[i]).to_bytes()
    
    correct_response += FPGA_POSTAMBLE
    correct_response += b'\x00'

    return correct_response


def get_PUS_8_TC(data):
    return get_PUS_TC(8, 1, data)

EN_CB_MODE_ID                   = 0xCA
DIS_CB_MODE_ID                  = 0xC0
SET_CB_VOL_LVL_ID               = 0xCB
GET_CB_VOL_LVL_ID               = 0xCC
SWT_ACTIVATE_SWEEP_ID           = 0xAA
SET_SWT_VOL_LVL_ID              = 0xAB
SET_SWT_STEPS_ID                = 0xAC
SET_SWT_SAMPLES_PER_STEP_ID     = 0xAD
SET_SWT_SAMPLE_SKIP_ID          = 0xAE
SET_SWT_SAMPLES_PER_POINT_ID    = 0xAF
SET_SWT_NPOINTS_ID              = 0xB0

GET_SWT_SWEEP_CNT_ID            = 0xA0
GET_SWT_VOL_LVL_ID              = 0xA1
GET_SWT_STEPS_ID                = 0xA2
GET_SWT_SAMPLES_PER_STEP_ID     = 0xA3
GET_SWT_SAMPLE_SKIP_ID          = 0xA4
GET_SWT_SAMPLES_PER_POINT_ID    = 0xA5
GET_SWT_NPOINTS_ID              = 0xA6

PROBE_ID_ARG_ID         = 0x01
STEP_ID_ARG_ID          = 0x02
VOL_LVL_ARG_ID          = 0x03
N_STEPS_ARG_ID          = 0x04
N_SKIP_ARG_ID           = 0x05
N_F_ARG_ID              = 0x06
N_POINTS_ARG_ID         = 0x07
GS_TARGET_ARG_ID        = 0x08
FRAM_TABLE_ID_ARG_ID    = 0x09
N_SAMPLES_PER_STEP_ARG_ID = 0x0A
    
EN_PROBE_CONST_BIAS_MODE                 = [EN_CB_MODE_ID,       0x00]
EN_PROBE_CONST_BIAS_MODE_COBS            = get_PUS_8_TC(bytearray(EN_PROBE_CONST_BIAS_MODE))
EN_PROBE_CONST_BIAS_MODE_RES             = get_correct_result([EN_PROBE_CONST_BIAS_MODE[0]])



SET_CONSTANT_BIAS_VOLTAGE                = [SET_CB_VOL_LVL_ID,        0x02,   PROBE_ID_ARG_ID,  0x00,  VOL_LVL_ARG_ID,   0xAB, 0xCD]
SET_CONSTANT_BIAS_VOLTAGE_COBS           = get_PUS_8_TC(bytearray(SET_CONSTANT_BIAS_VOLTAGE))
SET_CONSTANT_BIAS_VOLTAGE_RES            = get_correct_result([
                                                SET_CONSTANT_BIAS_VOLTAGE[0],
                                                SET_CONSTANT_BIAS_VOLTAGE[3],
                                                SET_CONSTANT_BIAS_VOLTAGE[-2],
                                                SET_CONSTANT_BIAS_VOLTAGE[-1],
                                            ])



DIS_PROBE_CONST_BIAS_MODE                 = [DIS_CB_MODE_ID,       0x00]
DIS_PROBE_CONST_BIAS_MODE_COBS            = get_PUS_8_TC(bytearray(DIS_PROBE_CONST_BIAS_MODE))
DIS_PROBE_CONST_BIAS_MODE_RES             = get_correct_result([DIS_PROBE_CONST_BIAS_MODE[0]])



GET_CURRENT_CONSTANT_BIAS_VALUE          = [GET_CB_VOL_LVL_ID,       0x01,   PROBE_ID_ARG_ID,  0x00]
GET_CURRENT_CONSTANT_BIAS_VALUE_COBS     = get_PUS_8_TC(bytearray(GET_CURRENT_CONSTANT_BIAS_VALUE))
GET_CURRENT_CONSTANT_BIAS_VALUE_RES      = get_correct_result([
                                                GET_CURRENT_CONSTANT_BIAS_VALUE[0],
                                                GET_CURRENT_CONSTANT_BIAS_VALUE[-1],
                                            ])



SWEEP_BIAS_MODE_ACTIVATE_SWEEP            = [SWT_ACTIVATE_SWEEP_ID,       0x00]
SWEEP_BIAS_MODE_ACTIVATE_SWEEP_COBS       = get_PUS_8_TC(bytearray(SWEEP_BIAS_MODE_ACTIVATE_SWEEP))
SWEEP_BIAS_MODE_ACTIVATE_SWEEP_RES        = get_correct_result([SWEEP_BIAS_MODE_ACTIVATE_SWEEP[0]])



SET_VOLTAGE_LEVEL_SWEEP_MODE             = [SET_SWT_VOL_LVL_ID, 0x04,   PROBE_ID_ARG_ID,  0x00,  STEP_ID_ARG_ID,   0x1A,   VOL_LVL_ARG_ID,  0xEC , 0x2A, GS_TARGET_ARG_ID, 0x00]
SET_VOLTAGE_LEVEL_SWEEP_MODE_COBS        = get_PUS_8_TC(bytearray(SET_VOLTAGE_LEVEL_SWEEP_MODE))
SET_VOLTAGE_LEVEL_SWEEP_MODE_RES         = get_correct_result([
                                                SET_VOLTAGE_LEVEL_SWEEP_MODE[0],
                                                SET_VOLTAGE_LEVEL_SWEEP_MODE[3],
                                                SET_VOLTAGE_LEVEL_SWEEP_MODE[5],
                                                SET_VOLTAGE_LEVEL_SWEEP_MODE[-4],
                                                SET_VOLTAGE_LEVEL_SWEEP_MODE[-3]
                                            ])



SET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM           = [SET_SWT_VOL_LVL_ID, 0x04,   PROBE_ID_ARG_ID,  0x00,  STEP_ID_ARG_ID,   0x0B,   VOL_LVL_ARG_ID,  0xE0 , 0xB1, GS_TARGET_ARG_ID, 0x01]
SET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_COBS      = get_PUS_8_TC(bytearray(SET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM))
SET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_RES       = get_correct_result([]) # No FPGA msg when setting in FRAM



SET_NOF_STEPS_SWEEP_MODE                 = [SET_SWT_STEPS_ID, 0x01,   N_STEPS_ARG_ID,  0xBC]
SET_NOF_STEPS_SWEEP_MODE_COBS            = get_PUS_8_TC(bytearray(SET_NOF_STEPS_SWEEP_MODE))
SET_NOF_STEPS_SWEEP_MODE_RES             = get_correct_result([
                                                SET_NOF_STEPS_SWEEP_MODE[0],
                                                SET_NOF_STEPS_SWEEP_MODE[-1]
                                            ])

SET_NOF_SAMPLES_PER_STEP                = [SET_SWT_SAMPLES_PER_STEP_ID, 0x01, N_SAMPLES_PER_STEP_ARG_ID, 0xE3, 0xB3]
SET_NOF_SAMPLES_PER_STEP_COBS           = get_PUS_8_TC(bytearray(SET_NOF_SAMPLES_PER_STEP))
SET_NOF_SAMPLES_PER_STEP_RES            = get_correct_result([
                                            SET_NOF_SAMPLES_PER_STEP[0],
                                            SET_NOF_SAMPLES_PER_STEP[-2],
                                            SET_NOF_SAMPLES_PER_STEP[-1],
                                        ])


SET_NOF_SKIP_SWEEP_MODE                 = [SET_SWT_SAMPLE_SKIP_ID, 0x01,   N_SKIP_ARG_ID,  0x07, 0x00]
SET_NOF_SKIP_SWEEP_MODE_COBS            = get_PUS_8_TC(bytearray(SET_NOF_SKIP_SWEEP_MODE))
SET_NOF_SKIP_SWEEP_MODE_RES             = get_correct_result([
                                                SET_NOF_SKIP_SWEEP_MODE[0],
                                                SET_NOF_SKIP_SWEEP_MODE[-2],
                                                SET_NOF_SKIP_SWEEP_MODE[-1],
                                            ])




SET_NOF_F_SWEEP_MODE                    = [SET_SWT_SAMPLES_PER_POINT_ID, 0x01,   N_F_ARG_ID,  0x12, 0x00]
SET_NOF_F_SWEEP_MODE_COBS               = get_PUS_8_TC(bytearray(SET_NOF_F_SWEEP_MODE))
SET_NOF_F_SWEEP_MODE_RES                = get_correct_result([
                                                SET_NOF_F_SWEEP_MODE[0],
                                                SET_NOF_F_SWEEP_MODE[-2],
                                                SET_NOF_F_SWEEP_MODE[-1],
                                            ])




SET_NOF_POINTS_SWEEP_MODE                 = [SET_SWT_NPOINTS_ID, 0x01,   N_POINTS_ARG_ID,  0xEE, 0x00]
SET_NOF_POINTS_SWEEP_MODE_COBS            = get_PUS_8_TC(bytearray(SET_NOF_POINTS_SWEEP_MODE))
SET_NOF_POINTS_SWEEP_MODE_RES             = get_correct_result([
                                                SET_NOF_POINTS_SWEEP_MODE[0],
                                                SET_NOF_POINTS_SWEEP_MODE[-2],
                                                SET_NOF_POINTS_SWEEP_MODE[-1],
                                            ])


GET_SWEEP_BIAS_MODE_SWEEP_COUNT           = [GET_SWT_SWEEP_CNT_ID, 0x00]
GET_SWEEP_BIAS_MODE_SWEEP_COUNT_COBS      = get_PUS_8_TC(bytearray(GET_SWEEP_BIAS_MODE_SWEEP_COUNT))
GET_SWEEP_BIAS_MODE_SWEEP_COUNT_RES       = get_correct_result([GET_SWEEP_BIAS_MODE_SWEEP_COUNT[0]])



GET_VOLTAGE_LEVEL_SWEEP_MODE             = [GET_SWT_VOL_LVL_ID, 0x03,   PROBE_ID_ARG_ID,  0x00,  STEP_ID_ARG_ID,   0x1A, GS_TARGET_ARG_ID, 0x00]
GET_VOLTAGE_LEVEL_SWEEP_MODE_COBS        = get_PUS_8_TC(bytearray(GET_VOLTAGE_LEVEL_SWEEP_MODE))
GET_VOLTAGE_LEVEL_SWEEP_MODE_RES         = get_correct_result([
                                                GET_VOLTAGE_LEVEL_SWEEP_MODE[0],
                                                GET_VOLTAGE_LEVEL_SWEEP_MODE[3],
                                                GET_VOLTAGE_LEVEL_SWEEP_MODE[-3]
                                            ])



GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM        = [GET_SWT_VOL_LVL_ID, 0x03,   PROBE_ID_ARG_ID,  0x00,  STEP_ID_ARG_ID,   0x0B, GS_TARGET_ARG_ID, 0x01]
GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_COBS   = get_PUS_8_TC(bytearray(GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM))
GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_RES    = get_correct_result([
                                                GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM[0],
                                                GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM[3],
                                                GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM[-3]
                                            ])



GET_NOF_STEPS_SWEEP_MODE                 = [GET_SWT_STEPS_ID, 0x00]
GET_NOF_STEPS_SWEEP_MODE_COBS            = get_PUS_8_TC(bytearray(GET_NOF_STEPS_SWEEP_MODE))
GET_NOF_STEPS_SWEEP_MODE_RES             = get_correct_result([GET_NOF_STEPS_SWEEP_MODE[0]])



GET_NOF_SAMPLES_PER_STEP                = [GET_SWT_SAMPLES_PER_STEP_ID, 0x00]
GET_NOF_SAMPLES_PER_STEP_COBS           = get_PUS_8_TC(bytearray(GET_NOF_SAMPLES_PER_STEP))
GET_NOF_SAMPLES_PER_STEP_RES            = get_correct_result([
                                            GET_NOF_SAMPLES_PER_STEP[0],
                                        ])


GET_NOF_SKIP_SWEEP_MODE                 = [GET_SWT_SAMPLE_SKIP_ID, 0x00]
GET_NOF_SKIP_SWEEP_MODE_COBS            = get_PUS_8_TC(bytearray(GET_NOF_SKIP_SWEEP_MODE))
GET_NOF_SKIP_SWEEP_MODE_RES             = get_correct_result([
                                                GET_NOF_SKIP_SWEEP_MODE[0],
                                            ])




GET_NOF_F_SWEEP_MODE                    = [GET_SWT_SAMPLES_PER_POINT_ID, 0x00]
GET_NOF_F_SWEEP_MODE_COBS               = get_PUS_8_TC(bytearray(GET_NOF_F_SWEEP_MODE))
GET_NOF_F_SWEEP_MODE_RES                = get_correct_result([
                                                GET_NOF_F_SWEEP_MODE[0],
                                            ])




GET_NOF_POINTS_SWEEP_MODE                 = [GET_SWT_NPOINTS_ID, 0x00]
GET_NOF_POINTS_SWEEP_MODE_COBS            = get_PUS_8_TC(bytearray(GET_NOF_POINTS_SWEEP_MODE))
GET_NOF_POINTS_SWEEP_MODE_RES             = get_correct_result([
                                                GET_NOF_POINTS_SWEEP_MODE[0],
                                            ])


PUS_8_TCs = [
    EN_PROBE_CONST_BIAS_MODE_COBS,
    SET_CONSTANT_BIAS_VOLTAGE_COBS,
    DIS_PROBE_CONST_BIAS_MODE_COBS,
    GET_CURRENT_CONSTANT_BIAS_VALUE_COBS,
    SWEEP_BIAS_MODE_ACTIVATE_SWEEP_COBS,
    SET_VOLTAGE_LEVEL_SWEEP_MODE_COBS,
    SET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_COBS,
    SET_NOF_STEPS_SWEEP_MODE_COBS,
    SET_NOF_SAMPLES_PER_STEP_COBS,
    SET_NOF_SKIP_SWEEP_MODE_COBS,
    SET_NOF_F_SWEEP_MODE_COBS,
    SET_NOF_POINTS_SWEEP_MODE_COBS,
    GET_SWEEP_BIAS_MODE_SWEEP_COUNT_COBS,
    GET_VOLTAGE_LEVEL_SWEEP_MODE_COBS,
    GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_COBS,
    GET_NOF_STEPS_SWEEP_MODE_COBS,
    GET_NOF_SAMPLES_PER_STEP_COBS,
    GET_NOF_SKIP_SWEEP_MODE_COBS,
    GET_NOF_F_SWEEP_MODE_COBS,
    GET_NOF_POINTS_SWEEP_MODE_COBS,
]

PUS_8_TC_SETs = [
    #EN_PROBE_CONST_BIAS_MODE_COBS,
    SET_CONSTANT_BIAS_VOLTAGE_COBS,
    SWEEP_BIAS_MODE_ACTIVATE_SWEEP_COBS,
    SET_VOLTAGE_LEVEL_SWEEP_MODE_COBS,
    SET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_COBS,
    SET_NOF_STEPS_SWEEP_MODE_COBS,
    SET_NOF_SAMPLES_PER_STEP_COBS,
    SET_NOF_SKIP_SWEEP_MODE_COBS,
    SET_NOF_F_SWEEP_MODE_COBS,
    SET_NOF_POINTS_SWEEP_MODE_COBS,
]

PUS_8_TC_GETs = [
    #DIS_PROBE_CONST_BIAS_MODE_COBS,
    GET_CURRENT_CONSTANT_BIAS_VALUE_COBS,
    GET_SWEEP_BIAS_MODE_SWEEP_COUNT_COBS,
    GET_VOLTAGE_LEVEL_SWEEP_MODE_COBS,
    GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_COBS,
    GET_NOF_STEPS_SWEEP_MODE_COBS,
    GET_NOF_SAMPLES_PER_STEP_COBS,
    GET_NOF_SKIP_SWEEP_MODE_COBS,
    GET_NOF_F_SWEEP_MODE_COBS,
    GET_NOF_POINTS_SWEEP_MODE_COBS,
]
response = [
    EN_PROBE_CONST_BIAS_MODE_RES,
    SET_CONSTANT_BIAS_VOLTAGE_RES,
    DIS_PROBE_CONST_BIAS_MODE_RES,
    GET_CURRENT_CONSTANT_BIAS_VALUE_RES,
    SWEEP_BIAS_MODE_ACTIVATE_SWEEP_RES,
    SET_VOLTAGE_LEVEL_SWEEP_MODE_RES,
    SET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_RES,
    SET_NOF_STEPS_SWEEP_MODE_RES,
    SET_NOF_SAMPLES_PER_STEP_RES,
    SET_NOF_SKIP_SWEEP_MODE_RES,
    SET_NOF_F_SWEEP_MODE_RES,
    SET_NOF_POINTS_SWEEP_MODE_RES,
    GET_SWEEP_BIAS_MODE_SWEEP_COUNT_RES,
    GET_VOLTAGE_LEVEL_SWEEP_MODE_RES,
    GET_VOLTAGE_LEVEL_SWEEP_MODE_FRAM_RES,
    GET_NOF_STEPS_SWEEP_MODE_RES,
    GET_NOF_SAMPLES_PER_STEP_RES,
    GET_NOF_SKIP_SWEEP_MODE_RES,
    GET_NOF_F_SWEEP_MODE_RES,
    GET_NOF_POINTS_SWEEP_MODE_RES,
]

def get_variable_name(obj, namespace):
    return [name for name, value in namespace.items() if value is obj][0]

if len(sys.argv) > 1 and sys.argv[1] == "r":
    for r in response:
        print(get_variable_name(r, locals()), "\t\t" ,r.hex())
#SET_DEV_STATE_NORMAL                     = [0x00, 0x01]

#SET_DEV_STATE_IDLE                       = [0x01, 0x01]

#SET_DEV_STATE_REBOOT                     = [0x03, 0x01]

#SET_DEV_STATE_UPDATE                     = [0x04, 0x01]

#SET_DEV_STATE_SWAP_IMAGE                 = [0x05, 0x01]


#data = bytearray([0x23, 0x00, 0x03, 0x01, 0x00, 0x02, 0xEF, 0x03, 0xEC, 0xDE])

#print(enc_spp.hex())
#print(enc_pus.hex())
#print(tot_hed.hex())
#print(data.hex())
#print(fin_msg.hex())
#print(cobs_msg.hex())
