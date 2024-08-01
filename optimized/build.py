import os
import sys
import subprocess
import shutil

try:
    import Cython
except ImportError:
    print("Cython not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Cython"])

modules = ['matrix_methods', 'generator', 'checker']

for module in modules:
    if os.path.exists(f'lineq/{module}/build'):
        shutil.rmtree(f'lineq/{module}/build')
    if os.path.exists(f'lineq/{module}/lowlevel/{module}.c'):
        os.remove(f'lineq/{module}/lowlevel/{module}.c')
    subprocess.check_call([sys.executable, f'lineq/{module}/setup.py', 'build_ext', '-b', 'build'])
    shutil.move('build', f'lineq/{module}/build')
    shutil.move(f'lineq/{module}/{module}.c', f'lineq/{module}/lowlevel/{module}.c')
