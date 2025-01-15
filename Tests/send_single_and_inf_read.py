from single_send import *
import PUS_Tests.PUS_8_test



readback_req = PUS_Tests.PUS_8_test.GET_CURRENT_CONSTANT_BIAS_VALUE_COBS

send_single(readback_req)

for res in read_inf():
    print(str(res, "UTF-8"))



