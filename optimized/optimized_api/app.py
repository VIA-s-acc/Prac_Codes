import subprocess
import configparser
import os, json, sys
import argparse

def check_config_parser():
    try:
        import configparser
        print("🟢 ConfigParser found.")
    except:
        print("🔴 ConfigParser not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "configparser"])
        print("🟢 ConfigParser installed.")
   
def run_build():
    os.chdir('optimized')
    subprocess.check_call([sys.executable, 'build.py'])
    os.chdir('..')
    
def check_lib_builds(flag):
    cfg = json.load(open('optimized/build_cfg/build_modules.json'))
    modules = cfg['modules']
    for lib in modules.keys():
        for module in modules[lib]:
            if not os.path.exists(f'optimized/{lib}/{module}/build'):
                print(f'🔴 Error in libs build | REBUILDING.')
                run_build()
                return True
    if flag:
        print("\033[93m -r --rebuild flag set | REBUILDING. \033[0m")
        run_build()
        
    return True

def check_config():
    check_config_parser()
    if not os.path.exists('optimized/optimized_api/static/config.ini'):

        config = configparser.ConfigParser()
        config["DEFAULT"] = {
                "API_KEY": "",
                "__LOCAL__": "True",
                "__DEBUG__": "True"
            }
        
        with open('optimized/optimized_api/static/config.ini', 'w') as configfile:
            config.write(configfile)
        
        
        
def load_config(profile='DEFAULT', flag=False):
    check_config()
    check_lib_builds(flag)
    config = configparser.ConfigParser()
    config.read('optimized/optimized_api/static/config.ini')
    return config[profile]

def check_flask():
    try:
        import flask
        print("🟢 Flask found.")
    except:
        print("🔴 Flask not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("🟢 Flask installed.")


def main(flag):
    check_flask()
    __FLAG__ = flag
    config = load_config('DEFAULT', flag = __FLAG__)
    try:
        __LOCAL__ = True if config["__LOCAL__"] == "True" else False
        __DEDBUG__ = True if config["__DEBUG__"] == "True" else False
        __API__ = str(config["API_KEY"])

    except Exception as EX: 
        print(f"🔴 {EX}")
        exit(-1)
    
    print("\033[1;32;40mAPI:\033[0m", "\033[1;31;40m", __API__, "\033[0m")
    print("\033[1;33;40mLOCAL:\033[0m", "\033[1;31;40m", __LOCAL__,  "\033[0m")
    print("\033[1;34;40mDEBUG:\033[0m", "\033[1;31;40m", __DEDBUG__, "\033[0m")
    print("\033[1;35;40mREBUILD FLAG:\033[0m", "\033[1;31;40m", __FLAG__, "\033[0m")
    
    from flask import Flask, jsonify, render_template
    from .mm_routes import (
        home,  # no input 
        det, max_matrix, lu, cholv1, cholv2, inverse, # 1 matrix
        sum_m, mult_m, # 2 matrices
        mult_m_s, # matrice and scalar
        signum, absoulte, # 1 scalar
        rand, # 2 scalar
        eigen, # 1 matrix, 2 scalars
        norm, # 1 vector
        approx, # 2 vectors
        )
    
    from .gntr_routes import (
        gen_rand_matrix,
        gen_rand_vec
    )
    
    from .chk_routes import (
        diag_dom,
        sylvesters_c,
        symm_c
    )

    app = Flask('optimized_API')

    if not __LOCAL__:
        from flask import request
        from .api_key.generate import is_valid_api_key ### realise your own api key generator and chekcer )    
        @app.before_request
        def before_request(): ### 
            nonlocal __API__
            if __API__ and is_valid_api_key(__API__):
                return
            return jsonify(error="Invalid API key", status=401, API=__API__), 401

    ### matrix_methods
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
    app.add_url_rule("/eig_mm/", "eig_mm", eigen, methods=['GET'])
    app.add_url_rule('/norm/', 'norm', norm, methods=['GET'])
    app.add_url_rule('/approx/', 'approx', approx, methods=['GET'])
    
    ### Generator
    app.add_url_rule('/rand_m/', 'gen_rand_matrix', gen_rand_matrix, methods=['GET'])
    app.add_url_rule('/rand_v/', 'gen_rand_vec', gen_rand_vec, methods=['GET'])
    
    ### Checker
    app.add_url_rule('/chk_dd/', 'diag_dom', diag_dom, methods=['GET'])
    app.add_url_rule('/chk_pd/', 'sylvesters_c', sylvesters_c, methods=['GET'])
    app.add_url_rule('/chk_sy/', 'symm_c', symm_c, methods=['GET'])
    
    @app.route('/main/')
    def main():
        return render_template('index.html')

    @app.route('/<module>')
    def module_func(module):
        return render_template(f"{module}/{module}.html", module = module)
    
    @app.route('/<module>/<submodule>')
    def submodule_func(module, submodule):
        return render_template(f"{module}/{submodule}/{submodule}.html", module = module, submodule = submodule)
    
    @app.route('/<module>/<submodule>/<func>')
    def func_func(module, submodule, func):
        print(f"{module}/{submodule}/{func}.html")
        return render_template(f"{module}/{submodule}/{func}.html", module = module, submodule = submodule, func = func)
    
        
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(error="Page not found", status=404), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error="Internal server error", status=500), 500

    app.run(debug=True, use_reloader = False)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'optimized_api',
        description='optimized_api FLASK app',
    )

    parser.add_argument(
        '-r', '--rebuild', '-re', action='store_true', help='Rebuild optimized_api'
    )
    args = parser.parse_args()

    main(flag=args.rebuild)

