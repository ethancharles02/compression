# Update metadata tuple for a's delimiters
from bit_string_generator import generate_string

# 1 1a0 b 1 0 b 1 1 b 1 0 b 0 0
# c 0 1 b 0 0a0 b 1 1a0 b 0 10

# ROW_LENGTH = 16
# COLUMN_HEIGHT = 64
ROW_LENGTH = 5
COLUMN_HEIGHT = 5

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
        rows = []
        for y in range(self.column_height):
            data, num_list = self.__get_row_nums(y)
            rows.append((data, [self.__convert_to_binary(number) for number in num_list]))

        columns = []
        for x in range(self.row_length):
            data, num_list = self.__get_column_nums(x)
            columns.append((data, [self.__convert_to_binary(number) for number in num_list]))
        
        # Columns and rows with the delimited a's between numbers
        compressed_columns_list = ["a".join(column[1]) for column in columns]
        for i in range(len(compressed_columns_list)):
            compressed_columns_list[i].insert(0, columns[i][0])
        
        print(compressed_columns_list)
        # compressed_rows_list = ["a".join(row[1]) for row in rows]
        # for compressed_column in compressed_columns_list:
        #     compressed_column.insert(0, '1')

        # # Columns and rows with the delimited b's between columns/rows
        # compressed_column_string = "b".join(compressed_columns_list)
        # compressed_row_string = "b".join(compressed_rows_list)
        
        # # Adds the c between the column section and the row section
        # bit_string = compressed_column_string + "c" + compressed_row_string

        # return bit_string

    def __create_grid(self, bits:str) -> list:
        grid = []
        for y in range(self.column_height):
            grid.append([])
            for x in range(self.row_length):
                grid[y].append(bits[y * self.row_length + x])
        return grid

    def __get_row_nums(self, row_num:int, symbol:str="1") -> tuple:
        return (symbol, self.__get_symbol_counts(self.grid[row_num], symbol))

    def __get_column_nums(self, column_num, symbol="1") -> tuple:
        bit_list = self.__get_column(column_num)
        return (symbol, self.__get_symbol_counts(bit_list, symbol))
    
    def __get_column(self, column_num) -> list:
        return [self.grid[i][column_num] for i in range(self.column_height)]

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

    def __convert_to_binary(self, int_string, offset=1) -> str:
        return str(bin(int(int_string) - offset))[2:]

if __name__ == "__main__":
    with open("Research_Testing/random_string_files/random_bit_strings_1.txt") as f:
        bitlist = f.read(25)
    
    grid = bit_grid(bitlist, ROW_LENGTH, COLUMN_HEIGHT)

    grid.print_grid()
    print(grid.compress())