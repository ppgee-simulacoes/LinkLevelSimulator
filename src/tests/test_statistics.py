# -*- coding: utf-8 -*-
"""
Unit tests for statistics class.

Created on Mon Mar 27 14:54:10 2017

@author: Calil
"""

import unittest

from src.statistics import Statistics

class StatisticsTest(unittest.TestCase):
    
    def setUp(self):
        conf = 0.95     # Confidence
        n_bits = 1000   # Number of bits per packet
        tx_rate = 50    # Tx rate in Mbps
        
        self.stat = Statistics(n_bits,tx_rate,conf)
        
    def test_get_conf(self):
        self.assertEqual(0.95,self.stat.get_conf())
        
    def test_get_n_bits(self):
        self.assertEqual(1000,self.stat.get_n_bits())
        
    def test_get_tx_rate(self):
        self.assertEqual(50,self.stat.get_tx_rate())
        
    def test_get_n_pcks(self):
        self.assertEqual(0,self.stat.get_n_pcks())
        
    def test_get_n_pck_errors(self):
        self.assertEqual(0,self.stat.get_n_pck_errors())
        
    def test_get_per_list(self):
        self.assertEqual(0,len(self.stat.get_per_list()))
        
    def test_get_thrpt_list(self):
        self.assertEqual(0,len(self.stat.get_thrpt_list()))
        
    def test_pck_received(self):
        self.stat.pck_received(False)
        self.stat.pck_received(False)
        self.stat.pck_received(False)
        self.stat.pck_received(True)
        
        self.assertEqual(4,self.stat.get_n_pcks())
        self.assertEqual(1,self.stat.get_n_pck_errors())
        
        # Test calc_iteration_results() method
        per, thrpt = self.stat.calc_iteration_results()
        self.assertEqual(0.25,per)
        self.assertEqual(37.5,thrpt)
        
        self.assertEqual([0.25],self.stat.get_per_list())
        self.assertEqual([37.5],self.stat.get_thrpt_list())     
        
    def test_conf_interval(self):
        # Data with zero standard deviation
        data = [5, 5, 5, 5, 5, 5, 5, 5]
        meanVal, interv = self.stat.conf_interval(data)
        self.assertEqual(5,meanVal)
        self.assertEqual(0,interv)
        
        # General data
        data = [1.0e-04, 5.0e-05, 1.0e-05, 2.0e-05]
        meanVal, interv = self.stat.conf_interval(data)
        self.assertAlmostEqual(4.5e-05,meanVal, delta = 0.05e-05)
        self.assertAlmostEqual(6.42995e-05,interv,delta=0.05e-05)
        
    def test_wrap_up(self):
        # Simulating iteration: 4 packets with tha same seed
        self.stat.pck_received(False)
        self.stat.pck_received(False)
        self.stat.pck_received(False)
        self.stat.pck_received(True)
        
        self.assertEqual(4,self.stat.get_n_pcks())
        self.assertEqual(1,self.stat.get_n_pck_errors())
        
        # calc_iteration_results() should yeld PER and Tput for this seed
        per, thrpt = self.stat.calc_iteration_results()
        self.assertEqual(0.25,per)
        self.assertEqual(37.5,thrpt)
        
        # calc_iteration_resulst() should also reset the number of packets
        self.assertEqual(0,self.stat.get_n_pcks())
        self.assertEqual(0,self.stat.get_n_pck_errors())
        
        # calc_iteration_results() should not reset lists, though
        self.assertEqual([0.25],self.stat.get_per_list())
        self.assertEqual([37.5],self.stat.get_thrpt_list()) 
        
        # Simulating another iteration
        self.stat.pck_received(False)
        self.stat.pck_received(False)
        self.stat.pck_received(False)
        self.stat.pck_received(True)
        
        # calc_iteration_results() finishes the iteration
        per, thrpt = self.stat.calc_iteration_results()
        
        per_tpl, thrpt_tpl = self.stat.wrap_up()
        
        self.assertEqual(0.25,per_tpl[0])
        self.assertEqual(0,per_tpl[1])
        self.assertEqual(37.5,thrpt_tpl[0])
        self.assertEqual(0,thrpt_tpl[1])
        
        # wrap_up() should reset lists
        self.assertEqual(0,len(self.stat.get_per_list()))
        self.assertEqual(0,len(self.stat.get_thrpt_list()))
        
if __name__ == '__main__':
    unittest.main()
        