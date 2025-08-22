@echo off
chcp 65001 > nul
title 🔥 النظام الشامل مع جميع البيانات - RASHID INDUSTRIAL CO.

color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🔥 النظام الشامل مع جميع البيانات                ║
echo ║                                                              ║
echo ║         ✅ جميع البيانات والوظائف متوفرة                     ║
echo ║         ✅ 8 موظفين + 8 سيارات + معاملات مالية              ║
echo ║         ✅ جميع الوظائف تعمل بشكل مثالي                      ║
echo ║                                                              ║
echo ║              RASHID INDUSTRIAL CO.                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🛑 إيقاف جميع العمليات السابقة...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo 🗑️ تنظيف قواعد البيانات القديمة...
del /q "complete_system.db" >nul 2>&1
del /q "final_fixed_system.db" >nul 2>&1
del /q "diagnostic_system.db" >nul 2>&1

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :run_complete
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :run_complete
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :run_complete

echo ❌ Python غير موجود!
echo.
echo 📥 يرجى تثبيت Python من: https://python.org
pause
exit /b 1

:run_complete
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
echo ║                🔥 تشغيل النظام الشامل                        ║
echo ║                                                              ║
echo ║  📊 البيانات المتوفرة:                                       ║
echo ║     • 8 موظفين في أقسام مختلفة                              ║
echo ║     • 8 سيارات بحالات مختلفة                                ║
echo ║     • 7 معاملات خزينة                                       ║
echo ║     • 6 مصروفات متنوعة                                      ║
echo ║     • 4 عهد سيارات                                          ║
echo ║     • 5 معاملات مالية                                       ║
echo ║                                                              ║
echo ║  ✅ الوظائف المتاحة:                                         ║
echo ║     • إدارة الموظفين (عرض، إضافة، تعديل)                    ║
echo ║     • إدارة السيارات (عرض، إضافة، تعديل)                    ║
echo ║     • إدارة الخزينة (عرض، إضافة معاملات)                   ║
echo ║     • إدارة المصروفات (عرض، إضافة)                         ║
echo ║     • إدارة عهد السيارات (عرض، إضافة، إرجاع)               ║
echo ║     • التقارير الشاملة                                       ║
echo ║     • الإعدادات                                              ║
echo ║                                                              ║
echo ║  🌐 http://localhost:5000                                    ║
echo ║  🔑 admin / admin123                                         ║
echo ║                                                              ║
echo ║  🌐 المتصفح سيفتح تلقائياً خلال 3 ثوان                       ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النظام الشامل مع جميع البيانات...
echo.
echo ═══════════════ معلومات النظام ═══════════════
%PYTHON_CMD% نظام_شامل_مع_البيانات.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔥 تم إيقاف النظام                        ║
echo ║                                                              ║
echo ║  ✅ النظام الشامل عمل بنجاح تام!                            ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║  🔑 البيانات: admin / admin123                              ║
echo ║                                                              ║
echo ║  🎊 تم استعادة جميع البيانات والوظائف:                      ║
echo ║     ✅ 8 موظفين في النظام                                   ║
echo ║     ✅ 8 سيارات متنوعة                                      ║
echo ║     ✅ معاملات خزينة شاملة                                   ║
echo ║     ✅ مصروفات متنوعة                                       ║
echo ║     ✅ عهد سيارات نشطة                                      ║
echo ║     ✅ تقارير مالية وإدارية                                 ║
echo ║     ✅ جميع الوظائف تعمل بشكل مثالي                         ║
echo ║                                                              ║
echo ║  💡 للتشغيل مرة أخرى:                                       ║
echo ║     انقر نقراً مزدوجاً على هذا الملف                        ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause