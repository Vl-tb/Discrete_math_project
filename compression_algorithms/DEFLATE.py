from LZ77 import compress_message, decompress_message
from HUFFMAN import HuffmanAlgorithm



def deflate_compress(src):
    """
    Encode the message accordingly to the deflate using
    LZ77 and Huffman algorithm
    """
    lz77_en = compress_message(src)
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
    inflated = decompress_message(lz77_en)
    return inflated


if __name__ == '__main__':
    message = 'fouugfhufhgjofhgjgohfokgjrpjgfojrhjfpowof  ddjgfjoierjgfgfiejrigjerihjgj foprkfokropfkok hpehplpl hlehleplhpeh'

    code = deflate_message(message)

    print(message == inflate_message(code))
