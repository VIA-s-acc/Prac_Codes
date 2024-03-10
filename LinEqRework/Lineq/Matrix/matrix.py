from ..Vector.vector import Vector

class Matrix:

    def __init__[T: list[list] | Vector[Vector] | 'Matrix' ](self, data: T) -> 'Matrix':
        if type(data) == list:
            self.data = Vector()
            
            for row in data:
                if type(row) != list:
                    raise ValueError('__init__(list) expected list of lists')
            for row in data:
                row = Vector(row)
                self.data.append(row)

        elif type(data) == Vector:
            for row in data.data:
                if type(row) != Vector:
                    raise ValueError('__init__(Vector) expected Vector of Vectors')
            self.data = data

        elif type(data) == Matrix:
            self.data = data.data

        self.shape = (len(self.data), len(self.data[0]))

    def __iter__(self) -> iter:
        return iter(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if type(value) != Vector:
            try:
                value = Vector(value)
            except:
                raise ValueError('__setitem__(Vector) expected Vector')
        self.data[index] = value   

    def __str__(self) -> str:
        max = 0
        for row in self.data:
            for element in row:
                if max < len(str(element)):
                    max = len(str(element))
        num_cols = len(self.data[0])
        num_rows = len(self.data)
        result = ""

        col_labels = " " * 10 + "|" + f"|".join(f"{f"Col {i}": >{max+4}} " for i in range(1, num_cols + 1)) + ' |'

        separator = "-" * (len(col_labels) + 2)
        result += f"{separator}\n{col_labels}\n{separator}"

        for i, row in enumerate(self):
            row_str = f"Row {i+1: <5} |" + "|".join(map(lambda x: f"{x: > {max+5}}", row)) + " |"
            result += f"\n{row_str}"
        result += "\n" + separator
        return result
    

                
    def __mul__[T: int | float | 'Matrix' | Vector](self, other: T) -> 'Matrix':

        if type(other) == int or type(other) == float:
            return Matrix([[x * other for x in row] for row in self.data])
        
        if type(other) == list or type(other) == tuple or type(other) == set:
            other = Vector(other)

        if type(other) == Vector:
            other = Vector([Vector(x) for x in other])
            if self.shape[1] == other.size:
                return Matrix([[sum(x*other[i][0] for i, x in enumerate(row, 0))] for row in self])    
                
            else:
                raise ValueError('Vector sizes do not match')

        if type(other) == Matrix:
            if self.shape[1] == other.shape[0]:
                return Matrix([[sum(x*other[i][j] for i, x in enumerate(row, 0)) for j in range(other.shape[1])] for row in self.data])
            

    def __add__[T: int | float | 'Matrix'](self, other: T) -> 'Matrix':
        if type(other) == int or type(other) == float:
            return Matrix([[x + other for x in row] for row in self.data])
        
        if type(other) == Matrix:
            if self.shape == other.shape:
                return Matrix([[x + y for x, y in zip(row, other[i])] for i, row in enumerate(self.data)])
            
    def __neg__(self) -> 'Matrix':
        return Matrix([[-x for x in row] for row in self.data])
    
    def __sub__(self, other) -> 'Matrix':
        return self + -other
    
    def __rsub__(self, other) -> 'Matrix':
        return -self + other
    
    def __radd__(self, other) -> 'Matrix':
        return self + other
    
    def __rmul__(self, other) -> 'Matrix':
        return self * other
    
    def __eq__(self, other) -> bool:
        return self.data == other
    
    def __ne__(self, other) -> bool:
        return self.data != other
    
    def __round__(self, n) -> 'Matrix':
        return Matrix([[round(x, n) for x in row] for row in self.data])
    
    
    


