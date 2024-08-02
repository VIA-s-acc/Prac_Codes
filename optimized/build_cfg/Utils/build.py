import sys, os, subprocess, shutil, traceback
def build(modules, settings, failed = {}):
    libs = list(modules.keys())
    for lib in libs:
        for module in modules[lib]:
            try:
                if os.path.exists(f'{lib}/{module}/build'):
                    shutil.rmtree(f'{lib}/{module}/build')
                if os.path.exists(f'{lib}/{module}/lowlevel/{module}.c'):
                    os.remove(f'{lib}/{module}/lowlevel/{module}.c')
                subprocess.check_call([sys.executable, f'{lib}/{module}/setup.py', 'build_ext', '-b', 'build'])
                shutil.move('build', f'{lib}/{module}/build')
                shutil.move(f'{lib}/{module}/{module}.c', f'{lib}/{module}/lowlevel/{module}.c')
                print(f'🟢 {lib}/{module} builded')
            except Exception as ex:
                print(f'🔴 {lib}/{module} build failed, ERROR: {ex}')
                if settings['traceback']:
                    print("\n-----ERROR TRACEBACK-----\n")
                    traceback.print_exc()
                    print("\n-------------------------\n")
                try:
                    failed[lib].append(module)
                except:
                    failed = {lib: [module]}
                pass           
        
    return libs, failed