import random

def compress_positions(pos_list):
    cp_pos_list = pos_list.copy()
    new_pos = []

    for i in range(0,len(pos_list)):
        for index,value in enumerate(cp_pos_list):
            if i == value:
                new_pos.append(index)
                cp_pos_list.pop(index)
                break

    return new_pos


def decompress_positions(pos_list):

    cp_pos_list = pos_list.copy()

    new_pos = [-1]*len(pos_list)

    for value in range(0, len(pos_list)):

        compressed_position = cp_pos_list.pop(0)
        counter = 0

        for index in range(0, len(new_pos)):
            final_value = new_pos[index]

            if counter == compressed_position and final_value == -1:
                new_pos[index] = value
                break

            if final_value == -1:
                counter += 1

    return new_pos

def test():
    test_list = []

    for i in range(0, 256):
        test_list.append(i)

    test_list.reverse()

    print("test list", test_list)
    compressed_list = compress_positions(test_list)
    print("compressed", compressed_list)
    uncompressed_list = decompress_positions(compressed_list)
    print("uncompressed list", uncompressed_list)



    random.shuffle( test_list )

    print("test list", test_list)
    compressed_list = compress_positions(test_list)
    print("compressed", compressed_list)
    uncompressed_list = decompress_positions(compressed_list)
    print("uncompressed list", uncompressed_list)




    for i in range(0, 256):
        if test_list[i] != uncompressed_list[i]:
            raise Exception("Doesnt work")

    print("\n\n\n")

    test_list = []
    for i in range(0, 10):
        test_list.append(i)

    random.shuffle(test_list)
    print("test list", test_list)
    compressed_list = compress_positions(test_list)
    print("compressed", compressed_list)
    uncompressed_list = decompress_positions(compressed_list)
    print("uncompressed list", uncompressed_list)


if __name__ == "__main__":
    test()
