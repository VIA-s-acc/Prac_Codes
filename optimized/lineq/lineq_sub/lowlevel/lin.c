#include "../../checker/lowlevel/ckr.c"
#include <string.h>
#include <stdbool.h> // Added for 'bool' type
#include <stdio.h>
#include <math.h>
void gauss(const double* matrix_a, const double* vector_, int size_m, int size_v, double* result)
{
    double* matrix = (double*)malloc(sizeof(double) * size_m * size_m);
    double* vector = (double*)malloc(sizeof(double) * size_m);
    
    memcpy(matrix, matrix_a, sizeof(double) * size_m * size_m);
    memcpy(vector, vector_, sizeof(double) * size_v);
    memset(result, 0, sizeof(double) * size_v);

    for (int i = 0; i < size_m; ++i)
    {
        int max_row = i;
        for (int k = i + 1; k < size_m; ++k)
        {
            if (abs_(matrix[k * size_m + i]) > abs_(matrix[max_row * size_m + i]))
            {
                max_row = k;
            }
        }

        if (i != max_row)
        {

            for (int j = 0; j < size_m; ++j)
            {
                double temp = matrix[i * size_m + j];
                matrix[i * size_m + j] = matrix[max_row * size_m + j];
                matrix[max_row * size_m + j] = temp;
            }
            double temp = vector[i];
            vector[i] = vector[max_row];
            vector[max_row] = temp;   
        }
        

        double pivot = matrix[i * size_m + i];

        if (abs_(pivot) < 1e-12)  // Используем abs_ для сравнения с нулем
        {
            free(matrix);
            free(vector);
            fprintf(stderr, "lineq.lineq_sub.gauss_solve::pivot_error\nPivot is near 0.0. Exiting.\n");
            exit(1);
        }

        for (int j = i; j < size_m; ++j)
        {
            matrix[i * size_m + j] /= pivot;
        }

        vector[i] /= pivot;

        for (int j = i + 1; j < size_m; ++j)
        {
            double factor = matrix[j * size_m + i];
            for (int k = i; k < size_m; ++k)
            {
                matrix[j * size_m + k] -= matrix[i * size_m + k] * factor;
            }
            vector[j] -= vector[i] * factor;
        }
    }

    for (int i = size_m - 1; i > -1; --i)
    {
        result[i] = vector[i];
        for (int j = i + 1; j < size_m; ++j)
        {
            result[i] -= matrix[i * size_m + j] * result[j];
        }
    }

    free(matrix);
    free(vector);
}
