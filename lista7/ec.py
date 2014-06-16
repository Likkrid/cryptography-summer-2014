from finite_fields.finitefield import FiniteField
import random

class Point(object):
	def __init__(self, curve, x, y):
		self.curve = curve
		self.x = x
		self.y = y

		if not curve.contains(x, y):
			raise Exception("%s does not contains (%s, %s)" % (self.curve, self.x, self.y))

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __neg__(self):
		return Point(self.curve, self.x, -self.y)

	def __repr__(self):
		return "(%r, %r)" % (self.x, self.y)

	def __add__(self, Q):
		if isinstance(Q, O):
			return self

		if (self.x, self.y) == (Q.x, Q.y):
			if self.y == 0:
				return O(self.curve)

			# slope of the tangent line
			m = (3 * self.x * self.x + self.curve.a) / (2 * self.y)
		else:
			if self.x == Q.x:
				return O(self.curve)

			# slope of the secant line
			m = (Q.y - self.y) / (Q.x - self.x)

		x_3 = m*m - Q.x - self.x
		y_3 = m*(x_3 - self.x) + self.y

		return Point(self.curve, x_3, -y_3)


	def __sub__(self, Q):
		return self + (-Q)

	def __mul__(self, n):
		if not (isinstance(n, int) or isinstance(n, long)):
			print n.__class__.__name__
			raise Exception("We don't scale a point by a non-int")
		else:
			if n < 0:
				return -self * -n
			if n == 0:
				return O(self.curve)
			else:
				Q = self
				R = self if n & 1 == 1 else O(self.curve)
 
				i = 2
				while i <= n:
					Q = Q + Q
 
					if n & i == i:
						R = Q + R
 
					i = i << 1
		return R
 
	def __rmul__(self, n):
		return self * n


#Point at Infinity
class O(Point):
	def __init__(self, curve):
		self.curve = curve

	def __neg__(self):
		return self

	def __add__(self, Q):
		return Q

	def __sub__(self, Q):
		return -Q

	def __mul__(self, n):
		if not isinstance(n, int):
			raise Exception("We don't scale a point by a non-int")
		else:
			return self

	def __repr__(self):
		return "Infinity"


class EllipticCurve(object):
	#y^2 = x^3 + ax + b
	def __init__(self, a, b):
		self.a = a
		self.b = b

		self.det = 4*(a*a*a) + 27*b*b
		if not self.is_nonsingular():
			raise ValueError("%s is not nonsingular" % self)

	def is_nonsingular(self):
		return self.det != 0

	def contains(self, x, y):
		return y*y == x**3 + self.a * x + self.b

	def __str__(self):
		return 'y^2 = x^3 + %sx + %s' % (self.a, self.b)

	def __eq__(self):
		return (self.a, self.b) == (other.a, other.b)


class PublicKey(object):
	def __init__(self, curve, P, Q, order):
		self.curve = curve
		self.P = P
		self.Q = Q
		self.order = order

		

class SecretKey(object):
	def __init__(self, order):
		self.a = random.randint(2, order)



if __name__ == '__main__':
	

	p = int("fffffffffffffffffffffffffffffffeffffffffffffffff", 16)
	print "p = ", p

	a = p - 3
	print "a = ", a

	b = int("64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1", 16)
	print "b = ", b

	x_G = int("188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012", 16)
	print "x_G = ", x_G

	y_G = int("07192b95ffc8da78631011ed6b24cdd573f977a11e794811", 16)
	print "y_G = ", y_G

	#order - rzad G
	order = int("ffffffffffffffffffffffff99def836146bc9b1b4d22831", 16)
	print "order = ", order
	F = FiniteField(p, 1)
	curve = EllipticCurve(a=F(a), b=F(b))
	P = Point(curve, F(x_G), F(y_G))


	r = random.randint(2, order)
	priv_key = SecretKey(r)
	P = r * P
	Q = priv_key.a * P

	pub_key = PublicKey(curve, P, Q, order)

	#STEP1 send R
	k = random.randint(1, order)
	R = k * P
	print "k = ", k

	#STEP2 send challenge
	e = random.randint(1, order)
	print "e = ", e

	#STEP3 compute s
	s = (k + priv_key.a * e) % order
	print "s = ", s

	#Verficiation
	print s * P
	print R + e * Q
	print s * P == R + e * Q