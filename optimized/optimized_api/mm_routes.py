import json
import time
from flask import request, render_template, jsonify
from ..lineq import MatrixMethods
from .RUtils.matrix_read import matrix_input_g, matrix_read, check_matrix_shape
from .RUtils.double_read import double_input_g, double_read
import math

def home():
    with open('optimized/optimized_api/static/data.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

def rand():
    start = time.time()
    double_input1 = double_input_g(request, name = 'double1')
    double_input2 = double_input_g(request, name = 'double2')
    if double_input1 is None or double_input2 is None:
        err_str_help = ' | double1 | ' if double_input1 is None else ''
        err_str_help += ' | double2 | ' if double_input2 is None else ''
        return jsonify({'result': None, 'error': f'Invalid input ( err in [{err_str_help}])', 'scalar1': double_input1, 'scalar2': double_input2, 'spent': None, 'result_calc_time': None})
    
    double1, flag_s = double_read(double_input1)
    double2, flag_s2 = double_read(double_input2)
    
    if flag_s or flag_s2:
        err_str_help = ' | double1 | ' if flag_s is None else ''
        err_str_help += ' | double2 | ' if flag_s2 is None else ''
        return jsonify({'result': None, 'error': f'Invalid scalar ( err in [{err_str_help}])', 'scalar1': double1, 'scalar2': double2, 'spent': time.time() - start, 'result_calc_time': None})
    
    calc_start = time.time()
    
    try:
        rand_ = MatrixMethods.random(double1, double2)
        return jsonify({'result': rand_, 'error': None, 'scalar1': double1, 'scalar2': double2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'scalar1': double1, 'scalar2': double2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def absoulte():
    start = time.time()
    double_input = double_input_g(request)
    if double_input is None:
        return jsonify({'result': None, 'error': 'Invalid input', 'scalar': None, 'spent': None, 'result_calc_time': None})
    
    double, flag_s = double_read(double_input)
    
    if flag_s:
        return jsonify({'result': None, 'error': f'Invalid scalar', 'scalar': double, 'spent': time.time() - start, 'result_calc_time': None})
    
    calc_start = time.time()
    
    try:
        abs_ = MatrixMethods.absolute(double)
        return jsonify({'result': abs_, 'error': None, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def signum():
    start = time.time()
    double_input = double_input_g(request)
    if double_input is None:
        return jsonify({'result': None, 'error': 'Invalid input', 'scalar': None, 'spent': None, 'result_calc_time': None})
    
    double, flag_s = double_read(double_input)
    
    if flag_s:
        return jsonify({'result': None, 'error': f'Invalid scalar', 'scalar': double, 'spent': time.time() - start, 'result_calc_time': None})
    
    calc_start = time.time()
    
    try:
        sig_ = MatrixMethods.sig(double)
        return jsonify({'result': sig_, 'error': None, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def mult_m_s():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    double_input = double_input_g(request)
    if matrix_input is None or double_input is None:
        err_str_help = " | Matrix_input | " if matrix_input is None else ""
        err_str_help += " | Scalar_input | " if double_input is None else ""
        return jsonify({'result': None, 'error': f'Invalid input (error in [{err_str_help}])', 'input_type ': tpe, 'matrix': matrix_input, 'scalar': double_input, 'spent': None, 'result_calc_time': None})
    
    matrix, flag = matrix_read(matrix_input, tpe)
    double, flag_s = double_read(double_input)
    if flag or flag_s:
        err_str_help = " | non numeric elements in matrix | " if flag else ""
        err_str_help += " | invalid scalar | " if flag_s else ""
        return jsonify({'result': None, 'error': f'Invalid matrix ([{err_str_help}])', 'input_type': tpe, 'matrix': matrix, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix[0]) == 0:
        return jsonify({'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': None})

    if not check_matrix_shape(matrix):
        return jsonify({'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, scalar: double,'spent': time.time() - start, 'result_calc_time': None})

    calc_start = time.time()
    
    try:
        multed_s = MatrixMethods.multiply_matrix_by_scalar(matrix, double)
        return jsonify({'result': multed_s, 'error': None, 'input_type': tpe,  'matrix': matrix, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def mult_m():
    start = time.time()
    matrix_input1, tpe = matrix_input_g(request, name= 'matrix1')
    matrix_input2, tpe = matrix_input_g(request, name= 'matrix2')
    
    if matrix_input1 is None or matrix_input2 is None:
        return jsonify({'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix1': matrix_input1, 'matrix2': matrix_input2, 'spent': None, 'result_calc_time': None})
    
    matrix1, flag = matrix_read(matrix_input1, tpe)
    matrix2, flag = matrix_read(matrix_input2, tpe)
    
    if flag:
        return jsonify({'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix1[0]) == 0 or len(matrix2[0]) == 0:
        return jsonify({'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None})
    
    m1_flag = check_matrix_shape(matrix1)
    m2_flag = check_matrix_shape(matrix2)
    
    if not m1_flag or not m2_flag:
        err_str_help = ' | Matrix1 | ' if not m1_flag else ''
        err_str_help += ' | Matrix2 | ' if not m2_flag else ''
        return jsonify({'result': None, 'error': 'Matrix must be rectangular (error in [' + err_str_help + '])', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None})

    calc_start = time.time()
    
    if (len(matrix1[0]) != len(matrix2)):
        return jsonify({'result': None, 'error': 'Matrix1 cols != Matrix2 rows', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None})
    try:                                                                                                                                    
        multed = MatrixMethods.multiply_matrices(matrix1, matrix2)
        return jsonify({'result': multed, 'error': None, 'input_type': tpe,  'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def sum_m():
    start = time.time()
    matrix_input1, tpe = matrix_input_g(request, name= 'matrix1')
    matrix_input2, tpe = matrix_input_g(request, name= 'matrix2')
    
    if matrix_input1 is None or matrix_input2 is None:
        return jsonify({'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix1': matrix_input1, 'matrix2': matrix_input2, 'spent': None, 'result_calc_time': None})
    
    matrix1, flag = matrix_read(matrix_input1, tpe)
    matrix2, flag = matrix_read(matrix_input2, tpe)
    
    if flag:
        return jsonify({'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix1[0]) == 0 or len(matrix2[0]) == 0:
        return jsonify({'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None})
    
    m1_flag = check_matrix_shape(matrix1)
    m2_flag = check_matrix_shape(matrix2)
    
    if not m1_flag or not m2_flag:
        err_str_help = ' | Matrix1 | ' if not m1_flag else ''
        err_str_help += ' | Matrix2 | ' if not m2_flag else ''
        return jsonify({'result': None, 'error': 'Matrix must be rectangular (error in [' + err_str_help + '])', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None})

    calc_start = time.time()
    
    if (len(matrix1) != len(matrix2)) or (len(matrix1[0]) != len(matrix2[0])):
        return jsonify({'result': None, 'error': 'Matrix1 and Matrix2 must have the same shape', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None})
    try:                                                                                                                                    
        summed = MatrixMethods.sum_matrices(matrix1, matrix2)
        return jsonify({'result': summed, 'error': None, 'input_type': tpe,  'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
def inverse():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    if matrix_input is None:
        return jsonify({'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None})
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify({'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix[0]) == 0:
        return jsonify({'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    if not check_matrix_shape(matrix):
        return jsonify({'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify({'result': None, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    try:
        inversed = MatrixMethods.inverse(matrix)
        return jsonify({'result': inversed, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def cholv2():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    if matrix_input is None:
        return jsonify({'result': {"l": None, 'd':None, 'u': None}, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None})
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify({'result': {"l": None, 'd':None, 'u': None}, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix[0]) == 0:
        return jsonify({'result': {"l": None, 'd':None, 'u': None}, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    if not check_matrix_shape(matrix):
        return jsonify({'result': {"l": None, 'd':None, 'u': None}, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify({'result': {"l": None, 'd':None, 'u': None}, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    try:
        L, D, U = MatrixMethods.cholv2(matrix)
        for row in L:
            for elem in row:
                if math.isnan(elem):
                    return jsonify({'result': {"l": None, 'd':None, 'u': None}, 'error': 'NaN in matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
                
        return jsonify({'result': {"l": L, 'd': D, 'u': U}, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': {"l": None, 'd':None, 'u': None}, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def cholv1():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    if matrix_input is None:
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None})
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix[0]) == 0:
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    if not check_matrix_shape(matrix):
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    try:
        L, U = MatrixMethods.cholv1(matrix)
        for row in L:
            for elem in row:
                if math.isnan(elem):
                    return jsonify({'result': {"l": None, 'u': None}, 'error': 'NaN in matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
                
        return jsonify({'result': {"l": L, 'u': U}, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': {"l": None, 'u': None}, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def lu():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    if matrix_input is None:
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None})
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix[0]) == 0:
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    if not check_matrix_shape(matrix):
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify({'result': {"l": None, 'u': None}, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    try:
        L, U = MatrixMethods.LU(matrix)
        for row in L:
            for elem in row:
                if math.isnan(elem):
                    return jsonify({'result': {"l": None, 'u': None}, 'error': 'NaN in matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
                
        return jsonify({'result': {"l": L, 'u': U}, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': {"l": None, 'u': None}, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def max_matrix():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    if matrix_input is None:
        return jsonify({'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None})
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify({'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix[0]) == 0:
        return jsonify({'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    if not check_matrix_shape(matrix):
        return jsonify({'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify({'result': None, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    try:
        max_matrix = MatrixMethods.max_matrix(matrix)
        return jsonify({'result': max_matrix, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })

def det():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    if matrix_input is None:
        return jsonify({'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None})
    
    matrix, flag = matrix_read(matrix_input, tpe)

    if flag:
        return jsonify({'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    
    if len(matrix[0]) == 0:
        return jsonify({'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})

    if not check_matrix_shape(matrix):
        return jsonify({'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
        
    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify({'result': None, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None})
    try:
        det = MatrixMethods.determinant(matrix)
        return jsonify({'result': det, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
    
    except Exception as ex:
        return jsonify({'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start })
