#!/usr/bin/env python

"""
@file:   HP4067_mux.py

@author: Jason Mayeda
@date:   05/04/2018

@brief:  Class for interfacing with the XXXX Multiplexer breakout board and
         Arduino integration using pyfirmata.
         Arduino boards require the standard firmata firmware.
         https://pypi.python.org/pypi/pyFirmata

"""

# Libraries
from pyfirmata import ArduinoMega, util
import time


class Mux():
    muxChannel = [[0, 0, 0, 0], # channel 1
                  [1, 0, 0, 0], # channel 2
                  [0, 1, 0, 0], # channel 3
                  [1, 1, 0, 0], # channel 4
                  [0, 0, 1, 0], # channel 5
                  [1, 0, 1, 0], # channel 6
                  [0, 1, 1, 0], # channel 7
                  [1, 1, 1, 0], # channel 8
                  [0, 0, 0, 1], # channel 9
                  [1, 0, 0, 1], # channel 10
                  [0, 1, 0, 1], # channel 11
                  [1, 1, 0, 1], # channel 12
                  [0, 0, 1, 1], # channel 13
                  [1, 0, 1, 1], # channel 14
                  [0, 1, 1, 1], # channel 15
                  [1, 1, 1, 1]] # channel 16

    def __init__(self, cfg):
        #load the config
        self.cfg = cfg
        self.board = ArduinoMega(cfg['ARDUINO_PORT'])

        # iterator thread for reading analog pins
        self.iter = util.Iterator(self.board)
        self.iter.start()
        print("iterator running.")

        # set the select pins as arduino digital pins
        self.s_pin_num = cfg['MUX_SELECT_PINS']
        self.s_pins = [self.board.get_pin('d:' + str(self.s_pin_num[0]) + ':o'),
                       self.board.get_pin('d:' + str(self.s_pin_num[1]) + ':o'),
                       self.board.get_pin('d:' + str(self.s_pin_num[2]) + ':o'),
                       self.board.get_pin('d:' + str(self.s_pin_num[3]) + ':o')]
        # set the signal pin
        # self.sig_pin = self.board.get_pin('d:' + str(cfg['MUX_SIG_PIN']) + ':o')

        # TODO: add some stuff to separate digital and analog pins
        self.sig_pin = self.board.get_pin('a:1:i')

        print("Mux connected.")

    def run(self):
        # TODO: Debugging
        for j in range(0, 5):
            for i in range(0, 3):
                print("channel: " + str(i))
                self.switch_mux(i, 1)

        # exit cleanly
        self.shutdown()

        return 0

    def switch_mux(self, channel, wait_s):
        """
        @about: switch mux signal pin to specified channel for specified time.
        @param: channel to switch the multiplexer to
        @param: wait_s delay time to stay at channel. sometimes the readings
                would take longer to "switch"
        """
        # write to selecter pins to specify the mux output channel
        for i in range(0, 4):
            self.s_pins[i].write(self.muxChannel[channel][i])

        print('Mux switched to channel %d' % channel)

        time.sleep(wait_s) # sleep and allow connection between the multimeter and selected pin

        return 0

    def write_mux(self, channel, wait_s, pin_value):
        """
        @about: call switch mux to switch mux channel. Write to signal pin with
                pin_value.
        # TODO: used for debugging
        """
        # call switch_mux to change the mux channel
        self.switch_mux(channel, wait_s)

        # do something with the LED's
        self.sig_pin.write(pin_value)
        time.sleep(wait_s)
        self.sig_pin.write(0)

        return 0

    def read_analog_resistance(self):
        """
        @brief: read the analog input pin and calculate the resistance
                using a voltage divider
        """
        R_IN = 1000.0
        V_IN = 5.0
        V_out = self.sig_pin.read() * V_IN # rescale it to the 5V bar
        R_out = (R_IN * V_out/V_IN) / (1.0 - (V_out/V_IN))
        print('R = %.2f' % R_out)

        return R_out

    def shutdown(self):
        """
        @about: close connection to board.
        """
        self.board.exit()
        print('Closed connection to mux.')

        return 0
