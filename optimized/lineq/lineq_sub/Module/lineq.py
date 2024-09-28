from ..build.lineq_sub import (
        solve_gauss,
        solve_lu,
        solve_tridiagonal
)
from ...matrix_methods import(
        MatrixMethods
)
from ...checker import (
        Checker
)



matrix =   [[7, 1, 0],
            [16, 5, 1],
            [0, 2, 8]]
vector = [-8, -2, 5]

vector1 = solve_gauss(matrix, vector)
vector2 = solve_lu(matrix, vector)
try:
        vector3 = solve_tridiagonal(matrix, vector)
except SystemExit as ex:
        print(ex)
        
print(vector1)
print(vector2)
print(MatrixMethods.multiply_matrices(matrix, [[vector1[0]], [vector1[1]], [vector1[2]]]))
print(MatrixMethods.multiply_matrices(matrix, [[vector2[0]], [vector2[1]], [vector2[2]]]))
print(MatrixMethods.multiply_matrices(matrix, [[vector3[0]], [vector3[1]], [vector3[2]]]))

