from bit_string_generator import generate_string

# 1 1a0 b 1 0 b 1 1 b 1 0 b 0 0
# c 0 1 b 0 0a0 b 1 1a0 b 0 10

ROW_LENGTH = 5

class bit_grid:
    def __init__(self, bit_list, row_length):
        bits = "".join(bit_list).replace(" ", "")
        
        self.rows = len(bits) // row_length

        # Initialize bit list
        self.grid = []

        for y in range(self.rows):
            self.grid.append([])
            for x in range(row_length):
                self.grid[y].append(bits[y * row_length + x])
    
    def compress(self):
        pass

    def __get_row_nums(self, row_num, symbol="1"):
        return self.__get_symbol_counts(self.grid[row_num], symbol)

    def __get_column_nums(self, column_num, symbol="1"):
        bit_list = self.__get_column(column_num)
        return self.__get_symbol_counts(bit_list, symbol)
    
    def __get_column(self, column_num):
        return [self.grid[i][column_num] for i in range(self.rows)]

    def __get_symbol_counts(self, iterable, symbol="1"):
        num_list = []

        bit_count = 0
        for bit in iterable:
            if bit == symbol:
                bit_count += 1
            elif bit_count > 0:
                num_list.append(bit_count)
                bit_count = 0
        
        if bit_count > 0:
            num_list.append(bit_count)

        return num_list

    

if __name__ == "__main__":
    with open("test_bitstring.txt") as f:
        bitlist = f.readlines()
    
    grid = bit_grid(bitlist, ROW_LENGTH)

    print(grid.grid)
    print(grid.compress())