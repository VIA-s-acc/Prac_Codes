from ..build.lineq_sub import (
        solve_gauss,
        solve_lu
)
from ...matrix_methods import(
        MatrixMethods
)



matrix =   [[7, 1, 3],
            [1, 4, 2],
            [3, 2, 8]]
vector = [-8, -2, 5]


vector1 = solve_gauss(matrix, vector)
vector2 = solve_lu(matrix, vector)
print(vector)
print(vector1)
print(matrix)
print(vector)
print(MatrixMethods.multiply_matrices(matrix, [[vector1[0]], [vector1[1]], [vector1[2]]]))
print(MatrixMethods.multiply_matrices(matrix, [[vector2[0]], [vector2[1]], [vector2[2]]]))

