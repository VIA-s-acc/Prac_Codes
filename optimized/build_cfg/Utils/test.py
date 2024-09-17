import sys, subprocess, os
def run_tests(settings, libs):
    if len(libs) > 0:
        if settings['run_tests']:  
            print('\nRUNNING TESTS\n')
            for lib in libs:        
                if os.path.exists(f'{lib}/TEST/test.pyc'):
                    os.remove(f'{lib}/TEST/test.pyc')
        
                print(f"Testing {lib}...")
                try:
                    subprocess.check_call([sys.executable, '-m', f'{lib}.TEST.test'])
                except Exception as ex:
                    print(f'🔴 {lib} TESTS FAILED, ERROR: {ex}')
        else:
            print('🛑 TESTS SKIPPED ( settings["run_tests"] = false ) \n')



