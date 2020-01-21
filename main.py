from tkinter import *
from tkinter import filedialog
from doc_class import document
import sys


class Redirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, input):
        self.textbox.configure(state='normal')
        self.textbox.insert(INSERT, input)
        self.textbox.configure(state='disabled')

    def flush(self):
        pass


class UI:
    def decrypt(self):
        try:
            doc = document(self.inputfile, self.outputfile.get())
            doc.decrypt()
        except IOError:
            print("Cannot open file")
        except ValueError:
            print("Cannot decrypt")

    def encrypt(self):
        doc = document(self.inputfile, self.outputfile.get())
        doc.encrypt()

    def __init__(self, master):
        self.topframe = Frame(master, bg="#2f2f2f", pady=5)
        self.topframe.pack(expand=TRUE, side=TOP, fill=BOTH)
        self.inputfile = ""
        self.show_inputfile = Label(self.topframe, text="No input file", bg="#2f2f2f", fg="#7e7e7e", pady=5)
        self.browse = Button(self.topframe, text='Browse', activebackground="#717171", bg="#1d1d1d", fg="#d0d0d0", bd=1,
                             command=self.read_filename)
        self.middleframe = Frame(master, bg="#505050")
        self.middleframe.pack(expand=TRUE, side=TOP, fill=BOTH)
        self.output_prompt = Label(self.middleframe, text="Save output as:", bg="#505050", fg="#bfbfbf")
        self.outputfile = Entry(self.middleframe, justify=LEFT)
        self.botframe = Frame(master, bg="#2a2a2a")
        self.botframe.pack(expand=TRUE, side=BOTTOM, fill=BOTH)
        self.select_enc = Button(self.botframe, text="Encrypt", relief=SUNKEN, bg="#777777", activebackground="#898989",
                                 bd=1, command=self.encrypt)
        self.select_dec = Button(self.botframe, text="Decrypt", relief=SUNKEN, bg="#777777", activebackground="#898989",
                                 bd=1, command=self.decrypt)
        self.select_dec.config(highlightthickness=0, highlightbackground="#777777")
        self.select_enc.config(highlightthickness=0, highlightbackground="#777777")

        self.browse.pack(side=TOP)
        self.show_inputfile.pack(fill=Y, side=TOP)
        self.output_prompt.grid(row=1, column=1, padx=15, pady=5, sticky=W+E)
        self.outputfile.grid(row=1, column=2, padx=5, pady=5, sticky=W+E)
        self.middleframe.grid_columnconfigure(2, weight=1)
        self.select_enc.pack(side=TOP, anchor=W, fill=X)
        self.select_dec.pack(side=TOP, anchor=W, fill=X)

    def read_filename(self):
        self.inputfile = filedialog.askopenfilename(title='Browse', filetypes=[("Text files", "*.txt")])
        self.show_inputfile.configure(text=self.inputfile)


root = Tk()
root.title("Encryptor/Decryptor")
gui_print = Text(root, state='disabled', bg="#353535", fg="#bbbbbb")
gui_print.pack(side=BOTTOM, fill=BOTH)
gui_print.config(highlightthickness=0)

sys.stdout = Redirector(gui_print)

window = UI(root)

root.mainloop()
