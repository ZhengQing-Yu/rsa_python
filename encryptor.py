from mod_operation import mod_power
from encode_64bit import encode
import key_object_rsa as RSA
import secrets
import hashlib

# public keys for message
public_key_message = RSA.PublicKey(5023106572088379812853312743905, 933183993936858500456026910116731535065137982451283)

# private keys for signature
n_private = 2
e_private = 1


def enc(unsigned_int, exponent, modulo):
    return pow(unsigned_int, exponent, modulo)


def encrypt_string(string, exponent, modulo):
    binary = ' '.join(format(ord(x), 'b') for x in string)
    binary = '{0} '.format(binary)
    cipher = ''
    cipher_text = ''
    count_splitstring = 0
    for char in binary:
        if char == ' ':
            rnd = secrets.SystemRandom().randint(2, 9)
            cipher += str(rnd)
            count_splitstring += 1
            if count_splitstring == 3 or rnd % 2 == 1:
                cipher_text = cipher_text + ' ' + str(enc(int(cipher), exponent, modulo))
                cipher = ''
                count_splitstring = 0
        elif char == '1':
            cipher = '{0}1'.format(cipher)
        elif char == '0':
            cipher = '{0}0'.format(cipher)
    if cipher != '':
        cipher_text = cipher_text + ' ' + str(enc(int(cipher), exponent, modulo))

    return cipher_text


def encrypt_file(read_from, write_to, public_key):
    try:
        open(read_from, "r", encoding='utf-8')
    except IOError:
        raise

    encrypted_text = open(write_to, "w", encoding='utf-8')

    signature = hashlib.sha256()

    with open(read_from) as f:
        for line in f:
            signature.update(line.encode('utf-8'))

            for element in encrypt_string(line, public_key.exponent, public_key.modulo).split():
                encrypted_text.write(encode(int(element)))
                encrypted_text.write(' ')

    encrypted_text.write('\n')
    # encrypted_text.write(str(enc(int(signature.hexdigest(), base=16), e_private, n_private)))

    encrypted_text.close()


encrypt_file("secret_decrypted.txt", "secret_encrypted.txt", public_key_message)

string = "iuygjg"
string_encode = string.encode('utf-8')
sign = hashlib.sha256()
sign.update(string_encode)
signature = encode(enc(int(sign.hexdigest(), base=16), public_key_message.exponent, public_key_message.modulo))
print(signature)

