from fractions import gcd
from random import randint

def lcm(a, b):
	return a * b // gcd(a, b)

def lcmm(*args):
    return reduce(lcm, args)

def pollard(n, B):
	k = lcmm(*range(2, B+1))
	it = 0
	while it <= 100:
		a = randint(2, n-2)
		r = pow(a, k, n)
		d = gcd(r-1, n)

		if not (d == 1 or d == n): return d, it

		it += 1

	return -1, it

def factor(n):
	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
	B = 4
	fact, it = pollard(n, B)
	while fact == -1:
		B += 1
		fact, it = pollard(n, B)

		if B >= 200:
			return -1, 0

	return fact, it


def main():
	n = 262063
	d, it = factor(n)
	if d != -1:
		print n/d, d, ' po ', it, ' iteracjach'

	n = 9420457
	d, it = factor(n)
	if d != -1:
		print n/d, d, ' po ', it, ' iteracjach'
	"""
	safe_prime = 2698727*2698679
	print safe_prime
	d, it = factor(safe_prime)
	if d != -1:
		print safe_prime/d, d, ' po ', it, ' iteracjach'

	not_safe_prime = 6283898324617
	print not_safe_prime
	d, it = factor(not_safe_prime)
	if d != -1:
		print not_safe_prime/d, d, ' po ', it, ' iteracjach'
	"""

	a = randint(2**100, 2**200)
	while a % 2 == 0:
		a = randint(2**100, 2**200)
	d, it = factor(a)
	if d != -1:
		print a/d, d, ' po ', it, ' iteracjach'


if __name__ == '__main__':
	main()