from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['lineq/matrix_methods/matrix_methods.pyx']

ext_modules = [
    Extension("matrix_methods", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {'language_level': "3str"} 

setup(name = 'Matrix_Methods',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )



#  python .\setup.py built_ext -b build