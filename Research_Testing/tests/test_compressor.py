# TODO
# Finish setting up tests between files
# Add comments to add any necessary context to tests (especially the folder one)
# Maybe make a custom function for replacing the file extension

import unittest

from sys import path
path.append("..")
from os import getcwd, listdir, remove as os_remove, path as os_path

from compressor import compressor

TXT_FOLDER = "Research_Testing/tests/compressor_text_files"
TST_FOLDER = f"{TXT_FOLDER}/test_files"
REF_FOLDER = f"{TXT_FOLDER}/reference_files"
DUMP_FOLDER = f"{TXT_FOLDER}/dump_files"

class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = compressor(24, 5)
        self.compressor.input_folder = TST_FOLDER
        self.compressor.output_folder = DUMP_FOLDER
    
    def tearDown(self):
        for f in listdir(DUMP_FOLDER):
            os_remove(os_path.join(DUMP_FOLDER, f))

    def assert_files_in_test_folders_are_equal(self, tst_filename, ref_filename = None):
        if ref_filename == None:
            ref_filename = tst_filename
        with open(f"{DUMP_FOLDER}/{tst_filename}") as f:
            test_list = list(f)
        with open(f"{REF_FOLDER}/{ref_filename}") as f:
            ref_list = list(f)
        self.assertListEqual(test_list, ref_list)

    def test_empty_file_compresses(self):
        filename = "text_empty.txt"
        self.compressor.run(filename)
        output_file = filename.replace(".txt", ".lor")
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_generic_file_compresses(self):
        filename = "text_generic.txt"
        self.compressor.run(filename)
        output_file = filename.replace(".txt", ".lor")
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_wont_compress_single_word_out_of_chunk_range(self):
        filename = "text_out_of_chunk_range.txt"
        self.compressor.run(filename)
        output_file = filename.replace(".txt", ".lor")
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_compress_single_word_when_on_the_chunk_border(self):
        filename = "text_on_chunk_border.txt"
        self.compressor.run(filename)
        output_file = filename.replace(".txt", ".lor")
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_compress_three_chunks(self):
        filename = "text_three_chunks.txt"
        self.compressor.run(filename)
        output_file = filename.replace(".txt", ".lor")
        self.assert_files_in_test_folders_are_equal(output_file)
    
    def test_compress_with_newlines(self):
        # AssertionError: Lists differ: ['test2 n1 n2\n', 'test2 n1 test n3\n', 'n4 n5 <3'] != ['test2 n1 n2\n', '<3 <3 test n3\n', 'n4 n5 <4']
        # First differing element 1:
        # 'test2 n1 test n3\n'
        # '<3 <3 test n3\n'
        # - ['test2 n1 n2\n', 'test2 n1 test n3\n', 'n4 n5 <3']
        # ?                        ---------                ^
        # + ['test2 n1 n2\n', '<3 <3 test n3\n', 'n4 n5 <4']
        # ?                    ++++++                    ^               ++++++                   ^^
        self.compressor.chunk_size = 200
        filename = "text_with_newlines.txt"
        self.compressor.run(filename)
        output_file = filename.replace(".txt", ".lor")
        self.assert_files_in_test_folders_are_equal(output_file)

class TestCompressor_folder_functionality(unittest.TestCase):
    def assert_files_are_equal(self, tst_filename, ref_filename):
        with open(tst_filename) as f:
            test_list = list(f)
        with open(ref_filename) as f:
            ref_list = list(f)
        self.assertListEqual(test_list, ref_list)

    @classmethod
    def setUpClass(cls):
        generic_text = "test2 n1 n2 test2"
        generic_compressed_text = "test2 n1 n2 <3"
        cls.in_file = "__test_folder_functionality.txt"
        cls.ref_file = "__ref_test_folder_functionality.lor"
        with open(cls.in_file, "w") as f:
            f.write(generic_text)
        with open(cls.ref_file, "w") as f:
            f.write(generic_compressed_text)

    @classmethod
    def tearDownClass(cls):
        os_remove(cls.in_file)
        os_remove(cls.ref_file)

    def setUp(self):
        self.compressor = compressor(24, 5)
        self.result_file = "__test_folder_functionality.lor"

    def tearDown(self):
        if os_path.exists(self.result_file):
            os_remove(self.result_file)

    def test_compress_no_input_folder(self):
        self.compressor.output_folder = DUMP_FOLDER

        self.compressor.run(self.in_file, self.result_file)
        self.assert_files_are_equal(f"{DUMP_FOLDER}/{self.result_file}", self.ref_file)
        os_remove(f"{DUMP_FOLDER}/{self.result_file}")

    def test_compress_no_output_folder(self):
        self.compressor.input_folder = TST_FOLDER
        filename = "text_generic.txt"

        self.compressor.run(filename, self.result_file)
        self.assert_files_are_equal(self.result_file, self.ref_file)

    def test_compress_no_io_folders(self):
        self.compressor.run(self.in_file, self.result_file)
        self.assert_files_are_equal(self.result_file, self.ref_file)