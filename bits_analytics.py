"""This module is for bytes analitycs"""

class BitsAnalytics:
    """This class helps to count bits and bytes"""
    def __init__(self):
        self.byte_counter = [0]*256
        self.byte_diff = [0]*256
        self.bit_counter = [0, 0]
        self.dupla_counter = [0, 0, 0, 0]
        self.total = 0
        self.byte_strings = []
        self.byte_previous = 0

        self.bit_dictionary = [[], []]
        self.dupla_dictionary = [[], [], [], []]

        bits = []
        for i in range(0, 8):
            bits.append(1<<(7-i))

        for i in range(0, 256):
            byte_string = ''
            eight_bit_counter = 0

            for bit_value in bits:
                current_bit = bit_value & i > 0
                eight_bit_counter += 1 if current_bit else 0
                byte_string += '1' if current_bit else '0'

            self.byte_strings.append(byte_string)

            self.bit_dictionary[0].append(8-eight_bit_counter)
            self.bit_dictionary[1].append(eight_bit_counter)

            dp_counter = [0, 0, 0, 0]
            dp_counter[3 & i] += 1
            dp_counter[(12 & i)>> 2] += 1
            dp_counter[(48 & i)>> 4] += 1
            dp_counter[(192 & i)>> 6] += 1

            for d_p in range(0, 4):
                self.dupla_dictionary[d_p].append(dp_counter[d_p])

    def process(self, byte_value):
        """Process one byte"""
        self.total += 1

        try:
            self.dupla_counter[0] += self.dupla_dictionary[0][byte_value]
            self.dupla_counter[1] += self.dupla_dictionary[1][byte_value]
            self.dupla_counter[2] += self.dupla_dictionary[2][byte_value]
            self.dupla_counter[3] += self.dupla_dictionary[3][byte_value]
            self.byte_counter[byte_value] += 1

            self.bit_counter[0] += self.bit_dictionary[0][byte_value]
            self.bit_counter[1] += self.bit_dictionary[1][byte_value]
            max_val = max(self.byte_previous, byte_value)
            min_val = min(self.byte_previous, byte_value)
            self.byte_diff[max_val-min_val] += 1
            self.byte_previous = byte_value
        except Exception as e:
            print("Excpetion on ",byte_value );
            print("dupla counter ",len( self.dupla_counter ) )
            print("byte counter ",len( self.byte_counter ) )
            print("bit counter ",len( self.bit_counter ) )

    def process_list(self, byte_list):
        """Process a list of bytes"""
        for i in byte_list:
            self.process(i)


    def generate_bars_image(self, list_256 ):
        """generate a image o pbm of array"""

        new_list = list_256.copy()
        #new_list.sort()

        total_elements = sum( list_256 )
        maximun = max( list_256 )

        print("Total",total_elements)

        string_image = "P2 1000 512 4\n"
        total = 0

        for item in new_list:
            pixels = int(float(item)/float(maximun))*1000;

            tmp_str = ""
            total += item;
            percent = int( total*100/total_elements )

            print("Percent", percent )

            for x in range(0,500):
                if percent > 90:
                    tmp_str += "4 4 " if x <= item*2 else "0 0 "
                elif percent > 75:
                    tmp_str += "3 3 " if x <= item*2 else "0 0 "
                elif percent > 50:
                    tmp_str += "2 2 " if x <= item*2 else "0 0 "
                else:
                    tmp_str += "1 1 " if x <= item*2 else "0 0 "

            for x in range(0,2):
                string_image += tmp_str.strip()+"\n"

        return string_image


    def printx(self):
        """Print the stats"""
        print("t bytes", self.total)
        print("bits", self.bit_counter)
        print("duplas", self.dupla_counter)
        print("Counter Average", sum(self.byte_counter)/256.0)

        byte_diff_sum = 0

        for x in range(0,256):
            byte_diff_sum += x*self.byte_counter[x]

        diff_avg = byte_diff_sum/self.total

        print("diff avg", sum(self.byte_diff), )
        print("byte diff", self.byte_diff)


    def generate_pbm_image(self, byte_list, width):
        """Generates a pbm image of the bits"""

        height = len(byte_list)/width

        string_image = 'P1'
        string_image += width
        string_image += '\n'
        string_image += height

        for i in range(0, width*height):
            string_image += self.byte_strings[byte_list[i]]

            if(i%width)== 0:
                string_image += '\n'

        return string_image




#   1 2 3 4
# 1 1 2 3 4
# 2 2 3 4 1
# 3 3 4 1 2
# 4 4 1 2 3


