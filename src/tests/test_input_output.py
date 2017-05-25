# -*- coding: utf-8 -*-
"""
Unit tests for Source class

Created on Sun Mar 26 08:14:37 2017

@author: Calil
"""

import unittest
import numpy as np
from input_output import InputOutput as io
from channel.channel import Channel
from support.enumerations import SimType, ChannelModel

class InputOuputTest(unittest.TestCase, ):
    
    def setUp(self):
        self.sim_type = SimType.FIXED_SEEDS
        self.packet_number = 1000
        self.warm_up_packet_number = 10
        self.bits_per_packet = 500
        self.bit_rate = 50
        self.channel_model = ChannelModel.IDEAL
        self.rrc_filter_span = 6
        self.plot_PSD = True
        self.roll_off = 0.5
        self.sample_frequency = 2e6

        self.io = io()

    def test_write_csv_file(self):
        filename = 'Teste.csv'
        fieldnames = ['Simulation Type', 'Packet Number', 'Warm-Up Packet Number', 'Bits per Packet', 'Transmission Rate',
                      'Channel Model', 'RRC-Filter Span', 'Plot PSD', 'Roll-Off', 'Sample Frequency']
        fieldvalues = [self.sim_type, self.packet_number, self.warm_up_packet_number, self.bits_per_packet, self.bit_rate,
                       self.channel_model, self.rrc_filter_span, self.plot_PSD, self.roll_off, self.sample_frequency]
        self.io.write_csv_file(filename, fieldnames, fieldvalues)

if __name__ == '__main__':
    unittest.main()