# TODO
# Continue TDD

class Text_Compressor(object):
    def __init__(self):
        self.data = None

    def compress(self, string:str):
        self.data = string.split(" ")
        if len(self.data) <= 1:
            pass
        elif self.data[0] == self.data[1]:
            if len(self.data[0]) > 2:
                self.data[1] = "<1"
        
        self.data = " ".join(self.data)

    def get_compressed_data(self):
        return self.data
        
if __name__ == "__main__":
    compressor = Text_Compressor()
    compressor.compress("  ")
    print(compressor.get_compressed_data())