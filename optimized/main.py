import lineq as lin

matrix = [[1, 0, 0], 
          [0, 12, 6], 
          [0, 6, 25]]

diag = lin.Checker.diagonal_domination(matrix)
print(diag)
symm = lin.Checker.symmetric_check(matrix)

print(symm)
sylv = lin.Checker.sylvesters_criterion([[1,0],
                                         [3,4]])

print(sylv)