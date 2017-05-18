# -*- coding: utf-8 -*-
"""
Unit tests for Source class

Created on Sun Mar 26 08:14:37 2017

@author: Calil
"""

import unittest
import numpy as np
from coding import Coding as coding

class CodingTest(unittest.TestCase, ):
    
    def setUp(self):
     
        self.generation_matrix = np.array([[1, 0, 0, 0, 1, 1, 0],
                                      [0, 1, 0, 0, 0, 1, 1],
                                      [0, 0, 1, 0, 1, 0, 1],
                                      [0, 0, 0, 1, 1, 1, 1]])

        self.coding_3 = coding(3, np.array([4, 7]), self.generation_matrix)

    def test_user_defined_matrix(self):
        self.assertTrue(np.array_equal(self.coding_3.get_codeword_table(),np.array([0, 15, 21, 26, 35, 44, 54, 57, 70, 73, 83, 92, 101, 106, 112, 127])))

    def test_encode(self):
        self.assertTrue(np.array_equal(self.coding_3.encode([0, 1, 0, 0, 1, 0, 0, 0, 1, 1]),
                                       np.array([0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1])))
        self.assertFalse(np.array_equal(self.coding_3.encode([0, 1, 0, 0, 1, 0, 0, 0, 1, 1]),
                                       np.array([0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0])))

if __name__ == '__main__':
    unittest.main()