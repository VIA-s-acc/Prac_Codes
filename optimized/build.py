from build_cfg.Utils.print_tree import res_print
from build_cfg.Utils.check import check_cython, check_setuptools
from build_cfg.Utils.load import load_cfg
from build_cfg.Utils.build import build
from build_cfg.Utils.test import run_tests
import copy
import traceback
import argparse

### RUN THIS SCRIPT FROM ROOT.OPTIMIZED FOLDER ###


def parse():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--modules', '-m', nargs='+', required=False, default='default')
    args = parser.parse_args()

    return args
    
def main():
    """
    This function is the main entry point of the program. It performs the following steps:
    1. Loads the configuration from the file using the `load_cfg()` function.
    2. Retrieves the settings from the loaded configuration.
    3. Retrieves the modules from the loaded configuration.
    4. Checks the installation of Cython using the `check_cython()` function. Checks the installation of setuptools using the `check_setuptools()` function.
    5. Builds the modules using the `build()` function.
    6. Runs the tests using the `run_tests()` function.
    7. Prints the result using the `res_print()` function.
    """

    args = parse()
    cfg = load_cfg() # load config
    settings = cfg['settings'] # get settings
    if args.modules == 'default' or args.modules[0] == 'all':
        modules = cfg['modules'] # get modules
    else:
        modules = {}
        for module in args.modules:
            m, s = module.split('.', 1)
            if m not in modules:
                modules[m] = []
            modules[m].append(s)
    try:
        check_cython(settings) # check cython installation
        check_setuptools(settings)
        libs, failed = build(modules, settings) # build modules
        test_libs = copy.copy(libs)
        for lib in libs:
            if lib in failed.keys():
                print(f"\n🔴 {lib} build failed, cant run {lib}.TEST.test | SKIPPED.") 
                test_libs.remove(lib) # remove failed libs from test
        run_tests(settings, test_libs) # run tests 
        res_print(settings, modules, libs, failed) # print result

    except Exception as e:
        print("Error: " + str(e))
        if settings['traceback']:
            traceback.print_exc()
            
if __name__ == '__main__':
    main() # run main


