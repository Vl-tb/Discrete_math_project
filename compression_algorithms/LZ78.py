
def lz78_compression(string):
    new_dict = {}
    dictionary = {}
    current_index = 0
    max_index = 0
    item = ""
    for i in range(len(string)):
        item += string[i]
        if item not in dictionary:
            max_index += 1
            dictionary[item] = (current_index,item[-1],max_index)
            item = ""
            current_index = 0
        else:
            current_index = dictionary[item][2]
    if current_index != 0:
        dictionary['*'] = (current_index,item[-1],max_index)

    for key in dictionary:
        tup = (dictionary[key][0],dictionary[key][1])
        new_dict[dictionary[key][2]] = tup

    output = transform(new_dict)
    return output

def transform(dictionary):
    output_string = ""
    for key in dictionary:
        output_string += str(dictionary[key][0])+str(dictionary[key][1])+" "
    output_string = output_string[:-1]
    return output_string


def detransform(string):
    dictionary = {}
    string = string.split(" ")
    counter = 1
    for element in string:
        dictionary[counter] = (int(element[:-1]),element[-1])
        counter += 1

    return str(dictionary)


def lz78_decompression(compressed_str):
    compressed = detransform(compressed_str)
    compressed = eval(compressed)
    output = ""
    output1 = ""
    dictionary = compressed

    for key in dictionary:
        initial_index = key
        if initial_index != 0:
            while initial_index != 0:

                if dictionary[initial_index][0] == 0:
                    output1 += dictionary[initial_index][1]
                    break

                output1 += str(dictionary[initial_index][1]) 

                initial_index = dictionary[initial_index][0]
                

            output +=  output1[::-1]
            output1 = ""

        elif dictionary[key] == "*":
            output += dictionary[key][1]
        else:
            output += str(dictionary[key][1])

    return output



if __name__ == '__main__':

    string = "aaabbbaaa"
    print("String\t",string)

    a = lz78_compression(string)

    print(a)
    print(lz78_decompression(a))