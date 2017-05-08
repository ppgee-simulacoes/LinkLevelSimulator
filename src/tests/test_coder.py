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
        k = 1
        mapping = np.array([[0,0,0,0],[1,1,1,1]])
        
        bits = np.array([1,0,1,0])
        
        coded_bits = self.coder.code(bits,k,mapping)
        
        expected = np.array([1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0])
        self.assertEqual(len(coded_bits),16)
        self.assertTrue(np.all(coded_bits == expected))
        
if __name__ == '__main__':
    unittest.main()
        