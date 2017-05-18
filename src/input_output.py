# -*- coding: utf-8 -*-
"""
Source class: reads and write files.

Created on Wed May 03 23:45:00 2017

@author: Guilherme
"""

import csv
import numpy as np
from conda._vendor.auxlib._vendor.five import values


class InputOutput(object):
    def __init__(self):
        pass

    def write_csv_file(self, filename, fieldnames, fieldvalues):
        with open(filename, 'w') as csvfile:
#            fieldnames = ['first_name', 'last_name']
             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

             # names_row = np.empty([1])
             # values_row = np.empty([1])
             #
             # for i in range(len(fieldnames)):
             #    names_row = np.append(names_row, fieldnames[i])
             #    values_row = np.append(values_row, str(fieldvalues[i]))
             #
#             names_row = ','.join(map(str, names_row))
             writer.writeheader()
             values_string = '{' #np.str

             for index in range(len(fieldnames)):
                 values_string = values_string + str(fieldnames[index]) + ': ' + str(fieldvalues[index])
                 if index < len(fieldnames) - 1:
                     values_string = values_string + ','
             values_string = values_string + '}'
             print (values_string)
             writer.writerow(values_string)

             # writer.writerow({fieldnames[0]: fieldvalues[0],
             #                  fieldnames[1]: fieldvalues[1],
             #                  fieldnames[2]: fieldvalues[2],
             #                  fieldnames[3]: fieldvalues[3],
             #                  fieldnames[4]: fieldvalues[4],
             #                  fieldnames[5]: fieldvalues[5],
             #                  fieldnames[6]: fieldvalues[6],
             #                  fieldnames[7]: fieldvalues[7],
             #                  fieldnames[8]: fieldvalues[8],
             #                  fieldnames[9]: fieldvalues[9]})


#           writer.writerow(names_row)
#           writer.writerow(fieldnames[1]: fieldvalues[1]})
