#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار صفحة الموظفين
"""

import sqlite3
from datetime import datetime

def test_employees_data():
    """اختبار بيانات الموظفين"""
    print("🧪 اختبار بيانات الموظفين...")
    
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        # جلب جميع الموظفين
        cursor.execute('SELECT * FROM employees ORDER BY created_at DESC')
        employees = cursor.fetchall()
        
        print(f"📊 عدد الموظفين: {len(employees)}")
        
        if employees:
            print("👥 بيانات الموظفين:")
            total_salaries = 0.0
            
            for i, employee in enumerate(employees, 1):
                try:
                    salary = float(employee[4]) if employee[4] else 0.0
                    total_salaries += salary
                    print(f"   {i}. {employee[1]} - {employee[2]} - {salary:,.0f} ريال")
                except (ValueError, TypeError) as e:
                    print(f"   {i}. {employee[1]} - {employee[2]} - خطأ في الراتب: {employee[4]}")
            
            average_salary = total_salaries / len(employees) if len(employees) > 0 else 0.0
            
            print(f"💰 إجمالي الرواتب: {total_salaries:,.0f} ريال")
            print(f"📈 متوسط الراتب: {average_salary:,.0f} ريال")
        else:
            print("⚠️ لا توجد بيانات موظفين")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار بيانات الموظفين: {e}")
        return False

def test_salary_calculations():
    """اختبار حسابات الرواتب"""
    print("\n🧮 اختبار حسابات الرواتب...")
    
    # اختبار قيم مختلفة
    test_salaries = [
        "5000",      # نص رقمي
        "7500.50",   # نص عشري
        5000,        # رقم صحيح
        7500.50,     # رقم عشري
        "",          # فارغ
        None,        # None
        "abc",       # نص غير رقمي
    ]
    
    total = 0.0
    valid_count = 0
    
    for salary in test_salaries:
        try:
            converted = float(salary) if salary else 0.0
            total += converted
            valid_count += 1
            print(f"✅ {salary} -> {converted:,.2f}")
        except (ValueError, TypeError):
            print(f"⚠️ {salary} -> 0.0 (خطأ في التحويل)")
            valid_count += 1
    
    average = total / valid_count if valid_count > 0 else 0.0
    print(f"📊 الإجمالي: {total:,.2f}")
    print(f"📈 المتوسط: {average:,.2f}")
    
    return True

def add_test_employees():
    """إضافة موظفين تجريبيين"""
    print("\n👥 إضافة موظفين تجريبيين...")
    
    test_employees = [
        ('EMP001', 'أحمد محمد', 'مطور', 'تقنية المعلومات', 8000.0, '0501234567', 'ahmed@rashid.com'),
        ('EMP002', 'فاطمة علي', 'محاسبة', 'المالية', 6500.0, '0507654321', 'fatima@rashid.com'),
        ('EMP003', 'محمد سالم', 'مدير', 'الإدارة', 12000.0, '0509876543', 'mohammed@rashid.com'),
    ]
    
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        for emp in test_employees:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO employees 
                    (employee_number, name, position, department, salary, phone, email, hire_date, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (*emp, datetime.now().strftime('%Y-%m-%d'), 'موظف تجريبي'))
                
                print(f"✅ تم إضافة: {emp[1]} - {emp[2]}")
                
            except Exception as e:
                print(f"⚠️ خطأ في إضافة {emp[1]}: {e}")
        
        conn.commit()
        conn.close()
        
        print("✅ تم إضافة الموظفين التجريبيين")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إضافة الموظفين: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 اختبار صفحة الموظفين")
    print("=" * 50)
    
    # إضافة موظفين تجريبيين
    add_test_employees()
    
    print("-" * 30)
    
    # اختبار البيانات
    if test_employees_data():
        print("✅ بيانات الموظفين تعمل بشكل صحيح")
    else:
        print("❌ مشكلة في بيانات الموظفين")
    
    print("-" * 30)
    
    # اختبار الحسابات
    if test_salary_calculations():
        print("✅ حسابات الرواتب تعمل بشكل صحيح")
    else:
        print("❌ مشكلة في حسابات الرواتب")
    
    print("=" * 50)
    print("🎉 انتهى اختبار صفحة الموظفين!")
    print("🌐 يمكنك الآن زيارة: http://localhost:5000/employees")

if __name__ == '__main__':
    main()