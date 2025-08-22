@echo off
echo ========================================
echo       نظام إدارة شامل - التثبيت والتشغيل
echo ========================================
echo.

echo التحقق من وجود Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python غير مثبت على النظام
    echo يرجى تثبيت Python من الرابط التالي:
    echo https://www.python.org/downloads/
    echo.
    echo بعد التثبيت، قم بتشغيل هذا الملف مرة أخرى
    pause
    exit /b 1
)

echo Python مثبت بنجاح!
echo.

echo تثبيت المكتبات المطلوبة...
pip install Flask==2.3.3 Werkzeug==2.3.7 Jinja2==3.1.2

echo.
echo تشغيل التطبيق...
echo.

python run_app.py

pause