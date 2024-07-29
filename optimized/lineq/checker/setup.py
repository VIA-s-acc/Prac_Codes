from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['lineq/checker/checker.pyx']

ext_modules = [
    Extension("checker", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {'language_level': "3str"} 

setup(name = 'checker',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )



#  python .\setup.py built_ext -b build