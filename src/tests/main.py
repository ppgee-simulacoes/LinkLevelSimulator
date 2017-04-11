# -*- coding: utf-8 -*-
"""
Main test routine

Created on Sun Mar 26 10:29:36 2017

@author: Calil
"""

import unittest

loader = unittest.TestLoader()
tests = loader.discover('.')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)