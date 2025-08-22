@echo off
chcp 65001 > nul
title نظام الإدارة الشامل - RASHID INDUSTRIAL CO.

color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                نظام الإدارة الشامل المتعدد الشاشات                ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 خيارات التشغيل:
echo.
echo [1] تشغيل عادي (بدون فتح المتصفح)
echo [2] تشغيل مع فتح المتصفح تلقائياً ⭐
echo [3] تشغيل مع البيانات التجريبية
echo [4] فحص النظام
echo [5] خروج
echo.
set /p choice=اختر رقم الخيار (1-5): 

if "%choice%"=="1" goto :normal_run
if "%choice%"=="2" goto :browser_run
if "%choice%"=="3" goto :sample_data
if "%choice%"=="4" goto :check_system
if "%choice%"=="5" goto :exit
goto :invalid

:invalid
echo ❌ خيار غير صحيح!
timeout /t 2 >nul
goto :start

:normal_run
cls
echo 🚀 تشغيل عادي...
goto :run_app

:browser_run
cls
echo 🌐 تشغيل مع فتح المتصفح...
goto :run_app

:sample_data
cls
echo 📊 إضافة البيانات التجريبية...
python إضافة_بيانات_تجريبية.py
pause
goto :run_app

:check_system
cls
echo 🔍 فحص النظام...
python فحص_سريع.py
pause
goto :start

:exit
echo 👋 وداعاً!
exit /b 0

:run_app
cd /d "%~dp0"

REM البحث عن Python
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :found_python
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :found_python
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :found_python

echo ❌ Python غير مثبت!
echo 📥 يرجى تثبيت Python من: https://python.org
pause
exit /b 1

:found_python
echo ✅ Python متوفر (%PYTHON_CMD%)

REM تثبيت المتطلبات
echo 📦 تحضير المتطلبات...
%PYTHON_CMD% -m pip install flask --quiet --user >nul 2>&1

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        🌟 النظام يعمل الآن                        ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول:                                      ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     📧 أو البريد: admin@rashid.com                          ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║

if "%choice%"=="2" (
    echo ║  🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان                     ║
) else (
    echo ║  🌐 افتح المتصفح يدوياً واذهب للرابط أعلاه                    ║
)

echo ║                                                              ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM تشغيل التطبيق
%PYTHON_CMD% app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  شكراً لاستخدام نظام الإدارة الشامل المتعدد الشاشات              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause