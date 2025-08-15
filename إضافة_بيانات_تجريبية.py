#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
إضافة بيانات تجريبية للنظام المتعدد الشاشات
RASHID INDUSTRIAL CO.
"""

import sqlite3
from datetime import datetime, timedelta
import random

def add_sample_data():
    """إضافة بيانات تجريبية للنظام"""
    
    conn = sqlite3.connect('management_system.db')
    cursor = conn.cursor()
    
    print("🔄 إضافة بيانات تجريبية...")
    
    # 1. إضافة موظفين تجريبيين
    sample_employees = [
        ('E001', 'أحمد محمد الأحمد', 'مدير عام', 'الإدارة', 15000, '0501234567', 'ahmed@rashid.com', '2020-01-15', 'موظف متميز'),
        ('E002', 'فاطمة علي السعد', 'محاسبة رئيسية', 'المحاسبة', 8000, '0507654321', 'fatima@rashid.com', '2021-03-10', 'خبرة 5 سنوات'),
        ('E003', 'محمد سعد الغامدي', 'سائق', 'النقل', 4500, '0512345678', 'mohammed@rashid.com', '2022-06-01', 'رخصة قيادة عامة'),
        ('E004', 'نورا خالد العتيبي', 'مشرفة مبيعات', 'المبيعات', 7000, '0598765432', 'nora@rashid.com', '2021-09-15', 'مبيعات ممتازة'),
        ('E005', 'عبدالله أحمد القحطاني', 'فني صيانة', 'الصيانة', 5500, '0556789012', 'abdullah@rashid.com', '2020-11-20', 'خبرة تقنية عالية'),
    ]
    
    for emp in sample_employees:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO employees 
                (employee_number, name, position, department, salary, phone, email, hire_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', emp)
        except Exception as e:
            print(f"خطأ في إضافة الموظف {emp[1]}: {e}")
    
    print("✅ تم إضافة الموظفين التجريبيين")
    
    # 2. إضافة سيارات تجريبية
    sample_cars = [
        ('تويوتا', 'كامري', 2022, 'أ ب ج 1234', 'أبيض', 85000, 80000, 'ENG001', 'CHS001', 'سيارة إدارية'),
        ('هوندا', 'أكورد', 2021, 'د هـ و 5678', 'أسود', 75000, 70000, 'ENG002', 'CHS002', 'سيارة تنفيذية'),
        ('نيسان', 'التيما', 2023, 'ز ح ط 9012', 'فضي', 90000, 88000, 'ENG003', 'CHS003', 'سيارة جديدة'),
        ('هيونداي', 'سوناتا', 2020, 'ي ك ل 3456', 'أزرق', 65000, 55000, 'ENG004', 'CHS004', 'حالة ممتازة'),
        ('كيا', 'أوبتيما', 2021, 'م ن س 7890', 'أحمر', 70000, 65000, 'ENG005', 'CHS005', 'صيانة دورية'),
    ]
    
    for car in sample_cars:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO cars 
                (brand, model, year, license_plate, color, purchase_price, current_value, engine_number, chassis_number, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', car)
        except Exception as e:
            print(f"خطأ في إضافة السيارة {car[0]} {car[1]}: {e}")
    
    print("✅ تم إضافة السيارات التجريبية")
    
    # 3. إضافة معاملات خزينة تجريبية
    today = datetime.now()
    treasury_transactions = []
    
    # إيداعات
    deposits = [
        (50000, 'إيداع رأس المال الأولي', 'REF001'),
        (25000, 'إيراد من المبيعات', 'REF002'),
        (15000, 'إيراد خدمات', 'REF003'),
        (30000, 'إيداع شهري', 'REF004'),
    ]
    
    balance = 0
    for i, (amount, desc, ref) in enumerate(deposits):
        date = (today - timedelta(days=30-i*7)).strftime('%Y-%m-%d')
        balance += amount
        treasury_transactions.append(('إيداع', amount, desc, ref, 'admin', date, balance))
    
    # سحوبات
    withdrawals = [
        (5000, 'رواتب الموظفين', 'REF005'),
        (3000, 'مصاريف تشغيلية', 'REF006'),
        (2000, 'صيانة السيارات', 'REF007'),
        (1500, 'مصاريف إدارية', 'REF008'),
    ]
    
    for i, (amount, desc, ref) in enumerate(withdrawals):
        date = (today - timedelta(days=20-i*3)).strftime('%Y-%m-%d')
        balance -= amount
        treasury_transactions.append(('سحب', amount, desc, ref, 'admin', date, balance))
    
    for trans in treasury_transactions:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO treasury 
                (transaction_type, amount, description, reference_number, created_by, date, balance_after)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', trans)
        except Exception as e:
            print(f"خطأ في إضافة معاملة الخزينة: {e}")
    
    print("✅ تم إضافة معاملات الخزينة التجريبية")
    
    # 4. إضافة مصروفات تجريبية
    sample_expenses = [
        ('تشغيلي', 'وقود', 2500, 'وقود السيارات الشهري', 'REC001', (today - timedelta(days=5)).strftime('%Y-%m-%d'), 'admin'),
        ('صيانة', 'قطع غيار', 1800, 'قطع غيار سيارة كامري', 'REC002', (today - timedelta(days=10)).strftime('%Y-%m-%d'), 'admin'),
        ('إداري', 'قرطاسية', 500, 'مواد مكتبية متنوعة', 'REC003', (today - timedelta(days=15)).strftime('%Y-%m-%d'), 'admin'),
        ('تشغيلي', 'تأمين', 3000, 'تأمين السيارات السنوي', 'REC004', (today - timedelta(days=20)).strftime('%Y-%m-%d'), 'admin'),
        ('صيانة', 'إطارات', 2200, 'إطارات جديدة للسيارات', 'REC005', (today - timedelta(days=25)).strftime('%Y-%m-%d'), 'admin'),
    ]
    
    for expense in sample_expenses:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO expenses 
                (expense_type, category, amount, description, receipt_number, date, approved_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', expense)
        except Exception as e:
            print(f"خطأ في إضافة المصروف: {e}")
    
    print("✅ تم إضافة المصروفات التجريبية")
    
    # 5. إضافة عهد سيارات تجريبية
    # الحصول على IDs الموظفين والسيارات
    cursor.execute('SELECT id, employee_number FROM employees LIMIT 3')
    employees = cursor.fetchall()
    
    cursor.execute('SELECT id FROM cars LIMIT 3')
    cars = cursor.fetchall()
    
    if employees and cars:
        custody_records = [
            (employees[0][0], employees[0][1], cars[0][0], (today - timedelta(days=30)).strftime('%Y-%m-%d'), 
             (today + timedelta(days=60)).strftime('%Y-%m-%d'), 'عهدة سيارة إدارية', 'نشط'),
            (employees[1][0], employees[1][1], cars[1][0], (today - timedelta(days=20)).strftime('%Y-%m-%d'), 
             (today + timedelta(days=70)).strftime('%Y-%m-%d'), 'عهدة سيارة تنفيذية', 'نشط'),
            (employees[2][0], employees[2][1], cars[2][0], (today - timedelta(days=45)).strftime('%Y-%m-%d'), 
             (today - timedelta(days=5)).strftime('%Y-%m-%d'), 'عهدة سيارة مُسلمة', 'مُسلم'),
        ]
        
        for custody in custody_records:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO car_custody 
                    (employee_id, employee_number, car_id, custody_date, expected_return, notes, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', custody)
                
                # تحديث حالة السيارة
                if custody[6] == 'نشط':
                    cursor.execute('UPDATE cars SET status = "مستأجر" WHERE id = ?', (custody[2],))
                
            except Exception as e:
                print(f"خطأ في إضافة عهدة السيارة: {e}")
        
        print("✅ تم إضافة عهد السيارات التجريبية")
    
    # 6. إضافة سجلات مالية تجريبية
    financial_records = [
        ('إيراد', 'مبيعات', 45000, 'إيرادات المبيعات الشهرية', (today - timedelta(days=10)).strftime('%Y-%m-%d')),
        ('إيراد', 'خدمات', 15000, 'إيرادات الخدمات', (today - timedelta(days=15)).strftime('%Y-%m-%d')),
        ('مصروف', 'رواتب', 25000, 'رواتب الموظفين', (today - timedelta(days=5)).strftime('%Y-%m-%d')),
        ('مصروف', 'تشغيل', 8000, 'مصاريف تشغيلية متنوعة', (today - timedelta(days=8)).strftime('%Y-%m-%d')),
    ]
    
    for record in financial_records:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO financial_records 
                (type, category, amount, description, date)
                VALUES (?, ?, ?, ?, ?)
            ''', record)
        except Exception as e:
            print(f"خطأ في إضافة السجل المالي: {e}")
    
    print("✅ تم إضافة السجلات المالية التجريبية")
    
    # حفظ التغييرات
    conn.commit()
    conn.close()
    
    print("\n🎉 تم إضافة جميع البيانات التجريبية بنجاح!")
    print("\n📊 ملخص البيانات المضافة:")
    print("   👥 5 موظفين")
    print("   🚗 5 سيارات") 
    print("   💰 8 معاملات خزينة")
    print("   💸 5 مصروفات")
    print("   📋 3 عهد سيارات")
    print("   📈 4 سجلات مالية")
    print("\n✨ النظام جاهز للاستخدام مع البيانات التجريبية!")

if __name__ == '__main__':
    add_sample_data()