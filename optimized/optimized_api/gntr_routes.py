from ..lineq import Generator
from .RUtils.glret import add_dicts, process_data, get_GlobalRet
from .RUtils.double_read import double_input_g, double_read
from flask import request, jsonify
import json
import time

def gen_rand_matrix():    
    start = time.time()
    size = double_input_g(request, name = 'size')
    rng = double_input_g(request, name = 'rng')
    mode = request.args.get('mode', type=str)
    upd_dict = get_GlobalRet(requset=request)
    if not mode in ['symm', '3diag']:
        mode = 'default' # <- default 
        
    if size is None or rng is None:
        err_str_help = ' | size | ' if size is None else ''
        err_str_help += ' | rng | ' if rng is None else ''
        return jsonify(add_dicts({'result': None, 'error': f'Invalid input ( err in [{err_str_help}])', 'size': size, 'rng': rng, 'mode': mode, 'spent': None, 'result_calc_time': None}, upd_dict))
    
    size, flag_s = double_read(size)
    rng, flag_s2 = double_read(rng)
    size = int(size)
    if flag_s or flag_s2:
        err_str_help = ' | size | ' if flag_s is None else ''
        err_str_help += ' | rng | ' if flag_s2 is None else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid scalar ( err in [{err_str_help}])', 'size': size, 'rng': rng, 'mode': mode, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        rand_ = Generator.generate_matrix(size, rng, mode)
        return jsonify(add_dicts(upd_dict, {'result': rand_, 'error': None, 'size': size, 'rng': rng, 'mode': mode, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
            
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'size': size, 'rng': rng, 'mode': mode, 'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
    
    
def gen_rand_vec():    
    start = time.time()
    size = double_input_g(request, name = 'size')
    rng = double_input_g(request, name = 'rng')
    upd_dict = get_GlobalRet(requset=request)

        
    if size is None or rng is None:
        err_str_help = ' | size | ' if size is None else ''
        err_str_help += ' | rng | ' if rng is None else ''
        return jsonify(add_dicts({'result': None, 'error': f'Invalid input ( err in [{err_str_help}])', 'size': size, 'rng': rng,  'spent': None, 'result_calc_time': None}, upd_dict))
    
    size, flag_s = double_read(size)
    rng, flag_s2 = double_read(rng)
    size = int(size)
    if flag_s or flag_s2:
        err_str_help = ' | size | ' if flag_s is None else ''
        err_str_help += ' | rng | ' if flag_s2 is None else ''
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': f'Invalid scalar ( err in [{err_str_help}])', 'size': size, 'rng': rng, 'spent': time.time() - start, 'result_calc_time': None}))
    
    calc_start = time.time()
    
    try:
        rand_ = Generator.generate_vector(size, rng)
        return jsonify(add_dicts(upd_dict, {'result': rand_, 'error': None, 'size': size, 'rng': rng,  'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))
            
    except Exception as ex:
        return jsonify(add_dicts(upd_dict, {'result': None, 'error': str(ex), 'size': size, 'rng': rng,  'spent': time.time() - start, 'result_calc_time': time.time() - calc_start }))