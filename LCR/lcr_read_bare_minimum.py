# #!/usr/bin/env python

# """
# lcr_read_bare_minimum.py

# @date: 04/03/2018
# @about: Simple script to read data from the Keysight E4980AL LCR meter using PyVisa.

# PyVisa Documentation:
# https://pyvisa.readthedocs.io/en/stable/index.html
# """

# import visa
# import matplotlib.pyplot as plt
# import time


# if __name__ == "__main__":
#     # ================================== CONFIG ================================= #
#     LCR1 = 'Cp'              # LCR Channel 1
#     LCR2 = 'Rs'              # LCR Channel 2
#     LCR1_PRESCALE = 1     # Prescaling value for LCR1 reading (for readibiltiy)
#     LCR2_PRESCALE = 1e3     # Prescaling value for LCR2 reading (for readibility)
#     NUM_SAMPLES = 100        # Number of sample points
#     POLL_FREQ = 10          # Polling frequency (Hz)
#                             # if you do not use sleep, sample @ 0.153 sec
#     # =========================================================================== #

#     # start the pyVisa resource manager
#     rm = visa.ResourceManager()

#     # connect to lcr
#     lcr = rm.open_resource('USB0::0x0957::0x0909::MY54202935::INSTR')

#     # data
#     lcr1, lcr2, t = [], [], []  # initialize empty list for LCR data

#     # start time
#     startTime = time.time()  # start time
#     currentTime = startTime

#     # print header
#     print('time(s) |dTime(s)|    %s    |    %s   ' % (LCR1, LCR2))

#     # ========================== main data collection =========================== #
#     for i in range(NUM_SAMPLES):

#         # sample data from LCR
#         # data = lcr.query(':FETCh:IMPedance:FORMatted?')
#         data = lcr.query(':FETC:IMP:FORM?') # lower case letters are omitted

#         # keep track of time stamps
#         prevTime = currentTime
#         currentTime = time.time() - startTime
#         if i == 0:
#             dTime = 0
#         else:
#             dTime = currentTime - prevTime
#         t.append(currentTime)

#         # parse data, multiply by PRESCALE value for readibility
#         out = data.split(",")
#         lcr1.append(float(out[0]) / LCR1_PRESCALE)
#         lcr2.append(float(out[1]) / LCR2_PRESCALE)

#         # print to screen
#         print('%.5f | %.4f | %.4f | %.4f' % (currentTime, dTime, lcr1[i], lcr2[i]))

#         # time.sleep(1/POLL_FREQ) # for sampling a certain frequency
#     # =========================================================================== #

#     # clear the bus and close connection to LCR
#     lcr.clear()
#     lcr.close()


#     # plot the LCR output data
#     plt.figure()
#     plt.subplot(2,1,1)
#     plt.plot(t, lcr1)
#     plt.title('LCR')
#     plt.ylabel('LCR1 (MOhms)')
#     plt.xlabel('Time (s)')
#     plt.subplot(2,1,2)
#     plt.plot(t, lcr2)
#     plt.ylabel('LCR2 (MOhms)')
#     plt.xlabel('Time (s)')
#     plt.show()
