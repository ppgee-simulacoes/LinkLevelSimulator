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


    def __init__(self,model,seed,p_val,transition_matrix):
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
        self.__transition_matrix = transition_matrix
        self.__previous_state = 0
        self.__current_state = None
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

    def get_transition_matrix(self):
        """Returns the channel transition matrix."""
        return self.__transition_matrix

    def get_previous_state(self):
        """Returns the channels previous state."""
        return self.__previous_state

    def set_previous_state(self, state):
        """Set a new value for the channel previous state."""
        self.__previous_state = state

    def get_current_state(self):
        """Returns the channels current state."""
        return self.__current_state

    def update_channel(self, previous_state):
        """Create the Markov Chain state according to the transition probabilities"""
        # Get the line of the matrix for the previous state and return the CDF
        state_distribution = self.get_transition_matrix()[previous_state, :]
        cumulative_distribution = np.cumsum(state_distribution)

        # Get sorted number between 0 and 1 and check it for the range of the CDF
        sorting_index = self.__rnd_state.rand()
        possible_indexes = np.where(cumulative_distribution > sorting_index)
        self.__current_state = np.min(possible_indexes[1])

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
            return self.__fade_markov(pck_Tx, self.get_previous_state())
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

    def __fade_markov(self, pck_Tx, state):
        """
        Markov chain modeled channel, BER changes for each packet.

        Keyword arguments:
            pck_Tx -- transmitted packet

        Returns:
            pck_Rx -- received packet
        """

        # State 0 => GOOD / BER = 0
        # State 1 => BAD / BER = 0.5
        # State 2 => UGLY / BER = p_val
        if state == 0:
            # If channel state equals 0, there are no errors in the packet
            ber = 0
        elif state == 1:
            # If channel state equals 1, there is a 0.5 probability of a bit error
            ber = 0.5
        elif state == 2:
            # If channel state equals 2, there is a ber_ugly probability of a bit error
            ber = self.get_p_val()

        error_probability = self.__rnd_state.rand(1, pck_Tx.size) < ber
        pck_Rx = pck_Tx ^ error_probability

        # Calls the method to update the channel state
        self.update_channel(state)
        self.set_previous_state(self.get_current_state())

        return pck_Rx
