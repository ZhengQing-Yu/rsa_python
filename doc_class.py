from encryptor import encrypt
from decryptor import decrypt
import os


class document:
    def __init__(self, *filenames):
        self.readfile = ''
        self.writefile = ''
        if len(filenames) == 0:
            print("Please enter valid input file")
            return
        self.readfile = filenames[0]
        if len(filenames) == 1:
            self.writefile = "asdf"
        elif len(filenames) == 2:
            self.writefile = os.path.split(self.readfile)[0] + '/' + filenames[1]

    def decrypt(self):
        if self.writefile == "asdf":
            readfile = os.path.splitext(self.readfile)
            self.writefile = readfile[0] + '_decrypted' + readfile[1]
        decrypt(self.readfile, self.writefile)

    def encrypt(self):
        if self.writefile == "asdf":
            readfile = os.path.splitext(self.readfile)
            self.writefile = readfile[0] + '_encrypted' + readfile[1]
        encrypt(self.readfile, self.writefile)


def test(*filenames):
    readfile = filenames[0]
    if len(filenames) == 1:
        print("The directory is:", os.path.split(readfile)[0])
        print("The filename is:", os.path.split(readfile)[1])
        readfile = os.path.splitext(readfile)
        print(readfile[0] + '_decrypted' + readfile[1])
    elif len(filenames) == 2:
        print(os.path.split(readfile)[0] + '/' + filenames[1])
    print("\n")


