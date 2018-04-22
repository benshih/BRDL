#!/usr/bin/env python

"""
lcr.py

@author: Jason Mayeda
@date:   04/03/2018

@about:  Python class for reading, plotting, and displaying data from the LCR.
         Data collection is initiated by calling 'run'.
@param:  'cfg' configuration parameters for the class
@return: plot of LCR data
"""

# Libraries
import visa
import matplotlib.pyplot as plt
import time


class LCR():
    def __init__(self, cfg):
        self.rm = visa.ResourceManager()  # start the pyVisa resource manager
        self.lcrObj = self.rm.open_resource('USB0::0x0957::0x0909::MY54202935::INSTR') # connect to lcr

        self.lcrOut1 = []  # LCR1 output list
        self.lcrOut2 = []  # LCR2 output list
        self.timeOut = []  # time list

        self.cfg = cfg     # load configuration parameters

    def run(self):
        # print header
        print('time(s) |    %s    |    %s   ' % (self.cfg['LCR1'], self.cfg['LCR2']))

        # get start time
        self.startTime = time.time()

        for i in range(self.cfg['NUM_SAMPLES']):
            # poll the data from the LCR
            out1, out2, timeSec = self.poll()

            # add outputs to list
            self.lcrOut1.append(out1)
            self.lcrOut2.append(out2)
            self.timeOut.append(timeSec)

            self.print_update(idx=i)

        # plot data using matplotlib
        self.plot_data()

        # call shutdown
        self.shutdown()

        self.testComplete = True
        print('Test complete.')

        return 0

    def poll(self):
        # poll the LCR
        data = self.lcrObj.query(':FETCh:IMPedance:FORM?')

        # split data string
        out = data.split(",")

        # scale outputs by prescaler for readibility
        out1 = float(out[0]) / self.cfg['LCR1_PRESCALE']
        out2 = float(out[1]) / self.cfg['LCR2_PRESCALE']

        # get current time in seconds
        timeSec = time.time() - self.startTime

        return out1, out2, timeSec

    def print_update(self, idx):
        # print data to the screen
        print('%.5f | %.4f | %.4f' % \
        (self.timeOut[idx], self.lcrOut1[idx], self.lcrOut2[idx]))

        return 0

    def shutdown(self):
        # close connection to the LCR
        self.lcrObj.close()

        self.lcrOut1 = []
        self.lcrOut2 = []
        self.timeOut = []

        return 0

    def plot_data(self):
        # plot the LCR output data
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(self.timeOut, self.lcrOut1)
        plt.title('LCR')
        plt.ylabel('LCR1 (MOhms)')
        plt.xlabel('Time (s)')
        plt.subplot(2,1,2)
        plt.plot(self.timeOut, self.lcrOut2)
        plt.ylabel('LCR2 (MOhms)')
        plt.xlabel('Time (s)')
        plt.show()

        return 0

    def plot_live_data(self):
        # TODO: python live plotting; ask Sebastian
        return 0
