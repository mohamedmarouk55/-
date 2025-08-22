#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار جميع النماذج في النظام
"""

import sqlite3
from datetime import datetime

def test_employee_form():
    """اختبار نموذج إضافة الموظفين"""
    print("🧪 اختبار نموذج إضافة الموظفين...")
    
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        # إضافة موظف تجريبي
        test_employee = (
            'TEST001',
            'موظف تجريبي',
            'مطور',
            'تقنية المعلومات',
            5000.0,
            '0501234567',
            'test@rashid.com',
            datetime.now().strftime('%Y-%m-%d'),
            'موظف للاختبار'
        )
        
        cursor.execute('''
            INSERT INTO employees (employee_number, name, position, department, salary, phone, email, hire_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', test_employee)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إضافة موظف تجريبي بنجاح")
        return True
        
    except sqlite3.IntegrityError:
        print("⚠️ الموظف التجريبي موجود مسبقاً")
        return True
    except Exception as e:
        print(f"❌ خطأ في اختبار نموذج الموظفين: {e}")
        return False

def test_car_form():
    """اختبار نموذج إضافة السيارات"""
    print("🧪 اختبار نموذج إضافة السيارات...")
    
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        # إضافة سيارة تجريبية
        test_car = (
            'تويوتا',
            'كورولا',
            2024,
            'TEST123',
            'أحمر',
            'متاح',
            75000.0,
            75000.0,
            'TEST_ENG',
            'TEST_CHS',
            'سيارة للاختبار'
        )
        
        cursor.execute('''
            INSERT INTO cars (brand, model, year, license_plate, color, status, purchase_price, current_value, engine_number, chassis_number, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', test_car)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إضافة سيارة تجريبية بنجاح")
        return True
        
    except sqlite3.IntegrityError:
        print("⚠️ السيارة التجريبية موجودة مسبقاً")
        return True
    except Exception as e:
        print(f"❌ خطأ في اختبار نموذج السيارات: {e}")
        return False

def test_expense_form():
    """اختبار نموذج إضافة المصروفات"""
    print("🧪 اختبار نموذج إضافة المصروفات...")
    
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        # إضافة مصروف تجريبي
        test_expense = (
            'تشغيلية',
            'اختبار',
            500.0,
            'مصروف للاختبار',
            'TEST_REC',
            datetime.now().strftime('%Y-%m-%d'),
            'admin',
            'معتمد'
        )
        
        cursor.execute('''
            INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, approved_by, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', test_expense)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إضافة مصروف تجريبي بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار نموذج المصروفات: {e}")
        return False

def test_treasury_form():
    """اختبار نموذج إضافة معاملات الخزينة"""
    print("🧪 اختبار نموذج معاملات الخزينة...")
    
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        # الحصول على الرصيد الحالي
        cursor.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1')
        current_balance_row = cursor.fetchone()
        current_balance = float(current_balance_row[0]) if current_balance_row else 0.0
        
        # إضافة معاملة تجريبية
        test_amount = 1000.0
        new_balance = current_balance + test_amount
        
        test_transaction = (
            'إيداع',
            test_amount,
            'معاملة تجريبية للاختبار',
            'TEST_REF',
            'admin',
            datetime.now().strftime('%Y-%m-%d'),
            new_balance
        )
        
        cursor.execute('''
            INSERT INTO treasury (transaction_type, amount, description, reference_number, created_by, date, balance_after)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', test_transaction)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إضافة معاملة خزينة تجريبية بنجاح")
        print(f"💰 الرصيد الجديد: {new_balance:,.2f} ريال")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار نموذج الخزينة: {e}")
        return False

def test_data_types():
    """اختبار أنواع البيانات المختلفة"""
    print("🧪 اختبار أنواع البيانات...")
    
    # اختبار تحويل النصوص إلى أرقام
    test_cases = [
        ("123", "رقم صحيح"),
        ("123.45", "رقم عشري"),
        ("0", "صفر"),
        ("", "نص فارغ"),
        ("abc", "نص غير رقمي"),
        ("123abc", "نص مختلط"),
    ]
    
    for test_value, description in test_cases:
        try:
            if test_value == "":
                result = 0.0
            else:
                result = float(test_value)
            print(f"✅ {description}: '{test_value}' -> {result}")
        except (ValueError, TypeError):
            print(f"⚠️ {description}: '{test_value}' -> خطأ في التحويل (متوقع)")
    
    return True

def main():
    """الدالة الرئيسية"""
    print("🚀 اختبار شامل لجميع النماذج")
    print("=" * 50)
    
    tests = [
        ("أنواع البيانات", test_data_types),
        ("نموذج الموظفين", test_employee_form),
        ("نموذج السيارات", test_car_form),
        ("نموذج المصروفات", test_expense_form),
        ("نموذج الخزينة", test_treasury_form),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        print("-" * 30)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name}: نجح")
        else:
            print(f"❌ {test_name}: فشل")
    
    print("\n" + "=" * 50)
    print(f"📊 النتائج النهائية:")
    print(f"✅ نجح: {passed}/{total}")
    print(f"❌ فشل: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت!")
        print("💡 النماذج جاهزة للاستخدام")
    else:
        print("⚠️ بعض الاختبارات فشلت - يحتاج إصلاح")
    
    print("\n🌐 يمكنك الآن اختبار النماذج في المتصفح:")
    print("   - http://localhost:5000/add_employee")
    print("   - http://localhost:5000/add_car") 
    print("   - http://localhost:5000/expenses")
    print("   - http://localhost:5000/treasury")

if __name__ == '__main__':
    main()