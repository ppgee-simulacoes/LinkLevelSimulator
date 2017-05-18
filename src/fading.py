#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 19:06:50 2017

@author: eduardo
"""

import numpy as np

class Fading(object):
    
    def __init__(self,doppler_frequency,m,in_signal = []):
        """
        Constructor method. Initializes attributes:
            
        doppler_frequency: integer.
            Doppler frequency. Corresponds to velocity + carrier frequency
        m: integer
            Number of scatterers.
        in_signal: 1D complex array
            Modulated signal.
        
        Parameters
        __________
        doppler_frequency: integer.
            Doppler frequency. Corresponds to velocity + carrier frequency
        m: integer
            Number of scatterers.
        in_signal: 1D complex array
            Modulated signal.
        """
            
    @property
    def doppler_frequency(self):
        return self.__doppler_frequency
    
    @property
    def m(self):
        return self.__m
    
    @property
    def in_signal(self):
        return self.__in_signal
    
    def add_fading(self,doppler_frequency,m,signal = []):
        """
        Add Rayleigh fading using Jake's model.
        
        Parameters
        __________
        doppler_frequency: float.
            Doppler frequency. Corresponds to velocity + carrier frequency
        m: integer
            Number of scatterers.
        in_signal: 1D complex array
            Modulated signal without AWGN.
        k = waveform over time
        alpha = Jake's model parameters. Usually equals 0.
        t = time variable
        
        Return
        ______
        out_signal = Signal after to apply Rayleigh fading.
        """
        in_signal = self.__constellation
        k = 2
        fm = self.__dopper_frequency
        alpha = 0
        t = np.linspace(0, (1/fm), num = 50)
        
        for n in range (0,m):
            beta_n = np.pi*n/(m+1)
            tetha_nk = beta_n + 2*np.pi*(k-1)/(m+1)
            rayleigh[n] = 2*np.sqrt(2)*(np.cos(beta_n)+(np.sin(beta_n))j)*np.cos(2*np.pi*fm*t+tetha_nk)+(1/np.sqrt(2))*(np.cos(alpha)+(np.sin(alpha))j)*np.cos(2*np.pi*fm*t)
        
        fading = np.sum(rayleigh)
        out_signal = fading*in_signal
        
        return out_signal
        
    def compensate_fading(self,fading ,signal = []):
        """
        Compensate fading
        
        Parameters
        __________
        fading: 1D complex array
            Rayleigh fading. Jake's model.
        
        signal: 1D complex array
            Signal after fading and AWGN.
        
        Return
        ______
        compensate_signal = Signal after to compensate Rayleigh fading.
        """
         
        compensate_signal = in_signal/fading
        
        return compensate_signal