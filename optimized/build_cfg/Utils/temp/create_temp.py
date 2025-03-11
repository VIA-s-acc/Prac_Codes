setup = lambda m, s: f'''
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['{m}/{s}/{s}.pyx', '{m}/{s}/lowlevel/{m}_{s}_c.c']

ext_modules = [
    Extension("{s}", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {{"language_level": "3str"}} 

setup(name = '{s}',
    cmdclass={{'build_ext': build_ext}},
    ext_modules=ext_modules
    )
'''

template_pyx = lambda m, s: f'''\
#==========================================================
# BASE PYX TEMPLATE
#==========================================================

from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

cdef extern from "lowlevel/{m}_{s}_c.h" nogil:
    int basic_function()

def call_basic_function():
    return basic_function()
'''

template_h = lambda m, s: f"""\
/*==========================================================
BASE HEADER TEMPLATE
==========================================================*/
#ifndef {s.upper()}_H
#define {s.upper()}_H


int basic_function();

#endif // {s.upper()}_H
"""

# Лямбда-шаблон для .c файла
template_c = lambda m, s: f"""\
/*==========================================================
BASE C TEMPLATE
==========================================================*/
#include "{m}_{s}_c.h"

int basic_function() {{
    return 1;
}}
"""


template_module = lambda m, s: f'''\

#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.{s} import (
    call_basic_function as raw_basic_function
)

class {s.capitalize()}Module:
    def __init__(self):
        pass

    def call_basic_function(self):
        return raw_basic_function()

def sample_function():
    instance = {s.capitalize()}Module()
    instance.call_basic_function()
    return "basic_function worked."
'''