# -*- coding: utf-8 -*-
"""
Enumerations used in the project.

Created on Sun Mar 26 12:06:35 2017

@author: Calil
"""

from enum import Enum

class ChannelModel(Enum):
    """
    Types of channel model
    """
    IDEAL = 0
    CONSTANT = 1
    MARKOV = 2
    
    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    
class SimType(Enum):
    """
    Types of simulation.
    """
    FIXED_SEEDS = 0
    FIXED_CONF = 1
    
    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented