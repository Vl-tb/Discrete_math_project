import heapq
import os
import base64
from io import StringIO
import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer


# HUFFMAN CODING
class Node:
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


class Tree:
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


class HuffmanAlgorithm:
    """
    This class can encode and decode files
    due to Huffman algorithm, based on using binary tree.
    """
    def __init__(self, data=''):
        self.data = data
        self.frequency = []
        self.tree_construtor = []
        self.dictionary = {}
        self.encode = None

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
        if self.frequency == []:
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


# LZ77 CODING
# Implementation of LZ77 compression algrorithm
def lz77_compression(src):
    """
    Compress the given string. Replace similar occurences
    with #copy,steps_back#
    """
    # MAX_BUFFER = 65536
    # MAX_BUFFER = 32768
    MAX_BUFFER = 4096
    # MAX_BUFFER = 2048
    # MAX_BUFFER = 100
    MAX_COPY_LEN = 10

    packed_message = ''

    run_idx = 0
    main_len = len(src)
    cache = {}
    cache_rev = {}
    to_del = []

    while run_idx < len(src):
        for what_to_del in to_del:
            try:
                for cache_val in cache_rev[what_to_del]:
                    del cache[cache_val]
                del cache_rev[run_idx]
            except KeyError:
                pass
        length = min(MAX_COPY_LEN, main_len-run_idx)

        while length > 4:
            message = src[run_idx:run_idx + length]
            try:
                copy_idx = cache[message]
                if copy_idx + length < run_idx:
                    packed_message += f"#{length},{run_idx - copy_idx}#"
                    to_del = range(run_idx-MAX_BUFFER, run_idx-MAX_BUFFER+length)
                    run_idx += length
                    break
                else:
                    length -= 1
            except KeyError:
                cache[message] = run_idx
                try:
                    cache_rev[run_idx].add(message)
                except KeyError:
                    cache_rev[run_idx] = {message}
                length -= 1
        else:
            packed_message += src[run_idx]
            to_del = [run_idx-MAX_BUFFER]
            run_idx += 1

    return packed_message


def lz77_decompression(encoded_message):
    """
    Decompress the given encoded string. Return the initial file
    in representation of string
    """
    unpack = ''
    i_pack = 0
    i_unpack = 0

    while i_pack < len(encoded_message):
        if encoded_message[i_pack] != '#':
            unpack += encoded_message[i_pack]
            i_unpack += 1
            i_pack += 1
            continue

        count = 1

        while encoded_message[i_pack + count] != ',':
            count += 1
        length = int(encoded_message[i_pack + 1:i_pack + count])

        count += 1
        count_ex = count

        while encoded_message[i_pack + count] != '#':
            count += 1
        distance = int(encoded_message[i_pack + count_ex:i_pack + count])
        unpack += unpack[i_unpack - distance:i_unpack - distance + length]
        i_unpack += length
        i_pack += count + 1

    return unpack


# LZW CODING
def lzw_compression(string) -> str:
    """ compression using the Lempel-Ziv-Welch algorithm (LZW). """

    dictionary = {'+':'0', '/':'1', '0':'2', '1':'3', '2':'4', '3':'5',
                  '4':'6', '5':'7', '6':'8', '7':'9', '8':'10', '9':'11',
                  '=':'12', 'A':'13', 'B':'14', 'C':'15', 'D':'16', 'E':'17',
                  'F':'18', 'G':'19', 'H':'20', 'I':'21', 'J':'22', 'K':'23',
                  'L':'24', 'M':'25', 'N':'26', 'O':'27', 'P':'28', 'Q':'29',
                  'R':'30', 'S':'31', 'T':'32', 'U':'33', 'V':'34', 'W':'35',
                  'X':'36', 'Y':'37', 'Z':'38', 'a':'39', 'b':'40', 'c':'41',
                  'd':'42', 'e':'43', 'f':'44', 'g':'45', 'h':'46', 'i':'47',
                  'j':'48', 'k':'49', 'l':'50', 'm':'51', 'n':'52', 'o':'53',
                  'p':'54', 'q':'55', 'r':'56', 's':'57', 't':'58', 'u':'59',
                  'v':'60', 'w':'61', 'x':'62', 'y':'63', 'z':'64', '\n':65}
    dict_size = 66

    sequence = ""
    compressed_im = []
    for char in string:
        sequence_char = sequence + char
        if sequence_char in dictionary:
            sequence = sequence_char
        else:
            compressed_im.append(dictionary[sequence])
            dictionary[sequence_char] = str(dict_size)
            dict_size += 1
            sequence = char

    # Output the code for sequence.
    if sequence:
        compressed_im.append(dictionary[sequence])
    return ' '.join(compressed_im)


