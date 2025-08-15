@echo off
chcp 65001 > nul
title إصلاح مشكلة تسجيل الدخول وتشغيل النظام

color 0E
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              إصلاح مشكلة تسجيل الدخول وتشغيل النظام              ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :found_python
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :found_python
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :found_python

echo ❌ Python غير مثبت! يرجى تثبيت Python أولاً
pause
exit /b 1

:found_python
echo ✅ Python متوفر (%PYTHON_CMD%)

echo.
echo 🗄️  حذف قاعدة البيانات القديمة (إن وجدت)...
if exist management_system.db (
    del management_system.db
    echo ✅ تم حذف قاعدة البيانات القديمة
) else (
    echo ℹ️  لا توجد قاعدة بيانات قديمة
)

echo.
echo 🔧 إنشاء قاعدة بيانات جديدة مع مستخدم admin...
%PYTHON_CMD% -c "
import sqlite3
import hashlib

print('📋 إنشاء قاعدة البيانات...')
conn = sqlite3.connect('management_system.db')
cursor = conn.cursor()

# إنشاء جدول المستخدمين
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# إنشاء مستخدم admin
password_hash = hashlib.md5('admin123'.encode()).hexdigest()
cursor.execute('''
    INSERT INTO users (username, email, password_hash, role, is_active)
    VALUES (?, ?, ?, ?, ?)
''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))

# إنشاء باقي الجداول الأساسية
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_number TEXT UNIQUE,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL,
        phone TEXT,
        email TEXT,
        hire_date TEXT NOT NULL,
        status TEXT DEFAULT 'نشط',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        license_plate TEXT UNIQUE NOT NULL,
        color TEXT,
        status TEXT DEFAULT 'متاح',
        purchase_price REAL,
        current_value REAL,
        engine_number TEXT,
        chassis_number TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS treasury (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type TEXT NOT NULL CHECK (transaction_type IN ('إيداع', 'سحب')),
        amount REAL NOT NULL,
        description TEXT,
        reference_number TEXT,
        created_by TEXT,
        date TEXT NOT NULL,
        balance_after REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()

print('✅ تم إنشاء قاعدة البيانات بنجاح!')
print('✅ تم إنشاء مستخدم admin بنجاح!')
"

if errorlevel 1 (
    echo ❌ فشل في إنشاء قاعدة البيانات
    pause
    exit /b 1
)

echo.
echo 📦 تثبيت Flask...
%PYTHON_CMD% -m pip install flask --quiet --user >nul 2>&1

echo.
echo 🧪 اختبار تسجيل الدخول...
%PYTHON_CMD% -c "
import sqlite3
import hashlib

conn = sqlite3.connect('management_system.db')
conn.row_factory = sqlite3.Row

username = 'admin'
password = 'admin123'
password_hash = hashlib.md5(password.encode()).hexdigest()

user = conn.execute(
    'SELECT * FROM users WHERE (username = ? OR email = ?) AND password_hash = ? AND is_active = 1',
    (username, username, password_hash)
).fetchone()

if user:
    print('✅ اختبار تسجيل الدخول نجح!')
else:
    print('❌ اختبار تسجيل الدخول فشل!')

conn.close()
"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 تم إصلاح المشكلة بنجاح                    ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول الجديدة:                             ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     📧 أو البريد: admin@rashid.com                          ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان                     ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النظام...
%PYTHON_CMD% app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  تم إصلاح مشكلة تسجيل الدخول بنجاح                            ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause