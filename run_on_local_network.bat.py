#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام إدارة السيارات - للوصول عبر الشبكة المحلية
RASHID INDUSTRIAL CO.
يعمل على جميع الأجهزة في نفس الشبكة
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
import sqlite3
import hashlib
import os
import webbrowser
import threading
import time
import socket
from datetime import datetime, timedelta

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'rashid-network-system-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# قاعدة البيانات
DATABASE = 'network_system.db'

def get_local_ip():
    """الحصول على عنوان IP المحلي"""
    try:
        # إنشاء اتصال وهمي للحصول على IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def init_database():
    """إنشاء قاعدة البيانات مع جميع البيانات"""
    try:
        print("🔧 إنشاء قاعدة البيانات للشبكة المحلية...")
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # حذف الجداول إذا كانت موجودة
        tables = ['users', 'employees', 'cars', 'treasury', 'expenses', 'car_custody']
        for table in tables:
            cursor.execute(f'DROP TABLE IF EXISTS {table}')
        
        # جدول المستخدمين
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
        
        # جدول الموظفين
        cursor.execute('''
            CREATE TABLE employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL,
                phone TEXT,
                email TEXT,
                hire_date TEXT,
                status TEXT DEFAULT 'نشط',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول السيارات
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
                purchase_date TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الخزينة
        cursor.execute('''
            CREATE TABLE treasury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                reference_number TEXT,
                date TEXT NOT NULL,
                balance_after REAL,
                created_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المصروفات
        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                receipt_number TEXT,
                date TEXT NOT NULL,
                approved_by TEXT,
                status TEXT DEFAULT 'معتمد',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول عهد السيارات
        cursor.execute('''
            CREATE TABLE car_custody (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER NOT NULL,
                employee_id INTEGER NOT NULL,
                custody_date TEXT NOT NULL,
                return_date TEXT,
                purpose TEXT,
                notes TEXT,
                status TEXT DEFAULT 'نشط',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (car_id) REFERENCES cars (id),
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        print("✅ تم إنشاء جميع الجداول")
        
        # إضافة البيانات
        add_sample_data(cursor)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إنشاء قاعدة البيانات للشبكة المحلية بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        return False

def add_sample_data(cursor):
    """إضافة بيانات تجريبية شاملة"""
    print("📊 إضافة البيانات التجريبية...")
    
    # إضافة المستخدمين
    users_data = [
        ('admin', 'admin@rashid.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin'),
        ('manager', 'manager@rashid.com', hashlib.md5('manager123'.encode()).hexdigest(), 'manager'),
        ('user', 'user@rashid.com', hashlib.md5('user123'.encode()).hexdigest(), 'user')
    ]
    
    cursor.executemany('INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)', users_data)
    
    # إضافة الموظفين
    employees_data = [
        ('EMP001', 'أحمد محمد علي', 'مدير عام', 'الإدارة', 15000.0, '01234567890', 'ahmed@rashid.com', '2020-01-15', 'نشط'),
        ('EMP002', 'فاطمة أحمد حسن', 'محاسبة', 'المالية', 8000.0, '01234567891', 'fatima@rashid.com', '2020-03-01', 'نشط'),
        ('EMP003', 'محمد سعد إبراهيم', 'سائق', 'النقل', 4500.0, '01234567892', 'mohamed@rashid.com', '2020-06-15', 'نشط'),
        ('EMP004', 'سارة علي محمود', 'سكرتيرة', 'الإدارة', 6000.0, '01234567893', 'sara@rashid.com', '2021-01-10', 'نشط'),
        ('EMP005', 'خالد عبد الله', 'فني صيانة', 'الصيانة', 5500.0, '01234567894', 'khalid@rashid.com', '2021-04-20', 'نشط'),
        ('EMP006', 'نور الدين أحمد', 'مشرف نقل', 'النقل', 7000.0, '01234567895', 'nour@rashid.com', '2021-08-01', 'نشط'),
        ('EMP007', 'ليلى حسام', 'موظفة استقبال', 'الإدارة', 4000.0, '01234567896', 'layla@rashid.com', '2022-02-15', 'نشط'),
        ('EMP008', 'عمر فاروق', 'مساعد إداري', 'الإدارة', 3500.0, '01234567897', 'omar@rashid.com', '2022-09-01', 'نشط')
    ]
    
    cursor.executemany('''
        INSERT INTO employees (employee_number, name, position, department, salary, phone, email, hire_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)
    
    # إضافة السيارات
    cars_data = [
        ('تويوتا', 'كامري', 2022, 'أ ب ج 1234', 'أبيض', 'متاح', 85000.0, '2022-01-15', 'سيارة إدارية'),
        ('هيونداي', 'إلنترا', 2021, 'د هـ و 5678', 'أسود', 'مستخدم', 65000.0, '2021-06-20', 'سيارة تنفيذية'),
        ('نيسان', 'صني', 2020, 'ز ح ط 9012', 'أزرق', 'متاح', 45000.0, '2020-08-10', 'سيارة اقتصادية'),
        ('كيا', 'سيراتو', 2023, 'ي ك ل 3456', 'أحمر', 'في الصيانة', 70000.0, '2023-03-01', 'سيارة حديثة'),
        ('شيفروليه', 'كروز', 2019, 'م ن س 7890', 'رمادي', 'متاح', 55000.0, '2019-12-05', 'سيارة متوسطة'),
        ('فورد', 'فوكس', 2021, 'ع ف ص 2468', 'أبيض', 'مستخدم', 60000.0, '2021-04-18', 'سيارة عملية'),
        ('مازدا', '3', 2022, 'ق ر ش 1357', 'أسود', 'متاح', 75000.0, '2022-07-22', 'سيارة رياضية'),
        ('هوندا', 'سيفيك', 2020, 'ت ث خ 9753', 'أزرق', 'متاح', 68000.0, '2020-11-30', 'سيارة موثوقة')
    ]
    
    cursor.executemany('''
        INSERT INTO cars (brand, model, year, license_plate, color, status, purchase_price, purchase_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', cars_data)
    
    # إضافة معاملات الخزينة
    treasury_data = [
        ('إيداع', 100000.0, 'رأس المال الأولي', 'REF001', '2024-01-01', 100000.0, 'admin'),
        ('إيداع', 50000.0, 'إيداع شهر يناير', 'REF002', '2024-01-15', 150000.0, 'admin'),
        ('سحب', 25000.0, 'مرتبات الموظفين', 'REF003', '2024-01-31', 125000.0, 'manager'),
        ('إيداع', 75000.0, 'إيداع شهر فبراير', 'REF004', '2024-02-15', 200000.0, 'admin'),
        ('سحب', 15000.0, 'صيانة السيارات', 'REF005', '2024-02-28', 185000.0, 'manager'),
        ('إيداع', 60000.0, 'إيداع شهر مارس', 'REF006', '2024-03-15', 245000.0, 'admin'),
        ('سحب', 30000.0, 'مصروفات تشغيلية', 'REF007', '2024-03-31', 215000.0, 'manager')
    ]
    
    cursor.executemany('''
        INSERT INTO treasury (transaction_type, amount, description, reference_number, date, balance_after, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', treasury_data)
    
    # إضافة المصروفات
    expenses_data = [
        ('وقود', 5000.0, 'وقود السيارات شهر يناير', 'REC001', '2024-01-31', 'admin', 'معتمد'),
        ('قطع غيار', 8000.0, 'قطع غيار سيارة كيا سيراتو', 'REC002', '2024-02-15', 'manager', 'معتمد'),
        ('مكتبية', 2000.0, 'أدوات مكتبية ومستلزمات', 'REC003', '2024-02-20', 'admin', 'معتمد'),
        ('تأمين', 12000.0, 'تأمين السيارات السنوي', 'REC004', '2024-03-01', 'admin', 'معتمد'),
        ('خدمة', 3000.0, 'خدمة دورية للسيارات', 'REC005', '2024-03-15', 'manager', 'معتمد'),
        ('اتصالات', 1500.0, 'فواتير الهاتف والإنترنت', 'REC006', '2024-03-31', 'admin', 'معتمد')
    ]
    
    cursor.executemany('''
        INSERT INTO expenses (category, amount, description, receipt_number, date, approved_by, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', expenses_data)
    
    # إضافة عهد السيارات
    custody_data = [
        (2, 1, '2024-01-15', None, 'اجتماعات إدارية', 'سيارة للمدير العام', 'نشط'),
        (6, 3, '2024-02-01', None, 'مهام النقل اليومية', 'سيارة للسائق', 'نشط'),
        (4, 5, '2024-02-15', '2024-03-01', 'فحص وصيانة', 'تم إرجاع السيارة بعد الصيانة', 'مكتمل'),
        (1, 4, '2024-03-01', None, 'مهام إدارية', 'سيارة للسكرتيرة', 'نشط')
    ]
    
    cursor.executemany('''
        INSERT INTO car_custody (car_id, employee_id, custody_date, return_date, purpose, notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', custody_data)
    
    print("✅ تم إضافة جميع البيانات التجريبية")

def get_db_connection():
    """الحصول على اتصال قاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """تأكيد تسجيل الدخول"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول للشبكة المحلية"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    error_message = None
    local_ip = get_local_ip()
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            error_message = 'يرجى إدخال اسم المستخدم وكلمة المرور!'
        elif (username.lower() == 'admin') and password == 'admin123':
            session.clear()
            session.permanent = True
            session['user_id'] = 1
            session['username'] = 'admin'
            session['role'] = 'admin'
            
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('index'))
        else:
            error_message = 'بيانات تسجيل الدخول غير صحيحة!'
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تسجيل الدخول - RASHID INDUSTRIAL CO.</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .login-container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                padding: 50px;
                width: 100%;
                max-width: 500px;
                text-align: center;
            }
            .logo { font-size: 4rem; color: #667eea; margin-bottom: 20px; }
            h1 { color: #333; margin-bottom: 10px; font-size: 2rem; }
            h2 { color: #666; margin-bottom: 40px; font-weight: normal; }
            .form-group { margin-bottom: 25px; text-align: right; }
            label { display: block; margin-bottom: 8px; color: #333; font-weight: bold; font-size: 1.1rem; }
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 18px;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                font-size: 16px;
                transition: all 0.3s ease;
            }
            input[type="text"]:focus, input[type="password"]:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            .btn {
                width: 100%;
                padding: 18px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            }
            .error {
                background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
                color: #721c24;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                border: 2px solid #f5c6cb;
                font-weight: bold;
            }
            .network-info {
                background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
                color: #0c5460;
                padding: 20px;
                border-radius: 15px;
                margin: 25px 0;
                font-size: 15px;
                text-align: right;
                border: 2px solid #17a2b8;
            }
            .success-badge {
                background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                color: #155724;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                font-weight: bold;
                border: 2px solid #28a745;
            }
            .device-list {
                background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                color: #856404;
                padding: 20px;
                border-radius: 15px;
                margin: 25px 0;
                font-size: 14px;
                text-align: right;
                border: 2px solid #ffc107;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">🚗</div>
            <h1>تسجيل الدخول</h1>
            <h2>RASHID INDUSTRIAL CO.</h2>
            
            {% if error_message %}
            <div class="error">❌ {{ error_message }}</div>
            {% endif %}
            
            <div class="success-badge">
                🌐 النظام متاح على جميع الأجهزة في الشبكة!
            </div>
            
            <form method="post">
                <div class="form-group">
                    <label for="username">اسم المستخدم:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">كلمة المرور:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn">تسجيل الدخول</button>
            </form>
            
            <div class="network-info">
                <strong>🌐 معلومات الوصول للشبكة المحلية:</strong><br><br>
                <strong>💻 من هذا الجهاز:</strong><br>
                • http://localhost:5000<br>
                • http://127.0.0.1:5000<br><br>
                
                <strong>📱 من الأجهزة الأخرى في نفس الشبكة:</strong><br>
                • http://{{ local_ip }}:5000<br><br>
                
                <strong>🔑 بيانات الدخول:</strong><br>
                👤 اسم المستخدم: <strong>admin</strong><br>
                🔑 كلمة المرور: <strong>admin123</strong>
            </div>
            
            <div class="device-list">
                <strong>📱 الأجهزة التي يمكنها الوصول:</strong><br>
                • 💻 أجهزة الكمبيوتر في نفس الشبكة<br>
                • 📱 الهواتف الذكية في نفس الشبكة<br>
                • 📟 الأجهزة اللوحية في نفس الشبكة<br>
                • 🖥️ أجهزة المكتب في نفس الشبكة<br><br>
                
                <strong>⚠️ ملاحظة:</strong><br>
                يجب أن تكون جميع الأجهزة متصلة بنفس شبكة الواي فاي أو الشبكة المحلية
            </div>
        </div>
    </body>
    </html>
    ''', error_message=error_message, local_ip=local_ip)

# الصفحة الرئيسية
@app.route('/')
@login_required
def index():
    """الواجهة الرئيسية للشبكة المحلية"""
    try:
        conn = get_db_connection()
        
        # إحصائيات الموظفين
        employees_count = conn.execute('SELECT COUNT(*) FROM employees WHERE status = "نشط"').fetchone()[0]
        
        # إحصائيات السيارات
        cars_count = conn.execute('SELECT COUNT(*) FROM cars').fetchone()[0]
        available_cars = conn.execute('SELECT COUNT(*) FROM cars WHERE status = "متاح"').fetchone()[0]
        used_cars = conn.execute('SELECT COUNT(*) FROM cars WHERE status = "مستخدم"').fetchone()[0]
        maintenance_cars = conn.execute('SELECT COUNT(*) FROM cars WHERE status = "في الصيانة"').fetchone()[0]
        
        # إحصائيات مالية
        treasury_balance = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY id DESC LIMIT 1').fetchone()
        current_balance = treasury_balance[0] if treasury_balance else 0
        
        # عهد السيارات النشطة
        active_custody = conn.execute('SELECT COUNT(*) FROM car_custody WHERE status = "نشط"').fetchone()[0]
        
        conn.close()
        
        local_ip = get_local_ip()
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>الواجهة الرئيسية - RASHID INDUSTRIAL CO.</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }
                .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
                .header p { font-size: 1.2rem; opacity: 0.9; }
                .content { padding: 40px; }
                .network-badge {
                    background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
                    color: #0c5460;
                    padding: 20px;
                    border-radius: 15px;
                    margin: 20px 0;
                    border: 2px solid #17a2b8;
                    text-align: center;
                    font-size: 1.1rem;
                }
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }
                .stat-card {
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    border-radius: 15px;
                    padding: 25px;
                    text-align: center;
                    border-left: 5px solid #667eea;
                    transition: transform 0.3s ease;
                }
                .stat-card:hover { transform: translateY(-5px); }
                .stat-card h3 { font-size: 2.5rem; color: #667eea; margin-bottom: 10px; }
                .stat-card p { color: #666; font-size: 1.1rem; }
                .buttons {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 40px 0;
                }
                .btn {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 18px 25px;
                    text-decoration: none;
                    border-radius: 10px;
                    font-size: 1.1rem;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    text-align: center;
                    display: block;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                }
                .btn:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                    color: white;
                    text-decoration: none;
                }
                .btn.logout {
                    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                    box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
                }
                .btn.logout:hover {
                    box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚗 نظام إدارة السيارات</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                    <p>مرحباً {{ session.username }} - متاح على الشبكة المحلية</p>
                </div>
                
                <div class="content">
                    <div class="network-badge">
                        <strong>🌐 النظام متاح على جميع الأجهزة!</strong><br>
                        📱 يمكن الوصول من الهواتف والأجهزة الأخرى عبر: <strong>http://{{ local_ip }}:5000</strong>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>{{ employees_count }}</h3>
                            <p>👥 إجمالي الموظفين</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{ cars_count }}</h3>
                            <p>🚗 إجمالي السيارات</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{ available_cars }}</h3>
                            <p>✅ السيارات المتاحة</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{ "{:,.0f}".format(current_balance) }}</h3>
                            <p>💰 رصيد الخزينة (ريال)</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{ used_cars }}</h3>
                            <p>🔴 سيارات مستخدمة</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{ maintenance_cars }}</h3>
                            <p>🔧 في الصيانة</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{ active_custody }}</h3>
                            <p>🤝 عهد نشطة</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{ local_ip }}</h3>
                            <p>🌐 عنوان IP المحلي</p>
                        </div>
                    </div>
                    
                    <div class="buttons">
                        <a href="#" class="btn">👥 إدارة الموظفين</a>
                        <a href="#" class="btn">🚗 إدارة السيارات</a>
                        <a href="#" class="btn">💰 الخزينة</a>
                        <a href="#" class="btn">🤝 عهد السيارات</a>
                        <a href="#" class="btn">📋 المصروفات</a>
                        <a href="#" class="btn">📊 التقارير</a>
                        <a href="{{ url_for('logout') }}" class="btn logout">🚪 تسجيل الخروج</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''', 
        session=session,
        employees_count=employees_count,
        cars_count=cars_count,
        available_cars=available_cars,
        used_cars=used_cars,
        maintenance_cars=maintenance_cars,
        current_balance=current_balance,
        active_custody=active_custody,
        local_ip=local_ip)
        
    except Exception as e:
        return f"خطأ في النظام: {str(e)}"

# تسجيل الخروج
@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("=" * 80)
    print("🌐 نظام إدارة السيارات - للشبكة المحلية")
    print("RASHID INDUSTRIAL CO.")
    print("=" * 80)
    
    # إنشاء قاعدة البيانات
    if init_database():
        print("✅ تم إنشاء قاعدة البيانات للشبكة المحلية")
    else:
        print("❌ فشل في إنشاء قاعدة البيانات")
        exit(1)
    
    # الحصول على عنوان IP المحلي
    local_ip = get_local_ip()
    
    print(f"\n🌐 معلومات الوصول:")
    print(f"   💻 من هذا الجهاز: http://localhost:5000")
    print(f"   📱 من الأجهزة الأخرى: http://{local_ip}:5000")
    print(f"   🔑 البيانات: admin / admin123")
    
    print(f"\n📱 الأجهزة التي يمكنها الوصول:")
    print(f"   • أجهزة الكمبيوتر في نفس الشبكة")
    print(f"   • الهواتف الذكية في نفس الشبكة")
    print(f"   • الأجهزة اللوحية في نفس الشبكة")
    print(f"   • أجهزة المكتب في نفس الشبكة")
    
    print(f"\n🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان...")
    print(f"⚠️  لإيقاف النظام: اضغط Ctrl+C")
    print("=" * 80)
    
    # فتح المتصفح في خيط منفصل
    def open_browser():
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # تشغيل النظام على جميع عناوين IP (0.0.0.0)
    app.run(host='0.0.0.0', port=5000, debug=False)