import json, os

standart_cfg = {
    "modules":
    {
        "lineq": [
                "matrix_methods", 
                "generator", 
                "checker"
            ]
    },

    "settings":
    {
        "check_cython": True,
        "run_tests": True,
        "print_result": True,
        "traceback": True,
        "prefix": ""
    }
}


def load_cfg():
    if not cfg_file_exists():
        print('🔴 build_modules.json not found. Creating...')
        json.dump(standart_cfg, open('build_cfg/build_modules.json', 'w'))
    
    print('🟢 build_modules.json found.')
    with open('build_cfg/build_modules.json') as f:
        cfg = json.load(f)
    return cfg

def cfg_file_exists():
    return os.path.exists('build_cfg/build_modules.json')