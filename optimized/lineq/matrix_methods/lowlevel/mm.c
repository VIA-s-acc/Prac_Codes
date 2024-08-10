#include <stdlib.h>
#include <math.h>
#include <stdbool.h> // Added for 'bool' type
#include <stdio.h>

//Other

int signum(double x) {
    if (x > 0) {
        return 1;
    } else if (x < 0) {
        return -1;
    } else {
        return 0;
    }
}

double abs_(double x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
}

// VECTORS

double e_norm(double* vector, int size){
    double sum = 0;
    for (int i = 0; i < size; ++i) {
        sum += vector[i] * vector[i];
    }
    return sqrt(sum);
}

bool vector_approx(double* vector_a, double* vector_b, int size, double tolerance) {
    double* new_vector = (double*)malloc(sizeof(double) * size);
    for (int i = 0; i < size; ++i) {
        new_vector[i] = vector_a[i] - vector_b[i];
    }
    double norm = e_norm(new_vector, size);
    free(new_vector);
    return norm < tolerance;
}


// MATRIX

void multiply_matrices(double* matrix_a, double* matrix_b, double* result_matrix, int rows_a, int cols_a, int rows_b, int cols_b) {
    for (int i = 0; i < rows_a; ++i) {
        for (int j = 0; j < cols_b; ++j) {
            result_matrix[i * cols_b + j] = 0;
            for (int k = 0; k < cols_a; ++k) {
                result_matrix[i * cols_b + j] += matrix_a[i * cols_a + k] * matrix_b[k * cols_b + j];
            }
        }
    }
}

void multiply_matrix_by_scalar(double* matrix, double scalar, double* result_matrix, int rows, int cols) {
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            result_matrix[i * cols + j] = matrix[i * cols + j] * scalar;
        }
    }
}

void sum_matrices(double* matrix_a, double* matrix_b, double* result_matrix, int rows, int cols) {
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            result_matrix[i * cols + j] = matrix_a[i * cols + j] + matrix_b[i * cols + j];
        }
    }
}

double det(double* matrix, int rows, int cols) {
    double determinant = 1;
    
    for ( int i = 0; i < rows; ++i )
    {
        int max_row = i;

        for ( int k = i+1; k < rows; ++k )
        {
            if (abs_(matrix[k * cols + i ] > abs_(matrix[max_row * cols + i ])))
            {
                max_row = k;
            }
        }

        if ( max_row != i )
        {
            for ( int j = 0; j < cols; ++j )
            {
                double temp = matrix[i * cols + j];
                matrix[i * cols + j] = matrix[max_row * cols + j];
                matrix[max_row * cols + j] = temp;
            }
            determinant = -determinant;
        }
        determinant *= matrix[i * cols + i];

        if ( matrix[i * cols + i] == 0 )
        {
            return 0;
        }

        for ( int k = i+1; k < rows; ++k )
        {
            double factor = -matrix[k * cols + i ] / matrix[i * cols + i];
            for ( int j = 0; j < cols; ++j )
            {
                matrix[k * cols + j] += factor * matrix[i * cols + j];
            }
        }
    }
    return determinant;
}

void inverse(double* matrix, double* result_matrix, int size) {
    memset(result_matrix, 0, sizeof(double) * size * size);

    for (int i = 0; i < size; ++i) {          
        result_matrix[i * size + i] = 1;
    }

    for ( int i = 0; i < size; ++i) {

        double diag = matrix[i * size + i];
        if ( diag == 0.0 )
        {
            for ( int k = i + 1; k < size; ++k )
            {
                if ( matrix[k * size + i] != 0.0 )
                {
                    for ( int j = 0; j < size; ++j )
                    {
                        double temp = matrix[i * size + j];
                        matrix[i * size + j] = matrix[k * size + j];
                        matrix[k * size + j] = temp;
                        temp = result_matrix[i * size + j];
                        result_matrix[i * size + j] = result_matrix[k * size + j];
                        result_matrix[k * size + j] = temp;
                    }
                    break;
                }

            }
        }
        diag = matrix[i * size + i];
        if ( diag == 0.0 )
        {
            printf("Warning!!!!! Matrix is not invertible ( determinant = 0 )\nResult is zeros matrix\n");
            memset(result_matrix, 0, sizeof(double) * size * size);
            return;
        }
        for ( int k = 0; k < size; ++k )
        {
            matrix[i * size + k] /= diag;
            result_matrix[i * size + k] /= diag;
        }
        for ( int j = 0; j < size; ++j )
        {
            if ( j != i )
            {
                double factor = matrix[j * size + i];
                for ( int k = 0; k < size; ++k )
                {
                    matrix[j * size + k] -= factor * matrix[i * size + k];
                    result_matrix[j * size + k] -= factor * result_matrix[i * size + k];
                }
            }
        }
    }
}

