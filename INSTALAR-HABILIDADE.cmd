@echo off
chcp 65001 >nul
title Instalar organização de casos jurídicos
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ferramentas\instalar-habilidade.ps1"
if errorlevel 1 (
  echo.
  echo A instalação não foi concluída. Leia a mensagem acima.
  pause
  exit /b 1
)
echo.
echo INSTALAÇÃO CONCLUÍDA.
echo Agora abra a pasta do caso e use a habilidade organizar-caso-juridico.
pause
