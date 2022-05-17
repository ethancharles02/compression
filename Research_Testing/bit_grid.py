from bit_string_generator import generate_string

# 1 1a0 b 1 0 b 1 1 b 1 0 b 0 0
# c 0 1 b 0 0a0 b 1 1a0 b 0 10

ROW_LENGTH = 16
COLUMN_HEIGHT = 64

class bit_grid:
    def __init__(self, bit_string:str, row_length:int, column_height:int):
        # bits = self.create_bit_string(bit_string)
        if row_length > 0:
            self.row_length = row_length
        else:
            raise(ValueError("Row length must be greater than zero!"))
        
        if column_height > 0:
            self.column_height = column_height
        else:
            raise(ValueError("Column height must be greater than zero!"))

        self.grid_size = self.column_height * self.row_length

        if self.grid_size > len(bit_string):
            raise(ValueError(f"Grid must not be larger than the number of bits. Bits given was {len(bit_string)} while the size of the grid was {self.grid_size}"))

        # Initialize bit list
        self.grid = self.__create_grid(bit_string)

    # def create_bit_string(self, bit_list):
    #     return "".join(bit_list).replace(" ", "")

    def compress(self) -> str:
        return "1b1b1b1b1c1b1b1b1b1"

    def __create_grid(self, bits:str) -> list:
        grid = []
        for y in range(self.column_height):
            grid.append([])
            for x in range(self.row_length):
                grid[y].append(bits[y * self.row_length + x])
        return grid

    def __get_row_nums(self, row_num:int, symbol:str="1") -> list:
        return self.__get_symbol_counts(self.grid[row_num], symbol)

    def __get_column_nums(self, column_num, symbol="1"):
        bit_list = self.__get_column(column_num)
        return self.__get_symbol_counts(bit_list, symbol)
    
    def __get_column(self, column_num):
        return [self.grid[i][column_num] for i in range(self.rows)]

    def __get_symbol_counts(self, iterable, symbol="1"):
        num_list = []

        consec_bit_count = 0
        for bit in iterable:
            if bit == symbol:
                consec_bit_count += 1
            elif consec_bit_count > 0:
                num_list.append(consec_bit_count)
                consec_bit_count = 0
        
        if consec_bit_count > 0:
            num_list.append(consec_bit_count)

        return num_list

    

if __name__ == "__main__":
    with open("Research_Testing/random_string_files/random_bit_strings_1.txt") as f:
        bitlist = f.read(1024)
    
    grid = bit_grid(bitlist, ROW_LENGTH, COLUMN_HEIGHT)

    print(grid.grid)
    print(grid.compress())