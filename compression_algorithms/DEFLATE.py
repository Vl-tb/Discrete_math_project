import base64


def deflate(data: str):
    data = data.encode("UTF-8")
    data = base64.b64encode(data)
    compressed = zlib.compress(data)
    return compressed


def inflate(data: bytes):
    decompressed = zlib.decompress(data)
    decompressed = base64.b64decode(decompressed)
    result = decompressed.decode("UTF-8")
    return result


import heapq
from heapq import heappop, heappush


# HUFFMAN PART
def isLeaf(root):
    return root.left is None and root.right is None
 
 
class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right


    def __lt__(self, other):
        return self.freq < other.freq


# Traverse the Huffman Tree and store Huffman Codes in a dictionary
def encode(root, str, huffman_code):
    if root is None:
        return

    # find a leaf node
    if isLeaf(root):
        huffman_code[root.ch] = str if len(str) > 0 else '1'

    encode(root.left, str + '0', huffman_code)
    encode(root.right, str + '1', huffman_code)


# Traverse the Huffman Tree and decode the encoded string
def decode(root, index, str):
    if root is None:
        return index

    # find a leaf node
    if isLeaf(root):
        print(root.ch, end='')
        return index

    index = index + 1
    root = root.left if str[index] == '0' else root.right
    return decode(root, index, str)


# Builds Huffman Tree and decodes the given input text
def huff_encode(text):
    if len(text) == 0:
        return

    # count the frequency of appearance of each character and store it in a dictionary
    freq = {i: text.count(i) for i in set(text)}

    # Create a priority queue to store live nodes of the Huffman tree.
    pq = [Node(k, v) for k, v in freq.items()]
    heapq.heapify(pq)

    # do till there is more than one node in the queue
    while len(pq) != 1:

        # Remove the two nodes of the highest priority (the lowest frequency) from the queue
        left = heappop(pq)
        right = heappop(pq)

        # create a new internal node with these two nodes as children and
        # with a frequency equal to the sum of the two nodes' frequencies.
        # Add the new node to the priority queue.
        total = left.freq + right.freq
        heappush(pq, Node(None, total, left, right))

    # `root` stores pointer to the root of Huffman Tree
    root = pq[0]

    # traverse the Huffman tree and store the Huffman codes in a dictionary
    huffman_code = {}
    encode(root, "", huffman_code)

    # print("Huffman Codes are:", huffmanCode)
    # print("The original string is:", text)

    # print the encoded string
    str = ""
    for c in text:
        str += huffman_code.get(c)

    # print("The encoded string is:", str)

    return pq, str


def huff_decode(root, str):
    if isLeaf(root):
        # Special case: For input like a, aa, aaa, etc.
        while root.freq > 0:
            print(root.ch, end='')
            root.freq = root.freq - 1
    else:
        # traverse the Huffman Tree again and this time,
        # decode the encoded string
        index = -1
        while index < len(str) - 1:
            index = decode(root, index, str)


text = "SOme random message" * 100

tree, code = huff_encode(text)
huff_decode(tree[0], code)


# LZ77 PART
# coding=utf8
class LZ77:
	def __init__(self):
		self.reference_prefix = "`"
		self.reference_prefix_code = ord(self.reference_prefix)
		self.reference_int_base = 96
		self.reference_int_floor_code = ord(" ")
		self.reference_int_ceil_code = self.reference_int_floor_code + self.reference_int_base - 1
		self.max_string_distance = self.reference_int_base ** 2 - 1
		self.min_string_length = 5
		self.max_string_length = self.reference_int_base ** 1 - 1 + self.min_string_length
		self.max_window_length = self.max_string_distance + self.min_string_length;		
		self.default_window_length = 144


	def compress(self, data, window_length = None):
		"""Compresses text data using the LZ77 algorithm."""
		if window_length == None:
			window_length = self.default_window_length

		compressed = ""
		pos = 0
		lastPos = len(data) - self.min_string_length

		while pos < lastPos:
			search_start = max(pos - window_length, 0)
			match_length = self.min_string_length
			found_match = False
			best_match_distance = self.max_string_distance
			best_match_length = 0
			new_compressed = None

			while (search_start + match_length) < pos:
				m1 = data[search_start : search_start + match_length]
				m2 = data[pos : pos + match_length]
				is_valid_match = (m1 == m2 and match_length < self.max_string_length)

				if is_valid_match:
					match_length += 1
					found_match = True
				else:
					real_match_length = match_length - 1

					if found_match and real_match_length > best_match_length:
						best_match_distance = pos - search_start - real_match_length
						best_match_length = real_match_length

					match_length = self.min_string_length
					search_start += 1
					found_match = False

			if best_match_length:
				new_compressed = (self.reference_prefix + self.__encode_reference_int(best_match_distance, 2) + self.__encode_reference_length(best_match_length))
				pos += best_match_length
			else:
				if data[pos] != self.reference_prefix:
					new_compressed = data[pos]
				else:
					new_compressed = self.reference_prefix + self.reference_prefix
				pos += 1	

			compressed += new_compressed

		return compressed + data[pos:].replace("`", "``")


	def decompress(self, data):
		"""Decompresses LZ77 compressed text data"""
		decompressed = ""
		pos = 0
		while pos < len(data):
			curr_char = data[pos]
			if curr_char != self.reference_prefix:
				decompressed += curr_char
				pos += 1
			else:
				next_char = data[pos + 1]
				if next_char != self.reference_prefix:
					distance = self.__decode_reference_int(data[pos + 1 : pos + 3], 2)
					length = self.__decode_reference_length(data[pos + 3])
					start = len(decompressed) - distance - length
					end = start + length
					decompressed += decompressed[start : end]
					pos += self.min_string_length - 1
				else:
					decompressed += self.reference_prefix
					pos += 2

		return decompressed


	def __encode_reference_int(self, value, width):
		if value >= 0 and value < (self.reference_int_base ** width - 1):
			encoded = ""
			while value > 0:
				encoded = chr((value % self.reference_int_base) + self.reference_int_floor_code) + encoded
				value = int(value / self.reference_int_base)

			missing_length = width - len(encoded)
			for i in range(missing_length):
				encoded = chr(self.reference_int_floor_code) + encoded

            return encoded
        else:
            raise Exception("Reference value out of range: %d (width = %d)" % (value, width))


	def __encode_reference_length(self, length):
		return self.__encode_reference_int(length - self.min_string_length, 1)


	def __decode_reference_int(self, data, width):
		value = 0
		for i in range(width):
			value *= self.reference_int_base
			char_code = ord(data[i])
			if char_code >= self.reference_int_floor_code and char_code <= self.reference_int_ceil_code:
				value += char_code - self.reference_int_floor_code
			else:
				raise Exception("Invalid char code: %d" % char_code)

		return value


	def __decode_reference_length(self, data):
		return self.__decode_reference_int(data, 1) + self.min_string_length
