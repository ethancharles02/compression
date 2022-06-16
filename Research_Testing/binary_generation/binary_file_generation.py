from bitarray import bitarray
import numpy as np

from os import fstat
from random import randint
from time import monotonic
from array import *

NUM_STRINGS = 10000
RANDOM_BITS_FILE = "Research_Testing\\random_bitstring_files\\random_bit_strings_" + str(NUM_STRINGS) + ".txt"

# def write_binary_string_to_file(filepath, string:str):
#     # split string to 8 bites long chunks
#     splits = [string[x:x + 8] for x in range(0, len(string), 8)]
#     # splits = string.split()

#     bin_array_in = array('B')

#     # convert bits to int and add to list
#     for split in splits:
#         bin_array_in.append(int(split, 2))

#     # dump list to file
#     with open(filepath, "wb+") as f:
#         bin_array_in.tofile(f)
#         f.close()

# def read_binary_file_to_string(filepath):
#     bin_array_out = array('B')
#     # get the list from file
#     with open(filepath, "rb+") as f:
#         file_size = fstat(f.fileno()).st_size
#         # bin_array_out.fromfile(f, len(bin_array_in))
#         bin_array_out.fromfile(f, file_size)
#         f.close()

#     # convert back to bin and join to one string 
#     string = ""
#     for i in bin_array_out:
#         string += "{:08b}".format(i, "08b")

#     return string

def write_binary_string_to_file(filepath, string:str):
    bitarr = bitarray(list(map(int,string)))

    with open(filepath,"wb+") as f:
        bitarr.tofile(f)

def read_binary_file_to_string(filepath):
    with open(filepath, "rb") as f:
        string = "".join(_reformat_bin(list(map(str,np.fromfile(f,"u1")))))
    
    return string

def create_random_bit_string_file():
    with open(RANDOM_BITS_FILE, "w") as f:
        for _ in range (NUM_STRINGS):
            bit_string = "".join([str(randint(0, 1)) for _ in range(2048)])
            f.write(bit_string + '\n')

def _reformat_bin(dec_string_array):
    byte_array = ["0"*(8 - len(bitstring)) + bitstring for bitstring in [bin(int(num_string))[2:] for num_string in dec_string_array]]
    return byte_array

if __name__ == "__main__":
    old_time = monotonic()

    with open("Research_Testing/random_bitstring_files/random_bit_strings_10000.txt", "r") as f:
        binary_string_list = f.read().splitlines()

    binary_string = "".join(binary_string_list)
    # binary_string = "00000000 11111111".replace(" ", "")

    path = "Research_Testing/binary_generation/"
    file = "bin1.bin"
    filepath = path + file
    write_binary_string_to_file(filepath, binary_string)
    new_string = read_binary_file_to_string(filepath)
    print(len(binary_string), len(new_string))
    print(new_string == binary_string)

    print(monotonic() - old_time)

    # create_random_bit_string_file()