def lzw_decompression(compressed_photo_str: str) -> str:
    """
    Reproduction of an file that has been compressed using
    the Lempel-Ziv-Welch (LZW) algorithm.
    """
    compressed = list(map(int, compressed_photo_str.split(' ')))
    dictionary = {0:'+', 1:'/', 2:'0', 3:'1', 4:'2', 5:'3',
                  6:'4', 7:'5', 8:'6', 9:'7', 10:'8', 11:'9',
                  12:'=', 13:'A', 14:'B', 15:'C', 16:'D', 17:'E',
                  18:'F', 19:'G', 20:'H', 21:'I', 22:'J', 23:'K',
                  24:'L', 25:'M', 26:'N', 27:'O', 28:'P', 29:'Q',
                  30:'R', 31:'S', 32:'T', 33:'U', 34:'V', 35:'W',
                  36:'X', 37:'Y', 38:'Z', 39:'a', 40:'b', 41:'c',
                  42:'d', 43:'e', 44:'f', 45:'g', 46:'h', 47:'i',
                  48:'j', 49:'k', 50:'l', 51:'m', 52:'n', 53:'o',
                  54:'p', 55:'q', 56:'r', 57:'s', 58:'t', 59:'u',
                  60:'v', 61:'w', 62:'x', 63:'y', 64:'z', 65:'\n'}
    dict_size = 66

    encoded_str = StringIO()
    sequence = dictionary[compressed[0]]
    compressed.remove(compressed[0])
    encoded_str.write(sequence)
    for char in compressed:
        if int(char) in dictionary:
            entry = dictionary[char]
        elif char == dict_size:
            entry = str(sequence) + str(sequence)[0]
        else:
            raise ValueError(f'Bad compressed k: {char}')
        encoded_str.write(entry)

        dictionary[dict_size] = str(sequence) + entry[0]
        dict_size += 1
        sequence = entry
    encoded_str = encoded_str.getvalue()
    return encoded_str


# DEFLATE CODING
def deflate_compress(src):
    """
    Encode the message accordingly to the deflate using
    LZ77 and Huffman algorithm
    """
    lz77_en = lz77_compression(src)
    huff_comp = HuffmanAlgorithm(lz77_en)
    deflated = huff_comp.encoding()

    return deflated + chr(0) + str(huff_comp.frequency)


def deflate_decompress(encoded_string):
    """
    Decode the message accordingly to the deflate using
    LZ77 and Huffman algorithm
    """
    encoded_message, huff_tree_str = encoded_string.split(chr(0))
    exmp = HuffmanAlgorithm()
    exmp.frequency = eval(huff_tree_str)
    exmp.binary_tree()
    exmp.set_dictionary()
    exmp.encode = encoded_message
    lz77_en = exmp.decoding()
    inflated = lz77_decompression(lz77_en)
    return inflated


# VIDEO PLAYER
def PlayVideo(video_path):
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while True:
        grabbed, frame=video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(46) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
    video.release()
    cv2.destroyAllWindows()


