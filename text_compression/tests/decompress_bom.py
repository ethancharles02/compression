import unittest
from sys import path
from test_text_compressor import TXT_FOLDER
path.append("..")
from text_decompressor import Text_Decompressor
TST_FOLDER = "C:\\Users\\joshd\\Documents\\_College Classes\\2022 - Spring\\CSE 499\\compression\\Research_Testing\\tests\\compressor_text_files"
CMPR_FILE = "Book_of_Mormon_la_512_ch_262144.lor"
ORG_FILE = "Book_of_Mormon.txt"
def assert_files_in_test_folders_are_equal():
        with open(f"{TXT_FOLDER}/{CMPR_FILE.replace('.lor', '.txt')}") as f:
            test_list = list(f)
        with open(f"{TXT_FOLDER}/{ORG_FILE}") as f:
            ref_list = list(f)
        # for i in range(len(test_list)):
        #     if i == 31570:
        #         print("".join(test_list[31560:]))
        #     if test_list[i] != ref_list[i]:
        #         print(f"Index:{i}\nResult:\"{test_list[i]}\"\nExpected:\"{ref_list[i]}\"")
        print(test_list == ref_list)

compressor = Text_Decompressor()
compressor.input_folder = TST_FOLDER
compressor.output_folder = compressor.input_folder
compressor.run(CMPR_FILE)
assert_files_in_test_folders_are_equal()


