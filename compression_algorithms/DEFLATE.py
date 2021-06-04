from LZ77 import compress_message, decompress_message
from HUFFMAN import Huffman_algorithm

def deflate_message(src):
    """
    Encode the message accordingly to the deflate using
    LZ77 and Huffman algorithm
    """
    lz77_en = compress_message(src)
    huff_comp = Huffman_algorithm(lz77_en)
    deflated = huff_comp.encoding()

    return (deflated, str(huff_comp.frequency))


def inflate_message(encoded_message, huff_tree_str):
    """
    Decode the message accordingly to the deflate using
    LZ77 and Huffman algorithm
    """
    exmp = Huffman_algorithm('')
    exmp.frequency = eval(huff_tree_str)
    exmp.binary_tree()
    exmp.set_dictionary()
    exmp.encode = encoded_message
    lz77_en = exmp.decoding()
    inflated = decompress_message(lz77_en)
    return inflated
