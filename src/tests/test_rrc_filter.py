# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:11:26 2017

@author: Calil
"""

import unittest
import numpy as np
import matplotlib.pylab as plt

from rrc_filter import RRCFilter

class RRCFilterTest(unittest.TestCase):
    
    def setUp(self):
        # Flag for plotting
        self.plot_flag = True
        
        # Filters
        self.filter1 = RRCFilter(1000,0.8,1e-4,2e6,8)
        self.filter2 = RRCFilter(2000,0.6,1e-3,2e5,16)
        self.filter3 = RRCFilter(33,0.911,2e-5,2.3e6,4)
        
    def test_N(self):
        self.assertEqual(self.filter1.N,1000)
        
    def test_alpha(self):
        self.assertEqual(self.filter1.alpha,0.8)
        
    def test_Ts(self):
        self.assertEqual(self.filter1.Ts,1e-4)
        
    def test_Fs(self):
        self.assertEqual(self.filter1.Fs,2e6)
        
    def test_up_factor(self):
        self.assertEqual(self.filter1.up_factor,8)
        
    def test_up_sample(self):
        symbs = np.ones(10)
        up_symbs = self.filter1.upsample(symbs)
        self.assertEqual(len(up_symbs),80)
        self.assertEqual(np.sum(up_symbs),10)
        
    def test_filter_response(self):
        h, t = self.filter1.filter_response(1000,0.8,1e-4,2e6)
        self.assertAlmostEqual(np.sum(abs(h)**2),1.0,delta=1e-5)
        self.assertTrue(np.all(h == self.filter1.response))
        self.assertTrue(np.all(t == self.filter1.time))
        
    def test_apply_filter(self):
        
        # Calculate response
        h = self.filter1.response
        t = self.filter1.time
        
        if self.plot_flag:
            plt.plot(t,h)
            plt.xlabel("Time [s]")
            plt.ylabel("Impulse response")
            plt.show()
            
        # Generate impulse at zero
        n = int(self.filter1.Fs/1000)
        t = np.linspace(0,0.001,n)
        sig = np.zeros(n)
        sig[0] = 2
        sig[n-1] = 1
        
        # Filter 1 and assert delay
        h = self.filter1.response
        filt_sig = self.filter1.apply_filter(h,sig,8)
        self.assertEqual(np.argmax(filt_sig),0)
        
        if self.plot_flag:
            plt.plot(filt_sig)
            plt.xlabel("Time [s]")
            plt.ylabel("Filtered signal")
            plt.show()
            
        # Filter 2 and assert delay
        h = self.filter2.response
        filt_sig = self.filter2.apply_filter(h,sig,16)
        self.assertEqual(np.argmax(filt_sig),0)
        
        if self.plot_flag:
            plt.plot(filt_sig)
            plt.xlabel("Time [s]")
            plt.ylabel("Filtered signal")
            plt.show()
        
        # Filter 3 and assert delay
        h = self.filter3.response
        filt_sig = self.filter3.apply_filter(h,sig,4)
        self.assertEqual(np.argmax(filt_sig),0)
        
        if self.plot_flag:
            plt.plot(filt_sig)
            plt.xlabel("Time [s]")
            plt.ylabel("Filtered signal")
            plt.show()
        
if __name__ == '__main__':
    unittest.main()