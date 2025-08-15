@echo off
chcp 65001 > nul
title نظام الإدارة الشامل - RASHID INDUSTRIAL CO.

color 0B
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                نظام الإدارة الشامل المتعدد الشاشات                ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ║                                                              ║
echo ║  🏠 الواجهة الرئيسية    💰 الخزينة        🚗 إدارة السيارات    ║
echo ║  👥 إدخال الموظفين     💸 المصروفات      📊 التقارير         ║
echo ║  ⚙️  الإعدادات         🔐 نظام الأمان     📱 تصميم متجاوب     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 البحث عن Python...

REM محاولة py أولاً (الأكثر شيوعاً في Windows)
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

REM لم يتم العثور على Python
echo ❌ لم يتم العثور على Python!
echo.
echo 📥 يرجى تثبيت Python أولاً:
echo    1. اذهب إلى: https://python.org
echo    2. حمل أحدث إصدار Python
echo    3. تأكد من تحديد "Add Python to PATH"
echo.
echo 🏪 أو من Microsoft Store:
echo    1. افتح Microsoft Store
echo    2. ابحث عن "Python"
echo    3. ثبت Python 3.11 أو أحدث
echo.
echo 📋 ثم شغل هذا الملف مرة أخرى
pause
exit /b 1

:found_python
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    الإصدار: %PYTHON_VERSION%
echo.

echo 📦 تثبيت Flask...
%PYTHON_CMD% -m pip install flask --quiet --disable-pip-version-check --user
if errorlevel 1 (
    echo ⚠️  تحذير: مشكلة في تثبيت Flask
    echo 💡 جاري المحاولة بطريقة أخرى...
    %PYTHON_CMD% -m pip install flask --user
)

echo ✅ تم تحضير المتطلبات
echo.

echo 🗄️  إنشاء قاعدة البيانات...
%PYTHON_CMD% -c "import sqlite3; conn = sqlite3.connect('management_system.db'); conn.close(); print('✅ قاعدة البيانات جاهزة')"

echo.
echo 🚀 بدء تشغيل النظام...
echo.

REM عرض معلومات التشغيل
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        🌟 النظام يعمل الآن                        ║
echo ║                                                              ║
echo ║  🌐 افتح المتصفح واذهب إلى:                                   ║
echo ║     http://localhost:5000                                    ║
echo ║     أو http://127.0.0.1:5000                                ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول:                                      ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     📧 أو البريد: admin@rashid.com                          ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  📋 الشاشات المتاحة:                                          ║
echo ║     🏠 الواجهة الرئيسية  💰 الخزينة  🚗 إدارة السيارات       ║
echo ║     👥 الموظفين  💸 المصروفات  📊 التقارير  ⚙️ الإعدادات    ║
echo ║                                                              ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C أو أغلق هذه النافذة          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM بدء تشغيل التطبيق في الخلفية وفتح المتصفح
echo 🌐 سيتم فتح المتصفح تلقائياً خلال 5 ثوان...

REM تشغيل التطبيق في الخلفية
start /B %PYTHON_CMD% app.py

REM انتظار 5 ثوان ثم فتح المتصفح
timeout /t 5 /nobreak >nul
start http://localhost:5000

REM انتظار إيقاف التطبيق
echo.
echo 🌐 تم فتح المتصفح! إذا لم يفتح تلقائياً، اذهب إلى: http://localhost:5000
echo.
echo ⚠️  لإيقاف النظام: اضغط Ctrl+C
echo.

REM انتظار إنهاء العملية
:wait_loop
timeout /t 1 /nobreak >nul
goto wait_loop

REM رسالة الإغلاق
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  شكراً لاستخدام نظام الإدارة الشامل المتعدد الشاشات              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ║                                                              ║
echo ║  💡 لتشغيل النظام مرة أخرى، شغل هذا الملف                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause