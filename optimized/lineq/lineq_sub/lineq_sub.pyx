from libc.stdlib cimport malloc, free

cdef extern from "lowlevel/lin.c" nogil:
    void gauss(const double* matrix_a, const double* vector_, int size_m, int size_v, double* result)



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

        raise MemoryError("Failed to allocate memory")
 
    if size_m != size_v or size_m == 0 or size_v == 0:
        free(c_result)
        free(c_matrix)
        free(c_vector)
        raise IndexError("size_m != size_v or one of them is 0.")


    for i in range(size_m):
        for j in range(size_m):
            c_matrix[i * size_m + j] = matrix[i][j]
    
    for i in range(size_v):
        c_vector[i] = vector[i]
        
    gauss(c_matrix, c_vector, size_m, size_v, c_result)

    result = [c_result[i] for i in range(size_v)]

    free(c_matrix)
    free(c_vector)
    free(c_result)
    
    return result
