@echo off
title START NOW - localhost:5000
cd /d "%~dp0"
taskkill /f /im python.exe >nul 2>&1
py --version >nul 2>&1 && set PYTHON_CMD=py && goto :go
python --version >nul 2>&1 && set PYTHON_CMD=python && goto :go
python3 --version >nul 2>&1 && set PYTHON_CMD=python3 && goto :go
echo Python not found & pause & exit /b 1
:go
%PYTHON_CMD% -c "import flask" >nul 2>&1 || %PYTHON_CMD% -m pip install flask --user --quiet
%PYTHON_CMD% -c "import sqlite3,hashlib;c=sqlite3.connect('management_system.db');x=c.cursor();x.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password_hash TEXT, role TEXT DEFAULT \"user\", is_active BOOLEAN DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)');x.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',)).fetchone()[0] == 0 and x.execute('INSERT INTO users (username, email, password_hash, role, is_active) VALUES (?, ?, ?, ?, ?)', ('admin', 'admin@rashid.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin', 1));c.commit();c.close()" >nul 2>&1
start http://localhost:5000
%PYTHON_CMD% app.py