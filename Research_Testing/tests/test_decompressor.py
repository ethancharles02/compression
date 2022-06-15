import unittest
from sys import path
path.append("..")
from os import getcwd, listdir, remove as os_remove, path as os_path

from decompressor import Decompressor, WrongFileFormatError


TXT_FOLDER = "Research_Testing/tests/compressor_text_files"
TST_FOLDER = f"{TXT_FOLDER}/test_files"
INPUT_FOLDER = f"{TXT_FOLDER}/reference_files"
OUTPUT_FOLDER = f"{TXT_FOLDER}/dump_files"

class Test_Decompressor(unittest.TestCase):
    def setUp(self):
        self.decompressor = Decompressor()
        self.decompressor.input_folder = INPUT_FOLDER
        self.decompressor.output_folder = OUTPUT_FOLDER

    def tearDown(self):
        for f in listdir(OUTPUT_FOLDER):
            os_remove(os_path.join(OUTPUT_FOLDER, f))

    def assert_files_in_test_folders_are_equal(self, tst_filename, ref_filename = None):
        if ref_filename == None:
            ref_filename = tst_filename
        with open(f"{OUTPUT_FOLDER}/{tst_filename}") as f:
            test_list = list(f)
        with open(f"{TST_FOLDER}/{ref_filename}") as f:
            ref_list = list(f)
        self.assertListEqual(test_list, ref_list)

    def test_reading_improperly_formatted_file(self):
        self.decompressor.input_folder = TST_FOLDER
        self.assertRaises(WrongFileFormatError, self.decompressor.run, "wrong_format.txt")

    def test_gets_correct_look_ahead_value_from_generic_file(self):
        filename = "text_generic.lor"
        self.decompressor.run(filename)
        self.assertEqual(self.decompressor.look_ahead, 5)

    def test_gets_correct_look_ahead_value_from_different_look_ahead_file(self):
        filename = "different_look_ahead.lor"
        self.decompressor.run(filename)
        self.assertEqual(self.decompressor.look_ahead, 10)

    def test_read_one_word(self):
        filename = "text_generic.lor"
        with open(f"{INPUT_FOLDER}/{filename}", "r") as f:
            self.decompressor._get_look_ahead(f)
            self.assertTrue(self.decompressor.read_one_word(f))
        self.assertEqual(self.decompressor.get_decompressed_data(), "testtest")
    
    def test_read_two_words(self):
        filename = "text_generic.lor"
        with open(f"{INPUT_FOLDER}/{filename}", "r") as f:
            self.decompressor._get_look_ahead(f)
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f))
        self.assertEqual(self.decompressor.get_decompressed_data(), "testtest n1")

    def test_read_word_before_newline_char(self):
        filename = "text_with_newlines.lor"
        with open(f"{INPUT_FOLDER}/{filename}", "r") as f:
            self.decompressor._get_look_ahead(f)
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f))
        self.assertEqual(self.decompressor._decompressed_data[-1], "\n")
    
    def test_read_word_after_newline_char(self):
        filename = "text_with_newlines.lor"
        with open(f"{INPUT_FOLDER}/{filename}", "r") as f:
            self.decompressor._get_look_ahead(f)
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f))
        self.assertEqual(self.decompressor._decompressed_data[-1], "test2")
    
    def test_decompress_nothing(self):
        self.assertEqual(self.decompressor._decompress(""), "")

    def test_decompress_reference_with_nothing_to_reference(self):
        self.decompressor._decompressed_data = []
        self.assertEqual(self.decompressor._decompress("<1"), "<1")

    def test_decompress_word_with_escape_char(self):
        self.decompressor._decompressed_data = ["hello", "to", "this", "World"]
        self.assertEqual(self.decompressor._decompress("~<1"), "~<1")

    def test_decompress_reference_with_newline_in_front(self):
        self.decompressor._decompressed_data = ["hello", "to", "this", "World"]
        self.assertEqual(self.decompressor._decompress("\n<1"), "\nWorld")

    def test_decompress_reference_one_word_away(self):
        self.decompressor._decompressed_data = ["hello", "to", "this", "World"]
        self.assertEqual(self.decompressor._decompress("<1"), "World")

    def test_decompress_reference_three_words_away(self):
        self.decompressor._decompressed_data = ["hello", "to", "this", "World"]
        self.assertEqual(self.decompressor._decompress("<4"), "hello")

    def test_read_and_decompress_one_word(self):
        filename = "text_generic.lor"
        with open(f"{INPUT_FOLDER}/{filename}", "r") as f:
            self.decompressor._get_look_ahead(f)
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f))
            self.assertTrue(self.decompressor.read_one_word(f)) # reference
        self.assertEqual(self.decompressor._decompressed_data[-1], "testtest")
    
    def test_build_up_decompressed_data_list(self):
        filename = "text_generic.lor"
        with open(f"{INPUT_FOLDER}/{filename}", "r") as f:
            self.decompressor._get_look_ahead(f)
            self.decompressor.look_ahead = 3  # This is so it won't read a reference yet.
            self.decompressor.fill_decompressed_data(f)
        self.assertEqual(self.decompressor.get_decompressed_data(), "testtest n1 n2")

    def test_default_input_folder(self):
        x = Decompressor()
        self.assertEqual(x.input_folder, getcwd())

    def test_default_output_folder(self):
        x = Decompressor()
        self.assertEqual(x.output_folder, getcwd())

    def test_generic_file_decompresses(self):
        filename = "text_generic.lor"
        self.decompressor.run(filename)
        output_file = filename.replace(".lor", ".txt")
        self.assert_files_in_test_folders_are_equal(output_file)

    def test_checks_length_of_decompressor_decompressed_data(self):
        filename = "text_three_chunks.lor"
        self.decompressor.run(filename)
        self.assertEqual(len(self.decompressor._decompressed_data), 5)

    def test_decompress_file_with_newlines(self):
        filename = "text_with_newlines.lor"
        self.decompressor.run(filename)
        output_file = filename.replace(".lor", ".txt")
        self.assert_files_in_test_folders_are_equal(output_file)
    