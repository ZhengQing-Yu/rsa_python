from encryptor import encrypt
from decryptor import decrypt
import os


class document:
    def __init__(self, *filenames):
        if len(filenames) == 0:
            print("Please enter valid input file")
            return
        self.readfile = filenames[0]
        if len(filenames) == 1:
            self.writefile = ""
        elif len(filenames) == 2:
            self.writefile = os.path.split(self.readfile)[0] + '/' + filenames[1]

    def decrypt(self):
        if self.writefile == "":
            readfile = os.path.splitext(self.readfile)
            self.writefile = readfile[0] + '_decrypted' + readfile[1]
        decrypt(self.readfile, self.writefile)

    def encrypt(self):
        if self.writefile == "":
            readfile = os.path.splitext(self.readfile)
            self.writefile = readfile[0] + '_encrypted' + readfile[1]
        encrypt(self.readfile, self.writefile)
