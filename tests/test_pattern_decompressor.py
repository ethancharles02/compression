# TODO
# The bit cutoff doesnt account for the special replace 2, it may need to be updated to account for that
import unittest
from sys import path
path.append("..")
from os import getcwd, listdir, remove as os_remove, path as os_path

from algorithms.pattern_compression.pattern_decompressor import Pattern_Decompressor


BIN_FOLDER = "tests/compressor_binary_files"
TST_FOLDER = f"{BIN_FOLDER}/test_files/"
INPUT_FOLDER = f"{BIN_FOLDER}/reference_files/"
OUTPUT_FOLDER = f"{BIN_FOLDER}/dump_files/"

class TestPatternDecompressor(unittest.TestCase):
    def setUp(self):
        self.decompressor = Pattern_Decompressor(chunk_size=10, raw_delimiter="01011", pattern_count_num_bits=4, pattern_bit_offset=1)
        # self.decompressor.input_folder = INPUT_FOLDER
        # self.decompressor.output_folder = OUTPUT_FOLDER

    def tearDown(self):
        for f in listdir(OUTPUT_FOLDER):
            os_remove(os_path.join(OUTPUT_FOLDER, f))

    def assert_files_in_test_folders_are_equal(self, tst_filename, ref_filename = None):
        if ref_filename == None:
            ref_filename = tst_filename
        with open(f"{OUTPUT_FOLDER}/{tst_filename}") as f:
            test_list = list(f)
        with open(f"{TST_FOLDER}/{ref_filename}") as f:
            ref_list = list(f)
        self.assertListEqual(test_list, ref_list)

    def assert_file_compresses_correctly(self, filename):
        input_file = INPUT_FOLDER + filename
        output_file = OUTPUT_FOLDER + filename.replace(".lor", "")
        result = self.decompressor.run(input_file, output_file)
        self.assertTrue(result)
        self.assert_files_in_test_folders_are_equal(filename.replace(".lor", ""))

    def test_32_bits_decompress(self):
        filename = "32_bits.bin.lor"
        self.assert_file_compresses_correctly(filename)

    def test_2_chunks_of_4_bytes_decompress(self):
        filename = "2_chunks_of_4.bin.lor"
        self.decompressor.chunk_size = 4
        self.assert_file_compresses_correctly(filename)

    def test_3_chunks_of_4_bytes_decompress(self):
        filename = "3_chunks_of_4.bin.lor"
        self.decompressor.chunk_size = 4
        self.assert_file_compresses_correctly(filename)

    def test_partial_bytes_decompress(self):
        filename = "partial_bytes.bin.lor"
        self.assert_file_compresses_correctly(filename)
        
    def test_delimiter_replace_string_between_chunks_decompress(self):
        filename = "replace_string_between_chunks.bin.lor"
        self.decompressor.chunk_size = 1
        self.assert_file_compresses_correctly(filename)

    # Make sure decompressor is getting additional bits to account for a num pattern that might also include a replace delimiter string in it