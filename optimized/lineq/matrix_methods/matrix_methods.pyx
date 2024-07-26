from libc.stdlib cimport malloc, free

cdef extern from "lowlevel\mm.c" nogil:
    
    #opers
    void multiply_matrices(double* matrix_a, double* matrix_b, double* result_matrix, int rows_a, int cols_a, int rows_b, int cols_b)
    void sum_matrices(double* matrix_a, double* matrix_b, double* result_matrix, int rows, int cols) 
    void multiply_matrix_by_scalar(double* matrix, double scalar, double* result_matrix, int rows, int cols) 
    
    #det and inverse
    double det(double* matrix, int rows, int cols) 
    void inverse(double* matrix, double* result_matrix, int size) 
    
    #numerical
    int signum(double x) 
    double abs_(double x) 
    double random_double(double min_value, double max_value) 
    double max_el_in_matrix(double* matrix, int rows, int cols) 
    
    #decomp 
    void LU_decomp(double* matrix, double* l_matrix, double* u_matrix, int size) 
    void cholesky_decomp1(double* matrix, double* l_matrix, double* u_matrix, int size) 
    void cholesky_decomp2(double* matrix, double* l_matrix, double* u_matrix, double* diag_matrix, int size) 

    # eigen
    double* get_eigen(double* matrix, int size, double* res_maxv, double* res_minv, int max_iterations, double tolerance) 
    double power_meth(double* matrix, int size, double* result_vec, double tolerance, int max_iterations)
    
    #vectors
    double e_norm(double* vector, int size)
    bint vector_approx(double* vector_a, double* vector_b, int size, double tolerance) 

    

def determinant(matrix_a):
    
    cdef int rows_a = int(len(matrix_a))
    cdef int cols_a = int(len(matrix_a[0]))

    cdef int size_a = int(rows_a * cols_a )
    cdef double* c_matrix_a = <double*>malloc(size_a * sizeof(double))

    if c_matrix_a == NULL:
        raise MemoryError("Failed to allocate memory")

    for i in range(rows_a):
        for j in range(cols_a):
            c_matrix_a[i * cols_a + j] = matrix_a[i][j]
    cdef double result = 0

    result = det(c_matrix_a, rows_a, cols_a)

    free(c_matrix_a)
    
    return result

def sum_matrices_wrapper(matrix_a, matrix_b):

    cdef int rows_a = int(len(matrix_a))
    cdef int cols_a = int(len(matrix_a[0]))
    
    cdef int size_a = int(rows_a * cols_a)
    
    cdef double* c_matrix_a = <double*>malloc(size_a * sizeof(double))
    cdef double* c_matrix_b = <double*>malloc(size_a * sizeof(double))
    cdef double* result_matrix = <double*>malloc(size_a * sizeof(double))
    
    if c_matrix_a == NULL or c_matrix_b == NULL or result_matrix == NULL:
        if c_matrix_a != NULL:
            free(c_matrix_a)
        if c_matrix_b != NULL:
            free(c_matrix_b)
        if result_matrix != NULL:
            free(result_matrix)

        raise MemoryError("Failed to allocate memory")

    for i in range(rows_a):
        for j in range(cols_a):
            c_matrix_a[i * cols_a + j] = matrix_a[i][j]
            c_matrix_b[i * cols_a + j] = matrix_b[i][j]



    sum_matrices(c_matrix_a, c_matrix_b, result_matrix, rows_a, cols_a)
    
    result = [[result_matrix[i * cols_a + j] for j in range(cols_a)] for i in range(rows_a)]
    
    free(c_matrix_a)
    free(c_matrix_b)
    free(result_matrix)
    
    return result

def multiply_matrix_by_scalar_wrapper(matrix, scalar):
    cdef int rows = int(len(matrix))
    cdef int cols = int(len(matrix[0]))

    cdef double c_scalar = scalar
    cdef int size = int(rows * cols)

    cdef double* c_matrix = <double*>malloc(size * sizeof(double))
    cdef double* result_matrix = <double*>malloc(size * sizeof(double))

    if c_matrix == NULL or result_matrix == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if result_matrix != NULL:
            free(result_matrix)

        raise MemoryError("Failed to allocate memory")

    for i in range(rows):
        for j in range(cols):
            c_matrix[i * cols + j] = matrix[i][j]


    multiply_matrix_by_scalar(c_matrix, c_scalar, result_matrix, rows, cols)

    result = [[result_matrix[i * cols + j] for j in range(cols)] for i in range(rows)]

    free(result_matrix)
    free(c_matrix)

    return result

