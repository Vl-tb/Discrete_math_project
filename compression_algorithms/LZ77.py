

def compress_message(src):
    """
    Compress the given string. Replace similar occurences
    with #copy,steps_back#
    """
    packed_message = ''

    run_idx = 0

    while run_idx < len(src):
        ln = 9
        found = False

        while not found and ln > 3:
            copy_idx =  run_idx - ln

            while copy_idx >= 0 and (run_idx-copy_idx) < 100:
                if src[run_idx: run_idx+ln] == src[copy_idx:copy_idx+ln]:
                    packed_message += f"#{ln}{run_idx-copy_idx}#"
                    run_idx += ln
                    found = True
                    break

                copy_idx -= 1
            ln -= 1

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
        length = int(encoded_message[i_pack+1])
        count = 3
        while encoded_message[i_pack+count] != '#':
            count += 1
        distance = int(encoded_message[i_pack+2:i_pack+count])
        unpack += unpack[i_unpack-distance:i_unpack-distance+length]
        i_unpack += length
        i_pack += count+1

    return unpack
