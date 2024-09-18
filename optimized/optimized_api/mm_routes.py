import json
import time
from flask import request, jsonify
from ..lineq import MatrixMethods
from .RUtils.matrix_read import matrix_input_g, matrix_read, check_matrix_shape
from .RUtils.double_read import double_input_g, double_read
from .RUtils.vector_read import vector_input_g, vector_read
from .RUtils.glret import add_dicts, process_data, get_GlobalRet
import math


    
def home():
    with open('optimized/optimized_api/static/data.json', 'r') as file:
        data = json.load(file)
        process_data(data=data, request=request)
    
    return jsonify(data)

def approx():
    start = time.time()
    vector_input1, tpe = vector_input_g(request, name='vector1')
    vector_input2, tpe = vector_input_g(request, name='vector2')
    tol = double_input_g(request, name='tol')
    upd_dict = get_GlobalRet(requset=request)

    if vector_input1 is None or vector_input2 is None or tol is None:
        err_str_help = ' | vector1 | ' if vector_input1 is None else ''
        err_str_help += ' | vector2 | ' if vector_input2 is None else ''
        err_str_help += ' | tol | ' if tol is None else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid input ({err_str_help})', 'input_type': tpe, 'vector1': vector_input1, 'vector2': vector_input2, 'tol': tol, 'spent': None, 'result_calc_time': None}))
    
    vector1, flag1 = vector_read(vector_input1, tpe)
    vector2, flag2 = vector_read(vector_input2, tpe)
    tol, flag3 = double_read(tol)
    if flag1 or flag2 or flag3:
        err_str_help = ' | vector1 | ' if flag1 else ''
        err_str_help += ' | vector2 | ' if flag2 else ''
        err_str_help += ' | tol | ' if flag3 else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid vector (non numeric elements in ({err_str_help}))', 'input_type': tpe, 'vector1': vector1, 'vector2': vector2, 'tol': tol, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(vector1) == 0 or len(vector2) == 0:
        err_str_help = ' | vector1 | ' if len(vector1) == 0 else ''
        err_str_help += ' | vector2 | ' if len(vector2) == 0 else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Empty vector ({err_str_help})', 'input_type': tpe, 'vector1': vector1, 'vector2': vector2, 'tol': tol, 'spent': time.time() - start, 'result_calc_time': None}))

    if len (vector1) != len(vector2):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Vectors must be the same length', 'input_type': tpe, 'vector1': vector1, 'vector2': vector2, 'tol': tol, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        approx = MatrixMethods.vec_approx(vector1, vector2)
        return jsonify(add_dicts(upd_dict, {'result': approx, 'error': None, 'input_type': tpe,  'vector1': vector1, 'vector2': vector2, 'spent': time.time() - start, 'tol': tol, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'vector1': vector1, 'vector2': vector2, 'spent': time.time() - start, 'tol': tol, 'result_calc_time': time.time() - calc_start }))


