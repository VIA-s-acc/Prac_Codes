import os
import shutil
from .temp.create_temp import setup, template_pyx, template_h, template_c, template_module




def recreate_or_create(module_name, submodule_name):
    """
    Create a new directory structure for a module/submodule or recreate it if it already exists.
    
    Args:
        module_name (str): Name of the parent module
        submodule_name (str): Name of the submodule
        
    Returns:
        int: 0 if successful, -1 if there was a permission error
    """
    path = os.path.join(module_name, submodule_name)
    subdirs = ["TEST", "Module", "lowlevel"]
    
    if os.path.exists(path):
        if not os.access(path, os.W_OK):
            print(f"🔴 {module_name}.{submodule_name} is not writable")
            return -1
            
        shutil.rmtree(path)
    
    os.makedirs(path, exist_ok=True)
    
    for subdir in subdirs:
        os.makedirs(os.path.join(path, subdir), exist_ok=True)
        
    return 0


def create_module(module_name, submodule_name):
    """
    Create a new module structure with the given module and submodule names.
    
    Args:
        module_name (str): The name of the parent module
        submodule_name (str): The name of the submodule to create
    
    Returns:
        bool: True if module was created successfully, False otherwise
    """
    if os.path.exists(f"{module_name}/{submodule_name}"):
        response = input(f"\n🔴 {module_name}.{submodule_name} already exists (You want to overwrite it? (Y/N)): \t")
        if response.lower() != 'y':
            return False
    
    if not os.path.exists(module_name):
        os.makedirs(f"{module_name}/TEST", exist_ok=True)
        _create_global_test_file(module_name)
    
    _update_test_imports(f"{module_name}/TEST/test.py", f"from ..{submodule_name}.Module.{submodule_name} import *\n")
    
    if recreate_or_create(module_name, submodule_name) == -1:
        print(f"\n🔴 {module_name}.{submodule_name} cannot be created | check access")
        return False
    
    _create_submodule_files(module_name, submodule_name)
    
    _create_submodule_test_file(module_name, submodule_name)
    
    _update_module_imports(module_name, submodule_name)
    
    print(f"\n🟢 {module_name}.{submodule_name} created successfully")
    return True

def _create_global_test_file(module_name):
    """Create the global test file for a module."""
    with open(f"{module_name}/TEST/test.py", 'w') as f:
        f.write(f'''#==========================================================
# WRITE YOUR GLOBAL {module_name} TESTS HERE
# ==========================================================\n''')

def _update_test_imports(test_file_path, import_statement):
    """Update test file with import statement if not already present."""
    if not os.path.exists(test_file_path):
        return
        
    with open(test_file_path, 'r') as f:
        lines = f.readlines()
    
    if import_statement not in lines:
        with open(test_file_path, 'a') as f:
            f.write(import_statement)

def _create_submodule_files(module_name, submodule_name):
    """Create all necessary files for the submodule."""
    file_templates = {
        f"{module_name}/{submodule_name}/Module/{submodule_name}.py": template_module(module_name, submodule_name),
        f"{module_name}/{submodule_name}/{submodule_name}.pyx": template_pyx(module_name, submodule_name),
        f"{module_name}/{submodule_name}/lowlevel/{module_name}_{submodule_name}_c.h": template_h(module_name, submodule_name),
        f"{module_name}/{submodule_name}/lowlevel/{module_name}_{submodule_name}_c.c": template_c(module_name, submodule_name),
        f"{module_name}/{submodule_name}/setup.py": setup(module_name, submodule_name),
        f"{module_name}/{submodule_name}/__init__.py": f"from .Module.{submodule_name} import *"
    }
    
    for file_path, content in file_templates.items():
        with open(file_path, 'w') as f:
            f.write(content)

def _create_submodule_test_file(module_name, submodule_name):
    """Create and initialize the test file for the submodule."""
    test_file = f"{module_name}/{submodule_name}/TEST/test.py"
    
    with open(test_file, "w") as f:
        f.write(f'''#==========================================================
# WRITE YOUR {module_name}.{submodule_name} TESTS HERE
# ==========================================================\n''')
    
    _update_test_imports(test_file, f"from ..Module.{submodule_name} import *\n")

def _update_module_imports(module_name, submodule_name):
    """Update the parent module's __init__.py with imports for the new submodule."""
    init_file = f"{module_name}/__init__.py"
    import_statement = f"from .{submodule_name}.Module.{submodule_name} import *\n"
    
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write(import_statement)
    else:
        _update_test_imports(init_file, import_statement)
