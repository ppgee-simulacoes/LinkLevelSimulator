# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:11:26 2017

@author: Calil
"""

import unittest
import numpy as np

from rrc_filter import RRCFilter

class RRCFilterTest(unittest.TestCase):
    
    def setUp(self):
        # Filter 1
        self.filter1 = RRCFilter(20,0.5,1e-3,2e6,8)
        
    def test_N(self):
        self.assertEqual(self.filter1.N,20)
        
    def test_alpha(self):
        self.assertEqual(self.filter1.alpha,0.5)
        
    def test_Ts(self):
        self.assertEqual(self.filter1.Ts,1e-3)
        
    def test_Fs(self):
        self.assertEqual(self.filter1.Fs,2e6)
        
    def test_up_factor(self):
        self.assertEqual(self.filter1.up_factor,8)
        
    def test_up_sample(self):
        symbs = np.ones(10)
        up_symbs = self.filter1.upsample(symbs)
        self.assertEqual(len(up_symbs),80)
        self.assertEqual(np.sum(up_symbs),10)
        
if __name__ == '__main__':
    unittest.main()