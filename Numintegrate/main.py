from NumIntegrate import *
from math import sin
func = lambda x: x**2
a = Integrate(func=func, interv=(0, 2), n = 1000)
Integral = a.squqqares('center')

print(Integral)