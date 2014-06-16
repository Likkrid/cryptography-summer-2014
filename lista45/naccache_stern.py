#Naccache-Stern
import random
from primality_test import miller_rabin, power_mod
from prime_generation import generate


primes_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

class PrivateKey(object):
	def __init__(self, p, q, prime_factors):
		self.p = p
		self.q = q
		self.prime_factors = prime_factors

class PublicKey(object):
	def __init__(self, n, g, sigma):
		self.n = n
		self.g = g
		self.sigma = sigma

def product(list):
	return reduce(lambda x, y: x * y, list, 1)

def generate_key(k=16):
	primes = random.sample(primes_list, k)
	u = product(primes[:k/2])
	v = product(primes[k/2:])
	sigma = u*v

	p = 1
	q = 1
	while True:
		a = generate(size=60, probability=0.8)
		b = generate(size=60, probability=0.8)

		print "Choosing ", a, " ", b
		#print a, b

		p = 2*a*u + 1
		q = 2*b*v + 1

		#p = 91171489299480956696641658942979185687
		#q = 21911692912613506361967764935240614120239

		if miller_rabin(p) and miller_rabin(q):
			break

	#setting n = pq
	n = p*q

	#selecting g
	#while True:
	g = 0
	while g == 0 or power_mod(g, (p-1)*(q-1)/4, n) != 1:
		g = random.randint(2, n-1)
		print 'Random choosing g: ', g
		
		
		phi = (p-1)*(q-1)
		for p_i in primes:
			if power_mod(g, phi/p_i, n) == 1:
				g = 0
				break
		

	print primes[:k/2]
	print primes[k/2:]
	print 'u ', u
	print 'v ', v
	print 'p ', p
	print 'q ', q
	print 'n ', n
	print 'g ', g

	privKey = PrivateKey(p, q, primes)
	pubKey = PublicKey(n, g, sigma)

	return pubKey, privKey

def encryption(m, pubKey):
	return power_mod(pubKey.g, m, pubKey.n)

def decryption(c, privKey, pubKey):
	phi = (privKey.p - 1)*(privKey.q - 1)
	n = privKey.p*privKey.q
	ms = []
	ps = []
	for p_i in privKey.prime_factors:
		c_i = power_mod(c, phi/p_i, n)
		for j in range(1, p_i):
			if c_i == power_mod(pubKey.g, j*phi/p_i, n):
				m_i = j
				ms.append(m_i)
				ps.append(p_i)

	print ms, ps
	message = chinese(ms, ps)

	return message


def chinese(a, n):
	N = reduce(lambda x,y: x*y, n, 1)
	return sum(map(lambda (ai, ni): ai*N*modinv(N/ni,ni)/ni, zip(a,n))) % N

def modinv(a, m):
	g, x, y = egcd(a, m)
	return x%m

def egcd(a, b):
    save_a, save_b = a, b
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        q = a / b
        a, b = b, a % b
        x, last_x = last_x - q*x, x
        y, last_y = last_y - q*y, y
    return save_a*last_x + save_b*last_y, last_x, last_y

def main():
	pubKey, privKey = generate_key()
	c = encryption(123, pubKey)
	m = decryption(c, privKey, pubKey)

	c1 = encryption(123+123, pubKey)
	print 'E(m+m) ', c1

	print 'E(m)*E(m) ', c*c % pubKey.n

	print 'E(17m) ', encryption(17*123, pubKey)

	print 'E(m)^17', power_mod(c, 17, pubKey.n)
if __name__ == '__main__':
	main()