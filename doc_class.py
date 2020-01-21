from encryptor import encrypt_file
from decryptor import decrypt
from encryptor import public_key_message
from decryptor import private_key_message
import os


class document:
    def __init__(self, *filenames):
        if len(filenames) == 0:
            print("Please enter valid input file")
            return
        self.readfile = filenames[0]
        if len(filenames) == 1 or filenames[1] == "":
            self.writefile = ""
        elif len(filenames) == 2:
            self.writefile = os.path.split(self.readfile)[0] + '/' + filenames[1]
        else:
            print("document takes 2 arguments")
            print(" 1- path to input file")
            print(" 2- name of output file")

    def decrypt(self):
        if self.writefile == "":
            readfile = os.path.splitext(self.readfile)
            self.writefile = readfile[0] + '_decrypted' + readfile[1]
        try:
            decrypt(self.readfile, self.writefile, private_key_message)
        except IOError:
            raise
        except ValueError:
            raise

    def encrypt(self):
        if self.writefile == "":
            readfile = os.path.splitext(self.readfile)
            self.writefile = readfile[0] + '_encrypted' + readfile[1]
        try:
            encrypt_file(self.readfile, self.writefile, public_key_message)
            return self.writefile
        except IOError:
            raise
