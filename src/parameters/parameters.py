# -*- coding: utf-8 -*-
"""
Parameters class.
Code adapted from: https://github.com/SIMULATOR-WG/SHARC

Created on Thu Mar 30 16:32:35 2017

@author: Calil
"""

import numpy as np
from support.enumerations import ChannelModel
from support.enumerations import BSCType
from support.enumerations import SimType
from support.enumerations import ModType

class Parameters(object):
    
    __instance = None
    
        
    def __new__(cls, val):
        """
        This is the Singleton Pattern to ensure that this class will have only one instance
        """        
        if Parameters.__instance is None:
            Parameters.__instance = object.__new__(cls)
        Parameters.__instance.val = val
        return Parameters.__instance    
    
    #########################################################################
    # SIMULATION PARAMETERS
    
    '''
    Simulation type:
        FIXED_SEEDS -- Simulate for given seeds and calculate confidence 
                       interval
        FIXED_CONF  -- Simulate multiple seeds util a confidence interval is
                       reached
    '''
    simulation_type = SimType.FIXED_SEEDS

    # Maximum number of simulation drops
    max_drops = 25

    # Seeds: used if self.simulation_type == SimType.FIXED_SEEDS
    seeds_flt = np.random.randint(2, 10051651, size=max_drops)
    seeds = seeds_flt.astype(int)
    
    # Confidence range: used if self.simulation_type = SimType.FIXED_CONF
    # Confidence interval  = (mean - h, mean + h)
    # h = conf_range * mean
    conf_range = 0.1
    
    # Confidence
    conf = 0.95
    
    # Number of transmitted packets
    n_pcks = 30
    
    # Warm-up: number of discarted packets at the beginning of iteration
    n_warm_up_pcks = 0
    
    # TRANSMISSION PARAMETERS
    
    # Number of bits per packet
    n_bits = 1000

    # Transmission rate [Mbps]
    tx_rate = 50
    
    # CHANNEL PARAMETERS

    # SNR Levels
    ebn0 = np.linspace(0, 10, num=11)

    # Channel model
    chan_mod = ChannelModel.IDEAL
    if chan_mod == ChannelModel.BSC:
        bsc_type = BSCType.MARKOV

    
    # Fixed log10(BER) = p
    '''
    This BER is used for the Constant channel and for state two of
    the Markov channel
    '''
    p = np.logspace(-6,-4, num = 20)
    
    # Markov Channel Transition Matrix
    '''
    If chan_mod != ChannelModel.MARKOV, these parameters are not considered.
    States:
        0: Good -> BER = 0
        1: Bad  -> BER = 0.5
        2: Ugly -> BER = p
        
        | P00 P01 P02 |
    T = | P10 P11 P12 |
        | P20 P21 P22 |
    '''
    # Line zero
    P00 = 0.1
    P01 = 0
    
    # Line one
    P10 = 0
    P11 = 0.01
    
    # Line two
    P20 = 0.1
    P21 = 0.05
    
    # Buiuld the transition matrix
    P02 = 1 - P00 - P01
    P12 = 1 - P10 - P11
    P22 = 1 - P20 - P21
    
    transition_mtx = np.matrix([[P00, P01, P02], [P10, P11, P12],[P20, P21, P22]])
    
    # MODULATION PARAMETERS
    
    # Modulation order
    mod_order = 2
    
    # Modulation type
    mod_type = ModType.PSK
    
    # Custom modulation type
    if mod_type == ModType.CUSTOM:
        constellation = np.array([1+0j, -1+1j, -1+0j, -1-1j])
        
    # Symbol normalization
    symbol_norm = False
    
    # Padding
    symbol_pad = False
    
    # RRC Filter span in symbols
    filter_span = 6
    
    # RRC Filter rolloff factor
    roll_off = 0.3
    
    # Symbol time [s]
    symbol_time = 1e-4
    
    # Sampling frequency [Hz]
    sample_frequency = 2e5

    # CODING PARAMETERS

    # Coding Process
    coding_process = 2

    # Matrix dimensions
    mtx_code_dim = [4, 7]

    # FADING PARAMETERS

    # Doppler frequency [Hz]
    doppler_freq = 100
    
    # Number of scatterers
    m = 10

    #Jake's Model parameter -  Rayleigh Fading
    k = 2

    # Time
    time = 1/sample_frequency


    # PSD PLOTTING OPTION
    plot_psd = False
    