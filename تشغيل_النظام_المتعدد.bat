@echo off
chcp 65001 > nul
title نظام الإدارة الشامل المتعدد الشاشات - RASHID INDUSTRIAL CO.

echo.
echo ========================================
echo    نظام الإدارة الشامل المتعدد الشاشات
echo        RASHID INDUSTRIAL CO.
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] فحص Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python أولاً
    echo.
    echo يمكنك تحميل Python من: https://python.org
    pause
    exit /b 1
)

echo ✅ Python متوفر
echo.

echo [2/3] تثبيت المتطلبات...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ فشل في تثبيت المتطلبات
    pause
    exit /b 1
)

echo ✅ تم تثبيت المتطلبات
echo.

echo [3/3] تشغيل النظام...
echo.
echo 🚀 النظام يعمل الآن على: http://localhost:5000
echo.
echo 📋 بيانات تسجيل الدخول:
echo    👤 اسم المستخدم: admin
echo    🔑 كلمة المرور: admin123
echo.
echo ⚠️  لإيقاف النظام اضغط Ctrl+C
echo.

python app.py

echo.
echo تم إيقاف النظام
pause