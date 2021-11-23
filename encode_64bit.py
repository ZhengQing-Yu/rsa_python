import string
import random


alphabet_b64 = string.digits + string.ascii_letters + '!@'


def encode(unsigned_int):
	remainder = unsigned_int & 63
	quotient = unsigned_int >> 6
	encoded_string = alphabet_b64[remainder]
	while quotient:
		remainder = quotient & 63
		quotient = quotient >> 6
		encoded_string = alphabet_b64[remainder] + encoded_string

	return encoded_string


def decode(string_b64):
	n = 0
	for digit in string_b64:
		n = n * 64 + alphabet_b64.index(digit)
	return n


if __name__ == '__main__':
	for x in (random.randint(10000000000000000000000000000000, 100000000000000000000000000000000000) for x in range(999999)):
		assert decode(encode(x)) == x