void LU_decomp(double* matrix, double* l_matrix, double* u_matrix, int size) {
    memset(l_matrix, 0, sizeof(double) * size * size);
    memset(u_matrix, 0, sizeof(double) * size * size);
    for (int i = 0; i < size; ++i) {
        l_matrix[i * size + i] = 1;
    }

    for (int i = 0; i < size; ++i) {

        for (int j = i; j < size; ++j) {
            double sum = 0;
            for (int k = 0; k < i; ++k) {
                sum += l_matrix[i * size + k] * u_matrix[k * size + j];
            }
            u_matrix[i * size + j] = matrix[i * size + j] - sum;
        }

        for (int j = i; j < size; ++j) {
            double sum = 0;
            for (int k = 0; k < i; ++k) {
                sum += l_matrix[j * size + k] * u_matrix[k * size + i];
            }
            l_matrix[j * size + i] = (matrix[j * size + i] - sum) / u_matrix[i * size + i];
        }
    }
}

void cholesky_decomp1(double* matrix, double* l_matrix, double* u_matrix, int size) {
    memset(l_matrix, 0, sizeof(double) * size * size);
    memset(u_matrix, 0, sizeof(double) * size * size);

    for (int i = 0; i < size; ++i) {
        for ( int j = 0; j < i+1; ++j) {
            if ( i == j )
            {
                double sum = 0;
                for ( int k = 0; k < j; ++k) {
                    sum += l_matrix[i * size + k] * l_matrix[i * size + k];
                }
                l_matrix[i * size + j] = sqrt(matrix[i * size + i] - sum);
                u_matrix[j * size + i] = l_matrix[i * size + j];
            }
            else {
                double sum = 0;
                for ( int k = 0; k < j; ++k) {
                    sum += l_matrix[i * size + k] * u_matrix[k * size + j];
                }
                l_matrix[i * size + j] = (1.0 / l_matrix[j * size + j] * (matrix[i * size + j] - sum));
                u_matrix[j * size + i] = l_matrix[i * size + j];
            }
        }
    }
}


void cholesky_decomp2(double* matrix, double* l_matrix, double* u_matrix, double* diag_matrix, int size) {
    memset(l_matrix, 0, sizeof(double) * size * size);
    memset(u_matrix, 0, sizeof(double) * size * size);
    memset(diag_matrix, 0, sizeof(double) * size * size);

    double* diagonal = (double*)malloc(sizeof(double) * size);
    memset(diagonal, 0, sizeof(double) * size);

    for ( int i = 0; i < size; ++i) {
        for ( int j = i; j < size; ++j)
        {
            if ( i == j )
            {
                double sum = 0;
                for ( int k = 0; k < i; ++k)
                {
                    sum += diagonal[k] * u_matrix[k * size + i] * u_matrix[k * size + i];
                }
                double sum_v = matrix[i * size + i] - sum;
                diagonal[i] = signum(sum_v);
                u_matrix[i * size + i] = sqrt(abs_(sum_v));
            }
            else{
                double sum = 0;
                for ( int k = 0; k < i; ++k)
                {
                    sum += diagonal[k] * u_matrix[k * size + i] * u_matrix[k * size + j];
                }
                double sum_v = (matrix[i * size + j] - sum)/(u_matrix[i * size + i] * diagonal[i]);
                u_matrix[i * size + j] = sum_v;
            }
        }
    }   

    for ( int i = 0; i < size; ++i) {
        for ( int j = 0; j < size; ++j)
        {
            if (i == j)
            {
                diag_matrix[i * size + j] = diagonal[i];
            }
            else
            {
                diag_matrix[i * size + j] = 0;
            }
            l_matrix[i * size + j] = u_matrix[j * size + i];
        }
    }
}


