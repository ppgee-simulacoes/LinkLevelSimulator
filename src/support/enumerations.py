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
    BSC = 1
    
    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


class BSCType(Enum):
    """
    Types of Binary Symmetric Channel
    """
    CONSTANT = 0
    MARKOV = 1

    def __eq__(self, other):
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
    
class ModType(Enum):
    """
    Supported modulations
    """
    PSK = 0
    QAM = 1
    CUSTOM = 2
    
    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented