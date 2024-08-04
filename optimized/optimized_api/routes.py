import json
import time
from flask import request, render_template, jsonify
from ..lineq import MatrixMethods
from .RUtils.matrix_read import matirx_input_g, matrix_read, check_matrix_shape
import math

def home():
    with open('optimized/optimized_api/static/data.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

def inverse():
    start = time.time()
    matrix_input, tpe = matirx_input_g(request)
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
    matrix_input, tpe = matirx_input_g(request)
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
    matrix_input, tpe = matirx_input_g(request)
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
    matrix_input, tpe = matirx_input_g(request)
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
    matrix_input, tpe = matirx_input_g(request)
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
    matrix_input, tpe = matirx_input_g(request)
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
