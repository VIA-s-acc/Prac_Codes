import json
import time
from flask import request, render_template, jsonify
from ..lineq import MatrixMethods
from .RUtils.matrix_read import matrix_input_g, matrix_read, check_matrix_shape
from .RUtils.double_read import double_input_g, double_read
import math
import os

def get_GlobalRet(requset):
    data = {
            "global_info": {
                "GlobalRet":
                    {
                        "headers": {}, 
                        "path": "", 
                        "full_path": "", 
                        "script_root": "", 
                        "url": "", 
                        "base_url": "", 
                        "url_root": "", 
                        "host_url": "", 
                        "host": "", 
                        "method": ""
                    },
                "link_to_api": "",
                "api_key": "",
        }
    }
    data['global_info']['link_to_api'] = request.base_url
    if request.args.get('api_key') is not None:
        data['global_info']['api_key'] = request.args.get('api_key')
    for key in request.headers:
        data['global_info']['GlobalRet']['headers'].update({key[0]: key[1]})
    data['global_info']['GlobalRet']['path'] = request.path
    data['global_info']['GlobalRet']['full_path'] = request.full_path
    data['global_info']['GlobalRet']['script_root'] = request.script_root
    data['global_info']['GlobalRet']['url'] = request.url
    data['global_info']['GlobalRet']['base_url'] = request.base_url
    data['global_info']['GlobalRet']['url_root'] = request.url_root
    data['global_info']['GlobalRet']['host_url'] = request.host_url
    data['global_info']['GlobalRet']['host'] = request.host
    data['global_info']['GlobalRet']['method'] = request.method
    
    return data
    
def add_dicts(dict1, dict2):
    dict1.update(dict2)
    return dict1
        
def process_data(data, request):
    data['global_info']['link_to_api'] = request.url
    if request.args.get('api_key') is not None:
        data['global_info']['api_key'] = request.args.get('api_key')
    # data['global_info']['GlobalRet']['headers'] = request.headers
    for key in request.headers:
        data['global_info']['GlobalRet']['headers'].update({key[0]: key[1]})
    data['global_info']['GlobalRet']['path'] = request.path
    data['global_info']['GlobalRet']['full_path'] = request.full_path
    data['global_info']['GlobalRet']['script_root'] = request.script_root
    data['global_info']['GlobalRet']['url'] = request.url
    data['global_info']['GlobalRet']['base_url'] = request.base_url
    data['global_info']['GlobalRet']['url_root'] = request.url_root
    data['global_info']['GlobalRet']['host_url'] = request.host_url
    data['global_info']['GlobalRet']['host'] = request.host
    data['global_info']['GlobalRet']['method'] = request.method
    
def home():
    with open('optimized/optimized_api/static/data.json', 'r') as file:
        data = json.load(file)
        process_data(data=data, request=request)
    
    return jsonify(data)

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
    double_input1 = double_input_g(request, name = 'double1')
    double_input2 = double_input_g(request, name = 'double2')
    upd_dict = get_GlobalRet(requset=request)
    if double_input1 is None or double_input2 is None:
        err_str_help = ' | double1 | ' if double_input1 is None else ''
        err_str_help += ' | double2 | ' if double_input2 is None else ''
        return jsonify(add_dicts({'result': None, 'error': f'Invalid input ( err in [{err_str_help}])', 'scalar1': double_input1, 'scalar2': double_input2, 'spent': None, 'result_calc_time': None}, upd_dict))
    
    double1, flag_s = double_read(double_input1)
    double2, flag_s2 = double_read(double_input2)
    
    if flag_s or flag_s2:
        err_str_help = ' | double1 | ' if flag_s is None else ''
        err_str_help += ' | double2 | ' if flag_s2 is None else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid scalar ( err in [{err_str_help}])', 'scalar1': double1, 'scalar2': double2, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        rand_ = MatrixMethods.random(double1, double2)
        return jsonify(add_dicts(upd_dict, {'result': rand_, 'error': None, 'scalar1': double1, 'scalar2': double2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'scalar1': double1, 'scalar2': double2, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def absoulte():
    start = time.time()
    double_input = double_input_g(request)
    upd_dict = get_GlobalRet(requset=request)
    if double_input is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'scalar': None, 'spent': None, 'result_calc_time': None}))
    
    double, flag_s = double_read(double_input)
    
    if flag_s:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid scalar', 'scalar': double, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        abs_ = MatrixMethods.absolute(double)
        return jsonify(add_dicts(upd_dict, {'result': abs_, 'error': None, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def signum():
    start = time.time()
    double_input = double_input_g(request)
    upd_dict = get_GlobalRet(requset=request)
    if double_input is None:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Invalid input', 'scalar': None, 'spent': None, 'result_calc_time': None}))
    
    double, flag_s = double_read(double_input)
    
    if flag_s:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid scalar', 'scalar': double, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        sig_ = MatrixMethods.sig(double)
        return jsonify(add_dicts(upd_dict, {'result': sig_, 'error': None, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def mult_m_s():
    start = time.time()
    matrix_input, tpe = matrix_input_g(request)
    double_input = double_input_g(request)
    upd_dict = get_GlobalRet(request)
    if matrix_input is None or double_input is None:
        err_str_help = " | Matrix_input | " if matrix_input is None else ""
        err_str_help += " | Scalar_input | " if double_input is None else ""
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid input (error in [{err_str_help}])', 'input_type ': tpe, 'matrix': matrix_input, 'scalar': double_input, 'spent': None, 'result_calc_time': None}))
    
    matrix, flag = matrix_read(matrix_input, tpe)
    double, flag_s = double_read(double_input)
    if flag or flag_s:
        err_str_help = " | non numeric elements in matrix | " if flag else ""
        err_str_help += " | invalid scalar | " if flag_s else ""
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid arg ([{err_str_help}])', 'input_type': tpe, 'matrix': matrix, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': None}))
    
    if len(matrix[0]) == 0:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': None}))

    if not check_matrix_shape(matrix):
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'scalar': double,'spent': time.time() - start, 'result_calc_time': None}))

    calc_start = time.time()
    
    try:
        multed_s = MatrixMethods.multiply_matrix_by_scalar(matrix, double)
        return jsonify(add_dicts(upd_dict, {'result': multed_s, 'error': None, 'input_type': tpe,  'matrix': matrix, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'scalar': double, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

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
