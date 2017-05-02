# -*- coding: utf-8 -*-
"""
Statistics class: computes simulation statistics

Created on Tue Mar 28 10:29:08 2017

@author: Calil
"""

import numpy as np
import scipy.stats as sp


class Statistics(object):
    def __init__(self, n_bits, tx_rate, conf=0.95):
        self.__conf = conf  # Confidence
        self.__n_bits = n_bits  # Number of bits per packet
        self.__tx_rate = tx_rate  # Transmission rate

        self.__n_pcks = 0
        self.__n_pck_errors = 0
        self.__n_bit_errors = []

        self.__ber_list = []
        self.__per_list = []
        self.__thrpt_list = []

    def get_conf(self):
        return self.__conf

    def get_n_bits(self):
        return self.__n_bits

    def get_tx_rate(self):
        return self.__tx_rate

    def get_n_pcks(self):
        return self.__n_pcks

    def get_n_pck_errors(self):
        return self.__n_pck_errors

    def get_n_bit_errors(self):
        return self.__n_bit_errors

    def get_ber_list(self):
        return self.__ber_list

    def get_per_list(self):
        return self.__per_list

    def get_thrpt_list(self):
        return self.__thrpt_list

    def __reset(self):
        """
        Resets number of transmitted packets and bit and packet errors at the end of
        iteration.
        """
        self.__n_pcks = 0
        self.__n_pck_errors = 0
        self.__n_bit_errors.clear()

    def pck_received(self, num_bit_errors, pck_error):
        """
        Increments number of transmitted packets and packet errors.
        
        Inputs:
            pck_error -- boolean indicating if there was a packet error
        """
        self.__n_pcks = self.__n_pcks + 1
        if pck_error:
            self.__n_pck_errors = self.__n_pck_errors + 1
            self.__n_bit_errors.append(num_bit_errors)

    def calc_iteration_results(self):
        """
        Calculates BER, PER and throughput during a given iteration.
        Also saves BER, PER and throughput in their respective lists and
        finishes an iteration.
        
        Returns:
            ber -- bit error rate
            per -- packet error rate
            thrpt -- throughput      
        """
        ber = sum(self.get_n_bit_errors()) / (self.get_n_pcks()*self.get_n_bits())
        per = self.get_n_pck_errors() / self.get_n_pcks()

        time = self.get_n_bits() * self.get_n_pcks() / (self.get_tx_rate())
        thrpt = (self.get_n_pcks() - self.get_n_pck_errors()) * \
                self.get_n_bits() / time

        self.get_ber_list().append(ber)
        self.get_per_list().append(per)
        self.get_thrpt_list().append(thrpt)

        self.__reset()

        return ber, per, thrpt

    def conf_interval(self, data_in):
        """
        Calculates the confidence interval of the mean of input data.
        Code adapted from: https://tinyurl.com/pn96ntp
        
        Keyword parameters:
            data_in -- input data
            
        Returns:
            mean_val -- mean value of data
            conf_int -- distance from mean of data's confidence interval
        """
        data = np.asarray(data_in)
        N_samples = len(data)
        mean_val = np.mean(data)
        se = sp.sem(data)
        conf_int = se * sp.t.ppf((1 + self.get_conf()) / 2., N_samples - 1)

        return mean_val, conf_int

    def wrap_up(self):
        """
        Finishes a group of iterations, and calculates mean PER and Throughput.
        
        Returns:
            ber -- mean bit error rate
            ber_conf -- confidence increment for ber
            per -- mean packet error rate
            per_conf -- confidence increment for per
            thrpt -- mean throughput
            thrpt_conf -- confidence increment for thrpt
        """

        ber, ber_conf = self.conf_interval(self.get_ber_list())
        per, per_conf = self.conf_interval(self.get_per_list())
        thrpt, thrpt_conf = self.conf_interval(self.get_thrpt_list())

        ber_tpl = (ber, ber_conf)
        per_tpl = (per, per_conf)
        thrpt_tpl = (thrpt, thrpt_conf)

        self.__ber_list.clear()
        self.__per_list.clear()
        self.__thrpt_list.clear()
        self.__reset()

        return ber_tpl, per_tpl, thrpt_tpl
