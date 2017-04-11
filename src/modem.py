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

class Modem(object):
    
    def __init__(self,mod_order):
        """
        Constructor method. Initializes attributes:
            
        mod_order: integer. Must be an even power of two (2**(2*k))
            QAM modulation order. Prvide 4 for QPSK.
                         
        Parameters
        __________
        mod_order: integer. Must be an even power of two (2**(2*k))
            QAM modulation order. Prvide 4 for QPSK.
        """
        pass
    
    def get_modulation_order(self):
        """
        Getter for modulation order.
        
        Returns
        _______
        mod_order: integer
            QAM modulation order. 4 means QPSK.
        """
        pass
    
    def set_modulation_order(self,mod_order):
        """
        Setter for modulation order.
        
        Parameters
        __________
        mod_order: integer
            New QAM modulation order. 4 means QPSK.
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