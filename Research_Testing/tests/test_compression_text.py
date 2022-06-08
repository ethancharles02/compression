import unittest
from sys import path
path.append("..")
from text_compression import Text_Compressor


class TestTextCompression(unittest.TestCase):
    def setUp(self):
        self.compressor = Text_Compressor(5)

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

    def test_compress_text_has_one_reference(self):
        self.compressor.compress("word word")
        self.assertEqual(self.compressor.get_compressed_data(), "word <1")

    def test_compress_adds_escape_char_if_string_already_has_reference_char(self):
        self.compressor.compress("word <1")
        self.assertEqual(self.compressor.get_compressed_data(), "word ~<1")
        self.compressor.compress("word ~<1")
        self.assertEqual(self.compressor.get_compressed_data(), "word ~~<1")

    def test_compress_one_reference_with_word_between(self):
        self.compressor.compress("word n word")
        self.assertEqual(self.compressor.get_compressed_data(), "word n <2")

    def test_compress_text_has_three_reference(self):
        self.compressor.compress("word word word word")
        self.assertEqual(self.compressor.get_compressed_data(), "word <1 <1 <1")

    def test_compress_text_with_words_between_references(self):
        string = "word n1 n2 n3 n4 word"
        expected_string = "word n1 n2 n3 n4 <5"
        self.compressor.compress(string)
        self.assertEqual(self.compressor.get_compressed_data(), expected_string)

    def test_compress_two_consecutive_strings(self):
        string2 = "word n3"
        string1 = "n2 n1 word"
        expected_string = "word n3 n2 n1 <4"
        self.compressor.compress(string1)
        self.compressor.compress(string2)
        self.assertEqual(self.compressor.get_compressed_data(), expected_string)

    def test_compress_three_consecutive_strings(self):
        string3 = "word n1 n2 word2"
        string2 = "word n3"
        string1 = "n4 word2 n5 word"
        expected_string = "word n1 n2 word2 <4 n3 n4 <4 n5 <5"
        self.compressor.compress(string1)
        self.compressor.compress(string2)
        self.compressor.compress(string3)
        self.assertEqual(self.compressor.get_compressed_data(), expected_string)

    def test_compress_two_consecutive_strings_with_line_breaks(self):
        string2 = "word n1\n"
        string1 = "n2 \nword2 n3 word"
        expected_string = "word n1\n n2 \nword2 n3 <5"
        self.compressor.compress(string1)
        self.compressor.compress(string2)
        self.assertEqual(self.compressor.get_compressed_data(), expected_string)

    def test_compress_two_consecutive_strings_one_string_small(self):
        string2 = "n1 word"
        string1 = "word"
        expected_string = "n1 word <1"
        self.compressor.compress(string1)
        self.compressor.compress(string2)
        self.assertEqual(self.compressor.get_compressed_data(), expected_string)

    def test_look_ahead_length_affects_compress_look_ahead(self):
        string = "word n1 n2 n3 n4 n5 word"
        self.compressor.compress(string)
        self.assertEqual(self.compressor.get_compressed_data(), string)

    def test_get_look_ahead_value(self):
        self.assertEqual(self.compressor.look_ahead, self.compressor._look_ahead)

    def test_set_look_ahead_value(self):
        x = 10
        self.compressor.look_ahead = x
        self.assertEqual(self.compressor._look_ahead, x)

    def test_set_min_ref_length_when_look_ahead_is_reset(self):
        self.compressor.look_ahead = 300
        self.assertEqual(self.compressor._min_reference_length, 4)

    def test_look_ahead_ignores_small_string(self):
        self.compressor.look_ahead = 5
        string = "www n1 www n1 w n3 w n4 word n5 word"
        expected_string = "www n1 <2 n1 w n3 w n4 word n5 <2"
        self.compressor.compress(string)
        self.assertEqual(self.compressor.get_compressed_data(), expected_string)

    def test_look_ahead_change_after_compression(self):
        self.test_look_ahead_ignores_small_string()
        self.compressor.look_ahead = 10
        string = "www n1 www n1 w n3 w n4 word n5 word"
        expected_string = "www n1 www n1 w n3 w n4 word n5 <2"
        self.compressor.compress(string)
        self.assertEqual(self.compressor.get_compressed_data(), expected_string)