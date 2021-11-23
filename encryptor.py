import key_object_rsa as RSA
import secrets
import hashlib
import os
import json
import encode_64bit

# public keys for message
public_key_message = RSA.PublicKey(5023106572088379812853312743905, 933183993936858500456026910116731535065137982451283)


def enc(unsigned_int, exponent, modulo):
    return pow(unsigned_int, exponent, modulo)


def encrypt_plain_text(read_from, write_to, public_key):
    def encrypt_string(string, exponent, modulo):
        binary = ' '.join(format(ord(x), 'b') for x in string)
        binary = '{0} '.format(binary)
        cipher, cipher_text = '', ''
        split = 0
        for char in binary:
            if char == ' ':
                rnd = secrets.SystemRandom().randint(2, 9)
                cipher += str(rnd)
                split += 1
                if split == 3:
                    cipher_text = cipher_text + ' ' + str(enc(int(cipher), exponent, modulo))
                    cipher = ''
                    split = 0
            elif char == '1':
                cipher = '{0}1'.format(cipher)
            elif char == '0':
                cipher = '{0}0'.format(cipher)
        if cipher != '':
            cipher_text = cipher_text + ' ' + str(enc(int(cipher), exponent, modulo))

        return cipher_text

    encrypted_text = open(write_to, "w", encoding='ASCII')
    with open(read_from, encoding='utf-8') as f:
        for line in f:
            for element in encrypt_string(line, public_key.exponent, public_key.modulo).split():
                encrypted_text.write(encode_64bit.encode(int(element)))
                encrypted_text.write(' ')

    encrypted_text.close()


def encrypt(read_from, public_key, write_to=None):
    filename, extension = os.path.splitext(read_from)

    if write_to is None:
        write_to = encode_64bit.encode(int(hashlib.sha256(read_from.encode(encoding='UTF-8')).hexdigest(), base=16))
        while os.path.exists(write_to + '.msg'):
            write_to = encode_64bit.encode(int(hashlib.sha256(write_to.encode(encoding='UTF-8')).hexdigest(), base=16))

    metadata = {
        "filename": filename,
        "extension": extension
    }

    try:
        try_open_file = open(read_from, "rb")
        try_open_file.close()
    except IOError:
        raise

    signature = hashlib.sha512()

    block_size = (len(str(public_key.modulo)) - 1) // 3

    metadata["block_size"] = block_size * 3

    with open(write_to, "w", encoding='ASCII') as encrypted_text:
        with open(read_from, "rb") as f:
            current_block = f.read(block_size)
            next_block = f.read(block_size)
            while next_block:
                signature.update(current_block)
                cipher_text = ''
                for single_byte in current_block:
                    cipher_text = cipher_text + str(single_byte).zfill(3)
                encrypted_text.write(encode_64bit.encode(enc(int(cipher_text), public_key.exponent, public_key.modulo)))
                encrypted_text.write('\n')

                current_block = next_block
                next_block = f.read(block_size)

            signature.update(current_block)
            cipher_text = ''
            last_block_size = 0
            for single_byte in current_block:
                last_block_size += 1
                cipher_text = cipher_text + str(single_byte).zfill(3)
            metadata["last_block_size"] = last_block_size * 3
            if last_block_size == 0:
                cipher_text = str(secrets.SystemRandom().randint(0, block_size))
            encrypted_text.write(encode_64bit.encode(enc(int(cipher_text), public_key.exponent, public_key.modulo)))

        metadata["signature"] = signature.hexdigest()

    with open('_plaintext_metadata', "w", encoding='utf-8') as metadata_file:
        json.dump(metadata, metadata_file, ensure_ascii=False)
    encrypt_plain_text('_plaintext_metadata', os.path.splitext(write_to)[0] + '.mdata', public_key)
    os.remove('_plaintext_metadata')

