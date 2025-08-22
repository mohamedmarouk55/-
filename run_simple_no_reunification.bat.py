#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تشغيل بسيط بدون إعادة توجيه
RASHID INDUSTRIAL CO.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib
import os
import webbrowser
import threading
import time

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'rashid-simple-key-2024'

# قاعدة البيانات
DATABASE = 'simple_system.db'

def init_db():
    """إنشاء قاعدة البيانات البسيطة"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    
    # إضافة مستخدم admin
    password_hash = hashlib.md5('admin123'.encode()).hexdigest()
    cursor.execute('INSERT OR REPLACE INTO users (id, username, password_hash) VALUES (1, "admin", ?)', (password_hash,))
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    """الصفحة الرئيسية البسيطة"""
    if 'logged_in' not in session:
        return redirect('/login')
    
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>نظام إدارة السيارات - RASHID INDUSTRIAL CO.</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0; }
            .container { background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }
            h1 { color: #333; }
            .success { color: green; font-size: 18px; margin: 20px 0; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚗 نظام إدارة السيارات</h1>
            <h2>RASHID INDUSTRIAL CO.</h2>
            <div class="success">✅ تم تسجيل الدخول بنجاح!</div>
            <p>مرحباً بك في نظام إدارة السيارات الشامل</p>
            <p>🌐 الرابط: http://localhost:5000</p>
            <p>👤 المستخدم: admin</p>
            <br>
            <a href="/logout" class="btn">تسجيل الخروج</a>
            <br><br>
            <p style="color: #666;">النظام يعمل بشكل مثالي بدون أخطاء إعادة التوجيه!</p>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول البسيطة"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = 'admin'
            return redirect('/')
        else:
            error = 'بيانات خاطئة! استخدم: admin / admin123'
    else:
        error = None
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تسجيل الدخول - RASHID INDUSTRIAL CO.</title>
        <style>
            body {{ font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
            .login-box {{ background: white; padding: 40px; border-radius: 15px; max-width: 400px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
            h1 {{ color: #333; margin-bottom: 30px; }}
            input {{ width: 100%; padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }}
            button {{ width: 100%; padding: 15px; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }}
            button:hover {{ background: #5a67d8; }}
            .error {{ color: red; margin: 10px 0; }}
            .info {{ color: #666; margin: 20px 0; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🚗 تسجيل الدخول</h1>
            <h3>RASHID INDUSTRIAL CO.</h3>
            
            <form method="post">
                <input type="text" name="username" placeholder="اسم المستخدم" required>
                <input type="password" name="password" placeholder="كلمة المرور" required>
                <button type="submit">تسجيل الدخول</button>
            </form>
            
            {f'<div class="error">❌ {error}</div>' if error else ''}
            
            <div class="info">
                <strong>بيانات تسجيل الدخول:</strong><br>
                👤 اسم المستخدم: admin<br>
                🔑 كلمة المرور: admin123
            </div>
            
            <div class="info">
                ✅ تم حل مشكلة ERR_TOO_MANY_REDIRECTS<br>
                🌐 http://localhost:5000
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    return redirect('/login')

def open_browser():
    """فتح المتصفح تلقائياً"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🔧 إعداد قاعدة البيانات البسيطة...")
    init_db()
    
    print("✅ تم حل مشكلة ERR_TOO_MANY_REDIRECTS")
    print("🌐 الرابط: http://localhost:5000")
    print("🔑 البيانات: admin / admin123")
    print("🌐 سيتم فتح المتصفح تلقائياً...")
    print("⚠️  لإيقاف النظام: اضغط Ctrl+C")
    print("=" * 50)
    
    # فتح المتصفح في خيط منفصل
    threading.Thread(target=open_browser, daemon=True).start()
    
    # تشغيل النظام
    app.run(host='0.0.0.0', port=5000, debug=False)