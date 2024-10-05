from libc.stdlib cimport malloc, free
cdef extern from "lowlevel/lin.c" nogil:
    void gauss(const double* matrix_a, const double* vector_, int size_m, int size_v, double* result)
    void _lu_solver(double* matrix, double* vec, int size, double* result) 
    void tridiagonal_elimination(double* matrix, double* vector, int size_m, int size_v, double* result)
    void simple_iteration(double* matrix, double* vector, int size_m, int size_v, double* result, double eps, int max_iter, int eigen_max_iter, double eigen_eps)


def iter_solve_simple(matrix, vector, eps=1e-12, max_iter=1000, eigen_max_iter=1000, eigen_eps=1e-12):
    cdef int size_m = int(len(matrix))
    cdef int size_v = int(len(vector))
    cdef double c_eps = float(eps)
    cdef int c_max_iter = int(max_iter)
    cdef int c_eigen_max_iter = int(eigen_max_iter)
    cdef double c_eigen_eps = float(eigen_eps)


    cdef double* c_matrix = <double*>malloc(size_m * size_m * sizeof(double))
    cdef double* c_vector = <double*>malloc(size_v * sizeof(double))
    cdef double* c_result = <double*>malloc(size_v * sizeof(double))

    if c_matrix == NULL or c_vector == NULL or c_result == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if c_vector != NULL:
            free(c_vector)
        if c_result != NULL:
            free(c_result)

        raise MemoryError("lineq.lineq_sub.iter_solve_simple::alloc_error\nFailed to allocate memory")
 
    if size_m != size_v or size_m == 0 or size_v == 0:
        free(c_matrix)
        free(c_vector)
        raise IndexError("lineq.lineq_sub.iter_solve_simple::size_error\nsize_m != size_v or one of them is 0.")

    for i in range(size_m):
        for j in range(size_m):
            c_matrix[i * size_m + j] = matrix[i][j]

    for i in range(size_v):
        c_vector[i] = vector[i]
    
    with nogil:
        simple_iteration(c_matrix, c_vector, size_m, size_v, c_result, c_eps, c_max_iter, c_eigen_max_iter, c_eigen_eps)

    result = [c_result[i] for i in range(size_v)]

    free(c_matrix)
    free(c_vector)
    free(c_result)

    return result

def solve_tridiagonal(matrix, vector):
    cdef int size_m = int(len(matrix))
    cdef int size_v = int(len(vector))


    cdef double* c_matrix = <double*>malloc(size_m * size_m * sizeof(double))
    cdef double* c_vector = <double*>malloc(size_v * sizeof(double))
    cdef double* c_result = <double*>malloc(size_v * sizeof(double))

    if c_matrix == NULL or c_vector == NULL or c_result == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if c_vector != NULL:
            free(c_vector)
        if c_result != NULL:
            free(c_result)

        raise MemoryError("lineq.lineq_sub.solve_tridiagonal::alloc_error\nFailed to allocate memory")
 
    if size_m != size_v or size_m == 0 or size_v == 0:
        free(c_matrix)
        free(c_vector)
        raise IndexError("lineq.lineq_sub.solve_tridiagonal::size_error\nsize_m != size_v or one of them is 0.")

    for i in range(size_m):
        for j in range(size_m):
            c_matrix[i * size_m + j] = matrix[i][j]
    
    for i in range(size_v):
        c_vector[i] = vector[i]
    
    with nogil:
        tridiagonal_elimination(c_matrix, c_vector, size_m, size_v, c_result)

    result = [c_result[i] for i in range(size_v)]

    free(c_matrix)
    free(c_vector)
    free(c_result)
    
    return result

def solve_gauss(matrix, vector):
    cdef int size_m = int(len(matrix))
    cdef int size_v = int(len(vector))


    cdef double* c_matrix = <double*>malloc(size_m * size_m * sizeof(double))
    cdef double* c_vector = <double*>malloc(size_v * sizeof(double))
    cdef double* c_result = <double*>malloc(size_v * sizeof(double))

    if c_matrix == NULL or c_vector == NULL or c_result == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if c_vector != NULL:
            free(c_vector)
        if c_result != NULL:
            free(c_result)

        raise MemoryError("lineq.lineq_sub.solve_gauss::alloc_error\nFailed to allocate memory")
 
    if size_m != size_v or size_m == 0 or size_v == 0:
        free(c_result)
        free(c_matrix)
        free(c_vector)
        raise IndexError("lineq.lineq_sub.solve_gauss::size_error\nsize_m != size_v or one of them is 0.")


    for i in range(size_m):
        for j in range(size_m):
            c_matrix[i * size_m + j] = matrix[i][j]
    
    for i in range(size_v):
        c_vector[i] = vector[i]

    with nogil:  
        gauss(c_matrix, c_vector, size_m, size_v, c_result)

    result = [c_result[i] for i in range(size_v)]

    free(c_matrix)
    free(c_vector)
    free(c_result)
    
    return result


def solve_lu(matrix, vector):
    cdef int size_m = int(len(matrix))
    cdef int size_v = int(len(vector))


    cdef double* c_matrix = <double*>malloc(size_m * size_m * sizeof(double))
    cdef double* c_vector = <double*>malloc(size_v * sizeof(double))
    cdef double* c_result = <double*>malloc(size_v * sizeof(double))

    if c_matrix == NULL or c_vector == NULL or c_result == NULL:
        if c_matrix != NULL:
            free(c_matrix)
        if c_vector != NULL:
            free(c_vector)
        if c_result != NULL:
            free(c_result)

        raise MemoryError("lineq.lineq_sub.solve_lu::alloc_error\nFailed to allocate memory")
 
    if size_m != size_v or size_m == 0 or size_v == 0:
        free(c_result)
        free(c_matrix)
        free(c_vector)
        raise IndexError("lineq.lineq_sub.solve_lu::size_error\nsize_m != size_v or one of them is 0.")

    for i in range(size_m):
        for j in range(size_m):
            c_matrix[i * size_m + j] = matrix[i][j]
    
    for i in range(size_v):
        c_vector[i] = vector[i]
    
    with nogil:
        _lu_solver(c_matrix, c_vector, size_m, c_result)
    
    result = [c_result[i] for i in range(size_v)]

    free(c_matrix)
    free(c_vector)
    free(c_result)
    
    return result
