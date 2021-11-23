from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from getpass import getpass
import tkinter as tk
import key_object_rsa as RSA
import argparse
import sys
import hashlib
import encryptor
import decryptor


class Redirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, stdout_output):
        self.textbox.configure(state='normal')
        self.textbox.insert(tk.INSERT, stdout_output)
        self.textbox.configure(state='disabled')

    def flush(self):
        pass


class UI:
    def __init__(self, master):
        self.topframe = tk.Frame(master, bg="#2f2f2f", pady=5)
        self.topframe.pack(expand=tk.TRUE, side=tk.TOP, fill=tk.BOTH)
        self.inputfile = ""
        self.show_inputfile = tk.Label(self.topframe, text="No input file", bg="#2f2f2f", fg="#7e7e7e", pady=5)
        self.browse = tk.Button(self.topframe, text='Browse', activebackground="#717171", bg="#1d1d1d", fg="#d0d0d0",
                                bd=1, command=self.read_filename)
        self.middleframe = tk.Frame(master, bg="#505050")
        self.middleframe.pack(expand=tk.TRUE, side=tk.TOP, fill=tk.BOTH)
        self.output_prompt = tk.Label(self.middleframe, text="Save output as:", bg="#505050", fg="#bfbfbf")
        self.outputfile = tk.Entry(self.middleframe, justify=tk.LEFT)
        self.botframe = tk.Frame(master, bg="#2a2a2a")
        self.botframe.pack(expand=tk.TRUE, side=tk.BOTTOM, fill=tk.BOTH)
        self.select_enc = tk.Button(self.botframe, text="Encrypt", relief=tk.SUNKEN, bg="#777777",
                                    activebackground="#898989", bd=1, command=self.encrypt)
        self.select_dec = tk.Button(self.botframe, text="Decrypt", relief=tk.SUNKEN, bg="#777777",
                                    activebackground="#898989", bd=1, command=self.decrypt)
        self.select_dec.config(highlightthickness=0, highlightbackground="#777777")
        self.select_enc.config(highlightthickness=0, highlightbackground="#777777")

        self.browse.pack(side=tk.TOP)
        self.show_inputfile.pack(fill=tk.Y, side=tk.TOP)
        self.output_prompt.grid(row=1, column=1, padx=15, pady=5, sticky=tk.W+tk.E)
        self.outputfile.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W+tk.E)
        self.middleframe.grid_columnconfigure(2, weight=1)
        self.select_enc.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)
        self.select_dec.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

    def decrypt(self):
        if self.inputfile == "":
            tk.messagebox.showwarning("Error", "No input file")
            return
        try:
            password = tk.simpledialog.askstring("Password", "Enter password", show='*')
            decryptor.decrypt(self.inputfile, RSA.generate_key_from_pwd(password), self.outputfile.get())
        except IOError:
            tk.messagebox.showerror("Error", "Cannot open file")
        except ValueError:
            tk.messagebox.showerror("Error", "Cannot decrypt")
        except decryptor.MetadataError as metadata_error:
            tk.messagebox.showerror("Error", repr(metadata_error))
        except decryptor.SignatureMismatchError as signature_mismatch_error:
            tk.messagebox.showerror("Error", repr(signature_mismatch_error))

    def encrypt(self):
        if self.inputfile == "":
            tk.messagebox.showwarning("Error", "No input file")
            return
        try:
            password = tk.simpledialog.askstring("Password", "Enter password", show='*')
            password = hashlib.sha512(password.encode(encoding='UTF-8')).hexdigest()[0:30]
            confirm_password = tk.simpledialog.askstring("Confirm password", "Confirm password", show='*')
            confirm_password = hashlib.sha512(confirm_password.encode(encoding='UTF-8')).hexdigest()[0:30]
            while password != confirm_password:
                password = tk.simpledialog.askstring("Passwords do not match", "Re-enter password", show='*')
                password = hashlib.sha512(password.encode(encoding='UTF-8')).hexdigest()[0:30]
                confirm_password = tk.simpledialog.askstring("Confirm password", "Confirm password", show='*')
                confirm_password = hashlib.sha512(confirm_password.encode(encoding='UTF-8')).hexdigest()[0:30]
            encryptor.encrypt(self.inputfile, RSA.generate_key_from_pwd(password).generate_public_key(), self.outputfile.get())
        except IOError:
            tk.messagebox.showerror("Error", "Cannot open file")

    def read_filename(self):
        self.inputfile = tk.filedialog.askopenfilename(title='Browse')
        self.show_inputfile.configure(text=self.inputfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="encrypt/decrypt files", formatter_class=argparse.RawTextHelpFormatter)

    ui = parser.add_mutually_exclusive_group()
    ui.add_argument("-c", "--cli", action="store_true", help="run using the command line", default=True)
    ui.add_argument("-g", "--gui", action="store_true", help="run with a graphical user interface\n"
                                                             "\tWhen using this option, discards all other arguments")

    action = parser.add_mutually_exclusive_group()
    action.add_argument("-e", "--encrypt", action="store_true", help="encrypt selected files")
    action.add_argument("-d", "--decrypt", action="store_true", help="decrypt selected files")

    parser.add_argument("-p", "--password", help="password used as encryption key")

    parser.add_argument("-v", "--verbose", action="store_true", help="more verbose output to stdout")

    parser.add_argument("files", nargs='*', help="files")

    arguments = parser.parse_args()

    if arguments.gui:
        root = tk.Tk()
        root.title("Encryptor/Decryptor")
        gui_print = tk.Text(root, state='disabled', bg="#353535", fg="#bbbbbb")
        gui_print.pack(side=tk.BOTTOM, fill=tk.BOTH)
        gui_print.config(highlightthickness=0)

        sys.stdout = Redirector(gui_print)

        window = UI(root)

        root.mainloop()

    elif arguments.cli:
        if arguments.encrypt:
            # getting the password for generating the encryption key
            password = arguments.password
            if password is None:
                password = getpass("Enter password: ")
                password = hashlib.sha512(password.encode(encoding='UTF-8')).hexdigest()
                confirm_password = getpass("Confirm password: ")
                confirm_password = hashlib.sha512(confirm_password.encode(encoding='UTF-8')).hexdigest()
                while password != confirm_password:
                    print("Password mismatch", file=sys.stderr)
                    password = getpass("Enter password: ")
                    password = hashlib.sha512(password.encode(encoding='UTF-8')).hexdigest()
                    confirm_password = getpass("Confirm password: ")
                    confirm_password = hashlib.sha512(confirm_password.encode(encoding='UTF-8')).hexdigest()
            else:
                password = hashlib.sha512(password.encode(encoding='UTF-8')).hexdigest()

            public_key = RSA.generate_key_from_pwd(password).generate_public_key()

            for file in arguments.files:
                if arguments.verbose:
                    print("Encrypting " + file)
                    sys.stdout.flush()
                encryptor.encrypt(file, public_key)

        elif arguments.decrypt:
            # getting the password for generating the private key
            password = arguments.password
            if password is None:
                password = getpass("Enter password: ")
            password = hashlib.sha512(password.encode(encoding='UTF-8')).hexdigest()
            private_key = RSA.generate_key_from_pwd(password)

            for file in arguments.files:
                if arguments.verbose:
                    print("Decrypting " + file)
                    sys.stdout.flush()
                try:
                    decryptor.decrypt(file, private_key)
                except IOError:
                    print(file + " cannot be opened")
                    sys.stdout.flush()
                except decryptor.MetadataError as e:
                    print(e.message)
                    sys.stdout.flush()
                except decryptor.SignatureMismatchError as e:
                    print("Signature mismatch")
                    sys.stdout.flush()
