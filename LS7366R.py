#!/usr/bin/python

#Python library to interface with the chip LS7366R for the Raspberry Pi
#Written by Federico Bolanos
#Source: https://github.com/fbolanos/LS7366R
#Last Edit: February 8th 2016
#Reason: Refactoring some names
#Update: November 4th 2017 by Thilo Brueckner & Sirius3 from 
#Forum: https://www.python-forum.de/viewtopic.php?f=31&t=41495#p316868

import struct
import spidev
from time import sleep


# Usage: import LS7366R then create an object by calling
# enc = LS7366R(cs_line, max_speed_hz, byte_mode)
# cs_line is either CE0 or CE1, max_speed_hz is the speed,
# byte_mode is the bytemode 1-4 the resolution of your counter.

class LS7366R():

    #-------------------------------------------
    # Constants

    #   Commands
    CLEAR_COUNTER = 0x20
    CLEAR_STATUS  = 0x30
    READ_COUNTER  = 0x60
    READ_STATUS   = 0x70
    WRITE_DTR     = 0x98
    LOAD_COUNTER  = 0xE0
    LOAD_OTR      = 0xE4
    WRITE_MODE0   = 0x88
    WRITE_MODE1   = 0x90

    #   Count Operating Modes
    #   0x00: non-quadrature count mode. (A = clock, B = direction).
    #   0x01: x1 quadrature count mode (one count per quadrature cycle).
    #   0x02: x2 quadrature count mode (two counts per quadrature cycle).
    #   0x03: x4 quadrature count mode (four counts per quadrature cycle).
    FOURX_COUNT = 0x01

    #   Count Byte Modes
    FOURBYTE_COUNTER  = 0x00	# counts from 0 to 4,294,967,295
    THREEBYTE_COUNTER = 0x01	# counts from 0 to    16,777,215
    TWOBYTE_COUNTER   = 0x02	# counts from 0 to        65,535
    ONEBYTE_COUNTER   = 0x03	# counts from 0 to           255

    #   Enable/disable counter
    EN_CNTR  = 0x00  # counting enabled
    DIS_CNTR = 0x04  # counting disabled

    BYTE_MODE = [ONEBYTE_COUNTER, TWOBYTE_COUNTER, THREEBYTE_COUNTER, FOURBYTE_COUNTER]

    #----------------------------------------------
    # Constructor

    def __init__(self, cs_line, max_speed_hz, byte_mode):
        self.byte_mode = byte_mode

        self.spi = spidev.SpiDev()
        self.spi.open(0, cs_line) # Which CS line will be used
        self.spi.max_speed_hz = max_speed_hz #Speed of clk (modifies speed transaction)

        #Init the Encoder
        self.clear_counter()
        self.clear_status()
        self.spi.xfer2([self.WRITE_MODE0, self.FOURX_COUNT])
        sleep(.1) #Rest
        self.spi.xfer2([self.WRITE_MODE1, self.BYTE_MODE[self.byte_mode-1]])

    def close(self):
        self.spi.close()

    def clear_counter(self):
        self.spi.xfer2([self.CLEAR_COUNTER])

    def clear_status(self):
        self.spi.xfer2([self.CLEAR_STATUS])

    def load_counter(self, enc_val):
        data = struct.pack(">I", enc_val)[-self.byte_mode:]
        self.spi.xfer2([self.WRITE_DTR] + list(ord(k) for k in data))
        self.spi.xfer2([self.LOAD_COUNTER])

    def read_counter(self):
        data = [self.READ_COUNTER] + [0] * self.byte_mode
        data = self.spi.xfer2(data)
        return reduce(lambda a,b: (a<<8) + b, data[1:], 0)

    def read_status(self):
        data = self.spi.xfer2([self.READ_STATUS, 0xFF])
        return data[1]


if __name__ == "__main__":
    from time import sleep

    encoder = LS7366R(0, 1000000, 4)
    try:
        while True:
	    sys.stdout.write('\rEncoder count: %11i CTRL+C for exit' % encoder.read_counter(),)
	    sys.stdout.flush()
            sleep(0.2)
    except KeyboardInterrupt:
        encoder.close()
        print "All done, bye bye."