def norm():
    start = time.time()
    vector_input, tpe = vector_input_g(request)
    upd_dict = get_GlobalRet(requset=request)

    if vector_input is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'input_type': tpe, 'vector': vector_input, 'spent': None, 'result_calc_time': None}))
    
    vector, flag = vector_read(vector_input, tpe)

    if flag:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid vector (non numeric elements)', 'input_type': tpe, 'vector': vector, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(vector) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty vector', 'input_type': tpe, 'vector': vector, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    try:
        norm = MatrixMethods.norm(vector)
        return jsonify(add_dicts(upd_dict, {'result': norm, 'error': None, 'input_type': tpe,  'vector': vector, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'vector': vector, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def eigen():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    double_input1 = double_input_g(request, name='itern')
    double_input2 = double_input_g(request, name='tol')
    upd_dict = get_GlobalRet(request)
    if matrix_input is None or double_input1 is None or double_input2 is None:
        err_str_help = " | Matrix_input | " if matrix_input is None else ""
        err_str_help += " | itern_input | " if double_input1 is None else ""
        err_str_help += " | tol_input | " if double_input2 is None else ""
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid input (error in [{err_str_help}])', 'input_type ': tpe, 'matrix': matrix_input, 'itern': double_input1, 'tol': double_input2, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)
    double1, flag_s = double_read(double_input1)
    double2, flag_s2 = double_read(double_input2)
    double1 = int(double1)
    
    if flag or flag_s or flag_s2:
        err_str_help = " | non numeric elements in matrix | " if flag else ""
        err_str_help += " | invalid itern | " if flag_s else ""
        err_str_help += " | invalid tol | " if flag_s2 else ""
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid arg ([{err_str_help}])', 'input_type': tpe, 'matrix': matrix, 'itern': double1, 'tol': double2, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'itern': double1, 'tol': double2, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'itern': double1, 'tol': double2, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    try:
        max_, min_ = MatrixMethods.eigen(matrix, int(double1), int(double2))
        return jsonify(add_dicts(upd_dict, {'result': {"max": {"eigenvector": max_[1], "eigenvalue": max_[0]}, "min": {"eigenvector": min_[1], "eigenvalue": min_[0]}}, 'error': None, 'input_type': tpe,  'matrix': matrix, 'itern': double1, 'tol': double2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'itern': double1, 'tol': double2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def rand():    
    start = time.time()
    double_input1 = double_input_g(request, name = 'dmin')
    double_input2 = double_input_g(request, name = 'dmax')
    upd_dict = get_GlobalRet(requset=request)
    if double_input1 is None or double_input2 is None:
        err_str_help = ' | dmin | ' if double_input1 is None else ''
        err_str_help += ' | dmax | ' if double_input2 is None else ''
        return jsonify(add_dicts({'result': None, 'error': f'Invalid input ( err in [{err_str_help}])', 'dmin': double_input1, 'dmax': double_input2, 'spent': None, 'result_calc_time': None}, upd_dict))
    
    dmin, flag_s = double_read(double_input1)
    dmax, flag_s2 = double_read(double_input2)
    
    if flag_s or flag_s2:
        err_str_help = ' | dmin | ' if flag_s is None else ''
        err_str_help += ' | dmax | ' if flag_s2 is None else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid scalar ( err in [{err_str_help}])', 'dmin': dmin, 'dmax': dmax, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        rand_ = MatrixMethods.random(dmin, dmax)
        return jsonify(add_dicts(upd_dict, {'result': rand_, 'error': None, 'dmin': dmin, 'dmax': dmax, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'dmin': dmin, 'dmax': dmax, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def absoulte():
    start = time.time()
    double_input = double_input_g(request)
    upd_dict = get_GlobalRet(requset=request)
    if double_input is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'double': None, 'spent': None, 'result_calc_time': None}))
    
    double, flag_s = double_read(double_input)
    
    if flag_s:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid scalar', 'double': double, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        abs_ = MatrixMethods.absolute(double)
        return jsonify(add_dicts(upd_dict, {'result': abs_, 'error': None, 'double': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'double': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def signum():
    start = time.time()
    double_input = double_input_g(request)
    upd_dict = get_GlobalRet(requset=request)
    if double_input is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'double': None, 'spent': None, 'result_calc_time': None}))
    
    double, flag_s = double_read(double_input)
    
    if flag_s:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid scalar', 'double': double, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        sig_ = MatrixMethods.sig(double)
        return jsonify(add_dicts(upd_dict, {'result': sig_, 'error': None, 'double': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'double': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def mult_m_s():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    double_input = double_input_g(request)
    upd_dict = get_GlobalRet(request)
    if matrix_input is None or double_input is None:
        err_str_help = " | Matrix_input | " if matrix_input is None else ""
        err_str_help += " | Double_input | " if double_input is None else ""
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid input (error in [{err_str_help}])', 'input_type ': tpe, 'matrix': matrix_input, 'double': double_input, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)
    double, flag_s = double_read(double_input)
    if flag or flag_s:
        err_str_help = " | non numeric elements in matrix | " if flag else ""
        err_str_help += " | invalid double | " if flag_s else ""
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid arg ([{err_str_help}])', 'input_type': tpe, 'matrix': matrix, 'double': double, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'double': double, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'double': double,'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    try:
        multed_s = MatrixMethods.multiply_matrix_by_scalar(matrix, double)
        return jsonify(add_dicts(upd_dict, {'result': multed_s, 'error': None, 'input_type': tpe,  'matrix': matrix, 'double': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'double': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def mult_m():
    start = time.time()
    matrix_input1, tpe = matrix_input_g(request, name= 'matrix1')
    matrix_input2, tpe = matrix_input_g(request, name= 'matrix2')
    upd_dict = get_GlobalRet(request=request)
    if matrix_input1 is None or matrix_input2 is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix1': matrix_input1, 'matrix2': matrix_input2, 'spent': None, 'result_calc_time': None}))
    
    matrix1, flag = matrix_read(matrix_input1, tpe)
    matrix2, flag = matrix_read(matrix_input2, tpe)
    
    if flag:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix1[0]) == 0 or len(matrix2[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None}))
    
    m1_flag = check_matrix_shape(matrix1)
    m2_flag = check_matrix_shape(matrix2)
    
    if not m1_flag or not m2_flag:
        err_str_help = ' | Matrix1 | ' if not m1_flag else ''
        err_str_help += ' | Matrix2 | ' if not m2_flag else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be rectangular (error in [' + err_str_help + '])', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    if (len(matrix1[0]) != len(matrix2)):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix1 cols != Matrix2 rows', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None}))
    try:                                                                                                                                    
        multed = MatrixMethods.multiply_matrices(matrix1, matrix2)
        return jsonify(add_dicts(upd_dict, {'result': multed, 'error': None, 'input_type': tpe,  'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def sum_m():
    start = time.time()
    matrix_input1, tpe = matrix_input_g(request, name= 'matrix1')
    matrix_input2, tpe = matrix_input_g(request, name= 'matrix2')
    upd_dict = get_GlobalRet(requset=request)
    if matrix_input1 is None or matrix_input2 is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix1': matrix_input1, 'matrix2': matrix_input2, 'spent': None, 'result_calc_time': None}))
    
    matrix1, flag = matrix_read(matrix_input1, tpe)
    matrix2, flag = matrix_read(matrix_input2, tpe)
    
    if flag:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix1[0]) == 0 or len(matrix2[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None}))
    
    m1_flag = check_matrix_shape(matrix1)
    m2_flag = check_matrix_shape(matrix2)
    
    if not m1_flag or not m2_flag:
        err_str_help = ' | Matrix1 | ' if not m1_flag else ''
        err_str_help += ' | Matrix2 | ' if not m2_flag else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be rectangular (error in [' + err_str_help + '])', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    if (len(matrix1) != len(matrix2)) or (len(matrix1[0]) != len(matrix2[0])):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix1 and Matrix2 must have the same shape', 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': None}))
    try:                                                                                                                                    
        summed = MatrixMethods.sum_matrices(matrix1, matrix2)
        return jsonify(add_dicts(upd_dict, {'result': summed, 'error': None, 'input_type': tpe,  'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix1': matrix1, 'matrix2': matrix2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
def inverse():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    upd_dict = get_GlobalRet(requset=request)
    if matrix_input is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    try:
        inversed = MatrixMethods.inverse(matrix)
        return jsonify(add_dicts(upd_dict, {'result': inversed, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def cholv2():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    upd_dict = get_GlobalRet(request=request)
    if matrix_input is None:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'd':None, 'u': None}, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'd':None, 'u': None}, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'd':None, 'u': None}, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'd':None, 'u': None}, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'd':None, 'u': None}, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    try:
        L, D, U = MatrixMethods.cholv2(matrix)
        for row in L:
            for elem in row:
                if math.isnan(elem):
                    return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'd':None, 'u': None}, 'error': 'NaN in matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
                
        return jsonify(add_dicts(upd_dict, {'result': {"l": L, 'd': D, 'u': U}, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'd':None, 'u': None}, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def cholv1():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    upd_dict = get_GlobalRet(requset=request)
    if matrix_input is None:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    try:
        L, U = MatrixMethods.cholv1(matrix)
        for row in L:
            for elem in row:
                if math.isnan(elem):
                    return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'NaN in matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
                
        return jsonify(add_dicts(upd_dict, {'result': {"l": L, 'u': U}, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def lu():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    upd_dict = get_GlobalRet(requset=request)
    if matrix_input is None:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    try:
        L, U = MatrixMethods.LU(matrix)
        for row in L:
            for elem in row:
                if math.isnan(elem):
                    return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': 'NaN in matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
                
        return jsonify(add_dicts(upd_dict, {'result': {"l": L, 'u': U}, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': {"l": None, 'u': None}, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def max_matrix():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    upd_dict = get_GlobalRet(requset=request)
    if matrix_input is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)
    
    if flag:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    try:
        max_matrix = MatrixMethods.max_matrix(matrix)
        return jsonify(add_dicts(upd_dict, {'result': max_matrix, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def det():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    upd_dict = get_GlobalRet(requset=request)

    if matrix_input is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'input_type': tpe, 'matrix': None, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)

    if flag:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
        
    calc_start = time.time()
    
    if len(matrix) != len(matrix[0]):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': None}))
    try:
        det = MatrixMethods.determinant(matrix)
        return jsonify(add_dicts(upd_dict, {'result': det, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
