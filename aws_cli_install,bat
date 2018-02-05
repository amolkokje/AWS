@setlocal enabledelayedexpansion
@echo off

:: check windows OS architecture type
SET ARCH_TYPE="32"
wmic OS get OSArchitecture | find /i "64"
if not errorlevel 1 (
    SET ARCH_TYPE=64
)

:: download installer
powershell (New-Object System.Net.WebClient).DownloadFile('https://s3.amazonaws.com/aws-cli/AWSCLI%ARCH_TYPE%.msi','AWSCLI%ARCH_TYPE%.msi')

:: run installer
start AWSCLI%ARCH_TYPE%.msi

endlocal
