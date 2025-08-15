@echo off
chcp 65001 > nul
title GitHub Quick Run - Car Management System

color 0E
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                  GITHUB QUICK RUN                            ║
echo ║              Car Management System                           ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ║                                                              ║
echo ║  🌐 GitHub: https://github.com/mohamedmarouk55/-             ║
echo ║  🚀 Quick Launch from GitHub                                 ║
echo ║  ⚡ Auto Setup & Run                                         ║
echo ╚══════════════════════════════════════════════════════════════╗
echo.

echo 🔍 Checking Python...
set PYTHON_CMD=

py --version >nul 2>&1 && set PYTHON_CMD=py && goto :found_python
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :found_python
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :found_python

echo ❌ Python not found!
echo.
echo 📥 Please install Python from: https://python.org
echo    Make sure to check "Add Python to PATH" during installation
echo.
pause
exit /b 1

:found_python
echo ✅ Python found: %PYTHON_CMD%

echo.
echo 🔍 Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git not found!
    echo 📥 Please install Git from: https://git-scm.com
    pause
    exit /b 1
)
echo ✅ Git is available

echo.
echo 📥 Cloning from GitHub...
if exist "car-management-system" (
    echo 🗂️  Directory exists, updating...
    cd car-management-system
    git pull origin main
) else (
    echo 📦 Cloning repository...
    git clone https://github.com/mohamedmarouk55/-.git car-management-system
    cd car-management-system
)

echo.
echo 📦 Installing requirements...
%PYTHON_CMD% -m pip install -r requirements.txt --user --quiet

echo.
echo 🗄️ Setting up database...
%PYTHON_CMD% -c "
import sqlite3
import hashlib
import os

try:
    conn = sqlite3.connect('management_system.db')
    cursor = conn.cursor()
    
    # Create users table
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
    
    # Ensure admin user exists
    admin_exists = cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',)).fetchone()[0]
    if admin_exists == 0:
        password_hash = hashlib.md5('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))
        print('✅ Admin user created')
    else:
        print('✅ Admin user exists')
    
    conn.commit()
    conn.close()
    print('✅ Database setup completed')
    
except Exception as e:
    print(f'❌ Database error: {e}')
"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🚀 LAUNCHING FROM GITHUB                      ║
echo ║                                                              ║
echo ║  🌐 URL: http://localhost:5000                               ║
echo ║  📂 GitHub: https://github.com/mohamedmarouk55/-             ║
echo ║                                                              ║
echo ║  🔑 Login Credentials:                                       ║
echo ║     👤 Username: admin                                       ║
echo ║     🔑 Password: admin123                                    ║
echo ║                                                              ║
echo ║  🌐 Browser will open automatically in 3 seconds            ║
echo ║  ⚠️  To stop: Press Ctrl+C                                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Starting system from GitHub...
echo.

REM Open browser after 3 seconds
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

REM Start the system
%PYTHON_CMD% app.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SYSTEM STOPPED                            ║
echo ║                                                              ║
echo ║  🎉 System worked successfully from GitHub!                  ║
echo ║  🌐 URL: http://localhost:5000                               ║
echo ║  📂 GitHub: https://github.com/mohamedmarouk55/-             ║
echo ║                                                              ║
echo ║                RASHID INDUSTRIAL CO.                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause