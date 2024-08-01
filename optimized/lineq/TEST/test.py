import unittest
from .. import MatrixMethods,Generator,Checker


MatrixMethods_ONEMATRIX_FUNCS = (
    MatrixMethods.determinant,
    MatrixMethods.inverse,
    MatrixMethods.max_matrix,
    MatrixMethods.LU,
    MatrixMethods.cholv1,
    MatrixMethods.cholv2,
)

MatrixMethods_TWOMATRIX_FUNCS = (
    MatrixMethods.sum_matrices,
    MatrixMethods.multiply_matrices,
    MatrixMethods.multiply_matrix_by_scalar,
)

MatrixMethods_DOUBLE_FUNCS = (
    MatrixMethods.sig,
    MatrixMethods.absolute,
    MatrixMethods.random,
)

MatrixMethods_ITERATIVE_FUNCS = (
    MatrixMethods.power_method,
    MatrixMethods.eigen,
)

MatrixMethods_VECTOR_FUNCS = (
    MatrixMethods.vec_approx,
    MatrixMethods.norm,    
)


Generator_FUNCS = (
    Generator.generate_matrix,
    Generator.generate_vector
)

Checker_FUNCS = (
    Checker.diagonal_domination,
    Checker.symmetric_check,
    Checker.sylvesters_criterion
)


class TestMatrixMethods(unittest.TestCase):
    def test_methods(self):
        for f in MatrixMethods_ONEMATRIX_FUNCS:
            try:
                f([[3,0],[0,2]])
            except Exception as e:
                self.fail(f'Ошибка: {e.__class__} {e}')
                
        for f in MatrixMethods_TWOMATRIX_FUNCS:
            if f.__name__ != 'multiply_matrix_by_scalar':
                try:
                    if f.__name__ != 'multiply_matrix_by_scalar':
                        f([[1,2],[3,4]],[[5,6],[7,8]])
                    else:
                        f([[1,2],[3,4]],5)
                except Exception as e:
                    self.fail(f'Ошибка: {e.__class__} {e}')
                    
        for f in MatrixMethods_DOUBLE_FUNCS:
                try:
                    if f.__name__ != 'random':
                        f(5)
                    else:
                        f(-5, 5)
                except Exception as e:
                    self.fail(f'Ошибка: {e.__class__} {e}')
                    
        for f in MatrixMethods_ITERATIVE_FUNCS:
            try:
                f([[5,1],[1,5]], 1, 0.1)
            except Exception as e:
                self.fail(f'Ошибка: {e.__class__} {e}')
                
        for f in MatrixMethods_VECTOR_FUNCS:
            try:
                if f.__name__ == 'norm':
                    f([1,2])
                else:
                    f([1,2], [1,2])
            except Exception as e:
                self.fail(f'Ошибка: {e.__class__} {e}')

class TestGenerator(unittest.TestCase):
    def test_methods(self):
        for f in Generator_FUNCS:
            try:
                f(5,5)
            except Exception as e:
                self.fail(f'Ошибка: {e.__class__} {e}')

class TestChecker(unittest.TestCase):
    def test_methods(self):
        for f in Checker_FUNCS:
            try:
                f([[1,2],[3,4]])
            except Exception as e:
                self.fail(f'Ошибка: {e.__class__} {e}')

if __name__ == '__main__':
    unittest.main()

