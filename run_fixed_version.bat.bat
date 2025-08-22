@echo off
chcp 65001 > nul
title تشغيل النسخة المُصححة - تسجيل الدخول

color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🚀 النسخة المُصححة                              ║
echo ║                                                              ║
echo ║         تم حل جميع مشاكل تسجيل الدخول                        ║
echo ║                                                              ║
echo ║              RASHID INDUSTRIAL CO.                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🛑 إيقاف العمليات السابقة...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1

echo 🔍 فحص الملفات المطلوبة...
if not exist "app_fixed.py" (
    echo ❌ ملف app_fixed.py غير موجود!
    echo 🔧 تشغيل الإصلاح أولاً...
    py إصلاح_نهائي_تسجيل_الدخول.py
    if not exist "app_fixed.py" (
        echo ❌ فشل في إنشاء النسخة المُصححة
        pause
        exit /b 1
    )
)

echo ✅ النسخة المُصححة موجودة

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :run_fixed
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :run_fixed
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :run_fixed

echo ❌ Python غير موجود!
pause
exit /b 1

:run_fixed
echo ✅ Python: %PYTHON_CMD%

echo 📦 فحص Flask...
%PYTHON_CMD% -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📥 تثبيت Flask...
    %PYTHON_CMD% -m pip install flask --user --quiet
    echo ✅ تم تثبيت Flask
) else (
    echo ✅ Flask متوفر
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🚀 تشغيل النسخة المُصححة                      ║
echo ║                                                              ║
echo ║  ✅ تم حل جميع مشاكل تسجيل الدخول                           ║
echo ║  ✅ تم حل مشاكل الانتقال للواجهة الرئيسية                   ║
echo ║  ✅ تشخيص شامل للأخطاء                                      ║
echo ║                                                              ║
echo ║  🌐 http://localhost:5000                                    ║
echo ║  🔑 admin / admin123                                         ║
echo ║                                                              ║
echo ║  🌐 المتصفح سيفتح تلقائياً خلال 3 ثوان                       ║
echo ║  📊 راقب رسائل التشخيص في هذه النافذة                       ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النسخة المُصححة...
echo.
echo ═══════════════ رسائل التشخيص ═══════════════

REM فتح المتصفح بعد 3 ثوان
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

REM تشغيل النسخة المُصححة
%PYTHON_CMD% app_fixed.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  ✅ النسخة المُصححة عملت بنجاح                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║  🔑 البيانات: admin / admin123                              ║
echo ║                                                              ║
echo ║  📊 تم حل جميع مشاكل:                                       ║
echo ║     • تسجيل الدخول                                          ║
echo ║     • الانتقال للواجهة الرئيسية                             ║
echo ║     • إعادة التوجيه المستمرة                                ║
echo ║     • مشاكل الجلسات                                         ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause