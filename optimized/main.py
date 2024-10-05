import lineq as lin

matrix = [[1, 2, 12.5], 
          [2, -12.2, 6.3], 
          [7.2, 6.21, 25]]

diag = lin.MatrixMethods.eigen(matrix)


print(lin.MatrixMethods.random(0,2))

print(lin.MatrixMethods.absolute(-15))