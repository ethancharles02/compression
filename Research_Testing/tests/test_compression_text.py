import unittest
from sys import path
path.append("..")
from text_compression import Text_Compressor
# import os.path
# TEST_FILE_FOLDER = "..\\random_string_files"


class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = Text_Compressor()

    def test_compress_empty_string(self):
        self.compressor.compress("")
        self.assertEqual(self.compressor.get_compressed_data(), "")

    def test_compress_a_space(self):
        self.compressor.compress(" ")
        self.assertEqual(self.compressor.get_compressed_data(), " ")

    def test_compress_two_spaces(self):
        self.compressor.compress("  ")
        self.assertEqual(self.compressor.get_compressed_data(), "  ")

    def test_compress_single_word(self):
        self.compressor.compress("word")
        self.assertEqual(self.compressor.get_compressed_data(), "word")

    def test_compress_one_reference(self):
        self.compressor.compress("word word")
        self.assertEqual(self.compressor.get_compressed_data(), "word <1")

    
        # self.compressor.compress("word <1")
        # self.assertEqual(self.compressor.get_compressed_data(), "word ~<1")
        # self.compressor.compress("word ~<1")
        # self.assertEqual(self.compressor.get_compressed_data(), "word ~~<1")