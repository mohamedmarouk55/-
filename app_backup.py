#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام الإدارة الشامل المتعدد الشاشات
RASHID INDUSTRIAL CO.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
from datetime import datetime, timedelta
import os
import hashlib
import webbrowser
import threading
import time
from functools import wraps
import werkzeug.routing.exceptions
from error_handler import setup_error_handlers, safe_route_handler

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'rashid-industrial-co-2024-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# إعداد معالجات الأخطاء
try:
    setup_error_handlers(app)
except ImportError:
    print("⚠️ لم يتم العثور على معالج الأخطاء، سيتم استخدام المعالجة الافتراضية")

# إعداد قاعدة البيانات
DATABASE = 'management_system.db'

def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """إنشاء قاعدة البيانات والجداول"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # جدول الموظفين
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
    
    # جدول السيارات
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
    
    # جدول الخزينة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treasury (
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
        CREATE TABLE IF NOT EXISTS expenses (
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
        CREATE TABLE IF NOT EXISTS car_custody (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            employee_number TEXT NOT NULL,
            car_id INTEGER NOT NULL,
            custody_date TEXT NOT NULL,
            expected_return TEXT,
            return_date TEXT,
            notes TEXT,
            return_notes TEXT,
            status TEXT DEFAULT 'نشط' CHECK (status IN ('نشط', 'مُسلم')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees (id),
            FOREIGN KEY (car_id) REFERENCES cars (id)
        )
    ''')
    
    # جدول البيانات المالية
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK (type IN ('إيراد', 'مصروف')),
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول المستخدمين
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
    
    # جدول الإعدادات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إضافة مستخدم افتراضي
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@rashid.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin'))
    
    # إضافة إعدادات افتراضية
    default_settings = [
        ('company_name', 'RASHID INDUSTRIAL CO.', 'اسم الشركة'),
        ('company_address', 'الرياض، المملكة العربية السعودية', 'عنوان الشركة'),
        ('currency', 'SAR', 'العملة المستخدمة'),
        ('tax_rate', '15', 'معدل الضريبة المضافة'),
    ]
    
    for key, value, description in default_settings:
        cursor.execute('''
            INSERT OR IGNORE INTO settings (key, value, description)
            VALUES (?, ?, ?)
        ''', (key, value, description))
    
    conn.commit()
    conn.close()

# تزيين للتحقق من تسجيل الدخول
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# الصفحة الرئيسية
@app.route('/')
def index():
    # إذا لم يكن المستخدم مسجل دخول، توجيهه لصفحة تسجيل الدخول
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # إذا كان مسجل دخول، عرض الصفحة الرئيسية
    conn = get_db_connection()
    
    # إحصائيات الموظفين
    employees_count = conn.execute('SELECT COUNT(*) FROM employees WHERE status = "نشط"').fetchone()[0]
    
    # إحصائيات السيارات
    cars_count = conn.execute('SELECT COUNT(*) FROM cars').fetchone()[0]
    available_cars = conn.execute('SELECT COUNT(*) FROM cars WHERE status = "متاح"').fetchone()[0]
    
    # إحصائيات مالية
    total_income = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"').fetchone()[0]
    total_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "سحب"').fetchone()[0]
    net_profit = total_income - total_expenses
    
    # رصيد الخزينة
    treasury_balance = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
    current_balance = treasury_balance[0] if treasury_balance else 0
    
    conn.close()
    
    stats = {
        'employees_count': employees_count,
        'cars_count': cars_count,
        'available_cars': available_cars,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'current_balance': current_balance
    }
    
    return render_template('index.html', stats=stats)

# تسجيل الدخول - نسخة مبسطة ومضمونة
@app.route('/login', methods=['GET', 'POST'])
def login():
    # إذا كان المستخدم مسجل دخول بالفعل، توجيهه للصفحة الرئيسية
    if 'user_id' in session:
        print("المستخدم مسجل دخول بالفعل، إعادة توجيه للصفحة الرئيسية")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        print(f"🔍 محاولة تسجيل دخول:")
        print(f"   اسم المستخدم: '{username}'")
        print(f"   كلمة المرور: '{password}'")
        
        # فحص بسيط للبيانات المدخلة
        if not username or not password:
            print("❌ بيانات ناقصة")
            flash('يرجى إدخال اسم المستخدم وكلمة المرور!', 'error')
            return render_template('login.html')
        
        # فحص بيانات admin المباشرة (بدون قاعدة بيانات أولاً)
        if (username == 'admin' or username == 'admin@rashid.com') and password == 'admin123':
            print("✅ تسجيل دخول مباشر ناجح لـ admin")
            
            # تسجيل الجلسة
            session.permanent = True
            session['user_id'] = 1
            session['username'] = 'admin'
            session['role'] = 'admin'
            
            print("✅ تم تسجيل الجلسة بنجاح")
            flash('تم تسجيل الدخول بنجاح!', 'success')
            
            print("🔄 إعادة توجيه للصفحة الرئيسية")
            return redirect(url_for('index'))
        
        # إذا لم تنجح البيانات المباشرة، جرب قاعدة البيانات
        try:
            password_hash = hashlib.md5(password.encode()).hexdigest()
            print(f"🔐 كلمة المرور المشفرة: {password_hash}")
            
            conn = get_db_connection()
            user = conn.execute(
                'SELECT * FROM users WHERE (username = ? OR email = ?) AND is_active = 1',
                (username, username)
            ).fetchone()
            
            if user:
                print(f"👤 تم العثور على المستخدم في قاعدة البيانات: {user['username']}")
                
                if user['password_hash'] == password_hash:
                    print("✅ كلمة المرور صحيحة من قاعدة البيانات")
                    
                    session.permanent = True
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    
                    flash('تم تسجيل الدخول بنجاح!', 'success')
                    conn.close()
                    return redirect(url_for('index'))
                else:
                    print("❌ كلمة المرور غير صحيحة في قاعدة البيانات")
                    flash('كلمة المرور غير صحيحة!', 'error')
            else:
                print("❌ لم يتم العثور على المستخدم في قاعدة البيانات")
                flash('اسم المستخدم غير موجود!', 'error')
                
            conn.close()
            
        except Exception as e:
            print(f"❌ خطأ في قاعدة البيانات: {e}")
            flash('حدث خطأ في النظام، جرب البيانات: admin / admin123', 'error')
            return render_template('login.html')
    
    print("📄 عرض صفحة تسجيل الدخول")
    return render_template('login.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح!', 'info')
    return redirect(url_for('login'))

# صفحة الخزينة
@app.route('/treasury', methods=['GET', 'POST'])
@login_required
def treasury():
    try:
        conn = get_db_connection()
        
        if request.method == 'POST':
            try:
                transaction_type = request.form['transaction_type']
                amount = float(request.form['amount'])
                description = request.form['description']
                reference_number = request.form.get('reference_number', '')
                date = request.form['date']
                created_by = session.get('username', 'admin')
                
                # حساب الرصيد الجديد
                current_balance_row = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
                current_balance = current_balance_row[0] if current_balance_row else 0
                
                if transaction_type == 'إيداع':
                    new_balance = current_balance + amount
                else:  # سحب
                    new_balance = current_balance - amount
                
                # إضافة المعاملة
                conn.execute('''
                    INSERT INTO treasury (transaction_type, amount, description, reference_number, created_by, date, balance_after)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (transaction_type, amount, description, reference_number, created_by, date, new_balance))
                
                conn.commit()
                flash(f'تم إضافة {transaction_type} بمبلغ {amount:,.0f} ريال بنجاح!', 'success')
                return redirect(url_for('treasury'))
                
            except ValueError as e:
                print(f"خطأ في قيمة المبلغ: {e}")
                flash('يرجى إدخال مبلغ صحيح', 'error')
            except Exception as e:
                print(f"خطأ في معالجة معاملة الخزينة: {e}")
                flash('حدث خطأ في تسجيل المعاملة', 'error')
        
        # جلب جميع المعاملات
        transactions = conn.execute('SELECT * FROM treasury ORDER BY created_at DESC').fetchall()
        
        # إحصائيات
        total_deposits = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"').fetchone()[0]
        total_withdrawals = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "سحب"').fetchone()[0]
        current_balance_row = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
        current_balance = current_balance_row[0] if current_balance_row else 0
        
        conn.close()
        
        return render_template('treasury.html', 
                             transactions=transactions,
                             total_deposits=total_deposits,
                             total_withdrawals=total_withdrawals,
                             current_balance=current_balance)
                             
    except Exception as e:
        print(f"خطأ في صفحة الخزينة: {e}")
        import traceback
        traceback.print_exc()
        flash('حدث خطأ في تحميل صفحة الخزينة', 'error')
        return redirect(url_for('index'))

# إدخال السيارات
@app.route('/car_entry', methods=['GET', 'POST'])
@login_required
def car_entry():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        license_plate = request.form['license_plate']
        color = request.form.get('color', '')
        purchase_price = request.form.get('purchase_price', 0) or 0
        current_value = request.form.get('current_value', 0) or 0
        engine_number = request.form.get('engine_number', '')
        chassis_number = request.form.get('chassis_number', '')
        notes = request.form.get('notes', '')
        
        conn = get_db_connection()
        
        try:
            conn.execute('''
                INSERT INTO cars (brand, model, year, license_plate, color, purchase_price, current_value, engine_number, chassis_number, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (brand, model, year, license_plate, color, purchase_price, current_value, engine_number, chassis_number, notes))
            
            conn.commit()
            flash('تم إضافة السيارة بنجاح!', 'success')
            return redirect(url_for('car_entry'))
        except sqlite3.IntegrityError:
            flash('رقم اللوحة موجود مسبقاً!', 'error')
        finally:
            conn.close()
    
    return render_template('car_entry.html')

# بيانات التسليم
@app.route('/car_delivery', methods=['GET', 'POST'])
@login_required
def car_delivery():
    if request.method == 'POST':
        employee_number = request.form['employee_number']
        return_date = request.form['return_date']
        notes = request.form.get('notes', '')
        
        conn = get_db_connection()
        
        # البحث عن العهدة النشطة للموظف
        custody = conn.execute('''
            SELECT cc.id, cc.car_id, e.name, c.brand, c.model, c.license_plate
            FROM car_custody cc
            JOIN employees e ON cc.employee_id = e.id
            JOIN cars c ON cc.car_id = c.id
            WHERE cc.employee_number = ? AND cc.status = 'نشط'
        ''', (employee_number,)).fetchone()
        
        if custody:
            # تحديث العهدة
            conn.execute('''
                UPDATE car_custody 
                SET return_date = ?, status = 'مُسلم', return_notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (return_date, notes, custody['id']))
            
            # تحديث حالة السيارة
            conn.execute('UPDATE cars SET status = "متاح" WHERE id = ?', (custody['car_id'],))
            
            conn.commit()
            flash(f'تم تسليم السيارة من الموظف {custody["name"]} بنجاح!', 'success')
        else:
            flash('لا توجد عهدة نشطة لهذا الموظف!', 'error')
        
        conn.close()
        return redirect(url_for('car_delivery'))
    
    return render_template('car_delivery.html')

# بيانات الاستلام
@app.route('/car_receipt', methods=['GET', 'POST'])
@login_required
def car_receipt():
    conn = get_db_connection()
    
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        car_id = request.form['car_id']
        custody_date = request.form['custody_date']
        expected_return = request.form.get('expected_return')
        notes = request.form.get('notes', '')
        
        # البحث عن الموظف
        employee = conn.execute('SELECT id, employee_number, name FROM employees WHERE id = ?', (employee_id,)).fetchone()
        
        if employee:
            try:
                # إضافة العهدة الجديدة
                conn.execute('''
                    INSERT INTO car_custody (employee_id, employee_number, car_id, custody_date, expected_return, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (employee['id'], employee['employee_number'], car_id, custody_date, expected_return, notes))
                
                # تحديث حالة السيارة
                conn.execute('UPDATE cars SET status = "مستأجر" WHERE id = ?', (car_id,))
                
                conn.commit()
                flash(f'تم تسجيل استلام السيارة للموظف {employee["name"]} بنجاح!', 'success')
                return redirect(url_for('car_receipt'))
            except sqlite3.Error as e:
                flash(f'حدث خطأ: {str(e)}', 'error')
        else:
            flash('الموظف غير موجود!', 'error')
    
    # جلب الموظفين والسيارات المتاحة
    employees = conn.execute('SELECT id, employee_number, name FROM employees WHERE status = "نشط"').fetchall()
    available_cars = conn.execute('SELECT id, brand, model, license_plate FROM cars WHERE status = "متاح"').fetchall()
    
    conn.close()
    
    return render_template('car_receipt.html', employees=employees, available_cars=available_cars)

# إدارة السيارات
@app.route('/cars')
@login_required
def cars():
    conn = get_db_connection()
    cars_data = conn.execute('SELECT * FROM cars ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('cars.html', cars=cars_data)

# إدارة الموظفين
@app.route('/employees')
@login_required
def employees():
    conn = get_db_connection()
    employees_data = conn.execute('SELECT * FROM employees ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('employees.html', employees=employees_data)

# إضافة موظف جديد
@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        employee_number = request.form['employee_number']
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        salary = float(request.form['salary'])
        phone = request.form['phone']
        email = request.form['email']
        hire_date = request.form['hire_date']
        notes = request.form.get('notes', '')
        
        conn = get_db_connection()
        
        try:
            conn.execute('''
                INSERT INTO employees (employee_number, name, position, department, salary, phone, email, hire_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (employee_number, name, position, department, salary, phone, email, hire_date, notes))
            
            conn.commit()
            flash('تم إضافة الموظف بنجاح!', 'success')
            return redirect(url_for('employees'))
        except sqlite3.IntegrityError:
            flash('الرقم الوظيفي موجود مسبقاً!', 'error')
        finally:
            conn.close()
    
    return render_template('add_employee.html')

# إدارة المصروفات
@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    conn = get_db_connection()
    
    if request.method == 'POST':
        expense_type = request.form['expense_type']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form.get('description', '')
        receipt_number = request.form.get('receipt_number', '')
        date = request.form['date']
        approved_by = session.get('username', 'admin')
        
        conn.execute('''
            INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, approved_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (expense_type, category, amount, description, receipt_number, date, approved_by))
        
        conn.commit()
        flash('تم إضافة المصروف بنجاح!', 'success')
        return redirect(url_for('expenses'))
    
    # جلب جميع المصروفات
    expenses_data = conn.execute('SELECT * FROM expenses ORDER BY date DESC, created_at DESC').fetchall()
    
    # إحصائيات المصروفات
    total_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses').fetchone()[0]
    category_stats = dict(conn.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category').fetchall())
    
    conn.close()
    
    return render_template('expenses.html', 
                         expenses=expenses_data,
                         total_expenses=total_expenses,
                         category_stats=category_stats)

# صفحة التقارير
@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

# صفحة الإعدادات
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    conn = get_db_connection()
    
    if request.method == 'POST':
        # حفظ الإعدادات
        for key, value in request.form.items():
            conn.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))
        
        conn.commit()
        flash('تم حفظ الإعدادات بنجاح!', 'success')
        return redirect(url_for('settings'))
    
    # جلب الإعدادات الحالية
    settings_data = dict(conn.execute('SELECT key, value FROM settings').fetchall())
    conn.close()
    
    return render_template('settings.html', settings=settings_data)

# API للبحث عن الموظف بالرقم الوظيفي
@app.route('/api/employee/<employee_number>')
@login_required
def get_employee_by_number(employee_number):
    conn = get_db_connection()
    
    # البحث عن الموظف والسيارة المسندة إليه
    result = conn.execute('''
        SELECT e.id, e.name, e.position, e.department,
               c.id as car_id, c.brand, c.model, c.license_plate,
               cc.custody_date
        FROM employees e
        LEFT JOIN car_custody cc ON e.id = cc.employee_id AND cc.status = 'نشط'
        LEFT JOIN cars c ON cc.car_id = c.id
        WHERE e.employee_number = ?
    ''', (employee_number,)).fetchone()
    
    conn.close()
    
    if result:
        return jsonify({
            'found': True,
            'employee': {
                'id': result['id'],
                'name': result['name'],
                'position': result['position'],
                'department': result['department']
            },
            'car': {
                'id': result['car_id'],
                'brand': result['brand'],
                'model': result['model'],
                'license_plate': result['license_plate'],
                'custody_date': result['custody_date']
            } if result['car_id'] else None
        })
    else:
        return jsonify({'found': False})

# API لإحصائيات العهد
@app.route('/api/custody_stats')
@login_required
def custody_stats():
    conn = get_db_connection()
    
    active = conn.execute('SELECT COUNT(*) FROM car_custody WHERE status = "نشط"').fetchone()[0]
    returned = conn.execute('SELECT COUNT(*) FROM car_custody WHERE status = "مُسلم"').fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'active': active,
        'returned': returned
    })

# حذف مصروف
@app.route('/delete_expense/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    
    flash('تم حذف المصروف بنجاح!', 'success')
    return redirect(url_for('expenses'))

# حذف موظف
@app.route('/delete_employee/<int:employee_id>')
@login_required
def delete_employee(employee_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
    conn.commit()
    conn.close()
    flash('تم حذف الموظف بنجاح!', 'success')
    return redirect(url_for('employees'))

# حذف سيارة
@app.route('/delete_car/<int:car_id>')
@login_required
def delete_car(car_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cars WHERE id = ?', (car_id,))
    conn.commit()
    conn.close()
    flash('تم حذف السيارة بنجاح!', 'success')
    return redirect(url_for('cars'))

# عهدة السيارات
@app.route('/car_custody')
@login_required
def car_custody():
    try:
        conn = get_db_connection()
        
        # جلب بيانات العهدة
        custody_records = conn.execute('''
            SELECT cc.*, e.name as employee_name, c.brand, c.model, c.license_plate
            FROM car_custody cc
            LEFT JOIN employees e ON cc.employee_id = e.id
            LEFT JOIN cars c ON cc.car_id = c.id
            ORDER BY cc.created_at DESC
        ''').fetchall()
        
        conn.close()
        
        return render_template('car_custody.html', custody_records=custody_records)
        
    except Exception as e:
        print(f'خطأ في صفحة عهدة السيارات: {e}')
        flash('حدث خطأ في تحميل صفحة عهدة السيارات', 'error')
        return redirect(url_for('index'))

# التقارير المالية
@app.route('/financial_reports')
@login_required
def financial_reports():
    try:
        conn = get_db_connection()
        
        # إحصائيات مالية
        total_income = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"').fetchone()[0]
        total_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses').fetchone()[0]
        net_profit = total_income - total_expenses
        
        conn.close()
        
        return render_template('financial_reports.html', 
                             total_income=total_income,
                             total_expenses=total_expenses,
                             net_profit=net_profit)
        
    except Exception as e:
        print(f'خطأ في صفحة التقارير المالية: {e}')
        flash('حدث خطأ في تحميل التقارير المالية', 'error')
        return redirect(url_for('index'))

# لوحة التحكم
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        return redirect(url_for('index'))
    except Exception as e:
        print(f'خطأ في لوحة التحكم: {e}')
        return redirect(url_for('index'))

# معالج أخطاء BuildError
@app.errorhandler(werkzeug.routing.exceptions.BuildError)
def handle_build_error(error):
    print(f"❌ خطأ في بناء الرابط: {error}")
    flash('الصفحة المطلوبة غير متوفرة حالياً', 'error')
    return redirect(url_for('index'))

# معالج الأخطاء العام
@app.errorhandler(500)
def internal_error(error):
    print(f"❌ خطأ داخلي في الخادم: {error}")
    import traceback
    traceback.print_exc()
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>خطأ في النظام</title>
        <style>
            body { font-family: Arial; padding: 50px; background: #f8f9fa; text-align: center; }
            .error-container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .error-icon { font-size: 4rem; color: #dc3545; margin-bottom: 20px; }
            h1 { color: #dc3545; margin-bottom: 20px; }
            .error-details { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: right; }
            .btn { display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-icon">⚠️</div>
            <h1>خطأ في النظام</h1>
            <p>حدث خطأ داخلي في الخادم. يرجى المحاولة مرة أخرى.</p>
            
            <div class="error-details">
                <strong>الحلول المقترحة:</strong><br>
                • تأكد من أن Python و Flask مثبتان بشكل صحيح<br>
                • تأكد من وجود ملفات النظام في المجلد الصحيح<br>
                • جرب إعادة تشغيل النظام<br>
                • شغل ملف: تشغيل_مع_تشخيص_الأخطاء.bat
            </div>
            
            <a href="/login" class="btn">العودة لتسجيل الدخول</a>
            <a href="/" class="btn">الصفحة الرئيسية</a>
        </div>
    </body>
    </html>
    ''', 500

@app.errorhandler(404)
def not_found(error):
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>الصفحة غير موجودة</title>
        <style>
            body { font-family: Arial; padding: 50px; background: #f8f9fa; text-align: center; }
            .error-container { max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
            .error-icon { font-size: 4rem; color: #ffc107; margin-bottom: 20px; }
            .btn { display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-icon">🔍</div>
            <h1>الصفحة غير موجودة</h1>
            <p>الصفحة التي تبحث عنها غير موجودة.</p>
            <a href="/login" class="btn">تسجيل الدخول</a>
            <a href="/" class="btn">الصفحة الرئيسية</a>
        </div>
    </body>
    </html>
    ''', 404

def open_browser():
    """فتح المتصفح تلقائياً بعد تشغيل الخادم"""
    time.sleep(3)  # انتظار 3 ثوان لضمان تشغيل الخادم
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 تم فتح المتصفح تلقائياً!")
    except Exception as e:
        print(f"⚠️  لم يتم فتح المتصفح تلقائياً: {e}")
        print("🌐 يرجى فتح المتصفح يدوياً والذهاب إلى: http://localhost:5000")

if __name__ == '__main__':
    try:
        print("🚀 بدء تشغيل نظام الإدارة الشامل...")
        print("🔧 تهيئة قاعدة البيانات...")
        
        # إنشاء قاعدة البيانات عند التشغيل
        init_database()
        print("✅ تم تهيئة قاعدة البيانات بنجاح")
        
        # تشغيل التطبيق
        print("🌐 الرابط: http://localhost:5000")
        print("👤 اسم المستخدم: admin")
        print("🔑 كلمة المرور: admin123")
        print("⚠️  لإيقاف النظام اضغط Ctrl+C")
        print("🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان...")
        print("=" * 50)
        
        # فتح المتصفح في خيط منفصل
        threading.Thread(target=open_browser, daemon=True).start()
        
        # تشغيل التطبيق مع معالجة الأخطاء
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 50)
        print("💡 الحلول المقترحة:")
        print("• تأكد من أن Python و Flask مثبتان")
        print("• تأكد من عدم استخدام المنفذ 5000 من برنامج آخر")
        print("• جرب تشغيل: تشغيل_مع_تشخيص_الأخطاء.bat")
        print("• أعد تشغيل الكمبيوتر وجرب مرة أخرى")
        input("\nاضغط Enter للخروج...")