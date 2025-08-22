@echo off
chcp 65001 > nul
title تشغيل فوري - http://localhost:5000

color 0B
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🚀 تشغيل فوري ومباشر                            ║
echo ║                                                              ║
echo ║         🌐 http://localhost:5000                             ║
echo ║                                                              ║
echo ║              RASHID INDUSTRIAL CO.                          ║
echo ║                                                              ║
echo ║  ⚡ تشغيل سريع بدون انتظار                                   ║
echo ║  🌐 فتح المتصفح تلقائياً                                      ║
echo ║  🔑 admin / admin123                                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM إيقاف أي خوادم سابقة
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1

echo 🔍 البحث عن Python...
set PYTHON_CMD=

py --version >nul 2>&1 && set PYTHON_CMD=py && goto :start_now
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :start_now
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :start_now

echo ❌ Python غير موجود!
pause
exit /b 1

:start_now
echo ✅ Python: %PYTHON_CMD%

REM تثبيت Flask سريع إذا لم يكن موجوداً
%PYTHON_CMD% -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 تثبيت Flask...
    %PYTHON_CMD% -m pip install flask --user --quiet >nul 2>&1
)

REM إعداد قاعدة البيانات سريع
%PYTHON_CMD% -c "
import sqlite3, hashlib
conn = sqlite3.connect('management_system.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password_hash TEXT, role TEXT DEFAULT \"user\", is_active BOOLEAN DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
if cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',)).fetchone()[0] == 0:
    cursor.execute('INSERT INTO users (username, email, password_hash, role, is_active) VALUES (?, ?, ?, ?, ?)', ('admin', 'admin@rashid.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin', 1))
conn.commit()
conn.close()
" >nul 2>&1

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🚀 تشغيل فوري الآن                            ║
echo ║                                                              ║
echo ║  🌐 http://localhost:5000                                    ║
echo ║  🔑 admin / admin123                                         ║
echo ║                                                              ║
echo ║  🌐 المتصفح سيفتح خلال ثانيتين                               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM فتح المتصفح فوراً
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5000"

REM تشغيل النظام
%PYTHON_CMD% app.py

pause