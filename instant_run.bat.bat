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
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت!
    echo 📥 يرجى تثبيت Python من: https://python.org
    pause
    exit /b 1
)

echo ✅ Python متوفر
echo.

echo 📦 تثبيت المتطلبات...
python -m pip install flask --quiet --disable-pip-version-check
if errorlevel 1 (
    echo ⚠️  تحذير: قد تكون هناك مشكلة في تثبيت Flask
)

echo ✅ تم تثبيت المتطلبات
echo.

echo 🚀 تشغيل النظام...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                      النظام يعمل الآن                       ║
echo ║                                                            ║
echo ║  🌐 الرابط: http://localhost:5000                         ║
echo ║                                                            ║
echo ║  🔑 بيانات تسجيل الدخول:                                   ║
echo ║     👤 اسم المستخدم: admin                               ║
echo ║     🔑 كلمة المرور: admin123                             ║
echo ║                                                            ║
echo ║  ⚠️  لإيقاف النظام اضغط Ctrl+C                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

python app.py

echo.
echo تم إيقاف النظام
pause