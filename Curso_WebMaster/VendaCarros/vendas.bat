@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=py"
where py >nul 2>&1
if errorlevel 1 set "PYTHON=python"
where %PYTHON% >nul 2>&1
if errorlevel 1 (
	echo Python nao foi encontrado. Instale Python ou ajuste o PATH.
	exit /b 1
)

echo Iniciando o servidor Flask...
echo A pagina sera aberta no navegador. Pressione Ctrl+C para parar o servidor.
%PYTHON% app.py

endlocal