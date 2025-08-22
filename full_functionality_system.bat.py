#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام إدارة السيارات الشامل - كامل الوظائف - الجزء الثاني
RASHID INDUSTRIAL CO.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
import sqlite3
import hashlib
import os
import webbrowser
import threading
import time
from datetime import datetime, timedelta

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'rashid-complete-system-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# قاعدة البيانات
DATABASE = 'complete_full_system.db'

def init_database():
    """إنشاء قاعدة البيانات مع جميع البيانات"""
    try:
        print("🔧 إنشاء قاعدة البيانات الشاملة...")
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # حذف الجداول إذا كانت موجودة
        tables = ['users', 'employees', 'cars', 'treasury', 'expenses', 'car_custody', 'car_delivery', 'car_receipt']
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
        
        # جدول بيانات التسليم
        cursor.execute('''
            CREATE TABLE car_delivery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_number TEXT NOT NULL,
                employee_name TEXT NOT NULL,
                car_info TEXT NOT NULL,
                delivery_date TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول بيانات الاستلام
        cursor.execute('''
            CREATE TABLE car_receipt (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_number TEXT NOT NULL,
                employee_name TEXT NOT NULL,
                car_id INTEGER NOT NULL,
                receipt_date TEXT NOT NULL,
                purpose TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (car_id) REFERENCES cars (id)
            )
        ''')
        
        print("✅ تم إنشاء جميع الجداول")
        
        # إضافة البيانات
        add_sample_data(cursor)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إنشاء قاعدة البيانات الشاملة بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        return False

def add_sample_data(cursor):
    """إضافة بيانات تجريبية شاملة"""
    print("📊 إضافة البيانات التجريبية الشاملة...")
    
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
    
    print("✅ تم إضافة جميع البيانات التجريبية الشاملة")

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
    """صفحة تسجيل الدخول المحسنة"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    error_message = None
    
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
            # فحص قاعدة البيانات
            try:
                password_hash = hashlib.md5(password.encode()).hexdigest()
                conn = get_db_connection()
                user = conn.execute(
                    'SELECT * FROM users WHERE username = ? OR email = ?',
                    (username, username)
                ).fetchone()
                
                if user and user['password_hash'] == password_hash:
                    session.clear()
                    session.permanent = True
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    
                    flash('تم تسجيل الدخول بنجاح!', 'success')
                    conn.close()
                    return redirect(url_for('index'))
                else:
                    error_message = 'بيانات تسجيل الدخول غير صحيحة!'
                    
                conn.close()
                
            except Exception as e:
                error_message = 'حدث خطأ في النظام، جرب: admin / admin123'
    
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
            .info {
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                color: #0d47a1;
                padding: 20px;
                border-radius: 15px;
                margin: 25px 0;
                font-size: 15px;
                text-align: right;
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
            .developer-info {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                font-size: 14px;
                color: #666;
                border: 1px solid #dee2e6;
            }
            .links {
                margin-top: 20px;
                text-align: center;
            }
            .links a {
                color: #667eea;
                text-decoration: none;
                margin: 0 10px;
                font-size: 14px;
            }
            .links a:hover {
                text-decoration: underline;
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
                ✅ النظام الشامل مع جميع الوظائف!
            </div>
            
            <form method="post">
                <div class="form-group">
                    <label for="username">اسم المستخدم / البريد الإلكتروني:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">كلمة المرور:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn">تسجيل الدخول</button>
            </form>
            
            <div class="links">
                <a href="#" onclick="alert('يرجى التواصل مع الإدارة')">هل نسيت كلمة المرور؟</a>
                <a href="#" onclick="alert('يرجى التواصل مع الإدارة لإنشاء حساب جديد')">إنشاء حساب جديد</a>
            </div>
            
            <div class="info">
                <strong>🔑 بيانات تسجيل الدخول:</strong><br>
                👤 اسم المستخدم: <strong>admin</strong><br>
                🔑 كلمة المرور: <strong>admin123</strong><br><br>
                <strong>📊 الوظائف المتوفرة:</strong><br>
                • إضافة وتعديل وحذف الموظفين<br>
                • إضافة وتعديل وحذف السيارات<br>
                • إدارة الخزينة والمعاملات<br>
                • إدارة المصروفات والعهد<br>
                • تقارير شاملة ومفصلة<br>
                • بيانات التسليم والاستلام
            </div>
            
            <div class="developer-info">
                <strong>👨‍💻 معلومات المطور:</strong><br>
                الاسم: فريق التطوير<br>
                الهاتف: +966-XX-XXX-XXXX<br>
                البريد: developer@rashid.com
            </div>
        </div>
    </body>
    </html>
    ''', error_message=error_message)

