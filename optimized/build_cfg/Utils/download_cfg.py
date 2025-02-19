
import os, sys, subprocess, urllib.request

def check_config_parser():
    try:
        import configparser
        print("🟢 ConfigParser found.")
    except:
        print("🔴 ConfigParser not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "configparser"])
        print("🟢 ConfigParser installed.")

def check_tqdm():
    try:
        import tqdm
        print("🟢 TQDM found.")
    except:
        print("🔴 TQDM not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
        print("🟢 TQDM installed.")

def download():
    check_config_parser()
    import tqdm
    with open('build_cfg/build_modules.json', 'wb') as f:
        with urllib.request.urlopen('https://raw.githubusercontent.com/VIA-s-acc/builder/main/build_cfg/build_modules.json') as response:
            total_size = int(response.headers.get('content-length', 0))
            print(f"Downloading {total_size} bytes")
            block_size = 1024
            pbar = tqdm.tqdm(total=total_size, unit="Bytes", unit_scale=True, unit_divisor=block_size, leave=False)
            while True:
                data = response.read(block_size)
                import time 
                if not data:
                    break
                pbar.update(len(data))
                f.write(data)
            time.sleep(0.1)
            pbar.update(0)
    print("\n🟢  downloaded.")
