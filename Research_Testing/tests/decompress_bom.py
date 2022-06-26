import filecmp
from sys import path
path.append("..")
from text_decompressor import Text_Decompressor
TST_FOLDER = "C:\\Users\\joshd\\Documents\\_College Classes\\2022 - Spring\\CSE 499\\compression\\Research_Testing\\tests\\compressor_text_files"
CMPR_FILE = "Book_of_Mormon_la_512_ch_262144.lor"
ORG_FILE = "Book_of_Mormon.txt"

compressor = Text_Decompressor()
compressor.input_folder = TST_FOLDER
compressor.output_folder = compressor.input_folder
compressor.run(CMPR_FILE)

print(filecmp.cmp(TST_FOLDER + "\\" + CMPR_FILE.replace(".txt",".lor"), TST_FOLDER + "\\" +  ORG_FILE, shallow=False))

