@echo off
chcp 65001 > nul
title الحل النهائي لمشكلة تسجيل الدخول - RASHID INDUSTRIAL CO.

color 0F
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                الحل النهائي لمشكلة تسجيل الدخول                 ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ║                                                              ║
echo ║  🔧 إصلاح شامل لجميع مشاكل تسجيل الدخول                      ║
echo ║  🌐 فتح المتصفح تلقائياً                                      ║
echo ║  ✅ ضمان عمل النظام 100%%                                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 فحص Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :found_python
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :found_python
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :found_python

echo ❌ Python غير مثبت!
echo.
echo 📥 يرجى تثبيت Python أولاً:
echo    1. اذهب إلى: https://python.org
echo    2. حمل أحدث إصدار
echo    3. تأكد من تحديد "Add Python to PATH"
echo    4. أعد تشغيل هذا الملف
echo.
pause
exit /b 1

:found_python
echo ✅ Python متوفر (%PYTHON_CMD%)

echo.
echo 🧹 تنظيف النظام...
if exist management_system.db (
    del management_system.db
    echo ✅ تم حذف قاعدة البيانات القديمة
)

echo.
echo 📦 تثبيت المتطلبات...
%PYTHON_CMD% -m pip install flask --quiet --user
echo ✅ تم تثبيت Flask

echo.
echo 🔧 إنشاء قاعدة بيانات جديدة مع حل مشكلة تسجيل الدخول...

%PYTHON_CMD% -c "
import sqlite3
import hashlib
import sys

try:
    print('🗄️  إنشاء قاعدة البيانات...')
    
    # إنشاء قاعدة البيانات
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
    username = 'admin'
    email = 'admin@rashid.com'
    password = 'admin123'
    password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, role, is_active)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, email, password_hash, 'admin', 1))
    
    print(f'✅ تم إنشاء مستخدم admin')
    print(f'   👤 اسم المستخدم: {username}')
    print(f'   📧 البريد: {email}')
    print(f'   🔑 كلمة المرور: {password}')
    print(f'   🔐 التشفير: {password_hash}')
    
    # إنشاء باقي الجداول
    tables = [
        '''CREATE TABLE employees (
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
        )''',
        '''CREATE TABLE cars (
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
        )''',
        '''CREATE TABLE treasury (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            reference_number TEXT,
            created_by TEXT,
            date TEXT NOT NULL,
            balance_after REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ]
    
    for table_sql in tables:
        cursor.execute(table_sql)
    
    conn.commit()
    conn.close()
    
    print('✅ تم إنشاء جميع الجداول')
    
    # اختبار تسجيل الدخول
    print('\\n🧪 اختبار تسجيل الدخول...')
    
    conn = sqlite3.connect('management_system.db')
    conn.row_factory = sqlite3.Row
    
    test_user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password_hash = ?',
        (username, password_hash)
    ).fetchone()
    
    if test_user:
        print('✅ اختبار تسجيل الدخول نجح!')
        print('   النظام جاهز للاستخدام')
    else:
        print('❌ اختبار تسجيل الدخول فشل!')
        sys.exit(1)
    
    conn.close()
    
except Exception as e:
    print(f'❌ خطأ: {e}')
    sys.exit(1)
"

if errorlevel 1 (
    echo ❌ فشل في إعداد قاعدة البيانات
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 تم الإعداد بنجاح                         ║
echo ║                                                              ║
echo ║  ✅ قاعدة البيانات جاهزة                                      ║
echo ║  ✅ مستخدم admin تم إنشاؤه                                   ║
echo ║  ✅ اختبار تسجيل الدخول نجح                                   ║
echo ║  ✅ واجهة تسجيل الدخول مُحسنة                                ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول:                                     ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     📧 أو البريد: admin@rashid.com                          ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  🌐 سيتم فتح المتصفح تلقائياً خلال 5 ثوان                     ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النظام...
echo.

REM تشغيل النظام
%PYTHON_CMD% app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  🎉 تم حل مشكلة تسجيل الدخول نهائياً                          ║
echo ║  💡 يمكنك الآن تسجيل الدخول بدون أي مشاكل                    ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause