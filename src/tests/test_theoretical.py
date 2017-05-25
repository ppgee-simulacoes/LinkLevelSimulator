# -*- coding: utf-8 -*-
"""
Theoretical class unit tests.

Created on Sun Apr  2 11:58:11 2017

@author: Calil
"""

import unittest
import numpy as np

from support.enumerations import ChannelModel, BSCType, ModType
from theoretical import Theoretical
from parameters import Parameters

class TheoreticalTest(unittest.TestCase):
    
    def setUp(self):
        param = Parameters(1)
        param.chan_mod = ChannelModel.IDEAL
        param.mod_order = 2
        param.mod_type = ModType.PSK
        param.ebn0 = np.linspace(0, 10, num=11)
        param.tx_rate = 50
        param.n_bits = 1000
        param.p = np.logspace(1.0e-5,1.0e-3, num = 25)
        
        # General object
        self.theo = Theoretical(param)
        
        # Ideal channel object, with noise
        self.theo_ideal = Theoretical(param)
        
        # Constant channel object
        param.chan_mod = ChannelModel.BSC
        param.bsc_type = BSCType.CONSTANT
        param.p = np.array([0.5, 1.0e-04])
        
        self.theo_const = Theoretical(param)
        
        # Markov channel
        param.chan_mod = ChannelModel.BSC
        param.bsc_type = BSCType.MARKOV
        param.p = np.array([0.5, 1.0e-4])
        
    def test_get_model(self):
        mod = self.theo.get_model()
        self.assertEqual(mod,ChannelModel.IDEAL)
        
    def test_get_tx_rate(self):
        rate = self.theo.get_tx_rate()
        self.assertEqual(50,rate)
        
    def test_get_n_bits(self):
        self.assertEqual(1000,self.theo.get_n_bits())
        
    def test_get_state_ps(self):
        ps = self.theo.get_state_ps()
        self.assertEqual(0,len(ps))
        
    def test_validate(self):
        # Ideal channel should have 0 BER and PER and Tput = tx_rate
        ber, per, thrpt = self.theo_ideal.validate()
        
        # Assert lenghts
        self.assertEqual(len(ber),11)
        self.assertEqual(len(per),11)
        self.assertEqual(len(thrpt),11)
        
        # Test constant channel
        ber, per, thrpt = self.theo_const.validate()
        self.assertTrue(np.all(np.array([0.5, 1.0e-04]) == ber))
        self.assertAlmostEqual(1,per[0],delta = 0.05)
        self.assertAlmostEqual(9.517e-2,per[1],delta = 0.05e-2)
        self.assertAlmostEqual(0,thrpt[0],delta = 0.05)
        self.assertAlmostEqual(45.242,thrpt[1],delta = 0.05)
        
        
    
if __name__ == '__main__':
    unittest.main()