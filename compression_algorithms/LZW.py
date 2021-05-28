def lzw_compression(string) -> str:
    """ compression using the Lempel-Ziv-Welch algorithm (LZW). """
    chars = set()
    for char in string:
        chars.add(char)
    dictionary = {val: i for i, val in enumerate(chars)}
    dict_size = len(dictionary)

    sequence = ""
    compressed_im = []
    for char in string:
        sequence_char = sequence + char
        if sequence_char in dictionary:
            sequence = sequence_char
        else:
            compressed_im.append(dictionary[sequence])
            dictionary[sequence_char] = dict_size
            dict_size += 1
            sequence = char

    # Output the code for sequence.
    if sequence:
        compressed_im.append(dictionary[sequence])
    return compressed_im


def lzw_decompression(compressed_photo: DynamicArray) -> object:
    """
    Reproduction of an image that has been compressed using
    the Lempel-Ziv-Welch (LZW) algorithm.
    """
    dictionary = {i:str(i) for i in range(10)}
    dictionary[10] = ','
    dictionary[11] = '\n'
    dict_size = 12

    encoded_str = StringIO()
    sequence = str(compressed_photo[0])
    compressed_photo.remove(compressed_photo[0])
    encoded_str.write(sequence)
    for char in compressed_photo:
        if char in dictionary:
            entry = dictionary[char]
        elif char == dict_size:
            entry = sequence + sequence[0]
        else:
            raise ValueError(f'Bad compressed k: {char}')
        encoded_str.write(entry)

        dictionary[dict_size] = sequence + entry[0]
        dict_size += 1
        sequence = entry
    encoded_str = encoded_str.getvalue()
    encoded_arr = DynamicArray()
    rows = 0
    encoded_arr.append(DynamicArray())
    num = ''
    for char in encoded_str:
        if char == ',':
            encoded_arr[rows].append(int(num))
            num = ''
        elif char == '\n':
            encoded_arr[rows].append(int(num))
            encoded_arr.append(DynamicArray())
            rows += 1
            num = ''
        else:
            num += char
    arr_2d = GrayscaleImage(len(encoded_arr), len(encoded_arr[0]))
    for i, dynamic_arr in enumerate(iter(encoded_arr)):
        for j, val in enumerate(iter(dynamic_arr)):
            arr_2d.setitem(i, j, val)
    return arr_2d
