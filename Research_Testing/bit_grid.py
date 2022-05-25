
class bit_grid(object):
    def __init__(self, height, width) -> None:
        self.grid_height = height
        self.grid_width = width
        self.grid_area = self.grid_height * self.grid_width
        self.grid = [[None for _ in range(self.grid_width)] \
                     for _ in range(self.grid_height)]

    def fill_grid_with(self, data_list):
        """
        Assumes grid is empty.
        Inputs-list of data.
        Fills its grid with the data.
        Outputs-None or leftover data.
        """
        y = 0
        x = 0
        for i in range(len(data_list)):
            if self.grid_has_space():
                self.grid[y][x] = data_list[i]
                if self.exceeded_grid_width(x):
                    x = 0
                    y += 1
                else:
                    x += 1
            else:
                break
        if len(data_list) > self.grid_area:
            return data_list[self.grid_area:]
        return None

    def grid_has_space(self):
        return self.grid[-1][-1] is None

    def exceeded_grid_width(self, x):
        return x >= self.grid_width-1

    def fill_index_with(self, col, row, data):
        self.grid[row][col] = data

    def get_row(self, row):
        return self.grid[row]

    def get_col(self, target_col):
        result_col = [row[target_col] for row in self.grid]
        return result_col
    
    def print_grid(self):
        for row in self.grid:
            print(row)