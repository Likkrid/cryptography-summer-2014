from Crypto.Hash import SHA512, MD5
import base64

def sha(number, size=32):
	h = SHA512.new()
	h.update(number)
	return int(h.hexdigest()[:size], 16)


def md5(number, size=32):
	h = MD5.new()
	h.update(number)
	return int(h.hexdigest()[:size], 16)

def concat(*args):
	s = ''
	for i in args:
		s += str(i)
	return s