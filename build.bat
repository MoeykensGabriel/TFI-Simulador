@echo off
:: ============================================================
::  build.bat - Genera el archivo .exe del simulador
::  Ejecutar desde la carpeta TFI-Simulador con doble click
:: ============================================================
echo.
echo  [BUILD] Generando ejecutable...
echo.

venv\Scripts\pyinstaller.exe ^
    --onefile ^
    --windowed ^
    --name "Simulador_EWaste" ^
    --distpath dist ^
    --workpath build_temp ^
    --specpath build_temp ^
    main.py

echo.
if exist "dist\Simulador_EWaste.exe" (
    echo  [OK] Ejecutable generado exitosamente en: dist\Simulador_EWaste.exe
) else (
    echo  [ERROR] Algo fallo. Revisar el log de arriba.
)
echo.
pause
