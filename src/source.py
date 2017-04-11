# -*- coding: utf-8 -*-
"""
Source class: crates packets and checks for bit and packet errors.

Created on Sun Mar 26 10:00:08 2017

@author: Calil
"""

import numpy as np

class Source(object):
    def __init__(self,n_bits,seed):
        """
        Class constructor.
        
        Keyword arguments:
            n_bits -- number of bits per packet
            seed -- seed for random number generator
        """
        self.__n_bits = n_bits
        self.__seed = seed
        self.__last_pck = np.zeros([1,n_bits]) # last transmitted packet
        self.__rnd_state = np.random.RandomState(seed)
    
    def get_n_bits(self):
        """Returns the number of bits per packet."""
        return self.__n_bits
    
    def get_seed(self):
        """Returnt the random number generator seed."""
        return self.__seed
    
    def set_seed(self,seed):
        """Set new seed."""
        self.__seed = seed
        self.__rnd_state.seed(seed)
    
    def get_last_pck(self):
        """Returns a reference to the last transmitted packet."""
        return self.__last_pck
    
    def get_rnd_state(self):
        """Returns the random state object."""
        return self.__rnd_state
    
    def generate_packet(self):
        """
        Returns a new, random generated, 0s and 1s packet.
        Also updates the last transmitted packet to new one.
        
        Returns:
            pck -- generated packet
        """
        pck = self.get_rnd_state().randint(2,\
                                            size=self.get_n_bits())
        # Last packet is a copy of sent packet, for further comparison
        self.__last_pck = np.array(pck,copy = True)

        return pck
    
    def calculate_error(self,pck):
        """
        Calculates bit and packet error.
        
        Keyword arguments:
            pck --  received packet, to be compared with last packet
            
        Returns:
            n_errors -- number of bit errors in received packet
            pck_error -- boolean, true if packet contains errors
        """
        n_errors = np.sum(pck != self.get_last_pck())
        pck_error = (n_errors != 0)
        
        return n_errors, pck_error