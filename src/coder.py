# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:10:20 2017

@author: Calil
"""

import numpy as np
import itertools

class Coder(object):
    
    def code(self,in_bits,k,maping,pad=True):
        """
        Code input bits according to maping matrix.
        
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

    def decode(self, in_signal, generator_matrix):

        # get message word size (k), codeword size (n), number of codewords (M)
        message_size = generator_matrix.shape[0]
        codeword_size = generator_matrix.shape[1]
        num_words = int(in_signal.size/codeword_size)

        # get all possible message words from mapping matrix
        message_alphabet, codeword_alphabet = self.get_alphabet(generator_matrix)

        # reshape in_signal (M codewords of n size)
        # Change for soft decision decoding
        signal_reshaped = np.reshape(in_signal, [num_words, codeword_size])

        message = np.empty([num_words, message_size], dtype=int)
        # LOOP: Compare each sequence to all possible codewords
        for cod_idx, codeword in enumerate(signal_reshaped):
            # Calculate distance(d)(hamming / euclidian)
            distances = self.calculate_hamming_distance(codeword, codeword_alphabet)
            # Choose message with min(d)
            msg_idx = np.where(distances == np.min(distances))
            message[cod_idx] = message_alphabet[msg_idx]

        # Reshape out_signal (M messages of k bits)
        message_bits = np.reshape(message, [1, message_size * num_words])

        return message_bits

    def get_alphabet(self, generator_matrix):
        # Get all corresponding codeword for each possible message for a given generator matrix

        # Get all possible permutation of bits of determined size
        message_size = generator_matrix.shape[0]
        messages = [message for message in itertools.product([0, 1], repeat=message_size)]
        message_alphabet = np.asarray(messages)

        codeword_alphabet = message_alphabet.dot(generator_matrix) % 2

        return message_alphabet, codeword_alphabet

    def bitarray2dec(self,in_bitarray):
        """
        Code adapted from: https://github.com/veeresht/CommPy
        """
        number = 0

        for i in range(len(in_bitarray)):
            number = number + in_bitarray[i]*pow(2, len(in_bitarray)-1-i)

        return number

    def calculate_hamming_distance(self, array1, array2):
        # Calculate the Hamming Distance between two arrays of bits
        hamming_distance = np.bitwise_xor(array1, array2).sum(1)

        return hamming_distance

    def calculate_euclidean_distance(self, array1, array2):
        # Calculate the Euclidean Distance between two arrays of floats
        euclidean_distance = ((array1 - array2)**2).sum()

        return euclidean_distance
