import secrets
from math import gcd
from mod_operation import mod_inverse
import rabin_miller as prime
import hashlib
import timeit


KEY_SIZE = 2 ** 2048


class PublicKey:
	def __init__(self, exponent, modulo):
		self.exponent = exponent
		self.modulo = modulo


class PrivateKey:
	def __init__(self, prime1=None, prime2=None, encryptor=None):
		if prime1 is None:
			prime1 = prime.generate_random(KEY_SIZE, KEY_SIZE >> 1)

		if prime2 is None:
			prime2 = prime.generate_random(KEY_SIZE, KEY_SIZE >> 1)

		phi = (prime1 - 1) * (prime2 - 1)

		if encryptor is None:
			e = phi
			lower_bound = phi >> 1
			upper_bound = phi
			while gcd(phi, e) != 1:
				e = secrets.SystemRandom().randint(lower_bound, upper_bound)
			self.encryptor = e
		else:
			self.encryptor = encryptor

		self.exponent = mod_inverse(self.encryptor, phi)
		self.modulo = prime1 * prime2

	def generate_public_key(self):
		return PublicKey(self.encryptor, self.modulo)


def generate_key_from_pwd(password='Password1', loud=False):
	def gen_prime(x):
		x = (int(x, base=16) ** 2) // 4 * 2 + 1
		while x < 4149515568880992958512407863691161151012446232242436899995657329690652811412908146399707048947103794288197886611300789182395151075411775307886874834113963687061181803401509523685376:
			x = (int(hashlib.sha512(str(x).encode(encoding='UTF-8')).hexdigest(), base=16) ** 2) // 4 * 2 + 1
		while not prime.is_prime(x):
			x += 2
		return x
	prime1 = hashlib.sha512(password.encode(encoding='UTF-8')).hexdigest()
	prime2 = hashlib.sha512(str(prime1).encode(encoding='UTF-8')).hexdigest()
	prime1 = gen_prime(prime1)
	prime2 = gen_prime(prime2)
	if loud:
		print(len(str(prime1)), prime1)
		print(len(str(prime2)), prime2)

	phi = (prime1 - 1) * (prime2 - 1)
	e = phi >> 1
	while gcd(phi, e) != 1:
		e += 1

	return PrivateKey(prime1, prime2, e)


if __name__ == "__main__":
	print(timeit.timeit(generate_key_from_pwd, number=10))

