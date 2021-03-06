# NOTE
# Chosen delimiter is necessary for compression to work properly. If not this, make sure end of the delimiter can't loop back to the start from any point
# character added to the delimiter is)

import unittest
from sys import path
path.append("..")
from src.algorithms.pattern_compression.pattern_algorithm_c import Pattern_Algorithm_C

RAW_DELIMITER = "011"
DELIMITER_REPLACE_CHAR = "0"
DELIMITER_CHAR = "1"
DELIMITER_REPLACE_STRING = RAW_DELIMITER + DELIMITER_REPLACE_CHAR
DELIMITER = RAW_DELIMITER + DELIMITER_CHAR

class TestPatternCompression(unittest.TestCase):
    def setUp(self):
        self.compressor = Pattern_Algorithm_C(max_look_ahead = 15, raw_delimiter = RAW_DELIMITER, pattern_count_num_bits = 3, pattern_bit_offset = 1)
    
    def test_compress_empty_string(self):
        self.compressor.compress("")
        self.assertEqual(self.compressor.get_compressed_data(), "")

    def test_compress_1_bit(self):
        self.compressor.compress("1")
        self.assertEqual(self.compressor.get_compressed_data(), "1")
        
        self.compressor.compress("0")
        self.assertEqual(self.compressor.get_compressed_data(), "0")

    def test_compressor_pattern_count_bits_setter_getter(self):
        self.assertEqual(self.compressor._is_pattern_count_limited, True)
        self.assertEqual(self.compressor.pattern_count_num_bits, 3)

        self.compressor.pattern_count_num_bits = None

        self.assertEqual(self.compressor._is_pattern_count_limited, False)
        self.assertIsNone(self.compressor.pattern_count_num_bits)

        self.compressor.pattern_count_num_bits = 10

        self.assertEqual(self.compressor._is_pattern_count_limited, True)
        self.assertEqual(self.compressor.pattern_count_num_bits, 10)
    
    def test_compress_adds_bits_to_one_existing_delimiter_strings(self):
        self.compressor.compress(RAW_DELIMITER)
        self.assertEqual(self.compressor.get_compressed_data(), DELIMITER_REPLACE_STRING)

    def test_compress_adds_bits_to_multiple_existing_delimiter_strings(self):
        self.compressor.compress(RAW_DELIMITER*3)
        self.assertEqual(self.compressor.get_compressed_data(), DELIMITER_REPLACE_STRING*3)
    
    def test_compressor_delimiter_setter_getter(self):
        self.assertEqual(self.compressor.raw_delimiter, RAW_DELIMITER)
        self.assertEqual(self.compressor._raw_delimiter, RAW_DELIMITER)
        self.assertEqual(self.compressor._delimiter, DELIMITER)
        self.assertEqual(self.compressor._delimiter_replace_string, DELIMITER_REPLACE_STRING)
        self.assertEqual(self.compressor._delimiter_length, 4)

        self.compressor.raw_delimiter = "11"
        self.assertEqual(self.compressor.raw_delimiter, "11")
        self.assertEqual(self.compressor._raw_delimiter, "11")
        self.assertEqual(self.compressor._delimiter, "110")
        self.assertEqual(self.compressor._delimiter_replace_string, "111")
        self.assertEqual(self.compressor._delimiter_length, 3)

        self.compressor.raw_delimiter = "1100"
        self.assertEqual(self.compressor.raw_delimiter, "1100")
        self.assertEqual(self.compressor._raw_delimiter, "1100")
        self.assertEqual(self.compressor._delimiter, "11000")
        self.assertEqual(self.compressor._delimiter_replace_string, "11001")
        self.assertEqual(self.compressor._delimiter_length, 5)

    def test_compressor_delimiter_costs_change_as_necessary(self):
        self.assertEqual(self.compressor._delimiter_cost, 4*2)

        self.compressor.pattern_count_num_bits = None
        self.assertEqual(self.compressor._delimiter_cost, 4*3)

        self.compressor.pattern_count_num_bits = 10
        self.assertEqual(self.compressor._delimiter_cost, 4*2)

        self.compressor.raw_delimiter = "0111"
        self.assertEqual(self.compressor._delimiter_cost, 5*2)

        self.compressor.pattern_count_num_bits = None
        self.assertEqual(self.compressor._delimiter_cost, 5*3)

    def test_compress_one_pattern(self):
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 100100001000 {DELIMITER} 000".replace(" ", ""))

    def test_compress_one_pattern_with_delimiter_patterns(self):
        self.compressor.compress("100110001000 100110001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 1001100001000 {DELIMITER} 000".replace(" ", ""))
    
    def test_compress_multiple_patterns(self):
        self.compressor.compress("100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 100100001000 {DELIMITER} 010".replace(" ", ""))

    def test_compress_multiple_patterns_with_extra_bits_on_outside(self):
        self.compressor.compress("01010 000100001001 000100001001 000100001001 000100001001 01010".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"01010 {DELIMITER} 000100001001 {DELIMITER} 010 01010".replace(" ", ""))

    def test_compress_pattern_longer_than_allocated_bits(self):
        self.compressor.pattern_count_num_bits = 2
        self.compressor.compress("100100001000 100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 100100001000 {DELIMITER} 11".replace(" ", ""))

        self.compressor.compress("100100001000 100100001000 100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 100100001000 {DELIMITER} 11 100100001000".replace(" ", ""))
    
    def test_compress_multiple_pieces_of_data(self):
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 100100001000 {DELIMITER} 000 {DELIMITER} 100100001000 {DELIMITER} 000".replace(" ", ""))

    def test_compress_multiple_pieces_of_data_creating_delimiters(self):
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 100100001000 {DELIMITER} 000 {DELIMITER} 100100001000 {DELIMITER} 000".replace(" ", ""))

    # def test_compress_dynamic_pattern_bit_allocation(self):
    #     self.compressor.pattern_count_num_bits = None

    #     self.compressor.compress("100100001000 100100001000 100100001000".replace(" ", ""))
    #     self.assertEqual(self.compressor.get_compressed_data(), "0110 100100001000 0110 1 0110".replace(" ", ""))

    # def test_compress_dynamic_pattern_bit_allocation_patterns_interfere_delimiter(self):
    #     self.compressor.pattern_count_num_bits = None

    #     self.compressor.compress("100100001000"*(12 + 1))
    #     self.assertEqual(self.compressor.get_compressed_data(), "0110 100100001000 0110 10111 0110".replace(" ", ""))

    #     self.compressor.compress("100100001000"*(24 + 1))
    #     self.assertEqual(self.compressor.get_compressed_data(), "0110 100100001000 0110 101111 0110".replace(" ", ""))

    def test_compressible_string_inside_larger_compressible_string(self):
        self.compressor._max_look_ahead = 30
        self.compressor.compress("100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 100100001000100100001000 {DELIMITER} 000".replace(" ", ""))

    def test_compressible_string_inside_larger_compressible_string_not_at_start(self):
        self.compressor._max_look_ahead = 30
        self.compressor.compress("01010 000100001001 000100001001 000100001001 000100001001 01010".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"01010 {DELIMITER} 000100001001000100001001 {DELIMITER} 000 01010".replace(" ", ""))
    
    # def test_delimiter_added_in_num_patterns_prevents_compression(self):
    #     self.compressor.raw_delimiter = "1"
    #     self.compressor.pattern_count_num_bits = None

    #     # When the delimiter appears in the binary num count, it has to be replaced to prevent confusion when decompressing
    #     # this can cause the string to not actually compress, this string would be compressed to "11 0000 11 1 110", which has 12
    #     # characters while the input has 13. However, the delimiter shows up in the binary num patterns of 1, resulting in a replacement
    #     # turning into 10, therefore bumping it up to 13, which is not less than the original input, therefore, it shouldn't compress
    #     # I had trouble coming up with a situation where it would result in more than the original input
    #     self.compressor.compress("0"*(12 + 1))
    #     self.assertEqual(self.compressor.get_compressed_data(), "0"*(12 + 1))
    
    def test_multiple_different_patterns(self):
        self.compressor.compress("000100001001 000100001001 000100001001 010001001001 010001001001 010001001001".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 000100001001 {DELIMITER} 001 {DELIMITER} 010001001001 {DELIMITER} 001".replace(" ", ""))

    def test_multiple_different_patterns_bits_separated(self):
        self.compressor.compress("000100001001 000100001001 000100001001 0000 010001001001 010001001001 010001001001".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 000100001001 {DELIMITER} 001 0000 {DELIMITER} 010001001001 {DELIMITER} 001".replace(" ", ""))
    
    # When put together, these two strings create a delimiter in the middle that needs to be fixed
    def test_delimiter_inbetween(self):
        self.compressor.compress("000100001001".replace(" ", ""))
        self.compressor.compress("100100001001".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), f"0001000010 {DELIMITER_REPLACE_STRING} 00100001001".replace(" ", ""))
    
    def test_delimiter_inbetween_with_compression(self):
        self.compressor.compress("000100001001"*7)
        self.compressor.compress("110100001001")
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 000100001001 {DELIMITER} 1 {DELIMITER_REPLACE_STRING} 10100001001".replace(" ", ""))

    def test_num_patterns_create_raw_delimiter_after_pattern(self):
        self.compressor.compress("000100001010"*7 + "10")
        self.assertEqual(self.compressor.get_compressed_data(), f"{DELIMITER} 000100001010 {DELIMITER} 1 {DELIMITER_REPLACE_STRING} 0".replace(" ", ""))

    def test_num_patterns_create_raw_delimiter_after_pattern_different_delimiter(self):
        self.compressor.raw_delimiter = "01011"
        self.compressor.compress("000100001010"*7 + "0110")
        self.assertEqual(self.compressor.get_compressed_data(), f"{self.compressor._delimiter} 000100001010 {self.compressor._delimiter} 1 {self.compressor._delimiter_replace_string} 0".replace(" ", ""))
    
    # def test_delimiter_replace_creates_delimiter(self):
    #     self.compressor.raw_delimiter = "01011"
    #     self.compressor.compress("01110000 11000100 00101011 10111011".replace(" ", ""))
    #     self.assertEqual(self.compressor.get_compressed_data(), "01110000 11000100 00101011 0 1011 0 1011 0".replace(" ", ""))
    
    # Add test for a pattern getting compressed immediately after one before it when the combination of the last one and the pattern created a delimiter
    # def test_