# -*- coding: utf-8 -*-
"""
Modem class unit test.

Created on Mon Apr 10 09:25:22 2017

@author: Calil
"""

import unittest
from modem import Modem

class ModemTest(unittest.TestCase):
    
    def setUp(self):   
        # BPSK modem
        self.mod_bpsk = Modem(2,True,True)
        # QPSK modem
        self.mod_qpsk = Modem(4,True,True)
        # 8-PSK modem
        self.mod_8psk = Modem(8,True,True)
        # 16-QAM modem
        self.mod_16qam = Modem(16,True,True)
        # 64-QAM modem
        self.mod_64qam = Modem(64,True,True)
        # 256-QAM modem
        self.mod_256qam = Modem(256,True,True)
        
        # No normalization
        self.mod_no_norm = Modem(2,False,True)
        
        # No padding
        self.mod_no_pad = Modem(2,True,False)
    
    def test_exeptions(self):
        # Test exception if modulation order is not a power of 2
        with self.assertRaises(NameError):
            Modem(15,True,True)
    
    def test_get_mod_order(self):
        self.assertEqual(2,self.mod_bpsk.get_mod_order())
        self.assertEqual(4,self.mod_qpsk.get_mod_order())
        self.assertEqual(8,self.mod_8psk.get_mod_order())
        self.assertEqual(16,self.mod_16qam.get_mod_order())
        self.assertEqual(64,self.mod_64qam.get_mod_order())
        self.assertEqual(256,self.mod_256qam.get_mod_order())
    
    def test_get_normalize(self):
        # Assert for normalization boolean
        self.assertTrue(self.mod_bpsk.get_normalize())
        self.assertTrue(self.mod_qpsk.get_normalize())
        self.assertTrue(self.mod_8psk.get_normalize())
        self.assertTrue(self.mod_16qam.get_normalize())
        self.assertTrue(self.mod_64qam.get_normalize())
        self.assertTrue(self.mod_256qam.get_normalize())
        
        self.assertFalse(self.mod_no_norm.get_normalize())
        pass
    
    def test_get_padding(self):
        # Assert for padding boolean
        self.assertTrue(self.mod_bpsk.get_padding())
        self.assertTrue(self.mod_qpsk.get_padding())
        self.assertTrue(self.mod_8psk.get_padding())
        self.assertTrue(self.mod_16qam.get_padding())
        self.assertTrue(self.mod_64qam.get_padding())
        self.assertTrue(self.mod_256qam.get_padding())
        
        self.assertFalse(self.mod_no_pad.get_padding())
        
    def test_get_constelation(self):
        self.assertEqual(0,self.mod_bpsk.get_constelation())
        self.assertEqual(0,self.mod_qpsk.get_constelation())
        self.assertEqual(0,self.mod_8psk.get_constelation())
        self.assertEqual(0,self.mod_16qam.get_constelation())
        self.assertEqual(0,self.mod_64qam.get_constelation())
        self.assertEqual(0,self.mod_256qam.get_constelation())
    
    def test_set_mod_order(self):
        # Create object
        mod_set = Modem(16,True,True)
        
        # Assert modulation order
        self.assertEqual(16,mod_set.get_mod_order())
        
        #Change order and assert again
        mod_set.set_mod_order(64)
        self.assertEqual(64,mod_set.get_mod_order())
    
    def test_modulate(self):
        pass
    
    def test_demodulate(self):
        pass
    
    def test_modulate_and_demodulate(self):
        pass
    
if __name__ == '__main__':
    unittest.main()