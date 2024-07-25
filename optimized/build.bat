@echo off
REM Сборка matrix_methods

if exist lineq\matrix_methods\build rmdir /S /Q lineq\matrix_methods\build 
if exist lineq\matrix_methods\lowlevel\matrix_methods.c del /Q lineq\matrix_methods\lowlevel\matrix_methods.c
python lineq\matrix_methods\setup.py build_ext -b build
move /Y build lineq\matrix_methods\build
move /Y lineq\matrix_methods\matrix_methods.c lineq\matrix_methods\lowlevel\matrix_methods.c

