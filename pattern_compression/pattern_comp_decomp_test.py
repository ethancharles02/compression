# TODO
# Figure out why decompression of the test1.bin.lor file results in an error
from sys import path
path.append(".")
from pattern_compression.pattern_compressor import Pattern_Compressor
from pattern_compression.pattern_decompressor import Pattern_Decompressor
from time import monotonic

INPUT_FOLDER = "pattern_compression/random_bitstring_files/bin_bitstring_files/"
OUTPUT_FOLDER = "pattern_compression/"
# INPUT_FOLDER = "pattern_compression/"
# OUTPUT_FOLDER = "pattern_compression/"

def are_files_in_test_folders_equal(filepath1, filepath2):
    with open(filepath1, "rb") as f:
        list1 = list(f)
    with open(filepath2, "rb") as f:
        list2 = list(f)
    
    lists_equal = list1 == list2
    if not lists_equal:
        print(f"Number of bytes read till unequal bits: {analyze_lists(list1, list2)}")

    return lists_equal

def analyze_strings(string1, string2):
    string1_length = len(string1)
    string2_length = len(string2)

    if string1_length < string2_length:
        for i in range(string2_length):
            if string1[i] != string2[i]:
                print(string1[i - 1], string2[i - 1])
                print(string1[i], string2[i])
                return i

    else:
        for i in range(string1_length):
            if string1[i] != string2[i]:
                print(string1[i - 1], string2[i - 1])
                print(string1[i], string2[i])
                return i

def analyze_lists(list1, list2):
    list1_length = len(list1)
    list2_length = len(list2)

    num_bytes_read = 0

    if list1_length < list2_length:
        for i in range(list2_length):
            if list1[i] != list2[i]:
                num_bytes_read += analyze_strings(list1[i], list2[i])
                return num_bytes_read
            num_bytes_read += len(list1[i])

    else:
        for i in range(list1_length):
            if list1[i] != list2[i]:
                num_bytes_read += analyze_strings(list1[i], list2[i])
                return num_bytes_read
            num_bytes_read += len(list1[i])

if __name__ == "__main__":
    # compressor = Pattern_Compressor(raw_delimiter="0101101", max_look_ahead=50, override_compression_check=True)
    compressor = Pattern_Compressor(raw_delimiter="01011", max_look_ahead=50, override_compression_check=True, override_chunk_size=True)
    # compressor.input_folder = INPUT_FOLDER
    # compressor.output_folder = INPUT_FOLDER

    decompressor = Pattern_Decompressor(raw_delimiter="01011", chunk_size=1)
    # decompressor.input_folder = INPUT_FOLDER
    # decompressor.output_folder = OUTPUT_FOLDER

    in_file = "random_bit_strings_10000.bin"
    out_file = "test1.bin.lor"
    # in_file = "test2.bin"
    # out_file = "test3.bin.lor"
    # in_file = "test.jpg"
    # out_file = "test1.jpg"

    in_path = INPUT_FOLDER + in_file
    out_path = OUTPUT_FOLDER + out_file

    old_time = monotonic()
    result = compressor.run(in_path, out_path)
    print(f"Compression took {(monotonic() - old_time):.2f} seconds. Successful: {result}")
    if result:
        in_path_d = out_path
        out_path_d = out_path.replace(".lor", "")
        old_time = monotonic()
        # decompressor.run(in_file + ".lor", "test1.txt")
        result = decompressor.run(in_path_d, out_path_d)
        print(f"Decompression took {(monotonic() - old_time):.2f} seconds. Successful: {result}")
    
        files_equal = are_files_in_test_folders_equal(in_path, out_path_d)
        print(f"File was successfully compressed and decompressed: {files_equal}")

    # print(are_files_in_test_folders_equal(f"{INPUT_FOLDER}/{in_file}", f"{OUTPUT_FOLDER}/{out_file}"))