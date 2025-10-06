@echo off
setlocal

REM Garantir que o CWD seja a pasta deste script (onde fica criptografia_janela.py)
cd /d "%~dp0"

title Sistema de Criptografia - Clinica 2K25
color 0A

echo.
echo ================================================================
echo    SISTEMA DE CRIPTOGRAFIA DE DADOS - CLINICA 2K25
echo ================================================================
echo.

echo Procurando Python instalado no sistema...

REM Tentar diferentes caminhos comuns do Python
set PYTHON_FOUND=0

REM Python 3.13
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe
    set PYTHON_FOUND=1
    goto :found
)

REM Python 3.12
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe
    set PYTHON_FOUND=1
    goto :found
)

REM Python 3.11
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
    set PYTHON_FOUND=1
    goto :found
)

REM Python 3.10
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe
    set PYTHON_FOUND=1
    goto :found
)

REM Python no PATH do sistema
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_PATH=python
    set PYTHON_FOUND=1
    goto :found
)

:notfound
echo.
echo ERRO: Python nao encontrado no sistema!
echo.
echo Para resolver este problema:
echo 1. Instale o Python em: https://www.python.org/downloads/
echo 2. Durante a instalacao, marque "Add Python to PATH"
echo 3. Reinicie o computador apos a instalacao
echo 4. Execute este script novamente
echo.
pause
exit /b 1

:found
echo Python encontrado: %PYTHON_PATH%
echo.

REM Verificar se o arquivo existe
if not exist "criptografia_janela.py" (
    echo ERRO: Arquivo 'criptografia_janela.py' nao encontrado!
    echo Certifique-se de executar este script na pasta correta do projeto.
    pause
    exit /b 1
)

REM Verificar se o banco existe
if not exist "database.db" (
    echo ERRO: Banco de dados 'database.db' nao encontrado!
    echo Certifique-se de que o arquivo database.db existe na pasta atual.
    pause
    exit /b 1
)

echo Abrindo janela de criptografia...
echo.

REM Executar a janela de criptografia
"%PYTHON_PATH%" "criptografia_janela.py"
