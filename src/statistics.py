# -*- coding: utf-8 -*-
"""
Statistics class: computes simulation statistics

Created on Tue Mar 28 10:29:08 2017

@author: Calil
"""

import numpy as np
import scipy.stats as sp


class Statistics(object):
    def __init__(self, snr_array, n_bits, tx_rate, conf=0.95):
        self.__snr_size = len(snr_array)
        self.__conf = conf  # Confidence
        self.__n_bits = n_bits  # Number of bits per packet
        self.__tx_rate = tx_rate  # Transmission rate

        self.__pck_cnt = 0
        self.__n_pck_errors = []
        self.__n_bit_errors = []

        self.__ber_list = []
        self.__per_list = []
        self.__thrpt_list = []

        self.__criteria_per_snr = [False] * self.__snr_size
        self.__stats_results = [[None] * self.__snr_size for row in range(3)]

    def get_conf(self):
        return self.__conf

    def get_n_bits(self):
        return self.__n_bits

    def get_tx_rate(self):
        return self.__tx_rate

    def get_pck_cnt(self):
        return self.__pck_cnt

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

    def get_criteria_per_snr(self):
        return self.__criteria_per_snr

    def set_criteria_per_snr(self, criteria):
        self.__criteria_per_snr = criteria

    def get_stats_results(self):
        return self.__stats_results

    def __reset(self):
        """
        Resets number of transmitted packets and bit and packet errors at the end of
        iteration.
        """
        self.__pck_cnt = 0
        self.__n_pck_errors.clear()
        self.__n_bit_errors.clear()

    def add_new_stats(self, num_bit_errors, pck_error):
        """
        Increments number of transmitted packets and packet errors.
        
        Inputs:
            pck_error -- boolean indicating if there was a packet error
        """
        self.__n_pck_errors.append(pck_error)
        self.__n_bit_errors.append(num_bit_errors)
        self.__pck_cnt = self.__pck_cnt + 1


    def add_iteration_results(self):
        """
        Calculates BER, PER and throughput during a given iteration.
        Also saves BER, PER and throughput in their respective lists and
        finishes an iteration.
        
        Returns:
            ber -- bit error rate
            per -- packet error rate
            thrpt -- throughput      
        """

        n_bit_errors_per_snr = np.sum(np.asarray(self.get_n_bit_errors()), 0)
        ber_per_snr = n_bit_errors_per_snr / (self.get_pck_cnt()*self.get_n_bits())

        n_pck_errors_per_snr = np.sum(np.asarray(self.get_n_pck_errors()), 0)
        per_per_snr = n_pck_errors_per_snr / self.get_pck_cnt()

        time = self.get_n_bits() * self.get_pck_cnt() / (self.get_tx_rate())
        thrpt_per_snr = (self.get_pck_cnt() - n_pck_errors_per_snr) * \
                         self.get_n_bits() / time

        self.get_ber_list().append(ber_per_snr)
        self.get_per_list().append(per_per_snr)
        self.get_thrpt_list().append(thrpt_per_snr)

        self.__reset()


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
        mean_val = np.mean(data, 0)
        se = sp.sem(data, 0)
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

        ber_tpl = list(zip(ber, ber_conf))
        per_tpl = list(zip(per, per_conf))
        thrpt_tpl = list(zip(thrpt, thrpt_conf))

        return ber_tpl, per_tpl, thrpt_tpl

    def check_stats_per_snr(self, ber_tpl, per_tpl, thrpt_tpl, conf_range):

        ber_mean = np.asarray([value[0] for value in ber_tpl])
        per_mean = np.asarray([value[0] for value in per_tpl])
        thrpt_mean = np.asarray([value[0] for value in thrpt_tpl])

        ber_conf = np.asarray([value[1] for value in ber_tpl])
        per_conf = np.asarray([value[1] for value in per_tpl])
        thrpt_conf = np.asarray([value[1] for value in thrpt_tpl])

        criteria = ber_conf / ber_mean <= conf_range
        if all(self.get_criteria_per_snr()) is not True:
            self.set_criteria_per_snr(criteria.tolist())
        for idx, value in enumerate(self.get_criteria_per_snr()):
            if value is True:
                self.get_stats_results()[0][idx] = ber_tpl[idx]
                self.get_stats_results()[1][idx] = per_tpl[idx]
                self.get_stats_results()[2][idx] = thrpt_tpl[idx]
