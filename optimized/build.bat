@echo off
setlocal

REM проверка на то, что это Windows или Linux
if "%OS%"=="Windows_NT" (
    set "IS_WINDOWS=true"
) else (
    set "IS_WINDOWS=false"
)

REM цикл по всем модулям
for %%i in (matrix_methods generator checker) do (
    REM удаление каталога build
    if exist lineq\%%i\build (
        if "%IS_WINDOWS%"=="true" (
            rmdir /S /Q lineq\%%i\build
        ) else (
            rm -rf lineq/%%i/build
        )
    )
    REM удаление файла lowlevel/matrix_methods.c
    if exist lineq\%%i\lowlevel\%%i.c (
        del /Q lineq\%%i\lowlevel\%%i.c
    )
    REM сборка
    python lineq\%%i\setup.py build_ext -b build
    REM перемещение каталога build
    if "%IS_WINDOWS%"=="true" (
        move /Y build lineq\%%i\build
    ) else (
        mv build lineq/%%i/build
    )
    REM перемещение файла matrix_methods.c
    if "%IS_WINDOWS%"=="true" (
        move /Y lineq\%%i\%%i.c lineq\%%i\lowlevel\%%i.c
    ) else (
        mv lineq/%%i/%%i.c lineq/%%i/lowlevel/%%i.c
    )
)

