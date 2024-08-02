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