def multiply_matrices_wrapper(matrix_a, matrix_b):  
    cdef int rows_a = int(len(matrix_a))
    cdef int cols_a = int(len(matrix_a[0]))
    cdef int rows_b = int(len(matrix_b))
    cdef int cols_b = int(len(matrix_b[0]))
    
    cdef int size_a = int(rows_a * cols_a)
    cdef int size_b = int(rows_b * cols_b)
    cdef int size_result = int(rows_a * cols_b)
    
    cdef double* c_matrix_a = <double*>malloc(size_a * sizeof(double))
    cdef double* c_matrix_b = <double*>malloc(size_b * sizeof(double))
    cdef double* result_matrix = <double*>malloc(size_result * sizeof(double))

    if c_matrix_a == NULL or c_matrix_b == NULL or result_matrix == NULL:
        if c_matrix_a != NULL:
            free(c_matrix_a)
        if c_matrix_b != NULL:
            free(c_matrix_b)
        if result_matrix != NULL:
            free(result_matrix)

        raise MemoryError("Failed to allocate memory")

    for i in range(rows_a):
        for j in range(cols_a):
            c_matrix_a[i * cols_a + j] = matrix_a[i][j]

    for i in range(rows_b):
        for j in range(cols_b):
            c_matrix_b[i * cols_b + j] = matrix_b[i][j]

    multiply_matrices(c_matrix_a, c_matrix_b, result_matrix, rows_a, cols_a, rows_b, cols_b)
    
    result = [[result_matrix[i * cols_b + j] for j in range(cols_b)] for i in range(rows_a)]
    
    free(c_matrix_a)
    free(c_matrix_b)
    free(result_matrix)
    
    return result

def sig(x):
    cdef double c_x = x
    cdef int result = 0

    result = signum(x)

    return result

def absolute(x):
    
    cdef double c_x = x
    cdef double result = 0

    result = abs_(x)

    return result

def random(minv, maxv):
    cdef double c_minv = minv
    cdef double c_maxv = maxv

    cdef double result = random_double(c_minv, c_maxv)

    return result

def max_matrix(matrix):
    cdef int rows = int(len(matrix))
    cdef int cols = int(len(matrix[0]))
    cdef int size = int(rows * cols)

    cdef double* c_matrix = <double*>malloc(size*sizeof(double))
    
    if c_matrix == NULL:
        raise MemoryError("Failed to allocate memory")
    
    for i in range(rows):
        for j in range(cols):
            c_matrix[i * cols + j] = matrix[i][j]
            
    cdef double result = 0

    result = max_el_in_matrix(c_matrix, rows, cols)
    
    free(c_matrix)
    
    return result

def inv(matrix):
    
    cdef int size = int(len(matrix)) 

    cdef double* c_matrix = <double*>malloc(size*size*sizeof(double))

    if c_matrix == NULL:
        raise MemoryError("Failed to allocate memory")

    for i in range(size):
        for j in range(size):
            c_matrix[i * size + j] = matrix[i][j]

    cdef double* result_m = <double*>malloc(size*size*sizeof(double))

    if result_m == NULL:
        raise MemoryError("Failed to allocate memory")

    inverse(c_matrix, result_m, size) 

    result = [[result_m[i*size+j] for j in range(size)] for i in range(size)]

    free(c_matrix)
    free(result_m)
    
    return result

def LU(matrix):
    cdef int size = int(len(matrix))

    cdef double* c_matrix = <double*>malloc(size*size*sizeof(double))
    cdef double* c_l_matrix = <double*>malloc(size*size*sizeof(double))
    cdef double* c_u_matrix = <double*>malloc(size*size*sizeof(double))

    if c_matrix == NULL or c_l_matrix == NULL or c_u_matrix == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if c_l_matrix != NULL:
            free(c_l_matrix)
        if c_u_matrix != NULL:
            free(c_u_matrix)

        raise MemoryError("Failed to allocate memory")


    for i in range(size):
        for j in range(size):
            c_matrix[i*size+j] = matrix[i][j]
    
    LU_decomp(c_matrix, c_l_matrix, c_u_matrix, size)

    result_l = [[c_l_matrix[i*size+j] for j in range(size)] for i in range(size)]
    result_u = [[c_u_matrix[i*size+j] for j in range(size)] for i in range(size)]
    free(c_l_matrix)
    free(c_u_matrix)
    free(c_matrix)

    return result_l, result_u

def cholv1(matrix):
    cdef int size = int(len(matrix))

    cdef double* c_matrix = <double*>malloc(size*size*sizeof(double))
    cdef double* c_l_matrix = <double*>malloc(size*size*sizeof(double))
    cdef double* c_u_matrix = <double*>malloc(size*size*sizeof(double))
    

    if c_matrix == NULL or c_l_matrix == NULL or c_u_matrix == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if c_l_matrix != NULL:
            free(c_l_matrix)
        if c_u_matrix != NULL:
            free(c_u_matrix)

        raise MemoryError("Failed to allocate memory")

    for i in range(size):
        for j in range(size):
            c_matrix[i*size+j] = matrix[i][j]
    
    cholesky_decomp1(c_matrix, c_l_matrix, c_u_matrix, size)
    

    result_l = [[c_l_matrix[i*size+j] for j in range(size)] for i in range(size)]
    result_u = [[c_u_matrix[i*size+j] for j in range(size)] for i in range(size)]
    free(c_l_matrix)
    free(c_u_matrix)
    free(c_matrix)

    return result_l, result_u

