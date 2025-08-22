#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار صفحة الخزينة
"""

import sqlite3
from datetime import datetime

def test_treasury_database():
    """اختبار قاعدة بيانات الخزينة"""
    print("🔍 اختبار قاعدة بيانات الخزينة...")
    
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        # فحص وجود جدول الخزينة
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='treasury'")
        if cursor.fetchone():
            print("✅ جدول الخزينة موجود")
        else:
            print("❌ جدول الخزينة غير موجود")
            return False
        
        # فحص البيانات
        cursor.execute("SELECT COUNT(*) FROM treasury")
        count = cursor.fetchone()[0]
        print(f"📊 عدد المعاملات: {count}")
        
        # فحص الإحصائيات
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"')
        total_deposits = cursor.fetchone()[0]
        print(f"💰 إجمالي الإيداعات: {total_deposits:,.2f} ريال")
        
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "سحب"')
        total_withdrawals = cursor.fetchone()[0]
        print(f"💸 إجمالي السحوبات: {total_withdrawals:,.2f} ريال")
        
        cursor.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1')
        current_balance_row = cursor.fetchone()
        current_balance = current_balance_row[0] if current_balance_row else 0
        print(f"🏦 الرصيد الحالي: {current_balance:,.2f} ريال")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")
        return False

def add_test_transaction():
    """إضافة معاملة تجريبية"""
    print("\n🔧 إضافة معاملة تجريبية...")
    
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        # الحصول على الرصيد الحالي
        cursor.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1')
        current_balance_row = cursor.fetchone()
        current_balance = current_balance_row[0] if current_balance_row else 0
        
        # إضافة معاملة إيداع تجريبية
        test_amount = 1000
        new_balance = current_balance + test_amount
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            INSERT INTO treasury (transaction_type, amount, description, reference_number, created_by, date, balance_after)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('إيداع', test_amount, 'معاملة تجريبية للاختبار', 'TEST001', 'admin', today, new_balance))
        
        conn.commit()
        conn.close()
        
        print(f"✅ تم إضافة معاملة إيداع بمبلغ {test_amount:,.0f} ريال")
        print(f"💰 الرصيد الجديد: {new_balance:,.2f} ريال")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إضافة المعاملة: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🧪 اختبار صفحة الخزينة")
    print("=" * 40)
    
    # اختبار قاعدة البيانات
    if test_treasury_database():
        print("✅ قاعدة بيانات الخزينة تعمل بشكل صحيح")
    else:
        print("❌ مشكلة في قاعدة بيانات الخزينة")
        return
    
    # إضافة معاملة تجريبية
    add_test_transaction()
    
    print("\n" + "=" * 40)
    print("🎉 انتهى اختبار الخزينة!")
    print("💡 يمكنك الآن الذهاب لصفحة الخزينة في المتصفح")

if __name__ == '__main__':
    main()