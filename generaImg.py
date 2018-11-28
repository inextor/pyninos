import sys

if __name__ == "__main__":


    print("P1\n1024\n1024")
    lines = []
    #print( sys.argv );
    #exit()
    counter = 0

    with open(sys.argv[1], 'rb') as fl:
        b = fl.read()

        for i in b:
            counter+=1
            for x in range( 0,8):
                current = (( 1 <<  x ) & i )>0;

                if current :
                    lines.append( 1 )
                else:
                   lines.append( 0 )

            if( counter >= 128 ):
                print('\t'.join(map(str,lines)))
                lines.clear()
                counter = 0;
