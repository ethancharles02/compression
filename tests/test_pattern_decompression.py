import unittest
from sys import path
path.append("..")
from pattern_compression.pattern_algorithm_d import Pattern_Algorithm_D

RAW_DELIMITER = "011"
DELIMITER_REPLACE_CHAR = "0"
DELIMITER_CHAR = "1"
DELIMITER_REPLACE_STRING = RAW_DELIMITER + DELIMITER_REPLACE_CHAR
DELIMITER = RAW_DELIMITER + DELIMITER_CHAR

class TestPatternDecompression(unittest.TestCase):
    def setUp(self):
        self.decompressor = Pattern_Algorithm_D(raw_delimiter = RAW_DELIMITER, pattern_count_num_bits = 3, pattern_bit_offset = 1)
    
    def test_decompress_empty(self):
        self.decompressor.decompress("")
        self.assertEqual(self.decompressor.get_decompressed_data(), "")
    
    def test_decompress_no_delimiters(self):
        self.decompressor.decompress("111000")
        self.assertEqual(self.decompressor.get_decompressed_data(), "111000")

    def test_decompress_one_delimiter_area(self):
        self.decompressor.decompress(f"{DELIMITER} 000000 {DELIMITER} 001".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "000000 000000 000000".replace(" ", ""))

    def test_decompress_1_bit(self):
        self.decompressor.decompress("1")
        self.assertEqual(self.decompressor.get_decompressed_data(), "1")
        
        self.decompressor.decompress("0")
        self.assertEqual(self.decompressor.get_decompressed_data(), "0")

    def test_decompressor_pattern_count_bits_setter_getter(self):
        self.assertEqual(self.decompressor.is_pattern_count_limited, True)
        self.assertEqual(self.decompressor.pattern_count_num_bits, 3)

        self.decompressor.pattern_count_num_bits = None

        self.assertEqual(self.decompressor.is_pattern_count_limited, False)
        self.assertIsNone(self.decompressor.pattern_count_num_bits)

        self.decompressor.pattern_count_num_bits = 10

        self.assertEqual(self.decompressor.is_pattern_count_limited, True)
        self.assertEqual(self.decompressor.pattern_count_num_bits, 10)
    
    def test_decompressor_delimiter_setter_getter(self):
        self.assertEqual(self.decompressor.raw_delimiter, RAW_DELIMITER)
        self.assertEqual(self.decompressor._raw_delimiter, RAW_DELIMITER)
        self.assertEqual(self.decompressor._delimiter, DELIMITER)
        self.assertEqual(self.decompressor._delimiter_replace_string, DELIMITER_REPLACE_STRING)

        self.decompressor.raw_delimiter = "11"
        self.assertEqual(self.decompressor.raw_delimiter, "11")
        self.assertEqual(self.decompressor._raw_delimiter, "11")
        self.assertEqual(self.decompressor._delimiter, "110")
        self.assertEqual(self.decompressor._delimiter_replace_string, "111")

        self.decompressor.raw_delimiter = "1100"
        self.assertEqual(self.decompressor.raw_delimiter, "1100")
        self.assertEqual(self.decompressor._raw_delimiter, "1100")
        self.assertEqual(self.decompressor._delimiter, "11000")
        self.assertEqual(self.decompressor._delimiter_replace_string, "11001")

    def test_decompress_one_pattern(self):
        self.decompressor.decompress(f"{DELIMITER} 100100001000 {DELIMITER} 000".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000 100100001000".replace(" ", ""))

    def test_decompress_one_pattern_with_delimiter_patterns(self):
        self.decompressor.decompress(f"{DELIMITER} 10 {DELIMITER_REPLACE_STRING} 0001000 {DELIMITER} 000".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "100110001000 100110001000".replace(" ", ""))
    
    def test_decompress_multiple_patterns(self):
        self.decompressor.decompress(f"{DELIMITER} 100100001000 {DELIMITER} 010".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000 100100001000 100100001000 100100001000".replace(" ", ""))

    def test_decompress_multiple_patterns_with_extra_bits_on_outside(self):
        self.decompressor.decompress(f"01010 {DELIMITER} 000100001001 {DELIMITER} 010 01010".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "01010 000100001001 000100001001 000100001001 000100001001 01010".replace(" ", ""))
    
    def test_decompress_pattern_longer_than_allocated_bits(self):
        self.decompressor.pattern_count_num_bits = 2
        self.decompressor.decompress(f"{DELIMITER} 100100001000 {DELIMITER} 11".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000 100100001000 100100001000 100100001000 100100001000".replace(" ", ""))

        self.decompressor.decompress(f"{DELIMITER} 100100001000 {DELIMITER} 11 100100001000".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000 100100001000 100100001000 100100001000 100100001000 100100001000".replace(" ", ""))
    
    def test_decompress_multiple_pieces_of_data(self):
        self.decompressor.decompress(f"{DELIMITER} 100100001000 {DELIMITER} 000".replace(" ", ""))
        self.decompressor.decompress(f"{DELIMITER} 100100001000 {DELIMITER} 000".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000 100100001000 100100001000 100100001000".replace(" ", ""))

    def test_decompress_multiple_pieces_of_data_creating_delimiters(self):
        self.decompressor.decompress(f"{DELIMITER} 100100001000 {DELIMITER} 000".replace(" ", ""))
        self.decompressor.decompress(f"{DELIMITER} 100100001000 {DELIMITER} 000".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000 100100001000 100100001000 100100001000".replace(" ", ""))

    # def test_decompress_dynamic_pattern_bit_allocation(self):
    #     self.decompressor.pattern_count_num_bits = None

    #     self.decompressor.decompress("0111 100100001000 0111 1 0111".replace(" ", ""))
    #     self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000 100100001000 100100001000".replace(" ", ""))

    # def test_decompress_dynamic_pattern_bit_allocation_patterns_interfere_delimiter(self):
    #     self.decompressor.pattern_count_num_bits = None

    #     self.decompressor.decompress("0111 100100001000 0111 10110 0111".replace(" ", ""))
    #     self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000"*(12 + 1))

    #     self.decompressor.decompress("0111 100100001000 0111 101101 0111".replace(" ", ""))
    #     self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000"*(24 + 1))

    def test_decompress_string_inside_larger_decompressible_string(self):
        self.decompressor.decompress(f"{DELIMITER} 100100001000100100001000 {DELIMITER} 000".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "100100001000 100100001000 100100001000 100100001000".replace(" ", ""))

    def test_decompress_string_inside_larger_decompressible_string_not_at_start(self):
        self.decompressor.decompress(f"01010 {DELIMITER} 000100001001000100001001 {DELIMITER} 000 01010".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "01010 000100001001 000100001001 000100001001 000100001001 01010".replace(" ", ""))
    
    def test_decompress_multiple_different_patterns(self):
        self.decompressor.decompress(f"{DELIMITER} 000100001001 {DELIMITER} 001 {DELIMITER} 010001001001 {DELIMITER} 001".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "000100001001 000100001001 000100001001 010001001001 010001001001 010001001001".replace(" ", ""))

    def test_decompress_multiple_different_patterns_bits_separated(self):
        self.decompressor.decompress(f"{DELIMITER} 000100001001 {DELIMITER} 001 0000 {DELIMITER} 010001001001 {DELIMITER} 001".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "000100001001 000100001001 000100001001 0000 010001001001 010001001001 010001001001".replace(" ", ""))
    
    def test_decompress_delimiter_replace_creates_delimiter(self):
        self.decompressor.raw_delimiter = "01011"
        self.decompressor.decompress("01110000 11000100 00101011 0 1011 0 1011 0".replace(" ", ""))
        self.assertEqual(self.decompressor.get_decompressed_data(), "01110000 11000100 00101011 10111011".replace(" ", ""))