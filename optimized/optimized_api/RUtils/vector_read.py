from flask import request, jsonify
import ast

def vector_input_g[T: (str, str)](request, name = 'vector') -> T:
    tpe = request.args.get('type', 'str', type=str)
    if tpe == 'list':
        try:
            vector_input = request.args.get(name, type=str)
            vector_input = ast.literal_eval(vector_input)
        except:
            return None, tpe
    
    elif tpe == 'str':
        vector_input = request.args.get(name, type=str)
        
    return vector_input, tpe


def vector_read[T: (list, bool)](vector_input, tpe) -> T:
    vector = []
    flag = False
    if tpe == 'str':
            for row in vector_input.strip().split():
                for element in row.split():
                    try:
                        vector.append(float(element))
                    except ValueError:
                        flag = True
                        vector.append(element)
                
    elif tpe == 'list':
        vector = vector_input
        for element in vector:
            try:
                float(element)
            except:
                flag = True
                    
    return vector, flag

def check_matrix_shape(matrix) -> bool:
    for row in matrix:
        if len(row) != len(matrix[0]):
            return False
    return True