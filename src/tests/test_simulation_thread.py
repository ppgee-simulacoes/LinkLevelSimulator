# -*- coding: utf-8 -*-
"""
SimulationThread class unit tests.

Created on Sun Apr  2 15:21:28 2017

@author: Calil
"""

import unittest
import numpy as np
from src.simulation_thread import SimulationThread
from src.parameters.parameters import Parameters
from src.support.enumerations import ChannelModel
from src.support.enumerations import SimType

class SimulationThreadTest(unittest.TestCase):
    
    def setUp(self):
        par = Parameters(1)
        figs_dir = "test_figs/"
        
        self.par = par
        
        # Redefine parameters for easy testing
        self.par.simulation_type = SimType.FIXED_SEEDS
        new_seed = np.array([0, 1, 2, 3, 4])
        self.par.seeds = new_seed.astype(int)
        self.par.n_pcks = 1000
        
        # Create thread with ideal channel
        self.par.chan_mod = ChannelModel.IDEAL
        self.sim = SimulationThread(self.par,figs_dir)
        
        # Crate thread with constant channel
        self.par.chan_mod = ChannelModel.CONSTANT
        const_figs_dir = "test_figs/const_"
        self.sim_const = SimulationThread(self.par,const_figs_dir)
    
    def test_get_seed_count(self):
        self.assertEqual(0,self.sim.get_seed_count())
        
    def test_get_ber_count(self):
        self.assertEqual(0,self.sim.get_ber_count())
        
    def test_send_pck(self):
        n_errors, pck_error = self.sim.send_pck()
        self.assertTrue(n_errors >= 0)
        if pck_error:
            self.assertTrue(n_errors > 0)
        else:
            self.assertTrue(n_errors == 0)
            
    def test_pck_loop(self):
        # Send all packets
        self.sim.pck_loop()
        self.assertEqual(990,self.sim.stat.get_n_pcks())
        self.assertEqual(0,self.sim.stat.get_n_pck_errors())
        
        # EMULATE END OF ITERATION
        per, thrpt = self.sim.stat.calc_iteration_results()
        self.assertEqual(0,per)
        self.assertEqual(50,thrpt)
        # Test lists
        self.assertEqual([0],self.sim.stat.get_per_list())
        self.assertEqual([50],self.sim.stat.get_thrpt_list()) 
        # Test if values were reset
        self.assertEqual(0,self.sim.stat.get_n_pcks())
        self.assertEqual(0,self.sim.stat.get_n_pck_errors())
        
        # Test if counters were note altered
        self.assertEqual(0,self.sim.get_seed_count())
        self.assertEqual(0,self.sim.get_ber_count())
        
    def test_seed_loop(self):
        # Loop through all the seeds
        self.sim.seed_loop()
        
        # Test counters
        self.assertEqual(5,self.sim.get_seed_count())
        self.assertEqual(0,self.sim.get_ber_count())
        
        # Test result storage
        self.assertEqual(0,len(self.sim.res.get_per_list()))
        self.assertEqual(0,len(self.sim.res.get_per_conf()))
        self.assertEqual(0,len(self.sim.res.get_thrpt_list()))
        self.assertEqual(0,len(self.sim.res.get_thrpt_conf()))
        
        # Test statistics lists length
        self.assertEqual(5,len(self.sim.stat.get_per_list()))
        self.assertEqual(5,len(self.sim.stat.get_thrpt_list()))
        
        # Test statistics lists elements
        expected_per = [0.0, 0.0, 0.0, 0.0, 0.0]
        expected_thrpt = [50.0, 50.0, 50.0, 50.0, 50.0]
        self.assertFalse(np.any(self.sim.stat.get_per_list() != expected_per))
        self.assertFalse(np.any(self.sim.stat.get_thrpt_list() != \
                                expected_thrpt))
        # Test if values were reset
        self.assertEqual(0,self.sim.stat.get_n_pcks())
        self.assertEqual(0,self.sim.stat.get_n_pck_errors())
        
        # EMULATE END OF SEEDS
        # Calculate mean and confidence
        per_tpl, thrpt_tpl = self.sim.stat.wrap_up()
        
        # Test results consistency
        self.assertEqual(0.0,per_tpl[0])
        self.assertEqual(0.0,per_tpl[1])
        self.assertEqual(50.0,thrpt_tpl[0])
        self.assertEqual(0.0,thrpt_tpl[1])
        
        # Test wrap up after math
        self.assertEqual(0,len(self.sim.stat.get_per_list()))
        self.assertEqual(0,len(self.sim.stat.get_thrpt_list()))
        self.assertEqual(0,self.sim.stat.get_n_pcks())
        self.assertEqual(0,self.sim.stat.get_n_pck_errors())
        
        # Store results
        self.sim.res.store_res(per_tpl,thrpt_tpl)
        
        # Test result storage
        self.assertEqual(1,len(self.sim.res.get_per_list()))
        self.assertEqual(1,len(self.sim.res.get_per_conf()))
        self.assertEqual(1,len(self.sim.res.get_thrpt_list()))
        self.assertEqual(1,len(self.sim.res.get_thrpt_conf()))
        self.assertEqual([0],self.sim.res.get_per_list())
        self.assertEqual([0],self.sim.res.get_per_conf())
        self.assertEqual([50],self.sim.res.get_thrpt_list())
        self.assertEqual([0],self.sim.res.get_thrpt_conf())
        
        
        # Prior to seed reset
        self.assertEqual(4 + 1,self.sim.get_seed_count())
        self.assertEqual(4,self.sim.station.get_seed())
        self.assertEqual(4,self.sim.chann.get_seed())
        
        # Reset seed counter
        self.sim.reset_seed()
        
        # After seed reset
        self.assertEqual(0,self.sim.get_seed_count())
        self.assertEqual(0,self.sim.station.get_seed())
        self.assertEqual(0,self.sim.chann.get_seed())
        
        # Set new BER
        self.sim.new_ber()
        
        # Test new BER
        self.assertEqual(1,self.sim.get_ber_count())
        self.assertEqual(self.par.p[1],self.sim.chann.get_p_val())
        
    def test_fixed_conf(self):                
        # Create thread with constant confidence
        self.par.simulation_type = SimType.FIXED_CONF
        conf_figs_dir = "test_figs/conf_"
        self.sim_conf = SimulationThread(self.par,conf_figs_dir)
        
        # Loop through all the seeds
        self.sim_conf.seed_loop()
        
        # Calculate iteration results
        per, per_conf = \
            self.sim_conf.stat.conf_interval(self.sim_conf.stat.get_per_list())
        thrpt, thrpt_conf = \
            self.sim_conf.stat.conf_interval(self.sim_conf.stat.get_thrpt_list())
            
        # Redefine minimum confidence
        conf_min = min([per_conf/per , thrpt_conf/thrpt])
        
        # Assert conf_min
        self.assertTrue(conf_min < self.par.conf_range)
        
        # Assert for seed  and BER counter
        self.assertTrue(self.sim_conf.get_seed_count() > 0)
        self.assertTrue(self.sim_conf.get_ber_count() == 0)
        
        # Assert for list lengths
        self.assertTrue(len(self.sim_conf.stat.get_per_list()) > 0)
        self.assertTrue(len(self.sim_conf.stat.get_thrpt_list()) > 0)
        
        # EMULATE END OF SEEDS
        # Calculate mean and confidence
        per_tpl, thrpt_tpl = self.sim_conf.stat.wrap_up()
        
        # Test wrap up after math
        self.assertEqual(0,len(self.sim_conf.stat.get_per_list()))
        self.assertEqual(0,len(self.sim_conf.stat.get_thrpt_list()))
        self.assertEqual(0,self.sim_conf.stat.get_n_pcks())
        self.assertEqual(0,self.sim_conf.stat.get_n_pck_errors())
        
        # Store results
        self.sim_conf.res.store_res(per_tpl,thrpt_tpl)
        
        # Test result storage
        self.assertEqual(1,len(self.sim_conf.res.get_per_list()))
        self.assertEqual(1,len(self.sim_conf.res.get_per_conf()))
        self.assertEqual(1,len(self.sim_conf.res.get_thrpt_list()))
        self.assertEqual(1,len(self.sim_conf.res.get_thrpt_conf()))        
        
        # Prior to seed reset
        self.assertTrue(self.sim_conf.get_seed_count() > 0)
        self.assertEqual(self.sim_conf.get_seed_count(),\
                         self.sim_conf.station.get_seed())
        self.assertEqual(self.sim_conf.get_seed_count(),\
                         self.sim_conf.chann.get_seed())
        
        # Reset seed counter
        self.sim_conf.reset_seed()
        
        # After seed reset
        self.assertEqual(0,self.sim_conf.get_seed_count())
        self.assertEqual(0,self.sim_conf.station.get_seed())
        self.assertEqual(0,self.sim_conf.chann.get_seed())
        
        # Set new BER
        self.sim_conf.new_ber()
        
        # Test new BER
        self.assertEqual(1,self.sim_conf.get_ber_count())
        self.assertEqual(self.par.p[1],self.sim_conf.chann.get_p_val())
        
    def test_new_seed(self):
        self.sim.new_seed()
        self.assertEqual(1,self.sim.get_seed_count())
        self.assertTrue(self.sim.station.get_seed() == self.par.seeds[1])
        self.assertTrue(self.sim.chann.get_seed() == self.par.seeds[1])
        
    def test_new_ber(self):
        self.sim.new_ber()
        self.assertEqual(1,self.sim.get_ber_count())
        self.assertTrue(self.sim.chann.get_p_val() == self.par.p[1])
        
    def test_simulate(self):
        self.sim.simulate()
        self.sim_const.simulate()
        
    def test_conf_simulate(self):
        # Create thread with constant confidence and range of 1% of mean
        self.par.simulation_type = SimType.FIXED_CONF
        self.par.conf_range = 0.01
        conf_figs_dir = "test_figs/conf1_"
        self.sim_conf = SimulationThread(self.par,conf_figs_dir)
        
        # Simulate              
        self.sim_conf.simulate()
        
        # Create thread with constant confidence and range of 5% of mean
        self.par.conf_range = 0.05
        conf_figs_dir = "test_figs/conf2_"
        self.sim_conf = SimulationThread(self.par,conf_figs_dir)
        
        # Simulate              
        self.sim_conf.simulate()
    
if __name__ == '__main__':
    unittest.main()