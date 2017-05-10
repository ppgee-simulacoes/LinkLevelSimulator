import numpy as np


class Noise(object):

    def __init__(self, seed, ebn0_db, mod_order):
        self.__seed = seed
        self.__rnd_state = np.random.RandomState(seed)
        self.__ebn0_db = ebn0_db
        self.__ebn0 = np.power(10, (self.__ebn0_db/10))
        self.__bits_per_symbol = int(np.log2(mod_order))
        self.__bit_energy = None
        self.__variance = None

    def get_ebn0_db(self):
        return self.__ebn0_db

    def set_ebn0_db(self, ebn0_db):
        self.__ebn0_db = ebn0_db
        self.__ebn0 = np.power(10, (self.__ebn0_db/10))

    def get_ebn0(self):
        return self.__ebn0

    def get_bit_energy(self):
        return self.__bit_energy

    def set_bit_energy(self, bit_energy):
        self.__bit_energy = bit_energy

    def get_bits_per_symbol(self):
        return self.__bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.__bits_per_symbol = bits_per_symbol

    def get_variance(self):
        return self.__variance

    def set_variance(self, variance):
        self.__variance = variance

    def add_noise(self, in_signal):

        # Calculate Variance
        if not self.get_bit_energy():
            energy = np.real(in_signal) ** 2 + np.imag(in_signal) ** 2
            self.set_bit_energy((np.sum(energy)/len(in_signal))/self.get_bits_per_symbol())
        self.set_variance(self.get_bit_energy() / self.get_ebn0())

        # Calculate Noise
        noise = self.__rnd_state.randn(1, in_signal.size) + 1j * self.__rnd_state.randn(1, in_signal.size)
        noise *= np.sqrt(self.get_variance()/2)

        # Add noise
        corrupted_signal = in_signal + noise
        return corrupted_signal

