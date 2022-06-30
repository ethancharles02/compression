from bz2 import compress
from sys import path
path.append("..")
from text_compression.text_compressor import Text_Compressor

compressor = Text_Compressor(262144, 512)
compressor.input_folder = "C:\\Users\\joshd\\Documents\\_College Classes\\2022 - Spring\\CSE 499\\compression\\Research_Testing\\tests\\compressor_text_files"
compressor.output_folder = compressor.input_folder
compressor.run("Book_of_Mormon.txt", "Book_of_Mormon_la_512_ch_262144.lor")