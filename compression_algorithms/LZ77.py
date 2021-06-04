""" Implementation of LZ77 compression algrorithm """


def compress_message(src):
    """
    Compress the given string. Replace similar occurences
    with #copy,steps_back#
    """
    packed_message = ''

    run_idx = 0
    main_len = len(src)
    cache = {}

    while run_idx < len(src):
        length = min(256, main_len-run_idx)
        found = False

        while not found and length > 4:
            copy_idx = run_idx - length
            message = src[run_idx:run_idx + length]
            try:
                copy_idx = cache[message]
                if copy_idx + length < run_idx:
                    packed_message += f"#{length},{run_idx - copy_idx}#"
                    run_idx += length
                    found = True
                    break
                else:
                    length -= 1
            except KeyError:
                cache[message] = run_idx
                length -= 1

        if not found:
            packed_message += src[run_idx]
            run_idx += 1

    return packed_message


def decompress_message(encoded_message):
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