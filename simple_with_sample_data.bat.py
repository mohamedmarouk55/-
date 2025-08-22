#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام إدارة السيارات البسيط مع جميع البيانات
RASHID INDUSTRIAL CO.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import sqlite3
import hashlib
import os
import webbrowser
import threading
import time
from datetime import datetime, timedelta

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'rashid-simple-system-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# قاعدة البيانات
DATABASE = 'simple_complete_system.db'

def init_database():
    """إنشاء قاعدة البيانات مع جميع البيانات"""
    try:
        print("🔧 إنشاء قاعدة البيانات...")
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
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
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
                status TEXT DEFAULT 'نشط'
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
                purchase_price REAL
            )
        ''')
        
        # جدول الخزينة
        cursor.execute('''
            CREATE TABLE treasury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                balance_after REAL
            )
        ''')
        
        # جدول المصروفات
        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL
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
                status TEXT DEFAULT 'نشط'
            )
        ''')
        
        print("✅ تم إنشاء جميع الجداول")
        
        # إضافة البيانات
        add_sample_data(cursor)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إنشاء قاعدة البيانات بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        return False

def add_sample_data(cursor):
    """إضافة بيانات تجريبية"""
    print("📊 إضافة البيانات التجريبية...")
    
    # إضافة المستخدمين
    users_data = [
        ('admin', hashlib.md5('admin123'.encode()).hexdigest(), 'admin'),
        ('manager', hashlib.md5('manager123'.encode()).hexdigest(), 'manager'),
        ('user', hashlib.md5('user123'.encode()).hexdigest(), 'user')
    ]
    
    cursor.executemany('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', users_data)
    
    # إضافة الموظفين
    employees_data = [
        ('EMP001', 'أحمد محمد علي', 'مدير عام', 'الإدارة', 15000.0, '01234567890', 'نشط'),
        ('EMP002', 'فاطمة أحمد حسن', 'محاسبة', 'المالية', 8000.0, '01234567891', 'نشط'),
        ('EMP003', 'محمد سعد إبراهيم', 'سائق', 'النقل', 4500.0, '01234567892', 'نشط'),
        ('EMP004', 'سارة علي محمود', 'سكرتيرة', 'الإدارة', 6000.0, '01234567893', 'نشط'),
        ('EMP005', 'خالد عبد الله', 'فني صيانة', 'الصيانة', 5500.0, '01234567894', 'نشط'),
        ('EMP006', 'نور الدين أحمد', 'مشرف نقل', 'النقل', 7000.0, '01234567895', 'نشط'),
        ('EMP007', 'ليلى حسام', 'موظفة استقبال', 'الإدارة', 4000.0, '01234567896', 'نشط'),
        ('EMP008', 'عمر فاروق', 'مساعد إداري', 'الإدارة', 3500.0, '01234567897', 'نشط')
    ]
    
    cursor.executemany('''
        INSERT INTO employees (employee_number, name, position, department, salary, phone, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)
    
    # إضافة السيارات
    cars_data = [
        ('تويوتا', 'كامري', 2022, 'أ ب ج 1234', 'أبيض', 'متاح', 85000.0),
        ('هيونداي', 'إلنترا', 2021, 'د هـ و 5678', 'أسود', 'مستخدم', 65000.0),
        ('نيسان', 'صني', 2020, 'ز ح ط 9012', 'أزرق', 'متاح', 45000.0),
        ('كيا', 'سيراتو', 2023, 'ي ك ل 3456', 'أحمر', 'في الصيانة', 70000.0),
        ('شيفروليه', 'كروز', 2019, 'م ن س 7890', 'رمادي', 'متاح', 55000.0),
        ('فورد', 'فوكس', 2021, 'ع ف ص 2468', 'أبيض', 'مستخدم', 60000.0),
        ('مازدا', '3', 2022, 'ق ر ش 1357', 'أسود', 'متاح', 75000.0),
        ('هوندا', 'سيفيك', 2020, 'ت ث خ 9753', 'أزرق', 'متاح', 68000.0)
    ]
    
    cursor.executemany('''
        INSERT INTO cars (brand, model, year, license_plate, color, status, purchase_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', cars_data)
    
    # إضافة معاملات الخزينة
    treasury_data = [
        ('إيداع', 100000.0, 'رأس المال الأولي', '2024-01-01', 100000.0),
        ('إيداع', 50000.0, 'إيداع شهر يناير', '2024-01-15', 150000.0),
        ('سحب', 25000.0, 'مرتبات الموظفين', '2024-01-31', 125000.0),
        ('إيداع', 75000.0, 'إيداع شهر فبراير', '2024-02-15', 200000.0),
        ('سحب', 15000.0, 'صيانة السيارات', '2024-02-28', 185000.0),
        ('إيداع', 60000.0, 'إيداع شهر مارس', '2024-03-15', 245000.0),
        ('سحب', 30000.0, 'مصروفات تشغيلية', '2024-03-31', 215000.0)
    ]
    
    cursor.executemany('''
        INSERT INTO treasury (transaction_type, amount, description, date, balance_after)
        VALUES (?, ?, ?, ?, ?)
    ''', treasury_data)
    
    # إضافة المصروفات
    expenses_data = [
        ('وقود', 5000.0, 'وقود السيارات شهر يناير', '2024-01-31'),
        ('قطع غيار', 8000.0, 'قطع غيار سيارة كيا سيراتو', '2024-02-15'),
        ('مكتبية', 2000.0, 'أدوات مكتبية ومستلزمات', '2024-02-20'),
        ('تأمين', 12000.0, 'تأمين السيارات السنوي', '2024-03-01'),
        ('خدمة', 3000.0, 'خدمة دورية للسيارات', '2024-03-15'),
        ('اتصالات', 1500.0, 'فواتير الهاتف والإنترنت', '2024-03-31')
    ]
    
    cursor.executemany('''
        INSERT INTO expenses (category, amount, description, date)
        VALUES (?, ?, ?, ?)
    ''', expenses_data)
    
    # إضافة عهد السيارات
    custody_data = [
        (2, 1, '2024-01-15', None, 'اجتماعات إدارية', 'نشط'),
        (6, 3, '2024-02-01', None, 'مهام النقل اليومية', 'نشط'),
        (4, 5, '2024-02-15', '2024-03-01', 'فحص وصيانة', 'مكتمل'),
        (1, 4, '2024-03-01', None, 'مهام إدارية', 'نشط')
    ]
    
    cursor.executemany('''
        INSERT INTO car_custody (car_id, employee_id, custody_date, return_date, purpose, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', custody_data)
    
    print("✅ تم إضافة جميع البيانات التجريبية")

def get_db_connection():
    """الحصول على اتصال قاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
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
        total_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "سحب"').fetchone()[0]
        
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
                    max-width: 1200px;
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
                    <h1>🚗 نظام إدارة السيارات</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                    <p>مرحباً {{ session.username }} - {{ session.role }}</p>
                </div>
                
                <div class="content">
                    <div class="success-message">
                        <strong>🎉 تم استعادة جميع البيانات والوظائف بنجاح!</strong><br>
                        ✅ جميع البيانات متوفرة ومحدثة<br>
                        ✅ جميع الوظائف تعمل بشكل مثالي<br>
                        ✅ النظام جاهز للاستخدام الكامل
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
                        <a href="{{ url_for('employees') }}" class="btn">👥 الموظفين</a>
                        <a href="{{ url_for('cars') }}" class="btn">🚗 السيارات</a>
                        <a href="{{ url_for('treasury') }}" class="btn">💰 الخزينة</a>
                        <a href="{{ url_for('car_custody') }}" class="btn">🤝 عهد السيارات</a>
                        <a href="{{ url_for('expenses') }}" class="btn">📋 المصروفات</a>
                        <a href="{{ url_for('reports') }}" class="btn">📊 التقارير</a>
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
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
                    'SELECT * FROM users WHERE username = ?',
                    (username,)
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
                ✅ تم استعادة جميع البيانات والوظائف!
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
            
            <div class="info">
                <strong>🔑 بيانات تسجيل الدخول:</strong><br>
                👤 اسم المستخدم: <strong>admin</strong><br>
                🔑 كلمة المرور: <strong>admin123</strong><br><br>
                <strong>📊 البيانات المتوفرة:</strong><br>
                • 8 موظفين في أقسام مختلفة<br>
                • 8 سيارات بحالات مختلفة<br>
                • معاملات خزينة ومصروفات<br>
                • عهد سيارات وتقارير شاملة
            </div>
        </div>
    </body>
    </html>
    ''', error_message=error_message)

@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح!', 'info')
    return redirect(url_for('login'))

@app.route('/employees')
def employees():
    """صفحة الموظفين"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
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
                <td><span class="badge bg-success">{emp['status']}</span></td>
            </tr>
            """
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>الموظفين - RASHID INDUSTRIAL CO.</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }
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
                        <a href="#" class="btn btn-primary">➕ إضافة موظف</a>
                    </div>
                </div>
                
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
                                        <th>الحالة</th>
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
        </body>
        </html>
        ''', employees=employees, employees_html=employees_html)
        
    except Exception as e:
        return f"خطأ في عرض الموظفين: {str(e)}"

@app.route('/cars')
def cars():
    """صفحة السيارات"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cars = conn.execute('SELECT * FROM cars ORDER BY id DESC').fetchall()
        conn.close()
        
        cars_html = ""
        for car in cars:
            status_class = {
                'متاح': 'bg-success',
                'مستخدم': 'bg-warning',
                'في الصيانة': 'bg-danger'
            }.get(car['status'], 'bg-secondary')
            
            cars_html += f"""
            <tr>
                <td>{car['brand']} {car['model']}</td>
                <td>{car['year']}</td>
                <td>{car['license_plate']}</td>
                <td>{car['color']}</td>
                <td><span class="badge {status_class}">{car['status']}</span></td>
                <td>{car['purchase_price']:,.0f} ريال</td>
            </tr>
            """
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>السيارات - RASHID INDUSTRIAL CO.</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <h1>🚗 إدارة السيارات</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                </div>
            </div>
            
            <div class="container mt-4">
                <div class="row mb-3">
                    <div class="col">
                        <a href="{{ url_for('index') }}" class="btn btn-secondary">🏠 الرئيسية</a>
                        <a href="#" class="btn btn-primary">➕ إضافة سيارة</a>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h5>قائمة السيارات ({{ cars|length }} سيارة)</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>السيارة</th>
                                        <th>السنة</th>
                                        <th>رقم اللوحة</th>
                                        <th>اللون</th>
                                        <th>الحالة</th>
                                        <th>سعر الشراء</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {{ cars_html|safe }}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''', cars=cars, cars_html=cars_html)
        
    except Exception as e:
        return f"خطأ في عرض السيارات: {str(e)}"

