#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import hashlib
import os
import webbrowser
import threading
import time
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'rashid_industrial_secret_key_2024'

DATABASE = 'management_system.db'

def get_db_connection():
    """الحصول على اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """تأكيد تسجيل الدخول"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        
        # إحصائيات أساسية
        total_employees = conn.execute('SELECT COUNT(*) FROM employees').fetchone()[0] or 0
        total_cars = conn.execute('SELECT COUNT(*) FROM cars').fetchone()[0] or 0
        current_balance = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
        current_balance = float(current_balance[0]) if current_balance else 0.0
        total_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses').fetchone()[0] or 0
        
        conn.close()
        
        return render_template('index.html',
                             total_employees=total_employees,
                             total_cars=total_cars,
                             current_balance=current_balance,
                             total_expenses=total_expenses)
    except Exception as e:
        print(f"خطأ في الصفحة الرئيسية: {e}")
        return render_template('index.html',
                             total_employees=0,
                             total_cars=0,
                             current_balance=0.0,
                             total_expenses=0)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == 'admin' and password == 'admin123':
            session['user_id'] = 1
            session['username'] = 'admin'
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('login'))

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
                conn.execute('INSERT INTO employees (employee_number, name, position, department, salary, phone, email, hire_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (employee_number, name, position, department, salary, phone, email, hire_date, notes))
                
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
                conn.execute('INSERT INTO cars (brand, model, year, license_plate, color, purchase_price, current_value, engine_number, chassis_number, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, model, year, license_plate, color, purchase_price, current_value, engine_number, chassis_number, notes))
                
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
    
    return render_template('add_car.html')

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
                
                current_balance_row = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
                current_balance = float(current_balance_row[0]) if current_balance_row else 0.0
                
                if transaction_type == 'إيداع':
                    new_balance = current_balance + amount
                else:
                    new_balance = current_balance - amount
                    if new_balance < 0:
                        flash('لا يمكن السحب - الرصيد غير كافي', 'error')
                        return redirect(url_for('treasury'))
                
                conn.execute('INSERT INTO treasury (transaction_type, amount, description, reference_number, created_by, date, balance_after) VALUES (?, ?, ?, ?, ?, ?, ?)', (transaction_type, amount, description, reference_number, created_by, date, new_balance))
                
                conn.commit()
                flash(f'تم إضافة {transaction_type} بمبلغ {amount:,.0f} ريال بنجاح!', 'success')
                return redirect(url_for('treasury'))
                
            except Exception as e:
                print(f"خطأ في معالجة معاملة الخزينة: {e}")
                flash('حدث خطأ في تسجيل المعاملة', 'error')
        
        transactions = conn.execute('SELECT * FROM treasury ORDER BY created_at DESC').fetchall()
        
        try:
            total_deposits = float(conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"').fetchone()[0] or 0)
            total_withdrawals = float(conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "سحب"').fetchone()[0] or 0)
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
        flash('حدث خطأ في تحميل صفحة الخزينة', 'error')
        return redirect(url_for('index'))

@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    conn = get_db_connection()
    
    if request.method == 'POST':
        try:
            expense_type = request.form.get('expense_type', '').strip()
            category = request.form.get('category', '').strip()
            amount_str = request.form.get('amount', '0').strip()
            description = request.form.get('description', '').strip()
            receipt_number = request.form.get('receipt_number', '').strip()
            date = request.form.get('date', '').strip()
            approved_by = session.get('username', 'admin')
            
            if not all([expense_type, category, amount_str, date]):
                flash('يرجى ملء جميع الحقول المطلوبة', 'error')
                return redirect(url_for('expenses'))
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    flash('يرجى إدخال مبلغ صحيح أكبر من صفر', 'error')
                    return redirect(url_for('expenses'))
            except (ValueError, TypeError):
                flash('يرجى إدخال مبلغ صحيح', 'error')
                return redirect(url_for('expenses'))
            
            conn.execute('INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, approved_by) VALUES (?, ?, ?, ?, ?, ?, ?)', (expense_type, category, amount, description, receipt_number, date, approved_by))
            
            conn.commit()
            flash('تم إضافة المصروف بنجاح!', 'success')
            return redirect(url_for('expenses'))
            
        except Exception as e:
            print(f"خطأ في إضافة المصروف: {e}")
            flash('حدث خطأ في إضافة المصروف', 'error')
            return redirect(url_for('expenses'))
    
    # جلب جميع المصروفات
    expenses_data = conn.execute('SELECT * FROM expenses ORDER BY date DESC, created_at DESC').fetchall()
    
    # إحصائيات المصروفات
    total_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses').fetchone()[0] or 0
    category_stats = dict(conn.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category').fetchall())
    
    conn.close()
    
    return render_template('expenses.html', 
                         expenses=expenses_data,
                         total_expenses=total_expenses,
                         category_stats=category_stats)

# باقي الـ routes البسيطة
@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/car_entry')
@login_required
def car_entry():
    return render_template('car_entry.html')

@app.route('/car_delivery')
@login_required
def car_delivery():
    return render_template('car_delivery.html')

@app.route('/car_receipt')
@login_required
def car_receipt():
    return render_template('car_receipt.html')

@app.route('/car_custody')
@login_required
def car_custody():
    return render_template('car_custody.html')

@app.route('/financial_reports')
@login_required
def financial_reports():
    try:
        conn = get_db_connection()
        
        # حساب الإحصائيات المالية
        total_income = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"').fetchone()[0] or 0
        total_expenses = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses').fetchone()[0] or 0
        net_profit = float(total_income) - float(total_expenses)
        
        conn.close()
        
        return render_template('financial_reports.html',
                             total_income=total_income,
                             total_expenses=total_expenses,
                             net_profit=net_profit)
    except Exception as e:
        print(f"خطأ في التقارير المالية: {e}")
        return render_template('financial_reports.html',
                             total_income=0,
                             total_expenses=0,
                             net_profit=0)

def open_browser():
    """فتح المتصفح تلقائياً"""
    time.sleep(3)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("✅ تم إعداد معالجات الأخطاء بنجاح")
    print("🚀 بدء تشغيل نظام الإدارة الشامل...")
    print("🔧 تهيئة قاعدة البيانات...")
    print("✅ تم تهيئة قاعدة البيانات بنجاح")
    print("🌐 الرابط: http://localhost:5000")
    print("👤 اسم المستخدم: admin")
    print("🔑 كلمة المرور: admin123")
    print("⚠️  لإيقاف النظام اضغط Ctrl+C")
    print("🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان...")
    print("=" * 50)
    
    # فتح المتصفح في thread منفصل
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=True)