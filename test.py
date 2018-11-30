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
        bits.append(1 << (7-i))

    for i in range(0, 256):
        previous0 = False
        previous1 = True

        zero_value = 0
        one_value = 0

        for bit_value in bits:
            current_bit = ( bit_value & i ) > 0

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


def test_transform(debug):

    rand_list = []

    for i in range(0, 256):
        rand_list.append(i)

    ba = BitsAnalytics()
    ba.process_list(rand_list)
    ba.printx()

    dic = generate_norm_dic()

    print("dictionary",dic)

    norm_list = transform_bytes(rand_list, dic, False)
    original = transform_bytes(norm_list, dic, True)

    if debug:
        print("byte_list", rand_list )
        print("norm list", norm_list)
        print("result", original)

    for i in range(0, 256):
        if rand_list[i] != original[i]:
            raise Exception("Doenst work")

    ba = BitsAnalytics()
    ba.process_list(norm_list)
    image_string = ba.generate_pbm_image( norm_list, 1000 )
    ba.printx()

    text_file = open("image.pbm", "w")
    text_file.write(image_string)
    text_file.close()


def test_transform_random():
    total = 4096
    dic = generate_norm_dic()
    rand_list = []

    for i in range(0, total):
        rand_list.append( random.randrange(0,256) )

    norm_list = transform_bytes(rand_list, dic, False)
    original = transform_bytes( norm_list, dic, True )
    print("byte_list", norm_list)
    print("result", original)

    for i in range(0, total):
        if rand_list[i] != original[i]:
            raise Exception("Doenst work")

    ba = BitsAnalytics()
    ba.process_list(norm_list)
    ba.printx()


    image_string = ba.generate_bars_image( ba.byte_diff )

    text_file = open("image.pgm", "w")
    text_file.write( image_string )
    text_file.close()


if __name__ == "__main__":
    #test_transform( True )
    test_transform_random()
