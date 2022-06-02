import unittest
from sys import path
path.append("..")
from compression import compressor

class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = compressor(20)
