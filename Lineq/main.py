from LinEq import *

matrix =   [[7, 1, 3],
            [1, 4, 2],
            [3, 2, 8]]
vec = [-8, -2, 5]








def main(matrix, vec, mode = 'gauss', eps: float = 1e-15, iter: int = 1000, dig: int = 3, s_flag = False):

    sol = LinEqSolver.generate_and_solve_linear_equations(3, 'Lineq/eq/matrix.txt', 'Lineq/eq/vec.txt', 'Lineq/eq/sol.txt', 'Lineq/eq/sol_ext.txt',dig = dig, check=False, mode = mode, epsilon=eps, random = False, prettier = True, prettier_path="Lineq/eq/prettier/pretty_", logger=True, matrix = matrix,vector = vec, eigen_iter = iter, eigen_eps = eps, method_iter = iter, method_eps = eps)  

    if s_flag:
        Saver._combine_txt("Lineq/eq/prettier/", "Lineq/eq/prettier_combine/prettier_combined.txt", delete_flag=True)
        Saver._combine_txt("Lineq/eq/", "Lineq/eq/prettier_combine/combined.txt", delete_flag=True)
    
    try:
        print("Solution:")
        print(Prettier._pretty_matrix([[x] for x in sol]))
        print("Matrix * Solution:")
        print(Prettier._pretty_matrix(Methods._matrix_multiply(matrix, [[x] for x in sol])))
        print("Vector:")
        print(Prettier._pretty_matrix([[x] for x in vec]))
        print("Vector - Matrix * Solution:")
        print(Prettier._pretty_matrix([[x-y[0]] for x,y in zip(vec, Methods._matrix_multiply(matrix, [[x] for x in sol]))]))
    except:
        print("No solution found")

main(matrix, vec, mode = 'iter_mincsei',eps = 1e-15, iter = 1000, dig = 15, s_flag = True)


