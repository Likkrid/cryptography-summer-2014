from ec import EllipticCurve, Point, O
from fractions import Fraction as frac
import matplotlib.pyplot as plt
import numpy as np


def draw(ec):
	y, x = np.ogrid[-10:10:100j, -10:10:100j]
	plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * ec.a - ec.b, [0])
	plt.grid()

def draw_point(P):
	plt.plot([P.x], [P.y], marker='o', color='r')

def draw_sum(P, Q):
	R = P + Q
	plt.plot([P.x, Q.x], [P.y, Q.y], marker='o', color='r')
	if isinstance(R, O):
		pass
	else:
		plt.plot([R.x], [R.y], marker='o', color='r')

if __name__ == '__main__':
	ec = EllipticCurve(a=frac(-2), b=frac(4))
	p = Point(ec, frac(3), frac(5))
	q = Point(ec, frac(-2), frac(0))
	print p + q
	print q + p
	print q + q
	print 10*p

	draw(ec)
	draw_sum(p, q)
	draw_sum(q, q)
	plt.show()