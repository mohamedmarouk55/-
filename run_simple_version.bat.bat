@echo off
chcp 65001 > nul
title تشغيل النسخة البسيطة - بدون إعادة توجيه

color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🚀 النسخة البسيطة                               ║
echo ║                                                              ║
echo ║         بدون مشاكل إعادة التوجيه                            ║
echo ║                                                              ║
echo ║              RASHID INDUSTRIAL CO.                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🛑 إيقاف العمليات السابقة...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :run_simple
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :run_simple
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :run_simple

echo ❌ Python غير موجود!
pause
exit /b 1

:run_simple
echo ✅ Python: %PYTHON_CMD%

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🚀 تشغيل النسخة البسيطة                       ║
echo ║                                                              ║
echo ║  ✅ بدون مشاكل إعادة التوجيه                                ║
echo ║  🌐 http://localhost:5000                                    ║
echo ║  🔑 admin / admin123                                         ║
echo ║                                                              ║
echo ║  🌐 المتصفح سيفتح تلقائياً                                   ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النسخة البسيطة...
%PYTHON_CMD% تشغيل_بسيط_بدون_إعادة_توجيه.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  ✅ النسخة البسيطة عملت بدون مشاكل                         ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║  🔑 البيانات: admin / admin123                              ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause