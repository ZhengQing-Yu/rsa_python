from mod_operation import mod_power
from random import randint
# 108bit rsa encryption

# public keys
n = 62020202065659977000000117124161
encipher = 5023106572088379812853312743905


def encrypt(read_file, write_file):
    def enc(number):
        return mod_power(number, encipher, n)

    cipher_text = []

    try:
        target = open(read_file, "r")
    except IOError:
        print("Can't read input file")
        return

    encrypted_text = open(write_file, "w")

    with open(read_file) as f:
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
            for count, element in enumerate(cipher_text, 1):
                encrypted_text.write(str(element))
                if count % 3 == 0:
                    encrypted_text.write('\n')
                else:
                    encrypted_text.write(' ')
            cipher_text.clear()

    """
    text = target.read()
    target.close()

    binary = ' '.join(format(ord(x), 'b') for x in text)
    binary = '{0} '.format(binary)
    cipher = ''
    count = 0
    for char in binary:
        if char == ' ':
            rnd = randint(2, 9)
            cipher += str(rnd)
            count += 1
            if count == 3 or rnd % 2 == 1:
                cipher_text.append(enc(int(cipher)))
                cipher = ''
                count = 0
        elif char == '1':
            cipher = '{0}1'.format(cipher)
        elif char == '0':
            cipher = '{0}0'.format(cipher)
    if cipher != '':
        cipher_text.append(enc(int(cipher)))

    for count, element in enumerate(cipher_text, 1):
        encrypted_text.write(str(element))
        if count % 3 == 0:
            encrypted_text.write('\n')
        else:
            encrypted_text.write(' ')

    encrypted_text.close()
    """


encrypt("secret_decrypted.txt", "secret.txt")
