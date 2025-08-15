#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
فحص سريع للنظام
"""

import os
import sys

def check_python():
    print("🐍 فحص Python...")
    print(f"   الإصدار: {sys.version}")
    if sys.version_info >= (3, 7):
        print("   ✅ إصدار Python مناسب")
        return True
    else:
        print("   ❌ يتطلب Python 3.7 أو أحدث")
        return False

def check_flask():
    print("\n📦 فحص Flask...")
    try:
        import flask
        print(f"   ✅ Flask متوفر - الإصدار: {flask.__version__}")
        return True
    except ImportError:
        print("   ❌ Flask غير مثبت")
        print("   💡 قم بتشغيل: pip install flask")
        return False

def check_files():
    print("\n📁 فحص الملفات الأساسية...")
    
    required_files = [
        'app.py',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - مفقود")
            all_exist = False
    
    return all_exist

def test_import():
    print("\n🔧 فحص استيراد التطبيق...")
    try:
        import app
        print("   ✅ يمكن استيراد app.py بنجاح")
        return True
    except Exception as e:
        print(f"   ❌ خطأ في استيراد app.py: {e}")
        return False

def main():
    print("=" * 50)
    print("🔍 فحص سريع للنظام")
    print("   RASHID INDUSTRIAL CO.")
    print("=" * 50)
    
    checks = [
        check_python(),
        check_flask(),
        check_files(),
        test_import()
    ]
    
    passed = sum(checks)
    total = len(checks)
    
    print("\n" + "=" * 50)
    print("📊 النتيجة النهائية:")
    print(f"   ✅ نجح: {passed}")
    print(f"   ❌ فشل: {total - passed}")
    print(f"   📈 المعدل: {(passed/total*100):.0f}%")
    
    if passed == total:
        print("\n🎉 النظام جاهز للتشغيل!")
        print("   يمكنك تشغيل النظام باستخدام:")
        print("   • تشغيل_بديل.bat")
        print("   • تشغيل_فوري.bat")
        print("   • python app.py")
    else:
        print(f"\n⚠️  يوجد {total - passed} مشكلة تحتاج إلى حل")
    
    print("=" * 50)

if __name__ == '__main__':
    main()
    input("\nاضغط Enter للخروج...")