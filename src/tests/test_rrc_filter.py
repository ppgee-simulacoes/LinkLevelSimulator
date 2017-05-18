# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:11:26 2017

@author: Calil
"""

import unittest
import numpy as np
import matplotlib.pylab as plt
import warnings

from rrc_filter import RRCFilter

class RRCFilterTest(unittest.TestCase):
    
    def setUp(self):
        # Display warning traceback
        warnings.simplefilter("error")
        
        # Flag for plotting
        self.plot_flag = True
        
        # Filters
        self.filter1 = RRCFilter(10,0.8,1e-4,2e6)
        self.filter2 = RRCFilter(20,0.6,1e-3,2e5)
        self.filter3 = RRCFilter(8,0.911,2e-5,2.3e6)
        self.filter4 = RRCFilter(6,0.5,1e-3,1e6)
        
    def test_N(self):
        self.assertEqual(self.filter1.N,10*int(1e-4*2e6))
        
    def test_alpha(self):
        self.assertEqual(self.filter1.alpha,0.8)
        
    def test_Ts(self):
        self.assertEqual(self.filter1.Ts,1e-4)
        
    def test_Fs(self):
        self.assertEqual(self.filter1.Fs,2e6)
        
    def test_up_factor(self):
        self.assertEqual(self.filter1.up_factor,int(1e-4*2e6))
        
    def test_up_and_down_sample(self):
        #Upsample
        symbs = np.ones(10)
        up_symbs = self.filter1.upsample(symbs)
        self.assertEqual(len(up_symbs),int(1e-4*2e6)*10)
        self.assertEqual(np.sum(up_symbs),10)
        #Downsample
        down_symbs = self.filter1.downsample(up_symbs)
        self.assertTrue(np.all(down_symbs == symbs))
        self.assertEqual(np.sum(down_symbs),10)
        
    def test_filter_response(self):
        h, t = self.filter1.filter_response(int(10*1e-4*2e6),0.8,1e-4,2e6)
        self.assertAlmostEqual(np.sum(abs(h)**2),1.0,delta=1e-5)
        self.assertTrue(np.all(h == self.filter1.response))
        self.assertTrue(np.all(t == self.filter1.time))
        
    def test_apply_filter(self):
        
        # Calculate response
        h = self.filter1.response
        t = self.filter1.time
        
        if self.plot_flag:
            plt.plot(t,h)
            plt.title("Filter 1 Response")
            plt.show()
            
        # Generate impulse at zero
        n = int(self.filter1.Fs/1000)
        t = np.linspace(0,0.001,n)
        sig = np.zeros(n)
        sig[0] = 1
        sig[n-1] = 1
        
        # Filter 1 and assert delay
        h = self.filter1.response
        filt_sig = self.filter1.apply_filter(h,sig)
        self.assertEqual(len(filt_sig),(len(h)+len(sig)))
        
        if self.plot_flag:
            plt.plot(filt_sig)
            plt.title("Filter 1: Filtered signal")
            plt.show()
            
        # Filter 2 and assert delay
        h = self.filter2.response
        filt_sig = self.filter2.apply_filter(h,sig)
        self.assertEqual(len(filt_sig),(len(h)+len(sig)))
        
        if self.plot_flag:
            plt.plot(filt_sig)
            plt.title("Filter 2: Filtered signal")
            plt.show()
        
        # Filter 3 and assert delay
        h = self.filter3.response
        filt_sig = self.filter3.apply_filter(h,sig)
        self.assertEqual(len(filt_sig),(len(h)+len(sig)))
        
        if self.plot_flag:
            plt.plot(filt_sig)
            plt.title("Filter 3: Filtered signal")
            plt.show()
            
    def test_tx_rx(self):
        #Create symbols
        symbs = np.random.choice([-3,-1,1,3],50)
        
        # Transmit symbols
        signal = self.filter4.tx_filter(symbs)
        up = self.filter4.up_factor
        h = self.filter4.response
        self.assertEqual(len(signal),up*len(symbs)+len(h))
        self.assertAlmostEqual(np.sum(np.imag(signal)),0,delta=1e-5)
        
        if self.plot_flag:
            plt.plot(np.real(signal))
            plt.title("Transmitted signal")
            plt.show()
            
        # Test second filtering
        h = self.filter4.response
        filt_sig = self.filter4.apply_filter(h,signal)
        
        if self.plot_flag:
            plt.plot(np.real(filt_sig))
            plt.title("Filtered signal")
            plt.show()
            
        # Receive signal
        rx_symb = self.filter4.rx_filter(signal)
        self.assertEqual(len(rx_symb),len(symbs))
        err = abs(symbs - rx_symb)
        self.assertAlmostEqual(np.max(err),0.0,delta=1e-1)
        
        if self.plot_flag:
            plt.plot(err)
            plt.title("Symbol error")
            plt.show()
        
if __name__ == '__main__':
    unittest.main()