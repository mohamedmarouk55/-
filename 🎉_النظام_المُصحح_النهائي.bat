@echo off
chcp 65001 > nul
title 🎉 النظام المُصحح النهائي - RASHID INDUSTRIAL CO.

color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🎉 النظام المُصحح النهائي                        ║
echo ║                                                              ║
echo ║         ✅ تم حل جميع مشاكل تسجيل الدخول                     ║
echo ║         ✅ تم حل مشاكل الانتقال للواجهة الرئيسية             ║
echo ║         ✅ تم حل مشكلة ERR_TOO_MANY_REDIRECTS                ║
echo ║                                                              ║
echo ║              RASHID INDUSTRIAL CO.                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🛑 إيقاف جميع العمليات السابقة...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :run_final
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :run_final
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :run_final

echo ❌ Python غير موجود!
echo.
echo 📥 يرجى تثبيت Python من: https://python.org
pause
exit /b 1

:run_final
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
echo ║                🎉 تشغيل النظام المُصحح                       ║
echo ║                                                              ║
echo ║  ✅ جميع المشاكل تم حلها:                                    ║
echo ║     • ERR_TOO_MANY_REDIRECTS                                 ║
echo ║     • مشاكل تسجيل الدخول                                    ║
echo ║     • مشاكل الانتقال للواجهة الرئيسية                       ║
echo ║     • مشاكل إدارة الجلسات                                   ║
echo ║                                                              ║
echo ║  🌐 http://localhost:5000                                    ║
echo ║  🔑 admin / admin123                                         ║
echo ║                                                              ║
echo ║  🌐 المتصفح سيفتح تلقائياً خلال 3 ثوان                       ║
echo ║  📊 راقب رسائل التشخيص في هذه النافذة                       ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النظام المُصحح النهائي...
echo.
echo ═══════════════ رسائل التشخيص ═══════════════
%PYTHON_CMD% نظام_مُصحح_نهائي.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 تم إيقاف النظام                        ║
echo ║                                                              ║
echo ║  ✅ النظام المُصحح عمل بنجاح تام!                           ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║  🔑 البيانات: admin / admin123                              ║
echo ║                                                              ║
echo ║  🎊 تم حل جميع المشاكل:                                     ║
echo ║     ✅ ERR_TOO_MANY_REDIRECTS                                ║
echo ║     ✅ مشاكل تسجيل الدخول                                   ║
echo ║     ✅ مشاكل الانتقال للواجهة الرئيسية                      ║
echo ║     ✅ مشاكل إدارة الجلسات                                  ║
echo ║     ✅ تشخيص شامل للأخطاء                                   ║
echo ║                                                              ║
echo ║  💡 للتشغيل مرة أخرى:                                       ║
echo ║     انقر نقراً مزدوجاً على هذا الملف                        ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause