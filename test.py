
if __name__ == "__main__":

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
        for i in b:
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

#        print('\t'.join(map(str,tuppleCounter)))
#        print('\t'.join(map(str,byteCounter)))
#
#        total = len( b )*8;
#        white = total
#        black = 0;
#
#        for x in range( 0, 8):
#            white -= byteCounter[ x ]
#            black += byteCounter[ x ]
#
#
#        print("0", white );
#        print("1", black );
#        print("total", total );

