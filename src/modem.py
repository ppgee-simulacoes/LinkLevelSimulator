# -*- coding: utf-8 -*-
"""
Modem class, modulates and demodulates signal.
Main methods:
    modulate -- modulates input bits. Modulation order is defined in 
                construction.
    demodulate --  demodulates input signal, returning bits.

Created on Mon Apr 10 08:54:40 2017

@author: Calil
"""

from commpy.modulation import QAMModem, PSKModem
import numpy as np

class Modem(object):
    
    def __init__(self,mod_order,norm,pad,constelation = 0):
        """
        Constructor method. Initializes attributes:
            
        mod_order: integer. Must be an even power of two (2**(2*k))
            QAM modulation order. Prvide 4 for QPSK.
                         
        Parameters
        __________
        mod_order: integer
            Modulation order:
                2       PBSK
                4       QPSK
                8       8-PSK
                16      16-QAM
                64      64-QAM
                256     256-QAM    
        norm: bool
            Boolean to indicate normalization usage
        pad: bool
            Boolean to indicate padding usage
        constelation: 1D complex array
            Symbol constelation mapping in bit counting order.
        """
        # Raise exception if provided value is not a power of 2
        if np.log2(mod_order) != round(np.log2(mod_order)):
            raise NameError('Modulation order not a power of 2!')
            
        # For modulation order lower than 16, use PSK. Otherwise, use QAM
        if mod_order < 16:
            self.__commpy_mod = PSKModem(mod_order)
        else:
            self.__commpy_mod = QAMModem(mod_order)
            
        self.__norm = norm
        self.__pad = pad
        self.__constelation = constelation
    
    def get_mod_order(self):
        """
        Getter for modulation order.
        
        Returns
        _______
        mod_order: integer
            QAM modulation order. 4 means QPSK.
        """
        return self.__commpy_mod.m
    
    def get_normalize(self):
        """
        Getter for normalization boolean
        
        Returns
        _______
        norm: bool
            True if normalization is performed. False otherwise.
        """
        return self.__norm
    
    def get_padding(self):
        """
        Getter for padding boolean
        
        Returns
        _______
        pad: bool
            True if padding is performed. False otherwise.
        """
        return self.__pad
    
    def get_constelation(self):
        """
        Getter for constelation mapping
        
        Returns
        _______
        constelation: complex 1D array
            Constelation in bit counting order.
        """
        return self.__constelation
    
    def set_mod_order(self,mod_order):
        """
        Setter for modulation order.
        
        Parameters
        __________
        mod_order: integer
            New QAM modulation order. 4 means QPSK.
        """
        # For modulation order lower than 16, use PSK. Otherwise, use QAM
        if mod_order < 16:
            self.__commpy_mod = PSKModem(mod_order)
        else:
            self.__commpy_mod = QAMModem(mod_order)
            
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