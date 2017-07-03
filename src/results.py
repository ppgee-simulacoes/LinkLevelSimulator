# -*- coding: utf-8 -*-
"""
Results class: saves and plots results.

Created on Thu Mar 30 16:41:59 2017

@author: Calil
"""

import numpy as np
import matplotlib.pyplot as plt
from input_output import InputOutput

class Results(object):
    
    def __init__(self, param, figs_dir):
        """
        Class constructor. Defines attributes:
            self.__param -- simulation parameters class
            self.__figs_dir -- figures directory
            self.__ber_list -- list of BER mean values
            self.__ber_conf_list -- list of BER confidences
            self.__per_list -- list of PER mean values
            self.__per_conf_list -- list of PER confidences
            self.__thrpt_list -- list of Throughput mean values
            self.__thrpt_conf_list -- list of Throughput confidences
            
        Keyword parameters:
            param -- Parameters class
            figs_dir -- string of figures directory
        """
        self.__param = param
        self.__figs_dir = figs_dir
        self.__ber_list = []
        self.__ber_conf_list = []
        self.__per_list = []
        self.__per_conf_list = []
        self.__thrpt_list = []
        self.__thrpt_conf_list = []
        pass
    
    def get_param(self):
        """Getter for parameters."""
        return self.__param
    
    def get_figs_dir(self):
        """Getter for figures directory string."""
        return self.__figs_dir

    def get_ber_list(self):
        """Getter for BER mean value list."""
        return self.__ber_list

    def set_ber_list(self, ber):
        """Getter for BER mean value list."""
        self.__ber_list = ber

    def get_ber_conf(self):
        """Getter for BER confidence delta list."""
        return self.__ber_conf_list

    def set_ber_conf(self, ber_conf):
        """Setter for PER confidence delta list."""
        self.__ber_conf_list = ber_conf

    def get_per_list(self):
        """Getter for PER mean value list."""
        return self.__per_list

    def set_per_list(self, per):
        """Setter for PER mean value list."""
        self.__per_list = per
    
    def get_per_conf(self):
        """Getter for PER confidence delta list."""
        return self.__per_conf_list

    def set_per_conf(self, per_conf):
        """Setter for PER confidence delta list."""
        self.__per_conf_list = per_conf

    def get_thrpt_list(self):
        """Getter for Throughput mean value list."""
        return self.__thrpt_list

    def set_thrpt_list(self, thrpt):
        """Setter for Throughput mean value list."""
        self.__thrpt_list = thrpt
    
    def get_thrpt_conf(self):
        """Getter form Throughput confidence delta list."""
        return self.__thrpt_conf_list

    def set_thrpt_conf(self, thrpt_conf):
        """Getter form Throughput confidence delta list."""
        self.__thrpt_conf_list = thrpt_conf

    def store_res(self, results):
        """
        Stores BER, PER and Throughput for future ploting.
        
        Keyword parameters:
            per -- tuple containg PER mean value and confidence delta
            thrpt -- tuple containing Tput mean value and confidence delta
        """

        ber_mean, ber_conf = zip(*results[0])
        per_mean, per_conf = zip(*results[1])
        thrpt_mean, thrpt_conf = zip(*results[2])

        self.set_ber_list(ber_mean)
        self.set_ber_conf(ber_conf)
        self.set_per_list(per_mean)
        self.set_per_conf(per_conf)
        self.set_thrpt_list(thrpt_mean)
        self.set_thrpt_conf(thrpt_conf)

        # Saving results in a file
        io = InputOutput()
        filename = 'Results.csv'
        fieldnames = ['BER MEAN', 'BER CONF', 'PER MEAN', 'PER CONF', 'THRPT MEAN', 'THRPT CONF', '', '', '', '']
        fieldvalues = [ber_mean, ber_conf, per_mean, per_conf, thrpt_mean, thrpt_conf, '', '', '', '']
        io.write_csv_file(filename, fieldnames, fieldvalues)

    def plot(self, theo_ber, theo_per, theo_thrpt):
        """
        Plots PER vs p and Throughput vs p simulation results.
        
        Keyword parameters:
            theo_per -- theoretical PER numpy array
            theo_thrpt -- theoretical Throughput numpy array
        """
        # PLOT BER
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(111)

        np_ber = np.array(self.get_ber_list())
        np_ber_conf = np.array(self.get_ber_conf())

        ax1.set_yscale('log')
        ax1.errorbar(self.get_param().ebn0, np_ber, yerr=np_ber_conf, fmt='o')
        ax1.plot(self.get_param().ebn0, theo_ber, 'r', linewidth=0.5)

        ax1.grid()

        ax1.set_xlabel("Eb/N0")
        ax1.set_ylabel("Bit Error Rate")

        # Save and show
        file_name = self.get_figs_dir() + "ber.png"
        plt.savefig(file_name)
        plt.show()

        # PLOT PER
        fig = plt.figure(figsize=(10,10))
        ax1 = fig.add_subplot(111)
        
        np_per = np.array(self.get_per_list())
        np_per_conf = np.array(self.get_per_conf())

        ax1.set_yscale('log')
        ax1.errorbar(self.get_param().ebn0,np_per,yerr = np_per_conf,fmt = 'o')
        ax1.plot(self.get_param().ebn0,theo_per,'r',linewidth = 0.5)
        
        ax1.grid()

        ax1.set_xlabel("Eb/N0")
        ax1.set_ylabel("Packet Error Rate")
        
        #Save and show
        file_name = self.get_figs_dir() + "per.png"
        plt.savefig(file_name)
        plt.show()
        
        # PLOT THROUGHPUT
        fig = plt.figure(figsize=(10,10))
        ax1 = fig.add_subplot(111)
        
        np_thrpt = np.array(self.get_thrpt_list())
        np_thrpt_conf = np.array(self.get_thrpt_conf())
        
        ax1.errorbar(self.get_param().ebn0,np_thrpt,yerr = np_thrpt_conf\
                     ,fmt = 'o')
        ax1.plot(self.get_param().ebn0,theo_thrpt,'r',linewidth = 0.5)
        
        ax1.grid()
        
        ax1.set_xlabel("Eb/N0")
        ax1.set_ylabel("Throughput [Mbps]")
        
        #Save and show
        file_name = self.get_figs_dir() + "thrpt.png"
        plt.savefig(file_name)
        plt.show()