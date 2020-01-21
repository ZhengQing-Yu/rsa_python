import secrets
from math import gcd
from mod_operation import mod_inverse
import rabin_miller as prime


KEY_SIZE = 2**128


class PublicKey:
	def __init__(self, exponent, modulo):
		self.exponent = exponent
		self.modulo = modulo


class PrivateKey:
	def __init__(self, prime1=None, prime2=None, encryptor=None):
		if prime1 is None:
			self.prime1 = prime.generate_random(KEY_SIZE, KEY_SIZE >> 1)
		else:
			self.prime1 = prime1
		if prime2 is None:
			self.prime2 = prime.generate_random(KEY_SIZE, KEY_SIZE >> 1)
		else:
			self.prime2 = prime2
		e = phi = (prime1 - 1) * (prime2 - 1)
		lower_bound = phi >> 1
		upper_bound = phi
		while gcd(phi, e) != 1:
			e = secrets.SystemRandom().randint(lower_bound, upper_bound)
		self.encryptor = e
		if encryptor is not None:
			self.encryptor = encryptor
		self.decryptor = pow(self.encryptor, -1, phi)
		self.modulo = self.prime1 * self.prime2

	def generate_public_key(self):
		return PublicKey(self.encryptor, self.modulo)
