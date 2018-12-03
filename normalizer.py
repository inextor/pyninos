"""This Module is to enable infinite compression"""

import random
import sys


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

    def process_list(self, byte_list, result):

        size = len(byte_list)

        for b in range(0,size):
            result[b] = self.process(byte_list[b]);

        return result

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

    is_to_compress = True
    is_test = False

    if( len( sys.argv ) > 1 ):
        #print(">2")
        if(sys.argv[1].find('-') != -1):
            #print("------")
            if(sys.argv[1].find('d') != -1 ):
                is_to_compress = False
                #print("is decompress")
            if(sys.argv[1].find('t') != -1 ):
                is_test = True
                #print("is test")

    if( is_test ):
        test_transform()
        sys.exit()

    size = 1024*1024*2
    compressor = Compress( is_to_compress )
    data = sys.stdin.buffer.read(size)
    result = bytearray( size )
    readed_size = len(data)

    while readed_size != 0:
        compressor.process_list(data, result)
        sys.stdout.buffer.write( result[:readed_size] )
        data = sys.stdin.buffer.read(size)
        readed_size = len( data )

