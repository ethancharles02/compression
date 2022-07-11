from os import fstat, path, remove as os_remove
from src.algorithms.pattern_compression.pattern_constants import *
from src.algorithms.pattern_compression.pattern_algorithm_d import Pattern_Algorithm_D
from bitarray import bitarray
from math import ceil
from src.basic_compressor import Basic_Compressor
from io import BufferedReader, BufferedRandom
from typing import Union

class WrongFileFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Pattern_Decompressor(Basic_Compressor):
    """ The pattern decompressor is used to facilitate decompressing of binary strings.

    Attributes:
        chunk_size (int): How many chunks to read in at a time
        _override_chunk_size (bool): Decides if the chunk size matters, if it doesn't, the whole file will be read in at once
        compressed_file_extension (str): The file extension to output to as a default
        pattern_algorithm (Pattern_Algorithm_D): Algorithm used for compression
        _leftover_bits (str): Bits leftover that weren't used in the current compression
        _bytes_read (int): Number of bytes that have been read
        _chunk_data (str): Current chunk data
        _output_data (str): Data that is used to output the decompressed data to a file

    Constructor Args:
        chunk_size (int): Same as attribute
        raw_delimiter (str): The delimiter before any changes are made for functionality
        pattern_count_num_bits (int): Number of bits used for storing the amount of patterns in a compressed string
        pattern_bit_offset (int): Offset for using bits for counting
        compressed_file_extension (str): Same as attribute
        override_chunk_size (bool): Same as attribute
        
    Class Methods:
        __init__(): Initializes the parent class, assigns attributes
        run() -> bool: Main function that decompresses a given file to an output file
        _check_and_update_io_files() -> str, str: Fixes any filepath issues and returns good filepaths (or errors)
        _append_binary_string_to_file() -> None: Appends a binary string to a file
        _read_chunk_data_to_delimiter() -> str: Reads in data to a safe point that won't be in the middle of a delimiter
        _get_num_bits_needed_for_pattern_count() -> int: Gets the number of bits needed to get the pattern count
        _read_bits() -> str | bool: Reads in a number of bits
        _cutoff_data() -> str: Cuts the data off at a safe place for decompression
        _get_safe_cutoff_index() -> int: Finds the index for cutting off the data
        _get_new_chunk_data() -> str: Gets new data to be decompressed
        _read_chunk_data() -> str: Reads in a number of bytes
        _convert_hex_bytes_to_bits() -> str: Converts bytes into bits
    """
    def __init__(self, 
                chunk_size:int = 1024, 
                raw_delimiter:str = None, 
                pattern_count_num_bits:int = None, 
                pattern_bit_offset:int = None, 
                compressed_file_extension:str = None, 
                override_chunk_size:bool = False):
        """ Initializes the parent class, assigns attributes

        Constructor Args:
            chunk_size (int): Same as attribute
            raw_delimiter (str): The delimiter before any changes are made for functionality
            pattern_count_num_bits (int): Number of bits used for storing the amount of patterns in a compressed string
            pattern_bit_offset (int): Offset for using bits for counting
            compressed_file_extension (str): Same as attribute
            override_chunk_size (bool): Same as attribute
        """
        self.chunk_size = chunk_size
        self._override_chunk_size = override_chunk_size

        if raw_delimiter is None:
            raw_delimiter = RAW_DELIMITER
        if pattern_count_num_bits is None:
            pattern_count_num_bits = PATTERN_COUNT_NUM_BITS
        if pattern_bit_offset is None:
            pattern_bit_offset = PATTERN_BIT_OFFSET
        if compressed_file_extension is None:
            compressed_file_extension = OUT_FILE_EXTENSION
        self.compressed_file_extension = compressed_file_extension
        super().__init__(compressed_file_extension)

        self.pattern_algorithm = Pattern_Algorithm_D(raw_delimiter, pattern_count_num_bits, pattern_bit_offset)

        self._leftover_bits = ""
        self._bytes_read = 0
        self._chunk_data = None
        self._output_data = ""

    def run(self, input_file:str, output_file:str = None) -> bool:
        """ Main function that compresses a given file to an output file

        Arguments:
            input_file (str): File to be compressed
            output_file (str): Output file
        """
        input_file, output_file = self._check_and_update_io_files(input_file, output_file)
        with open(input_file, "rb") as in_f:
            with open(output_file, "ab+") as out_f:
                if self._override_chunk_size:
                    self.chunk_size = fstat(in_f.fileno()).st_size

                self._chunk_data = self._read_chunk_data_to_delimiter(in_f, self.chunk_size)
                while self._chunk_data:

                    self.pattern_algorithm.decompress(self._chunk_data)
                    self._output_data += self.pattern_algorithm.get_decompressed_data()
                    if len(self._output_data) % 8 == 0:
                        self._append_binary_string_to_file(out_f, self._output_data)
                        self._output_data = ""

                    self._chunk_data = self._read_chunk_data_to_delimiter(in_f, self.chunk_size)

                if self._output_data:
                    self._append_binary_string_to_file(out_f, self._output_data)
                    self._output_data = ""
        
        return True


        # If an output file isn't specified, use the input with a replaced file extension
        if out_file is None:
            out_file = self._remove_file_extension(in_file)
        elif path.isdir(out_file):
            out_file = path.join(out_file, self._remove_file_extension(path.basename(in_file)))
        
        # If the output file already exists, it will remove it first
        if not path.exists(in_file):
            raise(FileNotFoundError())
        # If the output file already exists, it will remove it first
        if path.exists(out_file):
            os_remove(out_file)
        # If the directory given doesn't exist, it will error
        if not path.exists(path.dirname(out_file)):
            raise(Exception(f"No path found to the directory: {path.dirname(out_file)}"))

        return in_file, out_file

    def _append_binary_string_to_file(self, file:BufferedRandom, string:str):
        """ Appends a binary string to a file

        Arguments:
            file (BufferedRandom): Output file
            string (str): String to append
        """
        bitarr = bitarray(list(map(int, string)))

        file.write(bitarr)

    def _read_chunk_data_to_delimiter(self, file:BufferedReader, chunk_size:int = 1) -> str:
        """ Reads in data to a safe point that won't be in the middle of a delimiter

        Arguments:
            file (BufferedReader): File to read from
            chunk_size (int): Number of bytes to read
        """
        data = self._get_new_chunk_data(file, chunk_size)
        if data:
            num_delimiters = data.count(self.pattern_algorithm._delimiter)

            while num_delimiters % 2 != 0:
                new_data = self._get_new_chunk_data(file, 1)
                if new_data:
                    data = data + new_data
                    num_delimiters = data.count(self.pattern_algorithm._delimiter)
                else:
                    last_delimiter_index = data.rfind(self.pattern_algorithm._delimiter)
                    data = data[:last_delimiter_index]
                    break

            last_delimiter_index = data.rfind(self.pattern_algorithm._delimiter)
            if last_delimiter_index != -1:
            
                num_bits_needed = self._get_num_bits_needed_for_pattern_count(len(data), last_delimiter_index)
                if num_bits_needed > 0:
                    new_bits = self._read_bits(file, num_bits_needed)
                    if new_bits:
                        data = data + new_bits
            
        return data

    def _get_num_bits_needed_for_pattern_count(self, data_length:int, last_delimiter_index:int) -> int:
        """ Gets the number of bits needed to get the pattern count

        Arguments:
            data_length (int): Length of the data
            last_delimiter_index (int): Last position of a delimiter in the data
        """
        bits_needed = self.pattern_algorithm.pattern_count_num_bits - ((data_length - last_delimiter_index) - self.pattern_algorithm._delimiter_length)
        if bits_needed > 0:
            return bits_needed
        else:
            return 0
    
    def _read_bits(self, file:BufferedReader, num_bits:int) -> Union[str, bool]:
        """ Reads in a number of bits

        Arguments:
            file (BufferedReader): Input file
            num_bits (int): Number of bits to read in
        """
        num_leftover_bits = len(self._leftover_bits)
        additional_needed_bits = num_bits - num_leftover_bits
        if additional_needed_bits <= 0:
            output = self._leftover_bits[:num_bits]
            self._leftover_bits = self._leftover_bits[num_bits:]
            return output
        else:
            bytes_to_read = ceil(additional_needed_bits / 8)
            new_bits = self._read_chunk_data(file, bytes_to_read)
            if new_bits:
                output = self._leftover_bits + new_bits[:additional_needed_bits]

                self._leftover_bits = new_bits[additional_needed_bits - num_leftover_bits:]
                return output
            else:
                return False

    def _cutoff_data(self, data:str) -> str:
        """ Cuts the data off at a safe place for decompression

        Arguments:
            data (str): The data to cut off
        """
        if self._leftover_bits:
            raise Exception(f"There are leftover bits that shouldn't exist: {self._leftover_bits}")

        cutoff_index_needed = True

        test_string = data[-((self.pattern_algorithm._delimiter_length - 1) * 2):]
        if self.pattern_algorithm.raw_delimiter in test_string:
            relative_index = test_string.rfind(self.pattern_algorithm.raw_delimiter)

            if relative_index <= len(test_string) - self.pattern_algorithm._delimiter_length:
                index = -(len(test_string) - (relative_index + self.pattern_algorithm._delimiter_length))
                cutoff_index_needed = False
            else:
                cutoff_index_needed = True

        if cutoff_index_needed:
            string = data[-(self.pattern_algorithm._delimiter_length - 1):]
            relative_index = self._get_safe_cutoff_index(string)

            index = -(len(string) - relative_index)

        if index < 0:
            self._leftover_bits = data[index:]
            return data[:index]
        else:
            return data

    def _get_safe_cutoff_index(self, string:str) -> int:
        """ Finds the index for cutting off the data

        Arguments:
            string (str): String to find the index for
        """
        for i in range(len(string)):
            check_string = string[i:] + self.pattern_algorithm._delimiter[-(i + 1):]
            if check_string == self.pattern_algorithm._delimiter:
                return i
        return i + 1

    def _get_new_chunk_data(self, file:BufferedReader, chunk_size:int = 1) -> str:
        """ Gets new data to be compressed

        Arguments:
            file (BufferedReader): Input file
            chunk_size (int): Number of bytes to read in
        """
        output = self._leftover_bits + self._read_chunk_data(file, chunk_size)
        self._leftover_bits = ""

        if output:
            return self._cutoff_data(output)
        else:
            return ""

    def _read_chunk_data(self, file:BufferedReader, chunk_size:int = 1) -> str:
        """ Reads in a number of bytes

        Arguments:
            file (BufferedReader): Input file
            chunk_size (int): Number of bytes to read in
        """
        data = file.read(chunk_size)
        if data:
            self._bytes_read += chunk_size
            return self._convert_hex_bytes_to_bits(data)
        else:
            return ""

    def _convert_hex_bytes_to_bits(self, hex_bytes:bytes) -> str:
        """ Converts bytes into bits

        Arguments:
            hex_bytes (bytes): Bytes to be converted to bits
        """
        binary_string = bin(int(hex_bytes.hex(), base=16))[2:]
        num_leading_zeroes = (8 - len(bin(int(hex_bytes.hex(), base=16))[2:])) % 8
        return "0" * num_leading_zeroes + binary_string

if __name__ == "__main__":
    decompressor = Pattern_Decompressor()

    data = "0000000000 010110 1111011".replace(" ", "")
    print(decompressor._cutoff_data(data), decompressor._leftover_bits)