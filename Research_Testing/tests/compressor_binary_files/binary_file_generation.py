from bitarray import bitarray
import numpy as np

from os import fstat, remove as os_remove, listdir, path as os_path
from random import randint
from time import monotonic
from array import *

NUM_STRINGS = 10000
RANDOM_BITS_FILE = "Research_Testing\\random_bitstring_files\\random_bit_strings_" + str(NUM_STRINGS) + ".txt"

TEST_TEXT_FILEPATH = "Research_Testing\\tests\\compressor_binary_files\\test_text_files"
REFERENCE_TEXT_FILEPATH = "Research_Testing\\tests\\compressor_binary_files\\reference_text_files"
TEST_FILEPATH = "Research_Testing\\tests\\compressor_binary_files\\test_files"
REFERENCE_FILEPATH = "Research_Testing\\tests\\compressor_binary_files\\reference_files"

def write_binary_string_to_file(filepath, string:str):
    bitarr = bitarray(list(map(int,string)))

    with open(filepath,"wb+") as f:
        bitarr.tofile(f)
        # f.write(bitarr)

def read_binary_file_to_string(filepath):
    with open(filepath, "rb") as f:
        string = "".join(_reformat_bin(list(map(str,np.fromfile(f,"u1")))))
    
    return string

def read_bytes_from_file_to_string(file, num_bytes):
    return bin(int(file.read(num_bytes).hex(), base=16))[2:]

def create_random_bit_string_file():
    with open(RANDOM_BITS_FILE, "w") as f:
        for _ in range (NUM_STRINGS):
            bit_string = "".join([str(randint(0, 1)) for _ in range(2048)])
            f.write(bit_string + '\n')

def _reformat_bin(dec_string_array):
    byte_array = ["0"*(8 - len(bitstring)) + bitstring for bitstring in [bin(int(num_string))[2:] for num_string in dec_string_array]]
    return byte_array

def read_text_file_to_binary_string(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
    
    for i in range(len(lines)):
        lines[i] = lines[i].replace(" ", "")

    return "".join(lines)

def is_txt_binary_file_equal_to_bin(txt_binary_filepath, binary_filepath):
    return read_binary_file_to_string(binary_filepath) == read_text_file_to_binary_string(txt_binary_filepath)

def is_txt_folder_equal_to_bin_folder(txt_folderpath, bin_folderpath):
    txt_files = listdir(txt_folderpath)
    bin_files = listdir(bin_folderpath)

    if len(txt_files) != len(bin_files):
        return False

    for txt_file, bin_file in zip(txt_files, bin_files):
        if not is_txt_binary_file_equal_to_bin(os_path.join(txt_folderpath, txt_file), os_path.join(bin_folderpath, bin_file)):
            return False
    
    return True

def convert_txt_files_to_bin(input_folder, output_folder, clean_output=True, new_file_extension=None):
    if clean_output:
        for f in listdir(output_folder):
            os_remove(os_path.join(output_folder, f))
    
    if new_file_extension is None:
        new_file_extension = ".bin"

    for file in listdir(input_folder):
        string = read_text_file_to_binary_string(os_path.join(input_folder, file))
        write_binary_string_to_file(os_path.join(output_folder, file.replace(".txt", new_file_extension)), string)
        
if __name__ == "__main__":

    # path = "Research_Testing/"
    # file = "test.txt"
    # filepath = path + file
    # new_string = read_binary_file_to_string(filepath)

    # print(new_string)

    # path = "Research_Testing/"
    # file = "test1.txt"
    # filepath = path + file
    # new_string = read_binary_file_to_string(filepath)

    # print(new_string)
    # create_random_bit_string_file()

    convert_txt_files_to_bin(TEST_TEXT_FILEPATH, TEST_FILEPATH)
    convert_txt_files_to_bin(REFERENCE_TEXT_FILEPATH, REFERENCE_FILEPATH, new_file_extension=".bin.lor")

    print(is_txt_folder_equal_to_bin_folder(TEST_TEXT_FILEPATH, TEST_FILEPATH))
    print(is_txt_folder_equal_to_bin_folder(REFERENCE_TEXT_FILEPATH, REFERENCE_FILEPATH))