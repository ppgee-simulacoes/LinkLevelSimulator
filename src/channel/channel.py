from abc import ABC, abstractmethod
import numpy as np


class Channel(ABC):
    def __init__(self, seed):
        self.__seed = seed
        self.__rnd_state = np.random.RandomState(seed)

    @abstractmethod
    def update_channel(self):
        pass

    @abstractmethod
    def propagate(self):
        pass
