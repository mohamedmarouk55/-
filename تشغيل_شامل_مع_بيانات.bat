@echo off
chcp 65001 > nul
title نظام الإدارة الشامل المتعدد الشاشات - RASHID INDUSTRIAL CO.

color 0A
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

echo [1/5] فحص Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python أولاً
    echo.
    echo 📥 يمكنك تحميل Python من: https://python.org
    echo 💡 تأكد من تحديد "Add Python to PATH" أثناء التثبيت
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% متوفر
echo.

echo [2/5] تثبيت المتطلبات...
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo ❌ فشل في تثبيت المتطلبات
    echo 💡 تأكد من اتصال الإنترنت وحاول مرة أخرى
    pause
    exit /b 1
)

echo ✅ تم تثبيت المتطلبات بنجاح
echo.

echo [3/5] إنشاء قاعدة البيانات...
python -c "from database import DatabaseManager; db = DatabaseManager(); print('✅ تم إنشاء قاعدة البيانات')"
if errorlevel 1 (
    echo ❌ فشل في إنشاء قاعدة البيانات
    pause
    exit /b 1
)

echo.

echo [4/5] إضافة البيانات التجريبية...
set /p ADD_SAMPLE=هل تريد إضافة بيانات تجريبية؟ (y/n): 
if /i "%ADD_SAMPLE%"=="y" (
    python إضافة_بيانات_تجريبية.py
    if errorlevel 1 (
        echo ⚠️  تحذير: فشل في إضافة البيانات التجريبية
        echo 💡 يمكنك المتابعة بدون البيانات التجريبية
    )
) else (
    echo ⏭️  تم تخطي إضافة البيانات التجريبية
)

echo.

echo [5/5] تشغيل النظام...
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        🚀 النظام يعمل الآن                        ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║  🌐 أو:     http://127.0.0.1:5000                           ║
echo ║                                                              ║
echo ║  📋 بيانات تسجيل الدخول:                                      ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     📧 أو البريد: admin@rashid.com                          ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  ⚠️  لإيقاف النظام اضغط Ctrl+C                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔄 بدء تشغيل الخادم...
echo.

python app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  شكراً لاستخدام نظام الإدارة الشامل المتعدد الشاشات              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause