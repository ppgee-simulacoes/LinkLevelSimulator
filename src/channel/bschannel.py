import numpy as np

from channel import Channel
from src.support.enumerations import BSCType


class BSChannel(Channel):
    def __init__(self, model, seed, p_val, transition_matrix):
        # NEXT VERSION: super().__init__(seed) try to solve issue
        self.__seed = seed
        self.__rnd_state = np.random.RandomState(seed)
        self.__model = model
        self.__p_val = p_val
        self.__transition_matrix = transition_matrix
        self.__previous_state = 0
        self.__current_state = None

    def get_model(self):
        """Returns channel model."""
        return self.__model

    def set_seed(self, seed):
        """Set new seed."""
        self.__seed = seed
        self.__rnd_state.seed(seed)

    def get_seed(self):
        """Returns random number generator seed."""
        return self.__seed

    def set_p_val(self, p_val):
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

    def propagate(self, pkt_tx):
        """
        Applies fade to packet according to channel model, 
        introducing bit errors.

        Keyword arguments:
            pck_Tx -- transmitted packet

        Returns:
            pck_Rx -- received packet
        """

        if self.get_model() is BSCType.CONSTANT:
            return self.__propagate_constant(pkt_tx, self.get_p_val())
        elif self.get_model() is BSCType.MARKOV:
            return self.__propagate_markov(pkt_tx, self.get_previous_state())
        else:
            raise NameError('Unknown Binary Symmetric Channel Type!')

    def __propagate_constant(self, pkt_tx, exp_ber):
        """
        Constant channel, with a constant BER.

        Keyword arguments:
            pck_Tx -- transmitted packet
            exp_ber -- expected bit error rate

        Returns:
            pck_Rx -- received packet
        """
        error_probability = self.__rnd_state.rand(1, pkt_tx.size) < exp_ber
        pkt_rx = pkt_tx ^ error_probability
        return pkt_rx

    def __propagate_markov(self, pkt_tx, state):
        """
        Markov chain modeled channel, BER changes for each packet.

        Keyword arguments:
            pkt_tx -- transmitted packet

        Returns:
            pkt_rx -- received packet
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

        error_probability = self.__rnd_state.rand(1, pkt_tx.size) < ber
        pkt_rx = pkt_tx ^ error_probability

        # Calls the method to update the channel state
        self.update_channel(state)
        self.set_previous_state(self.get_current_state())

        return pkt_rx
