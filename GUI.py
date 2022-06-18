import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from os import path
this_file = path.basename(__file__)

def openfile(entryBox):
    filename = filedialog.askopenfilename()
    entryBox.delete(0, tk.END)
    entryBox.insert(tk.END, filename)

def openFolder(entryBox):
    filename = filedialog.askdirectory()
    entryBox.delete(0, tk.END)
    entryBox.insert(tk.END, filename)

def run():
    choice = Var1.get()
    if choice == "Compress":
        NewWindow("File Compressed Successfully")  # add the master compressor here
    elif choice == "Decompress":
        NewWindow("File Decompressed Successfully")  # add the master decompressor here
    else:
        NewWindow("Failed to run.")

def NewWindow(text):
    window = tk.Toplevel()
    window.geometry('300x150')
    newlabel = tk.Label(window, text = text)
    newlabel.pack()

root = tk.Tk()
frm = ttk.Frame(root, padding=20)
frm.grid()
root.title(this_file)
frm.config(height = 600, width = 400)

InFilelabel = ttk.Label(frm, text="File to compress:")
InFilelabel.grid(row=0, column=0)

fileEntryIn=ttk.Entry(frm)
fileEntryIn.grid(row=0,column=1)

selectInFileButton=ttk.Button(frm,text="Browse",command=partial(openfile,fileEntryIn))
selectInFileButton.grid(row=0,column=2)

OutFolderLabel = ttk.Label(frm, text="Decompress to:")
OutFolderLabel.grid(row=1, column=0)

FolderEntryOut=ttk.Entry(frm)
FolderEntryOut.grid(row=1,column=1)

selectOutFolderButton=ttk.Button(frm,text="Browse",command=partial(openFolder,FolderEntryOut))
selectOutFolderButton.grid(row=1,column=2)

Var1 = tk.StringVar()
 
RBttn = tk.Radiobutton(frm, text = "Compress   ", variable = Var1, value = "Compress")
RBttn.grid(row=2, column=0)
RBttn.invoke()

RBttn2 = tk.Radiobutton(frm, text = "Decompress", variable = Var1, value = "Decompress")
RBttn2.grid(row=3, column=0)

selectInFileButton=ttk.Button(frm,text="Run",command=run)
selectInFileButton.grid(row=2,column=1)


root.mainloop()