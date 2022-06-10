from bz2 import decompress
import unittest
from sys import path
path.append("..")
from text_decompression import Text_Decompressor

class Test_TextDecompressor(unittest.TestCase):
    def setUp(self):
        self.decompressor = Text_Decompressor()

    def test_decompress_empyt_string(self):
        self.decompressor.decompress("")
        self.assertEqual(self.decompressor.get_decompressed_data(), "")

    def test_decompress_a_space(self):
        self.decompressor.decompress(" ")
        self.assertEqual(self.decompressor.get_decompressed_data(), " ")

    def test_decompress_string_that_is_not_compressed(self):
        string = "Hello World!"
        self.decompressor.decompress(string)
        self.assertEqual(self.decompressor.get_decompressed_data(), string)

    def test_decompress_reference_to_nothing_with_no_other_words(self):
        string = "<3"
        self.decompressor.decompress(string)
        self.assertEqual(self.decompressor.get_decompressed_data(), string)

    def test_decompress_reference_to_nothing_with_other_words(self):
        string = "Why Hello <3"
        self.decompressor.decompress(string)
        self.assertEqual(self.decompressor.get_decompressed_data(), string)

    def test_decompress_one_word_reference(self):
        compressed = "text <1"
        decompressed = "text text"
        self.decompressor.decompress(compressed)
        self.assertEqual(self.decompressor.get_decompressed_data(), decompressed)

    def test_decompress_two_word_reference(self):
        compressed = "text text2 <2"
        decompressed = "text text2 text"
        self.decompressor.decompress(compressed)
        self.assertEqual(self.decompressor.get_decompressed_data(), decompressed)
        
    def test_decompress_string_that_has_escape_character(self):
        compressed = "text text2 ~<2"
        decompressed = "text text2 <2"
        self.decompressor.decompress(compressed)
        self.assertEqual(self.decompressor.get_decompressed_data(), decompressed)

    def test_decompress_string_that_has_double_escape_character(self):
        compressed = "text text2 ~~<2"
        decompressed = "text text2 ~<2"
        self.decompressor.decompress(compressed)
        self.assertEqual(self.decompressor.get_decompressed_data(), decompressed)

    def test_decompress_mulitple_references(self):
        compressed = "text text2 <2 <2"
        decompressed = "text text2 text text2"
        self.decompressor.decompress(compressed)
        self.assertEqual(self.decompressor.get_decompressed_data(), decompressed)

    def test_decompress_reference_with_endline_at_the_end(self):
        compressed = "text <1 \n "
        decompressed = "text text\n"
        self.decompressor.decompress(compressed)
        self.assertEqual(self.decompressor.get_decompressed_data(), decompressed)

    def test_decompress_reference_with_endline_at_the_front(self):
        compressed = "text  \n <1"
        decompressed = "text \ntext"
        self.decompressor.decompress(compressed)
        self.assertEqual(self.decompressor.get_decompressed_data(), decompressed)