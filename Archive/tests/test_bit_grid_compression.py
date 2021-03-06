# Notes:
# Test new compression

import unittest

from sys import path
from archive.bit_grid_compressor import bit_grid_compressor
path.append("../..")

from os import getcwd

class TestBit_Grid(unittest.TestCase):
    def setUp(self):
        # self.grid = bit_grid("0001101100100100000101100", 5, 5)
        pass

    def test_grid_compression_all_0s(self):
        self.grid = bit_grid_compressor("0"*25, 5, 5)
        # 00010 is the "a" delimiter
        # 00011 is the "b" delimiter
        self.assertEqual(self.grid.compress(),"0000010100000101 1 00011 1 00011 1 00011 1 00011 1 00011 1 00011 1 00011 1 00011 1 00011 1 00011".replace(" ", ""))
        
    def test_grid_compression_all_1s(self):
        self.grid = bit_grid_compressor("1"*25, 5, 5)
        # 00010 is the "a" delimiter
        # 00011 is the "b" delimiter
        # self.assertEqual(self.grid.compress(),"0000010100000101 1101 00011 1101 00011 1101 00011 1101 00011 1101 00011 1101 00011 1101 00011 1101 00011 1101 00011 1101 00011".replace(" ", ""))
        self.assertEqual(self.grid.compress(),"0000010100000101 0 00011 0 00011 0 00011 0 00011 0 00011 0 00011 0 00011 0 00011 0 00011 0 00011".replace(" ", ""))
        
    def test_grid_compression_random(self):
        self.grid = bit_grid_compressor("1001000000100000111011000", 5, 5)
        # 10010
        # 00000
        # 10000
        # 01110
        # 11000
        # 00010 is the "a" delimiter
        # 00011 is the "b" delimiter
        self.assertEqual(self.grid.compress(),"0000010100000101 1 1 00010 1 00011 1 00011 11 00011 111 00011 110 00011 11 00010 1 00010 1 00011 110 00011 11 00011 11 00010 1 00011 1 00011".replace(" ", ""))