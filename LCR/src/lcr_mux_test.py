#!/usr/bin/env python

"""
@file:   lcr_mux_test.py

@author: Jason Mayeda
@date:   05/08/18
@brief:  Test the LCR and multiplexer.
"""

import time
from E4980a_lcr import LCR
from HP4067_mux import Mux


if __name__ == "__main__":
    # ================================= config ============================== #
    # LCR parameters
    LCR1 = 'R'              # LCR Channel 1
    LCR2 = 'X'              # LCR Channel 2
    LCR1_PRESCALE = 1e6     # Prescaling value for LCR1 reading
    LCR2_PRESCALE = 1e6     # Prescaling value for LCR2 reading
    NUM_SAMPLES = 25        # Number of sample points
    NUM_CHANNELS = 2        # Number of channels being read (default: 1)
    POLL_FREQ = 10          # Polling frequency (Hz)
    LCR_USB_ADDRESS = 'USB0::0x0957::0x0909::MY54202935::INSTR'

    # mulitplexer + Arduino
    ARDUINO_PORT = '/dev/cu.usbmodem14121'  # Arduino port address
                                            # (usually ~COM1, COM#) on pc
    MUX_SELECT_PINS = [12, 11, 10, 9] # multiplexer select pins[S0, S1, S2, S3]
    MUX_SIG_PIN = 0                   # mux signal pin
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

    # setup the HP6067 Multiplexer
    mux = Mux(config)
    # setup the E4980a LCR
    lcr = LCR(config)

    time.sleep(1) # give stuff time to work


