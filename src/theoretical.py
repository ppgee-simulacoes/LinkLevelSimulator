# -*- coding: utf-8 -*-
"""
Theoretical results class.

Created on Sun Apr  2 11:16:43 2017

@author: Calil
"""

import numpy as np
from scipy import special
import scipy.sparse.linalg as sla
from support.enumerations import ChannelModel, BSCType, ModType


class Theoretical(object):
    def __init__(self, param):
        """
        Constructor method. Initializes atrributes:
            self.__model -- parameters object
            self.__p -- PER numpy array
            self.__state_ps -- stateebn probabilities for Markov channel
        
        Keyword parameters:
           model -- channel model
           p -- PER numpy array
        """
        self.__n_bits = param.n_bits
        self.__ebn0_db = param.ebn0
        self.__ebn0 = np.power(10, (self.__ebn0_db/10))
        self.__mod = param.mod_type
        self.__mod_order = param.mod_order
        self.__p = param.p
        self.__tx_rate = param.tx_rate
        self.__model = param.chan_mod
        if self.__model == ChannelModel.BSC:
            self.__bsc_type = param.bsc_type
            if self.__bsc_type == BSCType.MARKOV:
                self.__transition_matrix = param.transition_mtx
                self.__states_ber = [0, 0.5, self.get_p()]
                self.markov_solve(self.__transition_matrix)
        else:
            self.__state_ps = np.array([])

    def validate(self):
        """
        Calculates theoretical BER, PER and Throughput according to channel 
        model.
        
        Returns:
            ber_mean -- theoretical mean value of BER
            per_mean -- theoretical mean value of PER
            thrpt_mean -- theoretical mean value of Throughput
        """
        if self.__model is ChannelModel.IDEAL:
            return self.validate_awgn()
        elif self.__model is ChannelModel.BSC:
            if self.__bsc_type is BSCType.CONSTANT:
                return self.validate_constant()
            elif self.__bsc_type is BSCType.MARKOV:
                return self.validate_markov()
        else:
            raise NameError('Unknown channel model!')

    def get_model(self):
        """Getter for Parameters object."""
        return self.__model

    def get_ebn0(self):
        """Getter for Eb/N0 numpy array."""
        return self.__ebn0

    def get_p(self):
        """Getter for BER numpy array."""
        return self.__p

    def get_tx_rate(self):
        """Getter for tx_rate."""
        return self.__tx_rate

    def get_n_bits(self):
        """Getter for number of bits per packet."""
        return self.__n_bits

    def get_states_ber(self):
        """Getter for channel states BER."""
        return self.__states_ber

    def get_state_ps(self):
        """Getter for state probabilities."""
        return self.__state_ps

    def validate_awgn(self):
        """
        Calculates theoretical BER, PER and Throughput for AWGN channel.
        
        Returns:
            ber_mean -- theoretical mean value of BER
            per_mean -- theoretical mean value of PER
            thrpt_mean -- theoretical mean value of Throughput
        """
        q_func = lambda x: 0.5*special.erfc(x/np.sqrt(2))
        if(self.__mod == ModType.PSK):
            if(self.__mod_order == 2 or self.__mod_order == 2):
                ber_mean = 0.5*special.erfc(np.sqrt(self.get_ebn0()))
            else:
                ber_mean = (2/np.log2(self.__mod_order))*\
                    q_func(np.sqrt(2*self.get_ebn0()*np.log2(self.__mod_order))*\
                                np.sin(np.pi/self.__mod_order))
        elif(self.__mod == ModType.QAM):
            ber_mean = (4/np.log2(self.__mod_order))*\
                    q_func(np.sqrt((3*self.get_ebn0()*np.log2(self.__mod_order))/\
                                   (self.__mod_order - 1)))
        per_mean = 1 - np.power((1 - ber_mean), self.get_n_bits())
        thrpt_mean = self.get_tx_rate() * (1 - per_mean)
        return ber_mean, per_mean, thrpt_mean

    def validate_constant(self):
        """
        Calculates theoretical BER, PER and Throughput for constant channel.
        
        Returns:
            ber_mean -- theoretical mean value of BER
            per_mean -- theoretical mean value of PER
            thrpt_mean -- theoretical mean value of Throughput
        """
        ber_mean = self.get_p()
        per_mean = 1 - np.power((1 - ber_mean), self.get_n_bits())
        thrpt_mean = self.get_tx_rate() * (1 - per_mean)
        return ber_mean, per_mean, thrpt_mean

    def validate_markov(self):
        """
        Calculates theoretical BER, PER and Throughput for Markov channel.
        
        Returns:
            ber_mean -- theoretical mean value of BER
            per_mean -- theoretical mean value of PER
            thrpt_mean -- theoretical mean value of Throughput
        """
        # per_mean = 0 * p_good + 0.5 * p_bad + ber_ugly * p_ugly
        per_list = []
        for state, ber in enumerate(self.get_states_ber()):
            ber_mean = ber
            per_aux = 1 - np.power((1 - ber_mean), self.get_n_bits())
            per_list.append(per_aux * self.get_state_ps()[state])
        per_mean = np.sum(per_list)
        thrpt_mean = self.get_tx_rate() * (1 - per_mean)
        return ber_mean, per_mean, thrpt_mean

    def markov_solve(self, transition_matrix):
        """
        Solves the matrix equation to find Markov chain's steady state
        probabilities.
        
        Returns:
            state_ps -- numpy array of state probabilities
        """
        e_vals, e_vec = sla.eigs(transition_matrix.T, k=1, which='LM')
        self.__state_ps = (e_vec / e_vec.sum()).real
