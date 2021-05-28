import base64
from compression_algorithms.LZW import lzw_compression, lzw_decompression


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
    decompressed = lzw_decompression(compressed)
    with open(path_decompressed, "wb") as file_to_decompress:
        file_to_decompress.write(base64.b64decode(decompressed))


if __name__ == '__main__':
    compress(path='example_files/example.mp4',
             path_compressed='example_files/tests_files/example_compressed.mp4.txt',
             function=lzw_compression)
    decompress(path_compressed='example_files/tests_files/example_compressed.mp4.txt',
               path_decompressed='example_files/tests_files/example_decompressed.mp4',
               function=lzw_decompression)





# with open('file_before.txt', 'wb') as file:
#     file.write(bits)
# with open('file_after.txt', 'w') as file:
#     file.write(' '.join(map(str, compress)))
# encoded = lzw_decompression(compress)
# bit_str = str(bits)
# # print(bits)
# # print('----------------------------------------------------------')
# # print(bit_str)
# decompressed = lzw_decompression(compress)
# with open("example_files/video.mp4", "wb") as fh:
#     fh.write(base64.b64decode(decompressed))
#
# # decompressed = base64.b64encode(lzw_decompression(compress))
#
# # if len(bit_str) == len(encoded):
# #     for i, val in enumerate(bit_str):
# #         if val != encoded[i]:
# #             print(f'suka in {i}')
# # else:
# #     print('suka povna')
# #     print(f'bit_str - {len(bit_str)}\n'
# #           f'decompressed - {len(decompressed)}')
# # with open('example_files/encoded_example.mp4', 'wb') as file:
# #     file.write(decompressed)
# #
# # # 6845659
# # counter = 0
# # for i in range(336728):
# #     if decompressed[i] != bit_str[i]:
# #         print(f'bliat in {i}')
# #         print(f'decompressed - {decompressed[i]}\n'
# #               f'bit_str      - {bit_str[i]}')
# #         counter += 1
# #         if counter > 10:
# #             break
# # else:
# #     print('pizda')
#
#
# # print(compress)
# # print(len(bits))
#
# ###########################################################################
#
# # file = open("textTest1.txt", "wb")
# # file.write(bits)
# # file.close()
# # for bit in bits[:10]:
# #     print(f'{bit} {type(bit)}')
# # file = open("textTest2.txt", "w")
# # file.write(string)
# # file.close()
#
# ###########################################################################
#
# # fh = open("video.mp4", "wb")
# # fh.write(base64.b64decode(string))
# # fh.close()
