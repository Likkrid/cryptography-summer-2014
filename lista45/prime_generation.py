#prime generator
#according to http://csrc.nist.gov/publications/fips/fips186-3/fips_186-3.pdf
from primality_test import miller_rabin, fermat, solovay_strassen, power_mod
from random import randint

def fermat_2(n):
	"""
	return: False - composite
			True - possibly prime
	"""
	if n < 2: return False
	if n == 2: return True
	if not n & 1: return False

	a = 2
	if power_mod(a, n-1, n) != 1:
		return False

	return True

def initial_is_prime(n):
	if n < 2: return False
	
	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
	if n in primes:
		return True

	for prime in primes:
		if n % prime == 0:
			return False

	if not fermat_2(n):
		return False

	return True

def generate(size=1024, test=miller_rabin, probability=0.99):
	while True:
		result = randint(2**(size-1), 2**(size))
		if initial_is_prime(result):
			if test(result, probability):
				return result

def main():
	print generate(size=512, test=fermat, probability=0.8)
	print generate(size=1024, test=solovay_strassen, probability=0.85)
	print generate(size=2048, test=miller_rabin, probability=0.9)

if __name__ == '__main__':
	main()
