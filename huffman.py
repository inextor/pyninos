class Node:
    def __init__(self,value,freq,left,right):
        self.freq = freq;
        self.value = value
        self.left = None
        self.right = None
        self.branch = None
        self.parent = None
        self.huff_string = None

    def get_freq(self):
        return self.freq

class Huffman:

    def __init__(self,frequency_list):
        self.forrest    = []
        self.original   = []

        for index,freq in enumerate( frequency_list ):
            if i > 0 :
                node = Node(index, freq, None, None)
                self.forrest.append( node )
                self.original.append( node )


        while len(self.forrest)>1:
            self.forrest.sort(key=get_freq,false)

            n1 = self.pop(0)
            n2 = self.pop(0)
            n3 = None

            if( n2.freq > n1.freq ):
                n3 = Node(None, n1.freq+n2.freq, n1, n2 )
                n2.branch = 1
                n1.branch = 0
            else:
                n3 = Node(None, n1.freq+n2.freq, n2, n1 )
                n2.branch = 0
                n1.branch = 1

            n2.parent = n3
            n2.parent = n2

            self.forrest.append(n3)

        self.root_node = self.forrest[0]


        for i in self.original:
            temp_node = i
            while temp_node.parent != None: #&& temp_node != self.root_node
                if i.branch != None:
                    i.huff_string += "1" if i.branch == 1 else "0"

                temp_node = temp_node.parent

            i.huff_string = i.huff_string[::-1]

