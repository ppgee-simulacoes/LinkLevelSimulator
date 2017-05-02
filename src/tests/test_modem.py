# -*- coding: utf-8 -*-
"""
Modem class unit test.

Created on Mon Apr 10 09:25:22 2017

@author: Calil e Eduardo
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
        
        # 64 QAM modulator
        self.modem_64qam = Modem(64,ModType.QAM,norm=True)
        
    def test_mod_order(self):
        self.assertEqual(self.modem_qpsk.mod_order,4)
        self.assertEqual(self.modem_8psk.mod_order,8)
        self.assertEqual(self.modem_16qam.mod_order,16)
        with self.assertRaises(NameError):
            Modem(15,ModType.CUSTOM)
        
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
        
    def test_scaling(self):
        self.assertEqual(self.modem_16qam.scaling,np.sqrt(10))
        self.assertEqual(self.modem_qpsk.scaling,1)
        self.assertEqual(self.modem_64qam.scaling,np.sqrt(42))
    
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
        
    def test_set_modulation(self):
        with self.assertRaises(NameError):
            Modem(4,ModType.CUSTOM)
        
        with self.assertRaises(NameError):
            const = np.array([1, 2, 3])
            Modem(4,ModType.CUSTOM,constellation=const)
            
    def test_bitarray2dec(self):
        bits = np.array([1,0,1,1,1])
        self.assertEqual(self.modem_qpsk.bitarray2dec(bits),23)
        bits = np.array([1,1,0,1,1,0,0])
        self.assertEqual(self.modem_16qam.bitarray2dec(bits),108)
        bits = np.array([1,0])
        self.assertEqual(self.modem_custom.bitarray2dec(bits),2)
        
    def test_modulate(self):
        #Error margin
        eps = 1e-5
        
        # Tests without padding
        bits = np.array([0,0,0,1,1,0,1,1])
        
        # QPSK Modulation
        expected_symbs = np.array([0-1j,1+0j,0+1j,-1+0j])
        symbs = self.modem_qpsk.modulate(bits)
        self.assertEqual(len(symbs),len(bits)/2)
        self.assertTrue(np.allclose(np.real(symbs),np.real(expected_symbs),atol=eps))
        self.assertTrue(np.allclose(np.imag(symbs),np.imag(expected_symbs),atol=eps))
        
        # 8PSK Modulation
        with self.assertRaises(NameError):
            self.modem_8psk.modulate(bits)
        
        #16-QAM Modulation
        expected_symbs = np.array([-3-1j,1+3j])/np.sqrt(10)
        symbs = self.modem_16qam.modulate(bits)
        self.assertEqual(len(symbs),len(bits)/4)
        self.assertTrue(np.allclose(np.real(symbs),np.real(expected_symbs),atol=eps))
        self.assertTrue(np.allclose(np.imag(symbs),np.imag(expected_symbs),atol=eps))
        
        # Custom Modulation
        expected_symbs = np.array([1+0j, -1+1j, -1+0j, -1-1j])
        symbs = self.modem_custom.modulate(bits)
        self.assertEqual(len(symbs),len(bits)/2)
        self.assertTrue(np.allclose(np.real(symbs),np.real(expected_symbs),atol=eps))
        self.assertTrue(np.allclose(np.imag(symbs),np.imag(expected_symbs),atol=eps))
        
        # Tests with padding
        bits = np.array([0,0,0,1,1,0,1,1,0])
        
        # Tests without padding
        # QPSK Modulation
        expected_symbs = np.array([0-1j,1+0j,0+1j,-1+0j,0-1j])
        symbs = self.modem_qpsk.modulate(bits)
        self.assertEqual(len(symbs),1 + np.floor(len(bits)/2))
        self.assertTrue(np.allclose(np.real(symbs),np.real(expected_symbs),atol=eps))
        self.assertTrue(np.allclose(np.imag(symbs),np.imag(expected_symbs),atol=eps))
        
        #16-QAM Modulation
        expected_symbs = np.array([-3-1j,1+3j,-3-3j])/np.sqrt(10)
        symbs = self.modem_16qam.modulate(bits)
        self.assertEqual(len(symbs),1 + np.floor(len(bits)/4))
        self.assertTrue(np.allclose(np.real(symbs),np.real(expected_symbs),atol=eps))
        self.assertTrue(np.allclose(np.imag(symbs),np.imag(expected_symbs),atol=eps))
        
        # Custom Modulation
        expected_symbs = np.array([1+0j, -1+1j, -1+0j, -1-1j, 1+0j])
        symbs = self.modem_custom.modulate(bits)
        self.assertEqual(len(symbs),1 + np.floor(len(bits)/2))
        self.assertTrue(np.allclose(np.real(symbs),np.real(expected_symbs),atol=eps))
        self.assertTrue(np.allclose(np.imag(symbs),np.imag(expected_symbs),atol=eps))
        
    def test_demodulate(self):
        # QPSK Modulation
        in_symbols = np.array([0-1j,1+0j,0+1j,-1+0j])
        expected_bits = np.array([0,0,0,1,1,0,1,1])
        bits = self.modem_qpsk.demodulate(in_symbols)
        self.assertEqual(len(in_symbols)*2,len(expected_bits))
        self.assertTrue(np.allclose(bits,expected_bits))
        
        # From 16-QAM
        in_symbols = np.array([-3-1j,1+3j])/np.sqrt(10)
        expected_bits = np.array([0,0,0,1,1,0,1,1])
        bits = self.modem_16qam.demodulate(in_symbols)
        self.assertEqual(len(in_symbols)*4,len(expected_bits))
        self.assertTrue(np.allclose(bits,expected_bits))
        
        # Custom Modulation
        in_symbols = np.array([1+0j, -1+1j, -1+0j, -1-1j])
        expected_bits = np.array([0,0,0,1,1,0,1,1])
        bits = self.modem_custom.demodulate(in_symbols)
        self.assertEqual(len(in_symbols)*2,len(expected_bits))
        self.assertTrue(np.allclose(bits,expected_bits))
        
if __name__ == '__main__':
    unittest.main()