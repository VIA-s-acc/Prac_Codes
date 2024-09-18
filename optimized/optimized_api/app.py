import subprocess
import configparser
import os, json, sys
import argparse
import tqdm
import urllib
import time
from .RUtils.loggers import loggers

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
        print("🔴 config.ini not found. Downloading...")
        with open('optimized/optimized_api/static/config.ini', 'wb') as f:
            with urllib.request.urlopen('https://raw.githubusercontent.com/VIA-s-acc/Prac_Codes/main/optimized/optimized_api/static/config.ini') as response:
                total_size = int(response.headers.get('content-length', 0))
                print(f"Downloading {total_size} bytes")
                block_size = 1024
                pbar = tqdm.tqdm(total=total_size, unit="Bytes", unit_scale=True, unit_divisor=block_size, leave=False)
                while True:
                    data = response.read(block_size)
                    import time 
                    if not data:
                        break
                    pbar.update(len(data))
                    f.write(data)
                time.sleep(0.1)
                pbar.update(0)
        print("\n🟢 config.ini downloaded.")
    else:
        print("🟢 config.ini found.")
        
        
        
        
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
    

def check_loguru(flag = False):
    try:
        import loguru
        print("🟢 Loguru found.")
        return True
    except:
        if flag:
            print("🔴 Loguru not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "loguru"])
            print("🟢 Loguru installed.")
            return True
    return False


def main(flag):
    check_flask()
    __FLAG__ = flag
    config = load_config('DEFAULT', flag = __FLAG__)
    try:
        __LOCAL__ = True if config["__LOCAL__"] == "True" else False
        __DEDBUG__ = True if config["__DEBUG__"] == "True" else False
        __API__ = str(config["API_KEY"])
        __LOGGING__ = True if config["__LOGGING__"] == "True" else False
        if config["__LOGGERS__"]:
            __LOGGERS__ = config["__LOGGERS__"].replace(" ", "").split(",")
            _loggers = loggers(__LOGGERS__)

    except Exception as EX: 
        print(f"🔴 {EX}")
        exit(-1)
    
    lgru = check_loguru(flag = __LOGGING__)
    print("\033[1;32;40mAPI:\033[0m", "\033[1;31;40m", __API__, "\033[0m")
    print("\033[1;33;40mLOCAL:\033[0m", "\033[1;31;40m", __LOCAL__,  "\033[0m")
    print("\033[1;34;40mDEBUG:\033[0m", "\033[1;31;40m", __DEDBUG__, "\033[0m")
    print("\033[1;36;40mLOGGING:\033[0m", "\033[1;31;40m", __LOGGING__, "\033[0m")
    __LOGGERSF__ = True if len(__LOGGERS__) > 0 else False
    _loggers.print_loggers()           

    print("\033[1;35;40mREBUILD FLAG:\033[0m", "\033[1;31;40m", __FLAG__, "\033[0m")
    
    
    
    from flask import Flask, jsonify, render_template, request, send_from_directory
    from jinja2 import TemplateNotFound
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

    app = Flask(__name__)

    if not __LOCAL__:
        from .api_key.generate import is_valid_api_key ### realise your own api key generator and chekcer )    
        @app.before_request
        def API_check(): ### 
            nonlocal __API__
            if __LOGGING__ and lgru:
                logger.info(f"Request: {request.method} {request.url} from {request.remote_addr}")
                logger.debug(f"Headers: {request.headers}")
                logger.debug(f"Body: {request.get_data()}")  
                
            if __API__ and is_valid_api_key(__API__):
                if __LOGGING__ and lgru:
                    logger.debug("API key is valid\n\n\n")
                return
        
            if __LOGGING__ and lgru:
                logger.debug("API key is not valid\n\n\n")
                
            return jsonify(error="Invalid API key", status=401, API=__API__), 401

    if __LOGGING__ and lgru:
        from loguru import logger
        logger.remove(0)
        loggers_args = _loggers.get_loggers()
        print("\033[1;36;40mLoggers info: \033[0m")

        for k, v in loggers_args.items():
            if not k.startswith("__LSTDERR__"):
                try:
                    logger.add(f"optimized/optimized_api/logs/{k}.log", rotation="10 MB", retention="10 days", level=v)
                    if isinstance(v, int):
                        print(f"    🟢 Logger {k} created\tLevel: {v}\t {logger.level(f"{k}", no=v)}")
                    else:
                        print(f'    🟢 Logger {k} created\tLevel: {v}\t {logger.level(v)}')
                except Exception as EX:
                    print(f"    🔴 Logger {k} creating error, please check config.ini\tLevel: {v}\n{EX}")
                    exit(-1)
                    
            elif k.startswith("__LSTDERR__"):
                logger.add(sys.stderr, level = v)
                if isinstance(v, int):
                    print(f"    🟢 Logger {k} created\tLevel: {v}\t {logger.level(f"{k}", no=v)}")
                else:
                    print(f"    🟢 Logger {k} created\tLevel: {v}\t {logger.level(v)}")
            

        @app.before_request
        def log_request_info():
            logger.info(f"Request: {request.method} {request.url} from {request.remote_addr}")
            logger.debug(f"Headers: {request.headers}")
            logger.debug(f"Body: {request.get_data()}\n\n\n")

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
    
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    @app.route('/main/')
    def main():
        return render_template('index.html')
    
    @app.route('/main/<module>')
    def module_func(module):
        return render_template(f"{module}/{module}.html", module = module)
    
    @app.route('/main/<module>/<submodule>')
    def submodule_func(module, submodule):
        return render_template(f"{module}/{submodule}/{submodule}.html", module = module, submodule = submodule)
    
    @app.route('/main/<module>/<submodule>/<func>')
    def func_func(module, submodule, func):
        return render_template(f"{module}/{submodule}/{func}.html", module = module, submodule = submodule, func = func)
        
    @app.errorhandler(404)
    def page_not_found(e):
        if __LOGGING__ and lgru:
            logger.info(f"Request: {request.method} {request.url} from {request.remote_addr}")
            logger.debug(f"Headers: {request.headers}")
            logger.debug(f"Body: {request.get_data()}\n\n\n")
            logger.error(f"Page path: {request.path}\nfull path: {request.full_path}\nurl: {request.url} \n\n\n")
            logger.error("Page not found | 404\n\n\n")
        return jsonify(error="Page not found", status=404), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if __LOGGING__ and lgru:
            logger.info(f"Request: {request.method} {request.url} from {request.remote_addr}")
            logger.debug(f"Headers: {request.headers}")
            logger.debug(f"Body: {request.get_data()}")
            logger.exception(f"Error details: {e}")
            logger.error(f"Page path: {request.path}\nfull path: {request.full_path}\nurl: {request.url} \n\n\n")
            logger.error("Internal server error | 500\n\n\n")
        return jsonify(error="Internal server error", status=500), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        if __LOGGING__ and lgru:
            logger.info(f"Request: {request.method} {request.url} from {request.remote_addr}")
            logger.debug(f"Headers: {request.headers}")
            logger.debug(f"Body: {request.get_data()}")
            logger.exception(f"Error details: {e}")
            logger.error(f"Error Type: {type(e)}\nPage path: {request.path}\nfull path: {request.full_path}\nurl: {request.url} \n\n\n")
            logger.error("Internal server error | 500\n\n\n")
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

