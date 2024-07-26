#include "../matrix_methods/lowlevel/mm.c"
#include <string.h>

void random_matrix(int size, double rng, char* mode, double* result) {
    for (int i = 0; i < size * size; ++i) {
        result[i] = 0;
    }

    if (strcmp(mode, "3diag") == 0) {
        for (int i = 0; i < size; ++i) {
            result[i * size + i] = random_double(-rng, rng);

            if (i > 0) {
                result[i * size + i - 1] = random_double(-rng, rng);
            }
            if (i < size - 1) {
                result[i * size + i + 1] = random_double(-rng, rng);
            }
        }

    } else if (strcmp(mode, "symm") == 0) {
        for (int i = 0; i < size; ++i) {
            for (int j = i; j < size; ++j) {
                result[i * size + j] = random_double(-rng, rng);
                result[j * size + i] = result[i * size + j];
            }
        }
    } else {
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                result[i * size + j] = random_double(-rng, rng);
            }
        }
    }
}



void random_vector(int size, double rng, double* result) {
    for (int i = 0; i < size; ++i) {
        result[i] = random_double(-rng, rng);
    }
}