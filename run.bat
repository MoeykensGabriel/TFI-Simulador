@echo off
:: ============================================================
::  run.bat - Ejecuta el simulador en modo desarrollo
::  Usar esto durante el desarrollo (mas rapido que el .exe)
:: ============================================================
cd /d "%~dp0"
venv\Scripts\python.exe main.py
pause
