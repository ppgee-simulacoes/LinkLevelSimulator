# -*- coding: utf-8 -*-
"""
Results class: saves and plots results.

Created on Thu Mar 30 16:41:59 2017

@author: Calil
"""

import numpy as np
import matplotlib.pyplot as plt

class Results(object):
    
    def __init__(self,param,figs_dir):
        """
        Class constructor. Defines attributes:
            self.__param -- simulation parameters class
            self.__figs_dir -- figures directory
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
    
    def get_per_list(self):
        """Getter for PER mean value list."""
        return self.__per_list
    
    def get_per_conf(self):
        """Getter for PER confidence delta list."""
        return self.__per_conf_list
    
    def get_thrpt_list(self):
        """Getter for Throughput mean value list."""
        return self.__thrpt_list
    
    def get_thrpt_conf(self):
        """Getter form Throughput confidence delta list."""
        return self.__thrpt_conf_list
    
    def store_res(self,per,thrpt):
        """
        Stores PER and Throughput for future ploting.
        
        Keyword parameters:
            per -- tuple containg PER mean value and confidence delta
            thrpt -- tuple containing Tput mean value and confidence delta
        """
        self.get_per_list().append(per[0])
        self.get_per_conf().append(per[1])
        self.get_thrpt_list().append(thrpt[0])
        self.get_thrpt_conf().append(thrpt[1])
    
    def plot(self,theo_per,theo_thrpt):
        """
        Plots PER vs p and Throughput vs p simulation results.
        
        Keyword parameters:
            theo_per -- theoretical PER numpy array
            theo_thrpt -- theoretical Throughput numpy array
        """
        # PLOT PER
        fig = plt.figure(figsize=(10,10))
        ax1 = fig.add_subplot(111)
        
        np_per = np.array(self.get_per_list())
        np_per_conf = np.array(self.get_per_conf())
        
        ax1.set_xscale('log')
        ax1.errorbar(self.get_param().p,np_per,yerr = np_per_conf,fmt = 'o')
        ax1.plot(self.get_param().p,theo_per,'r',linewidth = 0.5)
        
        ax1.grid()
        
        ax1.set_xlabel("Bit Error Rate")
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
        
        ax1.set_xscale('log')
        ax1.errorbar(self.get_param().p,np_thrpt,yerr = np_thrpt_conf\
                     ,fmt = 'o')
        ax1.plot(self.get_param().p,theo_thrpt,'r',linewidth = 0.5)
        
        ax1.grid()
        
        ax1.set_xlabel("Bit Error Rate")
        ax1.set_ylabel("Throughput [Mbps]")
        
        #Save and show
        file_name = self.get_figs_dir() + "thrpt.png"
        plt.savefig(file_name)
        plt.show()