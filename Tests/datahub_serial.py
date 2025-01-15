"""Early serial communication test that used the command line mode of the SPIDER2 software.
   This mode is not supported anymore, thus, this test likely does not work anymore.
"""

import serial
import codecs

def send_console_command(ser, msg):
    for letter in msg:
        ser.write(letter.encode())
    output = ser.readlines();
    return output

def parse_response(list_of_bytes_strings):
    for bs in list_of_bytes_strings:
        try:
            lines = bs.split(b'\n')
            for line in lines:
                if len(line) == 0:
                    continue
                print(line.decode("ascii"))
        except UnicodeDecodeError:
            print("Could not decode byte")

ser = serial.Serial('COM10', 115200, timeout=0.2)

ser.write(b'!A')
ser.write(b'!B')
ser.write(b'!D')
ser.write(b'!E')

ser.write(b'!C')
output = ser.readlines();
parse_response(output)

exit_msg = "exit\r"
fram_list = "fram list\r"
spp_message = "spp_message 1941C00000091F03800000640000FA66\r"
# First command is always faulty.
parse_response(send_console_command(ser, exit_msg))

parse_response(send_console_command(ser, fram_list))



parse_response(send_console_command(ser, spp_message))

parse_response(send_console_command(ser, exit_msg))


