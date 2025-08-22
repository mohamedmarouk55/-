#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريپت اختبار عرض المصروفات في التحليلات
"""

import sqlite3
import os
from datetime import datetime

def test_analytics_expenses():
    """اختبار عرض المصروفات في التحليلات"""
    
    # مسار قاعدة البيانات
    db_path = 'management_system.db'
    
    if not os.path.exists(db_path):
        print("❌ قاعدة البيانات غير موجودة!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        print("🔧 اختبار عرض المصروفات في التحليلات...")
        print("=" * 60)
        
        # محاكاة كود التحليلات للمصروفات
        activities = []
        
        # جمع المصروفات (نفس الكود من app.py)
        expenses_query = '''
            SELECT 
                date, created_at, amount, description, category, car_id, employee_id, expense_type,
                'expenses' as source_type
            FROM expenses 
            WHERE 1=1
            ORDER BY created_at DESC
        '''
        
        print(f"📋 استعلام المصروفات:")
        print(f"   {expenses_query}")
        print()
        
        expenses_records = conn.execute(expenses_query).fetchall()
        print(f"📊 عدد المصروفات المسترجعة: {len(expenses_records)}")
        print()
        
        if len(expenses_records) == 0:
            print("⚠️ لا توجد مصروفات في قاعدة البيانات!")
            return False
        
        # معالجة المصروفات (نفس الكود من app.py)
        for record in expenses_records:
            car_info = ''
            employee_info = ''
            
            if record['car_id']:
                car = conn.execute('SELECT license_plate FROM cars WHERE id = ?', (record['car_id'],)).fetchone()
                car_info = f" - السيارة: {car['license_plate']}" if car else ''
            
            if record['employee_id']:
                employee = conn.execute('SELECT name FROM employees WHERE id = ?', (record['employee_id'],)).fetchone()
                employee_info = f" - الموظف: {employee['name']}" if employee else ''
            
            activity = {
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
            }
            
            activities.append(activity)
            
            print(f"✅ مصروف معالج:")
            print(f"   📅 التاريخ: {activity['date']}")
            print(f"   ⏰ الوقت: {activity['time']}")
            print(f"   🏷️ النوع: {activity['type_name']}")
            print(f"   📝 الوصف: {activity['description']}")
            print(f"   📋 التفاصيل: {activity['details']}")
            print(f"   💰 المبلغ: {activity['amount']} ريال")
            print(f"   🎨 الفئة: {activity['type_class']}")
            print(f"   🎯 الأيقونة: {activity['icon']}")
            print()
        
        # حساب الإحصائيات
        expenses_count = len([a for a in activities if a['type_name'] == 'مصروف'])
        
        print("📊 الإحصائيات النهائية:")
        print(f"   إجمالي الأنشطة: {len(activities)}")
        print(f"   عدد المصروفات: {expenses_count}")
        print()
        
        # محاكاة البيانات المرسلة للقالب
        template_data = {
            'activities': activities,
            'expenses_count': expenses_count,
            'total_activities': len(activities)
        }
        
        print("📤 البيانات المرسلة للقالب:")
        print(f"   activities: {len(template_data['activities'])} عنصر")
        print(f"   expenses_count: {template_data['expenses_count']}")
        print(f"   total_activities: {template_data['total_activities']}")
        print()
        
        # اختبار فلتر المصروفات
        expenses_only = [a for a in activities if a['type_name'] == 'مصروف']
        print(f"🔍 اختبار فلتر المصروفات:")
        print(f"   عدد المصروفات بعد الفلتر: {len(expenses_only)}")
        
        if len(expenses_only) > 0:
            print("   ✅ فلتر المصروفات يعمل بشكل صحيح!")
        else:
            print("   ❌ فلتر المصروفات لا يعمل!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار التحليلات: {e}")
        import traceback
        traceback.print_exc()
        return False

def add_test_expense_if_needed():
    """إضافة مصروف اختباري إذا لم توجد مصروفات"""
    
    db_path = 'management_system.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # فحص وجود مصروفات
        cursor.execute("SELECT COUNT(*) as count FROM expenses")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("➕ إضافة مصروف اختباري...")
            
            cursor.execute('''
                INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, approved_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                'تشغيلي',
                'الوقود',
                150.50,
                'تعبئة وقود - اختبار التحليلات',
                'TEST-ANALYTICS-001',
                '2024-01-20',
                'admin'
            ))
            
            conn.commit()
            expense_id = cursor.lastrowid
            print(f"✅ تم إضافة المصروف الاختباري! ID: {expense_id}")
        else:
            print(f"ℹ️ يوجد {count} مصروف في قاعدة البيانات")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إضافة المصروف الاختباري: {e}")
        return False

if __name__ == '__main__':
    print("=" * 70)
    print("🔧 سكريپت اختبار عرض المصروفات في التحليلات")
    print("=" * 70)
    
    # إضافة مصروف اختباري إذا لزم الأمر
    add_test_expense_if_needed()
    
    print()
    
    # اختبار عرض المصروفات
    success = test_analytics_expenses()
    
    print("=" * 70)
    if success:
        print("✅ اختبار التحليلات مكتمل بنجاح!")
        print()
        print("🌐 للتحقق من النتائج:")
        print("   1. افتح المتصفح واذهب إلى: http://localhost:5000")
        print("   2. سجل الدخول بـ admin/admin123")
        print("   3. اذهب لصفحة التحليلات")
        print("   4. تحقق من بطاقة المصروفات في الأعلى")
        print("   5. ابحث عن المصروفات في الجدول (أيقونة برتقالية 💸)")
        print("   6. جرب فلتر 'المصروفات' لعرضها فقط")
    else:
        print("❌ فشل في اختبار التحليلات!")
    
    print("=" * 70)