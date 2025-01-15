"""pyserial test"""
import serial
import codecs


ser = serial.Serial('COM10', 115200, timeout=10)

#ser.write(b'Z')
output = ser.read(172)
print(output)


