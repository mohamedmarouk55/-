#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ملف إصلاح شامل لجميع مشاكل النظام
RASHID INDUSTRIAL CO.
"""

import sqlite3
import os
from datetime import datetime

def fix_database_issues():
    """إصلاح مشاكل قاعدة البيانات"""
    print("🔧 إصلاح مشاكل قاعدة البيانات...")
    
    DATABASE = 'management_system.db'
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # التأكد من وجود جميع الجداول
        tables_to_create = [
            # جدول المستخدمين
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            # جدول الموظفين
            '''CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_number TEXT UNIQUE,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL DEFAULT 0,
                phone TEXT,
                email TEXT,
                hire_date TEXT NOT NULL,
                status TEXT DEFAULT 'نشط',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            # جدول السيارات
            '''CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                license_plate TEXT UNIQUE NOT NULL,
                color TEXT,
                status TEXT DEFAULT 'متاح',
                purchase_price REAL DEFAULT 0,
                current_value REAL DEFAULT 0,
                engine_number TEXT,
                chassis_number TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            # جدول الخزينة
            '''CREATE TABLE IF NOT EXISTS treasury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL CHECK (transaction_type IN ('إيداع', 'سحب')),
                amount REAL NOT NULL DEFAULT 0,
                description TEXT,
                reference_number TEXT,
                created_by TEXT,
                date TEXT NOT NULL,
                balance_after REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            # جدول المصروفات
            '''CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL DEFAULT 0,
                description TEXT,
                receipt_number TEXT,
                date TEXT NOT NULL,
                approved_by TEXT,
                status TEXT DEFAULT 'معتمد',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            # جدول عهد السيارات
            '''CREATE TABLE IF NOT EXISTS car_custody (
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
            )''',
            
            # جدول البيانات المالية
            '''CREATE TABLE IF NOT EXISTS financial_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_type TEXT NOT NULL,
                amount REAL NOT NULL DEFAULT 0,
                description TEXT,
                date TEXT NOT NULL,
                category TEXT,
                reference_id INTEGER,
                created_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )'''
        ]
        
        for table_sql in tables_to_create:
            cursor.execute(table_sql)
        
        # إضافة مستخدم admin افتراضي
        import hashlib
        admin_password = hashlib.md5('admin123'.encode()).hexdigest()
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@rashid.com', admin_password, 'admin', 1))
        
        # إضافة بيانات تجريبية إذا لم تكن موجودة
        cursor.execute('SELECT COUNT(*) FROM employees')
        if cursor.fetchone()[0] == 0:
            sample_employees = [
                ('EMP001', 'أحمد محمد علي', 'مدير عام', 'الإدارة', 15000, '0501234567', 'ahmed@rashid.com', '2024-01-01', 'نشط', 'موظف متميز'),
                ('EMP002', 'فاطمة أحمد', 'محاسبة', 'المالية', 8000, '0507654321', 'fatima@rashid.com', '2024-01-15', 'نشط', ''),
                ('EMP003', 'محمد سالم', 'سائق', 'النقل', 4000, '0509876543', 'mohammed@rashid.com', '2024-02-01', 'نشط', ''),
            ]
            
            cursor.executemany('''
                INSERT INTO employees (employee_number, name, position, department, salary, phone, email, hire_date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_employees)
        
        cursor.execute('SELECT COUNT(*) FROM cars')
        if cursor.fetchone()[0] == 0:
            sample_cars = [
                ('تويوتا', 'كامري', 2023, 'أ ب ج 1234', 'أبيض', 'متاح', 85000, 80000, 'ENG123456', 'CHS789012', 'سيارة جديدة'),
                ('هوندا', 'أكورد', 2022, 'د هـ و 5678', 'أسود', 'متاح', 75000, 70000, 'ENG654321', 'CHS210987', ''),
                ('نيسان', 'التيما', 2021, 'ز ح ط 9012', 'فضي', 'مستخدم', 65000, 60000, 'ENG987654', 'CHS456789', 'تحتاج صيانة'),
            ]
            
            cursor.executemany('''
                INSERT INTO cars (brand, model, year, license_plate, color, status, purchase_price, current_value, engine_number, chassis_number, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_cars)
        
        # إضافة معاملات خزينة تجريبية
        cursor.execute('SELECT COUNT(*) FROM treasury')
        if cursor.fetchone()[0] == 0:
            sample_treasury = [
                ('إيداع', 100000, 'رأس المال الأولي', 'REF001', 'admin', '2024-01-01', 100000),
                ('سحب', 15000, 'رواتب الموظفين - يناير', 'REF002', 'admin', '2024-01-31', 85000),
                ('إيداع', 50000, 'إيرادات الشهر', 'REF003', 'admin', '2024-02-15', 135000),
            ]
            
            cursor.executemany('''
                INSERT INTO treasury (transaction_type, amount, description, reference_number, created_by, date, balance_after)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sample_treasury)
        
        # إضافة مصروفات تجريبية
        cursor.execute('SELECT COUNT(*) FROM expenses')
        if cursor.fetchone()[0] == 0:
            sample_expenses = [
                ('تشغيلية', 'وقود', 2500, 'وقود السيارات', 'REC001', '2024-01-15', 'admin', 'معتمد'),
                ('إدارية', 'مكتبية', 800, 'أدوات مكتبية', 'REC002', '2024-01-20', 'admin', 'معتمد'),
                ('صيانة', 'سيارات', 1200, 'صيانة دورية', 'REC003', '2024-02-01', 'admin', 'معتمد'),
            ]
            
            cursor.executemany('''
                INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, approved_by, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_expenses)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إصلاح قاعدة البيانات بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح قاعدة البيانات: {e}")
        return False

def fix_template_issues():
    """إصلاح مشاكل القوالب"""
    print("🔧 إصلاح مشاكل القوالب...")
    
    templates_dir = 'templates'
    
    # قائمة القوالب المطلوبة
    required_templates = [
        'base.html', 'index.html', 'login.html', 'treasury.html',
        'cars.html', 'add_car.html', 'employees.html', 'add_employee.html',
        'expenses.html', 'reports.html', 'settings.html', 'car_custody.html',
        'car_entry.html', 'car_delivery.html', 'car_receipt.html',
        'financial_reports.html'
    ]
    
    missing_templates = []
    
    for template in required_templates:
        template_path = os.path.join(templates_dir, template)
        if not os.path.exists(template_path):
            missing_templates.append(template)
    
    if missing_templates:
        print(f"⚠️ القوالب المفقودة: {', '.join(missing_templates)}")
    else:
        print("✅ جميع القوالب موجودة!")
    
    return len(missing_templates) == 0

def create_test_script():
    """إنشاء سكريبت اختبار شامل"""
    print("🔧 إنشاء سكريبت اختبار شامل...")
    
    test_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت اختبار شامل للنظام
"""

