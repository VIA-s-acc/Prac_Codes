from ..build.lineq_sub import (
        solve_gauss,
)
from ...matrix_methods import(
        MatrixMethods
)



matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
vector = [1, 2, 3]


vector = solve_gauss(matrix, vector)


print(MatrixMethods.multiply_matrices(matrix, [[vector[0]], [vector[1]], [vector[2]]]))

