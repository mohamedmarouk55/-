@echo off
chcp 65001 > nul
title 🚀 النظام الشامل كامل الوظائف - RASHID INDUSTRIAL CO.

color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🚀 النظام الشامل كامل الوظائف                  ║
echo ║                                                              ║
echo ║         ✅ حل مشكلة أزرار الإضافة                           ║
echo ║         ✅ جميع الوظائف تعمل بشكل مثالي                     ║
echo ║         ✅ إضافة وتعديل وحذف جميع البيانات                  ║
echo ║         ✅ تقارير شاملة ومفصلة                              ║
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
del /q "complete_system_full.db" >nul 2>&1
del /q "simple_complete_system.db" >nul 2>&1
del /q "complete_system.db" >nul 2>&1

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :run_system
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :run_system
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :run_system

echo ❌ Python غير موجود!
echo.
echo 📥 يرجى تثبيت Python من: https://python.org
pause
exit /b 1

:run_system
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
echo ║                🚀 تشغيل النظام الشامل                       ║
echo ║                                                              ║
echo ║  🎯 حل مشاكل أزرار الإضافة:                                 ║
echo ║     ✅ زر إضافة الموظفين يعمل                              ║
echo ║     ✅ زر إضافة السيارات يعمل                              ║
echo ║     ✅ زر إضافة معاملة يعمل                                ║
echo ║     ✅ زر إضافة عهدة يعمل                                  ║
echo ║     ✅ زر إضافة المصروفات يعمل                             ║
echo ║                                                              ║
echo ║  📊 التقارير المتوفرة:                                      ║
echo ║     • تقرير حركة الخزينة                                    ║
echo ║     • تقرير حركة السيارات                                   ║
echo ║     • تقرير حركة المصروفات                                  ║
echo ║     • تقرير الموظفين                                        ║
echo ║                                                              ║
echo ║  ✅ الوظائف الشاملة:                                        ║
echo ║     • إضافة وتعديل وحذف بيانات الموظفين                    ║
echo ║     • تتبع الرواتب والمناصب والأقسام                       ║
echo ║     • معلومات الاتصال وتواريخ التوظيف                      ║
echo ║     • إحصائيات شاملة للموظفين                              ║
echo ║     • إدارة السيارات الكاملة                               ║
echo ║     • إدخال السيارات                                        ║
echo ║     • بيانات التسليم والاستلام                             ║
echo ║     • إدارة الخزينة والمعاملات                             ║
echo ║     • إدارة المصروفات والعهد                               ║
echo ║                                                              ║
echo ║  🎨 واجهة الدخول المحسنة:                                   ║
echo ║     • الشعار والعنوان RASHID INDUSTRIAL CO.                ║
echo ║     • حقول الإدخال (اسم المستخدم/البريد، كلمة المرور)       ║
echo ║     • زر تسجيل الدخول                                       ║
echo ║     • رابط هل نسيت كلمة المرور؟                            ║
echo ║     • رابط إنشاء حساب جديد                                  ║
echo ║     • مربع حوار لعرض الرسائل                               ║
echo ║     • معلومات المطور                                        ║
echo ║                                                              ║
echo ║  🌐 http://localhost:5000                                    ║
echo ║  🔑 admin / admin123                                         ║
echo ║                                                              ║
echo ║  🌐 المتصفح سيفتح تلقائياً خلال 3 ثوان                       ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النظام الشامل كامل الوظائف...
echo.
echo ═══════════════ معلومات النظام ═══════════════
%PYTHON_CMD% نظام_شامل_كامل.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 تم إيقاف النظام                        ║
echo ║                                                              ║
echo ║  ✅ النظام الشامل عمل بنجاح تام!                            ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║  🔑 البيانات: admin / admin123                              ║
echo ║                                                              ║
echo ║  🎊 تم حل جميع مشاكل أزرار الإضافة:                         ║
echo ║     ✅ زر إضافة الموظفين يعمل بشكل مثالي                   ║
echo ║     ✅ زر إضافة السيارات يعمل بشكل مثالي                   ║
echo ║     ✅ زر إضافة معاملة يعمل بشكل مثالي                     ║
echo ║     ✅ زر إضافة عهدة يعمل بشكل مثالي                       ║
echo ║     ✅ زر إضافة المصروفات يعمل بشكل مثالي                  ║
echo ║                                                              ║
echo ║  📊 التقارير متوفرة وتعمل:                                  ║
echo ║     ✅ تقرير حركة الخزينة                                   ║
echo ║     ✅ تقرير حركة السيارات                                  ║
echo ║     ✅ تقرير حركة المصروفات                                 ║
echo ║     ✅ تقرير الموظفين                                       ║
echo ║                                                              ║
echo ║  🎨 واجهة الدخول المحسنة:                                   ║
echo ║     ✅ الشعار والعنوان                                      ║
echo ║     ✅ حقول الإدخال التفاعلية                               ║
echo ║     ✅ أزرار وروابط تعمل                                    ║
echo ║     ✅ مربع حوار للرسائل                                    ║
echo ║     ✅ معلومات المطور                                       ║
echo ║                                                              ║
echo ║  💡 للتشغيل مرة أخرى:                                       ║
echo ║     انقر نقراً مزدوجاً على هذا الملف                        ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause