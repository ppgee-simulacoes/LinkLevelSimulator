# -*- coding: utf-8 -*-
"""
Unit tests for Source class

Created on Sun Mar 26 08:14:37 2017

@author: Calil
"""

import unittest
import numpy as np

from src.source import Source

class SourceTest(unittest.TestCase):
    
    def setUp(self):
        n_bits = 1000
        seed = 10
        
        # Generate Source object
        self.source = Source(n_bits,seed)
        
        # Genetare packets
        self.pck = self.source.generate_packet()
        
    def test_n_bits(self):
        self.assertEqual(1000,self.source.get_n_bits())
        
    def test_seed(self):
        self.assertEqual(10,self.source.get_seed())
        
    def test_last_packet(self):
        self.assertTrue(np.all(self.pck == self.source.get_last_pck()))
        
    def test_calculate_error(self):
        # Calculate packet errors
        n_errors, pck_error = self.source.calculate_error(self.pck)
        
        # Assert if no errors were found
        self.assertEqual(0,n_errors)
        self.assertFalse(pck_error)
        
        # Intentionally insert bit error
        pck2 = np.array(self.pck,copy = True)
        pck2[0] = abs(pck2[0] - 1.0)
        
        # Calculate packet errors
        n_errors, pck_error = self.source.calculate_error(pck2)
        
        # Assert if one error was found
        self.assertEqual(1,n_errors)
        self.assertTrue(pck_error)
        
    def test_generate_packet(self):
        # Test packet size
        self.assertEqual(1000,len(self.pck))
        
        # Test if it's just 0s and 1s
        self.assertTrue(np.all((self.pck == 0) | (self.pck == 1)))
        
        # Test if the number of 0s and 1s is aproximatelly equal
        self.assertAlmostEqual(0.5,np.mean(self.pck),delta = 0.05)
        
        # Test if packets are different
        pck2 = self.source.generate_packet()
        self.assertFalse(np.all(self.pck == pck2))
        
if __name__ == '__main__':
    unittest.main()