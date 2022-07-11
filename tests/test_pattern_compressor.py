import unittest

from sys import path
path.append("..")
from os import listdir, remove as os_remove, path as os_path

from src.algorithms.pattern_compression.pattern_compressor import Pattern_Compressor

BIN_FOLDER = "tests/compressor_binary_files"
INPUT_FOLDER = f"{BIN_FOLDER}/test_files/"
REF_FOLDER = f"{BIN_FOLDER}/reference_files/"
OUTPUT_FOLDER = f"{BIN_FOLDER}/dump_files/"

class TestPatternCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = Pattern_Compressor(chunk_size=10, pattern_bit_offset=1, max_look_ahead=15, raw_delimiter="01011", pattern_count_num_bits=4, compressed_file_extension=".lor")
        # self.compressor.input_folder = INPUT_FOLDER
        # self.compressor.output_folder = OUTPUT_FOLDER
    
    def tearDown(self):
        for f in listdir(OUTPUT_FOLDER):
            os_remove(os_path.join(OUTPUT_FOLDER, f))

    def assert_files_in_test_folders_are_equal(self, tst_filename, ref_filename = None):
        if ref_filename == None:
            ref_filename = tst_filename
        self.assert_files_are_equal(OUTPUT_FOLDER + tst_filename, REF_FOLDER + ref_filename)
    
    def assert_files_are_equal(self, file1, file2):
        with open(file1) as f:
            file1_list = list(f)
        with open(file2) as f:
            file2_list = list(f)
        self.assertListEqual(file1_list, file2_list)

    def assert_file_not_in_output_folder(self, filename):
        file_exists = os_path.exists(OUTPUT_FOLDER + filename)
        self.assertFalse(file_exists)

    def assert_file_doesnt_compress(self, filename):
        input_file = INPUT_FOLDER + filename
        output_file = OUTPUT_FOLDER + filename + ".lor"

        result = self.compressor.run(input_file, output_file)

        self.assertFalse(result)
        self.assert_file_not_in_output_folder(filename)

    def assert_file_compresses_correctly(self, input_filename):
        input_file = INPUT_FOLDER + input_filename
        output_file = OUTPUT_FOLDER + input_filename + ".lor"
        result = self.compressor.run(input_file, output_file)
        self.assertTrue(result)
        self.assert_files_in_test_folders_are_equal(input_filename + ".lor")

    # Since an empty file won't compress, it shouldn't even output
    def test_empty_file_does_not_compress(self):
        filename = "empty.bin"
        self.assert_file_doesnt_compress(filename)

    def test_8_bits_file_does_not_compress(self):
        filename = "8_bits.bin"
        self.assert_file_doesnt_compress(filename)

    def test_32_bits_compress(self):
        filename = "32_bits.bin"
        self.assert_file_compresses_correctly(filename)

    def test_partial_bytes_add_bits_to_end(self):
        filename = "partial_bytes.bin"
        self.assert_file_compresses_correctly(filename)

    # In the event that compression results in bytes that aren't finished, a delimiter should be added to the end that finishes off the bytes
    # This can add bits that would result in it not compressing which would normally compress
    # 01 00000000 0000000 010111 0011110111001 010111 0001 010111 0000
    def test_partial_bytes_add_bits_to_end_which_shouldnt_compress(self):
        filename = "partial_bytes_dont_compress.bin"
        self.assert_file_doesnt_compress(filename)

    def test_2_chunks_of_4_bytes(self):
        self.compressor.chunk_size = 4
        filename = "2_chunks_of_4.bin"
        self.assert_file_compresses_correctly(filename)

    def test_3_chunks_of_4_bytes(self):
        self.compressor.chunk_size = 4
        filename = "3_chunks_of_4.bin"
        self.assert_file_compresses_correctly(filename)
    
    def test_raw_delimiter_between_chunks_compresses_correctly(self):
        self.compressor.chunk_size = 6
        self.compressor.pattern_algorithm._max_look_ahead = 8
        filename = "raw_delimiter_between_chunks.bin"
        self.assert_file_compresses_correctly(filename)

    def test_compress_to_same_output_folder(self):
        filename = "32_bits.bin"
        input_file = INPUT_FOLDER + filename
        output_file = OUTPUT_FOLDER

        result = self.compressor.run(input_file, output_file)
        self.assertTrue(result)

        self.assert_files_are_equal(REF_FOLDER + filename + ".lor", output_file + filename + ".lor")
        if os_path.exists(output_file + filename + ".lor"):
            os_remove(output_file + filename + ".lor")

    def test_compress_to_different_output_folder(self):
        filename = "32_bits.bin"
        input_file = INPUT_FOLDER + filename
        output_file = "tests/compressor_binary_files/"

        result = self.compressor.run(input_file, output_file)
        self.assertTrue(result)

        self.assert_files_are_equal(REF_FOLDER + filename + ".lor", output_file + filename + ".lor")
        if os_path.exists(output_file + filename + ".lor"):
            os_remove(output_file + filename + ".lor")

    def test_compress_to_output_file(self):
        filename = "32_bits.bin"
        input_file = INPUT_FOLDER + filename
        output_file = "tests/compressor_binary_files/test1.lor"

        result = self.compressor.run(input_file, output_file)
        self.assertTrue(result)

        self.assert_files_are_equal(REF_FOLDER + filename + ".lor", output_file)
        if os_path.exists(output_file):
            os_remove(output_file)

    def test_compress_no_output_file(self):
        filename = "32_bits.bin"
        input_file = INPUT_FOLDER + filename
        output_file = INPUT_FOLDER + filename + ".lor"

        result = self.compressor.run(input_file)
        self.assertTrue(result)

        self.assert_files_are_equal(REF_FOLDER + filename + ".lor", output_file)
        if os_path.exists(output_file):
            os_remove(output_file)