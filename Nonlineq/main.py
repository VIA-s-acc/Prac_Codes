from NonLinEq import Polynom, NonLinEqSolver, time_decorator, Prettier, Interpolation
from math import cos, pi, sqrt, sin, tan, e
import random
def funct(x):
    return cos(x)*sin(x*pi)+sqrt(5+x)

a = Polynom([[1, 3, 0, -1.0],'x'])
b = Polynom([[1, 3, 0, -1.5],'x'])
d = Polynom([[1, 3, 0, -2.0],'x'])

# print(Prettier.pretty_polynom(a))
c = NonLinEqSolver(Polynom = a, Area = (-3,1))
c1 = NonLinEqSolver(Polynom = b, Area = (-3,1))
c2 = NonLinEqSolver(Polynom = d, Area = (-3,1))
sol = c.solve(mode = 'newton', eps = 1e-15, step = 1.25, max_iter = 50)
sol1 = c1.solve(mode = 'newton', eps = 1e-15, step = 1.25, max_iter = 50)
sol2 = c2.solve(mode = 'newton', eps = 1e-15, step = 1.25, max_iter = 50)

# print("\33[32mSoultions: ", "\n\33[0m","\33[33m",sol,"\33[0m\n")
plot = []
plot1 = []
plot2 = []
for num in sol:
    plot.append((num, a(num)))

for num1 in sol1:
    plot1.append((num1, b(num1)))

for num2 in sol2:
    plot2.append((num2, d(num2)))

# a.plot(range = (-3, 1), step=0.01, colors=['blue', 'green', 'red', 'cyan'], legend = True, solutions1 = plot, solutions2 = plot1, solutions3 = plot2, poly = [(b, 'maroon', 'b(x)'), (d, 'magenta', 'd(x)')], func = [(lambda x: cos(x)*sin(x*pi)+sqrt(5.5+x), 'gray', 'f1(x)'), (lambda x: cos(x)*sin(x)+sqrt(5.1+x), 'lightgreen', 'f2(x)'), (lambda x: cos(x-pi)*sin(x*pi)+sqrt(7+x), 'orange', 'f3(x)')])
f = lambda x: sin(x+(pi*x-1)) + cos(x*(e)) + cos(e**x)
pts = [(0, 1), (0, 1.5), (1, 2)]

plotter = Polynom([[0], 'x'])

b = Interpolation.interpolate(func = f, mode = 'newton', points = 'auto', intervals = (0, 3, 12), variable = 'x')
b1 = Interpolation.interpolate(func = f, mode = 'newton', points = 'auto', intervals = (0, 3, 6), variable = 'x')
b2 = Interpolation.interpolate(func = f, mode = 'lagrange', points = 'auto', intervals = (0, 3, 3), variable = 'x')
b3 = Interpolation.interpolate(func = f, mode = 'newton', points = 'auto', intervals = (0, 3, 25), variable = 'x')
cspl = Interpolation.interpolate(func = f, mode = 'cspline', points = 'auto', intervals = (0, 3, 30), variable = 'x')
colors = ['cyan', 'yellow', 'blue', 'green', 'magenta', 'lightgreen', 'gray', 'pink', 'orange']
for key in cspl.keys():
    color = random.choice(colors)
    cspl[key] = (cspl[key], color)
    colors.remove(color)
    if len(colors) == 0:
        colors = ['cyan', 'yellow', 'blue', 'green', 'magenta', 'lightgreen', 'gray', 'pink', 'orange']


plotter.plot(range = (0, 3), step = 0.001, colors = ['black'], legend = False, grid = True, self_flag = False, title = 'Nonlinear cspline Interpolation', func = (f, 'red', 'f(x) = sin(x+(pi*x-1)) + cos(x*(e)) + cos(e**x)'), cspline = cspl)