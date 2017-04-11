# -*- coding: utf-8 -*-
"""
Results class unit tests.

Created on Sun Apr  2 08:42:53 2017

@author: Calil
"""

import unittest
import numpy as np
from src.results import Results
from src.parameters.parameters import Parameters

class ResultsTest(unittest.TestCase):
    
    def setUp(self):
        param = Parameters(1)
        param.p = np.logspace(-6,-4, num = 20)
        figs_dir = "test_figs/"
        self.res = Results(param, figs_dir)
        
    def test_get_param(self):
        par = self.res.get_param()
        self.assertEqual(20,len(par.p))
        
    def test_get_figs_dir(self):
        f_dir = self.res.get_figs_dir()
        self.assertEqual("test_figs/",f_dir)
        
    def test_get_per_list(self):
        per = self.res.get_per_list()
        self.assertEqual(0,len(per))
        
    def test_get_per_conf(self):
        per_conf = self.res.get_per_conf()
        self.assertEqual(0,len(per_conf))
    
    def test_get_thrpt_list(self):
        thrpt = self.res.get_thrpt_list()
        self.assertEqual(0,len(thrpt))
    
    def test_get_thrpt_conf(self):
        thrpt_conf = self.res.get_thrpt_conf()
        self.assertEqual(0,len(thrpt_conf))
        
    def test_store_res_plot(self):
        per_tpl = (1.0e-05, 1.0e-06)
        thrpt_tpl = (50, 0.5)
        
        # Add len.p PER and Throughput results
        len_p = len(self.res.get_param().p)
        for k in range(0,len_p):
            self.res.store_res(per_tpl,thrpt_tpl)
            
        # Check PER length
        per = self.res.get_per_list()
        self.assertEqual(len_p,len(per))
        
        # Check PER confidence length
        per_conf = self.res.get_per_conf()
        self.assertEqual(len_p,len(per_conf))
        
        # Check thrpt length
        thrpt = self.res.get_thrpt_list()
        self.assertEqual(len_p,len(thrpt))
        
        # Check thrpt_conf lenth
        thrpt_conf = self.res.get_thrpt_conf()
        self.assertEqual(len_p,len(thrpt_conf))
        
        # Plot
        theo_per = 1.0e-05*np.ones([len_p,])
        theo_thrpt = 50*np.ones([len_p,])
        self.res.plot(theo_per,theo_thrpt)

if __name__ == '__main__':
    unittest.main()