double random_double(double min_value, double max_value) {
    return min_value + (double)rand() / RAND_MAX * (max_value - min_value);
}

double max_el_in_matrix(double* matrix, int rows, int cols) {
    double max = matrix[0];
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            if (matrix[i * cols + j] > max) {
                max = matrix[i * cols + j];
            }
        }
    }
    return max;
}

double power_meth(double* matrix, int size, double* result_vec, double tolerance, int max_iterations) {
    double max_v = max_el_in_matrix(matrix, size, size);
    double result_eigen = 0;
    double* start_vector = (double*)malloc(size*sizeof(double));
    double* eigen_value = (double*)malloc(sizeof(double));
    double* vec_ = (double*)malloc(sizeof(double) * size);
    double* new_vec = (double*) malloc(sizeof(double)*size);
    double* new_eigen_value = (double*)malloc(sizeof(double));
    double eigenvalue = 0;
    double new_eigenvalue = 0;
    double new_norm = 0;
    for (int i = 0; i < size; ++i) {
        start_vector[i] = random_double(0, max_v+1);
    }


    double norm = e_norm(start_vector, size);
    for (int i = 0; i < size; ++i) {
        start_vector[i] = start_vector[i] / norm;
    }
    for (int i = 0; i < max_iterations; ++i) {

        multiply_matrices(start_vector, matrix, vec_, 1, size, size, size);
        multiply_matrices(vec_, start_vector , eigen_value, 1, size, size, 1);
        eigenvalue = eigen_value[0];
        multiply_matrices(matrix, start_vector, new_vec, size, size, size, 1);
        new_norm = e_norm(new_vec, size);
        if ( new_norm == 0 )
        {
            for ( int i = 0; i < size; ++i) {
                result_vec[i] = start_vector[i];
            }
            result_eigen = eigenvalue;
            return result_eigen;
        } 

        for (int i = 0; i < size; ++i) {
            new_vec[i] = new_vec[i] / new_norm;
        }
        multiply_matrices(new_vec, matrix, vec_, 1, size, size, size);
        multiply_matrices(vec_, new_vec , new_eigen_value, 1, size, size, 1);
        new_eigenvalue = new_eigen_value[0] ;

        if ( abs_(eigenvalue - new_eigenvalue) < tolerance ) {
            for ( int i = 0; i < size; ++i) {
                result_vec[i] = new_vec[i];
            }
            result_eigen = new_eigenvalue;
            free(start_vector);
            free(eigen_value);
            free(vec_);
            free(new_vec);
            free(new_eigen_value);
            return result_eigen;
        }
        else{
            for ( int i = 0; i < size; ++i) {
                start_vector[i] = new_vec[i];
            }
            eigenvalue = new_eigenvalue;
        }   
    }
    for ( int i = 0; i < size; ++i) {
        result_vec[i] = start_vector[i];
    }
    result_eigen = eigenvalue;

    free(start_vector);
    free(eigen_value);
    free(vec_);
    free(new_vec);
    free(new_eigen_value);

    return result_eigen;
}

double* get_eigen(double* matrix, int size, double* res_maxv, double* res_minv, int max_iterations, double tolerance) {
    double* res_eigen = (double*)malloc(sizeof(double) * 2);
    double res_max = power_meth(matrix, size, res_maxv, tolerance, max_iterations);
    double* E_matrix = (double*)malloc(sizeof(double) * size * size);
    memset(E_matrix, 0, sizeof(double) * size * size);
    for (int i = 0; i < size; ++i) {
        E_matrix[i * size + i] = 1;

    }
    double* transform_matrix = (double*)malloc(sizeof(double) * size * size);
    for (int i = 0; i < size; ++i)
    {
        for (int j = 0; j < size; ++j)
        {
            transform_matrix[i * size + j] = matrix[i * size + j] - res_max * E_matrix[i * size + j];
        }
    }
    double res_min = power_meth(transform_matrix, size, res_minv, tolerance, max_iterations);
    
    free(E_matrix);
    free(transform_matrix);
    if ( res_max > 0)
    {
        res_min = res_max + res_min;
    }
    if (res_max < 0)
    {
        double temp = res_min;
        res_min = res_max;
        res_max = res_max + temp;
    }
    
    res_eigen[0] = res_max;
    res_eigen[1] = res_min;

    return res_eigen;
}



