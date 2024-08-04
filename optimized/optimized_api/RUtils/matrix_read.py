from flask import request, jsonify
import ast
def matirx_input_g(request):
    tpe = request.args.get('type', 'str', type=str)
    if tpe == 'list':
        try:
            matrix_input = request.args.get('matrix', type=str)
            matrix_input = ast.literal_eval(matrix_input)
 
        except:
            return None, tpe
    
    elif tpe == 'str':
        matrix_input = request.args.get('matrix', type=str)
        
    return matrix_input, tpe


def matrix_read(matrix_input, tpe):
    matrix = []
    prev_row = []
    flag = False
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
                    
    return matrix, flag

def check_matrix_shape(matrix):
    for row in matrix:
        if len(row) != len(matrix[0]):
            return False
    return True