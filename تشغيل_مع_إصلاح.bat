@echo off
chcp 65001 > nul
title نظام الإدارة الشامل - إصلاح وتشغيل

color 0C
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                نظام الإدارة الشامل - إصلاح وتشغيل                ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM البحث عن Python
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
echo 🔧 إصلاح قاعدة البيانات...
%PYTHON_CMD% -c "
import sqlite3
import hashlib

# إنشاء/فتح قاعدة البيانات
conn = sqlite3.connect('management_system.db')
cursor = conn.cursor()

# إنشاء جدول المستخدمين
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# حذف المستخدم الموجود وإنشاء جديد
cursor.execute('DELETE FROM users WHERE username = \"admin\" OR email = \"admin@rashid.com\"')

# إنشاء مستخدم admin
password_hash = hashlib.md5('admin123'.encode()).hexdigest()
cursor.execute('''
    INSERT INTO users (username, email, password_hash, role, is_active)
    VALUES (?, ?, ?, ?, ?)
''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))

conn.commit()
conn.close()
print('✅ تم إصلاح قاعدة البيانات وإنشاء مستخدم admin')
"

if errorlevel 1 (
    echo ❌ فشل في إصلاح قاعدة البيانات
    pause
    exit /b 1
)

echo.
echo 📦 تثبيت المتطلبات...
%PYTHON_CMD% -m pip install flask --quiet --user >nul 2>&1

echo ✅ تم الإصلاح والتحضير
echo.

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        🌟 النظام يعمل الآن                        ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول المُصلحة:                             ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     📧 أو البريد: admin@rashid.com                          ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان                     ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM تشغيل النظام
%PYTHON_CMD% app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  تم إصلاح مشكلة تسجيل الدخول                                  ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause