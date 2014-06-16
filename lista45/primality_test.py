from random import randint
from math import log

def power_mod(a, b, c):
	"""
	return: a^b mod c
	"""
	result = 1

	while b > 0:
		if b & 1:
			result = result * a
			result = result % c
		b = b >> 1
		a = a * a
		a = a % c

	return result

def fermat(n, probability=0.999):
	"""
	return: False - composite
			True - possibly prime
	"""
	assert(probability > 0 and probability < 1)

	if n < 2: return False
	if n == 2: return True
	if not n & 1: return False

	#print "1 - prob", 1-probability
	#print "# of trials", log(2, 1/(1-probability))
	#1/2 of witnesses are the good ones for non charmichaels...
	trials = int(-1*log( 1-probability, 2))
	print "# of trials: ", trials

	for i in range(trials):
		a = randint(2, n-1)
		if power_mod(a, n-1, n) != 1:
			return False

	return True

def decompose(n):
	"""
	return: (s, d)
	n = 2^s*d, where s is max
	"""
	s = 0
	while n % 2 == 0:
		s += 1
		n = n >> 1

	return s, n


def miller_rabin(n, probability=0.99):
	"""
	return: False - composite
			True - possibly prime
	"""
	assert(probability > 0 and probability < 1)

	if n < 2: return False
	if n == 2: return True
	if n % 2 == 0: return False

	#3/4 of witnesses are the good ones
	#print 1-probability
	#print "ilosc prob ", -log(4, 1.0-probability)
	trials = int(-log(1.0-probability, 4))
	#print "# of trials: ", trials

	s, d = decompose(n-1)
	assert(2**s*d == n-1)

	def try_composite(a):
		if power_mod(a, d, n) == 1:
			return False
		for r in range(s):
			if power_mod(a, d*2**r, n) == n - 1:
				return False
		return True

	if n < 475912314:
		return try_composite(2) or try_composite(17) or try_composite(61)

	if n < 341550071728321:
		A = [2, 3, 5, 7, 11, 13, 17]
		for a in A:
			if try_composite(a):
				return False

	for i in range(trials):
		a = randint(2, n-1)
		if try_composite(a):
			return False

	return True

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a


def jacobi(n, m):
    j = 1
 
    # rule 5
    n %= m
     
    while n:
        # rules 3 and 4
        t = 0
        while not n & 1:
            n /= 2
            t += 1
        if t & 1 and m % 8 in (3, 5):
            j = -j
 
        # rule 6
        if (n % 4 == m % 4 == 3):
            j = -j
 
        # rules 5 and 6
        n, m = m % n, n
 
    return j if m == 1 else 0


def solovay_strassen(n, probability=0.99):
	"""
	return: False - composite
			True - possibly prime
	"""
	assert(probability > 0 and probability < 1)

	if n < 2: return False
	if n == 2: return True
	if n % 2 == 0: return False

	#1/2 of witnesses are the good ones
	trials = int(-1*log(1-probability, 2))
	print "# of trials: ", trials

	for i in range(trials):
		a = randint(2, n-1)
		x = jacobi(a, n) % n
		if x == 0 or power_mod(a, (n-1)/2, n) != x:
			return False
		return True

def main():
	n = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000363615248995857033337070056421798084773928388404595478521275273323360314397140589053381064057676513405578269039657156654036652542534142153403813548019823067738139625064720279852053988015105159267671307376648098427305565548385579726693276910982152975578128195916170093939122526967786064150952048804043790984587576840497230860850442672367274264225126912681162393576808737503496204813545588228045007440964810028318157744742042164729179624735150857434459483953309429721400891961700680913357885554627008446097767344491265016105796794863212821920146792100243708856432511247267178527864170389794381289559776551453754231065288334690404642281796546160439820713674513539942680570165962426756831936897722911879111586768587821403760434759134443927568798788746120384016688199078106542047410157447996575683249525837908454550881


	print "is n prime?"
	print "Fermat: ", fermat(n)
	print "miller_rabin: ", miller_rabin(n)
	print "solovay_strassen: ", solovay_strassen(n)

if __name__ == '__main__':
	main()