# TODO
# Test with chunks enabled
# Update input parameters to consistent with the decompressor
# Make parent class for similar methods and attributes
# Consider adjusting the output to only do the final delimiter with bits at the end of the file
# Read in bits to get the chunk to be appended to be in byte format

from typing import Union
from os import path, fstat, remove as os_remove
from src.algorithms.pattern_compression.pattern_algorithm_c import Pattern_Algorithm_C
# from time import monotonic
from src.algorithms.pattern_compression.pattern_constants import *
from bitarray import bitarray
from math import ceil
from src.basic_compressor import Basic_Compressor
from io import BufferedReader

class Pattern_Compressor(Basic_Compressor):
    """ The pattern compressor is used to facilitate compressing of binary strings.
    Once the compression happens, any raw delimiters that exist are replaced with the corresponding delimiter string that won't mess with the delimiter.
    Compression only happens if bits will be saved in the process, it will place a delimiter before the pattern and one after to indicate that it is the pattern.
    After that second delimiter, a number of bits will indicate how many times the pattern occurs. If the number of bits isn't set, a third delimiter will exist at the end of the number to indicate this

    Attributes:
        _override_chunk_size (bool): Decides if the chunk size matters, if it doesn't, the whole file will be read in at once
        chunk_size (int): How many chunks to read in at a time
        compressed_file_extension (str): The file extension to output to as a default
        pattern_algorithm (Pattern_Algorithm_C): Algorithm used for compression
        _chunk_data (str): Current chunk data
        _leftover_bits (str): Bits leftover that weren't used in the current compression
        _bytes_read (int): Number of bytes that have been read
        _num_bits_output (int): Number of bits that have been written (used for making sure that the final output is of a multiple of 8)
        _file_size (int): Size of the file in bytes
        _print_time (float): How long to wait before printing completion percent
        _print_cur_time (float): Current time
        override_compression_check (bool): Decides if compression should be forcibly output even if the file ends up being larger than the input

    Constructor Args:
        chunk_size (int): Same as attribute
        pattern_bit_offset (int): Offset for using bits for counting
        max_look_ahead (int): Maximum value for looking ahead in the bit string
        raw_delimiter (str): The delimiter before any changes are made for functionality
        pattern_count_num_bits (int): Number of bits used for storing the amount of patterns in a compressed string
        compressed_file_extension (str): Same as attribute
        override_compression_check (bool): Same as attribute
        override_chunk_size (bool): Same as attribute
    
    Class Methods:
        __init__(): Initializes the parent class, assigns attributes
        run() -> bool: Main function that compresses a given file to an output file
        _get_final_output_string() -> str: Gets the end string needed to get the final output into byte format
        _append_binary_string_to_file() -> None: Appends a binary string to a file
        _compressed_successfully() -> bool: Compares the output file to the input file to see if the file was actually compressed
        _print_percentage_completion() -> None: Prints the percentage of completion
        _get_percentage_completion() -> float: Gets the percentage of completion
        _get_new_data() -> str: Gets new data to be compressed
        _read_chunk_data() -> str: Reads in a number of bytes
        _read_bits() -> str | bool: Reads in a number of bits
        _convert_hex_bytes_to_bits() -> str: Converts bytes into bits
        _check_and_update_io_files() -> str, str: Fixes any filepath issues and returns good filepaths (or errors)
    """
    def __init__(self, 
                chunk_size:int = 1024,
                pattern_bit_offset:int = None,
                max_look_ahead:int = None, 
                raw_delimiter:str = None, 
                pattern_count_num_bits:int = None, 
                compressed_file_extension:str = None, 
                override_compression_check:bool = False, 
                override_chunk_size:bool = False):
        """ Initializes the parent class, assigns attributes

        Constructor Args:
            chunk_size (int): Same as attribute
            pattern_bit_offset (int): Offset for using bits for counting
            max_look_ahead (int): Maximum value for looking ahead in the bit string
            raw_delimiter (str): The delimiter before any changes are made for functionality
            pattern_count_num_bits (int): Number of bits used for storing the amount of patterns in a compressed string
            compressed_file_extension (str): Same as attribute
            override_compression_check (bool): Same as attribute
            override_chunk_size (bool): Same as attribute
        """

        self._override_chunk_size = override_chunk_size
        self.chunk_size = chunk_size
        if pattern_bit_offset is None:
            pattern_bit_offset = PATTERN_BIT_OFFSET
        if max_look_ahead is None:
            max_look_ahead = MAX_LOOK_AHEAD
        if raw_delimiter is None:
            raw_delimiter = RAW_DELIMITER
        if pattern_count_num_bits is None:
            pattern_count_num_bits = PATTERN_COUNT_NUM_BITS
        if compressed_file_extension is None:
            compressed_file_extension = OUT_FILE_EXTENSION
        self.compressed_file_extension = compressed_file_extension
        super().__init__(compressed_file_extension)

        self.pattern_algorithm = Pattern_Algorithm_C(max_look_ahead = max_look_ahead, raw_delimiter = raw_delimiter, pattern_count_num_bits = pattern_count_num_bits, pattern_bit_offset = pattern_bit_offset)

        self._chunk_data = None
        self._leftover_bits = ""
        self._bytes_read = 0
        self._num_bits_output = 0
        self._file_size = 0
        # self._print_time = 5
        # self._print_cur_time = 0

        self.override_compression_check = override_compression_check
        
    def run(self, in_file:str, out_file:str = None) -> bool:
        """ Main function that compresses a given file to an output file

        Arguments:
            in_file (str): File to be compressed
            out_file (str): Output file
        """
        # Create initial compressed file
        in_filepath, out_filepath = self._check_and_update_io_files(in_file, out_file)

        f = open(out_filepath, 'wb+')
        f.close()
        
        with open(in_filepath, 'rb') as f:
            self._file_size = fstat(f.fileno()).st_size

            if self._override_chunk_size:
                self.chunk_size = self._file_size
            
            # Get chunk data
            self._chunk_data = self._get_new_data(f, self.chunk_size)

            # self._print_cur_time = monotonic()

            # As long as there is more data to read:
            while self._chunk_data:
                # if monotonic() - self._print_cur_time >= self._print_time:
                #     self._print_percentage_completion(2)
                #     self._print_cur_time = monotonic()

                # Compress the chunk
                self.pattern_algorithm.compress(self._chunk_data)

                self._append_binary_string_to_file(out_filepath, f, self.pattern_algorithm.get_compressed_data())
                
                # Get new chunk data
                self._chunk_data = self._get_new_data(f, self.chunk_size)
            self._print_percentage_completion(2)
        
        if self.override_compression_check:
            return True
        if self._compressed_successfully(in_filepath, out_filepath):
            return True
        else:
            os_remove(out_filepath)
            return False

    def _get_final_output_string(self, num_bits:int) -> str:
        """ Gets the end string needed to get the final output into byte format

        Arguments:
            num_bits (int): Number of bits needed
        """
        if num_bits != 0:
            num_zeroes_needed = (num_bits - self.pattern_algorithm._delimiter_length) % 8
            return self.pattern_algorithm._delimiter + "0" * num_zeroes_needed
        else:
            return ""

    def _append_binary_string_to_file(self, filepath:str, file:BufferedReader, string:str):
        """ Appends a binary string to a file

        Arguments:
            filepath (str): Output filepath
            file (BufferedReader): Input file
            string (str): String to append
        """
        string_length = len(string)

        needed_bits = (8 - string_length) % 8
        if needed_bits != 0:
            new_bits = self._read_bits(file, needed_bits)
            if new_bits:
                string = string + new_bits
            else:
                string = string + self._get_final_output_string(needed_bits)

        self._num_bits_output += string_length

        bitarr = bitarray(list(map(int,string)))

        with open(filepath,"ab+") as new_f:
            new_f.write(bitarr)

    def _compressed_successfully(self, input_filepath:str, output_filepath:str) -> bool:
        """ Compares the output file to the input file to see if the file was actually compressed

        Arguments:
            input_filepath, output_filepath (str): Filepaths to compare
        """
        with open(input_filepath, 'rb') as f:
            input_size = fstat(f.fileno()).st_size

        with open(output_filepath, 'rb') as f:
            output_size = fstat(f.fileno()).st_size
        
        return output_size < input_size

    def _print_percentage_completion(self, decimals:int):
        """ Prints the percentage of completion

        Arguments:
            decimals (int): Number of decimals to round to
        """
        print(f"{round(self._get_percentage_completion() * 100, decimals)}%")

    def _get_percentage_completion(self) -> float:
        """ Gets the percentage of completion
        """
        if self._file_size > 0:
            percent = self._bytes_read / self._file_size
            return percent if percent < 1 else 1
        else:
            return 1
    
    def _get_new_data(self, file:BufferedReader, chunk_size:int = 1) -> str:
        """ Gets new data to be compressed

        Arguments:
            file (BufferedReader): Input file
            chunk_size (int): Number of bytes to read in
        """
        output = self._leftover_bits + self._read_chunk_data(file, chunk_size)
        self._leftover_bits = ""
        return output

    def _read_chunk_data(self, file:BufferedReader, chunk_size:int = 1) -> str:
        """ Reads in a number of bytes

        Arguments:
            file (BufferedReader): Input file
            chunk_size (int): Number of bytes to read in
        """
        self._bytes_read += chunk_size
        data = file.read(chunk_size)
        if data:
            return self._convert_hex_bytes_to_bits(data)
        else:
            return ""
    
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

    def _convert_hex_bytes_to_bits(self, hex_bytes:bytes) -> str:
        """ Converts bytes into bits

        Arguments:
            hex_bytes (bytes): Bytes to be converted to bits
        """
        binary_string = bin(int(hex_bytes.hex(), base=16))[2:]
        num_leading_zeroes = (8 - len(bin(int(hex_bytes.hex(), base=16))[2:])) % 8
        return "0" * num_leading_zeroes + binary_string

    def _check_and_update_io_files(self, in_file:str, out_file:str = None):
        """ Fixes any filepath issues and returns good filepaths (or errors)

        Arguments:
            in_file (str): Input file, this is expected to be a good path to a file
            out_file (str): Output file, this is flexible and can take information from the input file if not enough is given
        """
        # If an output file isn't specified, use the input with a replaced file extension
        if out_file is None:
            out_file = in_file + self.compressed_file_extension
        elif path.isdir(out_file):
            out_file = path.join(out_file, path.basename(in_file) + self.compressed_file_extension)
        
        # If the input file doesn't exist, an error will be raised
        if not path.exists(in_file):
            raise(FileNotFoundError())
        # If the output file already exists, it will remove it first
        if path.exists(out_file):
            os_remove(out_file)
        # If the directory given doesn't exist, it will error
        if not path.exists(path.dirname(out_file)):
            raise(Exception(f"No path found to the directory: {path.dirname(out_file)}"))

        return in_file, out_file

if __name__ == "__main__":
    COMPRESSION_FOLDER = "Research_Testing/random_bitstring_files"

    file_compressor = Pattern_Compressor(15)
    print(file_compressor._get_file_extension("test.txt"))