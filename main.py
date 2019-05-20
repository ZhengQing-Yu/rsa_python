from tkinter import *
from tkinter import filedialog
from encryptor import encrypt
from decryptor import decrypt
from doc_class import document


def redirector(inputStr):
    gui_print.insert(INSERT, inputStr)


sys.stdout.write = redirector


class UI:
    def __init__(self, master):
        self.topframe = Frame(master, bg="#2f2f2f", pady=5)
        self.topframe.pack(expand=TRUE, side=TOP, fill=BOTH)
        self.inputfile = ""
        self.show_inputfile = Label(self.topframe, text="No input file", bg="#2f2f2f", fg="#7e7e7e", pady=5)
        self.browse = Button(self.topframe, text='Browse', activebackground="#717171", bg="#1d1d1d", fg="#d0d0d0",
                             bd=1, command=self.read_filename)
        self.middleframe = Frame(master, bg="#505050")
        self.middleframe.pack(expand=TRUE, side=TOP, fill=BOTH)
        self.output_prompt = Label(self.middleframe, text="Save output as:", bg="#505050", fg="#bfbfbf")
        self.outputfile = Entry(self.middleframe, justify=LEFT)
        self.botframe = Frame(master, bg="#2a2a2a")
        self.botframe.pack(expand=TRUE, side=BOTTOM, fill=BOTH)
        self.select_enc = Button(self.botframe, text="Encrypt", relief=RAISED,
                                 command=self.enc())
        self.select_dec = Button(self.botframe, text="Decrypt", relief=RAISED,
                                 command=self.dec)

        self.test = Button(self.topframe, command=self.print1)
        self.test.pack()

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

    def print1(self):
        print(self.inputfile)
        print(self.outputfile.get())
        print(self.inputfile + ' concatenated with ' + self.outputfile.get())

    def dec(self):
        decrypt(self.inputfile, self.outputfile.get())

    def enc(self):
        encrypt(self.inputfile, self.outputfile.get())


root = Tk()
root.title("Encryptor/Decryptor")
gui_print = Text(root)
gui_print.pack(side=BOTTOM, fill=BOTH)

window = UI(root)

root.mainloop()
