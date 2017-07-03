import numpy as np

from channel.channel import Channel


class Fading(Channel):

    def __init__(self, doppler_freq, m, k, time):
        self.__doppler_freq = doppler_freq
        self.__m = m
        self.__k = k
        self.__time = time
        self.__fading = 1

    def update_channel(self):
        pass

    def propagate(self, pkt_tx):
        t = np.linspace(0, self.__time, num=1001)
        rayleigh = list(range(self.__m))
        for n in range(0, self.__m):
            beta_n = np.pi*n/(self.__m+1)
            tetha_nk = beta_n + 2*np.pi*(self.__k-1)/(self.__m+1)
            alpha = 0
            rayleigh[n] = 2*np.sqrt(2)*((np.cos(beta_n)+np.sin(beta_n)*1j)*np.cos(2*np.pi*self.__doppler_freq*t+tetha_nk)+(1/np.sqrt(2))*(np.cos(alpha)+np.sin(alpha)*1j)*np.cos(2*np.pi*self.__doppler_freq*t))

        self.__fading = np.sum(rayleigh)
        pkt_rx = self.__fading*pkt_tx
        
        return pkt_rx

    def get_fading(self):
        return self.__fading
