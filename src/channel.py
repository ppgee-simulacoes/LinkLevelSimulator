# -*- coding: utf-8 -*-
"""
Channel class, which implements three different channel models.

TODO Implement Markov channel

Created on Mon Mar 27 09:16:52 2017

@author: Calil
"""

import numpy as np

from src.support.enumerations import ChannelModel

class Channel(object):
    
    def __init__(self,model,seed,p_val):
        """
        Class constructor.
        
        Keyword arguments:
            model -- channel model (IDEAL, CONSTANT or MARKOV)
            seed -- seed for random number generator
            p_val -- BER for constant channel and state 2 of Markov channel
        """
        self.__model = model
        self.__seed = seed
        self.__p_val = p_val
        self.__rnd_state = np.random.RandomState(seed)
        
    def get_model(self):
        """Returns channel model."""
        return self.__model
    
    def set_seed(self,seed):
        """Set new seed."""
        self.__seed = seed
        self.__rnd_state.seed(seed)
    
    def get_seed(self):
        """Returns random number generator seed."""
        return self.__seed
    
    def set_p_val(self,p_val):
        """Set new value of p."""
        self.__p_val = p_val
        
    def get_p_val(self):
        """Returns current value of p."""
        return self.__p_val
    
    def fade(self,pck_Tx):
        """
        Applies fade to packet according to channel model, 
        introducing bit errors.
        
        Keyword arguments:
            pck_Tx -- transmitted packet
            
        Returns:
            pck_Rx -- received packet
        """
#        print("Channel Model: ",self.get_model())
        if self.get_model() is ChannelModel.IDEAL:
            return self.__fade_ideal(pck_Tx)
        elif self.get_model() is ChannelModel.CONSTANT:
            return self.__fade_constant(pck_Tx,self.get_p_val())
        elif self.get_model() is ChannelModel.MARKOV:
            return self.__fade_markov(pck_Tx)
        else:
            raise NameError('Unknown channel model!')
        
    def __fade_ideal(self,pck_Tx):
        """
        Ideal channel, just returns a copy of transmitted packet
        
        Keyword arguments:
            pck_Tx -- transmitted packet
            
        Returns:
            pck_Rx -- received packet, a copy of pck_Tx
        """
        pck_Rx = np.array(pck_Tx,copy = True)
        return pck_Rx
    
    def __fade_constant(self,pck_Tx,exp_ber):
        """
        Constant channel, with a constant BER.
        
        Keyword arguments:
            pck_Tx -- transmitted packet
            exp_ber -- expected bit error rate
            
        Returns:
            pck_Rx -- received packet
        """
        err = 1.0*(self.__rnd_state.rand(len(pck_Tx)) < exp_ber)
        pck_Rx = abs(pck_Tx - err)
        return pck_Rx
    
    def __fade_markov(self,pck_Tx):
        """
        Markov chain modeled channel, BER changes for each packet.
        
        Keyword arguments:
            pck_Tx -- transmitted packet
            
        Returns:
            pck_Rx -- received packet
        """
        raise NotImplementedError