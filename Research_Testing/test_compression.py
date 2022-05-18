import unittest
from picross_compress import bit_grid


class TestBit_Grid(unittest.TestCase):
    
    def setUp(self):
       self.grid = bit_grid(["1010101010 10101010 10101000101 011110101010010010"], 1)

    def test_fail_to_create_a_grid_with_0_row_length(self):
        with self.assertRaises(ValueError) as cm:
            bit_grid([], 0)
        self.assertEqual(type(cm.exception), ValueError)

    def test_create_empty_bit_string_from_empty_list(self):
        self.assertEqual(self.grid.create_bit_string([]), "")    

    def test_create_empty_bit_string_from_list_with_a_space(self):
        self.assertEqual(self.grid.create_bit_string([" "]), "") 
