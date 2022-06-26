from sys import path
path.append("..")
from text_compression_algorithm import Text_Compression_Algorithm

compressor = Text_Compression_Algorithm(5)
string1 = "word n1 n2 n3 n4 n5\n"
expected_string = "word n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\nword n1 n2 n3 n4 n5\n"
for i in range(11):
    compressor.compress(string1)   
print(f"Result:\n{compressor.get_compressed_data()}")
print(f"Expected:\n{expected_string}")
