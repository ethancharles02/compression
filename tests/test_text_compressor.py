# TODO
# Finish setting up tests between files
# Add comments to add any necessary context to tests (especially the folder one)
# Maybe make a custom function for replacing the file extension

import unittest

from sys import path
path.append("..")
from os import listdir, remove as os_remove, path as os_path

from algorithms.text_compression.text_compressor import Text_Compressor

TXT_FOLDER = "tests/compressor_text_files"
INPUT_FOLDER = f"{TXT_FOLDER}/test_files"
REF_FOLDER = f"{TXT_FOLDER}/reference_files"
OUTPUT_FOLDER = f"{TXT_FOLDER}/dump_files"


class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = Text_Compressor(24, 5)
        self.compressor.compressed_file_extension = ".lor"  # for tests
        self.compressor.output_folder = OUTPUT_FOLDER
    
    def tearDown(self):
        for f in listdir(OUTPUT_FOLDER):
            os_remove(os_path.join(OUTPUT_FOLDER, f))

    def assert_files_in_test_folders_are_equal(self, tst_filename, ref_filename = None):
        if ref_filename == None:
            ref_filename = tst_filename
        with open(f"{OUTPUT_FOLDER}/{tst_filename}") as f:
            test_list = list(f)
        with open(f"{REF_FOLDER}/{ref_filename}") as f:
            ref_list = list(f)
        self.assertListEqual(test_list, ref_list)
    
    def assert_file_not_in_output_folder(self, filename):
        file_exists = os_path.exists(f"{OUTPUT_FOLDER}/{filename}")
        self.assertFalse(file_exists)

    def test_empty_file_compresses(self):
        filename = "/text_empty.txt"
        in_file = INPUT_FOLDER + filename
        result = self.compressor.run(in_file)
        self.assertEquals(result, False)
        ref_file = filename + ".lor"
        self.assert_file_not_in_output_folder(ref_file)

    def test_error_is_raised_if_output_is_to_wrong_file_type(self):
        filename = INPUT_FOLDER + "/text_generic.txt"
        output_file = filename.replace(".txt", ".fake")
        self.assertRaises(TypeError, self.compressor.run, args=(filename, output_file))

    def test_generic_file_compresses(self):
        filename = "/text_generic.txt"
        in_file = INPUT_FOLDER + filename
        result = self.compressor.run(in_file)
        self.assertTrue(result)
        output_file = filename + ".lor"
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_wont_compress_single_word_out_of_chunk_range(self):
        filename = "/text_out_of_chunk_range.txt"
        in_file = INPUT_FOLDER + filename
        result = self.compressor.run(in_file)
        self.assertTrue(result)
        output_file = filename + ".lor"
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_compress_single_word_when_on_the_chunk_border(self):
        filename = "/text_on_chunk_border.txt"
        in_file = INPUT_FOLDER + filename
        result = self.compressor.run(in_file)
        self.assertTrue(result)
        output_file = filename + ".lor"
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_compress_three_chunks(self):
        filename = "/text_three_chunks.txt"
        in_file = INPUT_FOLDER + filename
        result = self.compressor.run(in_file)
        self.assertTrue(result)
        output_file = filename + ".lor"
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_does_not_compress_file_that_would_not_save_space_when_compressed(self):
        filename = "/text_does_not_compress1.txt"
        in_file = INPUT_FOLDER + filename
        result = self.compressor.run(in_file)
        self.assertEquals(result, False)
        self.assert_file_not_in_output_folder(filename + ".lor")
        
    def test_does_not_compress_file_that_only_has_unique_words(self):
        filename = "/text_does_not_compress2.txt"
        in_file = INPUT_FOLDER + filename
        result = self.compressor.run(in_file)
        self.assertEquals(result, False)
        self.assert_file_not_in_output_folder(filename + ".lor")

    def test_compress_with_newlines(self):
        self.compressor.chunk_size = 200
        filename = "/text_with_newlines.txt"
        in_file = INPUT_FOLDER + filename
        self.compressor.run(in_file)
        output_file = filename + ".lor"
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
        generic_text = "testtest n1 n2 testtest"
        generic_compressed_text = "[5]testtest n1 n2 <3"
        cls.in_file = "__test_folder_functionality.txt"
        cls.ref_file = "__ref_test_folder_functionality.txt.lor"
        with open(cls.in_file, "w") as f:
            f.write(generic_text)
        with open(cls.ref_file, "w") as f:
            f.write(generic_compressed_text)

    @classmethod
    def tearDownClass(cls):
        os_remove(cls.in_file)
        os_remove(cls.ref_file)

    def setUp(self):
        self.compressor = Text_Compressor(24, 5)
        self.compressor.compressed_file_extension = ".lor"
        self.result_file = "__test_folder_functionality.txt.lor"

    def tearDown(self):
        if os_path.exists(self.result_file):
            os_remove(self.result_file)

    def test_compress_no_input_folder(self):
        # FileNotFoundError: [Errno 2] No such file or directory: 'Research_Testing/tests/compressor_text_files/dump_files/__test_folder_functionality.lor'
        self.compressor.output_folder = OUTPUT_FOLDER

        self.compressor.run(self.in_file)
        self.assert_files_are_equal(f"{OUTPUT_FOLDER}/{self.result_file}", self.ref_file)
        os_remove(f"{OUTPUT_FOLDER}/{self.result_file}")

    def test_compress_no_output_folder(self):
        filename = INPUT_FOLDER + "/text_generic.txt"

        self.compressor.run(filename)
        self.assert_files_are_equal(filename + ".lor", self.ref_file)
        os_remove(filename + ".lor")

    def test_compress_no_io_folders(self):
        self.compressor.run(self.in_file)
        self.assert_files_are_equal(self.result_file, self.ref_file)