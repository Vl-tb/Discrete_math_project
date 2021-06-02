import base64
from compression_algorithms.LZW import lzw_compression, lzw_decompression
from compression_algorithms.DEFLATE import deflate, inflate
from compression_algorithms.LZ77 import compress_message, decompress_message


def compress(path: str, path_compressed: str, function: callable):
    with open(path, "rb") as file_to_compress:
        bits = base64.b64encode(file_to_compress.read())
        string = ''
        for bit in bits:
            string += chr(bit)

    compressed = function(string)
    with open(path_compressed, 'w') as compressed_file:
        compressed_file.write(compressed)


def decompress(path_compressed: str, path_decompressed: str, function: callable):
    with open(path_compressed, 'r') as compressed_file:
        compressed = compressed_file.read()
    decompressed = function(compressed)
    with open(path_decompressed, "wb") as file_to_decompress:
        file_to_decompress.write(base64.b64decode(decompressed))


if __name__ == '__main__':
    print("-------")
    compress(path='example_files/example.mp4',
             path_compressed='example_files/tests_files/example_compressed.mp4.txt',
             function=compress_message)
    print("!!!!!!")
    decompress(path_compressed='example_files/tests_files/example_compressed.mp4.txt',
               path_decompressed='example_files/tests_files/example_decompressed.mp4',
               function=decompress_message)
    print("-------")
    compress(path='example_files/example.mp4',
             path_compressed='example_files/tests_files/example_compressed.mp4.txt',
             function=deflate)
    print("!!!!!!")
    decompress(path_compressed='example_files/tests_files/example_compressed.mp4.txt',
               path_decompressed='example_files/tests_files/example_decompressed.mp4',
               function=inflate)
