from ..lineq import Checker
from .RUtils.glret import add_dicts, process_data, get_GlobalRet
from .RUtils.matrix_read import matrix_input_g, matrix_read, check_matrix_shape
from flask import request, jsonify
import json
import time

def diag_dom():
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
    
    try:
        diag_ = Checker.diagonal_domination(matrix)
        return jsonify(add_dicts(upd_dict, {'result': diag_, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))



def sylvesters_c():
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
    
    try:
        sylv_ = Checker.sylvesters_criterion(matrix)
        return jsonify(add_dicts(upd_dict, {'result': sylv_, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))

def symm_c():
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
    
    try:
        symm_ = Checker.symmetric_check(matrix)
        return jsonify(add_dicts(upd_dict, {'result': symm_, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'input_type': tpe, 'matrix': matrix, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
