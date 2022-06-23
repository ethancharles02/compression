from pattern_compressor import Pattern_Compressor
from pattern_decompressor import Pattern_Decompressor
from time import monotonic

INPUT_FOLDER = "Research_Testing"
OUTPUT_FOLDER = "Research_Testing"

def are_files_in_test_folders_equal(filepath1, filepath2):
    with open(filepath1, "rb") as f:
        list1 = list(f)
    with open(filepath2, "rb") as f:
        list2 = list(f)
    return list1 == list2

if __name__ == "__main__":
    compressor = Pattern_Compressor(raw_delimiter="0101101", max_look_ahead=50, override_compression_check=True)
    compressor.input_folder = INPUT_FOLDER
    compressor.output_folder = OUTPUT_FOLDER

    decompressor = Pattern_Decompressor(raw_delimiter="0101101", chunk_size=1)
    decompressor.input_folder = INPUT_FOLDER
    decompressor.output_folder = OUTPUT_FOLDER

    # in_file = "test.txt"
    in_file = "test.jpg"
    out_file = "test1.jpg"

    old_time = monotonic()
    result = compressor.run(in_file)
    print(f"Compression took {(monotonic() - old_time):.2f} seconds. Successful: {result}")
    if result:
        old_time = monotonic()
        # decompressor.run(in_file + ".lor", "test1.txt")
        result = decompressor.run(in_file + ".lor", out_file)
        print(f"Decompression took {(monotonic() - old_time):.2f} seconds. Successful: {result}")
    
        files_equal = are_files_in_test_folders_equal(f"{INPUT_FOLDER}/{in_file}", f"{OUTPUT_FOLDER}/{out_file}")
        print(f"File was successfully compressed and decompressed: {files_equal}")
    # print(are_files_in_test_folders_equal(f"{INPUT_FOLDER}/{in_file}", f"{OUTPUT_FOLDER}/{out_file}"))
