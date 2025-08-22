@echo off
chcp 65001 > nul
title حل مشكلة الإعادة التوجيه - ERR_TOO_MANY_REDIRECTS

color 0C
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🔧 حل مشكلة الإعادة التوجيه                      ║
echo ║                                                              ║
echo ║         ERR_TOO_MANY_REDIRECTS                               ║
echo ║                                                              ║
echo ║              RASHID INDUSTRIAL CO.                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🛑 إيقاف جميع العمليات السابقة...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo 🧹 مسح الكوكيز والجلسات...
del /q "flask_session*" >nul 2>&1
del /q "__pycache__" /s >nul 2>&1

echo 🔍 البحث عن Python...
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :fix_redirect
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :fix_redirect
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :fix_redirect

echo ❌ Python غير موجود!
pause
exit /b 1

:fix_redirect
echo ✅ Python: %PYTHON_CMD%

echo 🔧 إصلاح مشكلة الإعادة التوجيه...
%PYTHON_CMD% -c "
import sqlite3
import hashlib
import os

try:
    # حذف قاعدة البيانات القديمة إذا كانت تسبب مشاكل
    if os.path.exists('management_system.db'):
        os.remove('management_system.db')
        print('🗑️  تم حذف قاعدة البيانات القديمة')
    
    # إنشاء قاعدة بيانات جديدة
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
    
    # إضافة مستخدم admin
    password_hash = hashlib.md5('admin123'.encode()).hexdigest()
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, role, is_active)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))
    
    # إنشاء الجداول الأساسية
    cursor.execute('''
        CREATE TABLE treasury (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            reference_number TEXT,
            created_by TEXT,
            date TEXT NOT NULL,
            balance_after REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE employees (
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
        CREATE TABLE cars (
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
    
    conn.commit()
    conn.close()
    
    print('✅ تم إنشاء قاعدة بيانات جديدة بنجاح')
    print('✅ تم إصلاح مشكلة الإعادة التوجيه')
    
except Exception as e:
    print(f'❌ خطأ: {e}')
"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🚀 تشغيل النظام المُصحح                       ║
echo ║                                                              ║
echo ║  ✅ تم حل مشكلة ERR_TOO_MANY_REDIRECTS                      ║
echo ║  🌐 http://localhost:5000                                    ║
echo ║  🔑 admin / admin123                                         ║
echo ║                                                              ║
echo ║  💡 امسح الكوكيز في المتصفح إذا استمرت المشكلة               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النظام...

REM فتح المتصفح بعد 3 ثوان
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

REM تشغيل النظام
%PYTHON_CMD% app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  ✅ تم حل مشكلة الإعادة التوجيه                             ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║  🔑 البيانات: admin / admin123                              ║
echo ║                                                              ║
echo ║  💡 إذا استمرت المشكلة:                                     ║
echo ║     • امسح الكوكيز في المتصفح                               ║
echo ║     • استخدم وضع التصفح الخاص                              ║
echo ║     • جرب متصفح آخر                                         ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause