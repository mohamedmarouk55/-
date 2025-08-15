@echo off
chcp 65001 > nul
title نظام الإدارة الشامل - RASHID INDUSTRIAL CO.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              نظام الإدارة الشامل المتعدد الشاشات              ║
echo ║                  RASHID INDUSTRIAL CO.                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 فحص Python...

REM محاولة استخدام py أولاً
py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر عبر py
    set PYTHON_CMD=py
    goto :install_deps
)

REM محاولة استخدام python
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر عبر python
    set PYTHON_CMD=python
    goto :install_deps
)

REM محاولة استخدام python3
python3 --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python متوفر عبر python3
    set PYTHON_CMD=python3
    goto :install_deps
)

echo ❌ Python غير مثبت أو غير متاح!
echo.
echo 📥 يرجى تثبيت Python من: https://python.org
echo 💡 تأكد من تحديد "Add Python to PATH" أثناء التثبيت
echo.
echo أو يمكنك تحميل Python من Microsoft Store
pause
exit /b 1

:install_deps
echo.
echo 📦 تثبيت المتطلبات...
%PYTHON_CMD% -m pip install flask --quiet --disable-pip-version-check
if errorlevel 1 (
    echo ⚠️  تحذير: قد تكون هناك مشكلة في تثبيت Flask
    echo 💡 تأكد من اتصال الإنترنت
)

echo ✅ تم تثبيت المتطلبات
echo.

echo 🚀 تشغيل النظام...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                      النظام يعمل الآن                       ║
echo ║                                                            ║
echo ║  🌐 الرابط: http://localhost:5000                         ║
echo ║  🌐 أو:     http://127.0.0.1:5000                         ║
echo ║                                                            ║
echo ║  🔑 بيانات تسجيل الدخول:                                   ║
echo ║     👤 اسم المستخدم: admin                               ║
echo ║     📧 أو البريد: admin@rashid.com                       ║
echo ║     🔑 كلمة المرور: admin123                             ║
echo ║                                                            ║
echo ║  ⚠️  لإيقاف النظام اضغط Ctrl+C                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

%PYTHON_CMD% app.py

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                      ║
echo ║                                                            ║
echo ║  شكراً لاستخدام نظام الإدارة الشامل المتعدد الشاشات        ║
echo ║                RASHID INDUSTRIAL CO.                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
pause