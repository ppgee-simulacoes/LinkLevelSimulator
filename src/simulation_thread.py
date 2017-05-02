# -*- coding: utf-8 -*-
"""
Simulation thread class.

Created on Sun Apr  2 11:04:28 2017

@author: Calil
"""

from results import Results
from source import Source
from src.channel import bschannel, ideal_channel, noise
from src.support.enumerations import SimType, ChannelModel
from statistics import Statistics
from theoretical import Theoretical


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
        if self.param.chan_mod == ChannelModel.IDEAL:
            self.chann = ideal_channel.IdealChannel(param.seeds[0], param.p[0])
        elif self.param.chan_mod == ChannelModel.BSC:
            self.chann = bschannel.BSChannel(param.bsc_type, param.seeds[0], param.p[0], param.transition_mtx)
        self.noise = noise.Noise(param.seeds[0], param.ebn0[0])
        self.stat = Statistics(param.n_bits, param.tx_rate, param.conf)
        self.res = Results(param, figs_dir)
        self.theo = Theoretical(param)
        
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
        
        # PER loop
        for ebn0_idx in range(0, len(self.param.ebn0)):
            # Seed loop
            self.seed_loop()
            
            # Calculate mean and confidence
            ber_tpl, per_tpl, thrpt_tpl = self.stat.wrap_up()
            self.res.store_res(ber_tpl, per_tpl, thrpt_tpl)
            
            # Reset seed counter and set new BER
            self.reset_seed()
            self.new_ebn0()
            
        # Validate and plot
        ber_theo, per_theo, thrpt_theo = self.theo.validate()
        self.res.plot(ber_theo, per_theo, thrpt_theo)
        
    def send_pck(self):
        """
        Generates, sends and calculates error for one packet.
        
        Returns:
            n_errors -- number of bir errors in received packet
            pck_error -- boolean, True if packet has errors
        """
        pck_tx = self.station.generate_packet()
        pck_bpsk = 2*pck_tx-1 # FOR TESTING
        pck_channel = self.chann.propagate(pck_bpsk)
        pck_corrupted = self.noise.add_noise(pck_channel)
        pck_received = 1*(pck_corrupted.real > 0) # FOR TESTING
        n_errors, pck_error = self.station.calculate_error(pck_received)
        
        return n_errors, pck_error
    
    def pck_loop(self):
        """
        Loops throug all the necessary packet transmissions.
        """
        for pck in range(0, self.param.n_pcks):
            # Send packet
            n_errors, pck_error = self.send_pck()
            
            # Save results only if warm-up is over
            if pck > self.param.n_warm_up_pcks - 1:
                self.stat.pck_received(n_errors, pck_error)
                
    def seed_loop(self):
        """
        Loops through all the seeds.
        """
        if self.param.simulation_type is SimType.FIXED_SEEDS:
            while(self.get_seed_count() < len(self.param.seeds)):
                # Packet loop, send all packets
                self.pck_loop()    

                # After all packets have been sent calculate iteration results
                self.stat.calc_iteration_results()
                
                # Set new seed
                self.new_seed()
                
        elif self.param.simulation_type is SimType.FIXED_CONF:
            # Minimum confidence range between PER and Throughput
            conf_min = 1
            while(conf_min > self.param.conf_range):
                # Packet loop, send all packets
                self.pck_loop()

                # After all packets have been sent calculate iteration results
                self.stat.calc_iteration_results()

                # After all packets have been sent calculate iteration results
                # Condition necessary for confidence interval can not be
                # computed with only one sample
                if self.get_seed_count() > 0:
                    ber, ber_conf = \
                        self.stat.conf_interval(self.stat.get_ber_list())
                    per, per_conf = \
                        self.stat.conf_interval(self.stat.get_per_list())
                    thrpt, thrpt_conf = \
                        self.stat.conf_interval(self.stat.get_thrpt_list())
                    
                    # Redefine minimum confidence
                    conf_min = min([ber_conf/ber, per_conf/per, thrpt_conf/thrpt])
                
                # Set new seed
                self.new_seed()
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
            self.station.set_seed(self.get_seed_count())
            self.chann.set_seed(self.get_seed_count())
            
        else:
            raise NameError('Unknown simulation type!')
    
    def new_ebn0(self):
        """
        Resets the channel's BER.
        """
        self.__ebn0_count = self.__ebn0_count + 1
        if self.get_ebn0_count() < len(self.param.ebn0):
            self.noise.set_ebn0_db(self.param.ebn0[self.get_ebn0_count()])