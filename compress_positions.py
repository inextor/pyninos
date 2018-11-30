def compress_positions(pos_list):
    cp_pos_list = pos_list.copy()
    new_pos = [];

    for i in range(0,len(pos_list)):
        for index,value in enumerate( cp_pos_list ):
            if i == value:
                new_pos.append( index )
                cp_pos_list.pop( index )
                break;

    return new_pos


def decompress_positions(pos_list):

    cp_pos_list = pos_list.copy()

    temp_pos = []
    new_pos = [0]*len(pos_list)

    for i in range( 0 ,len(pos_list) ):
        temp_pos.append( i );


    for value in range(0, len(pos_list) ):
        position = cp_pos_list[ i ]
        final_position = temp_pos.pop( position )
        new_pos[ final_position ] = value

    return new_pos

def test():
    test_list = []

    for i in range(0,256):
        test_list.append( i )

    test_list.reverse()

    print("test list",test_list )
    compressed_list = compress_positions( test_list )
    print("compressed", compressed_list )
    uncompressed_list = decompress_positions( compressed_list )
    print("uncompressed list", uncompressed_list )

    for i in range(0,256):
        if test_list[i] != uncompressed_list[i]:
            raise Exception("Doesnt work")


if __name__ == "__main__":
    test()
