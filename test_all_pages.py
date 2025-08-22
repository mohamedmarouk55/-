#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار جميع صفحات النظام
"""

import requests
import time

def test_page(url, page_name):
    """اختبار صفحة واحدة"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {page_name}: يعمل بشكل صحيح")
            return True
        else:
            print(f"⚠️ {page_name}: كود الاستجابة {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {page_name}: خطأ في الاتصال - {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🧪 اختبار جميع صفحات النظام")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # قائمة الصفحات للاختبار
    pages = [
        ("/", "الصفحة الرئيسية"),
        ("/login", "صفحة تسجيل الدخول"),
        ("/employees", "صفحة الموظفين"),
        ("/add_employee", "إضافة موظف"),
        ("/cars", "صفحة السيارات"),
        ("/add_car", "إضافة سيارة"),
        ("/treasury", "صفحة الخزينة"),
        ("/expenses", "صفحة المصروفات"),
        ("/settings", "صفحة الإعدادات"),
        ("/reports", "صفحة التقارير"),
    ]
    
    print("⏳ انتظار تشغيل الخادم...")
    time.sleep(3)
    
    successful_tests = 0
    total_tests = len(pages)
    
    for path, name in pages:
        url = base_url + path
        if test_page(url, name):
            successful_tests += 1
        time.sleep(0.5)  # انتظار قصير بين الاختبارات
    
    print("-" * 50)
    print(f"📊 نتائج الاختبار:")
    print(f"✅ نجح: {successful_tests}/{total_tests}")
    print(f"❌ فشل: {total_tests - successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print("🎉 جميع الصفحات تعمل بشكل صحيح!")
    else:
        print("⚠️ بعض الصفحات تحتاج إلى مراجعة")
    
    print("=" * 50)
    print("🌐 يمكنك زيارة النظام على: http://localhost:5000")
    print("👤 اسم المستخدم: admin")
    print("🔑 كلمة المرور: admin123")

if __name__ == '__main__':
    main()