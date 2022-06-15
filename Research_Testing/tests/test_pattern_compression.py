# TODO
# Test compressor to make sure it adds a bit to the front to indicate if it is unlimited pattern count or not (ie. is the pattern count limited to a bit length)

# NOTE
# Chosen delimiter is necessary for compression to work properly. If not this, make sure the starting bit is opposite of the ending bit

import unittest
from sys import path
path.append("..")
from pattern_compression import Pattern_Compressor


class TestPatternCompression(unittest.TestCase):
    def setUp(self):
        self.compressor = Pattern_Compressor(max_look_ahead = 15, raw_delimiter = "011", pattern_count_num_bits = 3, pattern_bit_offset = 1)
    
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
        self.compressor.compress("011")
        self.assertEqual(self.compressor.get_compressed_data(), "0110")

    def test_compress_adds_bits_to_multiple_existing_delimiter_strings(self):
        self.compressor.compress("011011011")
        self.assertEqual(self.compressor.get_compressed_data(), "011001100110")
    
    def test_compressor_delimiter_setter_getter(self):
        self.assertEqual(self.compressor.raw_delimiter, "011")
        self.assertEqual(self.compressor._raw_delimiter, "011")
        self.assertEqual(self.compressor._delimiter, "0111")
        self.assertEqual(self.compressor._delimiter_length, 4)

        self.compressor.raw_delimiter = "11"
        self.assertEqual(self.compressor.raw_delimiter, "11")
        self.assertEqual(self.compressor._raw_delimiter, "11")
        self.assertEqual(self.compressor._delimiter, "111")
        self.assertEqual(self.compressor._delimiter_length, 3)

        self.compressor.raw_delimiter = "1100"
        self.assertEqual(self.compressor.raw_delimiter, "1100")
        self.assertEqual(self.compressor._raw_delimiter, "1100")
        self.assertEqual(self.compressor._delimiter, "11001")
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
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 000".replace(" ", ""))

    def test_compress_one_pattern_with_delimiter_patterns(self):
        self.compressor.compress("100110001000 100110001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 1001100001000 0111 000".replace(" ", ""))
    
    def test_compress_multiple_patterns(self):
        self.compressor.compress("100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 010".replace(" ", ""))

    def test_compress_multiple_patterns_with_extra_bits_on_outside(self):
        self.compressor.compress("01010 000100001001 000100001001 000100001001 000100001001 01010".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "01010 0111 000100001001 0111 010 01010".replace(" ", ""))
    
    def test_compress_pattern_longer_than_allocated_bits(self):
        self.compressor.pattern_count_num_bits = 2
        self.compressor.compress("100100001000 100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 11".replace(" ", ""))

        self.compressor.compress("100100001000 100100001000 100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 11 100100001000".replace(" ", ""))
    
    def test_compress_multiple_pieces_of_data(self):
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 000 0111 100100001000 0111 000".replace(" ", ""))

    def test_compress_multiple_pieces_of_data_creating_delimiters(self):
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.compressor.compress("100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 000 0111 100100001000 0111 000".replace(" ", ""))

    def test_compress_dynamic_pattern_bit_allocation(self):
        self.compressor.pattern_count_num_bits = None

        self.compressor.compress("100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 1 0111".replace(" ", ""))

    def test_compress_dynamic_pattern_bit_allocation_patterns_interfere_delimiter(self):
        self.compressor.pattern_count_num_bits = None

        self.compressor.compress("100100001000"*(12 + 1))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 10110 0111".replace(" ", ""))

        self.compressor.compress("100100001000"*(24 + 1))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000 0111 101101 0111".replace(" ", ""))

    def test_compressible_string_inside_larger_compressible_string(self):
        self.compressor._max_look_ahead = 30
        self.compressor.compress("100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 100100001000100100001000 0111 000".replace(" ", ""))

    def test_compressible_string_inside_larger_compressible_string_not_at_start(self):
        self.compressor._max_look_ahead = 30
        self.compressor.compress("01010 000100001001 000100001001 000100001001 000100001001 01010".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "01010 0111 000100001001000100001001 0111 000 01010".replace(" ", ""))
    
    def test_delimiter_added_in_num_patterns_prevents_compression(self):
        self.compressor.raw_delimiter = "1"
        self.compressor.pattern_count_num_bits = None

        # When the delimiter appears in the binary num count, it has to be replaced to prevent confusion when decompressing
        # this can cause the string to not actually compress, this string would be compressed to "11 0000 11 1 110", which has 12
        # characters while the input has 13. However, the delimiter shows up in the binary num patterns of 1, resulting in a replacement
        # turning into 10, therefore bumping it up to 13, which is not less than the original input, therefore, it shouldn't compress
        # I had trouble coming up with a situation where it would result in more than the original input
        self.compressor.compress("0"*(12 + 1))
        self.assertEqual(self.compressor.get_compressed_data(), "0"*(12 + 1))
    
    def test_multiple_different_patterns(self):
        self.compressor.compress("000100001001 000100001001 000100001001 010001001001 010001001001 010001001001".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 000100001001 0111 001 0111 010001001001 0111 001".replace(" ", ""))

    def test_multiple_different_patterns_bits_separated(self):
        self.compressor.compress("000100001001 000100001001 000100001001 0000 010001001001 010001001001 010001001001".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0111 000100001001 0111 001 0000 0111 010001001001 0111 001".replace(" ", ""))