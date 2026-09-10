@echo off
chcp 65001 >nul
title Atualizar pacote único para ChatGPT e Claude
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ferramentas\gerar-pacote-unico.ps1"
if errorlevel 1 (
  echo.
  echo O pacote não foi atualizado. Leia a mensagem acima.
  pause
  exit /b 1
)
echo.
echo PACOTE ÚNICO ATUALIZADO.
pause
