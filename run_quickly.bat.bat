@echo off
chcp 65001 >nul
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██           RASHID INDUSTRIAL CO.                            ██
echo ██           نظام الإدارة الشامل                              ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 بدء تشغيل النظام...
echo.

REM التحقق من وجود Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ خطأ: Python غير مثبت على النظام
    echo.
    echo 📥 يرجى تثبيت Python من الرابط التالي:
    echo    https://www.python.org/downloads/
    echo.
    echo ⚠️  تأكد من تحديد "Add Python to PATH" أثناء التثبيت
    echo.
    pause
    exit /b 1
)

echo ✅ Python مثبت بنجاح
echo.

echo 📦 تثبيت المكتبات المطلوبة...
pip install Flask==2.3.3 Werkzeug==2.3.7 Jinja2==3.1.2 MarkupSafe==2.1.3 itsdangerous==2.1.2 click==8.1.7 blinker==1.6.3 >nul 2>&1

if %errorlevel% neq 0 (
    echo ❌ خطأ في تثبيت المكتبات
    echo 🔄 جاري المحاولة مرة أخرى...
    pip install -r requirements.txt
)

echo ✅ تم تثبيت المكتبات بنجاح
echo.

echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██                    🔐 معلومات تسجيل الدخول                ██
echo ██                                                            ██
echo ██  👤 اسم المستخدم: admin                                   ██
echo ██  📧 أو البريد: admin@rashid.com                           ██
echo ██  🔑 كلمة المرور: admin123                                 ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

echo 🌐 تشغيل الخادم...
echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🎉 النظام يعمل الآن على:                                 ██
echo ██     http://localhost:5000                                  ██
echo ██                                                            ██
echo ██  📱 يمكن الوصول من أي جهاز على نفس الشبكة               ██
echo ██  ⏹️  لإيقاف النظام: اضغط Ctrl+C                          ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

REM فتح المتصفح تلقائياً بعد 3 ثوان
start "" timeout /t 3 /nobreak >nul && start http://localhost:5000

REM تشغيل التطبيق
python app.py

echo.
echo 👋 شكراً لاستخدام نظام RASHID INDUSTRIAL CO.
pause