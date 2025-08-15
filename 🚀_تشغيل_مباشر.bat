@echo off
chcp 65001 > nul
title 🚀 تشغيل مباشر - localhost:5000

color 0A
cls
echo.
echo    🚀 تشغيل مباشر - http://localhost:5000
echo    ═══════════════════════════════════════════
echo.
echo    ⚡ تشغيل فوري...

cd /d "%~dp0"

REM إيقاف خوادم سابقة
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1

REM البحث عن Python
set PYTHON_CMD=
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :run
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :run
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :run

echo    ❌ Python غير موجود
pause
exit /b 1

:run
REM تثبيت Flask إذا لم يكن موجوداً
%PYTHON_CMD% -c "import flask" >nul 2>&1 || %PYTHON_CMD% -m pip install flask --user --quiet >nul 2>&1

REM إعداد قاعدة البيانات
%PYTHON_CMD% -c "import sqlite3,hashlib;conn=sqlite3.connect('management_system.db');cursor=conn.cursor();cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password_hash TEXT, role TEXT DEFAULT \"user\", is_active BOOLEAN DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)');cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',)).fetchone()[0] == 0 and cursor.execute('INSERT INTO users (username, email, password_hash, role, is_active) VALUES (?, ?, ?, ?, ?)', ('admin', 'admin@rashid.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin', 1));conn.commit();conn.close()" >nul 2>&1

echo    ✅ جاهز للتشغيل
echo    🌐 فتح http://localhost:5000
echo    🔑 admin / admin123
echo.

REM فتح المتصفح
start http://localhost:5000

REM تشغيل النظام
%PYTHON_CMD% app.py