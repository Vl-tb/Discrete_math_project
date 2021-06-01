"""
This module contains realisation of Huffman encoding/decoding algorithm.
"""

class Node():
    """
    This class represents a node for binary tree.
    """
    def __init__(self, value):
        self.value = value
        self.left_ch = None
        self.right_ch = None

    def get_value(self):
        """
        Gets the node's value.
        """
        return self.value

    def set_left_ch(self, value):
        """
        Sets node's left_child as node object.
        """
        self.left_ch = value

    def set_right_ch(self, value):
        """
        Sets node's right_child as node object.
        """
        self.right_ch = value

    def get_left_ch(self):
        """
        Gets node's left_child as node object.
        """
        return self.left_ch

    def get_right_ch(self):
        """
        Gets node's right_child as node object.
        """
        return self.right_ch

    def __str__(self):
        return f"{self.value}"


class Tree():
    """
    This class represents binary tree.
    """
    def __init__(self):
        self.root = None
    
    def set_root(self, value):
        """
        Set a root of this tree.
        """
        self.root = value

    def get_root(self):
        """
        Get a root of this tree.
        """
        return self.root

    def postorder(self, node, lst=[]):
        """
        One of possible traversals.
        """
        if node.left_ch:
            self.postorder(node.left_ch, lst)
        if node.right_ch:
            self.postorder(node.right_ch, lst)
        lst.append((node, node.value))
        return lst

    def is_leaf(self, item):
        """
        This method checks if item is lead in binary tree.
        """
        nodes_list = self.postorder(self.root)
        for element, value in nodes_list:
            if (element == item and
            element.left_ch == None and
            element.right_ch == None):
                return True
        return False

    def huffman_code(self):
        """
        Prints path ti the leafs in binary tree.
        """
        relation = {}
        nodes_in_tree = []
        nodes = self.postorder(self.root)
        for node, value in nodes:
            try:
                check = relation[node]
            except KeyError:
                nodes_in_tree.append(node)
                if not self.is_leaf(value):
                    if node.right_ch != None:
                        relation[node.right_ch] = (node, 1)
                    if node.left_ch != None:
                        relation[node.left_ch] = (node, 0)
            else:
                break
            
        def recurse(node, relation, code = ''):
            """
            Used for creation paths.
            """
            try:
                code += str(relation[node][1])
                return recurse(relation[node][0], relation, code)
            except KeyError:
                return code
        dictionary = {}
        for node in nodes_in_tree:
            if self.is_leaf(node):
                code = recurse(node, relation)
                dictionary[node.value[0]] = code[::-1]
        self.dictionary = dictionary
        return


class Huffman_algorithm():
    """
    This class can encode and decode files
    due to Huffman algorithm, based on using binary tree.
    """
    def __init__(self, data):
        self.data = data
        self.frequency = []
        self.tree_construtor = []
        self.dictionary = {}

    def set_data(self, data):
        """
        Sets a needed string.
        """
        self.data = data

    def set_frequency_list(self):
        """
        Creates attribute self.frequency,
        which contains tuples of chars and
        times it repeated in data-string.
        """
        freq_dict = {}
        for char in self.data:
            if char in freq_dict:
                freq_dict[char] += 1
            else:
                freq_dict[char] = 1
        freq_list = list(freq_dict.items())
        freq_list.sort(key=lambda x: x[1], reverse=True)
        self.frequency = freq_list

    def frequency_sort(self, node):
        """
        This method finds place for inserting
        a new node in the self.frequency.
        """
        node_value = node.get_value()[1]
        for index in range(len(self.tree_construtor)+1):
            if index == len(self.tree_construtor):
                self.tree_construtor.append(node)
                break
            index_value = self.tree_construtor[index].get_value()[1]
            if index_value <= node_value:
                self.tree_construtor.insert(index, node)
                break

    def binary_tree(self):
        """
        Creates a Huffman-tree, what is actually the binary-tree.
        """
        self.set_frequency_list()
        tree = Tree()
        for char_freq in self.frequency:
            node = Node(char_freq)
            self.tree_construtor.append(node)
        while len(self.tree_construtor) != 1:
            right_ch = self.tree_construtor.pop()
            left_ch = self.tree_construtor.pop()
            new_node = Node((right_ch.get_value()[0] + left_ch.get_value()[0],
                            right_ch.get_value()[1] + left_ch.get_value()[1]))
            new_node.set_left_ch(left_ch)
            new_node.set_right_ch(right_ch)
            self.frequency_sort(new_node)
        tree.set_root(self.tree_construtor[0])
        self.tree = tree

    def set_dictionary(self):
        """
        Creates a dictionary for encoding & decoding due
        Huffman algorithm.
        """
        self.tree.huffman_code()

    def encoding(self):
        """
        Encodes data (string value) to binary string.
        """
        self.binary_tree()
        self.set_dictionary()
        output = ''
        for char in self.data:
            output += self.tree.dictionary[char]
        self.encode = output
        return output      

    def decoding(self):
        """
        Decodes encoded data to initial format.
        """
        reversed_dict = {}
        for value, key in self.tree.dictionary.items():
            reversed_dict[key] = value
        left_index = 0
        right_index = 1
        output = ''
        while left_index != len(self.encode):
            if self.encode[left_index : right_index] in reversed_dict:
                output += reversed_dict[self.encode[left_index : right_index]]
                left_index = right_index
            right_index += 1
        self.decode = output
        return output
