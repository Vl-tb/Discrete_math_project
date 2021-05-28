from io import StringIO


def lzw_compression(string) -> str:
    """ compression using the Lempel-Ziv-Welch algorithm (LZW). """
    # chars = set()
    # for char in string:
    #     chars.add(char)
    # dictionary = {val: str(i) for i, val in enumerate(chars)}
    # print(', '.join([f"'{val}': '{str(i)}'" for i, val in enumerate(sorted(list(chars)))]))
    # dict_size = len(dictionary)
    # print(dictionary)
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
                  'v':'60', 'w':'61', 'x':'62', 'y':'63', 'z':'64'}
    dict_size = 65

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
    print(f'len file       - {len(string)}')
    print(f'len compressed - {len(compressed_im)}')
    print(f'len dictionary - {len(dictionary)}')
    # print(dictionary)
    print(type(compressed_im))
    return ' '.join(compressed_im)


def lzw_decompression(compressed_photo_str: str) -> object:
    """
    Reproduction of an image that has been compressed using
    the Lempel-Ziv-Welch (LZW) algorithm.
    """
    compressed_photo = list(map(int, compressed_photo_str.split(' ')))
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
                  60:'v', 61:'w', 62:'x', 63:'y', 64:'z'}
    dict_size = 65

    encoded_str = StringIO()
    sequence = compressed_photo[0]
    compressed_photo.remove(compressed_photo[0])
    encoded_str.write(str(sequence))
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
        print(sequence)
    encoded_str = encoded_str.getvalue()
    # encoded_arr = []
    # rows = 0
    # encoded_arr.append([])
    # num = ''
    # for char in encoded_str:
    #     if char == ',':
    #         encoded_arr[rows].append(int(num))
    #         num = ''
    #     elif char == '\n':
    #         encoded_arr[rows].append(int(num))
    #         encoded_arr.append([])
    #         rows += 1
    #         num = ''
    #     else:
    #         num += char
    # arr_2d = [[None] * len(encoded_arr) for _ in range(len(encoded_arr[0]))]
    # for i, dynamic_arr in enumerate(iter(encoded_arr)):
    #     for j, val in enumerate(iter(dynamic_arr)):
    #         arr_2d[i][j] = val
    return encoded_str


if __name__ == '__main__':
    string = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    compress = lzw_compression(string)
    print(compress)
    print(lzw_decompression(compress))

    # diction = {'+':'0', '/':'1', '0':'2', '1':'3', '2':'4', '3':'5',
    #            '4':'6', '5':'7', '6':'8', '7':'9', '8':'10', '9':'11',
    #            '=':'12', 'A':'13', 'B':'14', 'C':'15', 'D':'16', 'E':'17',
    #            'F':'18', 'G':'19', 'H':'20', 'I':'21', 'J':'22', 'K':'23',
    #            'L':'24', 'M':'25', 'N':'26', 'O':'27', 'P':'28', 'Q':'29',
    #            'R':'30', 'S':'31', 'T':'32', 'U':'33', 'V':'34', 'W':'35',
    #            'X':'36', 'Y':'37', 'Z':'38', 'a':'39', 'b':'40', 'c':'41',
    #            'd':'42', 'e':'43', 'f':'44', 'g':'45', 'h':'46', 'i':'47',
    #            'j':'48', 'k':'49', 'l':'50', 'm':'51', 'n':'52', 'o':'53',
    #            'p':'54', 'q':'55', 'r':'56', 's':'57', 't':'58', 'u':'59',
    #            'v':'60', 'w':'61', 'x':'62', 'y':'63', 'z':'64'}
    # new_key = []
    # new_val = []
    # for key, val in diction.items():
    #     new_key.append(key)
    #     new_val.append(val)
    # print({key:val for key, val in zip(new_val, new_key)})
