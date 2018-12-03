"""Compress a string"""
import sys
import io

def compress_positions(pos_list):
    """Normalize a position list"""
    cp_pos_list = pos_list.copy()
    new_pos = []

    for i in range(0, len(pos_list)):
        for index, value in enumerate(cp_pos_list):
            if i == value:
                new_pos.append(index)
                cp_pos_list.pop(index)
                break

    return new_pos

def decompress_positions(pos_list):
    """Unormalize position list"""

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

class Compressor:
    """This class helps to count bits and bytes"""

    def __init__(self, is_to_compress):
        self.byte_counter = [0]*256
        self.byte_diff = [0]*256
        self.total = 0
        self.byte_previous = 0
        self.byte_transitions = []
        self.is_to_compress = is_to_compress
        self.transitions_dictionary = None
        self.debug = False

        for i in range(0, 256):
            self.byte_transitions.append([0]*256)

    def generate_pos_dictionary(self):
        """generate a transition position dictionary"""
        dictionary = [0]*256

        for index_array in self.byte_transitions:
            sorted_indexes = index_array.copy()
            sorted_indexes.sort(reverse=True)

            for index, value in enumerate(sorted_indexes):
                dictionary[index] += value

        return dictionary

    def create_transition_dictionary(self):
        """Generates the transition dictionary"""

        positions_dictionary = []

        for index in range(0, 256):
            positions_dictionary.append([])

            for j in range(0, 256):
                positions_dictionary[index].append({
                    "value":j,
                    "freq": self.byte_transitions[index][j]
                    })

            ##Si ya se reviso todo y sigue estando mal puede ser esto
            #el orden no quedo igual entre el prime sort y el segundo sorg

            positions_dictionary[index].sort(key=lambda e: e["freq"], reverse=True)

            for j in range(0, 256):
                positions_dictionary[index][j]["index"] = j

            #Segundo Sort
            positions_dictionary[index].sort(key=lambda e: e["value"])

        self.transitions_dictionary = positions_dictionary

    def analyze(self, byte_value):
        """Process one byte"""
        self.total += 1

        self.byte_counter[byte_value] += 1

        max_val = max(self.byte_previous, byte_value)
        min_val = min(self.byte_previous, byte_value)
        self.byte_diff[max_val-min_val] += 1

        self.byte_transitions[self.byte_previous][byte_value] += 1
        self.byte_previous = byte_value

    def analyze_list(self, byte_list):
        """Process a list of bytes"""
        for byte_data in byte_list:
            self.analyze(byte_data)

        self.create_transition_dictionary()


    def read_dictionary_from_buffer(self, a_buffer):
        """Read dictionary from a buffer"""
        new_dictionary = []

        sys.stderr.write("Reading dictionaries\n")

        for i in range(0, 256):
            new_dictionary.append([])
            dictionary_index = a_buffer.read(256)

            for index, value in enumerate(dictionary_index):
                new_dictionary[i].append({
                    "value":index,
                    "freq":value,
                    "index":value
                })

            if self.debug and i < 5:
                dict_list = []

                for dic_index in range(0, 20):
                    dict_list.append(new_dictionary[i][dic_index]["freq"])

                sys.stderr.write(str(dict_list)+"\n")

            new_dictionary[i].sort(key=lambda e: e["index"])

        sys.stderr.write("End reading dictionary")
        self.transitions_dictionary = new_dictionary

    def read_dictionary_alt(self, a_buffer):
        """Read dictionary from a buffer"""
        new_dictionary = []

        sys.stderr.write("Reading dictionaries\n")

        for i in range(0, 256):
            new_dictionary.append([])
            unormalized_byte_list = a_buffer.read(256)
            unormal_list = []

            for k in unormalized_byte_list:
                unormal_list.append(k)

            dictionary_index = decompress_positions(unormal_list)

            for index, value in enumerate(dictionary_index):
                new_dictionary[i].append({
                    "value":index,
                    "freq":value,
                    "index":value
                })

            if self.debug and i < 5:
                dict_list = []

                for dic_index in range(0, 20):
                    dict_list.append(new_dictionary[i][dic_index]["freq"])

                sys.stderr.write(str(dict_list)+"\n")

            new_dictionary[i].sort(key=lambda e: e["index"])

        sys.stderr.write("End reading dictionary")
        self.transitions_dictionary = new_dictionary

    def write_dictionary_alt(self, a_buffer):
        """write dictionary to stdout"""
        for dic_index, dictionary in enumerate(self.transitions_dictionary):
            #dictionary.sort(key=lambda e: e["value"])

            if self.debug and dic_index < 5:
                dic_el = []
                for ele in dictionary:
                    dic_el.append(ele["index"])

                sys.stderr.write("Elements\n")
                sys.stderr.write(str(dic_el[0:20])+"\n")

            byte_list = []
            for obj in dictionary:
                byte_list.append(obj["index"])

            n_list = compress_positions(byte_list)
            a_buffer.write(bytearray(n_list))


    def write_dictionary_to_buffer(self, a_buffer):
        """write dictionary to stdout"""
        for dic_index, dictionary in enumerate(self.transitions_dictionary):
            #dictionary.sort(key=lambda e: e["value"])

            if self.debug and dic_index < 5:
                dic_el = []
                for ele in dictionary:
                    dic_el.append(ele["index"])

                sys.stderr.write("Elements\n")
                sys.stderr.write(str(dic_el[0:20])+"\n")

            byte_list = []
            for obj in dictionary:
                byte_list.append(obj["index"])

            a_buffer.write(bytearray(byte_list))

    def decompress_buffer(self, byte_list, a_buffer):
        """compress to a buffer"""
        result = []
        byte_previous = 0
        next_byte = 0
        dictionary = self.transitions_dictionary

        for index in byte_list:
            next_byte = dictionary[byte_previous][index]["value"]
            result.append(next_byte)
            byte_previous = next_byte

        if self.debug:
            sys.stderr.write("First 20 decompressed bytes")
            sys.stderr.write(str(result[0:20])+"\n")

        a_buffer.write(bytearray(result))


    def compress_buffer(self, byte_list, a_buffer):
        """Process to compress the byte list and writes to a buffer"""


        if self.debug:
            sys.stderr.write("First 20 to compressed bytes")
            tmp_list = []
            for i in range(0, 20):
                tmp_list.append(byte_list[i])

            sys.stderr.write(str(tmp_list)+"\n")
            sys.stderr.write("----")

        self.analyze_list(byte_list)
        dictionary = self.transitions_dictionary
        result = []

        self.write_dictionary_alt(a_buffer)

        byte_previous = 0
        next_byte = 0

        for i in byte_list:
            result.append(dictionary[byte_previous][i]["index"])
            byte_previous = i


        if self.debug:
            sys.stderr.write("First 20 compressed bytes")
            sys.stderr.write(str(result[0:20])+"\n")
            sys.stderr.write("----")

        a_buffer.write(bytearray(result))

