from sympy import *
from sympy.logic import SOPform
from sympy import symbols
x, y = symbols('x,y')
print( y | (x & y))
print( x >> y)
print(x | y)
print( ~x)
print((y & x).subs({x: True, y: True}))
print((x | y).atoms())
w, x, y, z = symbols('w x y z')
minterms = [[0, 0, 0, 1], [0, 0, 1, 1],[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1]]
dontcares = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]]
print(SOPform([w, x, y, z], minterms, dontcares))
