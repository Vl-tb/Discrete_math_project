# Discrete Math Project
We made up a program, which can use different algorithms for compression and decompression of the files.

***


# Table of contents
#### [Discrete Math Project](#discrete_math_project)

#### [Table of contents](#table-of-contents)

#### [Input and output](#input-and-output)

#### [Program structure](#program-structure)

#### [Usage](#usage)

#### [Licence](#licence)

***


# Input and output
### Input
* Give us your file
* Choose algorithm for compression or decompression.
### Output
* File (compressed or decompressed, depending on your choise).

***


# Program structure
### `LZ77.py`
LZ77 algorithm.
* `compress_message`
Compresses message by using LZ77 algorithm.

* `decompress_message`
Decompresses message by using LZ77 algorithm.


### `LZW.py`
LZW algorithm.
* `lzw_compression`
Compresses message by using LZW algorithm.

* `lzw_decompression`
Decompresses message by using LZW algorithm.


### `HUFFMAN.py`
Huffman algorithm.

#### `Node`
This class represents a node for binary tree.

* `get_value`
Gets the node's value.

* `set_left_ch`
Sets node's left_child as node object.

* `set_right_ch`
Sets node's right_child as node object.

* `get_left_ch`
Gets node's left_child as node object.

* `get_right_ch`
Gets node's right_child as node object.

* `__str__`
Prints the node's value.


#### `Tree`
This class represents binary tree.

* `set_root`
Set a root of this tree.

* `get_root`
Get a root of this tree.

* `postorder`
One of possible traversals.

* `is_leaf`
This method checks if item is lead in binary tree.

* `huffman_code`
Prints path ti the leafs in binary tree.

* `recurse`
Used for creation paths.


#### `Huffman_algorithm`
This class can encode and decode files due to Huffman algorithm, based on using binary tree.

* `set_data`
Sets a needed string.

* `set_frequency_list`
Creates attribute self.frequency, which contains tuples of chars and times it repeated in data-string.

* `frequency_sort`
This method finds place for inserting a new node in the self.frequency.

* `binary_tree`
Creates a Huffman-tree, what is actually the binary-tree.

* `set_dictionary`
Creates a dictionary for encoding & decoding due Huffman algorithm.

* `encoding`
Encodes data (string value) to binary string.

* `decoding`
Decodes encoded data to initial format.


### `DEFLATE.py`
Deflate algorithm.

* `deflate`
Using LZ77 and Huffman's coding encodes data.

* `inflate`
Using Huffman's coding and LZ77 decodes data.

***


# Usage
1. Compress your files when you don't need it so it won't use a lot of memory.
2. When you want to work with this files - just decompress them.
3. PROFIT

***


# Licence
Information for players provided by:
* https://csgostats.gg/
* https://steamcommunity.com/'


MIT License

Copyright (c) 2021 Vl-tb

***
