# -*- coding: utf-8 -*-
"""
Modem class unit test.

Created on Mon Apr 10 09:25:22 2017

@author: Calil
"""

import unittest
import numpy as np

from support.enumerations import ModType
from modem import Modem

class ModemTest(unittest.TestCase):
    
    def setUp(self):
        # QPSK Mpdulator
        self.modem_qpsk = Modem(4,ModType.PSK)
        #8PSK Modulator with no padding
        self.modem_8psk = Modem(8,ModType.PSK,pad=False)
        #16QAM Modulator with normalization
        self.modem_16qam = Modem(16,ModType.QAM,norm=True)
        #Custom modulation order 4
        const = np.array([1+0j, -1+1j, -1+0j, -1-1j])
        self.modem_custom = Modem(4,ModType.CUSTOM,constellation=const)
        
    def test_mod_order(self):
        self.assertEqual(self.modem_qpsk.mod_order,4)
        self.assertEqual(self.modem_8psk.mod_order,8)
        self.assertEqual(self.modem_16qam.mod_order,16)
        
    def test_bits_per_symbol(self):
        self.assertEqual(self.modem_qpsk.bits_per_symbol,2)
        self.assertEqual(self.modem_8psk.bits_per_symbol,3)
        self.assertEqual(self.modem_16qam.bits_per_symbol,4)
        
    def test_mod_type(self):
        self.assertEqual(self.modem_qpsk.mod_type,ModType.PSK)
        self.assertEqual(self.modem_16qam.mod_type,ModType.QAM)
        self.assertEqual(self.modem_custom.mod_type,ModType.CUSTOM)
        
    def test_pad(self):
        self.assertTrue(self.modem_qpsk.pad)
        self.assertFalse(self.modem_8psk.pad)
        
    def test_norm(self):
        self.assertFalse(self.modem_qpsk.norm)
        self.assertTrue(self.modem_16qam.norm)
    
    def test_constellation(self):
        #Tolerance
        eps = 1e-5
        
        const_qpsk_ang = np.deg2rad(np.array([-90,0,90,180]))
        self.assertTrue(np.allclose(abs(self.modem_qpsk.constellation),1,\
                                    atol = eps))
        self.assertTrue(np.allclose(np.angle(self.modem_qpsk.constellation),\
                                    const_qpsk_ang,atol=eps))
        
        const_8psk_ang = np.deg2rad(np.array([-45, 0, 45, 90, 135, 180,\
                                              -135,-90]))
        self.assertTrue(np.allclose(abs(self.modem_8psk.constellation),1,\
                                    atol = eps))
        self.assertTrue(np.allclose(np.angle(self.modem_8psk.constellation),\
                                    const_8psk_ang,atol=eps))
        
        const_16qam = np.array([-3.-3.j, -3.-1.j, -3.+1.j, -3.+3.j, -1.-3.j,\
                                -1.-1.j, -1.+1.j, -1.+3.j,  1.-3.j, 1.-1.j,\
                                1.+1.j,  1.+3.j,  3.-3.j,  3.-1.j,  3.+1.j,\
                                3.+3.j])
        self.assertTrue(np.allclose(np.real(self.modem_16qam.constellation),\
                                    np.real(const_16qam),atol = eps))
        self.assertTrue(np.allclose(np.imag(self.modem_16qam.constellation),\
                                    np.imag(const_16qam)))
        
        const_custom = np.array([1+0j, -1+1j, -1+0j, -1-1j])
        self.assertTrue(np.allclose(np.real(self.modem_custom.constellation),\
                                    np.real(const_custom),atol = eps))
        self.assertTrue(np.allclose(np.imag(self.modem_custom.constellation),\
                                    np.imag(const_custom)))

    
if __name__ == '__main__':
    unittest.main()