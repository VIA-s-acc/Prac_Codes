import os
import shutil
from .temp.create_temp import setup, template_pyx, template_h, template_c, template_module




def recreate_or_create(m, s):
    if os.path.exists(f"{m}/{s}"):
        if os.access(f"{m}/{s}", os.W_OK):
            shutil.rmtree(f"{m}/{s}")
            os.mkdir(f"{m}/{s}")
            os.mkdir(f"{m}/{s}/TEST")
            os.mkdir(f"{m}/{s}/Module")
            os.mkdir(f"{m}/{s}/lowlevel")
        else:
            print(f"🔴 {m}.{s} is not writable")
            return -1
    else:
        os.mkdir(f"{m}/{s}")
        os.mkdir(f"{m}/{s}/TEST")
        os.mkdir(f"{m}/{s}/Module")
        os.mkdir(f"{m}/{s}/lowlevel")
    return 0

def create_module(m, s):
    
    if os.path.exists(f"{m}/{s}"): 
        resp = input(f"\n🔴 {m}.{s} already exists (You want to overwrite it? (Y/N)): \t")
        if resp == 'y':
            pass
        else:
            return
    
    
    if not os.path.exists(m):
        os.mkdir(m)
        os.mkdir(f"{m}/TEST")
        with open(f"{m}/TEST/test.py", 'w') as f:
            f.write(f'''#==========================================================
# WRITE YOUR GLOBAL {m} TESTS HERE
# ==========================================================''')
            f.close()
        
    res = recreate_or_create(m, s)
    if res == -1:
        print(f"\n🔴 {m}.{s} cannot be created | check access")
        return
    
    with open(f"{m}/{s}/Module/{s}.py", 'w') as f:
        f.write(template_module(m, s)) 
    with open(f"{m}/{s}/{s}.pyx", 'w') as f:
        f.write(template_pyx(m, s))
    with open(f"{m}/{s}/lowlevel/{s}.h", 'w') as f:
        f.write(template_h(m, s))  
    with open(f"{m}/{s}/lowlevel/{s}.c", 'w') as f:
        f.write(template_c(m, s))


    with open(f"{m}/{s}/setup.py", 'w') as f:
        f.write(setup(m, s))
        f.close()
    with open(f"{m}/{s}/__init__.py", 'w') as f:
        f.write(f"from .Module.{s} import *")
        f.close()
    with open(f"{m}/{s}/TEST/test.py", "w") as f:
        f.write(f'''#==========================================================
# WRITE YOUR {m}.{s} TESTS HERE
# ==========================================================''')
        f.close()
        
    print(f"\n🟢 {m}.{s} created successfully")
    
    
        
    
    