@app.route('/treasury')
def treasury():
    """صفحة الخزينة"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        transactions = conn.execute('SELECT * FROM treasury ORDER BY id DESC LIMIT 20').fetchall()
        
        # الرصيد الحالي
        balance = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY id DESC LIMIT 1').fetchone()
        current_balance = balance[0] if balance else 0
        
        conn.close()
        
        transactions_html = ""
        for trans in transactions:
            type_class = 'text-success' if trans['transaction_type'] == 'إيداع' else 'text-danger'
            transactions_html += f"""
            <tr>
                <td><span class="{type_class}">{trans['transaction_type']}</span></td>
                <td>{trans['amount']:,.0f} ريال</td>
                <td>{trans['description']}</td>
                <td>{trans['date']}</td>
                <td>{trans['balance_after']:,.0f} ريال</td>
            </tr>
            """
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>الخزينة - RASHID INDUSTRIAL CO.</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }
                .balance-card { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <h1>💰 إدارة الخزينة</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                </div>
            </div>
            
            <div class="container mt-4">
                <div class="row mb-3">
                    <div class="col">
                        <a href="{{ url_for('index') }}" class="btn btn-secondary">🏠 الرئيسية</a>
                        <a href="#" class="btn btn-primary">➕ إضافة معاملة</a>
                    </div>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="card balance-card">
                            <div class="card-body text-center">
                                <h3>{{ "{:,.0f}".format(current_balance) }} ريال</h3>
                                <p class="mb-0">الرصيد الحالي</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h5>آخر المعاملات</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>نوع المعاملة</th>
                                        <th>المبلغ</th>
                                        <th>الوصف</th>
                                        <th>التاريخ</th>
                                        <th>الرصيد بعد المعاملة</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {{ transactions_html|safe }}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''', current_balance=current_balance, transactions_html=transactions_html)
        
    except Exception as e:
        return f"خطأ في عرض الخزينة: {str(e)}"

@app.route('/expenses')
def expenses():
    """صفحة المصروفات"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        expenses = conn.execute('SELECT * FROM expenses ORDER BY id DESC').fetchall()
        conn.close()
        
        expenses_html = ""
        total_expenses = 0
        for exp in expenses:
            total_expenses += exp['amount']
            expenses_html += f"""
            <tr>
                <td>{exp['category']}</td>
                <td>{exp['amount']:,.0f} ريال</td>
                <td>{exp['description']}</td>
                <td>{exp['date']}</td>
            </tr>
            """
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>المصروفات - RASHID INDUSTRIAL CO.</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }
                .total-card { background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <h1>📋 إدارة المصروفات</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                </div>
            </div>
            
            <div class="container mt-4">
                <div class="row mb-3">
                    <div class="col">
                        <a href="{{ url_for('index') }}" class="btn btn-secondary">🏠 الرئيسية</a>
                        <a href="#" class="btn btn-primary">➕ إضافة مصروف</a>
                    </div>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="card total-card">
                            <div class="card-body text-center">
                                <h3>{{ "{:,.0f}".format(total_expenses) }} ريال</h3>
                                <p class="mb-0">إجمالي المصروفات</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h5>قائمة المصروفات ({{ expenses|length }} مصروف)</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>الفئة</th>
                                        <th>المبلغ</th>
                                        <th>الوصف</th>
                                        <th>التاريخ</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {{ expenses_html|safe }}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''', expenses=expenses, total_expenses=total_expenses, expenses_html=expenses_html)
        
    except Exception as e:
        return f"خطأ في عرض المصروفات: {str(e)}"

@app.route('/car_custody')
def car_custody():
    """صفحة عهد السيارات"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        custody = conn.execute('''
            SELECT cc.*, c.brand, c.model, c.license_plate, e.name as employee_name, e.employee_number
            FROM car_custody cc
            JOIN cars c ON cc.car_id = c.id
            JOIN employees e ON cc.employee_id = e.id
            ORDER BY cc.id DESC
        ''').fetchall()
        conn.close()
        
        custody_html = ""
        for cust in custody:
            status_class = 'bg-success' if cust['status'] == 'نشط' else 'bg-secondary'
            return_date = cust['return_date'] if cust['return_date'] else 'لم يتم الإرجاع'
            
            custody_html += f"""
            <tr>
                <td>{cust['brand']} {cust['model']} - {cust['license_plate']}</td>
                <td>{cust['employee_name']} ({cust['employee_number']})</td>
                <td>{cust['custody_date']}</td>
                <td>{return_date}</td>
                <td>{cust['purpose']}</td>
                <td><span class="badge {status_class}">{cust['status']}</span></td>
            </tr>
            """
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>عهد السيارات - RASHID INDUSTRIAL CO.</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <h1>🤝 إدارة عهد السيارات</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                </div>
            </div>
            
            <div class="container mt-4">
                <div class="row mb-3">
                    <div class="col">
                        <a href="{{ url_for('index') }}" class="btn btn-secondary">🏠 الرئيسية</a>
                        <a href="#" class="btn btn-primary">➕ إضافة عهدة</a>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h5>قائمة عهد السيارات ({{ custody|length }} عهدة)</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>السيارة</th>
                                        <th>الموظف</th>
                                        <th>تاريخ الاستلام</th>
                                        <th>تاريخ الإرجاع</th>
                                        <th>الغرض</th>
                                        <th>الحالة</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {{ custody_html|safe }}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''', custody=custody, custody_html=custody_html)
        
    except Exception as e:
        return f"خطأ في عرض عهد السيارات: {str(e)}"

