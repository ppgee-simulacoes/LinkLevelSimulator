# -*- coding: utf-8 -*-
"""
Simulation thread class.

Created on Sun Apr  2 11:04:28 2017

@author: Calil
"""

from source import Source
from channel import Channel
from statistics import Statistics
from results import Results
from theoretical import Theoretical
from src.support.enumerations import SimType

class SimulationThread(object):
    def __init__(self,param,figs_dir):
        """
        Constructor method. Receives parameters and builds the simulation 
        objects.
        
        Keyword parameters:
            param -- parameters object
        """
        self.param = param
        self.station = Source(param.n_bits,param.seeds[0])
        self.chann = Channel(param.chan_mod,param.seeds[0],param.p[0])
        self.stat = Statistics(param.n_bits,param.tx_rate,param.conf)
        self.res = Results(param,figs_dir)
        self.theo = Theoretical(param)
        
        self.__seed_count = 0
        self.__ber_count = 0
        
    def get_seed_count(self):
        """Returns the seed count."""
        return self.__seed_count
        
    def get_ber_count(self):
        """Returns the BER count."""
        return self.__ber_count
    
    def simulate(self):
        """
        Performs simulation loop and generates results.
        """
        
        # PER loop
        for p_idx in range(0,len(self.param.p)):
            # Seed loop
            self.seed_loop()
            
            # Calculate mean and confidence
            per_tpl, thrpt_tpl = self.stat.wrap_up()
            self.res.store_res(per_tpl,thrpt_tpl)
            
            # Reset seed counter and set new BER
            self.reset_seed()
            self.new_ber()
            
        # Validate and plot
        ber_theo, per_theo, thrpt_theo = self.theo.validate()
        self.res.plot(per_theo, thrpt_theo)
        
    def send_pck(self):
        """
        Generates, sends and calculates error for one packet.
        
        Returns:
            n_errors -- number of bir errors in received packet
            pck_error -- boolean, True if packet has errors
        """
        pck_tx = self.station.generate_packet()
        pck_rx = self.chann.fade(pck_tx)
        n_errors, pck_error = self.station.calculate_error(pck_rx)
        
        return n_errors, pck_error
    
    def pck_loop(self):
        """
        Loops throug all the necessary packet transmissions.
        """
        for pck in range(0,self.param.n_pcks):
            # Send packet
            n_errors, pck_error = self.send_pck()
            
            # Save results only if warm-up is over
            if pck > self.param.n_warm_up_pcks - 1:
                self.stat.pck_received(pck_error)
                
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
                # compyted with only one sample
                if self.get_seed_count() > 0:
                    per, per_conf = \
                        self.stat.conf_interval(self.stat.get_per_list())
                    thrpt, thrpt_conf = \
                        self.stat.conf_interval(self.stat.get_thrpt_list())
                    
                    # Redefine minimum confidence
                    conf_min = min([per_conf/per , thrpt_conf/thrpt])
                
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
    
    def new_ber(self):
        """
        Resets the channel's BER.
        """
        self.__ber_count = self.__ber_count + 1
        if self.get_ber_count() < len(self.param.p):
            self.chann.set_p_val(self.param.p[self.get_ber_count()])