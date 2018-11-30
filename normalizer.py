"""This Module is to enable infinite compression"""

import random




class Compress:
    """format a random byte string to compress or decompress"""
    def __init__(self, is_to_compress):
        self.is_to_compress = is_to_compress
        self.previous = 0
        self.dictionary = self.get_dictionary()

    def process(self, byte):
        """Prepare a byte to be compressed or decompressed"""
        to_write = self.dictionary[self.previous][byte]

        if self.is_to_compress:
            self.previous = byte
        else:
            self.previous = to_write

        return to_write

    def get_dictionary(self):
        to_compress = []
        to_decompress = []

        for i in range(0, 256):
            to_compress.append([])
            to_decompress.append([0]*256)

        for i in range(0, 256):
            for j in range(0, 256):
                if (j-i) < 0:
                    to_compress[i].append(256+(j-i))
                    to_decompress[i][256+(j-i)] = j
                else:
                    to_compress[i].append(j-i)
                    to_decompress[i][(j-i)] = j

        return to_compress if self.is_to_compress else to_decompress


def test_transform():
    """Test the class"""
    test_list = []

    for i in range(0, 10):
        test_list.append(random.randrange(0, 256))

    compress = Compress(True)
    decompress = Compress(False)

    new_list = []
    original_list = []

    for i in test_list:
        new_list.append(compress.process(i))

    for i in new_list:
        original_list.append(decompress.process(i))

    print("Test list", test_list)
    print("Compressed", new_list )
    print("Uncompress", original_list)

    for i in range(0, len(test_list)):
        if original_list[i] != test_list[i]:
            raise Exception("DOes'tn work")


if __name__ == "__main__":
    #test_transform( True )
    test_transform()
