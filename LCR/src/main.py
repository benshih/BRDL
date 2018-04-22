#!/usr/bin/env python

"""
lcr_read

@date: 04/03/2018
@about: Simple script to read data from the Keysight E4980AL LCR meter using PyVisa.
        Creates an instance of LCR class. Polls data according to 'config'. Plots data after
        data collection is complete.
"""

import visa
import matplotlib.pyplot as plt
import time
from lcr import LCR


if __name__ == "__main__":
    # ================================== config ============================== #
    LCR1 = 'R'              # LCR Channel 1
    LCR2 = 'X'              # LCR Channel 2
    LCR1_PRESCALE = 1e6     # Prescaling value for LCR1 reading (for readibiltiy)
    LCR2_PRESCALE = 1e6     # Prescaling value for LCR2 reading (for readibility)
    NUM_SAMPLES = 50        # Number of sample points
    POLL_FREQ = 10          # Polling frequency (Hz)
    # ======================================================================== #

    # setup config parameters
    config = {'LCR1': LCR1,
             'LCR2': LCR2,
             'LCR1_PRESCALE': LCR1_PRESCALE,
             'LCR2_PRESCALE': LCR2_PRESCALE,
             'NUM_SAMPLES': NUM_SAMPLES,
             'POLL_FREQ': POLL_FREQ}

    # read the LCR
    lcr = LCR(config)
    lcr.run()
