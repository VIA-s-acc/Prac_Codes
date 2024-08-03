import pprint
def check_lib_failed(lib, failed):
    return lib in failed.keys()

def check_module_failed(lib, module, failed):
    if check_lib_failed(lib, failed):
        return module in failed[lib]
    return False

def print_tree_structure(libs, modules, prefix="", failed={}):
    def print_branch(items, prefix=prefix, parent_lib=None):
        for i, item in enumerate(items):
            # Determine if the current item is a library or module and its status
            if parent_lib is None:  # It's a library
                icon = "🔴" if check_lib_failed(item, failed) else "🟢"
            else:  # It's a module
                icon = "🔴" if check_module_failed(parent_lib, item, failed) else "🟢"

            if i == len(items) - 1:
                print(f"{prefix}└── {item}/ {icon}")
                if isinstance(modules.get(item), list):
                    print_branch(modules[item], prefix + "    ", parent_lib=item)
            else:
                print(f"{prefix}├── {item}/ {icon}")
                if isinstance(modules.get(item), list):
                    print_branch(modules[item], prefix + "│   ", parent_lib=item)
    
    res = "🟢"
    for lib in libs:
        if lib in failed.keys():
            res = "🔴"
    
    print("\nbuilder result:\n")
    print(f"builded_libs {res}")
    print_branch(libs)
    if res == "🔴":
        print("\n🔴 Some libraries failed to build. Do not use them.\n")
        pprint.pprint([
            'Failed_libs', failed
            ], indent=2, width=50)
    else:
        print("\n🟢 Build Done")
    
def res_print(settings, modules, libs, failed):
    if settings['print_result']:   
        print_tree_structure(libs, modules, prefix = settings['prefix'], failed = failed)
    else:
        print("🟢 Build Done")
