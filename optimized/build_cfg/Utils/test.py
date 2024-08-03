import sys, subprocess, os
def run_tests(settings, libs):
    if len(libs) > 0:
        if settings['run_tests']:  
            print('\nRUNNING TESTS\n')
            for lib in libs:        
                if os.path.exists('{lib}/TEST/test.pyc'):
                    os.remove('{lib}/TEST/test.pyc')
        
                print(f"Testing {lib}...")
                subprocess.check_call([sys.executable, '-m', f'{lib}.TEST.test'])
    
        else:
            print('🛑 TESTS SKIPPED ( settings["run_tests"] = false ) \n')



