import numpy as np

from channel.channel import Channel


class IdealChannel(Channel):

    def __init__(self, seed, p_val):
        self.__seed = seed
        self.__rnd_state = np.random.RandomState(seed)
        self.__p_val = p_val


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

    def update_channel(self):
        pass

    def propagate(self, pkt_tx):
        pkt_rx = np.array(pkt_tx, copy=True)
        return pkt_rx
