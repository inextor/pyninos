def compress_positions(pos_list):
    cp_pos_list = pos_list.copy()
    new_pos = [];

    for i in range(0,len(pos_list)):
        for index,value in enumerate( cp_pos_list ):
            if i == value:
                new_pos.append( index )
                cp_pos_list.pop( index )
                break;

def decompress_positions(pos_list):

    cp_pos_list = pos_list.copy()

    for i in range(1,len(pos_list) )





