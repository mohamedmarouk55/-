@echo off
chcp 65001 > nul
title اختبار تسجيل الدخول - RASHID INDUSTRIAL CO.

color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🧪 اختبار تسجيل الدخول                      ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ║                                                              ║
echo ║  🔍 اختبار مبسط لتسجيل الدخول                                ║
echo ║  ⚡ بدون قاعدة بيانات أو تعقيدات                             ║
echo ║  🌐 على المنفذ 5001 لتجنب التداخل                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :found_python
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :found_python
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :found_python

echo ❌ Python غير مثبت!
pause
exit /b 1

:found_python
echo ✅ Python متوفر (%PYTHON_CMD%)

echo.
echo 📦 تثبيت Flask...
%PYTHON_CMD% -m pip install flask --quiet --user >nul 2>&1

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🧪 بدء اختبار تسجيل الدخول                  ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5001                           ║
echo ║                                                              ║
echo ║  🔑 بيانات الاختبار:                                         ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     📧 أو البريد: admin@rashid.com                          ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  💡 هذا اختبار مبسط لتسجيل الدخول فقط                       ║
echo ║  ✅ إذا نجح الاختبار، فالمشكلة في النظام الأساسي             ║
echo ║  ❌ إذا فشل الاختبار، فالمشكلة في Python أو Flask           ║
echo ║                                                              ║
echo ║  ⚠️  لإيقاف الاختبار: اضغط Ctrl+C                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل اختبار تسجيل الدخول...
echo.

REM فتح المتصفح بعد 3 ثوان
start "" timeout /t 3 /nobreak >nul && start http://localhost:5001

REM تشغيل الاختبار
%PYTHON_CMD% test_login.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       انتهى الاختبار                          ║
echo ║                                                              ║
echo ║  📊 نتائج الاختبار:                                          ║
echo ║     • إذا تمكنت من تسجيل الدخول = المشكلة في النظام الأساسي   ║
echo ║     • إذا لم تتمكن = المشكلة في Python أو Flask             ║
echo ║                                                              ║
echo ║  🔧 الخطوة التالية:                                          ║
echo ║     • إذا نجح الاختبار: شغل ULTIMATE_FIX.bat               ║
echo ║     • إذا فشل: أعد تثبيت Python و Flask                    ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause