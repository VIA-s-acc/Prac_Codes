@echo off
REM Сборка matrix_methods

if exist lineq\matrix_methods\build rmdir /S /Q lineq\matrix_methods\build 
if exist lineq\matrix_methods\lowlevel\matrix_methods.c del /Q lineq\matrix_methods\lowlevel\matrix_methods.c
python lineq\matrix_methods\setup.py build_ext -b build
move /Y build lineq\matrix_methods\build
move /Y lineq\matrix_methods\matrix_methods.c lineq\matrix_methods\lowlevel\matrix_methods.c



REM сборка generator

if exist lineq\generator\build rmdir /S /Q lineq\generator\build 
if exist lineq\generator\lowlevel\generator.c del /Q lineq\generator\lowlevel\generator.c
python lineq\generator\setup.py build_ext -b build
move /Y build lineq\generator\build
move /Y lineq\generator\generator.c lineq\generator\lowlevel\generator.c




REM сборка checker

if exist lineq\checker\build rmdir /S /Q lineq\checker\build 
if exist lineq\checker\lowlevel\checker.c del /Q lineq\checker\lowlevel\checker.c
python lineq\checker\setup.py build_ext -b build
move /Y build lineq\checker\build
move /Y lineq\checker\checker.c lineq\checker\lowlevel\checker.c
