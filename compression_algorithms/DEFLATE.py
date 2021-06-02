from compression_algorithms.LZ77 import compress_message, decompress_message
import compression_algorithms.HUFFMAN as huff


def deflate(data):
    lz77_en = compress_massage(data)
    huff_comp = huff.Huffman_algorithm(lz77_en)
    deflated = huff_comp.encoding()
    return deflated


def inflate(data):
    huff_comp = huff.Huffman_algorithm(data)
    # huff_comp.binary_tree()
    lz77_en = huff_comp.decoding()
    inflated = decompress_massage(data)
    return inflated
