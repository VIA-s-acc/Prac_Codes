from MPE import *
from math import e, sin, pi, sqrt
import numpy as np
def func(x, y):
    return y

def sol(x):
    return e**x

# b = MPE.k_step_Adams_explicit(4)
# print(b)


mpe = MPE((0, 4), func, 1)
mpe_ = MPE((0, 4), func, 1)
mpe1 = MPE((0, 4), func, 1)
mpe2 = MPE((0, 4), func, 1)
mpe3 = MPE((0, 4), func, 1)

numeric1 = mpe.eiler(125)
numeric2 = mpe.heun(125)
numeric3 = mpe_.solve_Adams_KSE(k = 4, n = 8, preliminary_k_method = "rk2")
numeric4 = mpe1.rk2(8)
numeric5 = mpe2.solve_Adams_KSE(k = 4, n = 8, preliminary_k_method = "rk4")
numeric6 = mpe3.rk4(8)
plotter = Plotter((0, 4))

error_func = return_error(plotter.plot)
_, error_map = error_func(func=sol, step=0.1, pts_eiler_n125 = [mpe.x, numeric2], pts_heun_n125 = [mpe.x, numeric1], pts_adams4_rk2_n8 = [mpe_.x, numeric3], pts_rk2_n8 = [mpe1.x, numeric4], pts_adams4_rk4_n8 = [mpe2.x, numeric5], pts_rk4_n8 = [mpe3.x, numeric6])

print(re_map_pretty(error_map)[0])
plot_histogram(error_map)

def m1(t):
    return 0

def m2(t):
    return 0

def v0(x):
    return 0
def f(x, t):
    return sin(pi*x)

def sol(x, t):
    return (1/pi**2-1/(pi**2*np.exp(pi**2*t)))*np.sin(pi*x)

bvp = BVP(5, 1, m1, m2, v0, f)
solution1 = bvp.solve_heat_equation(10000, 25, scheme = "explicit")
solution2 = bvp.solve_heat_equation(100, 25, scheme = "implicit")
solution2_2 = bvp.solve_heat_equation(1000, 25, scheme = "implicit")
solution3 = bvp.solve_heat_equation(100, 25, scheme = "weighted", omega = 0.5)
solution3_2 = bvp.solve_heat_equation(1000, 25, scheme = "weighted", omega = 0.5)

plotter.plot_solution(5, 1, pts_explicit_T_10000 = solution1, pts_implicit_T_100 = solution2, pts_implicit_T_1000 = solution2_2, pts_weighted_T_100 = solution3, pts_weighted_T_1000 = solution3_2, func_analitiyc_sol = sol,  edgecolor = 'random')



def k(x):
    return 0  

def q(x):
    return 1

def f(x):
    return 1 + x - e**(x**pi) * sin(x)

def d(x):
    return x**2/2 * pi**e**x

u,x = ritz(f, 0, 1, k, q, 50, integrate_n = 100)
plotter.plot(pts = [x, u])
u,x = finit_diff(f, 0, 1, 50, d, m1, m2)
plotter.plot(pts = [x, u])


