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
import scipy.signal as sg

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
        
        h, t = self.filter_response(N,alpha,Ts,Fs)
        self.__response = h
        self.__time = t
    
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
        up_symbols = self.upsample(symbols)
        signal = self.apply_filter(self.response,up_symbols)
        return signal
    
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
    
    @property
    def time(self):
        return self.__time
    
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
    
    def apply_filter(self,resp,sig):
        delay_samp = int(0.5*(len(resp)))
        pad_sig = np.append(sig,np.zeros(delay_samp))
        y = sg.lfilter(resp,1.0,pad_sig)
        return y[delay_samp:]
    
    def downsample(self,sig):
        pass
    
    def filter_response(self,N,alpha,Ts,Fs):
        """
        Generates a root raised cosine (RRC) filter (FIR) impulse response.
        
        Code adapted from: https://github.com/veeresht/CommPy
    
        Parameters
        ----------
        N : int
            Length of the filter in samples.
    
        alpha : float
            Roll off factor (Valid values are [0, 1]).
    
        Ts : float
            Symbol period in seconds.
    
        Fs : float
            Sampling Rate in Hz.
    
        Returns
        ---------
    
        h_rrc : 1-D ndarray of floats
            Impulse response of the root raised cosine filter.
    
        time_idx : 1-D ndarray of floats
            Array containing the time indices, in seconds, for
            the impulse response.
        """
    
        T_delta = 1/float(Fs)
        time_idx = ((np.arange(N)-N/2))*T_delta
        sample_num = np.arange(N)
        h_rrc = np.zeros(N, dtype=float)
    
        for x in sample_num:
            t = (x-N/2)*T_delta
            if t == 0.0:
                h_rrc[x] = 1.0 - alpha + (4*alpha/np.pi)
            elif alpha != 0 and t == Ts/(4*alpha):
                h_rrc[x] = (alpha/np.sqrt(2))*(((1+2/np.pi)* \
                        (np.sin(np.pi/(4*alpha)))) + ((1-2/np.pi)*(np.cos(np.pi/(4*alpha)))))
            elif alpha != 0 and t == -Ts/(4*alpha):
                h_rrc[x] = (alpha/np.sqrt(2))*(((1+2/np.pi)* \
                        (np.sin(np.pi/(4*alpha)))) + ((1-2/np.pi)*(np.cos(np.pi/(4*alpha)))))
            else:
                h_rrc[x] = (np.sin(np.pi*t*(1-alpha)/Ts) +  \
                        4*alpha*(t/Ts)*np.cos(np.pi*t*(1+alpha)/Ts))/ \
                        (np.pi*t*(1-(4*alpha*t/Ts)*(4*alpha*t/Ts))/Ts)
    
        # Normalize filter
        power = np.sum(abs(h_rrc)**2)
        h_rrc = h_rrc/np.sqrt(power)
        
        return h_rrc, time_idx
    
    