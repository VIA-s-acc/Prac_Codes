from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['lineq/generator/generator.pyx']

ext_modules = [
    Extension("generator", 
            sources=sourceFiles),
]

setup(name = 'generator',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )



#  python .\setup.py built_ext -b build