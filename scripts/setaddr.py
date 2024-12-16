#
# set modbus device address
#

import serial
from modbus import read_register, write_register

UART = "/dev/ttyUSB0"

CONFIG_ADDRESS_REGISTER = 2000
CONFIG_SPEED_REGISTER = 2001

DEV_ADDR = 1
NEW_ADDR = 2

# (port,baudrate,timeout=0.001)
uart = serial.Serial(UART, 4800, timeout=1)


# set addr 1->2

# print( write_register(uart, DEV_ADDR, CONFIG_ADDRESS_REGISTER, NEW_ADDR))
# print( read_register(uart, NEW_ADDR, CONFIG_ADDRESS_REGISTER))

# set addr 2->1

# print( write_register(uart, NEW_ADDR, CONFIG_ADDRESS_REGISTER, DEV_ADDR))
# print( read_register(uart, DEV_ADDR, CONFIG_ADDRESS_REGISTER))

print( read_register(uart, DEV_ADDR, CONFIG_ADDRESS_REGISTER) )
print( read_register(uart, NEW_ADDR, CONFIG_ADDRESS_REGISTER) )

print( "reg0:", read_register(uart, DEV_ADDR, 0) )
print( "reg1:", read_register(uart, DEV_ADDR, 1) )

print( "reg0:", read_register(uart, NEW_ADDR, 0) )
print( "reg1:", read_register(uart, NEW_ADDR, 1) )
