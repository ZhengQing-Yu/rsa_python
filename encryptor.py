from mod_operation import mod_power
from random import randint

# public keys
n = 933183993936858500456026910116731535065137982451283
e = 5023106572088379812853312743905


def encrypt(read_file, write_file):
    def enc(number):
        return mod_power(number, e, n)

    cipher_text = []

    try:
        open(read_file, "r")
    except IOError:
        print("Can't read input file")
        return

    encrypted_text = open(write_file, "w")

    with open(read_file) as f:
        count_newline = 0
        for line in f:
            binary = ' '.join(format(ord(x), 'b') for x in line)
            binary = '{0} '.format(binary)
            cipher = ''
            count_splitstring = 0
            for char in binary:
                if char == ' ':
                    rnd = randint(2, 9)
                    cipher += str(rnd)
                    count_splitstring += 1
                    if count_splitstring == 3 or rnd % 2 == 1:
                        cipher_text.append(enc(int(cipher)))
                        cipher = ''
                        count_splitstring = 0
                elif char == '1':
                    cipher = '{0}1'.format(cipher)
                elif char == '0':
                    cipher = '{0}0'.format(cipher)
            if cipher != '':
                cipher_text.append(enc(int(cipher)))
            for element in cipher_text:
                encrypted_text.write(str(element))
                if count_newline % 3 == 2:
                    encrypted_text.write('\n')
                else:
                    encrypted_text.write(' ')
                count_newline = (count_newline + 1) % 3
            cipher_text.clear()

    encrypted_text.close()

    print("Encryption successful")
