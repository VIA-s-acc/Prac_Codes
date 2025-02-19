import json, os, shutil

standart_cfg = {
    "modules": # list of modules
    {
        "lineq": [ # list of libraries
                "matrix_methods", 
                "generator", 
                "checker",
                "lineq"
            ]
    },

    "settings": # settings
    {
        "check_cython": True, # check if cython is installed
        "check_setuptools": True, # check if setuptools is installed
        "run_tests": True, # run tests
        "print_result": True, # print result
        "traceback": True, # print traceback
        "prefix": "" # prefix for print
    }
}

keys = list(standart_cfg.keys())
settings_list = list(standart_cfg['settings'].keys())

def path_f():
    if not os.path.exists('build_cfg/backup'):
        os.mkdir('build_cfg/backup')
        
    path = f'build_cfg/backup/build_modules_backup.json'
    max_ = 0
    index = len('build_modules_backup_')
    for f in os.listdir('build_cfg/backup'):
        if f.startswith('build_modules_backup_'):
            
            try:
                if (num := int(f[index])) > max_:
                    max_ = num
            except:
                continue
            
    if max_ > 0:
        path = f'build_cfg/backup/build_modules_backup_{max_ + 1}.json'
    
    else:
        if os.path.exists('build_cfg/backup/build_modules_backup.json'): 
            path = f'build_cfg/backup/build_modules_backup_1.json'
        
    return path
    
def backup(string):
    print(string)
    path = path_f()
    try:
        if not os.path.exists('build_cfg/backup'):
            os.mkdir('build_cfg/backup')
        shutil.copyfile('build_cfg/build_modules.json', path)
    except:
        print("🔴 Failed to create backup file.")
    json.dump(standart_cfg, open('build_cfg/build_modules.json', 'w'))
    print('🟢 build_modules.json created.')
    print(f'# Backup file created: {path}')

def load():
    with open('build_cfg/build_modules.json') as f:
        cfg = json.load(f)
    return cfg

def check_cfg(cfg):
    for key in keys:
        if key not in cfg.keys():
            backup(f'🔴 {key} not found in "build_modules.json". Recreating...')
            return False
        
    for key in settings_list:
        if key not in cfg['settings'].keys():
            backup(f'🔴 {key} not found in "build_modules["settings"].json". Recreating...')
            return False
        
    return True

def load_cfg():
    if not cfg_file_exists():
        print('🔴 build_modules.json not found. Creating...')
        json.dump(standart_cfg, open('build_cfg/build_modules.json', 'w'))
    
    print('🟢 build_modules.json found.')
    
    try:
        cfg = load()
        if not check_cfg(cfg):
            cfg = load()
        
    except:
        backup('🔴 Failed to load build_modules.json. Recreating...')
        json.dump(standart_cfg, open('build_cfg/build_modules.json', 'w'))
        cfg = load()
    
    return cfg


def save_cfg(cfg):
    json.dump(cfg, open('build_cfg/build_modules.json', 'w'))

def cfg_file_exists():
    return os.path.exists('build_cfg/build_modules.json')