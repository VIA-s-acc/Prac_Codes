import subprocess
from ..lineq import MatrixMethods
import configparser

__LOCAL__: bool = True # True if it is running in local ( DISABLE API_KEY CHECK )


def check_flask():
    try:
        import flask
        print("🟢 Flask found.")
    except:
        print("🔴 Flask not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("🟢 Flask installed.")



def main():
    check_flask()
    from flask import Flask, jsonify
    from .mm_routes import (
        home,  # no input 
        det, max_matrix, lu, cholv1, cholv2, inverse, # 1 matrix
        sum_m, mult_m, # 2 matrices
        mult_m_s, # matrice and scalar
        signum, absoulte, # 1 scalar
        rand, # 2 scalar
        )

    app = Flask(__name__)

    if not __LOCAL__:
        from flask import request
        from .api_key.generate import is_valid_api_key ### realise your own api key generator and chekcer )    
        
        def before_request(): ### 
            api = request.args.get("api_key")
            if api and is_valid_api_key(api):
                return
            return jsonify(error="Invalid API key", status=401), 401

        app.before_request(before_request)

    app.add_url_rule('/', 'home', home, methods=['GET'])
    app.add_url_rule('/det/', 'determinant', det, methods=['GET'])
    app.add_url_rule('/max_m/', 'max_matrix', max_matrix, methods=['GET'])
    app.add_url_rule('/lu/', 'lu', lu, methods=['GET'])
    app.add_url_rule('/cholv1/', 'cholv1', cholv1, methods=['GET'])
    app.add_url_rule('/cholv2/', 'cholv2', cholv2, methods=['GET'])
    app.add_url_rule('/inv/', 'inv', inverse, methods=['GET'])
    app.add_url_rule("/sum_m/", 'sum_m', sum_m, methods=['GET'])
    app.add_url_rule("/mult_m/", 'mult_m', mult_m, methods=['GET'])
    app.add_url_rule("/mult_m_s/", 'mult_m_s', mult_m_s, methods=['GET'])
    app.add_url_rule("/sig/", 'sig', signum, methods=['GET'])
    app.add_url_rule("/abs/", 'abs', absoulte, methods=['GET'])
    app.add_url_rule("/rand/", "rand", rand, methods=['GET'])
    
    
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(error="Page not found", status=404), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error="Internal server error", status=500), 500
    
    app.run(debug=True)
    
if __name__ == "__main__":
    main()
