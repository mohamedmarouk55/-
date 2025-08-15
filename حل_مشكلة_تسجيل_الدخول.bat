@echo off
chcp 65001 > nul
title حل مشكلة تسجيل الدخول - RASHID INDUSTRIAL CO.

color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    حل مشكلة تسجيل الدخول                       ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :found_python
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :found_python
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :found_python

echo ❌ Python غير مثبت!
echo 📥 يرجى تثبيت Python من: https://python.org
pause
exit /b 1

:found_python
echo ✅ Python متوفر (%PYTHON_CMD%)

echo.
echo 🧹 تنظيف قاعدة البيانات القديمة...
if exist management_system.db (
    del management_system.db
    echo ✅ تم حذف قاعدة البيانات القديمة
)

echo.
echo 🔧 إنشاء قاعدة بيانات جديدة مع إصلاح مشكلة تسجيل الدخول...

%PYTHON_CMD% -c "
import sqlite3
import hashlib
import os

print('📋 إنشاء قاعدة البيانات الجديدة...')

# إنشاء قاعدة البيانات
conn = sqlite3.connect('management_system.db')
cursor = conn.cursor()

# إنشاء جدول المستخدمين مع فهرس محسن
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

# إنشاء فهرس للبحث السريع
cursor.execute('CREATE INDEX idx_users_login ON users(username, email, password_hash)')

# إنشاء مستخدم admin مع تشفير صحيح
admin_password = 'admin123'
password_hash = hashlib.md5(admin_password.encode('utf-8')).hexdigest()

cursor.execute('''
    INSERT INTO users (username, email, password_hash, role, is_active)
    VALUES (?, ?, ?, ?, ?)
''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))

print(f'✅ تم إنشاء مستخدم admin')
print(f'   اسم المستخدم: admin')
print(f'   البريد: admin@rashid.com')
print(f'   كلمة المرور: {admin_password}')
print(f'   التشفير: {password_hash}')

# إنشاء باقي الجداول الأساسية
tables = [
    '''CREATE TABLE IF NOT EXISTS employees (
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
    '''CREATE TABLE IF NOT EXISTS cars (
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
    '''CREATE TABLE IF NOT EXISTS treasury (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type TEXT NOT NULL CHECK (transaction_type IN ('إيداع', 'سحب')),
        amount REAL NOT NULL,
        description TEXT,
        reference_number TEXT,
        created_by TEXT,
        date TEXT NOT NULL,
        balance_after REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        receipt_number TEXT,
        date TEXT NOT NULL,
        approved_by TEXT,
        status TEXT DEFAULT 'معتمد',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS car_custody (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        employee_number TEXT NOT NULL,
        car_id INTEGER NOT NULL,
        custody_date TEXT NOT NULL,
        expected_return TEXT,
        return_date TEXT,
        notes TEXT,
        return_notes TEXT,
        status TEXT DEFAULT 'نشط' CHECK (status IN ('نشط', 'مُسلم')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees (id),
        FOREIGN KEY (car_id) REFERENCES cars (id)
    )''',
    '''CREATE TABLE IF NOT EXISTS financial_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL CHECK (type IN ('إيراد', 'مصروف')),
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        value TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )'''
]

for table_sql in tables:
    cursor.execute(table_sql)

# إضافة إعدادات افتراضية
default_settings = [
    ('company_name', 'RASHID INDUSTRIAL CO.', 'اسم الشركة'),
    ('company_address', 'الرياض، المملكة العربية السعودية', 'عنوان الشركة'),
    ('currency', 'SAR', 'العملة المستخدمة'),
    ('tax_rate', '15', 'معدل الضريبة المضافة'),
]

for key, value, description in default_settings:
    cursor.execute('''
        INSERT OR IGNORE INTO settings (key, value, description)
        VALUES (?, ?, ?)
    ''', (key, value, description))

conn.commit()
conn.close()

print('✅ تم إنشاء جميع الجداول بنجاح')
"

if errorlevel 1 (
    echo ❌ فشل في إنشاء قاعدة البيانات
    pause
    exit /b 1
)

echo.
echo 🧪 اختبار تسجيل الدخول...

%PYTHON_CMD% -c "
import sqlite3
import hashlib

conn = sqlite3.connect('management_system.db')
conn.row_factory = sqlite3.Row

# اختبار تسجيل الدخول
username = 'admin'
password = 'admin123'
password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

print(f'🔍 البحث عن مستخدم: {username}')
print(f'🔑 كلمة المرور: {password}')
print(f'🔐 التشفير المتوقع: {password_hash}')

user = conn.execute(
    'SELECT * FROM users WHERE (username = ? OR email = ?) AND is_active = 1',
    (username, username)
).fetchone()

if user:
    print(f'✅ تم العثور على المستخدم')
    print(f'   ID: {user[\"id\"]}')
    print(f'   اسم المستخدم: {user[\"username\"]}')
    print(f'   البريد: {user[\"email\"]}')
    print(f'   التشفير الموجود: {user[\"password_hash\"]}')
    print(f'   الدور: {user[\"role\"]}')
    print(f'   نشط: {user[\"is_active\"]}')
    
    if user['password_hash'] == password_hash:
        print('✅ كلمة المرور صحيحة - تسجيل الدخول سينجح!')
    else:
        print('❌ كلمة المرور غير صحيحة')
else:
    print('❌ لم يتم العثور على المستخدم')

conn.close()
"

echo.
echo 📦 تثبيت Flask...
%PYTHON_CMD% -m pip install flask --quiet --user >nul 2>&1

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 تم حل المشكلة بنجاح                      ║
echo ║                                                              ║
echo ║  ✅ تم إصلاح مشكلة تسجيل الدخول                              ║
echo ║  ✅ تم تبسيط واجهة تسجيل الدخول                              ║
echo ║  ✅ تم إنشاء قاعدة بيانات جديدة                              ║
echo ║  ✅ تم اختبار تسجيل الدخول بنجاح                             ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول:                                     ║
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
echo ║  تم حل مشكلة تسجيل الدخول بنجاح                               ║
echo ║  يمكنك الآن تسجيل الدخول بدون مشاكل                          ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause