#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت تحديث جدول المصروفات
إضافة أعمدة car_id و employee_id
"""

import sqlite3
import os

def update_expenses_table():
    """تحديث جدول المصروفات لإضافة الأعمدة المفقودة"""
    
    # مسار قاعدة البيانات
    db_path = 'management_system.db'
    
    if not os.path.exists(db_path):
        print("❌ قاعدة البيانات غير موجودة!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 بدء تحديث جدول المصروفات...")
        
        # التحقق من وجود الأعمدة
        cursor.execute("PRAGMA table_info(expenses)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"📋 الأعمدة الحالية: {columns}")
        
        # إضافة عمود car_id إذا لم يكن موجوداً
        if 'car_id' not in columns:
            print("➕ إضافة عمود car_id...")
            cursor.execute('ALTER TABLE expenses ADD COLUMN car_id INTEGER')
            print("✅ تم إضافة عمود car_id")
        else:
            print("✅ عمود car_id موجود بالفعل")
        
        # إضافة عمود employee_id إذا لم يكن موجوداً
        if 'employee_id' not in columns:
            print("➕ إضافة عمود employee_id...")
            cursor.execute('ALTER TABLE expenses ADD COLUMN employee_id INTEGER')
            print("✅ تم إضافة عمود employee_id")
        else:
            print("✅ عمود employee_id موجود بالفعل")
        
        # حفظ التغييرات
        conn.commit()
        print("💾 تم حفظ التغييرات")
        
        # التحقق من النتيجة النهائية
        cursor.execute("PRAGMA table_info(expenses)")
        updated_columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 الأعمدة بعد التحديث: {updated_columns}")
        
        conn.close()
        print("🎉 تم تحديث جدول المصروفات بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحديث الجدول: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("🔧 سكريبت تحديث جدول المصروفات")
    print("=" * 50)
    
    success = update_expenses_table()
    
    print("=" * 50)
    if success:
        print("✅ تم التحديث بنجاح!")
        print("🚀 يمكنك الآن تشغيل النظام بدون مشاكل")
    else:
        print("❌ فشل في التحديث!")
        print("🔧 يرجى التحقق من الأخطاء أعلاه")
    print("=" * 50)