@echo off
chcp 65001 > nul
title نظام الإدارة الشامل - RASHID INDUSTRIAL CO.

color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                نظام الإدارة الشامل المتعدد الشاشات                ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ║                                                              ║
echo ║  🌐 سيتم فتح المتصفح تلقائياً عند جاهزية النظام               ║
echo ║  🚀 تشغيل سريع ومحسن                                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM البحث عن Python
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :found
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :found
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :found

echo ❌ Python غير مثبت!
echo 📥 حمل Python من: https://python.org
echo 🏪 أو من Microsoft Store
pause
exit /b 1

:found
echo ✅ Python متوفر (%PYTHON_CMD%)

REM تثبيت Flask بصمت
echo 📦 تحضير المتطلبات...
%PYTHON_CMD% -m pip install flask --quiet --user >nul 2>&1

echo ✅ جاهز للتشغيل
echo.

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        🌟 بدء التشغيل                          ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║                                                              ║
echo ║  🔑 بيانات الدخول:                                           ║
echo ║     👤 المستخدم: admin                                      ║
echo ║     🔑 المرور: admin123                                      ║
echo ║                                                              ║
echo ║  🌐 سيفتح المتصفح تلقائياً خلال 3 ثوان                      ║
echo ║  ⚠️  للإيقاف: Ctrl+C                                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM تشغيل النظام (سيفتح المتصفح تلقائياً من داخل Python)
%PYTHON_CMD% app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  شكراً لاستخدام نظام RASHID INDUSTRIAL CO.                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause