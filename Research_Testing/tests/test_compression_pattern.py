# TODO
# Test compressor to make sure it adds a bit to the front to indicate if it is unlimited pattern count or not (ie. is the pattern count limited to a bit length)

import unittest
from sys import path
path.append("..")
from pattern_compression.pattern_compression import Pattern_Compressor


class TestPatternCompression(unittest.TestCase):
    def setUp(self):
        self.compressor = Pattern_Compressor(max_look_ahead = 15, raw_delimiter = "111", pattern_count_num_bits = 3, pattern_bit_offset = 1)
    
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
        self.compressor.compress("111")
        self.assertEqual(self.compressor.get_compressed_data(), "1110")

    def test_compress_adds_bits_to_multiple_existing_delimiter_strings(self):
        self.compressor.compress("111111111")
        self.assertEqual(self.compressor.get_compressed_data(), "111011101110")
    
    def test_compressor_delimiter_setter_getter(self):
        self.assertEqual(self.compressor.raw_delimiter, "111")
        self.assertEqual(self.compressor._raw_delimiter, "111")
        self.assertEqual(self.compressor._delimiter, "1111")
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

        self.compressor.raw_delimiter = "1111"
        self.assertEqual(self.compressor._delimiter_cost, 5*2)

        self.compressor.pattern_count_num_bits = None
        self.assertEqual(self.compressor._delimiter_cost, 5*3)

    def test_compress_one_pattern_with_internal_patterns_that_shouldnt_compress(self):
        self.compressor.compress("100110001001 100110001001".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "1111 100110001001 1111 000".replace(" ", ""))

    def test_compress_one_pattern_with_delimiter_patterns(self):
        self.compressor.compress("100111001001 100111001001".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "1111 1001110001001 1111 000".replace(" ", ""))
    
    def test_compress_multiple_patterns(self):
        self.compressor.compress("100110001001 100110001001 100110001001 100110001001".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "1111 100110001001 1111 010".replace(" ", ""))

    def test_compress_multiple_patterns_with_extra_bits_on_outside(self):
        self.compressor.compress("0000 100110001001 100110001001 100110001001 100110001001 0000".replace(" ", ""))
        self.assertEqual(self.compressor.get_compressed_data(), "0000 1111 100110001001 1111 010 0000".replace(" ", ""))
    
    def test_compress_pattern_longer_than_allocated_bits(self):
        raise NotImplementedError
    
    def test_compress_multiple_pieces_of_data(self):
        pass

    def test_compress_dynamic_pattern_bit_allocation(self):
        pass