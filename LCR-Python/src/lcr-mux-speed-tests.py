#!/usr/bin/env python

"""
@file: main.py

@date: 04/03/2018
@about: Simple script to read data from the Keysight E4980AL LCR meter using
        PyVisa. Creates an instance of LCR class. Polls data according to
        'config'. Plots data after data collection is complete.
"""

import time
from E4980a_lcr import LCR
from HP4067_mux import Mux
import math


if __name__ == "__main__":
    # ================================= config ============================== #
    # LCR parameters
    LCR1 = 'R'              # LCR Channel 1
    LCR2 = 'X'              # LCR Channel 2
    LCR1_PRESCALE = 1e6     # Prescaling value for LCR1 reading
    LCR2_PRESCALE = 1e6     # Prescaling value for LCR2 reading
    NUM_SAMPLES = 25        # Number of sample points
    NUM_CHANNELS = 3        # Number of channels being read (default: 1)
    POLL_FREQ = 10          # Polling frequency (Hz)
    LCR_USB_ADDRESS = 'USB0::0x0957::0x0909::MY54202935::INSTR'

    # mulitplexer + Arduino
    ARDUINO_PORT = '/dev/cu.usbmodem14111'  # Arduino port address
                                            # (usually ~COM1, COM#) on pc
    MUX_SELECT_PINS = [12, 11, 10, 9] # multiplexer select pins[S0, S1, S2, S3]
    MUX_SIG_PIN = 2                   # mux signal pin
    # ======================================================================= #

    # setup config parameters
    config = {'LCR1':            LCR1,
              'LCR2':            LCR2,
              'LCR1_PRESCALE':   LCR1_PRESCALE,
              'LCR2_PRESCALE':   LCR2_PRESCALE,
              'NUM_SAMPLES':     NUM_SAMPLES,
              'NUM_CHANNELS':    NUM_CHANNELS,
              'POLL_FREQ':       POLL_FREQ,
              'LCR_USB_ADDRESS': LCR_USB_ADDRESS,
              'ARDUINO_PORT':    ARDUINO_PORT,
              'MUX_SELECT_PINS': MUX_SELECT_PINS,
              'MUX_SIG_PIN':     MUX_SIG_PIN }

    # TODO: change way we handle the input channels
    inputChannels = [0, 1, 2]
    #----------------------------------------------#

    # initialize the LCR and Mux objects
    lcr = LCR(config)
    mux = Mux(config)

    # switch the mux to the first channel
    mux.switch_mux(channel=inputChannels[0], wait_s=0.0)

    # make pin 2 an output for reading on the o-scope
    pin2 = mux.board.get_pin('d:2:o')

    try:
        while True:
            # pull digital pin 2 HIGH
            pin2.write(1)

            mux.switch_mux(inputChannels[0], 0)
            lcr.poll()

            mux.switch_mux(inputChannels[1], 0)
            lcr.poll()

            mux.switch_mux(inputChannels[2], 0)
            lcr.poll()

            # pull digital pin 2 LOW
            pin2.write(0)

            # sleep
            time.sleep(0.1)  # 200 us
    except KeyboardInterrupt:
        pass

    mux.shutdown()
