# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:40:31 2017

@author: Calil
"""

import unittest 
import numpy as np

from encoder import Encoder

class EncoderTest(unittest.TestCase):
    
    def setUp(self):     
        self.encoder = Encoder()
        
    def test_code(self):
        ## Size of message word
        k = 1
        # Mapping matrix: each line is a message word
        mapping = np.array([[0,0,0,0],[1,1,1,1]])
        
        # Bits to be coded
        bits = np.array([1,0,1,0])
        
        # Code
        encoded_bits = self.encoder.encode(bits,k,mapping)
        
        # Compare with expected result
        expected = np.array([1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0])
        self.assertEqual(len(encoded_bits),16)
        self.assertTrue(np.all(encoded_bits == expected))
        
        ## Size of message word
        k = 2
        # Mapping matrix: each line is a message word
        mapping = np.array([[0,0,0,0],[0,0,1,1],[1,1,0,0],[1,1,1,1]])
        
        # Bits to be coded: Test with padding
        bits = np.array([1,0,1])
        
        # Code
        encoded_bits = self.encoder.encode(bits,k,mapping)
        
        # Compare with expected result
        expected = np.array([1,1,0,0,1,1,0,0])
        self.assertEqual(len(encoded_bits),8)
        self.assertTrue(np.all(encoded_bits == expected))
        
        ## Size of message word
        k = 2
        # Mapping matrix: each line is a message word
        mapping = np.array([[0,0,0,0],[0,0,1,1],[1,1,0,0],[1,1,1,1]])
        
        # Bits to be coded: Test with padding
        bits = np.array([1,0,1])
        
        # Code
        with self.assertRaises(NameError):
            encoded_bits = self.encoder.encode(bits,k,mapping,pad=False)

    def test_decode(self):
        # signal to enter the decoder
        signal_in = np.array([1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0])
        # Mapping matrix: each line is a message word
        mapping_matrix = np.array([[0, 0, 0, 0], [1, 1, 1, 1]])

        decoded_bits = self.encoder.decode(signal_in, mapping_matrix)

        # comparison with expected bits
        expected_bits = np.array([1, 0, 1, 0])
        self.assertTrue(np.all(decoded_bits == expected_bits))

        
if __name__ == '__main__':
    unittest.main()
        