# -*- coding: utf-8 -*-
"""
Unit tests for Channel class

Created on Sun Mar 26 12:12:32 2017

@author: Calil
"""

import unittest
import numpy as np

from src.support.enumerations import ChannelModel
from src.channel import Channel

class ChannelTest(unittest.TestCase):
    def setUp(self):
        seed = 10
        self.n_bits = 1000
        p_val = 1e-5
        self.channel1 = Channel(ChannelModel.IDEAL,seed,p_val)
        self.channel2 = Channel(ChannelModel.CONSTANT,seed,p_val)
        self.channel3 = Channel(ChannelModel.MARKOV,seed,p_val)
        self.channel4 = Channel(3,seed,p_val)
        
    def test_get_model(self):
        self.assertEqual(ChannelModel.IDEAL,\
                         self.channel1.get_model())
        self.assertEqual(ChannelModel.CONSTANT,\
                         self.channel2.get_model())
        self.assertEqual(ChannelModel.MARKOV,\
                         self.channel3.get_model())
        
    def test_get_seed(self):
        self.assertEqual(10,self.channel1.get_seed())
        
    def test_get_p_val(self):
        self.assertEqual(1e-5,self.channel1.get_p_val())
        
    def test_set_p_val(self):
        self.channel1.set_p_val(2e-5)
        self.assertEqual(2e-5,self.channel1.get_p_val())
        
    def test_fade(self):
        """
        TODO Implement unit test for Markov channel
        """
        pck_Tx = np.zeros(self.n_bits)
        self.assertEqual(self.n_bits,len(pck_Tx))
        
        # Ideal channel should cause no bit errors
        pck_Rx = self.channel1.fade(pck_Tx)
        self.assertEqual(0,np.sum(pck_Rx))
        self.assertTrue(np.all((pck_Rx == 0) | (pck_Rx == 1)))
        
        # Constant channel should introduce some error
        self.channel2.set_p_val(0.5)
        self.assertEqual(0.5,self.channel2.get_p_val())
        pck_Rx = self.channel2.fade(pck_Tx)
        self.assertTrue(np.all((pck_Rx == 0) | (pck_Rx == 1)))
        self.assertAlmostEqual(500.0,np.sum(pck_Rx),delta = 50)
            
        # For now, Markov channel sould raise exception
        with self.assertRaises(NotImplementedError):
            pck_Rx = self.channel3.fade(pck_Tx)
        
        # Invalid Channel Model should raise exception
        with self.assertRaises(NameError):
            pck_Rx = self.channel4.fade(pck_Tx)
        
if __name__ == '__main__':
    unittest.main()