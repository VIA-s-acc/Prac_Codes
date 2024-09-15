from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['lineq/lineq_sub/lineq_sub.pyx']

ext_modules = [
    Extension("lineq_sub", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {'language_level': "3str"} 

setup(name = 'Lineq_sub',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )



#  python .\setup.py built_ext -b build