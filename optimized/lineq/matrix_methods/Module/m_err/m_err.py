
class BaseMatrixMethodsError(Exception):
    
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    
    
class MatrixShapeError(BaseMatrixMethodsError):
    
    def __init__(self, message):
        super().__init__(message)
        
    def __str__(self):
        return self.message + f"\nCaused in matrix shape error.\n"
    
class MatrixValueError(BaseMatrixMethodsError):
    
    def __init__(self, message):
        super().__init__(message)
        
    def __str__(self):
        return self.message + "\nCaused in matrix value error."
    

class MatrixError(BaseMatrixMethodsError):
    
    def __init__(self, message):
        super().__init__(message)
        
    def __str__(self):
        return self.message + "\nCommon matrix error."
    
class MatrixMethodsError(BaseMatrixMethodsError):
    def __init__(self, message):
        super().__init__(message)
        
    def __str__(self):
        return self.message + '\nCaused in undefined error.'
    
    
