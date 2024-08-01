#include "../../matrix_methods/lowlevel/mm.c"
#include <string.h>
#include <stdbool.h> // Added for 'bool' type
#include <stdio.h>

bool _symmetric_check(double* matrix, int rows, int cols) {
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            if (matrix[i * cols + j] != matrix[j * cols + i]) {
                return false;
            }
        }
    }
    return true;
}

bool _diagonal_domination(double* matrix, int rows, int cols) {
    for (int i = 0; i < rows; ++i) {
        double sum = 0;
        for (int j = 0; j < cols; ++j) {
            if (i != j) {
                sum += matrix[i * cols + j];
            }
        }
        if (abs_(matrix[i * cols + i]) <= sum) {
            return false;
        }
    }
    return true;
}

bool _sylvesters_criterion(double* matrix, int size) {
    for (int i = 1; i < size + 1; ++i) {
        double* sub_matrix = (double*)malloc(sizeof(double) * i * i);
        memset(sub_matrix, 0, sizeof(double) * i * i);
        for (int j = 0; j < i; ++j) {
            for (int k = 0; k < i; ++k) {
                sub_matrix[j * i + k] = matrix[j * size + k];
            }
        }
        double det_sub = det(sub_matrix, i, i);

        
        free(sub_matrix);
        if (det_sub <= 0) {
            return false;
        }
    }
    return true;
}

