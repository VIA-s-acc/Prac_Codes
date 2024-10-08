from libc.stdlib cimport malloc, free
from libc.string cimport strcpy, strlen

cdef extern from "lowlevel/gn.c" nogil:
    void random_matrix(int size, double rng, char* mode, double* result)
    void random_vector(int size, double rng, double* result)


def generate_random_matrix(size, rng, mode):
    cdef int mode_size = int(len(mode))
    cdef char* mode_c = <char*>malloc((mode_size + 1) * sizeof(char))  # Include space for null terminator
    cdef int c_size = int(size)
    cdef double c_rng = rng

    cdef double* c_result = <double*>malloc(c_size * c_size * sizeof(double))

    if mode_c == NULL or c_result == NULL:
        if mode_c != NULL:
            free(mode_c)
        if c_result != NULL:
            free(c_result)
        raise MemoryError("lineq.generator.generate_random_matrix::alloc_error\nFailed to allocate memory")

    strcpy(mode_c, mode.encode('utf-8'))

    with nogil:
        random_matrix(c_size, c_rng, mode_c, c_result)

    result = [[c_result[i * c_size + j] for j in range(size)] for i in range(size)]

    free(mode_c)
    free(c_result)

    return result

def generate_random_vector(size, rng):
    cdef int c_size = int(size)
    cdef double c_rng = rng
    
    cdef double* c_result = <double*>malloc(c_size*sizeof(double))

    if c_result == NULL:
        raise MemoryError("lineq.generator.generate_random_vector::alloc_error\nFailed to allocate memory")

    with nogil:
        random_vector(c_size, c_rng, c_result)
    
    result = [c_result[i] for i in range(c_size)]
    
    free(c_result)

    return result