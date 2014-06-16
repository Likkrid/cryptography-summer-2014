# -*- coding: utf-8 -*-
import random
import math

def gcd(a, b):
   if abs(a) < abs(b):
      return gcd(b, a)

   while abs(b) > 0:
      _,r = divmod(a,b)
      a,b = b,r

   return a


def extendedEuclideanAlgorithm(a, b):
   if abs(b) > abs(a):
      (x, y, d) = extendedEuclideanAlgorithm(b, a)
      return (y, x, d)

   if abs(b) == 0:
      return (1, 0, a)

   x1, x2, y1, y2 = 0, 1, 1, 0
   while abs(b) > 0:
      q, r = divmod(a,b)
      x = x2 - q*x1
      y = y2 - q*y1
      a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y

   return (x2, y2, a)


class Point(object):
	def __init__(self, curve, x, y):
		self.curve = curve
		self.x = x
		self.y = y

		#Relaksacja wymagań dla przynależności punktów do krzywej
		#if not curve.contains(x, y):
			#raise Exception("%s does not contains (%s, %s)" % (self.curve, self.x, self.y))

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __neg__(self):
		return Point(self.curve, self.x, -self.y)

	def __repr__(self):
		return "(%r, %r)" % (self.x, self.y)

	def __add__(self, Q):
		if isinstance(Q, O):
			return self, 1

		x_1 = self.x
		y_1 = self.y

		x_2 = Q.x
		y_2 = Q.y

		n = self.curve.N

		x_1 %= n
		y_1 %= n
		x_2 %= n
		y_2 %= n
		
		if x_1 != x_2:
			#Wyliczamy slope: (y_1 - y_2)/(x_1 - x_2) -> extendedEuclid
			u, v, d = extendedEuclideanAlgorithm(x_1 - x_2, n)
			s = ((y_1 - y_2) * u) % n
			x_3 = (s * s - x_1 - x_2) % n
			y_3 = (-y_1 - s*(x_3 - x_1)) % n
		else:
			#jesli x_1 == x_2 mamy dwie opcje:
			#pierwsza: y_1 przystaje do -y_2 modulo n
			if (y_1 + y_2) % n == 0:
				return O(self.curve), 1

			#druga: R = P + P = 2P
			else:
				u, v, d = extendedEuclideanAlgorithm(2 * y_1, n)
				s = ((3 * x_1 * x_1 + self.curve.a) * u) % n
				x_3 = (s * s - 2*x_1) % n
				y_3 = (-y_1 - s*(x_3 - x_1)) % n

		return Point(self.curve, x_3, y_3), d


	def __sub__(self, Q):
		return self + (-Q)

	def __mul__(self, n):
		if not (isinstance(n, int) or isinstance(n, long)):
			print n.__class__.__name__
			raise Exception("Nie skalujemy punktów nie-intami")

		R = O(self.curve)
		d = 1
		while n != 0:
			if n % 2 != 0:
				R, d = self.__add__(R)
			if d != 1:
				#jesli w d dostaniemy cos != 1 to znaczy, ze mamy factor
				return R, d 
			self, d = self.__add__(self)
			if d != 1:
				return R, d
			n /= 2
		return R, d
 
	def __rmul__(self, n):
		return self * n


#Point at Infinity
class O(Point):
	def __init__(self, curve):
		self.curve = curve

	def __neg__(self):
		return self

	def __add__(self, Q):
		return Q, 1

	def __sub__(self, Q):
		return -Q

	def __mul__(self, n):
		if not isinstance(n, int):
			raise Exception("Nie skalujemy punktów nie-intami")
		else:
			return self, 1

	def __repr__(self):
		return "Infinity"


class EllipticCurve(object):
	#y^2 = x^3 + ax + b
	def __init__(self, a, b, N):
		self.a = a
		self.b = b
		self.N = N

		self.det = 4*(a*a*a) + 27*b*b
		if not self.is_nonsingular():
			raise ValueError("%s nie jest non-singular" % self)

	def is_nonsingular(self):
		return self.det != 0

	def contains(self, x, y):
		return y*y == x**3 + self.a * x + self.b

	def __str__(self):
		return 'y^2 = x^3 + %sx + %s' % (self.a, self.b)

	def __eq__(self):
		return (self.a, self.b) == (other.a, other.b)


def randomCurve(N):
	a, x, y = random.randint(1, N), random.randint(1, N), random.randint(1, N)
	b = (y * y - x * x * x - a * x) % N

	E = EllipticCurve(a, b, N)
	P = Point(E, x, y)

	return E, P

def factor(N, bsmooth, iter=5):
	for i in xrange(iter):
		E, P = randomCurve(N);
		Q, d = bsmooth * P
		if d != 1 : return d
	return N

if __name__=="__main__":
	N = 150010090798541562798048275641
	bsmooth = int(math.factorial(2000))
	counter = 0
	while N != 1:

		k = factor(N, bsmooth)
		k = abs(k)
		if k != 1 and k != N:
			counter = 0
			print k,
		elif k == 1:
			counter += 1

		N /= k
		if counter >= 30: 
			print N,
			break