from mod_operation import mod_power
from mod_operation import mod_inverse


a = 3101010101010109
b = 20000000014659029
# n = ab
n = 62020202065659977000000117124161
# phi = phi(n) = (a-1)(b-1) for a, b prime
phi = 62020202065659953898990001455024
encipher = 5023106572088379812853312743905
decipher = mod_inverse(encipher, phi)


def decrypt(read_file, write_file):
    decrypted_bin = []

    def dec(enc_int):
        dec_str = str(mod_power(enc_int, decipher, n))
        for bad_str in [(lambda x: str(x))(x) for x in range(2, 10)]:
            dec_str = dec_str.replace(bad_str, ' ')
        for dec_int in dec_str.split():
            decrypted_bin.append(dec_int)

    try:
        encrypted_file = open(read_file, "r")
    except IOError:
        print("Can't read input file")
        return

    decrypted_file = open(write_file, "w")

    with open(read_file) as f:
        for line in f:
            for enc_str in line.split():
                dec(int(enc_str))
                for string in decrypted_bin:
                    string = str(string)
                    decrypted = ''.join([chr(int(bc, 2)) for bc in string.split(' ')])
                    # print(decrypted, end='', flush=True)
                    decrypted_file.write(decrypted)
                decrypted_bin.clear()

    secret = encrypted_file.read()
    encrypted_file.close()

    """"
    for enc_str in secret.split():
        dec(int(enc_str))
        
    decrypted_file = open(write_file, "w")

    for string in decrypted_bin:
        string = str(string)
        decrypted = ''.join([chr(int(bc, 2)) for bc in string.split(' ')])
        # print(decrypted, end='', flush=True)
        decrypted_file.write(decrypted)
    decrypted_file.close()
    """
    decrypted_file.close()


def test(read_file):
    try:
        encrypted_file = open(read_file, "r")
    except IOError:
        print("Can't read input file")
        return

    with open(read_file) as encrypted_file:
        for line in encrypted_file:
            print(line)


#test("ob.txt")
decrypt("secret.txt", "secret_decrypted.txt")
