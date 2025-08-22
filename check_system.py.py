#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
فحص النظام - RASHID INDUSTRIAL CO.
التحقق من سلامة جميع مكونات النظام
"""

import os
import sys
import sqlite3
from datetime import datetime

def print_header():
    """طباعة رأس البرنامج"""
    print("=" * 70)
    print("🔍 فحص النظام - RASHID INDUSTRIAL CO.")
    print("=" * 70)
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

def check_python():
    """التحقق من إصدار Python"""
    print("🐍 فحص Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - مدعوم")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - غير مدعوم")
        print("   📥 يرجى تثبيت Python 3.7 أو أحدث")
        return False

def check_modules():
    """التحقق من المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات...")
    required_modules = [
        'flask',
        'werkzeug', 
        'jinja2',
        'markupsafe',
        'itsdangerous',
        'click',
        'blinker'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - مفقود")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n   📥 لتثبيت المكتبات المفقودة:")
        print(f"   pip install {' '.join(missing_modules)}")
        return False
    
    return True

def check_files():
    """التحقق من الملفات المطلوبة"""
    print("\n📁 فحص الملفات...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/login.html',
        'templates/base.html',
        'templates/index.html',
        'templates/employees.html',
        'templates/add_employee.html',
        'templates/cars.html',
        'templates/add_car.html',
        'templates/financial.html',
        'templates/add_financial.html',
        'static/css/custom.css',
        'static/js/main.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - مفقود")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_database():
    """التحقق من قاعدة البيانات"""
    print("\n🗄️  فحص قاعدة البيانات...")
    
    db_path = 'management_system.db'
    
    if not os.path.exists(db_path):
        print("   ⚠️  قاعدة البيانات غير موجودة - سيتم إنشاؤها عند التشغيل الأول")
        return True
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # التحقق من الجداول المطلوبة
        required_tables = ['employees', 'cars', 'financial_records']
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        for table in required_tables:
            if table in existing_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ جدول {table} - {count} سجل")
            else:
                print(f"   ❌ جدول {table} - مفقود")
        
        # حجم قاعدة البيانات
        size = os.path.getsize(db_path)
        size_mb = size / (1024 * 1024)
        print(f"   📊 حجم قاعدة البيانات: {size_mb:.2f} ميجابايت")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في قاعدة البيانات: {e}")
        return False

def check_ports():
    """التحقق من توفر المنافذ"""
    print("\n🌐 فحص المنافذ...")
    
    import socket
    
    def is_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return True
            except OSError:
                return False
    
    port = 5000
    if is_port_available(port):
        print(f"   ✅ المنفذ {port} متاح")
        return True
    else:
        print(f"   ❌ المنفذ {port} مستخدم من تطبيق آخر")
        print("   💡 جرب إغلاق التطبيقات الأخرى أو استخدم منفذ مختلف")
        return False

def check_permissions():
    """التحقق من الصلاحيات"""
    print("\n🔐 فحص الصلاحيات...")
    
    # التحقق من صلاحية الكتابة
    try:
        test_file = 'test_permissions.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("   ✅ صلاحية الكتابة متاحة")
        return True
    except Exception as e:
        print(f"   ❌ خطأ في صلاحية الكتابة: {e}")
        return False

def generate_report():
    """إنشاء تقرير الفحص"""
    print("\n📋 إنشاء تقرير الفحص...")
    
    report = f"""
تقرير فحص النظام - RASHID INDUSTRIAL CO.
==========================================

التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
نظام التشغيل: {os.name}
مجلد العمل: {os.getcwd()}
إصدار Python: {sys.version}

الملفات الموجودة:
"""
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.py', '.html', '.css', '.js', '.txt', '.md')):
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                report += f"  {file_path} ({size} بايت)\n"
    
    report_file = f"تقرير_الفحص_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"   ✅ تم حفظ التقرير في: {report_file}")
        return True
    except Exception as e:
        print(f"   ❌ خطأ في حفظ التقرير: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print_header()
    
    checks = [
        ("Python", check_python),
        ("المكتبات", check_modules),
        ("الملفات", check_files),
        ("قاعدة البيانات", check_database),
        ("المنافذ", check_ports),
        ("الصلاحيات", check_permissions)
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ خطأ في فحص {name}: {e}")
            results.append((name, False))
    
    # ملخص النتائج
    print("\n" + "=" * 70)
    print("📊 ملخص نتائج الفحص")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ نجح" if result else "❌ فشل"
        print(f"   {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 النتيجة الإجمالية: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 النظام جاهز للتشغيل!")
        print("💡 يمكنك الآن تشغيل النظام باستخدام: python app.py")
    else:
        print("⚠️  يرجى إصلاح المشاكل المذكورة أعلاه قبل التشغيل")
    
    # إنشاء تقرير
    generate_report()
    
    print("\n" + "=" * 70)
    print("👋 انتهى فحص النظام")
    print("=" * 70)
    
    return passed == total

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف الفحص بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)