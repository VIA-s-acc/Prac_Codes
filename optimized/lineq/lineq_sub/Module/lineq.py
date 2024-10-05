from ..build.lineq_sub import (
        solve_gauss,
        solve_lu,
        solve_tridiagonal,
        iter_solve_simple,
)
from ...matrix_methods import(
        MatrixMethods
)
from ...checker import (
        Checker
)
from ...generator import (
        Generator
)

import time
def time_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        name = func.__name__
        result = func(*args, **kwargs)
        spent = time.time() - start
        return result, spent, name
    return wrapper

td_gauss = time_decorator(solve_gauss)
td_lu = time_decorator(solve_lu)
td_tridiagonal = time_decorator(solve_tridiagonal)
td_iter = time_decorator(iter_solve_simple)

import random

def generate_random_symmetric_3diagonal_dd_matrix(n, lower_diag_range=(-1, 1), main_diag_range=(2, 5), upper_diag_range=(-1, 1)):

    # Initialize an empty matrix as a list of lists
    matrix = [[0] * n for _ in range(n)]

    # Fill the matrix with random values within the specified ranges
    for i in range(n):
        # Set the main diagonal
        matrix[i][i] = random.uniform(*main_diag_range)

        # Set the lower diagonal
        if i > 0:
            matrix[i][i - 1] = random.uniform(*lower_diag_range)

        # Set the upper diagonal
        if i < n - 1:
            matrix[i][i + 1] = random.uniform(*upper_diag_range)

    # Ensure the matrix is symmetric
    for i in range(n):
        for j in range(i + 1, n):
            matrix[j][i] = matrix[i][j]

    # Verify that the matrix is diagonal dominant
    for i in range(n):
        row_sum = sum(abs(matrix[i][j]) for j in range(n)) - abs(matrix[i][i])
        if abs(matrix[i][i]) < row_sum:
            raise ValueError(f"Matrix is not diagonal dominant at row {i}")

    return matrix
n = 50
matrix = generate_random_symmetric_3diagonal_dd_matrix(n, lower_diag_range=(-1, 1), main_diag_range=(3, 15), upper_diag_range=(-1, 1))


vector = [MatrixMethods.random(-100, 100) for i in range(n)]


import threading
import datetime

def solve_in_thread(func, matrix, vector, result, name ,*args):
        result.append(func(matrix, vector, *args))
        print(f"Поток {threading.current_thread().name} {name} завершен в {result[0][1]} секунд | TIME: {datetime.datetime.now()}" )


# ограничение на количество потоков

vector1 = []
vector2 = []
vector3 = []
vector4 = []

thread1 = threading.Thread(target=solve_in_thread, args=(td_gauss, matrix, vector, vector1, "gauss"))
thread2 = threading.Thread(target=solve_in_thread, args=(td_lu, matrix, vector, vector2, "lu"))
thread3 = threading.Thread(target=solve_in_thread, args=(td_tridiagonal, matrix, vector, vector3, "tridiagonal"))
thread4 = threading.Thread(target=solve_in_thread, args=(td_iter, matrix, vector, vector4, 'simple_iter',1e-16, 10, 10, 1e-16))

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()


res = [vector1[0], vector2[0], vector3[0], vector4[0]]
for i in range(len(res)):
        print(f"Method: {res[i][2]}\nspent: {res[i][1]}\nresult: ...\n" )

vector1 = vector1[0][0]
vector2 = vector2[0][0]
vector3 = vector3[0][0]
vector4 = vector4[0][0]


def vprint(vector, check, print_table = False):
        mult = MatrixMethods.multiply_matrices(matrix, [[vector[i]] for i in range(n)])
        abs_diff = 0
        max_diff = 0
        for index, row in enumerate(mult):
                if print_table:
                        print(row[0], "\t||\t", check[index], "\t||\t", row[0] - check[index])
                abs_diff = abs_diff + abs(row[0] - check[index])
                if abs(row[0] - check[index]) > max_diff:
                        max_diff = abs(row[0] - check[index])
        if print_table:
                print("Absolute difference: ", abs_diff)
                print("Max el difference: ", max_diff)


try:vprint(vector1, vector, print_table = True)
except Exception as Ex: print(Ex)
