import unittest
import encryptor
import decryptor
import filecmp
import os
import sys
from time import sleep


TEST_LOCATION = "/home/zheng/PycharmProjects/rsa/testcases"


class TestFiles(unittest.TestCase):
	def setUp(self) -> None:
		self.current_location = os.getcwd()
		os.chdir(TEST_LOCATION)

	def tearDown(self) -> None:
		os.remove("_encrypted")
		os.remove("_decrypted")
		os.remove("_encrypted.mdata")
		os.chdir(self.current_location)

	def test(self):
		for testfile in os.listdir("./"):
			print("Running test on: {filename}".format(filename=testfile), file=sys.stderr)
			encryptor.encrypt(testfile, encryptor.public_key_message, "_encrypted")
			decryptor.decrypt("_encrypted", decryptor.private_key_message, "_decrypted")
			self.assertTrue(
				filecmp.cmp(testfile, "_decrypted"),
				"Decrypted file is different from original: {filename}".format(filename=testfile)
			)


if __name__ == '__main__':
	unittest.main()
