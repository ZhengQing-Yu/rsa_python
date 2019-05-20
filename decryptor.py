from mod_operation import mod_power
from mod_operation import mod_inverse


a = 39875437854365412987387127
b = 23402476415307801465949829
# n = ab
n = 933183993936858500456026910116731535065137982451283
# phi = phi(n) = (a-1)(b-1) for a, b prime
phi = 933183993936858500456026846838817265391923529114328
# e coprime with phi
e = 5023106572088379812853312743905
d = mod_inverse(e, phi)


def decrypt(read_file, write_file):
    decrypted_bin = []

    def dec(enc_int):
        dec_str = str(mod_power(enc_int, d, n))
        for bad_str in [(lambda x: str(x))(x) for x in range(2, 10)]:
            dec_str = dec_str.replace(bad_str, ' ')
        for dec_int in dec_str.split():
            decrypted_bin.append(dec_int)

    try:
        open(read_file, "r")
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

    decrypted_file.close()

    print("decryption successful")
