#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت اختبار بيانات التحليلات
للتحقق من وجود المصروفات وباقي البيانات
"""

import sqlite3
import os
from datetime import datetime

def test_analytics_data():
    """اختبار بيانات التحليلات"""
    
    # مسار قاعدة البيانات
    db_path = 'management_system.db'
    
    if not os.path.exists(db_path):
        print("❌ قاعدة البيانات غير موجودة!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("🔧 بدء اختبار بيانات التحليلات...")
        print("=" * 50)
        
        # فحص المصروفات
        print("1️⃣ فحص جدول المصروفات:")
        cursor.execute("SELECT COUNT(*) as count FROM expenses")
        expenses_count = cursor.fetchone()['count']
        print(f"   📊 عدد المصروفات: {expenses_count}")
        
        if expenses_count > 0:
            cursor.execute("SELECT * FROM expenses ORDER BY created_at DESC LIMIT 3")
            recent_expenses = cursor.fetchall()
            print("   📋 آخر 3 مصروفات:")
            for i, expense in enumerate(recent_expenses, 1):
                print(f"     {i}. ID: {expense['id']}")
                print(f"        النوع: {expense['expense_type']}")
                print(f"        الفئة: {expense['category']}")
                print(f"        المبلغ: {expense['amount']}")
                print(f"        التاريخ: {expense['date']}")
                print(f"        الوصف: {expense['description']}")
                print(f"        تاريخ الإنشاء: {expense['created_at']}")
                print()
        
        # فحص الخزينة
        print("2️⃣ فحص جدول الخزينة:")
        cursor.execute("SELECT COUNT(*) as count FROM treasury")
        treasury_count = cursor.fetchone()['count']
        print(f"   📊 عدد حركات الخزينة: {treasury_count}")
        
        # فحص الموظفين
        print("3️⃣ فحص جدول الموظفين:")
        cursor.execute("SELECT COUNT(*) as count FROM employees")
        employees_count = cursor.fetchone()['count']
        print(f"   📊 عدد الموظفين: {employees_count}")
        
        # فحص السيارات
        print("4️⃣ فحص جدول السيارات:")
        cursor.execute("SELECT COUNT(*) as count FROM cars")
        cars_count = cursor.fetchone()['count']
        print(f"   📊 عدد السيارات: {cars_count}")
        
        # فحص عمليات التسليم
        print("5️⃣ فحص جدول التسليم:")
        cursor.execute("SELECT COUNT(*) as count FROM handovers")
        handovers_count = cursor.fetchone()['count']
        print(f"   📊 عدد عمليات التسليم: {handovers_count}")
        
        print("=" * 50)
        
        # محاكاة استعلام التحليلات للمصروفات
        print("🔍 محاكاة استعلام المصروفات في التحليلات:")
        expenses_query = '''
            SELECT 
                date, created_at, amount, description, category, car_id, employee_id, expense_type,
                'expenses' as source_type
            FROM expenses 
            WHERE 1=1
            ORDER BY created_at DESC
        '''
        
        cursor.execute(expenses_query)
        expenses_for_analytics = cursor.fetchall()
        
        print(f"📊 عدد المصروفات المسترجعة للتحليلات: {len(expenses_for_analytics)}")
        
        if len(expenses_for_analytics) > 0:
            print("📋 أول 3 مصروفات للتحليلات:")
            for i, expense in enumerate(expenses_for_analytics[:3], 1):
                print(f"  {i}. {expense['expense_type']} - {expense['description']} - {expense['amount']} ريال")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار البيانات: {e}")
        import traceback
        traceback.print_exc()
        return False

def add_test_expense():
    """إضافة مصروف اختباري"""
    
    db_path = 'management_system.db'
    
    if not os.path.exists(db_path):
        print("❌ قاعدة البيانات غير موجودة!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("➕ إضافة مصروف اختباري...")
        
        # بيانات اختبارية
        test_expense = {
            'expense_type': 'تشغيلي',
            'category': 'الوقود',
            'amount': 250.75,
            'description': 'تعبئة وقود للسيارة - اختبار التحليلات',
            'receipt_number': 'TEST-001',
            'date': '2024-01-20',
            'car_id': None,
            'employee_id': None,
            'approved_by': 'admin'
        }
        
        cursor.execute('''
            INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, car_id, employee_id, approved_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_expense['expense_type'],
            test_expense['category'],
            test_expense['amount'],
            test_expense['description'],
            test_expense['receipt_number'],
            test_expense['date'],
            test_expense['car_id'],
            test_expense['employee_id'],
            test_expense['approved_by']
        ))
        
        conn.commit()
        expense_id = cursor.lastrowid
        print(f"✅ تم إضافة المصروف الاختباري! ID: {expense_id}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إضافة المصروف الاختباري: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🔧 سكريبت اختبار بيانات التحليلات")
    print("=" * 60)
    
    # اختبار البيانات الحالية
    data_ok = test_analytics_data()
    
    if data_ok:
        print("\n" + "=" * 60)
        print("✅ تم فحص البيانات بنجاح!")
        
        # إضافة مصروف اختباري إذا لم توجد مصروفات
        print("\n🔄 إضافة مصروف اختباري للتأكد من عمل التحليلات...")
        add_test_expense()
        
        print("\n🔄 إعادة فحص البيانات بعد الإضافة...")
        test_analytics_data()
        
    else:
        print("❌ فشل في فحص البيانات!")
    
    print("=" * 60)