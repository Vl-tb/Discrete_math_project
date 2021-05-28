""" module with class GrayscaleImageADT,
use to convert photo with grayscale mod """

from io import StringIO
from PIL import Image, ImageOps
from arrays import DynamicArray, Array2D


class GrayscaleImage:
    """ class GrayscaleImage, for working with photos """
    def __init__(self, nrows: int, ncols: int) -> None:
        self.photo = Array2D(nrows, ncols)
        self.photo.clear(0)

    def width(self) -> int:
        """ Returns the width of the image. """
        return self.photo.num_cols()

    def height(self) -> int:
        """ Returns the height of the image. """
        return self.photo.num_rows()

    def clear(self, value: int) -> None:
        """
        Cleans the image by setting each pixel to a value. The value value
        should be in the range 0 to 255.
        """
        if 0 <= value < 256:
            self.photo.clear(value)
        else:
            raise ValueError(f'Can\'t clear photo with val: {value}')

    def getitem(self, row, col) -> int:
        """
        Returns the intensity value in a given pixel. Pixel coordinates must
        be in the correct range.
        """
        return self.photo[row, col]

    def setitem(self, row, col, value) -> None:
        """
        Set the intensity value for a given pixel. Pixel coordinates must
        be in the correct range. The value value should be
        in the range 0 to 255.
        """
        if 0 <= value < 256:
            self.photo[row, col] = value
        else:
            raise ValueError(f'Can\'t clear photo with val: {value}')

    @staticmethod
    def from_file(path: str) -> object:
        """
        Create an instance of a class based on an image saved
        in png or jpg format.
        """
        image_grayscale = ImageOps.grayscale(Image.open(rf"{path}"))
        pixels_info = image_grayscale.getdata()
        image_array = GrayscaleImage(*image_grayscale.size[::-1])
        index_by_row = 0
        for i in range(image_array.height()):
            for j in range(image_array.width()):
                image_array.setitem(i, j, pixels_info[j + index_by_row])
            index_by_row += image_array.width()
        return image_array

    def lzw_compression(self) -> DynamicArray:
        """ Image compression using the Lempel-Ziv-Welch algorithm (LZW). """
        dictionary = {str(i): i for i in range(10)}
        dictionary[','] = 10
        dictionary['\n'] = 11
        dict_size = 12

        rows_str = '\n'.join(','.join(list(map(str, current_row)))
                             for current_row in self.photo)
        sequence = ""
        compressed_im = DynamicArray()
        for char in rows_str:
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

    @staticmethod
    def lzw_decompression(compressed_photo: DynamicArray) -> object:
        """
        Reproduction of an image that has been compressed using
        the Lempel-Ziv-Welch (LZW) algorithm.
        """
        dictionary = {i: str(i) for i in range(10)}
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


if __name__ == '__main__':
    photo = GrayscaleImage.from_file('alone-with.jpg')
    compressed_image = photo.lzw_compression()
    print(len(compressed_image))
    print(photo.width()*photo.height())
    encoded_im = GrayscaleImage.lzw_decompression(compressed_image)
    print(encoded_im.width() * encoded_im.height())
