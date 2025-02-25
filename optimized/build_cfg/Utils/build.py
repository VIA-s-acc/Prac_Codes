import sys, os, subprocess, shutil, traceback, re
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
                if settings['auto_import']:
                    print(f"Adding imports to {lib}/{module}...")
                    import re
                    with open(f"{lib}/{module}/{module}.pyx", "r") as file:
                        content = file.read()
                    function_names = re.findall(r"def\s+(\w+)\(", content)
                    import_line = f"from ..build.{module} import ({', '.join([f'{name} as raw_{name}' for name in function_names])})\n"

                    with open(f'{lib}/{module}/Module/{module}.py', 'r') as f:
                        lines = f.readlines()

                    lines[0] = import_line

                    with open(f'{lib}/{module}/Module/{module}.py', 'w') as f:
                        f.writelines(lines)
                        
                    with open(f'{lib}/{module}/Module/{module}.py', 'r') as f:
                        lines = f.readlines()
                    class_name = f"{module}Module"
                    class_index = None
                    class_pattern = r"\bclass\s+(" + re.escape(class_name) + r")\b"

# Поиск строки с классом
                    for i, line in enumerate(lines):
                        if re.search(class_pattern, line):  # Ищем точное совпадение класса
                            class_index = i
                            break
                    if class_index is not None:
                        init_index = None
                        init_end_index = None
                        for i, line in enumerate(lines):
                            if "__init__" in line:
                                init_index = i
        
                                for j in range(i + 1, len(lines)):

                                    if lines[j].startswith("    "):  
                                        continue

                                    elif lines[j].strip() == "":  
                                        init_end_index = j + 1  
                                        break
                                    else:
                                        init_end_index = j 
                                        break
                                break


                        existing_methods = [line.strip().split('(')[0].split(' ')[1] for line in lines if 'def ' in line]

                        if init_index is not None and init_end_index is not None:
                            new_methods = []
                            for name in function_names:
                                if name not in existing_methods: 
                                    new_methods.append(f"\n    def {name}(self, *params):\n        return raw_{name}(*params)\n")
                            

                            lines.insert(init_end_index, ''.join(new_methods))

                            with open(f'{lib}/{module}/Module/{module}.py', 'w') as f:
                                f.writelines(lines)
                            
                    print(f'🟢 {lib}/{module} imports and methods added')
                    
                    
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