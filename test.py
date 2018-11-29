import sys



def get_binary_descriptor_dictionary():
    """Return a dictionary for descriptor"""

    dic0 = []
    dic1 = []

    for i in range(0, 256):
        previous0 = False
        previous1 = True

        dic_value0 = 0
        dic_value1 = 0

        for bit_index in range(0, 8):
            bit = (i & (1 << (7-bit_index))) > 0

            if previous0 == bit:
                dic_value0 += (1 << (7-bit_index))

            if previous1 == bit:
                dic_value1 += (1 << (7-bit_index))

            previous0 = bit
            previous1 = bit

        dic0.append(dic_value0)
        dic1.append(dic_value1)


def to_binary_descriptor(binary_list):
    for i in binary_list:




        tuppleCounter[  3 & i  ]+=1
        tuppleCounter[  (12 & i) >> 2  ]+=1
        tuppleCounter[  (48 & i) >> 4  ]+=1
        tuppleCounter[  (192 & i ) >> 6  ]+=1

        counter+=1

        for x in range( 0,8):
            current = (( 1 <<  x ) & i )>0;
            if last == -1 :
                if current :
                    lines.append( 1 )
                else:
                    lines.append( 0 )
            elif current:
                    lines.append( 1 )
            else:
                    lines.append( 0 )

        if( counter >= 128 ):
            print('\t'.join(map(str,lines)))
            lines.clear()
            counter = 0;





    bitCounter  = [0,0];
    tuppleCounter = [ 0, 0, 0 ,0 ]
    byteCounter = [ 0, 0, 0, 0, 0, 0, 0, 0]
    indexes =[ 3, 3<<2, 3<<4, 3<<6 ]
    move    =[ 0, 2, 4, 6 ]

    lines   = [];

    counter = 0;
    last = -1;

    print("P1\n1024\n1024")

    with open('1M2.bin', 'rb') as fl:
        b = fl.read()