if __name__ == "__main__":

    is_to_compress = True
    is_test = False

    if len( sys.argv ) > 1:
        if(sys.argv[1].find('-') != -1):
            if(sys.argv[1].find('d') != -1):
                is_to_compress = False
            if(sys.argv[1].find('t') != -1):
                is_test = True
                sys.stderr.write("is test\n")

    compressor = Compressor(is_to_compress)
    compressor.debug = True

    if is_test:
        output= io.BytesIO()
        #2, 0, 1, 3, 4
        data = [1,1,1,0,1,0,2,0,1,1,1,1,1,1,0,1,0,2,0,1,1,1,1,1,1,0,1,0,2,0,1,1,1]
                #0, 0, 0, 1, 0, 1, 1 ,0 ,0
                #0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0]

        compressor.is_debug = True
        compressor.compress_buffer(data, output)
        #z = output.read()
        #tmp_list = []
        #for i in range(0, len(z)):
        #    tmp_list.append(z[i])


        sys.stderr.write("decompressin\n")
        #compressor = Compressor(False)
        compressor.debug = True
        output= io.BytesIO()
        data = [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0]

        for freq_dic in compressor.transitions_dictionary:
            freq_dic.sort(key=lambda e: e["freq"], reverse=True)

        compressor.decompress_buffer(data, output)
        sys.exit()

    if is_to_compress:
        #buffer_size = 1024*1024*2
        data = sys.stdin.buffer.read()
        compressor.compress_buffer(data, sys.stdout.buffer)
    else:
        compressor.read_dictionary_alt(sys.stdin.buffer)
        data = sys.stdin.buffer.read()
        compressor.decompress_buffer(data, sys.stdout.buffer)

    #readed_size = len(data)

    #while readed_size != 0:
    #    compressor.process_list(data)
    #    data = sys.stdin.buffer.read(buffer_size)
    #    readed_size = len(data)

#4 bites long filesize
#256 #1=>dic size or 0=indicates full dictionary
#256 Dictionario 8 Bits ó n bytes as dictionary
#positiones based on dictionary full file
#
