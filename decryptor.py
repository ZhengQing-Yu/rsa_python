from mod_operation import mod_inverse
from encode_64bit import decode
import key_object_rsa as RSA
import os
import json
import hashlib


a = 39875437854365412987387127
b = 23402476415307801465949829
# n = ab
n = 933183993936858500456026910116731535065137982451283
# phi = phi(n) = (a-1)(b-1) for a, b prime
phi = 933183993936858500456026846838817265391923529114328
# e coprime with phi
e = 5023106572088379812853312743905
d = mod_inverse(e, phi)

private_key_message = RSA.PrivateKey(39875437854365412987387127, 23402476415307801465949829,
                                     5023106572088379812853312743905)


class MetadataError(Exception):
    def __init__(self, message):
        self.message = message


class SignatureMismatchError(Exception):
    def __init__(self, message):
        self.message = message


def decrypt_plaintext(read_file, write_file, private_key):
    decrypted_bin = []

    def dec(unsigned_int, exponent, modulo):
        dec_str = str(pow(unsigned_int, exponent, modulo))
        for bad_str in [(lambda x: str(x))(x) for x in range(2, 10)]:
            dec_str = dec_str.replace(bad_str, ' ')
        for dec_int in dec_str.split():
            decrypted_bin.append(dec_int)

    try:
        f = open(read_file, "r", encoding='ASCII')
        f.close()
    except IOError:
        raise

    decrypted_file = open(write_file, "w")

    with open(read_file, encoding='ASCII') as f:
        for line in f:
            for enc_str in line.split():
                dec(decode(enc_str), private_key.exponent, private_key.modulo)
                for string in decrypted_bin:
                    string = str(string)
                    decrypted = ''.join([chr(int(bc, 2)) for bc in string.split(' ')])
                    decrypted_file.write(decrypted)
                decrypted_bin.clear()

    decrypted_file.close()


def decrypt(read_file, private_key, write_file=None):
    def split_string_into_byte(string):
        return [int(string[i:i + 3]) for i in range(0, len(string), 3)]

    try:
        metadata_file = os.path.splitext(read_file)[0] + '.mdata'
        decrypt_plaintext(metadata_file, '_decrypted_metadata', private_key)
        decrypted_metadata = open('_decrypted_metadata', 'r', encoding='utf-8')
        metadata = json.load(decrypted_metadata)
        decrypted_metadata.close()
        os.remove('_decrypted_metadata')
    except IOError:
        raise MetadataError("Metadata file cannot be bound for " + read_file)
    except json.JSONDecodeError:
        raise MetadataError("Metadata file cannot be read for " + read_file)

    if write_file is None:
        try:
            write_file = metadata["filename"] + metadata["extension"]
        except KeyError:
            raise MetadataError("Metadata file has been tampered with. Cannot get original filename: " + read_file)

    try:
        try_open_file = open(read_file, "r", encoding='ASCII')
        try_open_file.close()
    except IOError:
        raise

    try:
        block_size = metadata["block_size"]
    except KeyError:
        raise MetadataError("Metadata file has been tampered with. Block size not found for " + read_file)
    try:
        last_block_size = metadata["last_block_size"]
    except KeyError:
        raise MetadataError("Metadata file has been tampered with. SIze of last block not found for " + read_file)
    try:
        original_signature = metadata["signature"]
    except KeyError:
        raise MetadataError("Metadata file has been tampered with. Signature not found for " + read_file)

    with open(write_file, "wb") as decrypted_file:
        if last_block_size == 0:
            return

        signature = hashlib.sha512()

        with open(read_file, encoding='ASCII') as f:
            current_line = f.readline()
            next_line = f.readline()
            while next_line:
                for enc_str in current_line.split():
                    encrypted = decode(enc_str)
                    decrypted = str(pow(encrypted, private_key.exponent, private_key.modulo))
                    decrypted = decrypted.zfill(block_size)
                    binary_output = bytes(split_string_into_byte(decrypted))
                    signature.update(binary_output)
                    decrypted_file.write(binary_output)
                    current_line = next_line
                    next_line = f.readline()

            encrypted = decode(current_line)
            decrypted = str(pow(encrypted, private_key.exponent, private_key.modulo))
            decrypted = decrypted.zfill(last_block_size)
            if last_block_size == 0:
                decrypted = ''
            binary_output = bytes(split_string_into_byte(decrypted))
            signature.update(binary_output)
            decrypted_file.write(binary_output)

    # verify signatures
    if original_signature != signature.hexdigest():
        raise SignatureMismatchError(read_file)
