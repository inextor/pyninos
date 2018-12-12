"""This module is for bytes analitycs"""
import sys

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
        self.half_byte_previous = 0
        self.byte_transitions = []
        self.half_byte_transitions = []
        self.b_bits = [0,0,0,0,0,0,0,0]

        self.bit_dictionary = [[], []]
        self.dupla_dictionary = [[], [], [], []]

        bits = []
        for i in range(0, 8):
            bits.append(1<<(7-i))

        for i in range(0,16):
            self.half_byte_transitions.append([0]*16)

        for i in range(0, 256):
            self.byte_transitions.append([0]*256)
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

            self.byte_transitions[self.byte_previous][byte_value] += 1
            self.byte_previous = byte_value

            for i in range(0, 8):
                if (1 << (7-i)) & byte_value:
                    self.b_bits[i] += 1

            #half_byte = byte_value>>4;
            #self.half_byte_transitions[ self.half_byte_previous ][ half_byte ] += 1
            #self.half_byte_previous = half_byte;
            #half_byte = (byte_value&0x0F)
            #self.half_byte_transitions[ self.half_byte_previous ][ half_byte ] += 1

            #self.half_byte_previous = half_byte

        except Exception as e_f:
            print("Excpetion on ", e_f )
            #print("Excpetion on ",self.half_byte)
            #print("Excpetion on ",byte_value );
            #print("dupla counter ",len( self.dupla_counter ) )
            #print("byte counter ",len( self.byte_counter ) )
            #print("bit counter ",len( self.bit_counter ) )

    def process_list(self, byte_list):
        """Process a list of bytes"""
        for i in byte_list:
            self.process(i)


    def generate_half_byte_dictionary(self):
        """generate a transition position dictionary"""
        dictionary = [0]*16

        for i in self.half_byte_transitions:
            z = i.copy();
            z.sort(key=int)
            z.reverse()
            for index,value in enumerate(z):
                dictionary[index]+=value;

        return dictionary;


    def generate_pos_dictionary(self):
        """generate a transition position dictionary"""
        dictionary = [0]*256

        for i in self.byte_transitions:
            z = i.copy();
            z.sort(key=int)
            z.reverse()
            for index,value in enumerate(z):
                dictionary[index]+=value;

        return dictionary;

    def generate_transitions_image(self):
        """generate a image of the dictionary"""
        max_value = 0

        for i in self.byte_transitions:
            for j in i:
                if j > max_value:
                    max_value = j


        image = "P2\n1024\n1024\n255\n"

        for i in self.byte_transitions:
            image_line = ""
            z = i.copy();
            z.sort(key=int)

            for j in z:
                percent = int( 1.0*j*255/max_value)
                for k in range(0, 4):
                    image_line += str(percent)+" "

            for j in range(0, 4):
                image += image_line.strip()+"\n"

        return image;

    def generate_bars_image(self, list_256 ):
        """generate a image o pbm of array"""

        new_list = list_256.copy()
        #new_list.sort()

        total_elements = sum( list_256 )
        maximun = max( list_256 )

        string_image = "P2\n1000 512\n12\n"
        total = 0

        sys.stderr.write("Max "+str(new_list[0]*100/total_elements)+"%\n")
        line = 0;
        for item in new_list:
            pixels = int(float(item)*500.0/float(maximun));

            tmp_str = ""
            total += item;
            percent = 100-int(total*100.0/total_elements)

            if( line == 10 ):
                sys.stderr.write("In 10 "+str(total*100/total_elements)+"%\n")

            line += 1

            for x in range(0, 500):
                if percent > 90:
                    tmp_str += "11 3 " if x <= pixels else "0 1 "
                elif percent > 80:
                    tmp_str += "10 10 " if x <= pixels else "0 1 "
                elif percent > 70:
                    tmp_str += "9 9 " if x <= pixels else "0 1 "
                elif percent > 60:
                    tmp_str += "8 8 " if x <= pixels else "0 1 "
                elif percent > 50:
                    tmp_str += "7 7 " if x <= pixels else "0 1 "
                elif percent > 40:
                    tmp_str += "6 6 " if x <= pixels else "0 1 "
                elif percent > 30:
                    tmp_str += "5 5 " if x <= pixels else "0 1 "
                elif percent > 20:
                    tmp_str += "4 4 " if x <= pixels else "0 1 "
                elif percent > 10:
                    tmp_str += "3 3 " if x <= pixels else "0 1 "
                else:
                    tmp_str += "2 2 " if x <= pixels else "0 1 "

            for x in range(0, 2):
                string_image += tmp_str.strip()+"\n"

        return string_image

    def printx(self):
        """Print the stats"""
        print("t bytes", self.total)
        print("bits", self.bit_counter)
        print("duplas", self.dupla_counter)
        print("Counter Average", sum(self.byte_counter)/256.0)
        print("R Bits ", self.b_bits)

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


if __name__ == "__main__":


    is_bars = False
    print_graph = True

    if( len( sys.argv ) > 1 ):
        #print(">2")
        if(sys.argv[1].find('-') != -1):
            #print("------")
            if sys.argv[1].find('b') != -1:
                is_bars = True
            if sys.argv[1].find('p') != -1:
                print_graph = False

    if print_graph:
        b = BitsAnalytics()
        data = sys.stdin.buffer.read()
        b.process_list( data)
        if is_bars:
            b.byte_diff.sort(reverse=True)
            print( b.generate_bars_image( b.byte_diff ) );#b.generate_pos_dictionary() ) )
        else:
            print(  b.generate_transitions_image() )
    else:
        bi_global = BitsAnalytics()
        data = sys.stdin.buffer.read()

        bitan = []
        for i in range(0, 256):
            bitan.append( BitsAnalytics())

        counter = 0

        for i in data:
            #sys.stderr.write("FoOOOOOOOO"+str(counter%256)+"\n")
            bitan[counter%256].process(i)
            bi_global.process(i)
            counter += 1

        for i in bitan:
            i.printx()

        bi_global.printx()


#   1 2 3 4
# 1 1 2 3 4
# 2 2 3 4 1
# 3 3 4 1 2
# 4 4 1 2 3


