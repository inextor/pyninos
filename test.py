#!/bin/python3

import sys
import random

from bits_analytics import BitsAnalytics

"""Data analytics"""

def generate_norm_dic():

    dic = {
        'zero': [],
        'one': [],
        'reverse_zero': [],
        'reverse_one': [],
        'last': []
    }

    for i in range(0, 256):
        dic['last'].append(i & 1)
        dic['reverse_zero'].append(0)
        dic['reverse_one'].append(0)

    previous0 = False
    previous1 = True

    bits = []
    for i in range(0, 8):
        bits.append(1 >> (7-i))

    for i in range(0, 256):
        previous0 = False
        previous1 = True

        zero_value = 0
        one_value = 0

        for bit_value in bits:
            current_bit = bit_value & i > 0

            if previous0 != current_bit:
                zero_value += bit_value

            if previous1 != current_bit:
                one_value += bit_value

            previous0 = current_bit
            previous1 = current_bit

        dic['zero'].append(zero_value)
        dic['one'].append(one_value)

        dic['reverse_zero'][zero_value] = i
        dic['reverse_one'][one_value] = i

    return dic


def transform_bytes(byte_list, dictionary, is_reverse):
    new_values = []
    previous = False
    zero_index = 'reverse_zero' if is_reverse else  'zero'
    one_index = 'reverse_one' if is_reverse else 'one'

    for byte_v in byte_list:
        replacement = dictionary[one_index][byte_v] if previous else dictionary[zero_index][byte_v]
        new_values.append(replacement)
        previous = dictionary['last'][replacement if is_reverse else byte_v]

    return new_values


def test_transform():
    total = 1024

    rand_list = []
    print(rand_list, ", ")
    for i in range(0, total):
        ##rand_list.append(i)
        rand_list.append(random.randrange(0, 256))

    ba = BitsAnalytics()
    ba.process_list(rand_list)
    ba.printx()


    dic = generate_norm_dic()
    norm_list = transform_bytes(rand_list, dic, False)
    #print("byte_list", norm_list)
    original = transform_bytes(norm_list, dic, True)
    #print("result", original)

    for i in range(0, total):
        if rand_list[i] != original[i]:
            raise Exception("Doenst work")

if __name__ == "__main__":
    test_transform()
