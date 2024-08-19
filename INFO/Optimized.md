## Microsoft Visual C++ 14.0 or greater is required in Windows
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

[optimized.lineq.matrix_methods.python_interface](../optimized/lineq/matrix_methods/Module/module.py) 
---
| function | args | description | use_pattern | example |
| :------- | :-- | :---------: | :---------- | :------ | 
| determinant   | type: type of input <br> matrix: matrix | Returns determinant of matrix | link_to_api/det/?type=type&matrix=matrix ( list or str ). | example_str: link_to_api/det/?matrix=1 2 3\n4 5 6\n7 8 9, <br> example_list: link_to_api/det/?type=list&matrix=[[1,2,3],[4,5,6],[7,8,9]] |
| sum_matrices | type: type of input <br> matrix1: matrix1 <br> matrix2: matrix2 |  Returns sum of matrices  | link_to_api/sum_m/?type=type&matrix1=matrix1&matrix2=matrix2 ( list or str ) | example_str: link_to_api/sum_m/?matrix1=1 2 3\n4 5 6\n7 8 9, <br> example_list: link_to_api/sum_m/?type=list&matrix1=[[2,2,3],[4,5,5],[7,1.2,7]]&matrix2=[[1,2,3],[7,4,6],[7,1.2,7]] |
| multiply_matrix_by_scalar | type: type of input <br> matrix: matrix <br> double: scalar | Returns multiplied matrix | link_to_api/mult_m_s/?type=type&matrix=matrix1&double=double ( list or str for matrix, int or float for double ) | example_str: link_to_api/mult_m_s/?matrix=1 2 3\n4 5 6\n7 8 9&double=1.23, <br> example_list: link_to_api/mult_m_s/?type=list&matrix=[[2,2,3],[4,5,5],[7,1.2,7]]&double=1.23 |
| multiply_matrices  | type: type of input <br> matrix1: matrix1 <br> matrix2: matrix2 |  Returns multiplied matrix  | link_to_api/mult_m/?type=type&matrix1=matrix1&matrix2=matrix2 ( list or str ) | example_str: link_to_api/mult_m/?matrix1=1 2 3\n4 5 6\n7 8 9, <br> example_list: link_to_api/mult_m/?type=list&matrix1=[[2,2,3],[4,5,5],[7,1.2,7]]&matrix2=[[1,2,3],[7,4,6],[7,1.2,7]] |
| sig | double: x | Returns -1 if x < 0, 0 if x == 0, 1 if x > 0 | link_to_api/sig/?double=double | example: link_to_api/sig/?double=1.23 |
| absolute  | double: x |  Returns absolute value of number | link_to_api/abs/?double=double | example: link_to_api/abs/?double=1.23 | 
| random  | dmin: min <br> dmax: max |  Returns random number in range (min, max) | link_to_api/rand/?dmin=dmin&dmax=dmax | example: link_to_api/rand/?dmin=1.23&dmax=1.43 |
| max_matrix | type: type of input <br> matrix: matrix |  Returns max value in matrix | link_to_api/max_m/?type=type&matrix=matrix ( list or str ) | example_str: link_to_api/max_m/?matrix=1 2 3\n4 5 6\n7 8 9, <br> example_list: link_to_api/max_m/?type=list&matrix=[[2,2,3],[4,5,5],[7,1.2,7]] |
| inverse | type: type of input <br> matrix: matrix |   Returns inverted matrix | link_to_api/inv/?type=type&matrix=matrix ( list or str ) | example_str: link_to_api/inv/?matrix=1 2 3\n4 5 6\n7 8 9, <br> example_list: link_to_api/inv/?type=list&matrix=[[2,2,3],[4,5,5],[7,1.2,7]] |
| LU | type: type of input <br> matrix: matrix | Returns LU decomposition | link_to_api/lu/?type=type&matrix=matrix ( list or str ) | example_str: link_to_api/lu/?matrix=1 2 3\n4 5 6\n7 8 9, <br> example_list: link_to_api/lu/?type=list&matrix=[[2,2,3],[4,5,5],[7,1.2,7]] |
| cholv1 | type: type of input <br> matrix: matrix | Returns cholesky decomposition | link_to_api/cholv1/?type=type&matrix=matrix ( list or str ) | example_str: link_to_api/cholv1/?matrix=1 2 3\n4 5 6\n7 8 9, <br> example_list: link_to_api/cholv1/?type=list&matrix=[[2,2,3],[4,5,5],[7,1.2,7]] |
| cholv2 | type: type of input <br> matrix: matrix |Returns cholesky decomposition | link_to_api/cholv2/?type=type&matrix=matrix ( list or str ) | example_str: link_to_api/cholv2/?matrix=1 2 3\n4 5 6\n7 8 9, <br> example_list: link_to_api/cholv2/?type=list&matrix=[[2,2,3],[4,5,5],[7,1.2,7]] |
| eigen  | type: type of input <br> matrix: matrix <br> itern: number <br> tol: tolerance |  Returns eigenvalues and eigenvectors (max, min) <-> max = (max, maxv), min = (min, minv) | link_to_api/eig_mm/?type=type&matrix=matrix1&itern=itern&tol=double ( list or str for matrix, int or float for double ) | example_str: link_to_api/eig_mm/?matrix=1 2 3\n4 5 6\n7 8 9&itern=10&tol=0.01 |
| norm | type: type of input <br> vector: vector | Returns norm of vector | link_to_api/norm/?type=type&vector=vector ( list or str for vector) | example_str: link_to_api/norm/?vector=1 2 3, <br> example_list: link_to_api/norm/?type=list&vector=[1,2,3] |
| vec_approx(vector_a, vector_b)  | type: type of input <br> vector1: vector <br> vector2: vector | Returns vector approximation ( True or False ) | link_to_api/approx/?type=type&vector1=vector1&vector2=vector2 ( list or str for vector) | example_str: link_to_api/approx/?vector1=1 2 3&vector2=4 5 6 <br> example_list: link_to_api/approx/?type=list&vector1=[1,2,3]&vector2=[4,5,6] |

---

#### CLI-API:

still in development
