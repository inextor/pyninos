class BitsAnalitycs:

    def __init__(self):
        self.byte_counter =[0]*256
        self.bit_counter = [0, 0]
        self.dupla_counter = [0, 0, 0, 0]
        self.total = 0
        self.byte_strings = []

        self.bit_dictionary  =[[],[]]
        self.dupla_dictionary =[[],[],[],[]]

        bits = []
        for i in range(0,8):
            bits.append( 1<<(7-i) )

        for i in range(0, 256):
            byte_string = '';
            eight_bit_counter = 0

            for bit_value in bits:
                current_bit = bit_value & i>0;
                eight_bit_counter += 1 if current_bit else 0
                byte_string += '1' if current_bit else '0'

            self.byte_strings.append( byte_string.stri() )

            self.bit_dictionary[0].append( 8-eight_bit_counter )
            self.bit_dictionary[1].append( eight_bit_counter )

            dp_counter = [ 0, 0, 0, 0]
            dp_counter[3 & i] +=1
            dp_counter[(12 & i) >> 2] += 1
            dp_counter[(48 & i) >> 4] += 1
            dp_counter[(192 & i) >> 6] += 1

            for dp in range(0,4):
                self.dupla_dictionary[dp].append(dp_counter[dp])

    def process(self,byte_value):

        self.total += 1
        self.dupla_counter[0] += self.dupla_dictionary[0][byte_value];
        self.dupla_counter[1] += self.dupla_dictionary[1][byte_value];
        self.dupla_counter[2] += self.dupla_dictionary[2][byte_value];
        self.dupla_counter[3] += self.dupla_dictionary[3][byte_value];

        self.byte_counter[byte_value] += 1;

        self.bit_counter[0] += self.bit_dictionary[0][byte_value];
        self.bit_counter[1] += self.bit_dictionary[1][byte_value];


    def process_list( self, byte_list ):
        for i in byte_list:
            self.process( i )


    def printx(self):
        print("t bytes", self.total );
        print("bits", self.bit_counter);
        print("duplas", self.dupla_counter );
        print("Counter Average", sum(self.byte_counter)/256.0 );


    def generate_pbm_image(self,byte_list,width):

        height = len(byte_list)/width

        string_image = 'P1'
        string_image += width
        string_image += '\n'
        string_image += height

        for i in range(0,width*height):
            string_image += self.byte_strings[ byte_list[ i ] ]

            if((i%width) == 0):
                string_image+='\n'

        return string_image


#   1 2 3 4
# 1 1 2 3 4
# 2 2 3 4 1
# 3 3 4 1 2
# 4 4 1 2 3

