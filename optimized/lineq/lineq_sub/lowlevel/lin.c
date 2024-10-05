#include "../../checker/lowlevel/ckr.c"
#include <string.h>
#include <stdbool.h> // Added for 'bool' type
#include <stdio.h>
#include <math.h>


// READY
//     - `gauss_elimination(matrix, vec, dig)`: Performs Gaussian elimination to solve a system of linear equations.
//     - `_lu_solver(matrix, vec, dig):` Solves a linear system of equations using LU decomposition.
//     - `_forward_substitution(matrix, vec, dig)`: Solves a system of linear equations using forward substitution.
//     - `_backward_substitution(matrix, vec, dig)`: Solves a system of linear equations using backward substitution.
//     - `tridiagonal_elimination(matrix, vec, dig)`: Performs Tridiagonal elimination to solve a system of linear equations.
//     - `simple_iteration(matrix, vec, max_iter, eigen_max_iter, eigen_eps, eps, dig)`: Performs simple iteration to solve a system of linear equations.



// NOT READY
//     - `seidel_iteration(matrix, vec, dig)`: Performs Seidel iteration to solve a system of linear equations.
//     - `jacobi_iteration(matrix, vec, max_iter, eps, dig)`: Performs Jacobi iteration to solve a system of linear equations.
//     - `relaxation_method(matrix, vec, dig, omega)`: Performs relaxation method to solve a system of linear equations.
//     - `_select_omega(matrix, eigen_max_iter, eigen_eps)`: Selects the relaxation parameter for the relaxation method.
//     - `explicit_iteration(matrix, vec, dig)`: Performs explicit iteration to solve a system of linear equations.
//     - `min_res_iteration(matrix, vec, max_iter, eps, dig)`: Performs minimum residual iteration to solve a system of linear equations.
//     - `min_chg_iteration(matrix, vec, max_iter, eps, dig, matrix_choose_mode)`: Performs minimum change iteration to solve a system of linear equations.
//     - `step_desc_iteration(matrix, vec, max_iter, eps, dig)`: Performs method of steepest descent to solve a system of linear equations.
//     - `step_desc_iteration_imp(matrix, vec, max_iter, eps, dig, matrix_choose_mode)`: Performs implicit method of steepest descent to solve a system of linear equations.
//     - `_chol_solver(matrix, vec, dig, mode)`: Solves a linear system using Cholesky decomposition.

