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
    mux.switch_mux(channel=inputChannels[0], wait_s=0.5)

    lcr.startTime = time.time() # get start time

    # get NUM_SAMPLES data points
    for i in range(0, lcr.cfg['NUM_SAMPLES']):

        # log the time stamp
        lcr.timeOut[i] = time.time() - lcr.startTime

        # step over 2 steps at a time to record both measurements per channel
        for j in range(0, lcr.cfg['NUM_CHANNELS'] * 2 - 1, 2):

            # switch the mux to the c hannel of interest
            channelNum = math.floor(j/2)
            mux.switch_mux(channel=inputChannels[channelNum], wait_s=0.0)

            # poll the LCR
            out1, out2, timeSec = lcr.poll()
            lcr.output[i, j] = out1
            lcr.output[i, j+1] = out2

        # print update
        lcr.print_update(i)

    # plot data with matplotlib
    lcr.plot_data()

    # switch the mux between three channels
    lcr.save_to_txt()

    # just read the lcr
    lcr.shutdown()
    mux.shutdown()
