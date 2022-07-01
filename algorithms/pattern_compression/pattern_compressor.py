# TODO
# Add docstrings
# Add in a 1 or a 0 at the beginning of the output file only if dynamic bit storing is fixed
from os import path, listdir, fstat, remove as os_remove
from algorithms.pattern_compression.pattern_algorithm_c import Pattern_Algorithm_C
from time import monotonic
from algorithms.pattern_compression.pattern_constants import *
from bitarray import bitarray
from math import ceil
from basic_compressor import Basic_Compressor

class Pattern_Compressor(Basic_Compressor):
    def __init__(self, chunk_size=1024, pattern_bit_offset=None, max_look_ahead=None, raw_delimiter=None, pattern_count_num_bits=None, compressed_file_extension=None, override_compression_check=False, override_chunk_size=False):

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

        self.pattern_compressor = Pattern_Algorithm_C(max_look_ahead = max_look_ahead, raw_delimiter = raw_delimiter, pattern_count_num_bits = pattern_count_num_bits, pattern_bit_offset = pattern_bit_offset)
        # self.output_folder = None

        self._chunk_data = None
        self._leftover_bits = ""
        self._bytes_read = 0
        self._num_bits_output = 0
        self._file_size = 0
        self._print_time = 5
        self._print_cur_time = 0

        self.override_compression_check = override_compression_check
        
    def run(self, in_file:str, out_file=None):
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

            self._print_cur_time = monotonic()

            # As long as there is more data to read:
            while self._chunk_data:
                if monotonic() - self._print_cur_time >= self._print_time:
                    self._print_percentage_completion(2)
                    self._print_cur_time = monotonic()

                # Compress the chunk
                self.pattern_compressor.compress(self._chunk_data)

                self._append_binary_string_to_file(out_filepath, f, self.pattern_compressor.get_compressed_data())
                
                # Get new chunk data
                # self.chunk_data = f.read(self.chunk_size)
                self._chunk_data = self._get_new_data(f, self.chunk_size)
            self._print_percentage_completion(2)
        
        if self.override_compression_check:
            return True
        if self._compressed_successfully(in_filepath, out_filepath):
            return True
        else:
            os_remove(out_filepath)
            return False

    # def _patch_intersection_with_data(self):
    #     if self._data:
    #         split_length = self._raw_delimiter_length - 1
    #         mid_string = self._data[-1][-(split_length):] + self._working_string[:split_length]
    #         if self._raw_delimiter in mid_string:
    #             insert_index = mid_string.index(self._raw_delimiter) + self._raw_delimiter_length - split_length
    #             self._working_string = self._working_string[:insert_index] + self._replace_delimiter_character + self._working_string[insert_index:]

    def _get_file_extension(self, string:str):
        index = string.rfind(".")
        if index != -1:
            return string[index:]
        else:
            raise ValueError(f"File extension did not exist on the given file: {string}")

    def _get_final_output_string(self, num_bits):
        if num_bits != 0:
            num_zeroes_needed = (num_bits - self.pattern_compressor._delimiter_length) % 8
            return self.pattern_compressor._delimiter + "0" * num_zeroes_needed
        else:
            return ""

    def _append_binary_string_to_file(self, filepath, file, string:str):
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

    def _compressed_successfully(self, input_filepath, output_filepath):
        with open(input_filepath, 'rb') as f:
            input_size = fstat(f.fileno()).st_size

        with open(output_filepath, 'rb') as f:
            output_size = fstat(f.fileno()).st_size
        
        return output_size < input_size

    def _print_percentage_completion(self, decimals):
        print(f"{round(self._get_percentage_completion() * 100, decimals)}%")

    def _get_percentage_completion(self):
        if self._file_size > 0:
            percent = self._bytes_read / self._file_size
            return percent if percent < 1 else 1
        else:
            return 1
    
    def _get_new_data(self, file, chunk_size = 1):
        output = self._leftover_bits + self._read_chunk_data(file, chunk_size)
        self._leftover_bits = ""
        return output

    def _read_chunk_data(self, file, chunk_size = 1):
        self._bytes_read += chunk_size
        data = file.read(chunk_size)
        if data:
            return self._convert_hex_bytes_to_bits(data)
        else:
            return ""
    
    def _read_bits(self, file, num_bits):
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

    def _convert_hex_bytes_to_bits(self, hex_bytes):
        binary_string = bin(int(hex_bytes.hex(), base=16))[2:]
        num_leading_zeroes = (8 - len(bin(int(hex_bytes.hex(), base=16))[2:])) % 8
        return "0" * num_leading_zeroes + binary_string

    # def _is_chunk_data_on_delimiter(self):
    #     if self._chunk_data:
    #         pass

    def _check_and_update_io_files(self, in_file, out_file):
        # If an output file isn't specified, use the input with a replaced file extension
        if out_file is None:
            out_file = path.basename(in_file) + self.compressed_file_extension
            
        # If the input folder or output folders are specified, it updates the corresponding file with a path
        # if self.input_folder is not None:
        #     in_file = f"{self.input_folder}/{in_file}"
        # if self.output_folder is not None:
        #     out_file = f"{self.output_folder}/{out_file}"
        
        # If the input file doesn't exist, an error will be raised
        if not path.exists(in_file):
            raise(FileNotFoundError())
        if path.exists(out_file):
            os_remove(out_file)

        return in_file, out_file

if __name__ == "__main__":
    COMPRESSION_FOLDER = "Research_Testing/random_bitstring_files"

    file_compressor = Pattern_Compressor(15)
    print(file_compressor._get_file_extension("test.txt"))