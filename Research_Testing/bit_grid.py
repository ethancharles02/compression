# Notes:
# Count number of row b delimiters until it == num_rows then switch to columns
# Add function to optimize for compressibility and decompressibility

from bit_string_generator import generate_string
from constants import *

# NUM_COLUMNS = 16
# NUM_ROWS = 64
NUM_COLUMNS = 5
NUM_ROWS = 5

class bit_grid:
    def __init__(self, bit_string:str, num_columns:int, num_rows:int):
        # bits = self.create_bit_string(bit_string)
        if num_columns > 0:
            self.num_columns = num_columns
        else:
            raise(ValueError("Row length must be greater than zero!"))
        
        if num_rows > 0:
            self.num_rows = num_rows
        else:
            raise(ValueError("Column height must be greater than zero!"))

        self.grid_size = self.num_rows * self.num_columns

        if self.grid_size > len(bit_string):
            raise(ValueError(f"Grid must not be larger than the number of bits. Bits given was {len(bit_string)} while the size of the grid was {self.grid_size}"))

        # Initialize bit list
        self.grid = self.__create_grid(bit_string)

    def compress(self) -> str:
        row_a_delimiter = "0" * len(bin(self.num_rows)[2:]) + "10"
        row_b_delimiter = "0" * len(bin(self.num_rows)[2:]) + "11"

        column_a_delimiter = "0" * len(bin(self.num_columns)[2:]) + "10"
        column_b_delimiter = "0" * len(bin(self.num_columns)[2:]) + "11"

        # Converting rows and columns to their condensed numbers in binary
        rows = []
        for y in range(self.num_rows):
            data, num_list = self.__get_row_nums(y)
            rows.append((data, [self.__convert_to_binary(number) for number in num_list]))

        columns = []
        for x in range(self.num_columns):
            data, num_list = self.__get_column_nums(x)
            columns.append((data, [self.__convert_to_binary(number) for number in num_list]))
        
        # Columns and rows with the delimited a's between numbers
        compressed_rows_list = [row_a_delimiter.join(row[1]) for row in rows]
        for i in range(len(compressed_rows_list)):
            compressed_rows_list[i] = rows[i][0] + compressed_rows_list[i]
            
        compressed_columns_list = [column_a_delimiter.join(column[1]) for column in columns]
        for i in range(len(compressed_columns_list)):
            compressed_columns_list[i] = columns[i][0] + compressed_columns_list[i]
        

        # Columns and rows with the delimited b's between columns/rows
        compressed_row_string = row_b_delimiter.join(compressed_rows_list)
        compressed_column_string = column_b_delimiter.join(compressed_columns_list)
        
        # Dedicates 16 bytes to indicate the number of columns and rows
        # Errors if there are too many rows or columns
        binary_row_nums = str(bin(self.num_rows)[2:])
        if len(binary_row_nums) > DEDICATED_ROW_SPACE:
            raise Exception("Too many rows in the grid")
        binary_row_nums = "0"*(DEDICATED_ROW_SPACE - len(binary_row_nums)) + binary_row_nums

        binary_column_nums = str(bin(self.num_columns)[2:])
        if len(binary_column_nums) > DEDICATED_COLUMN_SPACE:
            raise Exception("Too many columns in the grid")
        binary_column_nums = "0"*(DEDICATED_COLUMN_SPACE - len(binary_column_nums)) + binary_column_nums

        column_row_num_string = binary_row_nums + binary_column_nums

        # Adds the c between the column section and the row section
        bit_string = column_row_num_string + compressed_row_string + row_b_delimiter + compressed_column_string

        return bit_string

    def __create_grid(self, bits:str) -> list:
        grid = []
        for y in range(self.num_rows):
            grid.append([])
            for x in range(self.num_columns):
                grid[y].append(bits[y * self.num_columns + x])
        return grid

    def __get_row_nums(self, row_num:int, symbol:str="1") -> tuple:
        return (symbol, self.__get_symbol_counts(self.grid[row_num], symbol))

    def __get_column_nums(self, column_num, symbol="1") -> tuple:
        bit_list = self.__get_column(column_num)
        return (symbol, self.__get_symbol_counts(bit_list, symbol))
    
    def __get_column(self, column_num) -> list:
        return [self.grid[i][column_num] for i in range(self.num_rows)]

    def __get_symbol_counts(self, iterable, symbol="1") -> list:
        num_list = []

        consec_bit_count = 0
        for bit in iterable:
            if bit == symbol:
                consec_bit_count += 1
            elif consec_bit_count > 0:
                num_list.append(str(consec_bit_count))
                consec_bit_count = 0
        
        if consec_bit_count > 0:
            num_list.append(str(consec_bit_count))

        return num_list

    def print_grid(self):
        for row in self.grid:
            print(row)

    def __convert_to_binary(self, int_string, offset=0) -> str:
        return str(bin(int(int_string) - offset))[2:]

if __name__ == "__main__":
    # with open("Research_Testing/random_string_files/random_bit_strings_1.txt") as f:
    with open("random_string_files/random_bit_strings_1.txt") as f:
        bitlist = f.read(25)
    
    grid = bit_grid(bitlist, NUM_COLUMNS, NUM_ROWS)

    grid.print_grid()
    print(grid.compress())