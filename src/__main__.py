from sys import path
path.append(".")

from src.GUI import Compression_GUI

if __name__ == "__main__":
    gui = Compression_GUI()
    gui.start()