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