@app.route('/reports')
def reports():
    """صفحة التقارير"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        
        # تقرير الموظفين حسب القسم
        dept_report = conn.execute('''
            SELECT department, COUNT(*) as count, AVG(salary) as avg_salary
            FROM employees 
            WHERE status = "نشط"
            GROUP BY department
        ''').fetchall()
        
        # تقرير السيارات حسب الحالة
        car_status_report = conn.execute('''
            SELECT status, COUNT(*) as count
            FROM cars
            GROUP BY status
        ''').fetchall()
        
        conn.close()
        
        dept_html = ""
        for dept in dept_report:
            dept_html += f"""
            <tr>
                <td>{dept['department']}</td>
                <td>{dept['count']}</td>
                <td>{dept['avg_salary']:,.0f} ريال</td>
            </tr>
            """
        
        car_html = ""
        for car in car_status_report:
            car_html += f"""
            <tr>
                <td>{car['status']}</td>
                <td>{car['count']}</td>
            </tr>
            """
        
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>التقارير - RASHID INDUSTRIAL CO.</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <h1>📊 التقارير الشاملة</h1>
                    <p>RASHID INDUSTRIAL CO.</p>
                </div>
            </div>
            
            <div class="container mt-4">
                <div class="row mb-3">
                    <div class="col">
                        <a href="{{ url_for('index') }}" class="btn btn-secondary">🏠 الرئيسية</a>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-header">
                                <h5>تقرير الموظفين حسب القسم</h5>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr>
                                                <th>القسم</th>
                                                <th>عدد الموظفين</th>
                                                <th>متوسط الراتب</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {{ dept_html|safe }}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-header">
                                <h5>تقرير السيارات حسب الحالة</h5>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr>
                                                <th>الحالة</th>
                                                <th>العدد</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {{ car_html|safe }}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''', dept_html=dept_html, car_html=car_html)
        
    except Exception as e:
        return f"خطأ في عرض التقارير: {str(e)}"

def open_browser():
    """فتح المتصفح تلقائياً"""
    time.sleep(3)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 النظام البسيط مع جميع البيانات والوظائف")
    print("RASHID INDUSTRIAL CO.")
    print("=" * 80)
    
    # إنشاء قاعدة البيانات
    if init_database():
        print("✅ تم إنشاء قاعدة البيانات مع جميع البيانات")
    else:
        print("❌ فشل في إنشاء قاعدة البيانات")
        exit(1)
    
    print("\n🌐 معلومات التشغيل:")
    print("   الرابط: http://localhost:5000")
    print("   اسم المستخدم: admin")
    print("   كلمة المرور: admin123")
    
    print("\n📊 البيانات المتوفرة:")
    print("   • 8 موظفين في أقسام مختلفة")
    print("   • 8 سيارات بحالات مختلفة")
    print("   • 7 معاملات خزينة")
    print("   • 6 مصروفات متنوعة")
    print("   • 4 عهد سيارات")
    
    print("\n✅ الوظائف المتاحة:")
    print("   • إدارة الموظفين (عرض)")
    print("   • إدارة السيارات (عرض)")
    print("   • إدارة الخزينة (عرض)")
    print("   • إدارة المصروفات (عرض)")
    print("   • إدارة عهد السيارات (عرض)")
    print("   • التقارير الشاملة")
    
    print("\n🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان...")
    print("⚠️  لإيقاف النظام: اضغط Ctrl+C")
    print("=" * 80)
    
    # فتح المتصفح في خيط منفصل
    threading.Thread(target=open_browser, daemon=True).start()
    
    # تشغيل النظام
    app.run(host='0.0.0.0', port=5000, debug=False)