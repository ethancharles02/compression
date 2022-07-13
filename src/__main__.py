from sys import path
path.append(".")

from src.GUI import Compression_GUI
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    gui = Compression_GUI()
    gui.start()