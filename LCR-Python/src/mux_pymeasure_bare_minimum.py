#!/usr/bin/env python

from pymeasure.instruments.agilent import AgilentE4980
from pymeasure.adapters import VISAAdapter
from HP4067_mux import Mux
import matplotlib.pyplot as plt
import time


if __name__ == "__main__":
    # ================================= config ============================== #
    # LCR parameters (DEPRECATED)
    LCR1 = 'R'  # LCR Channel 1
    LCR2 = 'X'  # LCR Channel 2
    LCR1_PRESCALE = 1e6  # Prescaling value for LCR1 reading
    LCR2_PRESCALE = 1e6  # Prescaling value for LCR2 reading
    NUM_SAMPLES = 25     # Number of sample points
    NUM_CHANNELS = 3     # Number of channels being read (default: 1)
    POLL_FREQ = 10       # Polling frequency (Hz)
    # DEPRECATED ---------------------------------------------------------------

    # LCR Parameters for PyMeasure 
    LCR_USB_ADDRESS = 'USB0::0x0957::0x0909::MY54202935::INSTR'
    LCR_AC_FREQUENCY = 15000 # AC signal frequencyb
    LCR_AC_VOLTAGE = 0.5     # AC signal voltage
    LCR_MEAS_TIME = "SHORT"  # LCR measurement time

    # mulitplexer + Arduino
    ARDUINO_PORT = '/dev/cu.usbmodem14111'  # Arduino port address, COM# in PC
    MUX_SELECT_PINS = [12, 11, 10, 9]  # multiplexer select pins[S0, S1, S2, S3]
    MUX_SIG_PIN = 2
    # ======================================================================= #

    # setup config parameters
    config = {'LCR1': LCR1,
              'LCR2': LCR2,
              'LCR1_PRESCALE': LCR1_PRESCALE,
              'LCR2_PRESCALE': LCR2_PRESCALE,
              'NUM_SAMPLES': NUM_SAMPLES,
              'NUM_CHANNELS': NUM_CHANNELS,
              'POLL_FREQ': POLL_FREQ,
              'LCR_USB_ADDRESS': LCR_USB_ADDRESS,
              'ARDUINO_PORT': ARDUINO_PORT,
              'MUX_SELECT_PINS': MUX_SELECT_PINS,
              'MUX_SIG_PIN': MUX_SIG_PIN}

    # TODO: change way we handle the input channels
    muxInputChannels = [0, 1, 2]
    # ----------------------------------------------#

    # initialize the multiplexer board through pyFirmata
    mux = Mux(config)
    # pin2 = mux.board.get_pin('d:2:o')

    # setup the LCR
    adapter = VISAAdapter("USB0::0x0957::0x0909::MY54202935::INSTR")
    lcr = AgilentE4980(adapter)
    print("LCR connected.")

    # TODO: make new LCR class to make this process cleaner
    lcr.reset()
    lcr.aperture(LCR_MEAS_TIME)       # set measurement time
    lcr.frequency = LCR_AC_FREQUENCY  # set AC signal frequency
    lcr.ac_voltage = LCR_AC_VOLTAGE   # set AC signal voltage

    # initialize lists to store data
    timeOut = []
    ROut = []
    LOut = []
    COut = []

    # record start time
    timeStart = time.time()

    # Cycle through channels R-L-C
    try:
        while True:
            # for Debugging
            # pin2.write(1) # pull the pin high

            # Switch mux to channel 0
            mux.switch_mux(channel=muxInputChannels[0], wait_s=0.0)
            lcr.mode = "RX"  # set mode to resistance in series
            ROut.append(lcr.impedance[0])

            # Switch mux to channel 1
            mux.switch_mux(channel=muxInputChannels[1], wait_s=0.0)
            lcr.mode = "LPD"  # set mode to Inductance in parallel
            LOut.append(lcr.impedance[0])

            # switch mux to channel 2
            mux.switch_mux(channel=muxInputChannels[2], wait_s=0.0)
            lcr.mode = "CPD"  # set mode to Capacitance in parallel
            COut.append(lcr.impedance[0])

            # record time stamp used for all channels
            timeOut = time.time() - timeStart

            # For debugging
            # pull pin 0 low
            # pin2.write(0)
            # sleep for o-scope tests
            # time.sleep(0.100)

    except KeyboardInterrupt:
        pass

    # Exit cleanly
    lcr.shutdown()
    mux.shutdown()
    print("Exiting cleanly...")

    # Graph the data
    plt.figure()
    plt.subplot(311)
    plt.plot(timeOut, ROut, color='b', linestyle = ':')
    plt.xlabel('time (s)')
    plt.ylabel('Resistance')
    plt.subplot(312)
    plt.plot(timeOut, LOut, color='y', linestyle = ':')
    plt.xlabel('time (s)')
    plt.ylabel('Inductance')
    plt.subplot(313)
    plt.plot(timeOut, COut, color='g', linestyle = ':')
    plt.xlabel('time (s)')
    plt.ylabel('Capacitance')
    plt.show()
