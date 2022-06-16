# TODO
# Add docstrings
# Rename compressions to algorithm, create specific compressors for each algorithm
# Create decompressors for each algorithm
# Move/create constants for compressors
from os import path, listdir, fstat, remove as os_remove
from pattern_algorithm_c import Pattern_Algorithm_C
from time import monotonic
from pattern_constants import *

COMPRESSION_FOLDER = "Research_Testing/random_bitstring_files"

class Pattern_Compressor(object):
    def __init__(self, chunk_size=1024):
        self.chunk_size = chunk_size
        self.pattern_compressor = Pattern_Algorithm_C(max_look_ahead = MAX_LOOK_AHEAD, raw_delimiter = RAW_DELIMITER, pattern_count_num_bits = PATTERN_COUNT_NUM_BITS, pattern_bit_offset = PATTERN_BIT_OFFSET)
        self.input_folder = None
        self.output_folder = None

        self._chunk_data = None
        self._bits_read = 0
        self._file_size = 0
        self._print_time = 5
        self._print_cur_time = 0
        
    def run(self, in_file:str, out_file=None):
        # Create initial compressed file
        in_filepath, out_filepath = self._check_and_update_io_files(in_file, out_file)

        # with open(in_filepath, 'rb') as f:
        with open(in_filepath, 'r') as f:
            self._file_size = fstat(f.fileno()).st_size
            # Get chunk data
            # self.chunk_data = f.read(self.chunk_size)
            self._chunk_data = self._read_chunk_data(f, self.chunk_size)

            self._print_cur_time = monotonic()

            # As long as there is more data to read:
            while self._chunk_data:
                if monotonic() - self._print_cur_time >= self._print_time:
                    self._print_percentage_completion(2)
                    self._print_cur_time = monotonic()

                # Append additional chunk data till it has a full word at the end
                self._update_chunk_data_to_end_of_delimiter(f)

                # Compress the chunk
                self.pattern_compressor.compress(self._chunk_data)
                # write the chunk to the output file
                with open(out_filepath, 'a') as new_f:
                    new_f.write(self.pattern_compressor.get_compressed_data())
                
                # Get new chunk data
                # self.chunk_data = f.read(self.chunk_size)
                self._chunk_data = self._read_chunk_data(f, self.chunk_size)
            self._print_percentage_completion(2)
        
        if self._compressed_successfully(in_filepath, out_filepath):
            return True
        else:
            os_remove(out_filepath)
            return False

    def _compressed_successfully(self, input_filepath, output_filepath):
        with open(input_filepath, 'r') as f:
            input_size = fstat(f.fileno()).st_size

        with open(output_filepath, 'r') as f:
            output_size = fstat(f.fileno()).st_size
        
        return output_size < input_size

    def _print_percentage_completion(self, decimals):
        print(f"{round(self._get_percentage_completion() * 100, decimals)}%")

    def _get_percentage_completion(self):
        if self._file_size > 0:
            percent = self._bits_read / self._file_size
            return percent if percent < 1 else 1
        else:
            return 1

    def _read_chunk_data(self, file, chunk_size = 1):
        self._bits_read += chunk_size
        data = file.read(chunk_size)
        return data

    def _is_chunk_data_on_delimiter(self):
        if self._chunk_data:
            pass

    def _update_chunk_data_to_end_of_delimiter(self, f):
        if self.pattern_compressor.is_pattern_count_limited:
            pass
        # Keeps reading in chunk data till the last character is a space
        while self._chunk_data[-1] != " ":
            new_character = self._read_chunk_data(f, 1)
            # Updates the chunk data unless it hits the end of the file
            if new_character:
                self._chunk_data = self._chunk_data + new_character
            else:
                break

    def _check_and_update_io_files(self, in_file, out_file):
        # If an output file isn't specified, use the input with a replaced file extension
        if out_file is None:
            out_file = in_file.replace(".txt", ".lor")

        # If the input folder or output folders are specified, it updates the corresponding file with a path
        if self.input_folder is not None:
            in_file = f"{self.input_folder}/{in_file}"
        if self.output_folder is not None:
            out_file = f"{self.output_folder}/{out_file}"
        
        # If the input file doesn't exist, an error will be raised
        if not path.exists(in_file):
            raise(FileNotFoundError())

        return in_file, out_file

if __name__ == "__main__":
    file_compressor = pattern_compressor(15)
    
    file_compressor.input_folder = COMPRESSION_FOLDER
    file_compressor.run("random_bit_strings_1.txt")