void simple_iteration(double* matrix, double* vector, int size_m, int size_v, double* result, double eps, int max_iter, int eigen_max_iter, double eigen_eps)
{    
    if (!_symmetric_check(matrix, size_m, size_m))
    {
        fprintf(stderr, "lineq.lineq_sub.simple_iteration::symmetric_check_error\nThe matrix is not symmetric.\n");
        exit(1);
    }
    if (!_sylvesters_criterion(matrix, size_m))
    {
        fprintf(stderr, "lineq.lineq_sub.simple_iteration::sylvesters_criterion_error\nThe matrix is not positive definite.\n");
        exit(1);
    }
    double* eigen = (double*)malloc(sizeof(double) * 2);
    double* remax_v = (double*)malloc(sizeof(double) * size_v);
    double* remin_v = (double*)malloc(sizeof(double) * size_v);

    if (eigen == NULL || remax_v == NULL || remin_v == NULL)
    {
        if (eigen != NULL) {free(eigen); eigen = NULL;}
        if (remax_v != NULL) {free(remax_v); remax_v = NULL;}
        if (remin_v != NULL) {free(remin_v); remin_v = NULL;}
        fprintf(stderr, "lineq.lineq_sub.simple_iteration::alloc_error\nFailed to allocate memory.\n");
        exit(1);
    }
    eigen = get_eigen(matrix, size_m, remax_v, remin_v, eigen_max_iter, eigen_eps);
    if (eigen == NULL)
    {
        fprintf(stderr, "lineq.lineq_sub.simple_iteration::eigen_error\nFailed to calculate eigenvalues.\n");
        exit
        (1);
    }
    if (remax_v != NULL) {free(remax_v); remax_v = NULL;}
    if (remin_v != NULL) {free(remin_v); remin_v = NULL;}
            
    double max_eigen = eigen[0]; 
    double min_eigen = eigen[1];
    if (eigen != NULL) {free(eigen); eigen = NULL;}
    if (max_eigen <= 0 || min_eigen <= 0)
    {
        fprintf(stderr, "lineq.lineq_sub.simple_iteration::eigen_error\nThe matrix is not positive definite (max_eigen<=0).\n");
        exit(1);
    }
    double thau = 2/(max_eigen + min_eigen);
    double max_v = max_el_in_matrix(matrix, size_m, size_m);
    double* start_vector = (double*)malloc(sizeof(double) * size_v);
    if (start_vector == NULL)
    {
        fprintf(stderr, "lineq.lineq_sub.simple_iteration::alloc_error\nFailed to allocate memory.\n");
        exit(1);
    }
    memset(start_vector, 0, sizeof(double) * size_v);
    for (int i = 0; i < size_v; ++i) {
        start_vector[i] = random_double(0, 1+max_v);
    }
    
    for (int i = 0; i < max_iter; ++i)
    {
        double* new_vector = (double*)malloc(sizeof(double) * size_v);
        if (new_vector == NULL)
        {
            fprintf(stderr, "lineq.lineq_sub.simple_iteration::alloc_error\nFailed to allocate memory.\n");
            exit(1);
        }
        for ( int j = 0; j < size_v; ++j )
        {
            double sum = 0;
            for ( int k = 0; k < size_m; ++k )
            {
                sum += matrix[j * size_m + k] * start_vector[k];
            }
            new_vector[j] = start_vector[j] - thau * (sum - vector[j]);
        }
        if (vector_approx(new_vector, start_vector, size_v, eps)){   
            memcpy(result, new_vector, sizeof(double) * size_v);            
            if (new_vector != NULL) free(new_vector);
            new_vector = NULL;
            if (start_vector != NULL) free(start_vector);
            return;

        }
        memcpy(start_vector, new_vector, sizeof(double) * size_v);
    }

    fprintf(stderr, "lineq.lineq_sub.simple_iteration::max_iter_error\nMaximum number of iterations reached. return last result\n");
    memcpy(result, start_vector, sizeof(double) * size_v);
    if (start_vector != NULL) free(start_vector);
}


void tridiagonal_elimination(double* matrix, double* vector, int size_m, int size_v, double* result)
{
    memset(result, 0, sizeof(double) * size_v);

    if( _diagonal_domination(matrix, size_m, size_m) )
    {
        double* c_prime = (double*)malloc(sizeof(double) * size_m);
        double* d_prime = (double*)malloc(sizeof(double) * size_m);
        
        if ( c_prime == NULL || d_prime == NULL )
        {
            if (c_prime != NULL) free(c_prime);
            if (d_prime != NULL) free(d_prime);
            fprintf(stderr, "lineq.lineq_sub.tridiagonal_elimination::alloc_error\nFailed to allocate memory.\n");
            exit(1);
        }

        memset(c_prime, 0, sizeof(double) * size_m);
        memset(d_prime, 0, sizeof(double) * size_m);

        c_prime[0] = matrix[ 0 * size_m + 1] / matrix[ 0 * size_m + 0];
        d_prime[0] = vector[ 0] / matrix[ 0 * size_m + 0];


        for (int i = 1; i < size_m; ++i)
        {
            double temp = matrix[ i * size_m + i] - matrix[ i * size_m + i - 1] * c_prime[ i - 1];
            if ( i < size_m - 1 )
            {   
                c_prime[ i] = matrix[ i * size_m + i + 1] / temp;
            }
            else {
                c_prime[ i] = 0;
            }
            d_prime[i] = (vector[ i] - matrix[ i * size_m + i - 1] * d_prime[ i - 1]) / temp;
        }

        result[ size_m - 1] = d_prime[ size_m - 1];
        for (int i = size_m - 2; i > -1; --i)
            {
                result[ i] = d_prime[ i] - c_prime[ i] * result[ i + 1];
            }

        free(c_prime);
        free(d_prime);

    }
    else {
        fprintf(stderr, "lineq.lineq_sub.tridiagonal_elimination::diagonal_domination_error\nMatrix is not diagonally dominant.\n");
        exit(1);
    }
}

