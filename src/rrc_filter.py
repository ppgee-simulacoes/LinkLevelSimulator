# -*- coding: utf-8 -*-
"""
Root raised cosine filter, with upsampling and downsampling.

Main methods:
    tx_filter: upsamples and filters input symbols
    rx_filter: filters and downsamples input signal

Created on Tue Apr 25 20:06:30 2017

@author: Calil
"""

import numpy as np

class RRCFilter(object):
    def __init__(self,N,alpha,Ts,Fs,up_factor):
        """
        Constructor method. Initializes attributes:
            
        N: int
            Filter length
        alpha: float
            Roll off factor (Valid values are [0, 1])
        Ts: float
            Symbol time
        Fs: float
            Sampling rate in Hz
        up_factor: int
            Upsampling factor
        
        Parameters
        __________
        
        N: int
            Filter length
        alpha: float
            Roll off factor (Valid values are [0, 1])
        Ts: float
            Symbol time
        Fs: float
            Sampling rate in Hz
        up_factor: int
            Upsampling factor
        """
        self.__N = N
        self.__alpha = alpha
        self.__Ts = Ts
        self.__Fs = Fs
        self.__up_factor = up_factor
        
        self.__response = self.filter_response(N,alpha,Ts,Fs)
    
    def tx_filter(self,symbols):
        """
        Upsamples and filters input symbols.

        Parameters
        ----------
        symbols: 1D complex array
            Input symbols

        Returns
        ---------
        signal: 1D complex array
            Output signal
        """
        pass
    
    def rx_filter(self,signal):
        """
        Filters and downsamples signal.

        Parameters
        ----------
        signal: 1D complex array
            Input signal
        
        Returns
        ---------
        symbols: 1D complex array
            Output symbols
        """
        pass
    
    @property
    def N(self):
        return self.__N
    
    @property
    def alpha(self):
        return self.__alpha
    
    @property
    def Ts(self):
        return self.__Ts
    
    @property
    def Fs(self):
        return self.__Fs
    
    @property
    def up_factor(self):
        return self.__up_factor
    
    @property
    def response(self):
        return self.__response
    
    def upsample(self,x):
        """
        Upsample the input array by a factor of n
    
        Adds n-1 zeros between consecutive samples of x
        
        Code adapted from: https://github.com/veeresht/CommPy
    
        Parameters
        ----------
        x : 1D ndarray
            Input array.
    
        Returns
        -------
        y : 1D ndarray
            Output upsampled array.
        """
        y = np.empty(len(x)*self.__up_factor, dtype=complex)
        y[0::self.__up_factor] = x
        zero_array = np.zeros(len(x), dtype=complex)
        for i in range(1, self.__up_factor):
            y[i::self.__up_factor] = zero_array
    
        return y
    
    def apply_filter(self,sig):
        pass
    
    def downsample(self,sig):
        pass
    
    def filter_response(self,N,alpha,Ts,Fs):
        pass
    
    