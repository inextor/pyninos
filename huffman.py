"""Hufman coding helper"""
import sys

class Node:
    """Node class for temporary use only in the huffman codding"""
    def __init__(self, value, freq, node1, node2):
        self.freq = freq
        self.value = value


        self.left = node2
        self.right = node1

        if node1 is None:
            self.right = node2

        if node2 is None:
            self.right = node1

        if node1 is not None and node2 is not None:
            if self.left.freq > self.right.freq:
                temp = self.right
                self.right = self.left
                self.left = temp
            elif self.left.freq == self.right.freq and self.left.value is None:
                temp = self.right
                self.right = self.left
                self.left = temp


        if self.left is not None:
            self.left.branch = 0
            self.left.parent = self

        if self.right is not None:
            self.right.branch = 1
            self.right.parent = self

        self.branch = None
        self.parent = None
        self.huff_string = None

    def get_freq(self):
        """Only for comparison"""
        return self.freq

    def get_parent_freq(self):
        temp_node = self
        parent_path = ""

        while  temp_node is not None:#&& temp_node != root_node
            parent_path += "->"
            parent_path += str(temp_node.parent.freq) if temp_node.parent is not None else "-1"
            temp_node = temp_node.parent

        return parent_path

    def print_tree(self):
        levels = [[self]]
        current_level = [self]
        next_level = []

        while current_level:
            current_node = current_level.pop()
            if current_node.left is not None:
                next_level.append(current_node.left)

            if current_node.right is not None:
                next_level.append(current_node.right)

            if not current_level and next_level:
                current_level = next_level
                levels.append(current_level.copy())
                next_level = []

        #list_size = len(levels)

        #for index, node_list in enumerate(levels):
        for node_list in levels:
            str_rep = ""
            for node in node_list:
                str_rep += node.get_string()

            #if index < (list_size-1):
            #    str_rep = "   "*len(levels[index+1])+str_rep
            print(str_rep)


    def get_string(self):
        """ return a string"""
        arrow = ">" if self.branch == 1 else "<"

        if self.value is not None:
            return arrow+str(self.value)+","+str(self.freq)+"   "

        return arrow+"   ,   "


    def print(self):
        """It prints the values of the node"""
        print("Value ", self.value,
              "Freq: ", self.freq,
              "S: ", self.huff_string,
              self.get_parent_freq())

def get_canonical_huffman(node_list):
    canonical_list = []



def get_huffman_dictionary(frequency_list):
    """The main function for the huffman coding"""
    forrest = []
    original = []

    for index, freq in enumerate(frequency_list):
        node = Node(index, freq, None, None)
        forrest.append(node)
        original.append(node)


    while len(forrest) > 1:
        forrest.sort(key=lambda e: e.freq)
        for i in forrest:
            i.print()
        print("----------------------")

        node_1 = forrest.pop(0)
        node_2 = forrest.pop(0)
        node_3 = Node(None, node_1.freq+node_2.freq, node_1, node_2)

        forrest.insert(0, node_3 )


    for i in original:
        temp_node = i
        i.huff_string = ""

        while  temp_node is not None:#&& temp_node != root_node
            if temp_node.branch is not None:
                i.huff_string += "1" if temp_node.branch == 1 else "0"

            temp_node = temp_node.parent

        i.huff_string = i.huff_string[::-1]


    forrest[0].print_tree()

    return original


if __name__ == "__main__":
    get_huffman_dictionary([ 7, 4, 4, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1 ])



#Value  0 Freq:  7 S:  111 ->12->20->36->-1 // ✓
#Value  1 Freq:  4 S:  001 ->8->16->36->-1  ✗
#Value  2 Freq:  4 S:  000 ->8->16->36->-1  ✓
#Value  3 Freq:  3 S:  1101 ->5->12->20->36->-1  ✓
#Value  4 Freq:  2 S:  0100 ->4->8->16->36->-1 ✗
#Value  5 Freq:  2 S:  1011 ->4->8->20->36->-1 ✓
#Value  6 Freq:  2 S:  1010 ->4->8->20->36->-1 ✗
#Value  7 Freq:  2 S:  1001 ->4->8->20->36->-1
#Value  8 Freq:  2 S:  1000 ->4->8->20->36->-1
#Value  9 Freq:  2 S:  1100 ->5->12->20->36->-1
#Value  10 Freq:  1 S:  01011 ->2->4->8->16->36->-1
#Value  11 Freq:  1 S:  01010 ->2->4->8->16->36->-1
#Value  12 Freq:  1 S:  01111 ->2->4->8->16->36->-1
#Value  13 Freq:  1 S:  01110 ->2->4->8->16->36->-1
#Value  14 Freq:  1 S:  01101 ->2->4->8->16->36->-1
#Value  15 Freq:  1 S:  01100 ->2->4->8->16->36->-1

