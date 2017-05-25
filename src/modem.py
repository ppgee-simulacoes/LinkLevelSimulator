# -*- coding: utf-8 -*-
"""
Modem class, modulates and demodulates signal.

Main methods:
    modulate -- modulates input bits. Modulation order is defined in 
                construction.
    demodulate --  demodulates input signal, returning bits.

Created on Mon Apr 10 08:54:40 2017

@author: Calil and Eduardo
"""

from numpy import log2,sin,cos,pi,arange,array,sqrt,append,zeros,sum,argmin,hstack
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
        in_symbols: 1D complex array
        
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
        in_symbols: 1D complex array
            Symbol constellation mapping in bit counting order.
        """
        self.pad_len = 0
        if mod_order == 0 or ((mod_order & (mod_order - 1))) != 0:
            raise NameError("Modulation order not a power of two!")
        
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
    
    @property
    def scaling(self):
        return self.__scaling
    
    @property
    def in_symbols(self):
        return self.__in_symbols
    
    
    def modulate(self,in_bits):
        """
        Modulates input bits, creating correspondent symbols according to the
        modulation order.
        
        Code adapted from: https://github.com/veeresht/CommPy
        
        Parameters
        __________
        in_bits: 1D array of integers
            Bits to be modulated.
            
        Returns
        _______
        symbols: 1D array of complex numbers
            Symbols correspondent to modulated bits
        """
        padded = self.pad_bits(in_bits)
        mp = map(lambda i: self.bitarray2dec(padded[i:i+self.__bits_per_symbol]),\
                 range(0, len(padded), self.__bits_per_symbol))
        index_list = array(list(mp))
        baseband_symbols = self.constellation[index_list.astype(int)]
        
        if self.__norm:
            baseband_symbols = baseband_symbols/self.__scaling

        return baseband_symbols
    
    def demodulate(self,in_symbols):
        """
        Demodulates input symbols, by finding closes constelation element.
        
        Parameters
        __________
        in_symbols: 1D array of complex numbers
            Received symbol signal. May contain noise.
            
        Returns
        _______
        demod_bits: 1D array of integers
            Closest bit demodulation for received symbols.
            
        
        Code adapted from: https://github.com/veeresht/CommPy
        """
        if self.__norm:
            in_symbols = in_symbols*self.__scaling
        
        mp = map(lambda i: argmin(abs(in_symbols[i] - self.constellation)), \
                             range(0, len(in_symbols)))
        
        index_list = array(list(mp))
                           
        full_demod_bits = hstack(map(lambda i: self.dec2bitarray(i, self.__bits_per_symbol), \
                                index_list))
        
        demod_bits = self.unpad_bits(full_demod_bits)
        
        return demod_bits
    
    def set_modulation(self,mod_order,mod_type,constellation):
        """        
        Code adapted from: https://github.com/veeresht/CommPy
        """
        
        self.__mod_order = mod_order
        self.__bits_per_symbol = int(log2(self.__mod_order))
        self.__mod_type = mod_type
        
        self.__symbol_mapping = arange(self.__mod_order)
        
        if self.__mod_type == ModType.PSK:
            self.__constellation = array(list(map(self.__psk_symbol,\
                                                  self.__symbol_mapping)))
            
        elif self.__mod_type == ModType.QAM:
            mapping_array = arange(1, sqrt(self.__mod_order)+1) -\
            (sqrt(self.__mod_order)/2)
            
            self.__constellation = array(list(map(self.__qam_symbol,
                                 list(product(mapping_array, repeat=2)))))
            
        elif self.__mod_type == ModType.CUSTOM:
            if len(constellation) != self.__mod_order:
                raise NameError('Custom constellation error!')
            else:
                self.__constellation = constellation
                
        self.__scaling = sqrt(sum(abs(self.__constellation)**2)/\
                                   len(self.__constellation))
                
    def __psk_symbol(self,i):
        return cos(2*pi*(i-1)/self.__mod_order) +\
               sin(2*pi*(i-1)/self.__mod_order)*(0+1j)
    
    def __qam_symbol(self,i):
        return (2*i[0]-1) + (2*i[1]-1)*(1j)
    
    def bitarray2dec(self,in_bitarray):
        """
        Code adapted from: https://github.com/veeresht/CommPy
        """
        number = 0

        for i in range(len(in_bitarray)):
            number = number + in_bitarray[i]*pow(2, len(in_bitarray)-1-i)

        return number
    
    def dec2bitarray(self, in_number, bit_width):
        """
        Code adapted from: https://github.com/veeresht/CommPy
        """

        binary_string = bin(in_number)
        length = len(binary_string)
        bitarray = zeros(bit_width, 'int')
        for i in range(length-2):
            bitarray[bit_width-i-1] = int(binary_string[length-i-1])

        return bitarray
    
    def pad_bits(self,in_bits):
        remainder = len(in_bits) % self.__bits_per_symbol
        if remainder != 0:
            if self.__pad:
                self.pad_len = self.__bits_per_symbol - remainder
                return append(in_bits,zeros(self.pad_len))
            else:
                raise NameError('Bit array length error!')
        return in_bits
    
    def unpad_bits(self,in_bits):
        if self.pad_len != 0:
            bits = in_bits[: -self.pad_len]
            return bits
        else:
            return in_bits