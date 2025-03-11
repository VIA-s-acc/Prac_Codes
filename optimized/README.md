## Repository: [GitHub - Builder](https://github.com/VIA-s-acc/builder/tree/main)

### System Requirements

#### Windows Requirements
- **Microsoft Visual C++ 14.0 or greater** is required.  
  You can download the required version through the [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

#### Global Requirements
- **Python 3.10 or greater** must be installed.

---

### Build Process

The `build.py` script automates the creation and building of C-based Python libraries. Here's how to set it up and use it.

#### Configuration File

A configuration file must be created at `build_cfg/build_modules.json` in the root directory. Below is an example configuration structure:

```json
{
  "modules": {
    "TestLib1": ["TestMod1_1", "TestMod1_2"],
    "TestLib2": ["TestMod2_1", "TestMod2_2"]
  },
  "settings": {
    "check_cython": true,
    "check_setuptools": true,
    "create_if_not_exist": false,
    "run_tests": true,
    "print_result": true,
    "traceback": true,
    "prefix": ""
  }
}
```

#### Explanation:
- **modules**: A dictionary defining the libraries and the modules to build.  
  Example: 
  ```json
  "modules": {
    "TestLib1": ["TestMod1_1", "TestMod1_2"],
    "TestLib2": ["TestMod2_1", "TestMod2_2"]
  }
  ```

- **settings**: Configuration for the build process:
  - `check_cython`: Checks if Cython is installed.
  - `check_setuptools`: Checks if setuptools is installed.
  - `create_if_not_exist`: Create missing modules and submodules if they don't exist.
  - `run_tests`: Runs tests after building.
  - `print_result`: Displays the build results.
  - `auto_import`: auto-imports functions detected in the `.pyx` file to `Module.submodule.py` as `raw_func_name` after building also auto-creating functions for class `module` if class exists. 

>[!Note]
>(as 1 line, be careful not to lose anything in this line during the build).

  - Example:
      - `.pyx` file: 
        ```python
          #==========================================================
          # BASE PYX TEMPLATE
          #==========================================================

          from libc.stdlib cimport malloc, free

          cdef extern from "lowlevel/modules_Funcs_c.h" nogil:
              int basic_function()

          def call_basic_function():
              return basic_function()


          def test_2_func(test):
              return "test_2_func"

          def test_3_func():
              return "test_3_func"
          ```
        - auto created `Module.submodule.py`:
          ```python
          from ..build.Funcs import (call_basic_function as raw_call_basic_function, test_2_func as raw_test_2_func, test_3_func as raw_test_3_func)
          # BASE MODULE TEMPLATE
          #==========================================================

          from ..build.Funcs import (
              call_basic_function as raw_basic_function
          )

          class FuncsModule:
            def __init__(self):
                pass


            def test_2_func(self, *params):
                return raw_test_2_func(*params)

            def test_3_func(self, *params):
                return raw_test_3_func(*params)
            def call_basic_function(self):
                return raw_basic_function()

            def sample_function():
                instance = FuncsModule()
                instance.call_basic_function()
                return "basic_function worked."
        ```
  - `traceback`: Displays traceback in case of errors.
  - `prefix`: Prefix for the build process.

---

### Command-Line Interface (CLI)

Navigate to the `Main_Codes` directory and run the `build.py` script to manage your modules.

#### Usage:

```bash
usage: build.py [-h] [--modules MODULES [MODULES ...]] [--create CREATE [CREATE ...]] [--reset] [--test]
```

**Options:**
- `-h`, `--help`: Show help message.
- `--modules MODULES [MODULES ...]`, `-m MODULES [MODULES ...]`: Specify which modules to build. Use `'all'` to build everything.
- `--create CREATE [CREATE ...]`, `-c CREATE [CREATE ...]`: Create new modules in the format `module.submodule` (e.g., `utils.parser`).
- `--reset`, `-r`: Reset the build configuration.
- `--test`, `-t`: Test modules (all if not specified by -m (--modules) ).

---

### Build and Create Modules

#### Syntax for `build.py -c` (Create Modules):

```bash
build.py -c module1.submodule1 module1.submodule2 module2.submodule2
```

- This command will create new modules template and add them to the build configuration.
>[!Note]
> IF YOU DELETED BASE_FUNCTION AFTER CREATING BY TEMPLATE, REMOVE IMPORTS FROM `module.submodule.Module.submodule.py`.
- If the module or submodule doesn't exist, it will be created and added.
- If a submodule exists, you’ll be prompted to recreate it.

#### Example Directory Structure After Creation:

```
Main_Codes/
  ├── module1/
  │   ├── submodule1/
  │   │   ├── lowlevel/
  │   │   │   ├── module1_submodule1_c.c
  │   │   │   └── module1_submodule1_c.h
  │   │   ├── Module
  │   │   │   └── submodule.py
  │   │   ├── __init__.py
  │   │   ├── setup.py
  │   │   ├── submodule.pyx
  │   │   └── TEST/
  │   │       └── test.py
  │   ├── submodule2/
  │   │   ├── __init__.py
  │   │   ├── build.py
  │   │   ├── setup.py
  │   │   └── ...
  ├── module2/
  │   ├── submodule1/
  │   └── ...
  └── ...
```

- Each submodule will have the corresponding `.pyx` and C files along with test files in the `TEST/` directory.

---

### Building the Modules

#### Syntax for `build.py -m` (Build Modules):

```bash
build.py -m module1.submodule1 module1.submodule2 module2.submodule2
```

- This command builds the specified modules and submodules.

---

### Templates

#### `s.pyx` Template (for Submodules):
```py
#==========================================================
# BASE PYX TEMPLATE
#==========================================================

from libc.stdlib cimport malloc, free

cdef extern from "lowlevel/{m}_{s}_c.h" nogil:
    int basic_function()

def call_basic_function():
    return basic_function()
```

#### `m_s_c.c` Template (C Code):
```c
/*==========================================================
BASE C TEMPLATE
==========================================================*/
#include "{m}_{s}_c.h"

int basic_function() {{
    return 1;
}}
```

#### `m_s_c.h` Template (C Header):
```h
/*==========================================================
BASE HEADER TEMPLATE
==========================================================*/
#ifndef {s.upper()}_H
#define {s.upper()}_H

int basic_function();

#endif // {s.upper()}_H
```

#### `setup.py` Template:
```py
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['{m}/{s}/{s}.pyx', '{m}/{s}/lowlevel/{m}_{s}_c.c']

ext_modules = [
    Extension("{s}", 
              sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3str"} 

setup(name = '{s}',
      cmdclass={'build_ext': build_ext},
      ext_modules=ext_modules
      )
```

#### `__init__.py` Template:
```py
from .Module.Funcs import *
```

#### Module Template (`s.py`):
```py
#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.{s} import (
    call_basic_function
)

class {s.capitalize()}Module:
    def __init__(self):
        pass

    def basic_function(self):
        return call_basic_function()

def sample_function():
    instance = {s.capitalize()}Module()
    instance.basic_function()
    return "basic_function worked."
```
