# Notes:
# Test new compression

import unittest

from sys import path
path.append("..")
from bit_grid import bit_grid

from os import getcwd

class TestBit_Grid(unittest.TestCase):
    def setUp(self):
        # self.grid = bit_grid("0001101100100100000101100", 5, 5)
        pass

    def test_grid_compression_all_0s(self):
        self.grid = bit_grid("0"*25, 5, 5)
        self.assertEqual(self.grid.compress(),"1b1b1b1b1c1b1b1b1b1")
        # 1 b 1 b 1 b 1 b 1
        # c 1 b 1 b 1 b 1 b 1
        
    def test_grid_compression_all_1s(self):
        self.grid = bit_grid("1"*25, 5, 5)
        self.assertEqual(self.grid.compress(),"1101b1101b1101b1101b1101c1101b1101b1101b1101b1101")
        # 1 100 b 1 100 b 1 100 b 1 100 b 1 100
        # c 1 100 b 1 100 b 1 100 b 1 100 b 1 100
    
    def test_grid_compression_random(self):
        self.grid = bit_grid("1001000000100000111011000", 5, 5)
        self.assertEqual(self.grid.compress(),"11a1b1b11b111b110c11a1a1b110b11b11a1b1")

