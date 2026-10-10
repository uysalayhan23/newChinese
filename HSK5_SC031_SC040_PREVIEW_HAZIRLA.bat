@echo off
setlocal
cd /d "%~dp0"
echo.
echo NewChinese HSK5 SC031/034/036/040 - Canonical preview hazirlama
echo Actions calistirilmaz. QA kabulu otomatik yapilmaz.
echo.
where py >nul 2>nul
if not errorlevel 1 (
    py -3 tools\prepare_hsk5_sc031_sc040.py --publish
) else (
    python tools\prepare_hsk5_sc031_sc040.py --publish
)
if errorlevel 1 (
    echo.
    echo DURDURULDU: Once yukaridaki hatayi giderin. Sahne kabul edilmedi.
    pause
    exit /b 1
)
echo.
echo Preview katmanlari GitHub'a yuklendi. Gorsel kimlik ve continuity QA halen bekliyor.
pause
exit /b 0
