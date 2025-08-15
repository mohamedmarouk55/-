@echo off
chcp 65001 > nul
title تشغيل سريع مباشر - RASHID INDUSTRIAL CO.

color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    تشغيل سريع مباشر                           ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ║                                                              ║
echo ║  🚀 تشغيل فوري للنظام                                        ║
echo ║  🌐 فتح المتصفح تلقائياً                                      ║
echo ║  ⚡ بدون فحوصات معقدة                                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 البحث عن Python...
set PYTHON_CMD=

REM جرب py أولاً
py --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    echo ✅ تم العثور على Python: py
    goto :start_app
)

REM جرب python
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    echo ✅ تم العثور على Python: python
    goto :start_app
)

REM جرب python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    echo ✅ تم العثور على Python: python3
    goto :start_app
)

echo ❌ Python غير مثبت أو غير موجود في PATH
echo.
echo 📥 يرجى تثبيت Python من: https://python.org
echo    تأكد من تحديد "Add Python to PATH" أثناء التثبيت
echo.
pause
exit /b 1

:start_app
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 تشغيل النظام                            ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول:                                     ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان                     ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النظام...

REM فتح المتصفح بعد 3 ثوان
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

REM تشغيل النظام
%PYTHON_CMD% app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  💡 إذا كان النظام يعمل بشكل صحيح:                           ║
echo ║     • الرابط: http://localhost:5000                         ║
echo ║     • البيانات: admin / admin123                           ║
echo ║                                                              ║
echo ║  🔧 إذا واجهت مشاكل:                                         ║
echo ║     • جرب: تشغيل_بدون_أخطاء.bat                            ║
echo ║     • أو: حل_نهائي_شامل.bat                                ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause