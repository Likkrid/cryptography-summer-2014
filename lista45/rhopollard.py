def f(x):
	return x**2 + 1

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def rhopollard(n):
	x, y, d = 2, 2, 1
	steps = 0
	while d == 1:
		steps += 1
		x = f(x) % n
		y = f(y) % n
		y = f(y) % n
		d = gcd(abs(x-y), n)
		print x, y, d
	if d == n: return -1, steps
	return d, steps


def main():
	numbers = [262063, 420457,181937053]
	for n in numbers:
		d, steps = rhopollard(n)
		print 'factors: ', d, n/d, ' in ', steps, ' steps'

if __name__ == '__main__':
	main()