from build_cfg.Utils.print_tree import res_print
from build_cfg.Utils.check import check_cython
from build_cfg.Utils.load import load_cfg
from build_cfg.Utils.build import build
from build_cfg.Utils.test import run_tests
import copy
import traceback


def main():
    """
    This function is the main entry point of the program. It performs the following steps:
    1. Loads the configuration from the file using the `load_cfg()` function.
    2. Retrieves the settings from the loaded configuration.
    3. Retrieves the modules from the loaded configuration.
    4. Checks the installation of Cython using the `check_cython()` function.
    5. Builds the modules using the `build()` function.
    6. Runs the tests using the `run_tests()` function.
    7. Prints the result using the `res_print()` function.
    """
    cfg = load_cfg() # load config
    settings = cfg['settings'] # get settings
    modules = cfg['modules'] # get modules
    try:
        check_cython(settings) # check cython installation
        libs, failed = build(modules, settings) # build modules
        test_libs = copy.copy(libs)
        for lib in libs:
            if lib in failed.keys():
                print(f"\n🔴 {lib} build failed, cant run {lib}.TEST.test | SKIPPED.") 
                test_libs.remove(lib) # remove failed libs from test
        run_tests(settings, test_libs) # run tests 
        res_print(settings, modules, libs, failed) # print result
        if len(list(failed.keys())) > 0:
            print("\n🔴 Some libraries failed to build. Do not use them.\nFailed: {}".format(failed)) 
    except Exception as e:
        print("Error: " + str(e))
        if settings['traceback']:
            traceback.print_exc()
            
if __name__ == '__main__':
    main() # run main


