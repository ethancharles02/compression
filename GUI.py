from dis import COMPILER_FLAG_NAMES
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from os import path

from master_compressor import Master_Compressor


COMPRESS = "compress"
DECOMPRESS = "decompress"
THIS_FILE = path.basename(__file__)


class Compression_GUI():
    def __init__(self) -> None:
        self.root = self.create_root()
        self.frm = self.create_frame()
        self.in_file_entry = self.create_infile_entry_and_label()
        self.out_file_entry = self.create_outfile_entry_and_label()
        self.set_up_run_type_radio_buttons()
        self.create_run_button()

    def create_run_button(self):
        run_button=ttk.Button(self.frm,text="Run",command=self.run)
        run_button.grid(row=2,column=1)

    def create_outfile_entry_and_label(self):
        out_folder_label = ttk.Label(self.frm, text="Out folder:")
        out_folder_label.grid(row=1, column=0)
        out_folder_entry=ttk.Entry(self.frm)
        out_folder_entry.grid(row=1,column=1)
        select_out_folder_button=ttk.Button(self.frm,text="Browse",command=partial(self.openFolder,out_folder_entry))
        select_out_folder_button.grid(row=1,column=2)
        return out_folder_entry

    def create_infile_entry_and_label(self):
        in_file_label = ttk.Label(self.frm, text="In file:")
        in_file_label.grid(row=0, column=0)
        in_file_entry=ttk.Entry(self.frm)
        in_file_entry.grid(row=0,column=1)
        select_in_file_button=ttk.Button(self.frm,text="Browse",command=partial(self.openfile,in_file_entry))
        select_in_file_button.grid(row=0,column=2)
        return in_file_entry

    def create_frame(self):
        frm = ttk.Frame(self.root, padding=20)
        frm.grid()
        frm.config(height = 600, width = 400)
        return frm

    def create_root(self):
        root = tk.Tk()
        root.title(THIS_FILE)
        return root

    def set_up_run_type_radio_buttons(self):
        self.run_type = tk.StringVar()
        RBttn = tk.Radiobutton(self.frm, text = "Compress   ", variable = self.run_type, value = COMPRESS)
        RBttn.grid(row=2, column=0)
        RBttn.invoke()
        RBttn2 = tk.Radiobutton(self.frm, text = "Decompress", variable = self.run_type, value = DECOMPRESS)
        RBttn2.grid(row=3, column=0)

    def openfile(self, entryBox:ttk.Entry):
        filename = filedialog.askopenfilename()
        self.update_entry(entryBox, filename)

    def openFolder(self, entryBox:ttk.Entry):
        filename = filedialog.askdirectory()
        self.update_entry(entryBox, filename)

    def update_entry(self, entryBox:ttk.Entry, filename):
        entryBox.delete(0, tk.END)
        entryBox.insert(tk.END, filename)

    def run(self):
        choice = self.run_type.get()
        in_file = "in: " + self.in_file_entry.get() + "\n"
        out_folder = "out: " + self.out_file_entry.get() + "\n"
        if choice == COMPRESS:
            self.NewWindow(in_file + out_folder + "File Compressed Successfully")  # add the master compressor here
        elif choice == DECOMPRESS:
            self.NewWindow(in_file + out_folder + "File Decompressed Successfully")  # add the master decompressor here
        else:
            self.NewWindow("ERROR: Compress/Decompress not set!")

    def NewWindow(self, text):
        window = tk.Toplevel()
        window.geometry('300x150')
        newlabel = tk.Label(window, text=text)
        newlabel.pack()

    def start(self):
        self.root.mainloop()

    
if __name__ == "__main__":
    gui = Compression_GUI()
    gui.start()