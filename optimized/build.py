import os
import sys
import subprocess
import shutil

try:
    import Cython
except ImportError:
    print("Cython not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Cython"])


libs = ['lineq']
modules = {'lineq': ['matrix_methods', 'generator', 'checker']}
for lib in libs:
    for module in modules[lib]:
        if os.path.exists(f'{lib}/{module}/build'):
            shutil.rmtree(f'{lib}/{module}/build')
        if os.path.exists(f'{lib}/{module}/lowlevel/{module}.c'):
            os.remove(f'{lib}/{module}/lowlevel/{module}.c')
        subprocess.check_call([sys.executable, f'{lib}/{module}/setup.py', 'build_ext', '-b', 'build'])
        shutil.move('build', f'{lib}/{module}/build')
        shutil.move(f'{lib}/{module}/{module}.c', f'{lib}/{module}/lowlevel/{module}.c')
        
print('\n\n\nBUILD DONE\nRUNNING TESTS\n\n\n')
for lib in libs:        
    if os.path.exists('{lib}/TEST/test.pyc'):
        os.remove('{lib}/TEST/test.pyc')
   
    print(f"Testing {lib}...")
    subprocess.check_call([sys.executable, '-m', f'{lib}.TEST.test'])
