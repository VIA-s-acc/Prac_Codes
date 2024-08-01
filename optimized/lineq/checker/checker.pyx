from libc.stdlib cimport malloc, free

cdef extern from "lowlevel/ckr.c" nogil:
    bint _symmetric_check(double* matrix, int rows, int cols)
    bint _diagonal_domination(double* matrix, int rows, int cols) 
    bint _sylvesters_criterion(double* matrix, int size)


def symmetric_check_pyx(matrix):
    cdef int rows = int(len(matrix))
    cdef int cols = int(len(matrix[0]))
    cdef int size = rows * cols

    cdef double* c_matrix = <double*>malloc(sizeof(double) * size)

    if c_matrix == NULL:
        raise MemoryError("Failed to allocate memory")


    for i in range(rows):
        for j in range(cols):
            c_matrix[i * cols + j] = matrix[i][j]

    cdef bint result = _symmetric_check(c_matrix, rows, cols)

    free(c_matrix)

    return result

def diagonal_domination_pyx(matrix):
    cdef int rows = int(len(matrix))
    cdef int cols = int(len(matrix[0]))
    cdef int size = rows * cols

    cdef double* c_matrix = <double*>malloc(sizeof(double) * size)

    if c_matrix == NULL:
        raise MemoryError("Failed to allocate memory")

    for i in range(rows):
        for j in range(cols):
            c_matrix[i * cols + j] = matrix[i][j]

    cdef bint result = _diagonal_domination(c_matrix, rows, cols)

    free(c_matrix)

    return result


def sylvesters_criterion_pyx(matrix):
    cdef int rows = int(len(matrix))
    cdef int cols = int(len(matrix[0]))
    cdef int size = rows * cols

    cdef double* c_matrix = <double*>malloc(sizeof(double) * size)
    
    if c_matrix == NULL:
        raise MemoryError("Failed to allocate memory")
        
    for i in range(rows):
        for j in range(cols):
            c_matrix[i * cols + j] = matrix[i][j]

    cdef bint result = _sylvesters_criterion(c_matrix, rows)

    free(c_matrix)

    return result


