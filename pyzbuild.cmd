@echo off
pushd "%~dp0"
setlocal

SET PYTHON=py
SET NAME=etcddump
SET PACKAGE=etcddump

rmdir /q /s build
mkdir build\app

%PYTHON% setup.py bdist_wheel ^
    --dist-dir build

%PYTHON% -m pip install ^
    -r requirements.txt ^
    --target build\app

%PYTHON% -m pip install ^
    --no-index ^
    --no-deps ^
    --find-links build ^
    --target build\app ^
    %NAME%

%PYTHON% -m zipapp ^
    --python "/usr/bin/env python3" ^
    --main "%PACKAGE%.__main__:main" ^
    --output build\%NAME%.pyz ^
    build\app

mkdir build\zip
copy LICENSE build\zip\LICENSE
copy README.rst build\zip\README.rst
copy build\%NAME%.pyz build\zip\%NAME%.pyz

pushd build\zip
%PYTHON% -m zipfile -c ..\%NAME%.zip .
popd

endlocal
popd
