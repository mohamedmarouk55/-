#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار تسجيل الدخول
RASHID INDUSTRIAL CO.
"""

import requests
import time

def test_login():
    """اختبار تسجيل الدخول"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 اختبار تسجيل الدخول...")
    
    try:
        # اختبار 1: الوصول للصفحة الرئيسية بدون تسجيل دخول
        print("1️⃣ اختبار الوصول للصفحة الرئيسية بدون تسجيل دخول...")
        response = requests.get(base_url, allow_redirects=False)
        if response.status_code == 302:
            print("✅ تم إعادة التوجيه بشكل صحيح (302)")
        else:
            print(f"❌ كود الاستجابة غير متوقع: {response.status_code}")
        
        # اختبار 2: الوصول لصفحة تسجيل الدخول
        print("2️⃣ اختبار الوصول لصفحة تسجيل الدخول...")
        response = requests.get(f"{base_url}/login")
        if response.status_code == 200:
            print("✅ صفحة تسجيل الدخول تعمل بشكل صحيح")
        else:
            print(f"❌ مشكلة في صفحة تسجيل الدخول: {response.status_code}")
        
        # اختبار 3: تسجيل دخول بالبيانات الصحيحة
        print("3️⃣ اختبار تسجيل الدخول بالبيانات الصحيحة...")
        session = requests.Session()
        
        # الحصول على صفحة تسجيل الدخول أولاً
        login_page = session.get(f"{base_url}/login")
        
        # إرسال بيانات تسجيل الدخول
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        
        if response.status_code == 302:
            print("✅ تم تسجيل الدخول بنجاح (إعادة توجيه)")
            
            # اختبار الوصول للصفحة الرئيسية بعد تسجيل الدخول
            main_page = session.get(base_url)
            if main_page.status_code == 200:
                print("✅ تم الوصول للصفحة الرئيسية بنجاح")
            else:
                print(f"❌ مشكلة في الوصول للصفحة الرئيسية: {main_page.status_code}")
        else:
            print(f"❌ فشل تسجيل الدخول: {response.status_code}")
        
        print("🎉 انتهى الاختبار")
        
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم. تأكد من تشغيل النظام على http://localhost:5000")
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 اختبار نظام تسجيل الدخول")
    print("RASHID INDUSTRIAL CO.")
    print("=" * 50)
    
    print("⚠️  تأكد من تشغيل النظام أولاً على http://localhost:5000")
    input("اضغط Enter للمتابعة...")
    
    test_login()
