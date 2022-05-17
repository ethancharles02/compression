from re import T
import unittest
import compression
import os.path
# TEST_FILE_FOLDER = "C:\\Users\\joshd\\Documents\\_College Classes\\2022 - Spring\\CSE 499\\compression\\Research_Testing\\random_string_files"
TEST_FILE_FOLDER = ""


class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = compression.compressor()

    def test_compressor_grid_width_is_an_integer(self):
        self.assertIsInstance(self.compressor.row_length, int)

    def test_compressor_grid_height_is_an_integer(self):
        self.assertIsInstance(self.compressor.col_height, int)

    def test_compressor_chunck_size_is_an_integer(self):
        self.assertIsInstance(self.compressor.chunk_size, int)

    def test_compress_when_given_nothing(self):
        self.assertRaises(FileNotFoundError, self.compressor.compress, "")

    def test_compressor_creates_compressed_file(self):
        self.compressor.compress(f"{TEST_FILE_FOLDER}\\random_bit_strings_1.txt")
        self.assertTrue(os.path.exists(f"{TEST_FILE_FOLDER}\\random_bit_strings_1.lor"))

    def test_reads_correct_chunk_size(self):
        self.compressor.compress(f"{TEST_FILE_FOLDER}\\random_bit_strings_1.txt")
        
    # def test_can_create_grid()

    # def test_compress_creates_grid(self):
    #     self.compressor.compress("")
    #     self.assertEqual(self.compressor.grid, [])

