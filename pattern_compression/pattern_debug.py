from sys import path
path.append(".")
from tests.compressor_binary_files.binary_file_generation import read_binary_file_to_string, convert_txt_files_to_bin, output_bytes_to_file, read_bytes_to_string

def get_smallest_string_where_error_occurs():
    pass

if __name__ == "__main__":

    path = "pattern_compression/random_bitstring_files/bin_bitstring_files/"
    filename = "random_bit_strings_100.bin"
    filepath = path + filename

    second_path = "pattern_compression/"
    second_filename = "test1.bin"
    second_filepath = second_path + second_filename
    print(read_bytes_to_string(filepath, 264, 268))
    print(read_bytes_to_string(second_filepath, 264, 268))

    path = "pattern_compression/"
    filename = "test2.bin"
    out_filepath = path + filename

    output_bytes_to_file(filepath, out_filepath, 264, 268)
    # new_string = read_binary_file_to_string(out_filepath)
    # new_string = read_binary_file_to_string(filepath)

    # print(new_string)

    # path = "Research_Testing/"
    # file = "test1.bin"
    # filepath = path + file
    # new_string = read_binary_file_to_string(filepath)

    # print(new_string)

    # convert_txt_files_to_bin("Research_Testing/random_bitstring_files", "Research_Testing\\random_bitstring_files\\bin_bitstring_files")