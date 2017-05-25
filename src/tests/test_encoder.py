# -*- coding: utf-8 -*-
"""
Unit tests for Source class

Created on Sun Mar 26 08:14:37 2017

@author: Calil
"""

import unittest
import numpy as np
from encoder import Encoder as encoder

class EncodingTest(unittest.TestCase):
    
    def setUp(self):
     
        self.generation_matrix = np.array([[1, 0, 0, 0, 1, 1, 0],
                                      [0, 1, 0, 0, 0, 1, 1],
                                      [0, 0, 1, 0, 1, 0, 1],
                                      [0, 0, 0, 1, 1, 1, 1]])

        self.encoder = encoder(3, np.array([4, 7]), self.generation_matrix)

    def test_user_defined_matrix(self):
        self.assertTrue(np.array_equal(self.encoder.get_codeword_table(),np.array([0, 15, 21, 26, 35, 44, 54, 57, 70, 73, 83, 92, 101, 106, 112, 127])))

    def test_encode(self):
        self.assertTrue(np.array_equal(self.encoder.encode([0, 1, 0, 0, 1, 0, 0, 0, 1, 1]),
                                       np.array([0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1])))
        self.assertFalse(np.array_equal(self.encoder.encode([0, 1, 0, 0, 1, 0, 0, 0, 1, 1]),
                                       np.array([0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0])))

    def test_decode(self):
        # signal to enter the decoder
        signal_in = np.array([0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1])

        decoded_bits = self.encoder.decode(signal_in)

        # comparison with expected bits
        expected_bits = np.array([0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0])
        self.assertTrue(np.array_equal(decoded_bits, expected_bits))

if __name__ == '__main__':
    unittest.main()