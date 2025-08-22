#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت اختبار إضافة المصروفات
للتحقق من وجود أي أخطاء في قاعدة البيانات
"""

import sqlite3
import os
from datetime import datetime

def test_add_expense():
    """اختبار إضافة مصروف جديد"""
    
    # مسار قاعدة البيانات
    db_path = 'management_system.db'
    
    if not os.path.exists(db_path):
        print("❌ قاعدة البيانات غير موجودة!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("🔧 بدء اختبار إضافة المصروف...")
        
        # بيانات اختبارية
        test_data = {
            'expense_type': 'تشغيلي',
            'category': 'الوقود',
            'amount': 150.50,
            'description': 'تعبئة وقود للسيارة',
            'receipt_number': 'REC-001',
            'date': '2024-01-15',
            'car_id': None,
            'employee_id': None,
            'approved_by': 'admin'
        }
        
        print(f"📋 البيانات الاختبارية: {test_data}")
        
        # محاولة الإدراج
        cursor.execute('''
            INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, car_id, employee_id, approved_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_data['expense_type'],
            test_data['category'],
            test_data['amount'],
            test_data['description'],
            test_data['receipt_number'],
            test_data['date'],
            test_data['car_id'],
            test_data['employee_id'],
            test_data['approved_by']
        ))
        
        conn.commit()
        expense_id = cursor.lastrowid
        print(f"✅ تم إضافة المصروف بنجاح! ID: {expense_id}")
        
        # التحقق من الإدراج
        cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
        expense = cursor.fetchone()
        
        if expense:
            print("📊 بيانات المصروف المضاف:")
            for key in expense.keys():
                print(f"  {key}: {expense[key]}")
        
        # حذف البيانات الاختبارية
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        print("🗑️ تم حذف البيانات الاختبارية")
        
        conn.close()
        print("🎉 اختبار إضافة المصروف نجح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار إضافة المصروف: {e}")
        print(f"نوع الخطأ: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def check_database_structure():
    """فحص بنية قاعدة البيانات"""
    
    db_path = 'management_system.db'
    
    if not os.path.exists(db_path):
        print("❌ قاعدة البيانات غير موجودة!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 فحص بنية جدول المصروفات...")
        
        # فحص الأعمدة
        cursor.execute("PRAGMA table_info(expenses)")
        columns = cursor.fetchall()
        
        print("📋 أعمدة الجدول:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - Default: {col[4]}")
        
        # فحص عدد السجلات
        cursor.execute("SELECT COUNT(*) FROM expenses")
        count = cursor.fetchone()[0]
        print(f"📊 عدد المصروفات الحالية: {count}")
        
        # فحص آخر 3 مصروفات
        if count > 0:
            cursor.execute("SELECT * FROM expenses ORDER BY created_at DESC LIMIT 3")
            recent_expenses = cursor.fetchall()
            print("📋 آخر 3 مصروفات:")
            for i, expense in enumerate(recent_expenses, 1):
                print(f"  {i}. ID: {expense[0]}, النوع: {expense[1]}, المبلغ: {expense[3]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🔧 سكريبت اختبار إضافة المصروفات")
    print("=" * 60)
    
    # فحص بنية قاعدة البيانات
    print("\n1️⃣ فحص بنية قاعدة البيانات:")
    db_ok = check_database_structure()
    
    if db_ok:
        print("\n2️⃣ اختبار إضافة مصروف:")
        test_ok = test_add_expense()
        
        print("\n" + "=" * 60)
        if test_ok:
            print("✅ جميع الاختبارات نجحت!")
            print("🚀 يمكن إضافة المصروفات بدون مشاكل")
        else:
            print("❌ فشل في اختبار إضافة المصروف!")
            print("🔧 يرجى مراجعة الأخطاء أعلاه")
    else:
        print("❌ مشكلة في بنية قاعدة البيانات!")
    
    print("=" * 60)