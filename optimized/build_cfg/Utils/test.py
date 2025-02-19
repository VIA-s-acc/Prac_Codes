import sys, subprocess, os
def run_tests(settings, libs, modules):
    if len(libs) > 0:
        if settings['run_tests']:  
            print('\nRUNNING GLOBAL TESTS\n')
            
            ##Global TESTS
            for lib in libs:        
                if os.path.exists(f'{lib}/TEST/test.pyc'):
                    os.remove(f'{lib}/TEST/test.pyc')
        
                print(f"Testing {lib}...")
                try:
                    subprocess.check_call([sys.executable, '-m', f'{lib}.TEST.test'])
                except Exception as ex:
                    print(f'🔴 {lib} TESTS FAILED, ERROR: {ex}')
                    
            ##Module TESTS
            print('\nRUNNING MODULE TESTS\n')
            for lib in libs:
                for module in modules[lib]:
                    if os.path.exists(f'{lib}/{module}/test.pyc'):
                        os.remove(f'{lib}/{module}/test.pyc')
                    print(f"Testing {lib}/{module}...")
                    try:
                        subprocess.check_call([sys.executable, '-m', f'{lib}.{module}.TEST.test'])
                    except Exception as ex:
                        print(f'🔴 {module} TESTS FAILED, ERROR: {ex}')
                    
            
        else:
            print('🛑 TESTS SKIPPED ( settings["run_tests"] = false ) \n')



