@echo off
chcp 65001 > nul
title تشخيص وحل مشاكل تسجيل الدخول

color 0E
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🔧 تشخيص شامل لتسجيل الدخول                     ║
echo ║                                                              ║
echo ║         حل جميع مشاكل الانتقال للواجهة الرئيسية              ║
echo ║                                                              ║
echo ║              RASHID INDUSTRIAL CO.                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🛑 إيقاف جميع العمليات السابقة...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo 🧹 تنظيف الملفات المؤقتة...
del /q "diagnostic_system.db" >nul 2>&1
del /q "simple_system.db" >nul 2>&1
rmdir /s /q "__pycache__" >nul 2>&1

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :run_diagnostic
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :run_diagnostic
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :run_diagnostic

echo ❌ Python غير موجود!
echo.
echo 📥 يرجى تثبيت Python من: https://python.org
pause
exit /b 1

:run_diagnostic
echo ✅ Python: %PYTHON_CMD%

echo 📦 تثبيت Flask إذا لم يكن موجوداً...
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
echo ║                🔧 تشغيل التشخيص الشامل                       ║
echo ║                                                              ║
echo ║  🔍 تشخيص مشاكل تسجيل الدخول                               ║
echo ║  🔧 حل مشاكل الانتقال للواجهة الرئيسية                      ║
echo ║  📊 عرض معلومات تفصيلية عن الأخطاء                         ║
echo ║                                                              ║
echo ║  🌐 http://localhost:5000                                    ║
echo ║  🔑 admin / admin123                                         ║
echo ║                                                              ║
echo ║  🌐 المتصفح سيفتح تلقائياً خلال 3 ثوان                       ║
echo ║  📊 راقب الرسائل التشخيصية في هذه النافذة                   ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل نظام التشخيص الشامل...
echo.
echo ═══════════════ رسائل التشخيص ═══════════════
%PYTHON_CMD% تشخيص_تسجيل_الدخول_شامل.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    تم إيقاف التشخيص                         ║
echo ║                                                              ║
echo ║  📊 تم تشخيص جميع مشاكل تسجيل الدخول                       ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║  🔑 البيانات: admin / admin123                              ║
echo ║                                                              ║
echo ║  💡 إذا استمرت المشاكل:                                     ║
echo ║     • تحقق من رسائل التشخيص أعلاه                          ║
echo ║     • امسح كوكيز المتصفح                                    ║
echo ║     • جرب متصفح آخر                                         ║
echo ║     • استخدم وضع التصفح الخاص                              ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause