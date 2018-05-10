#!/usr/bin/env python

"""
@file:   E4980a_lcr.py

@author: Jason Mayeda
@date:   04/03/2018

@about:  Python class for reading, plotting, and displaying data from the LCR.
         Data collection is initiated by calling 'run'.
"""

# Libraries
import visa
import matplotlib.pyplot as plt
import numpy as np
import time


class LCR():
    def __init__(self, cfg):
        self.cfg = cfg     # load configuration parameters
        self.numChannels = self.cfg['NUM_CHANNELS']

        self.rm = visa.ResourceManager()  # start the pyVisa resource manager
        # connect to lcr
        self.lcr = self.rm.open_resource(self.cfg['LCR_USB_ADDRESS'])

        self.timeOut = np.zeros((self.cfg['NUM_SAMPLES'], 1))

        # output stores the LCR data and is a
            # np array numSample x (numChannels*2)
        self.output = np.zeros((self.cfg['NUM_SAMPLES'], self.numChannels * 2))

        self.startTime = -1.0

        print('LCR connected.')

    def run_single_channel(self, numSamples):
        """
        @about: read the LCR on a single channel
        @param: numSamples number of sample points.
        """
        # get start time
        self.startTime = time.time()

        for i in range(0, numSamples):
            # poll the data from the LCR
            out1, out2, timeSec = self.poll()

            self.output[i, 0] = out1
            self.output[i, 1] = out2
            self.timeOut[i] = timeSec

            self.print_update(idx=i)

        # save data
        self.save_to_txt()

        # plot data using matplotlib
        self.plot_data()

        # call shutdown
        self.shutdown()

        return 0

    def run_with_mux(self):
        #TODO: add mux object to lcr class
        return 0

    def poll(self):
        """
        @about: poll the LCR for one measurement of the current setting.
        @return: parsed output from LCR and time stamp
        """
        # poll the LCR
        data = self.lcr.query(':FETCh:IMPedance:FORM?')

        # split data string
        out = data.split(",")

        # scale outputs by prescaler for readibility
        out1 = float(out[0]) #/ self.cfg['LCR1_PRESCALE']
        out2 = float(out[1]) #/ self.cfg['LCR2_PRESCALE']

        # get current time in seconds
        timeSec = time.time() - self.startTime

        return out1, out2, timeSec

    def switch_lcr_meas(self, function):
        """
        TODO: add switch case statement for switching measurement function
        @about: change the lcr measurement function using pyvisa write.
        @param: function string describing measurement function.
                ex: CpD for Capacitance in Parallel
        """
        # self.lcr.write(':FUNC:IMP:CPD')
        return 0

    def print_update(self, idx):
        """
        @about: print an update of all data in a single line
        @param: idx index of the data in the numpy array
        """
        print('%.2f' % self.timeOut[idx], end = '')

        # loop through all the channels and print to screen
        for j in range(0, self.numChannels * 2):
            print(' %.4f ' % self.output[idx, j], end = '')

        print('') # print a new line

        return 0

    def plot_data(self):
        """
        @about: plot the LCR output data in a single figure
        """
        plt.figure()
        for i in range(0, self.numChannels * 2):
            plt.subplot(self.numChannels, 2, i+1)
            plt.plot(self.timeOut, self.output[:, i], '*')
            plt.xlabel('Time (s)')
            plt.ylabel('')

            if (i % 2 == 0):
                plt.title('R') # TODO: change plot labels
            else:
                plt.title('X')

        # plot all channels on one graph
        plt.figure()
        for i in range(0, self.numChannels * 2 - 1, 2):
            plt.plot(self.timeOut, self.output[:,i], '+')
            plt.xlabel('Time (s)')
        plt.show()

        return 0

    def plot_live_data(self):
        """
        @about: plot live data to the screen
        TODO: python live plotting; ask Sebastian
        """
        return 0

    def save_to_txt(self):
        """
        @about: save data to a text file
        """
        # TODO: add a more descriptive string
        txtData = np.concatenate((self.timeOut, self.output), axis=1)
        np.savetxt('sample_data', txtData, delimiter=',')

        return 0

    def shutdown(self):
        """
        @brief: close connection to the LCR, clear arrays
        """
        self.lcr.clear()
        self.lcr.close()

        # clear output arrays
        self.timeOut = np.zeros((self.cfg['NUM_SAMPLES']))
        self.output = np.zeros((self.cfg['NUM_SAMPLES'], self.numChannels * 2))

        print('LCR shutting down...')

        return 0
