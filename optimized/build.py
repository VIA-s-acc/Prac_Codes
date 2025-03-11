from build_cfg.Utils.print_tree import res_print
from build_cfg.Utils.check import check_cython, check_setuptools
from build_cfg.Utils.load import load_cfg, save_cfg
from build_cfg.Utils.build import build
from build_cfg.Utils.test import run_tests
from build_cfg.Utils.create_new import create_module
from build_cfg.Utils.download_cfg import download
import traceback
import argparse
import os
### RUN THIS SCRIPT FROM ROOT.OPTIMIZED FOLDER ###


def parse():
    parser = argparse.ArgumentParser(
        description="Build and manage modules in the project."
    )

    parser.add_argument(
        '--modules', '-m',
        nargs='*',
        required=False,
        default=['all'],
        help="Specify the modules to build. Use 'all' to build everything."
    )

    parser.add_argument(
        '--create', '-c',
        nargs='+',
        required=False,
        help="Create new modules. Format: module.submodule (e.g., utils.parser)."
    )
    parser.add_argument(
        '--reset', '-r',
        action='store_true',
        help="Reset the build configuration."
    )
    
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        required=False,
        help="Test modules (all if not specified by -m (--modules) )."
    )
    
    
    
    args = parser.parse_args()

    return args
    
def main():
    
    """
    Main entry point of the script. Parses the command line arguments, loads the
    configuration, and either creates new modules, builds and tests existing ones, or
    resets the configuration.

    -   If --reset is specified, the configuration is reset and the script exits.
    -   If --create is specified, new modules are created and the script prompts the user to build them.
    -   If --modules is specified, the script builds and tests the specified modules.
    -   If --modules is not specified, the script builds and tests all modules.

    If an error occurs during the build or test process, the script prints the
    error message and exits.
    """
    args = parse()
        
    
    if args.reset:
        reset_configuration()
        return
    
    cfg = load_cfg()
    settings = cfg['settings']
    
    if args.test:
        print("🟢 Testing...")
        modules = select_modules(args.modules, cfg)
        test_libs = [lib for lib in modules.keys()]
        run_tests(cfg['settings'], test_libs, modules)
        return
    
    if args.create:
        modules = handle_module_creation(args.create, cfg)
        if not prompt_for_build():
            return
    else:
        modules = select_modules(args.modules, cfg)
    
    try:
        check_dependencies(settings)
        handle_missing_modules(modules, settings)
        
        libs, failed = build(modules, settings)
        test_libs = [lib for lib in libs if lib not in failed]
        
        run_tests(settings, test_libs, modules)
        res_print(settings, modules, libs, failed)

    except Exception as e:
        handle_error(e, settings)


def reset_configuration():
    """Reset the configuration file and download fresh defaults."""
    print("\n🟢 Resetting configuration...")
    config_path = 'build_cfg/build_modules.json'
    if os.path.exists(config_path):
        os.remove(config_path)
    download()
    print("🟢 Configuration reset.")


def handle_module_creation(module_names, cfg):
    """Create new modules and update configuration."""
    print(f"\n🟢 Creating modules: {module_names}")
    modules = cfg['modules']
    
    for module_name in module_names:
        module, submodule = module_name.split('.', 1)
        
        # Ensure module exists in config
        if module not in modules:
            modules[module] = []
            
        # Add submodule if not already present
        if submodule not in modules[module]:
            modules[module].append(submodule)
            
        create_module(module, submodule)
    
    save_cfg(cfg)
    print('\n🟢 Modules created.\n')
    return modules


def prompt_for_build():
    """Ask user if they want to proceed with building."""
    return input("🟢 run build? (Y/N):\t").lower() == 'y'


def select_modules(module_args, cfg):
    """Determine which modules to build based on command line arguments."""
    print(f"\n🟢 Selected modules: {module_args}")
    if len(module_args) == 0:
        module_args = ['all']
    if module_args[0] == 'all':
        return cfg['modules']
    all_modules = cfg['modules']
    modules = {}
    for module_name in module_args:
        try:
            module, submodule = module_name.split('.', 1)
        except ValueError:
            module = module_name
            if module in list(all_modules.keys()):
                submodules = all_modules[module_name]
                print(f"\n🟡 Submodules for {module} not specified - taking from configuration.\n\tSubmodules: {submodules}")
                for submodule in submodules:
                    if module not in modules:
                        modules[module] = []
                    if submodule not in modules[module]:
                        modules[module].append(submodule)
            else:
                print(f"\n🟡 Module {module_name} does not exist. Skipping...")
            continue
        except Exception as e:
            handle_error(e, cfg['settings'])
        
        if module not in modules:
            modules[module] = []
        if submodule not in modules[module]:
            modules[module].append(submodule)
    return modules


def check_dependencies(settings):
    """Verify that required dependencies are installed."""
    check_cython(settings)
    check_setuptools(settings)


def handle_missing_modules(modules, settings):
    """Create missing modules if enabled in settings."""
    create_if_missing = settings.get("create_if_not_exist", False)
    
    for module_name, submodules in modules.items():
        for submodule in submodules:
            module_path = f"{module_name}/{submodule}"
            
            if not os.path.exists(module_path):
                if create_if_missing:
                    print(f"\n🟢 Module {module_name}.{submodule} does not exist. Creating base module...")
                    create_module(module_name, submodule)
                else:
                    print(f"\n🟡 Module {module_name}.{submodule} does not exist. "
                            f"Skipping (create_if_not_exist = False).")


def handle_error(error, settings):
    """Handle exceptions with optional traceback."""
    print("Error: " + str(error))
    if settings.get('traceback', False):
        traceback.print_exc()

            
if __name__ == '__main__':
    main() # run main


