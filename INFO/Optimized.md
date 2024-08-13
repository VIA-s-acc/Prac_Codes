## Microsoft Visual C++ 14.0 or greater is required
Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Optimized Experimental
To use the optimized codes,create virtual environment, install all the dependencies and run the ~~`build.bat` ( for Windows )~~ **`[DELETED, use python script]`**[UPD 02.08.2024](../README.MD#update-02082024-info) `build.py` ( universal )  file from the `optimized` directory. The script will automatically build all the C libraries for you. All the codes will be available in this directory.

Alternatively, you can download the release from GitHub. 

## Overview optimiezed

Still in development. ([Last Update](../README.MD#last-update)), build and use the optimized codes in the `optimized` directory. 
(Modules ready to use [Ready](#ready)) 

The names of the functions and classes in the **NON OPTIMIZED PYTHON VERSION** are different from their counterparts after the build in the `optimized` version. Stay tuned for a table of content that includes all of them. For now, you can look at the `__init__.py` files in the respective directories and modules. For modules you can look at `optimized/lib_name/module_name/Module/*.py file`

also you can import raw functions from the `optimized/lib_name/module_name/build` directory. For functions names look at `optimized/lib_name/module_name/*.pyx` file.

Example: 
---
Python Interface:
- [lienq.class_names](../optimized/lineq/__init__.py) 
- [lineq.MatrixMethods.funcs](../optimized/lineq/matrix_methods/Module/module.py)

Raw import:
```py
from optimized.lineq.matrix_methods.build import determinant
``` 
( all functions names also in `optimized/lib_name/module_name/Module/*.py` file). Example - [lineq.MatrixMethods.funcs](../optimized/lineq/matrix_methods/Module/module.py) line 1:18
```py 
from ..build.matrix_methods import (
    determinant,
    sum_matrices_wrapper,
    multiply_matrix_by_scalar_wrapper,
    multiply_matrices_wrapper,
    sig,
    absolute,
    random,
    max_matrix,
    inv,
    LU,
    cholv1,
    cholv2,
    eigen,
    power_method,
    norm,
    vec_approx,
)
```
Functions names are `determinant`, `sum_matrices_wrapper`, `multiply_matrix_by_scalar_wrapper`, `multiply_matrices_wrapper`, `sig`, `absolute`, `random`, `max_matrix`, `inv`, `LU`, `cholv1`, `cholv2`, `eigen`, `power_method`, `norm`, `vec_approx`.



## Table of Content (OPTIMIZED)

Still in development. ([Last Update](../README.MD#last-update)), build and use the optimized codes in the `optimized` directory.

### Ready: 
-   [**Optimized.lineq.matrix_methods**](../optimized/lineq/matrix_methods/)
    -   [**Optimized.lineq.matrix_methods python interface**](../optimized/lineq/matrix_methods/Module/module.py)
-   [**Optimized.lineq.generator**](../optimized/lineq/generator/)
    -   [**Optimized.lineq.generator python interface**](../optimized/lineq/generator/Module/generator.py)
-   [**Optimized.lineq.checker**](../optimized/lineq/checker/)
    -   [**Optimized.lineq.checker python interface**](../optimized/lineq/checker/Module/checker.py)
---
### Api
---
Version - `API-v0.1A2`

To run api local host use `run_api.py` script. ( I will add CLI for API usage in future [CLI-API](#cli-api)) \
Check usage instructions in [API-DATA](../optimized/optimized_api/static/data.json) or just run [run_api.py](../run_api.py) and check home page.

---
#### Current Api Support:
Current version of API supports the following functions:
```py
determinant(matrix_a) -> double : Returns determinant of matrix_a 
sum_matrices(matrix_a, matrix_b) -> matrix : Returns sum of matrices  
multiply_matrix_by_scalar(matrix_a, scalar) -> matrix : Returns multiplied matrix 
multiply_matrices(matrix_a, matrix_b) -> matrix : Returns multiplied matrix  
sig(x) -> int : Returns -1 if x < 0, 0 if x == 0, 1 if x > 0 
absolute(x) -> double : Returns absolute value of number 
random(min, max) -> double : Returns random number in range (min, max) 
max_matrix(matrix_a) -> double : Returns max value in matrix 
inverse(matrix_a) -> matrix : Returns inverted matrix 
LU(matrix_a) -> tuple[matrix, matrix] : Returns LU decomposition 
cholv1(matrix_a) -> tuple[matrix, matrix] : Returns cholesky decomposition 
cholv2(matrix_a) -> tuple[matrix, matrix, matrix] : Returns cholesky decomposition 
eigen(matrix_a, max_iter, tol) -> tuple[tuple[double, vector], tuple[double, vector]] : Returns eigenvalues and eigenvectors (max, min) 

```
---
#### CLI-API:

still in development