# MAIN COMPRESS/DECOMPRESS
def compress(path: str, path_compressed: str, function: callable):
    with open(path, "rb") as file_to_compress:
        bits = base64.b64encode(file_to_compress.read())
        string = ''
        for bit in bits:
            string += chr(bit)
    print(len(string))

    compressed = function(string)
    with open(path_compressed, 'w') as compressed_file:
        compressed_file.write(compressed)


def decompress(path_compressed: str, path_decompressed: str, function: callable):
    with open(path_compressed, 'r') as compressed_file:
        compressed = compressed_file.read()
    decompressed = function(compressed)
    with open(path_decompressed, "wb") as file_to_decompress:
        file_to_decompress.write(base64.b64decode(decompressed))


# MAIN
def main():
    """Main function"""
    print("Welcome to our program, what do you want?")
    print("p - play a video.")
    print("c - compress a file.")
    print("d - decompress a file.")
    answer_1 = input()

    # playing a video
    if answer_1 == 'p':
        print("What video do you want to play? (enter it's full name).")
        answer_1 = input()
        print("If you want to quit watching simply press 'q' button.")
        PlayVideo(answer_1)

    # compression
    elif answer_1 == 'c':
        print("Choose the file (enter it's full name).")
        answer_1 = input()
        print("Now choose in which way do you want to do this.")
        print("lz77")
        print("lzw")
        print("huf (Huffman's coding)")
        print("def (DEFLATE)")
        answer_2 = input()
        
        if answer_2 == "lz77":
            print("Give this compressed file a name:")
            answer_3 = input()
            compress(answer_1, answer_3, lz77_compression)

        elif answer_2 == "lzw":
            print("Give this compressed file a name:")
            answer_3 = input()
            compress(answer_1, answer_3, lzw_compression)

        elif answer_2 == 'huf':
            print("Give this compressed file a name:")
            answer_3 = input()
            with open(answer_1, "rb") as file_to_compress:
                bits = base64.b64encode(file_to_compress.read())
                string = ''
                for bit in bits:
                    string += chr(bit)
            huff_comp = HuffmanAlgorithm(string)
            compressed = huff_comp.encoding()
            with open(answer_3, 'w') as compressed_file:
                compressed_file.write(compressed)

        elif answer_2 == "def":
            print("Give this compressed file a name:")
            answer_3 = input()
            compress(answer_1, answer_3, deflate_compress)

    # decompression
    elif answer_1 == "d":
        print("Choose the file (enter it's full name).")
        answer_1 = input()
        print("Now choose in which way do you want to do this.")
        print("(make sure the method is the same as it was encoded or it won't work...)")
        print("lz77")
        print("lzw")
        print("huf (Huffman's coding)")
        print("def (DEFLATE)")
        answer_2 = input()

        if answer_2 == "lz77":
            print("Give this new file a name:")
            answer_3 = input()
            decompress(answer_1, answer_3, lz77_decompression)

        elif answer_2 == "lzw":
            print("Give this new file a name:")
            answer_3 = input()
            decompress(answer_1, answer_3, lzw_decompression)

        elif answer_2 == 'huf':
            print("Give this new file a name:")
            answer_3 = input()
            with open(answer_1, 'r') as compressed_file:
                data = compressed_file.read()
            encoded_message, huff_tree_str = data.split(chr(0))
            exmp = HuffmanAlgorithm()
            exmp.frequency = eval(huff_tree_str)
            exmp.binary_tree()
            exmp.set_dictionary()
            exmp.encode = encoded_message
            decompressed = exmp.decoding()
            with open(answer_3, "wb") as file_to_decompress:
                file_to_decompress.write(base64.b64decode(decompressed))

        elif answer_2 == "def":
            print("Give this new file a name:")
            answer_3 = input()
            decompress(answer_1, answer_3, deflate_decompress)

    print("DONE")
    print("Thank you for using our software!")
    print("Have a nice day!")


if __name__ == "__main__":
    main()
