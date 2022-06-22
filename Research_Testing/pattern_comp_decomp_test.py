from pattern_compressor import Pattern_Compressor
from pattern_decompressor import Pattern_Decompressor

INPUT_FOLDER = "Research_Testing"
OUTPUT_FOLDER = "Research_Testing"

if __name__ == "__main__":
    compressor = Pattern_Compressor()
    compressor.input_folder = INPUT_FOLDER
    compressor.output_folder = OUTPUT_FOLDER

    decompressor = Pattern_Decompressor(chunk_size=1)
    decompressor.input_folder = INPUT_FOLDER
    decompressor.output_folder = OUTPUT_FOLDER

    # in_file = "test.txt"
    in_file = "compressor.py"
    
    result = compressor.run(in_file)
    print(result)
    if result:
        # decompressor.run(in_file + ".lor", "test1.txt")
        decompressor.run(in_file + ".lor", "test1.py")
