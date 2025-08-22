#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام الإدارة الشامل المتعدد الشاشات
AL RASHID INDUSTRIAL CO.
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
            car_id INTEGER,
            employee_id INTEGER,
            approved_by TEXT,
            status TEXT DEFAULT 'معتمد',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (car_id) REFERENCES cars (id),
            FOREIGN KEY (employee_id) REFERENCES employees (id)
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
    
    # جدول بيانات المطور
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS developer_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_ar TEXT NOT NULL,
            name_en TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إضافة مستخدم افتراضي
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@rashid.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin'))
    
    # إضافة بيانات المطور
    cursor.execute('''
        INSERT OR IGNORE INTO developer_info (name_ar, name_en, email, mobile)
        VALUES (?, ?, ?, ?)
    ''', ('محمد مبروك عطية', 'Mohamed Marouk Atia', 'mohamedmarouk55@gmail.com', '0570453337'))
    
    # إضافة إعدادات افتراضية
    default_settings = [
        ('company_name', 'AL RASHID INDUSTRIAL CO.', 'اسم الشركة'),
        ('company_address', 'الرياض، المملكة العربية السعودية', 'عنوان الشركة'),
        ('currency', 'SAR', 'العملة المستخدمة'),
        ('tax_rate', '15', 'معدل الضريبة المضافة'),
        ('developer_name_ar', 'محمد مبروك عطية', 'اسم المطور بالعربية'),
        ('developer_name_en', 'Mohamed Marouk Atia', 'اسم المطور بالإنجليزية'),
        ('developer_email', 'mohamedmarouk55@gmail.com', 'بريد المطور الإلكتروني'),
        ('developer_mobile', '0570453337', 'رقم جوال المطور'),
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
    
    # إحصائيات مالية - مع معالجة حالة عدم وجود عمود type
    try:
        # محاولة استخدام عمود type إذا كان موجوداً
        total_income = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "إيداع"').fetchone()[0]
        total_expenses_treasury = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "سحب"').fetchone()[0]
    except sqlite3.OperationalError:
        # إذا لم يكن عمود type موجوداً، استخدم طريقة بديلة
        print("⚠️ عمود type غير موجود في جدول treasury، استخدام طريقة بديلة...")
        # افتراض أن المبالغ الموجبة إيداعات والسالبة سحوبات
        total_income = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE amount > 0').fetchone()[0]
        total_expenses_treasury = conn.execute('SELECT COALESCE(SUM(ABS(amount)), 0) FROM treasury WHERE amount < 0').fetchone()[0]
    
    total_expenses_table = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses').fetchone()[0]
    total_expenses = total_expenses_treasury + total_expenses_table
    net_profit = total_income - total_expenses
    
    # رصيد الخزينة - مع معالجة حالة عدم وجود عمود balance
    try:
        treasury_balance = conn.execute('SELECT COALESCE(balance, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
        current_balance = treasury_balance[0] if treasury_balance else 0
    except sqlite3.OperationalError:
        # إذا لم يكن عمود balance موجوداً، احسب الرصيد من المجموع
        print("⚠️ عمود balance غير موجود، حساب الرصيد من المجموع...")
        try:
            # حساب الرصيد من الإيداعات والسحوبات
            income = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "إيداع"').fetchone()[0]
            expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "سحب"').fetchone()[0]
            current_balance = income - expenses
        except sqlite3.OperationalError:
            # إذا لم يكن عمود type موجوداً أيضاً
            income = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE amount > 0').fetchone()[0]
            expenses = conn.execute('SELECT COALESCE(SUM(ABS(amount)), 0) FROM treasury WHERE amount < 0').fetchone()[0]
            current_balance = income - expenses
    
    # إحصائيات إضافية
    used_cars = conn.execute('SELECT COUNT(*) FROM cars WHERE status = "مستخدم"').fetchone()[0]
    maintenance_cars = conn.execute('SELECT COUNT(*) FROM cars WHERE status = "صيانة"').fetchone()[0]
    active_custody = conn.execute('SELECT COUNT(*) FROM car_custody WHERE status = "نشط"').fetchone()[0]
    
    # مصروفات الشهر الحالي
    current_month = datetime.now().strftime('%Y-%m')
    monthly_expenses = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE strftime("%Y-%m", created_at) = ?', 
        (current_month,)
    ).fetchone()[0]
    
    conn.close()
    
    # التأكد من أن جميع القيم رقمية وليست None
    stats = {
        'employees_count': employees_count or 0,
        'cars_count': cars_count or 0,
        'available_cars': available_cars or 0,
        'used_cars': used_cars or 0,
        'maintenance_cars': maintenance_cars or 0,
        'active_custody': active_custody or 0,
        'total_income': total_income or 0,
        'total_expenses': total_expenses or 0,
        'net_profit': (total_income or 0) - (total_expenses or 0),
        'current_balance': current_balance or 0,
        'monthly_expenses': monthly_expenses or 0
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
                transaction_type = request.form.get('transaction_type', '')
                amount_str = request.form.get('amount', '0')
                description = request.form.get('description', '')
                reference_number = request.form.get('reference_number', '')
                date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
                created_by = session.get('username', 'admin')
                
                # التحقق من صحة البيانات
                if not transaction_type or transaction_type not in ['إيداع', 'سحب']:
                    flash('يرجى اختيار نوع المعاملة', 'error')
                    return redirect(url_for('treasury'))
                
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        flash('يرجى إدخال مبلغ صحيح أكبر من صفر', 'error')
                        return redirect(url_for('treasury'))
                except (ValueError, TypeError):
                    flash('يرجى إدخال مبلغ صحيح', 'error')
                    return redirect(url_for('treasury'))
                
                # حساب الرصيد الجديد
                current_balance_row = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
                current_balance = float(current_balance_row[0]) if current_balance_row else 0.0
                
                if transaction_type == 'إيداع':
                    new_balance = current_balance + amount
                else:  # سحب
                    new_balance = current_balance - amount
                    if new_balance < 0:
                        flash('لا يمكن السحب - الرصيد غير كافي', 'error')
                        return redirect(url_for('treasury'))
                
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
        
        # الحصول على فلاتر التاريخ
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
        # بناء الاستعلام مع الفلاتر
        query = 'SELECT * FROM treasury'
        params = []
        
        if start_date and end_date:
            query += ' WHERE date BETWEEN ? AND ?'
            params = [start_date, end_date]
        elif start_date:
            query += ' WHERE date >= ?'
            params = [start_date]
        elif end_date:
            query += ' WHERE date <= ?'
            params = [end_date]
        
        query += ' ORDER BY created_at DESC'
        
        # جلب المعاملات مع الفلاتر
        transactions = conn.execute(query, params).fetchall()
        
        # إحصائيات مع حماية من الأخطاء للفترة المحددة
        try:
            deposits_query = 'SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"'
            withdrawals_query = 'SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "سحب"'
            
            if params:
                if start_date and end_date:
                    deposits_query += ' AND date BETWEEN ? AND ?'
                    withdrawals_query += ' AND date BETWEEN ? AND ?'
                elif start_date:
                    deposits_query += ' AND date >= ?'
                    withdrawals_query += ' AND date >= ?'
                elif end_date:
                    deposits_query += ' AND date <= ?'
                    withdrawals_query += ' AND date <= ?'
            
            total_deposits = float(conn.execute(deposits_query, params).fetchone()[0] or 0)
            total_withdrawals = float(conn.execute(withdrawals_query, params).fetchone()[0] or 0)
            
            # الرصيد الحالي (دائماً من آخر معاملة بغض النظر عن الفلتر)
            current_balance_row = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
            current_balance = float(current_balance_row[0]) if current_balance_row else 0.0
        except Exception as e:
            print(f"خطأ في حساب الإحصائيات: {e}")
            total_deposits = 0.0
            total_withdrawals = 0.0
            current_balance = 0.0
        
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

# تعديل معاملة الخزينة
@app.route('/edit_treasury/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_treasury(transaction_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        try:
            transaction_type = request.form.get('transaction_type', '')
            amount_str = request.form.get('amount', '0')
            description = request.form.get('description', '')
            reference_number = request.form.get('reference_number', '')
            date = request.form.get('date', '')
            
            # التحقق من صحة البيانات
            if not transaction_type or transaction_type not in ['إيداع', 'سحب']:
                flash('يرجى اختيار نوع المعاملة', 'error')
                return redirect(url_for('edit_treasury', transaction_id=transaction_id))
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    flash('يرجى إدخال مبلغ صحيح أكبر من صفر', 'error')
                    return redirect(url_for('edit_treasury', transaction_id=transaction_id))
            except (ValueError, TypeError):
                flash('يرجى إدخال مبلغ صحيح', 'error')
                return redirect(url_for('edit_treasury', transaction_id=transaction_id))
            
            # تحديث المعاملة (بدون إعادة حساب الرصيد لتجنب التعقيد)
            conn.execute('''
                UPDATE treasury 
                SET transaction_type = ?, amount = ?, description = ?, 
                    reference_number = ?, date = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (transaction_type, amount, description, reference_number, date, transaction_id))
            
            conn.commit()
            flash('تم تحديث المعاملة بنجاح!', 'success')
            return redirect(url_for('treasury'))
            
        except Exception as e:
            print(f"خطأ في تحديث معاملة الخزينة: {e}")
            flash('حدث خطأ في تحديث المعاملة', 'error')
            conn.close()
            return redirect(url_for('edit_treasury', transaction_id=transaction_id))
    
    # جلب بيانات المعاملة للعرض
    try:
        transaction = conn.execute('SELECT * FROM treasury WHERE id = ?', (transaction_id,)).fetchone()
        conn.close()
        
        if transaction:
            return render_template('edit_treasury.html', transaction=transaction)
        else:
            flash('المعاملة غير موجودة!', 'error')
            return redirect(url_for('treasury'))
    except Exception as e:
        print(f"خطأ في جلب بيانات المعاملة: {e}")
        flash('حدث خطأ في جلب بيانات المعاملة', 'error')
        if 'conn' in locals():
            conn.close()
        return redirect(url_for('treasury'))

# حذف معاملة الخزينة
@app.route('/delete_treasury/<int:transaction_id>', methods=['POST'])
@login_required
def delete_treasury(transaction_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM treasury WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()
        
        flash('تم حذف المعاملة بنجاح!', 'success')
    except Exception as e:
        print(f"خطأ في حذف المعاملة: {e}")
        flash('حدث خطأ في حذف المعاملة', 'error')
    
    return redirect(url_for('treasury'))

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
        try:
            employee_id = request.form.get('employee_id', '').strip()
            car_id = request.form.get('car_id', '').strip()
            custody_date = request.form.get('custody_date', '').strip()
            expected_return = request.form.get('expected_return', '').strip()
            notes = request.form.get('notes', '').strip()
            
            print(f"Debug - employee_id: '{employee_id}', car_id: '{car_id}', custody_date: '{custody_date}'")
            
            # التحقق من وجود البيانات المطلوبة
            if not employee_id or not car_id or not custody_date:
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                conn.close()
                return redirect(url_for('car_receipt'))
            
            # البحث عن الموظف
            employee = conn.execute('SELECT id, employee_number, name FROM employees WHERE id = ?', (employee_id,)).fetchone()
            
            if employee:
                # إضافة العهدة الجديدة
                conn.execute('''
                    INSERT INTO car_custody (employee_id, employee_number, car_id, custody_date, expected_return, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (employee['id'], employee['employee_number'], car_id, custody_date, expected_return, notes))
                
                # تحديث حالة السيارة
                conn.execute('UPDATE cars SET status = "مستأجر" WHERE id = ?', (car_id,))
                
                conn.commit()
                flash(f'تم تسجيل استلام السيارة للموظف {employee["name"]} بنجاح!', 'success')
                conn.close()
                return redirect(url_for('car_receipt'))
            else:
                flash('الموظف غير موجود!', 'error')
                conn.close()
                return redirect(url_for('car_receipt'))
                
        except Exception as e:
            print(f"خطأ عام في car_receipt: {e}")
            flash('حدث خطأ في معالجة الطلب', 'error')
            conn.close()
            return redirect(url_for('car_receipt'))
    
    # جلب الموظفين والسيارات المتاحة
    employees = conn.execute('SELECT id, employee_number, name FROM employees WHERE status = "نشط"').fetchall()
    available_cars = conn.execute('SELECT id, brand, model, license_plate FROM cars WHERE status = "متاح"').fetchall()
    
    conn.close()
    
    return render_template('car_receipt.html', employees=employees, available_cars=available_cars)

# إدارة السيارات
@app.route('/cars')
@login_required
def cars():
    try:
        conn = get_db_connection()
        cars_data = conn.execute('SELECT * FROM cars ORDER BY created_at DESC').fetchall()
        
        # حساب الإحصائيات المالية
        total_purchase_price = 0.0
        total_current_value = 0.0
        
        if cars_data:
            try:
                for car in cars_data:
                    # العمود 7 هو purchase_price والعمود 8 هو current_value
                    purchase_price = float(car[7]) if car[7] else 0.0
                    current_value = float(car[8]) if car[8] else 0.0
                    total_purchase_price += purchase_price
                    total_current_value += current_value
                    
            except Exception as e:
                print(f"خطأ في حساب إحصائيات السيارات: {e}")
                total_purchase_price = 0.0
                total_current_value = 0.0
        
        conn.close()
        return render_template('cars.html', 
                             cars=cars_data,
                             total_purchase_price=total_purchase_price,
                             total_current_value=total_current_value)
    except Exception as e:
        print(f"خطأ في صفحة السيارات: {e}")
        return render_template('cars.html', 
                             cars=[],
                             total_purchase_price=0.0,
                             total_current_value=0.0)

# إضافة سيارة جديدة
@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    if request.method == 'POST':
        try:
            brand = request.form.get('brand', '').strip()
            model = request.form.get('model', '').strip()
            year_str = request.form.get('year', '').strip()
            license_plate = request.form.get('license_plate', '').strip()
            color = request.form.get('color', '').strip()
            purchase_price_str = request.form.get('purchase_price', '0').strip()
            current_value_str = request.form.get('current_value', '0').strip()
            engine_number = request.form.get('engine_number', '').strip()
            chassis_number = request.form.get('chassis_number', '').strip()
            notes = request.form.get('notes', '').strip()
            responsible_employee = request.form.get('responsible_employee', '').strip()
            insurance_expiry = request.form.get('insurance_expiry', '').strip()
            
            # التحقق من البيانات المطلوبة
            if not all([brand, model, year_str, license_plate]):
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                return render_template('add_car.html')
            
            # التحقق من صحة السنة
            try:
                year = int(year_str)
                if year < 1900 or year > 2030:
                    flash('يرجى إدخال سنة صحيحة', 'error')
                    return render_template('add_car.html')
            except (ValueError, TypeError):
                flash('يرجى إدخال سنة صحيحة', 'error')
                return render_template('add_car.html')
            
            # التحقق من الأسعار
            try:
                purchase_price = float(purchase_price_str) if purchase_price_str else 0.0
                current_value = float(current_value_str) if current_value_str else 0.0
            except (ValueError, TypeError):
                purchase_price = 0.0
                current_value = 0.0
            
            conn = get_db_connection()
            
            try:
                conn.execute('''
                    INSERT INTO cars (brand, model, year, license_plate, color, purchase_price, current_value, engine_number, chassis_number, notes, responsible_employee_id, insurance_expiry)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (brand, model, year, license_plate, color, purchase_price, current_value, engine_number, chassis_number, notes, 
                      responsible_employee if responsible_employee else None, insurance_expiry if insurance_expiry else None))
                
                conn.commit()
                flash('تم إضافة السيارة بنجاح!', 'success')
                return redirect(url_for('cars'))
            except sqlite3.IntegrityError:
                flash('رقم اللوحة موجود مسبقاً!', 'error')
            except Exception as e:
                print(f"خطأ في إضافة السيارة: {e}")
                flash('حدث خطأ في إضافة السيارة', 'error')
            finally:
                conn.close()
                
        except Exception as e:
            print(f"خطأ عام في معالجة بيانات السيارة: {e}")
            flash('حدث خطأ في معالجة البيانات', 'error')
    
    # جلب قائمة الموظفين النشطين
    try:
        conn = get_db_connection()
        employees = conn.execute('SELECT id, employee_number, name FROM employees WHERE status = "نشط" ORDER BY name').fetchall()
        conn.close()
        return render_template('add_car.html', employees=employees)
    except Exception as e:
        print(f"خطأ في جلب الموظفين: {e}")
        return render_template('add_car.html', employees=[])

# إدارة الموظفين
@app.route('/employees')
@login_required
def employees():
    try:
        conn = get_db_connection()
        employees_data = conn.execute('SELECT * FROM employees ORDER BY created_at DESC').fetchall()
        
        # حساب الإحصائيات
        total_salaries = 0.0
        average_salary = 0.0
        
        if employees_data:
            try:
                # حساب إجمالي الرواتب
                for employee in employees_data:
                    salary = float(employee[5]) if employee[5] else 0.0  # العمود السادس هو الراتب
                    total_salaries += salary
                
                # حساب متوسط الراتب
                average_salary = total_salaries / len(employees_data) if len(employees_data) > 0 else 0.0
                
            except Exception as e:
                print(f"خطأ في حساب إحصائيات الرواتب: {e}")
                total_salaries = 0.0
                average_salary = 0.0
        
        conn.close()
        return render_template('employees.html', 
                             employees=employees_data,
                             total_salaries=total_salaries,
                             average_salary=average_salary)
    except Exception as e:
        print(f"خطأ في صفحة الموظفين: {e}")
        return render_template('employees.html', 
                             employees=[],
                             total_salaries=0.0,
                             average_salary=0.0)

# إضافة موظف جديد
@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        try:
            employee_number = request.form.get('employee_number', '').strip()
            name = request.form.get('name', '').strip()
            position = request.form.get('position', '').strip()
            department = request.form.get('department', '').strip()
            salary_str = request.form.get('salary', '0').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            hire_date = request.form.get('hire_date', '').strip()
            notes = request.form.get('notes', '').strip()
            
            # التحقق من البيانات المطلوبة
            if not all([employee_number, name, position, department, salary_str, hire_date]):
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                return render_template('add_employee.html')
            
            # التحقق من صحة الراتب
            try:
                salary = float(salary_str)
                if salary < 0:
                    flash('يرجى إدخال راتب صحيح', 'error')
                    return render_template('add_employee.html')
            except (ValueError, TypeError):
                flash('يرجى إدخال راتب صحيح', 'error')
                return render_template('add_employee.html')
            
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
            except Exception as e:
                print(f"خطأ في إضافة الموظف: {e}")
                flash('حدث خطأ في إضافة الموظف', 'error')
            finally:
                conn.close()
                
        except Exception as e:
            print(f"خطأ عام في معالجة بيانات الموظف: {e}")
            flash('حدث خطأ في معالجة البيانات', 'error')
    
    return render_template('add_employee.html')

# عرض تفاصيل الموظف
@app.route('/employee/<int:employee_id>')
@login_required
def view_employee(employee_id):
    try:
        conn = get_db_connection()
        employee = conn.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()
        conn.close()
        
        if employee:
            return render_template('employee_details.html', employee=employee)
        else:
            flash('الموظف غير موجود!', 'error')
            return redirect(url_for('employees'))
    except Exception as e:
        print(f"خطأ في عرض تفاصيل الموظف: {e}")
        flash('حدث خطأ في عرض تفاصيل الموظف', 'error')
        return redirect(url_for('employees'))

# تعديل الموظف
@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        try:
            employee_number = request.form.get('employee_number', '').strip()
            name = request.form.get('name', '').strip()
            position = request.form.get('position', '').strip()
            department = request.form.get('department', '').strip()
            salary_str = request.form.get('salary', '0').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            hire_date = request.form.get('hire_date', '').strip()
            status = request.form.get('status', 'نشط').strip()
            notes = request.form.get('notes', '').strip()
            
            # التحقق من البيانات المطلوبة
            if not all([employee_number, name, position, department, salary_str, hire_date]):
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                return redirect(url_for('edit_employee', employee_id=employee_id))
            
            # التحقق من صحة الراتب
            try:
                salary = float(salary_str)
                if salary < 0:
                    flash('يرجى إدخال راتب صحيح', 'error')
                    return redirect(url_for('edit_employee', employee_id=employee_id))
            except (ValueError, TypeError):
                flash('يرجى إدخال راتب صحيح', 'error')
                return redirect(url_for('edit_employee', employee_id=employee_id))
            
            try:
                conn.execute('''
                    UPDATE employees 
                    SET employee_number = ?, name = ?, position = ?, department = ?, 
                        salary = ?, phone = ?, email = ?, hire_date = ?, status = ?, 
                        notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (employee_number, name, position, department, salary, phone, email, 
                      hire_date, status, notes, employee_id))
                
                conn.commit()
                flash('تم تحديث بيانات الموظف بنجاح!', 'success')
                return redirect(url_for('employees'))
                
            except sqlite3.IntegrityError:
                flash('الرقم الوظيفي موجود مسبقاً!', 'error')
            except Exception as e:
                print(f"خطأ في تحديث الموظف: {e}")
                flash('حدث خطأ في تحديث الموظف', 'error')
            finally:
                conn.close()
                
        except Exception as e:
            print(f"خطأ عام في معالجة بيانات الموظف: {e}")
            flash('حدث خطأ في معالجة البيانات', 'error')
    
    # جلب بيانات الموظف للعرض
    try:
        employee = conn.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()
        conn.close()
        
        if employee:
            return render_template('edit_employee.html', employee=employee)
        else:
            flash('الموظف غير موجود!', 'error')
            return redirect(url_for('employees'))
    except Exception as e:
        print(f"خطأ في جلب بيانات الموظف: {e}")
        flash('حدث خطأ في جلب بيانات الموظف', 'error')
        return redirect(url_for('employees'))

# حذف الموظف
@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
@login_required
def delete_employee(employee_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        conn.close()
        
        flash('تم حذف الموظف بنجاح!', 'success')
    except Exception as e:
        print(f"خطأ في حذف الموظف: {e}")
        flash('حدث خطأ في حذف الموظف', 'error')
    
    return redirect(url_for('employees'))

# إدارة المصروفات
@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    conn = get_db_connection()
    
    if request.method == 'POST':
        try:
            # طباعة جميع البيانات المرسلة للتشخيص
            print("=== بيانات النموذج المرسلة ===")
            for key, value in request.form.items():
                print(f"{key}: '{value}'")
            print("================================")
            
            expense_type = request.form.get('expense_type', '').strip()
            category = request.form.get('category', '').strip()
            amount_str = request.form.get('amount', '0').strip()
            description = request.form.get('description', '').strip()
            receipt_number = request.form.get('receipt_number', '').strip()
            date = request.form.get('date', '').strip()
            related_car = request.form.get('related_car', '').strip()
            related_employee = request.form.get('related_employee', '').strip()
            approved_by = session.get('username', 'admin')
            
            print(f"البيانات بعد المعالجة:")
            print(f"expense_type: '{expense_type}'")
            print(f"category: '{category}'")
            print(f"amount_str: '{amount_str}'")
            print(f"date: '{date}'")
            print(f"related_car: '{related_car}'")
            print(f"related_employee: '{related_employee}'")
            
            # التحقق من البيانات المطلوبة
            missing_fields = []
            if not expense_type:
                missing_fields.append('نوع المصروف')
            if not category:
                missing_fields.append('الفئة')
            if not amount_str:
                missing_fields.append('المبلغ')
            if not date:
                missing_fields.append('التاريخ')
            
            if missing_fields:
                error_msg = f'يرجى ملء الحقول التالية: {", ".join(missing_fields)}'
                print(f"خطأ في البيانات المطلوبة: {error_msg}")
                flash(error_msg, 'error')
                return redirect(url_for('expenses'))
            
            # التحقق من صحة المبلغ
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print(f"خطأ في المبلغ: {amount} <= 0")
                    flash('يرجى إدخال مبلغ صحيح أكبر من صفر', 'error')
                    return redirect(url_for('expenses'))
            except (ValueError, TypeError) as e:
                print(f"خطأ في تحويل المبلغ: {e}")
                flash('يرجى إدخال مبلغ صحيح', 'error')
                return redirect(url_for('expenses'))
            
            # معالجة القيم الاختيارية
            car_id = None
            employee_id = None
            
            if related_car and related_car.isdigit():
                car_id = int(related_car)
                print(f"تم تحديد السيارة: {car_id}")
            
            if related_employee and related_employee.isdigit():
                employee_id = int(related_employee)
                print(f"تم تحديد الموظف: {employee_id}")
            
            print(f"البيانات النهائية للإدراج:")
            print(f"expense_type: {expense_type}")
            print(f"category: {category}")
            print(f"amount: {amount}")
            print(f"description: {description}")
            print(f"receipt_number: {receipt_number}")
            print(f"date: {date}")
            print(f"car_id: {car_id}")
            print(f"employee_id: {employee_id}")
            print(f"approved_by: {approved_by}")
        
            cursor = conn.execute('''
                INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, car_id, employee_id, approved_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (expense_type, category, amount, description, receipt_number, date, car_id, employee_id, approved_by))
            
            conn.commit()
            expense_id = cursor.lastrowid
            print(f"✅ تم إضافة المصروف بنجاح! ID: {expense_id}")
            flash('تم إضافة المصروف بنجاح!', 'success')
            return redirect(url_for('expenses'))
            
        except Exception as e:
            print(f"❌ خطأ في إضافة المصروف: {e}")
            print(f"نوع الخطأ: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            flash(f'حدث خطأ في إضافة المصروف: {str(e)}', 'error')
            return redirect(url_for('expenses'))
    
    # الحصول على فلاتر التاريخ
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    # بناء الاستعلام مع الفلاتر
    query = 'SELECT * FROM expenses'
    params = []
    
    if start_date and end_date:
        query += ' WHERE date BETWEEN ? AND ?'
        params = [start_date, end_date]
    elif start_date:
        query += ' WHERE date >= ?'
        params = [start_date]
    elif end_date:
        query += ' WHERE date <= ?'
        params = [end_date]
    
    query += ' ORDER BY date DESC, created_at DESC'
    
    # جلب المصروفات مع الفلاتر
    expenses_data = conn.execute(query, params).fetchall()
    
    # إحصائيات المصروفات للفترة المحددة
    stats_query = 'SELECT COALESCE(SUM(amount), 0) FROM expenses'
    if params:
        if start_date and end_date:
            stats_query += ' WHERE date BETWEEN ? AND ?'
        elif start_date:
            stats_query += ' WHERE date >= ?'
        elif end_date:
            stats_query += ' WHERE date <= ?'
    
    total_expenses = conn.execute(stats_query, params).fetchone()[0]
    category_stats = dict(conn.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category').fetchall())
    
    # جلب السيارات والموظفين للنموذج
    cars = conn.execute('SELECT * FROM cars ORDER BY brand, model').fetchall()
    employees = conn.execute('SELECT id, employee_number, name FROM employees WHERE status = "نشط" ORDER BY name').fetchall()
    
    conn.close()
    
    return render_template('expenses.html', 
                         expenses=expenses_data,
                         total_expenses=total_expenses,
                         category_stats=category_stats,
                         cars=cars,
                         employees=employees)

# تعديل المصروف
@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        try:
            expense_type = request.form.get('expense_type', '').strip()
            category = request.form.get('category', '').strip()
            amount_str = request.form.get('amount', '0').strip()
            description = request.form.get('description', '').strip()
            receipt_number = request.form.get('receipt_number', '').strip()
            date = request.form.get('date', '').strip()
            
            # التحقق من البيانات المطلوبة
            if not all([expense_type, category, amount_str, date]):
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                return redirect(url_for('edit_expense', expense_id=expense_id))
            
            # التحقق من صحة المبلغ
            try:
                amount = float(amount_str)
                if amount <= 0:
                    flash('يرجى إدخال مبلغ صحيح أكبر من صفر', 'error')
                    return redirect(url_for('edit_expense', expense_id=expense_id))
            except (ValueError, TypeError):
                flash('يرجى إدخال مبلغ صحيح', 'error')
                return redirect(url_for('edit_expense', expense_id=expense_id))
            
            try:
                conn.execute('''
                    UPDATE expenses 
                    SET expense_type = ?, category = ?, amount = ?, description = ?, 
                        receipt_number = ?, date = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (expense_type, category, amount, description, receipt_number, date, expense_id))
                
                conn.commit()
                flash('تم تحديث المصروف بنجاح!', 'success')
                return redirect(url_for('expenses'))
                
            except Exception as e:
                print(f"خطأ في تحديث المصروف: {e}")
                flash('حدث خطأ في تحديث المصروف', 'error')
            finally:
                conn.close()
                
        except Exception as e:
            print(f"خطأ عام في معالجة بيانات المصروف: {e}")
            flash('حدث خطأ في معالجة البيانات', 'error')
    
    # جلب بيانات المصروف للعرض
    try:
        expense = conn.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,)).fetchone()
        conn.close()
        
        if expense:
            return render_template('edit_expense.html', expense=expense)
        else:
            flash('المصروف غير موجود!', 'error')
            return redirect(url_for('expenses'))
    except Exception as e:
        print(f"خطأ في جلب بيانات المصروف: {e}")
        flash('حدث خطأ في جلب بيانات المصروف', 'error')
        return redirect(url_for('expenses'))

# حذف المصروف
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        
        flash('تم حذف المصروف بنجاح!', 'success')
    except Exception as e:
        print(f"خطأ في حذف المصروف: {e}")
        flash('حدث خطأ في حذف المصروف', 'error')
    
    return redirect(url_for('expenses'))

# طباعة سجل المصروفات
@app.route('/print_expenses')
@login_required
def print_expenses():
    try:
        conn = get_db_connection()
        
        # الحصول على فلاتر التاريخ
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
        # بناء الاستعلام
        query = 'SELECT * FROM expenses'
        params = []
        
        if start_date and end_date:
            query += ' WHERE date BETWEEN ? AND ?'
            params = [start_date, end_date]
        elif start_date:
            query += ' WHERE date >= ?'
            params = [start_date]
        elif end_date:
            query += ' WHERE date <= ?'
            params = [end_date]
        
        query += ' ORDER BY date DESC'
        
        expenses_data = conn.execute(query, params).fetchall()
        total_expenses = sum(float(expense[3]) for expense in expenses_data)
        
        conn.close()
        
        return render_template('print_expenses.html', 
                             expenses=expenses_data,
                             total_expenses=total_expenses,
                             start_date=start_date,
                             end_date=end_date)
    except Exception as e:
        print(f"خطأ في طباعة المصروفات: {e}")
        flash('حدث خطأ في إعداد الطباعة', 'error')
        return redirect(url_for('expenses'))

# طباعة سجل الخزينة
@app.route('/print_treasury')
@login_required
def print_treasury():
    try:
        conn = get_db_connection()
        
        # الحصول على فلاتر التاريخ
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
        # بناء الاستعلام
        query = 'SELECT * FROM treasury'
        params = []
        
        if start_date and end_date:
            query += ' WHERE date BETWEEN ? AND ?'
            params = [start_date, end_date]
        elif start_date:
            query += ' WHERE date >= ?'
            params = [start_date]
        elif end_date:
            query += ' WHERE date <= ?'
            params = [end_date]
        
        query += ' ORDER BY date DESC'
        
        transactions_data = conn.execute(query, params).fetchall()
        
        # حساب الإحصائيات للفترة المحددة
        total_deposits = sum(float(t[2]) for t in transactions_data if t[1] == 'إيداع')
        total_withdrawals = sum(float(t[2]) for t in transactions_data if t[1] == 'سحب')
        
        conn.close()
        
        return render_template('print_treasury.html', 
                             transactions=transactions_data,
                             total_deposits=total_deposits,
                             total_withdrawals=total_withdrawals,
                             start_date=start_date,
                             end_date=end_date)
    except Exception as e:
        print(f"خطأ في طباعة سجل الخزينة: {e}")
        flash('حدث خطأ في إعداد الطباعة', 'error')
        return redirect(url_for('treasury'))

# صفحة التقارير
@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

# صفحة التحليلات الشاملة
@app.route('/analytics')
@login_required
def analytics():
    conn = get_db_connection()
    
    # الحصول على فلاتر البحث
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    activity_type = request.args.get('activity_type')
    
    activities = []
    
    try:
        # جمع حركات الخزينة
        if not activity_type or activity_type == 'treasury':
            treasury_query = '''
                SELECT 
                    date, created_at, type, amount, description, reference_number,
                    'treasury' as source_type
                FROM treasury 
                WHERE 1=1
            '''
            params = []
            
            if start_date:
                treasury_query += ' AND date >= ?'
                params.append(start_date)
            if end_date:
                treasury_query += ' AND date <= ?'
                params.append(end_date)
                
            treasury_query += ' ORDER BY created_at DESC'
            
            treasury_records = conn.execute(treasury_query, params).fetchall()
            
            for record in treasury_records:
                activities.append({
                    'date': record['date'],
                    'time': record['created_at'].split(' ')[1] if record['created_at'] and ' ' in record['created_at'] else '',
                    'type_name': 'حركة الخزينة',
                    'type_class': 'bg-success' if record['type'] == 'إيداع' else 'bg-danger',
                    'icon': 'fas fa-cash-register',
                    'description': f"{record['type']} - {record['description']}",
                    'details': f"رقم المرجع: {record['reference_number']}",
                    'amount': record['amount'],
                    'user': 'النظام',
                    'responsible': '',
                    'status': record['type'],
                    'status_class': 'bg-success' if record['type'] == 'إيداع' else 'bg-danger',
                    'sort_date': record['created_at'] or record['date']
                })
        
        # جمع المصروفات
        if not activity_type or activity_type == 'expenses':
            expenses_query = '''
                SELECT 
                    date, created_at, amount, description, category, car_id, employee_id, expense_type,
                    'expenses' as source_type
                FROM expenses 
                WHERE 1=1
            '''
            expenses_params = []
            
            if start_date:
                expenses_query += ' AND date >= ?'
                expenses_params.append(start_date)
            if end_date:
                expenses_query += ' AND date <= ?'
                expenses_params.append(end_date)
                
            expenses_query += ' ORDER BY created_at DESC'
            
            print(f"Debug - استعلام المصروفات: {expenses_query}")
            print(f"Debug - معاملات المصروفات: {expenses_params}")
            
            expenses_records = conn.execute(expenses_query, expenses_params).fetchall()
            print(f"Debug - عدد المصروفات المسترجعة: {len(expenses_records)}")
            
            for record in expenses_records:
                car_info = ''
                employee_info = ''
                
                if record['car_id']:
                    car = conn.execute('SELECT license_plate FROM cars WHERE id = ?', (record['car_id'],)).fetchone()
                    car_info = f" - السيارة: {car['license_plate']}" if car else ''
                
                if record['employee_id']:
                    employee = conn.execute('SELECT name FROM employees WHERE id = ?', (record['employee_id'],)).fetchone()
                    employee_info = f" - الموظف: {employee['name']}" if employee else ''
                
                print(f"Debug - إضافة مصروف: {record['description']} - {record['amount']}")
                
                activities.append({
                    'date': record['date'],
                    'time': record['created_at'].split(' ')[1] if record['created_at'] and ' ' in record['created_at'] else '',
                    'type_name': 'مصروف',
                    'type_class': 'bg-warning',
                    'icon': 'fas fa-money-bill-wave',
                    'description': f"{record['expense_type']} - {record['description']}",
                    'details': f"الفئة: {record['category']}{car_info}{employee_info}",
                    'amount': -abs(record['amount']),  # سالب للمصروفات
                    'user': 'النظام',
                    'responsible': '',
                    'status': 'مصروف',
                    'status_class': 'bg-warning',
                    'sort_date': record['created_at'] or record['date']
                })
        
        # جمع حركات الموظفين
        if not activity_type or activity_type == 'employees':
            # إضافة موظفين جدد
            employees_query = '''
                SELECT 
                    created_at, name, position, department, salary,
                    'employee_add' as source_type
                FROM employees 
                WHERE 1=1
            '''
            employees_params = []
            
            if start_date:
                employees_query += ' AND DATE(created_at) >= ?'
                employees_params.append(start_date)
            if end_date:
                employees_query += ' AND DATE(created_at) <= ?'
                employees_params.append(end_date)
                
            employees_query += ' ORDER BY created_at DESC'
            
            employees_records = conn.execute(employees_query, employees_params).fetchall()
            
            for record in employees_records:
                activities.append({
                    'date': record['created_at'].split(' ')[0] if record['created_at'] else '',
                    'time': record['created_at'].split(' ')[1] if record['created_at'] and ' ' in record['created_at'] else '',
                    'type_name': 'إضافة موظف',
                    'type_class': 'bg-info',
                    'icon': 'fas fa-user-plus',
                    'description': f"إضافة موظف جديد: {record['name']}",
                    'details': f"المنصب: {record['position']} - القسم: {record['department']}",
                    'amount': None,
                    'user': 'النظام',
                    'responsible': record['name'],
                    'status': 'نشط',
                    'status_class': 'bg-success',
                    'sort_date': record['created_at']
                })
        
        # جمع حركات السيارات
        if not activity_type or activity_type == 'cars':
            cars_query = '''
                SELECT 
                    created_at, license_plate, brand, model, year, status,
                    'car_add' as source_type
                FROM cars 
                WHERE 1=1
            '''
            cars_params = []
            
            if start_date:
                cars_query += ' AND DATE(created_at) >= ?'
                cars_params.append(start_date)
            if end_date:
                cars_query += ' AND DATE(created_at) <= ?'
                cars_params.append(end_date)
                
            cars_query += ' ORDER BY created_at DESC'
            
            cars_records = conn.execute(cars_query, cars_params).fetchall()
            
            for record in cars_records:
                activities.append({
                    'date': record['created_at'].split(' ')[0] if record['created_at'] else '',
                    'time': record['created_at'].split(' ')[1] if record['created_at'] and ' ' in record['created_at'] else '',
                    'type_name': 'إضافة سيارة',
                    'type_class': 'bg-primary',
                    'icon': 'fas fa-car',
                    'description': f"إضافة سيارة جديدة: {record['license_plate']}",
                    'details': f"{record['brand']} {record['model']} - {record['year']}",
                    'amount': None,
                    'user': 'النظام',
                    'responsible': '',
                    'status': record['status'],
                    'status_class': 'bg-success' if record['status'] == 'متاح' else 'bg-warning',
                    'sort_date': record['created_at']
                })
        
        # جمع عمليات التسليم والتسلم
        if not activity_type or activity_type == 'handovers':
            custody_query = '''
                SELECT 
                    cc.created_at, cc.custody_date, cc.return_date, cc.status, cc.notes,
                    c.license_plate, e.name as employee_name,
                    'custody' as source_type
                FROM car_custody cc
                LEFT JOIN cars c ON cc.car_id = c.id
                LEFT JOIN employees e ON cc.employee_id = e.id
                WHERE 1=1
            '''
            custody_params = []
            
            if start_date:
                custody_query += ' AND DATE(cc.created_at) >= ?'
                custody_params.append(start_date)
            if end_date:
                custody_query += ' AND DATE(cc.created_at) <= ?'
                custody_params.append(end_date)
                
            custody_query += ' ORDER BY cc.created_at DESC'
            
            custody_records = conn.execute(custody_query, custody_params).fetchall()
            
            for record in custody_records:
                status_text = 'تسليم' if record['status'] == 'نشط' else 'تسلم'
                activities.append({
                    'date': record['created_at'].split(' ')[0] if record['created_at'] else '',
                    'time': record['created_at'].split(' ')[1] if record['created_at'] and ' ' in record['created_at'] else '',
                    'type_name': f'عملية {status_text}',
                    'type_class': 'bg-secondary',
                    'icon': 'fas fa-exchange-alt',
                    'description': f"{status_text} سيارة {record['license_plate']} للموظف {record['employee_name']}",
                    'details': f"تاريخ التسليم: {record['custody_date']} - الملاحظات: {record['notes'] or 'لا توجد'}",
                    'amount': None,
                    'user': 'النظام',
                    'responsible': record['employee_name'],
                    'status': record['status'],
                    'status_class': 'bg-success' if record['status'] == 'نشط' else 'bg-info',
                    'sort_date': record['created_at']
                })
        
        # ترتيب الأنشطة حسب التاريخ (الأحدث أولاً)
        activities.sort(key=lambda x: x['sort_date'] or '', reverse=True)
        
        # طباعة تشخيصية
        print(f"Debug - إجمالي الأنشطة المجمعة: {len(activities)}")
        activity_types = {}
        for activity in activities:
            activity_type = activity['type_name']
            activity_types[activity_type] = activity_types.get(activity_type, 0) + 1
        
        print("Debug - توزيع الأنشطة:")
        for activity_type, count in activity_types.items():
            print(f"  {activity_type}: {count}")
        
        # حساب الإحصائيات
        total_activities = len(activities)
        treasury_count = len([a for a in activities if a['type_name'] == 'حركة الخزينة'])
        car_activities_count = len([a for a in activities if 'سيارة' in a['type_name']])
        employee_activities_count = len([a for a in activities if 'موظف' in a['type_name']])
        expenses_count = len([a for a in activities if a['type_name'] == 'مصروف'])
        
        print(f"Debug - الإحصائيات النهائية:")
        print(f"  إجمالي الأنشطة: {total_activities}")
        print(f"  حركات الخزينة: {treasury_count}")
        print(f"  حركات السيارات: {car_activities_count}")
        print(f"  حركات الموظفين: {employee_activities_count}")
        print(f"  المصروفات: {expenses_count}")
        
    except Exception as e:
        print(f"خطأ في جمع بيانات التحليلات: {e}")
        activities = []
        total_activities = treasury_count = car_activities_count = employee_activities_count = expenses_count = 0
    
    finally:
        conn.close()
    
    return render_template('analytics.html', 
                         activities=activities,
                         total_activities=total_activities,
                         treasury_count=treasury_count,
                         car_activities_count=car_activities_count,
                         employee_activities_count=employee_activities_count,
                         expenses_count=expenses_count)

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
    
    return render_template('settings_simple.html', settings=settings_data)

# النسخ الاحتياطي
@app.route('/backup', methods=['POST'])
@login_required
def create_backup():
    try:
        import shutil
        import os
        from datetime import datetime
        
        # إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجوداً
        backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # اسم ملف النسخة الاحتياطية
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'backup_{timestamp}.db'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # نسخ قاعدة البيانات
        db_path = os.path.join(os.path.dirname(__file__), 'car_management.db')
        shutil.copy2(db_path, backup_path)
        
        flash(f'تم إنشاء النسخة الاحتياطية بنجاح: {backup_filename}', 'success')
    except Exception as e:
        print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
        flash('حدث خطأ في إنشاء النسخة الاحتياطية', 'error')
    
    return redirect(url_for('settings'))

# استعادة النسخة الاحتياطية
@app.route('/restore', methods=['POST'])
@login_required
def restore_backup():
    try:
        if 'backup_file' not in request.files:
            flash('يرجى اختيار ملف النسخة الاحتياطية', 'error')
            return redirect(url_for('settings'))
        
        file = request.files['backup_file']
        if file.filename == '':
            flash('يرجى اختيار ملف النسخة الاحتياطية', 'error')
            return redirect(url_for('settings'))
        
        if file and file.filename.endswith('.db'):
            import os
            import shutil
            
            # حفظ النسخة الحالية كنسخة احتياطية
            current_db = os.path.join(os.path.dirname(__file__), 'car_management.db')
            backup_current = os.path.join(os.path.dirname(__file__), 'car_management_backup_before_restore.db')
            shutil.copy2(current_db, backup_current)
            
            # استعادة النسخة الاحتياطية
            file.save(current_db)
            
            flash('تم استعادة النسخة الاحتياطية بنجاح!', 'success')
        else:
            flash('يرجى اختيار ملف نسخة احتياطية صحيح (.db)', 'error')
    except Exception as e:
        print(f"خطأ في استعادة النسخة الاحتياطية: {e}")
        flash('حدث خطأ في استعادة النسخة الاحتياطية', 'error')
    
    return redirect(url_for('settings'))

# تصدير البيانات إلى Excel
@app.route('/export/<table_name>')
@login_required
def export_to_excel(table_name):
    try:
        import pandas as pd
        from datetime import datetime
        
        conn = get_db_connection()
        
        # تحديد الجداول المسموح بتصديرها
        allowed_tables = {
            'employees': 'الموظفين',
            'cars': 'السيارات', 
            'expenses': 'المصروفات',
            'treasury': 'الخزينة',
            'car_custody': 'عهدة السيارات'
        }
        
        if table_name not in allowed_tables:
            flash('جدول غير صحيح', 'error')
            return redirect(url_for('settings'))
        
        # جلب البيانات
        df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
        conn.close()
        
        # إنشاء ملف Excel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{allowed_tables[table_name]}_{timestamp}.xlsx'
        
        # حفظ الملف مؤقتاً
        import os
        temp_path = os.path.join(os.path.dirname(__file__), 'temp', filename)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        df.to_excel(temp_path, index=False, engine='openpyxl')
        
        # إرسال الملف للتحميل
        from flask import send_file
        return send_file(temp_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        print(f"خطأ في تصدير البيانات: {e}")
        flash('حدث خطأ في تصدير البيانات', 'error')
        return redirect(url_for('settings'))

# إدارة المستخدمين
@app.route('/users')
@login_required
def users():
    try:
        conn = get_db_connection()
        users_data = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
        conn.close()
        return render_template('users.html', users=users_data)
    except Exception as e:
        print(f"خطأ في جلب المستخدمين: {e}")
        flash('حدث خطأ في جلب بيانات المستخدمين', 'error')
        return redirect(url_for('index'))

# إضافة مستخدم جديد
@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            role = request.form.get('role', 'user').strip()
            
            if not username or not password:
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                return redirect(url_for('add_user'))
            
            # التحقق من عدم وجود المستخدم
            conn = get_db_connection()
            existing = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
            if existing:
                flash('اسم المستخدم موجود بالفعل', 'error')
                conn.close()
                return redirect(url_for('add_user'))
            
            # تشفير كلمة المرور
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash(password)
            
            # إضافة المستخدم
            conn.execute('''
                INSERT INTO users (username, password, role, created_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (username, hashed_password, role))
            
            conn.commit()
            conn.close()
            
            flash('تم إضافة المستخدم بنجاح!', 'success')
            return redirect(url_for('users'))
            
        except Exception as e:
            print(f"خطأ في إضافة المستخدم: {e}")
            flash('حدث خطأ في إضافة المستخدم', 'error')
    
    return render_template('add_user.html')

# حذف مستخدم
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    try:
        # منع حذف المستخدم الحالي
        conn = get_db_connection()
        current_user = conn.execute('SELECT username FROM users WHERE id = ?', (user_id,)).fetchone()
        
        if current_user and current_user[0] == session.get('username'):
            flash('لا يمكن حذف المستخدم الحالي', 'error')
            conn.close()
            return redirect(url_for('users'))
        
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        flash('تم حذف المستخدم بنجاح!', 'success')
    except Exception as e:
        print(f"خطأ في حذف المستخدم: {e}")
        flash('حدث خطأ في حذف المستخدم', 'error')
    
    return redirect(url_for('users'))

# تغيير كلمة المرور
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        try:
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if not all([current_password, new_password, confirm_password]):
                flash('يرجى ملء جميع الحقول', 'error')
                return redirect(url_for('change_password'))
            
            if new_password != confirm_password:
                flash('كلمة المرور الجديدة غير متطابقة', 'error')
                return redirect(url_for('change_password'))
            
            # التحقق من كلمة المرور الحالية
            conn = get_db_connection()
            user = conn.execute('SELECT password FROM users WHERE username = ?', 
                              (session.get('username'),)).fetchone()
            
            if not user:
                flash('المستخدم غير موجود', 'error')
                conn.close()
                return redirect(url_for('change_password'))
            
            from werkzeug.security import check_password_hash, generate_password_hash
            if not check_password_hash(user[0], current_password):
                flash('كلمة المرور الحالية غير صحيحة', 'error')
                conn.close()
                return redirect(url_for('change_password'))
            
            # تحديث كلمة المرور
            hashed_password = generate_password_hash(new_password)
            conn.execute('UPDATE users SET password = ? WHERE username = ?', 
                        (hashed_password, session.get('username')))
            conn.commit()
            conn.close()
            
            flash('تم تغيير كلمة المرور بنجاح!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"خطأ في تغيير كلمة المرور: {e}")
            flash('حدث خطأ في تغيير كلمة المرور', 'error')
    
    return render_template('change_password.html')

# عرض بيانات المطور
@app.route('/developer_info')
@login_required
def developer_info():
    try:
        conn = get_db_connection()
        developer = conn.execute('SELECT * FROM developer_info ORDER BY created_at DESC LIMIT 1').fetchone()
        conn.close()
        
        if developer:
            return render_template('developer_info.html', developer=developer)
        else:
            # إذا لم توجد بيانات، إنشاء بيانات افتراضية
            flash('لم يتم العثور على بيانات المطور', 'info')
            return redirect(url_for('settings'))
    except Exception as e:
        print(f"خطأ في جلب بيانات المطور: {e}")
        flash('حدث خطأ في جلب بيانات المطور', 'error')
        return redirect(url_for('index'))

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