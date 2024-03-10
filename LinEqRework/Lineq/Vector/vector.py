
class Vector:
    def __init__[T: list | tuple | set | float | int | str | 'Vector' | None](self, data: T = None) -> 'Vector':
        if data is None:
            self.data = []

        if type(data) == list or type(data) == tuple or type(data) == set or type(data) == str:
            self.data = list(data)

        if type(data) == float or type(data) == int:
            self.data = [data]

        if type(data) == str:
            self.data = [int(x) for x in data.split(', ') if x.isdigit()]

        if type(data) == Vector:
            self.data = data.data

        self.size = len(self.data) 

    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        self.data[index] = value

    def __round__(self, n):
        return Vector([round(x, n) for x in self.data])
    
    def from_number[T: float | int | str](size, number: T = 1) -> 'Vector':
        if type(number) == float or type(number) == int:
            return Vector([number] * size)
        if type(number) == str:
            return Vector([int(number)] * size if number.isdigit() else [0] * size)

    def __str__(self):
        return '[' + ', '.join(str(x) for x in self.data) + ']'

    def __iter__(self):
        return iter(self.data)


    def append(self, value):
        self.data.append(value)
        self.size += 1

    def extend(self, values):
        self.data.extend(values)
        self.size += len(values)

    def __len__(self):
        return self.size
    
    def __add__[T: int | float | list | set | tuple | 'Vector'](self, other: T) -> 'Vector':
        if type(other) == int or type(other) == float:
            return Vector([x + other for x in self.data])
        
        if type(other) == list or type(other) == tuple or type(other) == set:
            if len(other) == self.size:
                return Vector([x + y for x, y in zip(self.data, other)])
            else:
                raise ValueError('Vector sizes do not match')
            
        if type(other) == Vector:
            if self.size == other.size:
                return Vector([x + y for x, y in zip(self.data, other.data)])
            else:
                raise ValueError('Vector sizes do not match')
            
    def __radd__(self, other) -> 'Vector':
        return self + other
    
    def __max__(self):
        return max(self.data)
    
    def __min__(self):
        return min(self.data)
    
    def __mul__[T: int | float | 'Vector' | list | set | tuple](self, other) -> 'Vector':
        if type(other) == int or type(other) == float:
            return Vector([x * other for x in self.data])
        if type(other) == Vector:
            if self.size == other.size:
                return sum(x * y for x, y in zip(self.data, other.data))
            else:
                raise ValueError('Vector sizes do not match')

        if type(other) == list or type(other) == tuple or type(other) == set:
            if len(other) == self.size:
                return Vector([x * other[i] for i, x in enumerate(self.data)])
            else:
                raise ValueError('Vector sizes do not match')

    def __neg__(self) -> 'Vector':
        return Vector([-x for x in self.data])

    def __rmul__(self, other) -> 'Vector':
        return self * other
    
    def __sub__(self, other) -> 'Vector':
        return self + -other

    def approximate[T: 'Vector'](vector1: T, vector2: T, eps: float = 1e-6) -> bool:
        for i in range(vector1.size):
            if abs(vector1.data[i] - vector2.data[i]) > eps:
                return False
        return True
    

    def norm(self) -> float:
        return sum(x * x for x in self.data) ** 0.5
    
    @property
    def normalize(self) -> 'Vector':
        if self.norm() == 0:
            raise ValueError('Zero vector')
        temp = [x / self.norm() for x in self.data]
        self.data = temp
    


a = Vector('1, 2, 3')
b = Vector([1.1, 2.1, 3.1])
a.normalize
