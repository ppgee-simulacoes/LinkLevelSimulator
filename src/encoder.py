# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:10:20 2017

@author: Calil
"""

import numpy as np

class Encoder(object):
    
    def encode(self,in_bits,k,maping,pad=True):
        """
        Encode input bits according to maping matrix.
        
        Code adapted from: https://github.com/veeresht/CommPy
        
        Parameters
        __________
        in_bits: 1D array of integers
            Bits to be coded.
        k: int
            Length of message word.
        maping: 2D array of integers
            Mapping matrix, each row corresponding to a possible message word.
        pad : bool
            Padding flag
            
        Returns
        _______
        maped_ar: 1D array
            Coded bits.
        """
        
        # Define remainder
        rem = len(in_bits) % k
        
        # Pad, if necessary
        if pad:
            bits_pad = np.append(in_bits,np.zeros(rem))
        else:
            bits_pad = in_bits
            if rem != 0: raise NameError("Padding not used!")
        
        # Define number of words
        word_num = int(len(bits_pad)/k)
        # Reshape to column vector
        bits_re = np.reshape(bits_pad,[word_num,k])
        
        # Convert to decimal
        dec_re = np.array([self.bitarray2dec(bits_re[j,:]) \
                                            for j in range(word_num)])
        # Map, rehsape to row vector and ravel
        maped = maping[dec_re.astype(int),:]
        maped_re = np.reshape(maped,[1,np.size(maped)])
        maped_ra = maped_re.ravel()
        
        return maped_ra
    
        
    def bitarray2dec(self,in_bitarray):
        """
        Code adapted from: https://github.com/veeresht/CommPy
        """
        number = 0

        for i in range(len(in_bitarray)):
            number = number + in_bitarray[i]*pow(2, len(in_bitarray)-1-i)

        return number