# -*- coding: utf-8 -*-
"""
Modem class, modulates and demodulates signal.

Code adapted from: https://github.com/veeresht/CommPy

Main methods:
    modulate -- modulates input bits. Modulation order is defined in 
                construction.
    demodulate --  demodulates input signal, returning bits.

Created on Mon Apr 10 08:54:40 2017

@author: Calil
"""

from numpy import log2,sin,cos,pi,arange,array,sqrt
from itertools import product

from support.enumerations import ModType

class Modem(object):
    
    def __init__(self,mod_order,mod_type,norm=False,pad=True,constellation = []):
        """
        Constructor method. Initializes attributes:
            
        mod_order: integer.
            Modulation order. Must be a power of two.
        mod_type: ModType
            Type of modulation (PSK, QAM, CUSTOM)
        norm: bool
            Boolean to indicate normalization usage.
        pad: bool
            Bootlan to indicate padding usage.
        constellation: 1D complex array
            Custom symbol constellation mapping in bit counting order.
        
        Parameters
        __________
        mod_order: integer
            Modulation order.
        norm: bool
            Boolean to indicate normalization usage
        pad: bool
            Boolean to indicate padding usage
        constellation: 1D complex array
            Symbol constellation mapping in bit counting order.
        """
        self.set_modulation(mod_order,mod_type,constellation)
        
        self.__norm = norm
        self.__pad = pad
    
    @property
    def mod_order(self):
        return self.__mod_order
    
    @property
    def bits_per_symbol(self):
        return self.__bits_per_symbol
    
    @property
    def mod_type(self):
        return self.__mod_type
    
    @property
    def norm(self):
        return self.__norm
    
    @property
    def pad(self):
        return self.__pad
    
    @property
    def constellation(self):
        return self.__constellation
    
    def set_modulation(self,mod_order,mod_type,constellation):
        
        self.__mod_order = mod_order
        self.__bits_per_symbol = int(log2(self.__mod_order))
        self.__mod_type = mod_type
        
        self.__symbol_mapping = arange(self.__mod_order)
        
        if self.__mod_type == ModType.PSK:
            self.__constellation = array(list(map(self.psk_symbol,\
                                                  self.__symbol_mapping)))
            
        elif self.__mod_type == ModType.QAM:
            mapping_array = arange(1, sqrt(self.__mod_order)+1) -\
            (sqrt(self.__mod_order)/2)
            
            self.__constellation = array(list(map(self.qam_symbol,
                                 list(product(mapping_array, repeat=2)))))
            
        elif self.__mod_type == ModType.CUSTOM:
            if len(constellation) != self.__mod_order:
                raise NameError('Custom constellation error!')
            else:
                self.__constellation = constellation
                
    def psk_symbol(self,i):
        return cos(2*pi*(i-1)/self.__mod_order) +\
               sin(2*pi*(i-1)/self.__mod_order)*(0+1j)
    
    def qam_symbol(self,i):
        return (2*i[0]-1) + (2*i[1]-1)*(1j)
            
    def map_bits(self,in_bits):
        """
        Maps bits to symbols according to modulation scheme.
        
        Parameters
        __________
        in_bits: 1D array of integers
            Bits to be mapped.
            
        Returns
        _______
        symbols: 1D array of complex numbers
            Symbols correspondent to mapped bits
        """
        pass
    
    def demap_bits(self,in_symbols):
        """
        Maps symbols to bits according to modulation scheme.
        
        Parameters
        __________
        in_symbols: 1D array of complex numbers
            Symbols correspondent to mapped bits
            
        Returns
        _______
        bits: 1D array of integers
            Demapped bits.
        """
        pass
    
    def modulate(self,in_bits):
        """
        Modulates input bits, creating correspondent symbols according to the
        modulation order.
        
        Parameters
        __________
        in_bits: 1D array of integers
            Bits to be modulated.
            
        Returns
        _______
        symbols: 1D array of complex numbers
            Symbols correspondent to modulated bits
        """
        pass
    
    def demodulate(self,in_symbols):
        """
        Demodulates imput symbols, by finding closes constelation element.
        
        Parameters
        __________
        in_symbols: 1D array of complex numbers
            Received symbol signal. May contain noise.
            
        Returns
        _______
        bits: 1D array of integers
            Closest bit demodulation for received symbols.
        """
        pass