def cholv2(matrix):
    cdef int size = int(len(matrix))

    cdef double* c_matrix = <double*>malloc(size*size*sizeof(double))
    cdef double* c_l_matrix = <double*>malloc(size*size*sizeof(double))
    cdef double* c_u_matrix = <double*>malloc(size*size*sizeof(double))
    cdef double* c_d_matrix = <double*>malloc(size*size*sizeof(double))

    if c_matrix == NULL or c_l_matrix == NULL or c_u_matrix == NULL or c_d_matrix == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if c_l_matrix != NULL:
            free(c_l_matrix)
        if c_u_matrix != NULL:
            free(c_u_matrix)
        if c_d_matrix != NULL:
            free(c_d_matrix)
        
        raise MemoryError("Failed to allocate memory")

    for i in range(size):
        for j in range(size):
            c_matrix[i*size+j] = matrix[i][j]

    cholesky_decomp2(c_matrix, c_l_matrix, c_u_matrix, c_d_matrix, size)

    result_l = [[c_l_matrix[i*size+j] for j in range(size)] for i in range(size)]
    result_u = [[c_u_matrix[i*size+j] for j in range(size)] for i in range(size)]
    result_d = [[c_d_matrix[i*size+j] for j in range(size)] for i in range(size)]
    free(c_l_matrix)
    free(c_u_matrix)
    free(c_matrix)
    free(c_d_matrix)

    return result_l, result_d, result_u

def eigen(matrix, max_iter = 100, tol = 0.01):
    cdef int size = int(len(matrix))
    cdef int c_iter = max_iter
    cdef double c_tol = tol
    
    cdef double* c_maxv = <double*>malloc(size*sizeof(double))

    cdef double* c_minv = <double*>malloc(size*sizeof(double))

    cdef double* c_matrix = <double*>malloc(size*size*sizeof(double))

    if c_maxv == NULL or c_minv == NULL or c_matrix == NULL:
        if c_maxv != NULL:
            free(c_maxv)
        if c_minv != NULL:
            free(c_minv)
        if c_matrix != NULL:
            free(c_matrix)
                
        raise MemoryError("Failed to allocate memory")


    for i in range(size):
        for j in range(size):
            c_matrix[i*size+j] = matrix[i][j]

    cdef double* c_res = get_eigen(c_matrix, size, c_maxv, c_minv, c_iter, c_tol)

    res_maxv = [c_maxv[i] for i in range(size)]
    res_minv = [c_minv[i] for i in range(size)]
    res_min = c_res[1]
    res_max = c_res[0]


    free(c_matrix)
    free(c_maxv)
    free(c_minv)
    free(c_res)

    return (res_max, res_maxv), (res_min, res_minv)

def power_method(matrix, max_iter = 100, tol = 0.01):
    cdef int size = int(len(matrix))
    cdef int c_iter = max_iter
    cdef double c_tol = tol
    
    cdef double* c_maxv = <double*>malloc(size*sizeof(double))
    cdef double c_max = 0

    cdef double* c_matrix = <double*>malloc(size*size*sizeof(double))

    if c_matrix == NULL or c_maxv == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if c_maxv != NULL:
            free(c_maxv)
        
        raise MemoryError("Failed to allocate memory")


    for i in range(size):
        for j in range(size):
            c_matrix[i*size+j] = matrix[i][j]

    c_max = power_meth(c_matrix, size, c_maxv, c_tol, c_iter)

    res_maxv = [c_maxv[i] for i in range(size)]


    free(c_matrix)
    free(c_maxv)

    return (c_max, res_maxv)

def norm(vector):

    cdef int size = int(len(vector))

    cdef double* c_vec = <double*>malloc(size*sizeof(double))
    cdef double c_res = 0

    if c_vec == NULL:
        raise MemoryError("Failed to allocate memory")

    for i in range(size):
        c_vec[i] = vector[i]

    c_res = e_norm(c_vec, size)

    free(c_vec)

    return c_res

def vec_approx(vec_a, vec_b, tol = 0.01):
    cdef double c_tol = tol
    cdef int size = int(len(vec_a))

    cdef double* c_vec_a = <double*>malloc(size*sizeof(double)) 
    cdef double* c_vec_b = <double*>malloc(size*sizeof(double))

    if c_vec_a == NULL or c_vec_b == NULL:
        if c_vec_a != NULL:
            free(c_vec_a)
        if c_vec_b != NULL:
            free(c_vec_b)
        
        raise MemoryError("Failed to allocate memory")

    for i in range(size):
        c_vec_a[i] = vec_a[i]
        c_vec_b[i] = vec_b[i]

    cdef bint c_res = vector_approx(c_vec_a, c_vec_b, size, c_tol)

    free(c_vec_a)
    free(c_vec_b)

    return c_res












