@echo off
setlocal

REM проверка на то, что это Windows или Linux
if "%OS%"=="Windows_NT" (
    set "IS_WINDOWS=true"
) else (
    set "IS_WINDOWS=false"
)

REM цикл по всем модулям
for %%l in (lineq) do (
    for %%i in (matrix_methods generator checker) do (
        REM удаление каталога build
        if exist %%l\%%i\build (
            if "%IS_WINDOWS%"=="true" (
                rmdir /S /Q %%l\%%i\build
            ) else (
                rm -rf %%l/%%i/build
            )
        )
        REM удаление файла lowlevel/matrix_methods.c
        if exist %%l\%%i\lowlevel\%%i.c (
            del /Q %%l\%%i\lowlevel\%%i.c
        )
        REM сборка
        python %%l\%%i\setup.py build_ext -b build
        REM перемещение каталога build
        if "%IS_WINDOWS%"=="true" (
            move /Y build %%l\%%i\build
        ) else (
            mv build %%l/%%i/build
        )
        REM перемещение файла matrix_methods.c
        if "%IS_WINDOWS%"=="true" (
            move /Y %%l\%%i\%%i.c %%l\%%i\lowlevel\%%i.c
        ) else (
            mv %%l/%%i/%%i.c %%l/%%i/lowlevel/%%i.c
        )
    )
)

for %%l in (lineq) do (
    REM запуск тестов 
    echo.
    echo Testing %%l...
    python -m %%l.TEST.test
)