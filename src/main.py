# -*- coding: utf-8 -*-
"""
Main script.

Created on Mon Apr  3 20:35:22 2017

@author: Calil
"""

from parameters.parameters import Parameters
from simulation_thread import SimulationThread

figs_dir = "figs/"

param = Parameters(1)
sim_thread = SimulationThread(param,figs_dir)

sim_thread.simulate()