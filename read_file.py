import base64
from compression_algorithms.LZW import lzw_compression

with open("example_files/example.mp4", "rb") as videoFile:
    bits = base64.b64encode(videoFile.read())
    string = ''
    for bit in bits:
        string += chr(bit)

    compress = lzw_compression(string)

    with open('file_before.txt', 'wb') as file:
        file.write(bits)
    with open('file_after.txt', 'w') as file:
        file.write(' '.join(map(str, compress)))

    # print(compress)
    # print(len(bits))

    ###########################################################################

    # file = open("textTest1.txt", "wb")
    # file.write(bits)
    # file.close()
    # for bit in bits[:10]:
    #     print(f'{bit} {type(bit)}')
    # file = open("textTest2.txt", "w")
    # file.write(string)
    # file.close()

    ###########################################################################

    # fh = open("video.mp4", "wb")
    # fh.write(base64.b64decode(string))
    # fh.close()
