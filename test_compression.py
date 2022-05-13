from re import T
import unittest
import compression
import os.path
TEST_FILE_FOLDER = "C:\\Users\\joshd\\Documents\\_College Classes\\2022 - Spring\\CSE 499\\compression\\Research_Testing\\random_string_files"


class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = compression.compressor()

    def test_compressor_creates_compressed_file(self):
        self.compressor.compress("".join([TEST_FILE_FOLDER,"\\random_bit_string_1.txt"]))
        self.assertTrue(os.path.exists("".join([TEST_FILE_FOLDER, "\\random_bit_string_1.lor"])))

    # def test_
