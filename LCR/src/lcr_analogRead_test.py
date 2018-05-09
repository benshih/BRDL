#!/usr/bin/env python

"""
@file: lcr_analogRead_test.py
@date: 05/08/18
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
    ARDUINO_PORT = '/dev/cu.usbmodem14111'  # Arduino port address
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

    # substitute the lcr with the analog read of the arduino for now.
    # want to cycle through mux pin
    #   C0: 2kohm
    #   C1: 10kohm
    #   C2: 100kohm
    myMux = Mux(config)

    time.sleep(1) # give stuff time to work

    myMux.switch_mux(channel=0, wait_s=0.05)
    print('mux switched to channel 0, R = 2kOhm')
    for i in range(10):
        print('R = 2000.0 | ', end='')
        # myMux.read_analog_resistance()
        time.sleep(.05)

    myMux.switch_mux(channel=1, wait_s=0.05)
    print('mux switched to channel 1, R = 10kOhm')
    for i in range(10):
        print('R = 10000.0 | ', end='')
        myMux.read_analog_resistance()
        time.sleep(.05)

    myMux.switch_mux(channel=2, wait_s=0.05)
    print('mux switched to channel 2, R = 100kOhm')
    for i in range(10):
        print('R = 100000.0 | ', end='')
        myMux.read_analog_resistance()
        time.sleep(.05)
 
    # loop through all of the channels
    R_OUT = [2000, 10000, 100000]
    for j in range(0, 3):
        myMux.switch_mux(channel=j, wait_s=0.05)
        print('R = %.2f | ' % R_OUT[j], end='')
        myMux.read_analog_resistance()
        time.sleep(.05)

    myMux.shutdown()