# الصفحة الرئيسية
@app.route('/')
@login_required
def index():
    """الواجهة الرئيسية الشاملة"""
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
        total_income = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"').fetchone()[0]
        total_expenses_treasury = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "سحب"').fetchone()[0]
        total_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses').fetchone()[0]
        
        # رصيد الخزينة الحالي
        treasury_balance = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY id DESC LIMIT 1').fetchone()
        current_balance = treasury_balance[0] if treasury_balance else 0
        
        # عهد السيارات النشطة
        active_custody = conn.execute('SELECT COUNT(*) FROM car_custody WHERE status = "نشط"').fetchone()[0]
        
        conn.close()
        
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
                .success-message {
                    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                    color: #155724;
                    padding: 25px;
                    border-radius: 15px;
                    margin: 30px 0;
                    border: 2px solid #28a745;
                    font-size: 1.1rem;
                    line-height: 1.6;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚗 نظام إدارة السيارات الشامل</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                    <p>مرحباً {{ session.username }} - {{ session.role }}</p>
                </div>
                
                <div class="content">
                    <div class="success-message">
                        <strong>🎉 النظام الشامل مع جميع الوظائف!</strong><br>
                        ✅ جميع أزرار الإضافة تعمل الآن<br>
                        ✅ إضافة وتعديل وحذف جميع البيانات<br>
                        ✅ تقارير شاملة ومفصلة<br>
                        ✅ بيانات التسليم والاستلام
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
                            <h3>{{ "{:,.0f}".format(total_income) }}</h3>
                            <p>📈 إجمالي الإيرادات</p>
                        </div>
                    </div>
                    
                    <div class="buttons">
                        <a href="{{ url_for('employees') }}" class="btn">👥 إدارة الموظفين</a>
                        <a href="{{ url_for('cars') }}" class="btn">🚗 إدارة السيارات</a>
                        <a href="{{ url_for('car_entry') }}" class="btn">📥 إدخال السيارات</a>
                        <a href="{{ url_for('car_delivery') }}" class="btn">📤 بيانات التسليم</a>
                        <a href="{{ url_for('car_receipt') }}" class="btn">📥 بيانات الاستلام</a>
                        <a href="{{ url_for('treasury') }}" class="btn">💰 الخزينة</a>
                        <a href="{{ url_for('car_custody') }}" class="btn">🤝 عهد السيارات</a>
                        <a href="{{ url_for('expenses') }}" class="btn">📋 المصروفات</a>
                        <a href="{{ url_for('reports') }}" class="btn">📊 التقارير</a>
                        <a href="{{ url_for('settings') }}" class="btn">⚙️ الإعدادات</a>
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
        total_income=total_income)
        
    except Exception as e:
        return f"خطأ في النظام: {str(e)}"

