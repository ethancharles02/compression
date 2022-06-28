from os import getcwd, fstat, path, remove as os_remove
from pattern_constants import *
from pattern_algorithm_d import Pattern_Algorithm_D
from bitarray import bitarray
from math import ceil

class WrongFileFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Pattern_Decompressor(object):
    def __init__(self, chunk_size=1024, raw_delimiter=None, pattern_count_num_bits=None, pattern_bit_offset=None, input_file_extension=None) -> None:
        self.input_folder = getcwd()
        self.output_folder = self.input_folder

        self.chunk_size = chunk_size

        if raw_delimiter is None:
            raw_delimiter = RAW_DELIMITER
        if pattern_count_num_bits is None:
            pattern_count_num_bits = PATTERN_COUNT_NUM_BITS
        if pattern_bit_offset is None:
            pattern_bit_offset = PATTERN_BIT_OFFSET
        if input_file_extension is None:
            self.input_file_extension = OUT_FILE_EXTENSION

        self.pattern_decompressor = Pattern_Algorithm_D(raw_delimiter, pattern_count_num_bits, pattern_bit_offset)

        self._decompressed_data = []
        self._leftover_bits = ""
        self._bytes_read = 0
        self._chunk_data = None
        self._output_data = ""
        # self._last_word_written = None
        # self._has_written_from_overflow = False

    def run(self, input_file:str, output_file=None):
        input_file, output_file = self._check_and_update_io_files(input_file, output_file)
        # if output_file is None:
        #     output_file = self._remove_file_extension(input_file)
        # if path.exists(output_file):
        #     os_remove(output_file)
        with open(input_file, "rb") as in_f:
            with open(output_file, "ab+") as out_f:
                self.chunk_size = fstat(in_f.fileno()).st_size

                self._chunk_data = self._read_chunk_data_to_delimiter(in_f, self.chunk_size)
                while self._chunk_data:

                    self.pattern_decompressor.decompress(self._chunk_data)
                    self._output_data += self.pattern_decompressor.get_decompressed_data()
                    if len(self._output_data) % 8 == 0:
                        self._append_binary_string_to_file(out_f, self._output_data)
                        self._output_data = ""

                    self._chunk_data = self._read_chunk_data_to_delimiter(in_f, self.chunk_size)

                if self._output_data:
                    self._append_binary_string_to_file(out_f, self._output_data)
                    self._output_data = ""
        
        return True

    def _check_and_update_io_files(self, in_file, out_file):
        # If an output file isn't specified, use the input with a replaced file extension
        if out_file is None:
            out_file = self._remove_file_extension(in_file)

        # If the input folder or output folders are specified, it updates the corresponding file with a path
        if self.input_folder is not None:
            in_file = f"{self.input_folder}/{in_file}"
        if self.output_folder is not None:
            out_file = f"{self.output_folder}/{out_file}"
        
        # If the input file doesn't exist, an error will be raised
        if not path.exists(in_file):
            raise(FileNotFoundError())
        if path.exists(out_file):
            os_remove(out_file)

        return in_file, out_file

    def _remove_file_extension(self, string:str):
        index = string.rfind(self.input_file_extension)
        if index != -1:
            return string[:index]
        else:
            raise ValueError(f"No file extension of {self.input_file_extension} found for {string}")

    def _append_binary_string_to_file(self, file, string:str):
        # string_length = len(string)

        # needed_bits = (8 - string_length) % 8
        # if needed_bits != 0:
        #     new_bits = self._read_bits(file, needed_bits)
        #     if new_bits:
        #         string = string + new_bits
        #     else:
        #         string = string + self._get_final_output_string(needed_bits)

        bitarr = bitarray(list(map(int, string)))

        file.write(bitarr)

    def _read_chunk_data_to_delimiter(self, file, chunk_size = 1):
        data = self._get_new_chunk_data(file, chunk_size)
        if data:
            num_delimiters = data.count(self.pattern_decompressor._delimiter)

            while num_delimiters % 2 != 0:
                new_data = self._get_new_chunk_data(file, 1)
                if new_data:
                    data = data + new_data
                    num_delimiters = data.count(self.pattern_decompressor._delimiter)
                else:
                    last_delimiter_index = data.rfind(self.pattern_decompressor._delimiter)
                    data = data[:last_delimiter_index]
                    break

            last_delimiter_index = data.rfind(self.pattern_decompressor._delimiter)
            if last_delimiter_index != -1:
            
                num_bits_needed = self._get_num_bits_needed_for_pattern_count(len(data), last_delimiter_index)
                if num_bits_needed > 0:
                    new_bits = self._read_bits(file, num_bits_needed)
                    if new_bits:
                        data = data + new_bits
            
        return data

    def _get_num_bits_needed_for_pattern_count(self, data_length, last_delimiter_index):
        bits_needed = self.pattern_decompressor.pattern_count_num_bits - ((data_length - last_delimiter_index) - self.pattern_decompressor._delimiter_length)
        if bits_needed > 0:
            return bits_needed
        else:
            return 0
    
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

    def _cutoff_data(self, data):
        if self._leftover_bits:
            raise Exception(f"There are leftover bits that shouldn't exist: {self._leftover_bits}")

        cutoff_index_needed = True

        test_string = data[-((self.pattern_decompressor._delimiter_length - 1) * 2):]
        if self.pattern_decompressor.raw_delimiter in test_string:
            relative_index = test_string.rfind(self.pattern_decompressor.raw_delimiter)

            if relative_index <= len(test_string) - self.pattern_decompressor._delimiter_length:
                index = -(len(test_string) - (relative_index + self.pattern_decompressor._delimiter_length))
                cutoff_index_needed = False
            else:
                cutoff_index_needed = True

        if cutoff_index_needed:
            string = data[-(self.pattern_decompressor._delimiter_length - 1):]
            relative_index = self._get_safe_cutoff_index(string)

            index = -(len(string) - relative_index)

        if index < 0:
            self._leftover_bits = data[index:]
            return data[:index]
        else:
            return data

    def _get_safe_cutoff_index(self, string):
        for i in range(len(string)):
            check_string = string[i:] + self.pattern_decompressor._delimiter[-(i + 1):]
            if check_string == self.pattern_decompressor._delimiter:
                return i
        return i + 1

    def _get_new_chunk_data(self, file, chunk_size = 1):
        output = self._leftover_bits + self._read_chunk_data(file, chunk_size)
        self._leftover_bits = ""

        if output:
            return self._cutoff_data(output)
        else:
            return ""

    def _read_chunk_data(self, file, chunk_size = 1):
        data = file.read(chunk_size)
        if data:
            self._bytes_read += chunk_size
            return self._convert_hex_bytes_to_bits(data)
        else:
            return ""

    def _convert_hex_bytes_to_bits(self, hex_bytes):
        binary_string = bin(int(hex_bytes.hex(), base=16))[2:]
        num_leading_zeroes = (8 - len(bin(int(hex_bytes.hex(), base=16))[2:])) % 8
        return "0" * num_leading_zeroes + binary_string

if __name__ == "__main__":
    decompressor = Pattern_Decompressor()

    data = "0000000000 010110 1111011".replace(" ", "")
    print(decompressor._cutoff_data(data), decompressor._leftover_bits)