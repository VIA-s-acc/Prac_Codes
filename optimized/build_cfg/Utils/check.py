import sys, subprocess
def check_cython(settings):
    if settings['check_cython']:
        try:
            import Cython
            print("🟢 Cython found.")
        except ImportError:
            print("🔴 Cython not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Cython"])
            print("🟢 Cython installed.")


def check_setuptools(settings):
    if settings['check_setuptools']:
        try:
            import setuptools
            print("🟢 Setuptools found.")
        except ImportError:
            print("🔴 Setuptools not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
            print("🟢 Setuptools installed.")