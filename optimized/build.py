from build_cfg.Utils.print_tree import res_print
from build_cfg.Utils.check import check_cython, check_setuptools
from build_cfg.Utils.load import load_cfg, save_cfg
from build_cfg.Utils.build import build
from build_cfg.Utils.test import run_tests
from build_cfg.Utils.create_new import create_module
from build_cfg.Utils.download_cfg import download
import copy
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
        nargs='+',
        required=False,
        default='default',
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
    
    args = parser.parse_args()

    return args
    
def main():
    """
    Main entry point of the program that handles configuration management,
    module creation, building, and testing.
    """
    args = parse()
    
    if args.reset:
        reset_configuration()
        return
    
    cfg = load_cfg()
    settings = cfg['settings']
    
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
    if module_args == 'default' or module_args[0] == 'all':
        return cfg['modules']
    
    modules = {}
    for module_name in module_args:
        module, submodule = module_name.split('.', 1)
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
                    print(f"\n🔴 Module {module_name}.{submodule} does not exist. "
                            f"Skipping (create_if_not_exist = False).")


def handle_error(error, settings):
    """Handle exceptions with optional traceback."""
    print("Error: " + str(error))
    if settings.get('traceback', False):
        traceback.print_exc()

            
if __name__ == '__main__':
    main() # run main


