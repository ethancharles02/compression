# TODO
# Finish setting up tests between files
# Add a dump folder that will get deleted between every test (be careful when deleting all the files)
# Compress a file and output to the dump folder, check the dumped file with the reference file to test equality

import unittest

from sys import path
path.append("..")
from os import getcwd

from compression import compressor

TXT_FOLDER = "Research_Testing/tests/compressor_text_files"
TST_FOLDER = f"{TXT_FOLDER}/test_files"
REF_FOLDER = f"{TXT_FOLDER}/reference_files"

class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = compressor(20)
    
    def tearDown(self):
        print("test")

    def are_files_equal_to_each_other(self, tst_path, ref_path):
        with open(f"{TST_FOLDER}/{tst_path}") as f:
            test_list = list(f)
        with open(f"{REF_FOLDER}/{ref_path}") as f:
            ref_list = list(f)
        self.assertListEqual(test_list, ref_list)

    def test_empty_file_compresses(self):
        filename = "text_empty.txt"
        self.are_files_equal_to_each_other(filename, filename)