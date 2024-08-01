#!/bin/bash

# Определение, что это Windows или Linux
if [[ "$OS" == "Windows_NT" ]]; then
    IS_WINDOWS=true
else
    IS_WINDOWS=false
fi

# Цикл по всем модулям
for module in matrix_methods generator checker; do
    # Удаление каталога build
    if [[ -d "lineq/$module/build" ]]; then
        if [[ "$IS_WINDOWS" == true ]]; then
            rm -rf "lineq\\$module\\build"
        else
            rm -rf "lineq/$module/build"
        fi
    fi

    # Удаление файла lowlevel/matrix_methods.c
    if [[ -f "lineq/$module/lowlevel/$module.c" ]]; then
        rm -f "lineq/$module/lowlevel/$module.c"
    fi  

    # Сборка
    python lineq/$module/setup.py build_ext -b build

    # Перемещение каталога build
    if [[ "$IS_WINDOWS" == true ]]; then
        mv -f build "lineq\\$module\\build"
    else
        mv build "lineq/$module/build"
    fi

    # Перемещение файла matrix_methods.c
    if [[ "$IS_WINDOWS" == true ]]; then
        mv -f "lineq\\$module\\$module.c" "lineq\\$module\\lowlevel\\$module.c"
    else
        mv "lineq/$module/$module.c" "lineq/$module/lowlevel/$module.c"
    fi
done
