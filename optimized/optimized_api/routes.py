import json
import ast
import time
from flask import request, render_template, jsonify
from ..lineq import MatrixMethods


def home():
    with open('optimized/optimized_api/static/data.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

def det():
    tpe = request.args.get('type', 'str', type=str)
    if tpe == 'list':
        try:
            matrix_input = request.args.get('matrix', type=str)
            matrix_input = ast.literal_eval(matrix_input)
        except:
            return jsonify({'det': None, 'error': 'Invalid matrix input', 'input_type': tpe, 'matrix': None, 'spent': None, 'det_calc_time': None})
    elif tpe == 'str':
        matrix_input = request.args.get('matrix', type=str)
      
    if matrix_input is not None:  
        matrix = []
        prev_row = []
        flag = False
        start = time.time()
        if tpe == 'str':
            for row in matrix_input.strip().split('\\n'):
                row_list = []
                for element in row.split():
                    try:
                        row_list.append(float(element))
                    except ValueError:
                        flag = True
                        row_list.append(element)
                matrix.append(row_list)
        elif tpe == 'list':
            matrix = matrix_input
            for row in matrix:
                for element in row:
                    try:
                        float(element)
                    except:
                        flag = True

        end = time.time() - start
        if flag:
            return jsonify({'det': None, 'error': 'Invalid matrix (non numeric elements)', 'input_type': tpe, 'matrix': matrix, 'spent': end, 'det_calc_time': None})
        end = time.time() - start
        if len(matrix[0]) == 0:
            return jsonify({'det': None, 'error': 'Empty matrix', 'input_type': tpe, 'matrix': matrix, 'spent': end, 'det_calc_time': None})
        
        prev = matrix[0]
        for row in matrix[1:]:
            if len(prev) != len(row):
                end = time.time() - start
                return jsonify({'det': None, 'error': 'Matrix must be rectangular', 'input_type': tpe, 'matrix': matrix, 'spent': end, 'det_calc_time': None})
            prec = row
            
        calc_start = time.time()
        end = time.time() - start
        if len(matrix) != len(matrix[0]):
            return jsonify({'det': None, 'error': 'Matrix must be square', 'input_type': tpe, 'matrix': matrix, 'spent': end, 'det_calc_time': None})
        try:
            det = MatrixMethods.determinant(matrix)
            calc_time = time.time() - start 
            return jsonify({'det': det, 'error': None, 'input_type': tpe,  'matrix': matrix, 'spent': calc_time, 'det_calc_time': calc_time})
        except Exception as ex:
            return jsonify({'error': str(ex)})
    else:
        return jsonify({'det': None, 'error': 'Matrix not found (invalid input)', 'input_type': tpe, 'matrix': None, 'spent': None, 'det_calc_time': None})
        
