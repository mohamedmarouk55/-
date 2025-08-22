@echo off
chcp 65001 > nul
title نظام الإدارة - RASHID INDUSTRIAL CO.

color 0A
cls
echo.
echo ════════════════════════════════════════════════════════════
echo           نظام الإدارة الشامل - RASHID INDUSTRIAL CO.
echo ════════════════════════════════════════════════════════════
echo.
echo 🚀 جاري التشغيل...
echo 🌐 سيتم فتح المتصفح تلقائياً
echo.

cd /d "%~dp0"

REM البحث عن Python بطريقة مبسطة
py --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ يرجى تثبيت Python من: https://python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py
)

REM تثبيت Flask
%PYTHON_CMD% -m pip install flask --quiet --user >nul 2>&1

echo ✅ جاهز!
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    النظام يعمل الآن                        ║
echo ║                                                            ║
echo ║  🌐 سيفتح المتصفح تلقائياً                                ║
echo ║  🔑 اسم المستخدم: admin                                  ║
echo ║  🔑 كلمة المرور: admin123                                ║
echo ║                                                            ║
echo ║  ⚠️  للإيقاف: أغلق هذه النافذة                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM تشغيل النظام
%PYTHON_CMD% app.py

pause