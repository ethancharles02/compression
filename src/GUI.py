import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from os import path
import json

# eval(f"from algorithms.{'master_compressor'} import Master_Compressor")

from src.master_compressor import Master_Compressor, WrongFileType
from src.algorithms.algorithms import ALGORITHMS, ALGORITHMS_OBJECTS

COMPRESS = "compress"
DECOMPRESS = "decompress"
THIS_FILE = path.basename(__file__)


class Compression_GUI():
    def __init__(self) -> None:
        self.get_algorithm_data()
        self.compresser = Master_Compressor(self.algorithms, ALGORITHMS_OBJECTS)
        self.define_grid_locations()
        self.root = self.create_root()
        self.frm = self.create_frame()
        self.in_file_entry = self.create_infile_entry_and_label()
        self.out_file_entry = self.create_outfile_entry_and_label()
        self.set_up_combo_box()
        self.set_up_run_type_radio_buttons()
        self.create_run_button()

    def define_grid_locations(self):
        self.in_file_label_loc =            (0,0)
        self.in_file_entry_loc =            (1,0)
        self.select_in_file_button_loc =    (2,0)
        self.out_folder_label_loc =         (0,1)
        self.out_folder_entry_loc =         (1,1)
        self.select_out_folder_button_loc = (2,1)
        self.run_type_radio_loc1 =          (1,2)
        self.run_type_radio_loc2 =          (1,3)
        self.algorithm_box_loc =            (1,4)
        self.combo_box_label_loc =          (0,4)
        self.run_botton_loc =               (2,4)

    def get_algorithm_data(self):
        self.algorithms = ALGORITHMS
        # if not path.exists("algorithms/algorithms.json"):
        #     raise FileNotFoundError("No algorithms json file found")
        # with open("algorithms/algorithms.json") as f:
        #     self.algorithms = json.load(f)

    def create_root(self):
        root = tk.Tk()
        root.title(THIS_FILE)
        return root

    def create_frame(self):
        frm = ttk.Frame(self.root, padding=20)
        frm.grid(sticky="we")
        return frm

    def create_run_button(self):
        run_button=ttk.Button(self.frm,text="Run",command=self.run)
        run_button.grid(row=self.run_botton_loc[1], column=self.run_botton_loc[0], sticky="we")

    def create_outfile_entry_and_label(self):
        out_folder_label = ttk.Label(self.frm, text="Out folder:")
        out_folder_label.grid(row=self.out_folder_label_loc[1], column=self.out_folder_label_loc[0], sticky="e")
        out_folder_entry=ttk.Entry(self.frm)
        out_folder_entry.grid(row=self.out_folder_entry_loc[1], column=self.out_folder_entry_loc[0], sticky="we")
        select_out_folder_button=ttk.Button(self.frm,text="Browse",command=partial(self.openFolder,out_folder_entry))
        select_out_folder_button.grid(row=self.select_out_folder_button_loc[1], column=self.select_out_folder_button_loc[0], sticky="we")
        return out_folder_entry

    def create_infile_entry_and_label(self):
        in_file_label = ttk.Label(self.frm, text="In file:")
        in_file_label.grid(row=self.in_file_label_loc[1], column=self.in_file_label_loc[0], sticky="e")
        in_file_entry = ttk.Entry(self.frm)
        in_file_entry.grid(row=self.in_file_entry_loc[1], column=self.in_file_entry_loc[0], sticky="we")
        select_in_file_button = ttk.Button(self.frm, text="Browse", command=partial(self.openfile, in_file_entry))
        select_in_file_button.grid(row=self.select_in_file_button_loc[1], column=self.select_in_file_button_loc[0], sticky="we")
        return in_file_entry

    def set_up_run_type_radio_buttons(self):
        self.run_type = tk.StringVar()
        RBttn = tk.Radiobutton(self.frm, text = "Compress   ", variable = self.run_type, value = COMPRESS, command=self.enable_combo_box)
        RBttn.grid(row=self.run_type_radio_loc1[1], column=self.run_type_radio_loc1[0])
        RBttn.invoke()
        RBttn2 = tk.Radiobutton(self.frm, text = "Decompress", variable = self.run_type, value = DECOMPRESS, command=self.disable_combo_box)
        RBttn2.grid(row=self.run_type_radio_loc2[1], column=self.run_type_radio_loc2[0])
    
    def disable_combo_box(self):
        if self.is_combo_box_enabled:
            self.old_algorithm = self.algorithm.get()
            self.algorithm_box["state"] = "disabled"
            self.is_combo_box_enabled = False
            self.algorithm_box.set("")

    def enable_combo_box(self):
        if not self.is_combo_box_enabled:
            self.algorithm_box.set(self.old_algorithm)
            self.algorithm_box["state"] = "readonly"
            self.is_combo_box_enabled = True

    def set_up_combo_box(self):
        out_folder_label = ttk.Label(self.frm, text="Algorithm:")
        out_folder_label.grid(row=self.combo_box_label_loc[1], column=self.combo_box_label_loc[0], sticky="e")
        self.algorithm = tk.StringVar()
        algorithms = list(self.algorithms.keys())
        self.old_algorithm = algorithms[0]

        self.algorithm_box = ttk.Combobox(self.frm, textvariable=self.algorithm, values=algorithms)
        self.algorithm_box["state"] = "readonly"
        self.is_combo_box_enabled = True
        self.algorithm_box.set(self.old_algorithm)
        self.algorithm_box.grid(row=self.algorithm_box_loc[1], column=self.algorithm_box_loc[0], sticky="we")

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
        in_file = self.in_file_entry.get()
        out_folder = self.out_file_entry.get()
        if len(out_folder) == 0:
            out_folder = path.dirname(in_file)
        if choice == COMPRESS:
            try:
                if self.compresser.compress(in_file, out_folder, self.algorithm.get()):
                    self.NewWindow(in_file + "\ncompressed successfully to\n" + out_folder)
                else:
                    self.NewWindow("Failed to compress. File is not compressible with this algorithm.")
            except WrongFileType:
                self.NewWindow("ERROR! Wrong file type!")
            except FileNotFoundError:
                self.NewWindow("ERROR! file not found!")
            except Exception:
                self.NewWindow("There was an error!")
        elif choice == DECOMPRESS:
            try:
                self.compresser.decompress(in_file, out_folder)
                self.NewWindow(in_file + "\ndecompressed successfully to\n" + out_folder)
            except WrongFileType:
                self.NewWindow("ERROR! Wrong file type!")
            except FileNotFoundError:
                self.NewWindow("ERROR! file not found!")
            except Exception:
                self.NewWindow("There was an error!")
        else:
            self.NewWindow("ERROR: Compress/Decompress not selected!")

    def NewWindow(self, text):
        text_len = max([len(line) for line in text.split('\n')])
        window = tk.Toplevel()
        window.geometry(f'{text_len*9}x50')
        newlabel = tk.Label(window, text=text)
        newlabel.pack()

    def start(self):
        self.root.mainloop()

    
if __name__ == "__main__":
    gui = Compression_GUI()
    # print(gui.file_extensions[".lorp"])
    # print(gui.algorithms)
    gui.start()