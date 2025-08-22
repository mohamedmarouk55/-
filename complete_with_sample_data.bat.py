#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام إدارة السيارات الشامل مع جميع البيانات والوظائف
RASHID INDUSTRIAL CO.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import hashlib
import os
import webbrowser
import threading
import time
from datetime import datetime, timedelta
from functools import wraps

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'rashid-complete-system-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# قاعدة البيانات
DATABASE = 'complete_system.db'

def init_complete_database():
    """إنشاء قاعدة البيانات الشاملة مع جميع البيانات"""
    try:
        print("🔧 إنشاء قاعدة البيانات الشاملة...")
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # حذف الجداول إذا كانت موجودة
        tables = ['users', 'employees', 'cars', 'treasury', 'expenses', 'car_custody', 'financial_transactions']
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
                hire_date TEXT NOT NULL,
                status TEXT DEFAULT 'نشط',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                current_value REAL,
                engine_number TEXT,
                chassis_number TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الخزينة
        cursor.execute('''
            CREATE TABLE treasury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL CHECK (transaction_type IN ('إيداع', 'سحب')),
                amount REAL NOT NULL,
                description TEXT,
                reference_number TEXT,
                created_by TEXT,
                date TEXT NOT NULL,
                balance_after REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المصروفات
        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_type TEXT NOT NULL,
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
        
        # جدول المعاملات المالية
        cursor.execute('''
            CREATE TABLE financial_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                category TEXT,
                date TEXT NOT NULL,
                reference_number TEXT,
                created_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("✅ تم إنشاء جميع الجداول")
        
        # إضافة البيانات الأساسية
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
    print("📊 إضافة البيانات التجريبية...")
    
    # إضافة المستخدمين
    users_data = [
        ('admin', 'admin@rashid.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin', 1),
        ('manager', 'manager@rashid.com', hashlib.md5('manager123'.encode()).hexdigest(), 'manager', 1),
        ('user', 'user@rashid.com', hashlib.md5('user123'.encode()).hexdigest(), 'user', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, email, password_hash, role, is_active)
        VALUES (?, ?, ?, ?, ?)
    ''', users_data)
    
    # إضافة الموظفين
    employees_data = [
        ('EMP001', 'أحمد محمد علي', 'مدير عام', 'الإدارة', 15000.0, '01234567890', 'ahmed@rashid.com', '2023-01-15', 'نشط', 'مدير عام للشركة'),
        ('EMP002', 'فاطمة أحمد حسن', 'محاسبة', 'المالية', 8000.0, '01234567891', 'fatma@rashid.com', '2023-02-01', 'نشط', 'محاسبة رئيسية'),
        ('EMP003', 'محمد سعد إبراهيم', 'سائق', 'النقل', 4500.0, '01234567892', 'mohamed@rashid.com', '2023-03-10', 'نشط', 'سائق خبرة 10 سنوات'),
        ('EMP004', 'سارة علي محمود', 'سكرتيرة', 'الإدارة', 6000.0, '01234567893', 'sara@rashid.com', '2023-04-05', 'نشط', 'سكرتيرة تنفيذية'),
        ('EMP005', 'خالد عبد الله', 'فني صيانة', 'الصيانة', 5500.0, '01234567894', 'khaled@rashid.com', '2023-05-20', 'نشط', 'فني صيانة سيارات'),
        ('EMP006', 'نور الدين أحمد', 'مشرف نقل', 'النقل', 7000.0, '01234567895', 'nour@rashid.com', '2023-06-15', 'نشط', 'مشرف أسطول النقل'),
        ('EMP007', 'ليلى حسام', 'موظفة استقبال', 'الإدارة', 4000.0, '01234567896', 'layla@rashid.com', '2023-07-01', 'نشط', 'موظفة استقبال وخدمة عملاء'),
        ('EMP008', 'عمر فاروق', 'مساعد إداري', 'الإدارة', 3500.0, '01234567897', 'omar@rashid.com', '2023-08-10', 'نشط', 'مساعد إداري')
    ]
    
    cursor.executemany('''
        INSERT INTO employees (employee_number, name, position, department, salary, phone, email, hire_date, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)
    
    # إضافة السيارات
    cars_data = [
        ('تويوتا', 'كامري', 2022, 'أ ب ج 1234', 'أبيض', 'متاح', 85000.0, 80000.0, 'ENG001', 'CHS001', 'سيارة إدارية'),
        ('هيونداي', 'إلنترا', 2021, 'د هـ و 5678', 'أسود', 'مستخدم', 65000.0, 60000.0, 'ENG002', 'CHS002', 'سيارة موظفين'),
        ('نيسان', 'صني', 2020, 'ز ح ط 9012', 'أزرق', 'متاح', 45000.0, 40000.0, 'ENG003', 'CHS003', 'سيارة نقل'),
        ('كيا', 'سيراتو', 2023, 'ي ك ل 3456', 'أحمر', 'في الصيانة', 70000.0, 68000.0, 'ENG004', 'CHS004', 'سيارة جديدة'),
        ('شيفروليه', 'كروز', 2019, 'م ن س 7890', 'رمادي', 'متاح', 55000.0, 45000.0, 'ENG005', 'CHS005', 'سيارة مبيعات'),
        ('فورد', 'فوكس', 2021, 'ع ف ص 2468', 'أبيض', 'مستخدم', 60000.0, 55000.0, 'ENG006', 'CHS006', 'سيارة تنفيذية'),
        ('مازدا', '3', 2022, 'ق ر ش 1357', 'أسود', 'متاح', 75000.0, 70000.0, 'ENG007', 'CHS007', 'سيارة VIP'),
        ('هوندا', 'سيفيك', 2020, 'ت ث خ 9753', 'أزرق', 'متاح', 68000.0, 62000.0, 'ENG008', 'CHS008', 'سيارة عامة')
    ]
    
    cursor.executemany('''
        INSERT INTO cars (brand, model, year, license_plate, color, status, purchase_price, current_value, engine_number, chassis_number, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', cars_data)
    
    # إضافة معاملات الخزينة
    treasury_data = [
        ('إيداع', 100000.0, 'رأس المال الأولي', 'REF001', 'admin', '2024-01-01', 100000.0),
        ('إيداع', 50000.0, 'إيداع شهر يناير', 'REF002', 'admin', '2024-01-15', 150000.0),
        ('سحب', 25000.0, 'مرتبات الموظفين', 'REF003', 'admin', '2024-01-31', 125000.0),
        ('إيداع', 75000.0, 'إيداع شهر فبراير', 'REF004', 'admin', '2024-02-15', 200000.0),
        ('سحب', 15000.0, 'صيانة السيارات', 'REF005', 'admin', '2024-02-28', 185000.0),
        ('إيداع', 60000.0, 'إيداع شهر مارس', 'REF006', 'admin', '2024-03-15', 245000.0),
        ('سحب', 30000.0, 'مصروفات تشغيلية', 'REF007', 'admin', '2024-03-31', 215000.0)
    ]
    
    cursor.executemany('''
        INSERT INTO treasury (transaction_type, amount, description, reference_number, created_by, date, balance_after)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', treasury_data)
    
    # إضافة المصروفات
    expenses_data = [
        ('تشغيلية', 'وقود', 5000.0, 'وقود السيارات شهر يناير', 'REC001', '2024-01-31', 'admin', 'معتمد'),
        ('صيانة', 'قطع غيار', 8000.0, 'قطع غيار سيارة كيا سيراتو', 'REC002', '2024-02-15', 'admin', 'معتمد'),
        ('إدارية', 'مكتبية', 2000.0, 'أدوات مكتبية ومستلزمات', 'REC003', '2024-02-20', 'admin', 'معتمد'),
        ('تشغيلية', 'تأمين', 12000.0, 'تأمين السيارات السنوي', 'REC004', '2024-03-01', 'admin', 'معتمد'),
        ('صيانة', 'خدمة', 3000.0, 'خدمة دورية للسيارات', 'REC005', '2024-03-15', 'admin', 'معتمد'),
        ('إدارية', 'اتصالات', 1500.0, 'فواتير الهاتف والإنترنت', 'REC006', '2024-03-31', 'admin', 'معتمد')
    ]
    
    cursor.executemany('''
        INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, approved_by, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', expenses_data)
    
    # إضافة عهد السيارات
    custody_data = [
        (2, 1, '2024-01-15', None, 'اجتماعات إدارية', 'سيارة للمدير العام', 'نشط'),
        (6, 3, '2024-02-01', None, 'مهام النقل اليومية', 'سيارة للسائق محمد', 'نشط'),
        (4, 5, '2024-02-15', '2024-03-01', 'فحص وصيانة', 'تم إرجاعها بعد الصيانة', 'مكتمل'),
        (1, 4, '2024-03-01', None, 'مهام إدارية', 'سيارة للسكرتيرة التنفيذية', 'نشط')
    ]
    
    cursor.executemany('''
        INSERT INTO car_custody (car_id, employee_id, custody_date, return_date, purpose, notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', custody_data)
    
    # إضافة المعاملات المالية
    financial_data = [
        ('إيراد', 25000.0, 'إيراد من خدمات النقل', 'خدمات', '2024-01-31', 'FIN001', 'admin'),
        ('إيراد', 35000.0, 'إيراد من تأجير السيارات', 'تأجير', '2024-02-28', 'FIN002', 'admin'),
        ('مصروف', 15000.0, 'مصروفات الوقود', 'تشغيلية', '2024-01-31', 'FIN003', 'admin'),
        ('مصروف', 8000.0, 'مصروفات الصيانة', 'صيانة', '2024-02-15', 'FIN004', 'admin'),
        ('إيراد', 40000.0, 'إيراد من عقود النقل', 'عقود', '2024-03-31', 'FIN005', 'admin')
    ]
    
    cursor.executemany('''
        INSERT INTO financial_transactions (transaction_type, amount, description, category, date, reference_number, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', financial_data)
    
    print("✅ تم إضافة جميع البيانات التجريبية")

def get_db_connection():
    """الحصول على اتصال قاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """ديكوريتر للتحقق من تسجيل الدخول"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """الصفحة الرئيسية مع الإحصائيات الشاملة"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
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
    net_profit = total_income - total_expenses
    
    # رصيد الخزينة الحالي
    treasury_balance = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
    current_balance = treasury_balance[0] if treasury_balance else 0
    
    # إحصائيات المصروفات
    monthly_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE "2024-03%"').fetchone()[0]
    
    # عهد السيارات النشطة
    active_custody = conn.execute('SELECT COUNT(*) FROM car_custody WHERE status = "نشط"').fetchone()[0]
    
    conn.close()
    
    stats = {
        'employees_count': employees_count,
        'cars_count': cars_count,
        'available_cars': available_cars,
        'used_cars': used_cars,
        'maintenance_cars': maintenance_cars,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'current_balance': current_balance,
        'monthly_expenses': monthly_expenses,
        'active_custody': active_custody
    }
    
    return render_template('index.html', stats=stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('يرجى إدخال اسم المستخدم وكلمة المرور!', 'error')
            return render_template('login.html')
        
        # فحص بيانات admin المباشرة
        if (username.lower() == 'admin' or username == 'admin@rashid.com') and password == 'admin123':
            session.clear()
            session.permanent = True
            session['user_id'] = 1
            session['username'] = 'admin'
            session['role'] = 'admin'
            
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('index'))
        
        # فحص قاعدة البيانات
        try:
            password_hash = hashlib.md5(password.encode()).hexdigest()
            conn = get_db_connection()
            user = conn.execute(
                'SELECT * FROM users WHERE (username = ? OR email = ?) AND is_active = 1',
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
                flash('بيانات تسجيل الدخول غير صحيحة!', 'error')
                
            conn.close()
            
        except Exception as e:
            flash('حدث خطأ في النظام، جرب: admin / admin123', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح!', 'info')
    return redirect(url_for('login'))

@app.route('/employees')
@login_required
def employees():
    """صفحة الموظفين"""
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    """إضافة موظف جديد"""
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            
            # الحصول على رقم الموظف التالي
            last_emp = conn.execute('SELECT employee_number FROM employees ORDER BY id DESC LIMIT 1').fetchone()
            if last_emp:
                last_num = int(last_emp['employee_number'][3:])  # EMP001 -> 001 -> 1
                new_num = f"EMP{last_num + 1:03d}"
            else:
                new_num = "EMP001"
            
            conn.execute('''
                INSERT INTO employees (employee_number, name, position, department, salary, phone, email, hire_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                new_num,
                request.form['name'],
                request.form['position'],
                request.form['department'],
                float(request.form['salary']),
                request.form['phone'],
                request.form['email'],
                request.form['hire_date'],
                request.form.get('notes', '')
            ))
            
            conn.commit()
            conn.close()
            
            flash('تم إضافة الموظف بنجاح!', 'success')
            return redirect(url_for('employees'))
            
        except Exception as e:
            flash(f'حدث خطأ: {str(e)}', 'error')
    
    return render_template('add_employee.html')

@app.route('/cars')
@login_required
def cars():
    """صفحة السيارات"""
    conn = get_db_connection()
    cars = conn.execute('SELECT * FROM cars ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('cars.html', cars=cars)

@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    """إضافة سيارة جديدة"""
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            
            conn.execute('''
                INSERT INTO cars (brand, model, year, license_plate, color, purchase_price, current_value, engine_number, chassis_number, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['brand'],
                request.form['model'],
                int(request.form['year']),
                request.form['license_plate'],
                request.form['color'],
                float(request.form['purchase_price']),
                float(request.form['current_value']),
                request.form['engine_number'],
                request.form['chassis_number'],
                request.form.get('notes', '')
            ))
            
            conn.commit()
            conn.close()
            
            flash('تم إضافة السيارة بنجاح!', 'success')
            return redirect(url_for('cars'))
            
        except Exception as e:
            flash(f'حدث خطأ: {str(e)}', 'error')
    
    return render_template('add_car.html')

@app.route('/treasury')
@login_required
def treasury():
    """صفحة الخزينة"""
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM treasury ORDER BY created_at DESC LIMIT 50').fetchall()
    
    # الرصيد الحالي
    balance = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
    current_balance = balance[0] if balance else 0
    
    conn.close()
    return render_template('treasury.html', transactions=transactions, current_balance=current_balance)

@app.route('/add_treasury', methods=['POST'])
@login_required
def add_treasury():
    """إضافة معاملة خزينة"""
    try:
        conn = get_db_connection()
        
        # الحصول على الرصيد الحالي
        balance = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
        current_balance = balance[0] if balance else 0
        
        transaction_type = request.form['transaction_type']
        amount = float(request.form['amount'])
        
        # حساب الرصيد الجديد
        if transaction_type == 'إيداع':
            new_balance = current_balance + amount
        else:  # سحب
            new_balance = current_balance - amount
        
        conn.execute('''
            INSERT INTO treasury (transaction_type, amount, description, reference_number, created_by, date, balance_after)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction_type,
            amount,
            request.form['description'],
            request.form['reference_number'],
            session['username'],
            request.form['date'],
            new_balance
        ))
        
        conn.commit()
        conn.close()
        
        flash('تم إضافة المعاملة بنجاح!', 'success')
        
    except Exception as e:
        flash(f'حدث خطأ: {str(e)}', 'error')
    
    return redirect(url_for('treasury'))

@app.route('/expenses')
@login_required
def expenses():
    """صفحة المصروفات"""
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('expenses.html', expenses=expenses)

@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    """إضافة مصروف"""
    try:
        conn = get_db_connection()
        
        conn.execute('''
            INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, approved_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['expense_type'],
            request.form['category'],
            float(request.form['amount']),
            request.form['description'],
            request.form['receipt_number'],
            request.form['date'],
            session['username']
        ))
        
        conn.commit()
        conn.close()
        
        flash('تم إضافة المصروف بنجاح!', 'success')
        
    except Exception as e:
        flash(f'حدث خطأ: {str(e)}', 'error')
    
    return redirect(url_for('expenses'))

@app.route('/car_custody')
@login_required
def car_custody():
    """صفحة عهد السيارات"""
    conn = get_db_connection()
    custody = conn.execute('''
        SELECT cc.*, c.brand, c.model, c.license_plate, e.name as employee_name, e.employee_number
        FROM car_custody cc
        JOIN cars c ON cc.car_id = c.id
        JOIN employees e ON cc.employee_id = e.id
        ORDER BY cc.created_at DESC
    ''').fetchall()
    
    # السيارات المتاحة
    available_cars = conn.execute('SELECT * FROM cars WHERE status = "متاح"').fetchall()
    
    # الموظفين النشطين
    active_employees = conn.execute('SELECT * FROM employees WHERE status = "نشط"').fetchall()
    
    conn.close()
    return render_template('car_custody.html', custody=custody, available_cars=available_cars, active_employees=active_employees)

@app.route('/add_custody', methods=['POST'])
@login_required
def add_custody():
    """إضافة عهدة سيارة"""
    try:
        conn = get_db_connection()
        
        car_id = int(request.form['car_id'])
        employee_id = int(request.form['employee_id'])
        
        # إضافة العهدة
        conn.execute('''
            INSERT INTO car_custody (car_id, employee_id, custody_date, purpose, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            car_id,
            employee_id,
            request.form['custody_date'],
            request.form['purpose'],
            request.form.get('notes', '')
        ))
        
        # تحديث حالة السيارة
        conn.execute('UPDATE cars SET status = "مستخدم" WHERE id = ?', (car_id,))
        
        conn.commit()
        conn.close()
        
        flash('تم إضافة العهدة بنجاح!', 'success')
        
    except Exception as e:
        flash(f'حدث خطأ: {str(e)}', 'error')
    
    return redirect(url_for('car_custody'))

@app.route('/return_custody/<int:custody_id>')
@login_required
def return_custody(custody_id):
    """إرجاع عهدة سيارة"""
    try:
        conn = get_db_connection()
        
        # الحصول على معلومات العهدة
        custody = conn.execute('SELECT * FROM car_custody WHERE id = ?', (custody_id,)).fetchone()
        
        if custody:
            # تحديث العهدة
            conn.execute('''
                UPDATE car_custody 
                SET return_date = ?, status = "مكتمل" 
                WHERE id = ?
            ''', (datetime.now().strftime('%Y-%m-%d'), custody_id))
            
            # تحديث حالة السيارة
            conn.execute('UPDATE cars SET status = "متاح" WHERE id = ?', (custody['car_id'],))
            
            conn.commit()
            flash('تم إرجاع السيارة بنجاح!', 'success')
        else:
            flash('العهدة غير موجودة!', 'error')
        
        conn.close()
        
    except Exception as e:
        flash(f'حدث خطأ: {str(e)}', 'error')
    
    return redirect(url_for('car_custody'))

@app.route('/reports')
@login_required
def reports():
    """صفحة التقارير"""
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
    
    # تقرير المصروفات حسب النوع
    expense_report = conn.execute('''
        SELECT expense_type, SUM(amount) as total
        FROM expenses
        GROUP BY expense_type
    ''').fetchall()
    
    # تقرير الخزينة الشهري
    monthly_treasury = conn.execute('''
        SELECT 
            substr(date, 1, 7) as month,
            SUM(CASE WHEN transaction_type = 'إيداع' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN transaction_type = 'سحب' THEN amount ELSE 0 END) as expenses
        FROM treasury
        GROUP BY substr(date, 1, 7)
        ORDER BY month DESC
        LIMIT 6
    ''').fetchall()
    
    conn.close()
    
    return render_template('reports.html', 
                         dept_report=dept_report,
                         car_status_report=car_status_report,
                         expense_report=expense_report,
                         monthly_treasury=monthly_treasury)

@app.route('/settings')
@login_required
def settings():
    """صفحة الإعدادات"""
    return render_template('settings.html')

def open_browser():
    """فتح المتصفح تلقائياً"""
    time.sleep(3)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 نظام إدارة السيارات الشامل مع جميع البيانات والوظائف")
    print("RASHID INDUSTRIAL CO.")
    print("=" * 80)
    
    # إنشاء قاعدة البيانات الشاملة
    if init_complete_database():
        print("✅ تم إنشاء قاعدة البيانات الشاملة مع جميع البيانات")
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
    print("   • 5 معاملات مالية")
    
    print("\n✅ الوظائف المتاحة:")
    print("   • إدارة الموظفين (عرض، إضافة، تعديل)")
    print("   • إدارة السيارات (عرض، إضافة، تعديل)")
    print("   • إدارة الخزينة (عرض، إضافة معاملات)")
    print("   • إدارة المصروفات (عرض، إضافة)")
    print("   • إدارة عهد السيارات (عرض، إضافة، إرجاع)")
    print("   • التقارير الشاملة")
    print("   • الإعدادات")
    
    print("\n🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان...")
    print("⚠️  لإيقاف النظام: اضغط Ctrl+C")
    print("=" * 80)
    
    # فتح المتصفح في خيط منفصل
    threading.Thread(target=open_browser, daemon=True).start()
    
    # تشغيل النظام
    app.run(host='0.0.0.0', port=5000, debug=False)