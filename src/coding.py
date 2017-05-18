# -*- coding: utf-8 -*-
"""
Source class: encodes and decodes using Hamming Code.

Created on Sun May 14 10:00:08 2017

@author: Guilherme
"""

import numpy as np
import random


class Coding(object):
    def __init__(self, coding_process, matrix_dimensions, generation_matrix):
        """
        Class constructor.

        Keyword arguments:
            coding_process -- indicates if the generation uses a random table, 
                              one of the pre-defined matrixes or a user-provided one.
            matrix_dimensions -- array with two quantities: number of message bits and number of code bits
            generation_matrix -- in case of the user is supposed to provide the generation matrix
        """

        # Pre-defined generation matrixes

        self.__coding_process = coding_process
        self.__message_size = matrix_dimensions[0]
        self.__codeword_size = matrix_dimensions[1]
        if self.__coding_process == 1:  # random matrix
            self.__coding_table = self.generate_table(self.__message_size, self.__codeword_size)
        elif self.__coding_process == 2:  # pre-defined matrix
            self.__coding_table = self.get_pre_defined_table(self.__message_size, self.__codeword_size)
        else:  # user-provided matrix
            self.__coding_table = self.get_user_defined_table(self.__message_size, self.__codeword_size,
                                                              generation_matrix)

    def generate_table(self, k, n):
        """Generates a random codeword table"""

        table = np.random.choice(2 ** n, 2 ** k, replace=False)

        return table

    def get_pre_defined_table(self, k, n):
        """Returns a pre-defined codeword table."""

        if k == 4:
            generation_matrix = np.array([[1, 0, 0, 0, 1, 1, 0],
                                          [0, 1, 0, 0, 0, 1, 1],
                                          [0, 0, 1, 0, 1, 0, 1],
                                          [0, 0, 0, 1, 1, 1, 1]])
        else:
            generation_matrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                                          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                                          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                                          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                                          [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                                          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
                                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                                          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]])

        return self.convert_matrix_to_table(k, n, generation_matrix)

    def get_user_defined_table(self, k, n, generation_matrix):
        """Returns a user-defined codeword table."""

        return self.convert_matrix_to_table(k, n, generation_matrix)

    def convert_matrix_to_table(self, k, n, generation_matrix):

        table = np.zeros(2 ** k, int)

        for index in range(2 ** k):
            bit_array = self.dec2bitarray(index, k)
            codeword_array = np.ravel(np.mat(bit_array) * np.mat(generation_matrix))
            for index_2 in range(n):
                codeword_array[index_2] = codeword_array[index_2] % 2
            codeword_int = self.bitarray2dec(codeword_array)
            table[index] = codeword_int

        return table

    def get_codeword_table(self):

        return self.__coding_table

    def encode(self, in_bits):

        remainder = len(in_bits) % self.__message_size
        padded_in_bits = in_bits
        if remainder > 0:
            padded_in_bits = np.append(padded_in_bits, np.zeros(self.__message_size - remainder))

        number_of_msg_words = int(len(padded_in_bits) / self.__message_size)
        msg_words_array = np.reshape(padded_in_bits, [number_of_msg_words, self.__message_size])

        msg_words_array_dec = np.array([self.bitarray2dec(msg_words_array[j, :]) \
                                        for j in range(number_of_msg_words)])
        coded_words_array_dec = np.zeros(number_of_msg_words, int)
        table = self.get_codeword_table()
        for index in range(number_of_msg_words):
            coded_words_array_dec[index] = table[int(msg_words_array_dec[index])]

        coded_words_array = np.empty([number_of_msg_words, self.__codeword_size], int)
        for index in range(number_of_msg_words):
            coded_words_array[index] = self.dec2bitarray(coded_words_array_dec[index], self.__codeword_size)

        return coded_words_array.ravel()

    def dec2bitarray(self, in_decimal, bit_number):
        """
        Code adapted from: https://github.com/veeresht/CommPy
        """
        bit_array = np.zeros(bit_number, int)
        indice = bit_number - 1

        while in_decimal > 0:
            remainder = int(in_decimal % 2)
            if remainder > 0:
                bit_array[indice] = remainder
            in_decimal = int(in_decimal / 2)
            indice = indice - 1

        return bit_array

    def bitarray2dec(self, in_bitarray):
        """
        Code adapted from: https://github.com/veeresht/CommPy
        """
        number = 0

        for i in range(len(in_bitarray)):
            number = number + in_bitarray[i] * (2 ** (len(in_bitarray) - 1 - i))

        return number