from flask import request, jsonify


def double_input_g(request, name = 'double') -> str:
    double_input = request.args.get(name, type=str)
    return double_input

def double_read[T: (float, bool)](double_input) -> T:
    try: 
        double = float(double_input)
        return double, False
    except:
        return double_input, True