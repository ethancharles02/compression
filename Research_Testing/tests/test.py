# Text Compression Algorithm
from sys import path
path.append("..")
from text_compression_algorithm import Text_Compression_Algorithm

# compressor = Text_Compression_Algorithm(5)
# compressor.compress("\nword")
# string1 = "word n1 n2 n3 n4 n5\n"
# expected_string = "word n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\n"
# for i in range(11):
#     compressor.compress(string1)   
# print(f"Result:\n{compressor.get_compressed_data()}")
# print(f"Expected:\n{expected_string}")

# Text Compressor
# from sys import path
# path.append("..")
# from os import getcwd, listdir, remove as os_remove, path as os_path

# from text_compressor import Text_Compressor

# TXT_FOLDER = "compressor_text_files"
# INPUT_FOLDER = f"{TXT_FOLDER}/test_files"
# REF_FOLDER = f"{TXT_FOLDER}/reference_files"
# OUTPUT_FOLDER = f"{TXT_FOLDER}/dump_files"


# # setup
# compressor = Text_Compressor(24, 5)
# compressor.input_folder = INPUT_FOLDER
# compressor.output_folder = OUTPUT_FOLDER
# # test
# filename = "text_out_of_chunk_range.txt"
# result = compressor.run(filename)
# assert result is True
# output_file = filename.replace(".txt", ".lor") 

# # prints
# print("Result:")
# with open(OUTPUT_FOLDER + '/' + output_file, "r") as f:
#     print(f.readlines())
# print("Expected:")
# with open(REF_FOLDER + '/' + output_file, "r") as f:
#     print(f.readlines())

# # teardown
# for f in listdir(OUTPUT_FOLDER):
#             os_remove(os_path.join(OUTPUT_FOLDER, f))