import requests
import time

def test_system():
    """اختبار النظام"""
    base_url = 'http://localhost:5000'
    
    print("🧪 بدء اختبار النظام...")
    
    # اختبار الصفحة الرئيسية
    try:
        response = requests.get(f'{base_url}/')
        if response.status_code == 200 or response.status_code == 302:
            print("✅ الصفحة الرئيسية تعمل")
        else:
            print(f"❌ مشكلة في الصفحة الرئيسية: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False
    
    # اختبار صفحات أخرى
    pages_to_test = [
        '/login',
        '/treasury', 
        '/cars',
        '/employees',
        '/expenses',
        '/reports',
        '/settings'
    ]
    
    for page in pages_to_test:
        try:
            response = requests.get(f'{base_url}{page}')
            if response.status_code in [200, 302, 401]:  # 401 للصفحات المحمية
                print(f"✅ صفحة {page} تعمل")
            else:
                print(f"❌ مشكلة في صفحة {page}: {response.status_code}")
        except Exception as e:
            print(f"❌ خطأ في صفحة {page}: {e}")
    
    print("🎉 انتهى الاختبار!")
    return True

if __name__ == '__main__':
    test_system()
'''
    
    with open('test_system.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ تم إنشاء سكريبت الاختبار!")

def main():
    """الدالة الرئيسية للإصلاح"""
    print("🚀 بدء الإصلاح الشامل للنظام...")
    print("=" * 50)
    
    # إصلاح قاعدة البيانات
    if fix_database_issues():
        print("✅ تم إصلاح قاعدة البيانات")
    else:
        print("❌ فشل في إصلاح قاعدة البيانات")
    
    print("-" * 30)
    
    # إصلاح القوالب
    if fix_template_issues():
        print("✅ جميع القوالب سليمة")
    else:
        print("⚠️ هناك قوالب مفقودة")
    
    print("-" * 30)
    
    # إنشاء سكريبت الاختبار
    create_test_script()
    
    print("=" * 50)
    print("🎉 انتهى الإصلاح الشامل!")
    print("💡 يمكنك الآن تشغيل النظام باستخدام: python app.py")
    print("🧪 لاختبار النظام استخدم: python test_system.py")

if __name__ == '__main__':
    main()