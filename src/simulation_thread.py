# -*- coding: utf-8 -*-
"""
Simulation thread class.

Created on Sun Apr  2 11:04:28 2017

@author: Calil
"""

import numpy as np

from results import Results
from source import Source
from channel import bschannel, ideal_channel, noise
from encoder import Encoder
from support.enumerations import SimType, ChannelModel, ModType
from statistics import Statistics
from theoretical import Theoretical
from modem import Modem
from rrc_filter import RRCFilter
from channel.fading import Fading
from input_output import InputOutput

class SimulationThread(object):
    def __init__(self,param,figs_dir):
        """
        Constructor method. Receives parameters and builds the simulation 
        objects.
        
        Keyword parameters:
            param -- parameters object
        """
        self.param = param
        self.station = Source(param.n_bits, param.seeds[0])
        self.encoder = Encoder(self.param.coding_process, self.param.mtx_code_dim, 0)
        if self.param.mod_type == ModType.CUSTOM:
            self.modem = Modem(self.param.mod_order, self.param.mod_type,
                               norm=self.param.symbol_norm,
                               pad=self.param.symbol_pad,
                               constellation=self.param.constellation)
        else:
            self.modem = Modem(self.param.mod_order, self.param.mod_type,
                               norm=self.param.symbol_norm,
                               pad=self.param.symbol_pad)
        
        self.filter = RRCFilter(self.param.filter_span, self.param.roll_off,
                                self.param.symbol_time,
                                self.param.sample_frequency)

        if self.param.chan_mod == ChannelModel.IDEAL:
            self.chann = ideal_channel.IdealChannel(self.param.seeds[0], self.param.p[0])
        elif self.param.chan_mod == ChannelModel.BSC:
            self.chann = bschannel.BSChannel(self.param.bsc_type, self.param.seeds[0],
                                             self.param.p[0], self.param.transition_mtx)

        self.noise = noise.Noise(self.param.seeds[0], self.param.ebn0[0],
                                 self.param.mod_order, self.param.n_bits)
        self.fading = Fading(self.param.doppler_freq, self.param.m,
                             self.param.m, self.param.time)
        self.stat = Statistics(self.param.ebn0, self.param.n_bits, self.param.tx_rate, self.param.conf)
        self.res = Results(self.param, figs_dir)
        self.theo = Theoretical(self.param)

        self.io = InputOutput()
        filename = 'Parameters.csv'
        fieldnames = ['Simulation Type', 'Packet Number', 'Warm-Up Packet Number', 'Bits per Packet', 'Transmission Rate',
                      'Channel Model', 'RRC-Filter Span', 'Plot PSD', 'Roll-Off', 'Sample Frequency']
        fieldvalues = [self.param.simulation_type, self.param.n_pcks, self.param.n_warm_up_pcks, self.param.n_bits, self.param.tx_rate,
                       self.param.chan_mod, self.param.filter_span, self.param.plot_psd, self.param.roll_off, self.param.sample_frequency]
        self.io.write_csv_file(filename, fieldnames, fieldvalues)

        self.__seed_count = 0
        self.__ebn0_count = 0

    def get_seed_count(self):
        """Returns the seed count."""
        return self.__seed_count
        
    def get_ebn0_count(self):
        """Returns the BER count."""
        return self.__ebn0_count
    
    def simulate(self):
        """
        Performs simulation loop and generates results.
        """
        # Seed loop
        self.seed_loop()

        # Validate and plot
        ber_theo, per_theo, thrpt_theo = self.theo.validate()
        self.res.plot(ber_theo, per_theo, thrpt_theo)
        
    def send_pck(self):
        """
        Generates, sends and calculates error for one packet for each SNR.
        
        Returns:
            n_errors -- number of bir errors in received packet
            pck_error -- boolean, True if packet has errors
        """
        # Transmission chain
        pck_tx = self.station.generate_packet()
        coded_tx = self.encoder.encode(pck_tx)
        sym_tx = self.modem.modulate(coded_tx)
        sig_tx = self.filter.tx_filter(sym_tx)

        # Test if the PSD graphic is supposed to be plotted
        if self.param.plot_psd:
           self.stat.plot_psd(self.param.sample_frequency, sig_tx)

        # Channel
        sig_rx = self.chann.propagate(sig_tx)

        # Noise addition
        n_errors_list = [0] * len(self.param.ebn0)
        pck_error_list = [0] * len(self.param.ebn0)
        for ebn0_idx in range(0, len(self.param.ebn0)):
            if not self.stat.get_criteria_per_snr()[ebn0_idx]:
                sig_corrupted = self.noise.add_noise(sig_rx)

                # Reception chain
                sym_rx_with_fading = self.fading.propagate(sig_corrupted)
                sym_rx_filtered = self.filter.rx_filter(sym_rx_with_fading)
                sym_rx = sym_rx_filtered/self.fading.get_fading()
                coded_rx = self.modem.demodulate(sym_rx)
                pck_rx = self.encoder.decode(coded_rx)
                n_errors, pck_error = self.station.calculate_error(pck_rx)
                n_errors_list[ebn0_idx] = n_errors
                pck_error_list[ebn0_idx] = pck_error
            else:
                pass
            self.new_ebn0()

        return n_errors_list, pck_error_list
    
    def pck_loop(self):
        """
        Loops throug all the necessary packet transmissions.
        """
        for pck in range(0, self.param.n_pcks):

            # Send packet
            n_errors_per_snr, pck_error_per_snr = self.send_pck()

            # Save results only if warm-up is over
            if pck > self.param.n_warm_up_pcks - 1:
                self.stat.add_new_stats(n_errors_per_snr, pck_error_per_snr)

            self.reset_ebn0()

    def seed_loop(self):
        """
        Loops through all the seeds.
        """
        drop_number = 1
        if self.param.simulation_type is SimType.FIXED_SEEDS:
            while drop_number <= self.param.max_drops:
                # Print drop number to screen
                print("Running drop number {}...".format(drop_number))

                # Packet loop, send all packets
                self.pck_loop()    

                # After all packets have been sent calculate iteration results
                self.stat.add_iteration_results()

                # Set new seed
                self.new_seed()

                drop_number += 1

            ber_tpl, per_tpl, thrpt_tpl = self.stat.wrap_up()

            self.res.store_res([ber_tpl, per_tpl, thrpt_tpl])

        elif self.param.simulation_type is SimType.FIXED_CONF:
            # Minimum confidence range between PER and Throughput
            while not all(self.stat.get_criteria_per_snr()):

                if drop_number == self.param.max_drops:
                    self.stat.set_criteria_per_snr([True for value in self.stat.get_criteria_per_snr()])

                # Print drop number to screen
                print("Running drop number {}...".format(drop_number))

                # Packet loop, send all packets
                self.pck_loop()

                # After all packets have been sent calculate iteration results
                self.stat.add_iteration_results()

                # Condition necessary for confidence interval can not be
                # computed with only one sample
                if self.get_seed_count() > 0:
                    ber_tpl, per_tpl, thrpt_tpl = self.stat.wrap_up()
                    self.stat.check_stats_per_snr(ber_tpl, per_tpl, thrpt_tpl, self.param.conf_range)

                # Set new seed
                self.new_seed()

                drop_number += 1

            self.res.store_res(self.stat.get_stats_results())

        else:
            raise NameError('Unknown simulation type!')
        
    
    def new_seed(self):
        """
        Sets the seed of all objects, incrementing the seed counter.
        """
        # Increment seed counter
        self.__seed_count = self.__seed_count + 1
        
        # If simulation type is fixed seeds
        if self.param.simulation_type is SimType.FIXED_SEEDS:
            
            # If the previous was not the last seed
            if self.get_seed_count() < len(self.param.seeds):
                # New seed is taken from param.seeds
                self.station.set_seed(self.param.seeds[self.get_seed_count()])
                self.chann.set_seed(self.param.seeds[self.get_seed_count()])
                
        # If simulation type is fixed confidence range
        elif self.param.simulation_type is SimType.FIXED_CONF:
            # New seed is the seed counter
            self.station.set_seed(self.get_seed_count())
            self.chann.set_seed(self.get_seed_count())
            
        else:
            raise NameError('Unknown simulation type!')
        
    def reset_seed(self):
        """
        Resets the seed of all objects.
        """
        # Set seed counter to zero
        self.__seed_count = 0
        
        # If simulation type is fixed seeds
        if self.param.simulation_type is SimType.FIXED_SEEDS:
            # New seed is taken from param.seeds
            self.station.set_seed(self.param.seeds[self.get_seed_count()])
            self.chann.set_seed(self.param.seeds[self.get_seed_count()])
            
        # If simulation type is fixed confidence range
        elif self.param.simulation_type is SimType.FIXED_CONF:
            # New seed is the seed counter
            self.station.set_seed(np.random.randint(1000000))
            self.chann.set_seed(np.random.randint(1000000))
            
        else:
            raise NameError('Unknown simulation type!')
    
    def new_ebn0(self):
        """
        Resets the channel's EBN0.
        """
        self.__ebn0_count = self.__ebn0_count + 1
        if self.get_ebn0_count() < len(self.param.ebn0):
            self.noise.set_ebn0_db(self.param.ebn0[self.get_ebn0_count()])

    def reset_ebn0(self):
        self.__ebn0_count = 0
        self.noise.set_ebn0_db(self.param.ebn0[self.get_ebn0_count()])
