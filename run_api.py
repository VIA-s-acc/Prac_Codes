import subprocess, sys

subprocess.check_call([sys.executable, "-m", "optimized.optimized_api.app"] + sys.argv[1:])