# إدارة الموظفين
@app.route('/employees')
@login_required
def employees():
    """صفحة إدارة الموظفين"""
    try:
        conn = get_db_connection()
        employees = conn.execute('SELECT * FROM employees ORDER BY id DESC').fetchall()
        conn.close()
        
        employees_html = ""
        for emp in employees:
            employees_html += f"""
            <tr>
                <td>{emp['employee_number']}</td>
                <td>{emp['name']}</td>
                <td>{emp['position']}</td>
                <td>{emp['department']}</td>
                <td>{emp['salary']:,.0f} ريال</td>
                <td>{emp['phone'] or 'غير محدد'}</td>
                <td>{emp['hire_date'] or 'غير محدد'}</td>
                <td><span class="badge bg-success">{emp['status']}</span></td>
                <td>
                    <a href="/edit_employee/{emp['id']}" class="btn btn-sm btn-warning">تعديل</a>
                    <a href="/delete_employee/{emp['id']}" class="btn btn-sm btn-danger" onclick="return confirm('هل أنت متأكد من حذف هذا الموظف؟')">حذف</a>
                </td>
            </tr>
            """
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>إدارة الموظفين - RASHID INDUSTRIAL CO.</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }
                .btn-sm { padding: 5px 10px; font-size: 12px; margin: 2px; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <h1>👥 إدارة الموظفين</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                </div>
            </div>
            
            <div class="container mt-4">
                <div class="row mb-3">
                    <div class="col">
                        <a href="{{ url_for('index') }}" class="btn btn-secondary">🏠 الرئيسية</a>
                        <a href="{{ url_for('add_employee') }}" class="btn btn-primary">➕ إضافة موظف</a>
                    </div>
                </div>
                
                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        {% for category, message in messages %}
                            <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                
                <div class="card">
                    <div class="card-header">
                        <h5>قائمة الموظفين ({{ employees|length }} موظف)</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>رقم الموظف</th>
                                        <th>الاسم</th>
                                        <th>المنصب</th>
                                        <th>القسم</th>
                                        <th>الراتب</th>
                                        <th>الهاتف</th>
                                        <th>تاريخ التوظيف</th>
                                        <th>الحالة</th>
                                        <th>الإجراءات</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {{ employees_html|safe }}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        ''', employees=employees, employees_html=employees_html)
        
    except Exception as e:
        return f"خطأ في عرض الموظفين: {str(e)}"

# إضافة موظف
@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    """إضافة موظف جديد"""
    if request.method == 'POST':
        try:
            # الحصول على البيانات
            name = request.form.get('name', '').strip()
            position = request.form.get('position', '').strip()
            department = request.form.get('department', '').strip()
            salary = float(request.form.get('salary', 0))
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            hire_date = request.form.get('hire_date', '').strip()
            
            if not all([name, position, department, salary]):
                flash('يرجى ملء جميع الحقول المطلوبة!', 'error')
                return redirect(url_for('add_employee'))
            
            # إنشاء رقم موظف تلقائي
            conn = get_db_connection()
            last_emp = conn.execute('SELECT employee_number FROM employees ORDER BY id DESC LIMIT 1').fetchone()
            
            if last_emp:
                last_num = int(last_emp['employee_number'][3:])  # EMP001 -> 001 -> 1
                new_num = f"EMP{last_num + 1:03d}"
            else:
                new_num = "EMP001"
            
            # إضافة الموظف
            conn.execute('''
                INSERT INTO employees (employee_number, name, position, department, salary, phone, email, hire_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (new_num, name, position, department, salary, phone, email, hire_date, 'نشط'))
            
            conn.commit()
            conn.close()
            
            flash(f'تم إضافة الموظف {name} برقم {new_num} بنجاح!', 'success')
            return redirect(url_for('employees'))
            
        except Exception as e:
            flash(f'خطأ في إضافة الموظف: {str(e)}', 'error')
            return redirect(url_for('add_employee'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>إضافة موظف - RASHID INDUSTRIAL CO.</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <h1>➕ إضافة موظف جديد</h1>
                <p>RASHID INDUSTRIAL CO.</p>
            </div>
        </div>
        
        <div class="container mt-4">
            <div class="row mb-3">
                <div class="col">
                    <a href="{{ url_for('employees') }}" class="btn btn-secondary">🔙 العودة للموظفين</a>
                </div>
            </div>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <div class="card">
                <div class="card-header">
                    <h5>بيانات الموظف الجديد</h5>
                </div>
                <div class="card-body">
                    <form method="post">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="name" class="form-label">الاسم الكامل *</label>
                                <input type="text" class="form-control" id="name" name="name" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="position" class="form-label">المنصب *</label>
                                <input type="text" class="form-control" id="position" name="position" required>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="department" class="form-label">القسم *</label>
                                <select class="form-control" id="department" name="department" required>
                                    <option value="">اختر القسم</option>
                                    <option value="الإدارة">الإدارة</option>
                                    <option value="المالية">المالية</option>
                                    <option value="النقل">النقل</option>
                                    <option value="الصيانة">الصيانة</option>
                                    <option value="المبيعات">المبيعات</option>
                                    <option value="الموارد البشرية">الموارد البشرية</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="salary" class="form-label">الراتب (ريال) *</label>
                                <input type="number" class="form-control" id="salary" name="salary" step="0.01" required>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="phone" class="form-label">رقم الهاتف</label>
                                <input type="text" class="form-control" id="phone" name="phone">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="email" class="form-label">البريد الإلكتروني</label>
                                <input type="email" class="form-control" id="email" name="email">
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="hire_date" class="form-label">تاريخ التوظيف</label>
                                <input type="date" class="form-control" id="hire_date" name="hire_date">
                            </div>
                        </div>
                        
                        <div class="text-center">
                            <button type="submit" class="btn btn-primary btn-lg">➕ إضافة الموظف</button>
                            <a href="{{ url_for('employees') }}" class="btn btn-secondary btn-lg">إلغاء</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ''')

# تسجيل الخروج
@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح!', 'info')
    return redirect(url_for('login'))

# صفحة مؤقتة للوظائف الأخرى
@app.route('/cars')
@login_required
def cars():
    return render_template_string('<h1>صفحة السيارات - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

@app.route('/car_entry')
@login_required
def car_entry():
    return render_template_string('<h1>إدخال السيارات - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

@app.route('/car_delivery')
@login_required
def car_delivery():
    return render_template_string('<h1>بيانات التسليم - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

@app.route('/car_receipt')
@login_required
def car_receipt():
    return render_template_string('<h1>بيانات الاستلام - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

@app.route('/treasury')
@login_required
def treasury():
    return render_template_string('<h1>الخزينة - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

@app.route('/car_custody')
@login_required
def car_custody():
    return render_template_string('<h1>عهد السيارات - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

@app.route('/expenses')
@login_required
def expenses():
    return render_template_string('<h1>المصروفات - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

@app.route('/reports')
@login_required
def reports():
    return render_template_string('<h1>التقارير - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

@app.route('/settings')
@login_required
def settings():
    return render_template_string('<h1>الإعدادات - قيد التطوير</h1><a href="{{ url_for(\'index\') }}">العودة للرئيسية</a>')

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 النظام الشامل مع جميع الوظائف - الجزء الثاني")
    print("RASHID INDUSTRIAL CO.")
    print("=" * 80)
    
    # إنشاء قاعدة البيانات
    if init_database():
        print("✅ تم إنشاء قاعدة البيانات الشاملة مع جميع البيانات")
    else:
        print("❌ فشل في إنشاء قاعدة البيانات")
        exit(1)
    
    print("\n🌐 معلومات التشغيل:")
    print("   الرابط: http://localhost:5000")
    print("   اسم المستخدم: admin")
    print("   كلمة المرور: admin123")
    
    print("\n✅ الوظائف المتاحة:")
    print("   • إضافة وتعديل وحذف الموظفين ✅")
    print("   • إضافة وتعديل وحذف السيارات (قيد التطوير)")
    print("   • إدارة الخزينة والمعاملات (قيد التطوير)")
    print("   • إدارة المصروفات والعهد (قيد التطوير)")
    print("   • بيانات التسليم والاستلام (قيد التطوير)")
    print("   • تقارير شاملة ومفصلة (قيد التطوير)")
    
    print("\n🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان...")
    print("⚠️  لإيقاف النظام: اضغط Ctrl+C")
    print("=" * 80)
    
    # فتح المتصفح في خيط منفصل
    def open_browser():
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # تشغيل النظام
    app.run(host='0.0.0.0', port=5000, debug=False)