import lineq as lin

matrix = [[1, 2, 12.5], 
          [2, -12.2, 6.3], 
          [7.2, 6.21, 25]]

diag = lin.Checker.diagonal_domination(matrix)
print(diag)
symm = lin.Checker.symmetric_check(matrix)

print(symm)
sylv = lin.Checker.sylvesters_criterion([[1,0],
                                         [3,-4]])

print(sylv)
