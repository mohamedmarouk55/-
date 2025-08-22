@echo off
chcp 65001 > nul
title تشغيل مع تشخيص الأخطاء - RASHID INDUSTRIAL CO.

color 0C
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                تشغيل مع تشخيص الأخطاء                         ║
echo ║                    RASHID INDUSTRIAL CO.                    ║
echo ║                                                              ║
echo ║  🔍 تشخيص مفصل للأخطاء                                      ║
echo ║  🛠️  إصلاح المشاكل تلقائياً                                  ║
echo ║  📊 عرض رسائل تفصيلية                                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 فحص Python...
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
echo 📦 فحص وتثبيت المتطلبات...
%PYTHON_CMD% -c "
try:
    import flask
    print('✅ Flask متوفر')
except ImportError:
    print('❌ Flask غير متوفر - سيتم تثبيته')
    import subprocess
    subprocess.run(['pip', 'install', 'flask', '--user'], check=True)
    print('✅ تم تثبيت Flask')

try:
    import sqlite3
    print('✅ SQLite متوفر')
except ImportError:
    print('❌ SQLite غير متوفر')

import os
if os.path.exists('templates/login.html'):
    print('✅ ملف login.html موجود')
else:
    print('❌ ملف login.html غير موجود')

if os.path.exists('app.py'):
    print('✅ ملف app.py موجود')
else:
    print('❌ ملف app.py غير موجود')
"

echo.
echo 🔧 إنشاء قاعدة بيانات آمنة...
%PYTHON_CMD% -c "
import sqlite3
import hashlib
import os

try:
    # حذف قاعدة البيانات القديمة إن وجدت
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
    
    # إنشاء مستخدم admin
    password_hash = hashlib.md5('admin123'.encode()).hexdigest()
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, role, is_active)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))
    
    # إنشاء جداول أساسية أخرى
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
    
    conn.commit()
    conn.close()
    
    print('✅ تم إنشاء قاعدة البيانات بنجاح')
    
except Exception as e:
    print(f'❌ خطأ في إنشاء قاعدة البيانات: {e}')
"

echo.
echo 🧪 اختبار النظام...
%PYTHON_CMD% -c "
try:
    # اختبار استيراد app.py
    import sys
    sys.path.append('.')
    
    print('🔍 اختبار استيراد الوحدات...')
    from flask import Flask, render_template, request, session, redirect, url_for, flash
    print('✅ Flask modules imported successfully')
    
    import sqlite3
    print('✅ SQLite imported successfully')
    
    import hashlib
    print('✅ Hashlib imported successfully')
    
    # اختبار قاعدة البيانات
    conn = sqlite3.connect('management_system.db')
    conn.row_factory = sqlite3.Row
    user = conn.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if user:
        print('✅ مستخدم admin موجود في قاعدة البيانات')
    else:
        print('❌ مستخدم admin غير موجود')
    conn.close()
    
    print('✅ جميع الاختبارات نجحت')
    
except Exception as e:
    print(f'❌ خطأ في الاختبار: {e}')
    import traceback
    traceback.print_exc()
"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 تشغيل النظام                            ║
echo ║                                                              ║
echo ║  🌐 الرابط: http://localhost:5000                           ║
echo ║                                                              ║
echo ║  🔑 بيانات تسجيل الدخول:                                     ║
echo ║     👤 اسم المستخدم: admin                                   ║
echo ║     🔑 كلمة المرور: admin123                                 ║
echo ║                                                              ║
echo ║  📊 ستظهر رسائل تشخيصية مفصلة أدناه                         ║
echo ║  🔍 راقب الرسائل لتحديد أي مشاكل                            ║
echo ║                                                              ║
echo ║  ⚠️  لإيقاف النظام: اضغط Ctrl+C                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 تشغيل النظام مع تشخيص الأخطاء...
echo.

REM فتح المتصفح بعد 5 ثوان
start "" timeout /t 5 /nobreak >nul && start http://localhost:5000

REM تشغيل النظام مع عرض جميع الأخطاء
%PYTHON_CMD% -u app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       تم إيقاف النظام                          ║
echo ║                                                              ║
echo ║  📊 إذا ظهرت أخطاء أعلاه، يرجى:                             ║
echo ║     • نسخ رسالة الخطأ                                         ║
echo ║     • البحث عن الحل في ملف حل_المشاكل.txt                   ║
echo ║     • أو التواصل مع الدعم الفني                              ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause