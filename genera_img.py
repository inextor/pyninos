"""Bynary Data visualization"""

import sys


def genera_img(filename):
    """genera_img Generate a image of the binary data of the filename"""
    print("P1\n1024\n1024")

    lines = []
    counter = 0

    with open(filename, 'rb') as file_descriptor:
        byte_list = file_descriptor.read()

    for i in byte_list:
        counter += 1

        for zero_eight in range(0, 8):
            current = ((1 <<  zero_eight) & i) > 0

            if current:
                lines.append(1)
            else:
                lines.append(0)

        if counter >= 128:
            print('\t'.join(map(str, lines)))
            lines.clear()
            counter = 0

if __name__ == "__main__":
    genera_img(sys.argv[1])
