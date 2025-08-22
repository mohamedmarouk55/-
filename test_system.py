#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت اختبار شامل للنظام
"""

import requests
import time

def test_system():
    """اختبار النظام"""
    base_url = 'http://localhost:5000'
    
    print("🧪 بدء اختبار النظام...")
    
    # اختبار الصفحة الرئيسية
    try:
        response = requests.get(f'{base_url}/')
        if response.status_code == 200 or response.status_code == 302:
            print("✅ الصفحة الرئيسية تعمل")
        else:
            print(f"❌ مشكلة في الصفحة الرئيسية: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False
    
    # اختبار صفحات أخرى
    pages_to_test = [
        '/login',
        '/treasury', 
        '/cars',
        '/employees',
        '/expenses',
        '/reports',
        '/settings'
    ]
    
    for page in pages_to_test:
        try:
            response = requests.get(f'{base_url}{page}')
            if response.status_code in [200, 302, 401]:  # 401 للصفحات المحمية
                print(f"✅ صفحة {page} تعمل")
            else:
                print(f"❌ مشكلة في صفحة {page}: {response.status_code}")
        except Exception as e:
            print(f"❌ خطأ في صفحة {page}: {e}")
    
    print("🎉 انتهى الاختبار!")
    return True

if __name__ == '__main__':
    test_system()
