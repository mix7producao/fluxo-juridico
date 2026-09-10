@echo off
chcp 65001 >nul
title Publicar instruções no GitHub
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ferramentas\publicar-no-github.ps1"
if errorlevel 1 (
  echo.
  echo A publicação não foi concluída. Leia a mensagem acima.
  pause
  exit /b 1
)
echo.
echo PUBLICAÇÃO CONCLUÍDA.
pause
