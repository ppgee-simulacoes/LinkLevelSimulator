# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:40:31 2017

@author: Calil
"""

import unittest 
import numpy as np

from coder import Coder

class CoderTest(unittest.TestCase):
    
    def setUp(self):     
        self.coder = Coder()
        
    def test_code(self):
        ## Size of message word
        k = 1
        # Mapping matrix: each line is a message word
        mapping = np.array([[0,0,0,0],[1,1,1,1]])
        
        # Bits to be coded
        bits = np.array([1,0,1,0])
        
        # Code
        coded_bits = self.coder.code(bits,k,mapping)
        
        # Compare with expected result
        expected = np.array([1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0])
        self.assertEqual(len(coded_bits),16)
        self.assertTrue(np.all(coded_bits == expected))
        
        ## Size of message word
        k = 2
        # Mapping matrix: each line is a message word
        mapping = np.array([[0,0,0,0],[0,0,1,1],[1,1,0,0],[1,1,1,1]])
        
        # Bits to be coded: Test with padding
        bits = np.array([1,0,1])
        
        # Code
        coded_bits = self.coder.code(bits,k,mapping)
        
        # Compare with expected result
        expected = np.array([1,1,0,0,1,1,0,0])
        self.assertEqual(len(coded_bits),8)
        self.assertTrue(np.all(coded_bits == expected))
        
        ## Size of message word
        k = 2
        # Mapping matrix: each line is a message word
        mapping = np.array([[0,0,0,0],[0,0,1,1],[1,1,0,0],[1,1,1,1]])
        
        # Bits to be coded: Test with padding
        bits = np.array([1,0,1])
        
        # Code
        with self.assertRaises(NameError):
            coded_bits = self.coder.code(bits,k,mapping,pad=False)
        
if __name__ == '__main__':
    unittest.main()
        