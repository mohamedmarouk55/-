@echo off
chcp 65001 > nul
title نظام الإدارة الشامل - RASHID INDUSTRIAL CO.

color 0B
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                نظام الإدارة الشامل المتعدد الشاشات                ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ║                                                              ║
echo ║  🌐 سيتم فتح المتصفح تلقائياً عند جاهزية النظام               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 البحث عن Python...

REM محاولة py أولاً
py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ تم العثور على Python عبر 'py'
    set PYTHON_CMD=py
    goto :found_python
)

REM محاولة python
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ تم العثور على Python عبر 'python'
    set PYTHON_CMD=python
    goto :found_python
)

REM محاولة python3
python3 --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ تم العثور على Python عبر 'python3'
    set PYTHON_CMD=python3
    goto :found_python
)

echo ❌ لم يتم العثور على Python!
echo 📥 يرجى تثبيت Python من: https://python.org
pause
exit /b 1

:found_python
echo.
echo 📦 تثبيت Flask...
%PYTHON_CMD% -m pip install flask --quiet --disable-pip-version-check --user >nul 2>&1

echo ✅ تم تحضير المتطلبات
echo.

echo 🚀 بدء تشغيل النظام...
echo.

REM إنشاء ملف مؤقت لفتح المتصفح
echo @echo off > open_browser.bat
echo timeout /t 8 /nobreak ^>nul >> open_browser.bat
echo start http://localhost:5000 >> open_browser.bat
echo del "%%~f0" >> open_browser.bat

REM تشغيل فتح المتصفح في الخلفية
start /min open_browser.bat

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        🌟 النظام يعمل الآن                        ║
echo ║                                                              ║
echo ║  🌐 سيتم فتح المتصفح تلقائياً خلال 8 ثوان                     ║
echo ║     أو اذهب يدوياً إلى: http://localhost:5000                ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول:                                      ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     📧 أو البريد: admin@rashid.com                          ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C أو أغلق هذه النافذة          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM تشغيل التطبيق
%PYTHON_CMD% app.py

REM رسالة الإغلاق
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  شكراً لاستخدام نظام الإدارة الشامل المتعدد الشاشات              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause