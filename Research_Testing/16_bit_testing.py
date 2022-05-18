from random import randint
from os import remove
NUM_STRINGS = 1
RANDOM_BITS_FILE = "Research_Testing\\random_string_files\\random_bit_strings_" + str(NUM_STRINGS) + ".txt"

def read_bits(bit_dict,bits):
    four_bits = ""
    eight_bits = ""
    # sixteen_bits = ""
    for bit in bits:
        four_bits += bit
        eight_bits += bit
        # sixteen_bits += bit
        four_bits = something(bit_dict, four_bits, 4)
        eight_bits = something(bit_dict, eight_bits, 8)
        # sixteen_bits = something(bit_dict, sixteen_bits, 16)
        
def something(bit_dict, bits, num_bits):
    if len(bits) >= num_bits:
        update_dictionary(bit_dict, bits)
        return ""
    else:
        return bits

def update_dictionary(bit_dict, bits):
    if bits in bit_dict:
            bit_dict[bits] += 1
    else: bit_dict[bits] = 1

def create_random_bit_string_file():
    with open(RANDOM_BITS_FILE, "w") as f:
        for _ in range (NUM_STRINGS):
            bit_string = "".join([str(randint(0, 1)) for _ in range(2042)])
            f.write(bit_string + '\n')

if __name__ == "__main__":
    # bit_dictionary = {}
    # with open(RANDOM_BITS_FILE, "r") as f:
    #     line = f.readline()
    #     while line:
    #         read_bits(bit_dictionary, line)
    #         line = f.readline()
    # data = []
    # for key in bit_dictionary.keys():
    #     data.append((bit_dictionary[key], key))
    # data.sort(reverse=True, key=lambda x: x[0])

    # with open("Research_Testing\\research_test.txt", "w") as f:
    #     for _tuple in data:
    #         f.write("{}:\t\t{}\n".format(_tuple[1], _tuple[0]))
    create_random_bit_string_file()
    