void gauss(const double* matrix_, const double* vector_, int size_m, int size_v, double* result)
{
    double* matrix = (double*)malloc(sizeof(double) * size_m * size_m);
    double* vector = (double*)malloc(sizeof(double) * size_m);
    if ( matrix == NULL || vector == NULL )
    {
        fprintf(stderr, "lineq.lineq_sub.gauss::alloc_error\nFailed to allocate memory.\n");
        if (matrix != NULL) free(matrix);
        if (vector != NULL) free(vector);
        exit(1);
    }
    
    memcpy(matrix, matrix_, sizeof(double) * size_m * size_m);
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

        if (abs_(pivot) < 1e-15)  // Используем abs_ для сравнения с нулем
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

double* _forward_substitution( double* matrix, double* vec, int size ) {
    double* y = (double*)malloc(size * sizeof(double));
    if (y == NULL) {
        fprintf(stderr, "lineq.lineq_sub._forward_substitution::alloc_error\nFailed to allocate memory.\n");
        exit(1);
    }
    memset(y, 0, sizeof(double) * size);
    y[0] = vec[0] / matrix[0];
    for (int i = 1; i < size; ++i ){
        double sum = 0.0;
        for (int j = 0; j < i; ++j ){
            sum += matrix[i * size + j] * y[j];
        }
        y[i] = (vec[i] - sum) / matrix[i * size + i];
    }

    return y;
}


double* _backward_substitution( double* matrix, double* vec, int size) {
    double* x = (double*)malloc(size * sizeof(double));
    if (x == NULL) {
        fprintf(stderr, "lineq.lineq_sub._backward_substitution::alloc_error\nFailed to allocate memory.\n");
        exit(1);
    }
    memset(x, 0, sizeof(double) * size);
    x[size-1] = vec[size-1] / matrix[(size-1) * size + size-1];
    
    for ( int i = size - 2; i > -1; --i)
    {
        double sum = 0.0;
        for ( int j = i + 1; j < size; ++j)
        {
            sum += matrix[i * size + j] * x[j];
        }
        x[i] = (vec[i] - sum) / matrix[i * size + i];
    }

    return x;
}


void _lu_solver(double* matrix,  double* vec, int size, double* result) {
    
   
    double* lower = (double*)malloc(size * size * sizeof(double));
    double* upper = (double*)malloc(size * size * sizeof(double));
    if (lower == NULL || upper == NULL) {
        if (lower != NULL) free(lower);
        if (upper != NULL) free(upper);
        fprintf(stderr, "lineq.lineq_sub._lu_solver::alloc_error\nCannot allocate memory for LU decomposition. Exiting.\n");
        exit(1);
    }
    
    LU_decomp(matrix, lower, upper, size);
   

    double* y = _forward_substitution(lower, vec, size);
    if (y == NULL) {
        if (lower != NULL) free(lower);
        if (upper != NULL) free(upper);
        fprintf(stderr, "lineq.lineq_sub._lu_solver::alloc_error\nCannot allocate memory for LU solver. Exiting.\n");
        exit(1);
    }
    double* x = _backward_substitution(upper, y, size);

    if (x == NULL) {
        if (y != NULL) free(y);
        if (lower != NULL) free(lower);
        if (upper != NULL) free(upper);
        fprintf(stderr, "lineq.lineq_sub._lu_solver::alloc_error\nCannot allocate memory for LU solver. Exiting.\n");
        exit(1);
    }
    
        

    for (int i = 0; i < size; ++i) {
        result[i] = x[i];
    }

    free(lower);
    free(upper);
    free(y);
    free(x);
}


