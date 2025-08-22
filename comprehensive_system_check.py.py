#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
فحص شامل للنظام المتعدد الشاشات
RASHID INDUSTRIAL CO.
"""

import os
import sys
import sqlite3
import importlib.util
from datetime import datetime

def print_header():
    """طباعة رأس الفحص"""
    print("=" * 70)
    print("🔍 فحص شامل للنظام المتعدد الشاشات")
    print("   RASHID INDUSTRIAL CO.")
    print("=" * 70)
    print()

def check_python():
    """فحص إصدار Python"""
    print("🐍 فحص Python...")
    version = sys.version_info
    print(f"   الإصدار: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("   ✅ إصدار Python مناسب")
        return True
    else:
        print("   ❌ يتطلب Python 3.7 أو أحدث")
        return False

def check_files():
    """فحص الملفات المطلوبة"""
    print("\n📁 فحص الملفات...")
    
    required_files = [
        'app.py',
        'database.py', 
        'config.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/treasury.html',
        'templates/car_entry.html',
        'templates/car_delivery.html',
        'templates/car_receipt.html',
        'templates/cars.html',
        'templates/add_employee.html',
        'templates/employees.html',
        'templates/expenses.html',
        'templates/reports.html',
        'templates/settings.html',
        'templates/login.html',
        'static/css/custom.css',
        'static/js/main.js'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - مفقود")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n   ⚠️  {len(missing_files)} ملف مفقود")
        return False
    else:
        print(f"\n   ✅ جميع الملفات موجودة ({len(required_files)} ملف)")
        return True

def check_modules():
    """فحص المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات...")
    
    required_modules = [
        'flask',
        'sqlite3',
        'datetime',
        'os',
        'hashlib',
        'functools'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'sqlite3':
                import sqlite3
            elif module == 'flask':
                import flask
            elif module == 'datetime':
                import datetime
            elif module == 'os':
                import os
            elif module == 'hashlib':
                import hashlib
            elif module == 'functools':
                import functools
            
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - غير مثبت")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n   ⚠️  {len(missing_modules)} مكتبة مفقودة")
        print("   💡 قم بتشغيل: pip install -r requirements.txt")
        return False
    else:
        print(f"\n   ✅ جميع المكتبات متوفرة ({len(required_modules)} مكتبة)")
        return True

def check_database():
    """فحص قاعدة البيانات"""
    print("\n🗄️  فحص قاعدة البيانات...")
    
    db_file = 'management_system.db'
    
    if not os.path.exists(db_file):
        print("   ⚠️  قاعدة البيانات غير موجودة - سيتم إنشاؤها عند التشغيل")
        return True
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # فحص الجداول المطلوبة
        required_tables = [
            'employees',
            'cars', 
            'financial_records',
            'users',
            'audit_logs',
            'settings',
            'car_custody',
            'treasury',
            'expenses'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = []
        for table in required_tables:
            if table in existing_tables:
                print(f"   ✅ جدول {table}")
            else:
                print(f"   ❌ جدول {table} - مفقود")
                missing_tables.append(table)
        
        # إحصائيات البيانات
        if not missing_tables:
            print("\n   📊 إحصائيات البيانات:")
            for table in required_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"      {table}: {count} سجل")
                except:
                    print(f"      {table}: خطأ في القراءة")
        
        # حجم قاعدة البيانات
        db_size = os.path.getsize(db_file)
        print(f"\n   📏 حجم قاعدة البيانات: {db_size:,} بايت ({db_size/1024:.1f} KB)")
        
        conn.close()
        
        if missing_tables:
            print(f"\n   ⚠️  {len(missing_tables)} جدول مفقود")
            return False
        else:
            print(f"\n   ✅ جميع الجداول موجودة ({len(required_tables)} جدول)")
            return True
            
    except Exception as e:
        print(f"   ❌ خطأ في فحص قاعدة البيانات: {e}")
        return False

def check_config():
    """فحص ملف الإعدادات"""
    print("\n⚙️  فحص الإعدادات...")
    
    try:
        import config
        
        required_configs = [
            'SECRET_KEY',
            'DATABASE_PATH',
            'DEBUG'
        ]
        
        missing_configs = []
        for conf in required_configs:
            if hasattr(config, conf):
                print(f"   ✅ {conf}")
            else:
                print(f"   ❌ {conf} - مفقود")
                missing_configs.append(conf)
        
        if missing_configs:
            print(f"\n   ⚠️  {len(missing_configs)} إعداد مفقود")
            return False
        else:
            print(f"\n   ✅ جميع الإعدادات موجودة ({len(required_configs)} إعداد)")
            return True
            
    except ImportError:
        print("   ❌ ملف config.py غير موجود")
        return False
    except Exception as e:
        print(f"   ❌ خطأ في فحص الإعدادات: {e}")
        return False

def check_app_structure():
    """فحص هيكل التطبيق"""
    print("\n🏗️  فحص هيكل التطبيق...")
    
    try:
        import app
        
        # فحص المسارات المطلوبة
        required_routes = [
            'index',
            'login',
            'logout',
            'treasury',
            'car_entry',
            'car_delivery', 
            'car_receipt',
            'cars',
            'add_employee',
            'employees',
            'expenses',
            'reports_page',
            'settings'
        ]
        
        # الحصول على قائمة المسارات المتاحة
        available_routes = []
        for rule in app.app.url_map.iter_rules():
            if rule.endpoint != 'static':
                available_routes.append(rule.endpoint)
        
        missing_routes = []
        for route in required_routes:
            if route in available_routes:
                print(f"   ✅ مسار {route}")
            else:
                print(f"   ❌ مسار {route} - مفقود")
                missing_routes.append(route)
        
        if missing_routes:
            print(f"\n   ⚠️  {len(missing_routes)} مسار مفقود")
            return False
        else:
            print(f"\n   ✅ جميع المسارات موجودة ({len(required_routes)} مسار)")
            return True
            
    except ImportError:
        print("   ❌ لا يمكن استيراد app.py")
        return False
    except Exception as e:
        print(f"   ❌ خطأ في فحص هيكل التطبيق: {e}")
        return False

def check_permissions():
    """فحص الصلاحيات"""
    print("\n🔐 فحص الصلاحيات...")
    
    # فحص صلاحيات الكتابة
    try:
        test_file = 'test_write_permission.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("   ✅ صلاحيات الكتابة")
    except:
        print("   ❌ صلاحيات الكتابة - مرفوضة")
        return False
    
    # فحص صلاحيات قاعدة البيانات
    try:
        if os.path.exists('management_system.db'):
            conn = sqlite3.connect('management_system.db')
            conn.close()
            print("   ✅ صلاحيات قاعدة البيانات")
        else:
            print("   ⚠️  قاعدة البيانات غير موجودة")
    except:
        print("   ❌ صلاحيات قاعدة البيانات - مرفوضة")
        return False
    
    return True

def generate_report():
    """إنشاء تقرير الفحص"""
    print("\n📋 إنشاء تقرير الفحص...")
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_file = f'تقرير_فحص_النظام_{timestamp}.txt'
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("تقرير فحص النظام المتعدد الشاشات\n")
            f.write("RASHID INDUSTRIAL CO.\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"تاريخ الفحص: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"إصدار Python: {sys.version}\n")
            f.write(f"نظام التشغيل: {os.name}\n\n")
            
            # يمكن إضافة المزيد من التفاصيل هنا
            
        print(f"   ✅ تم إنشاء التقرير: {report_file}")
        return True
    except Exception as e:
        print(f"   ❌ فشل في إنشاء التقرير: {e}")
        return False

def main():
    """الوظيفة الرئيسية للفحص"""
    print_header()
    
    checks = [
        ("Python", check_python),
        ("الملفات", check_files),
        ("المكتبات", check_modules),
        ("قاعدة البيانات", check_database),
        ("الإعدادات", check_config),
        ("هيكل التطبيق", check_app_structure),
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
    failed = 0
    
    for name, result in results:
        if result:
            print(f"✅ {name}: نجح")
            passed += 1
        else:
            print(f"❌ {name}: فشل")
            failed += 1
    
    print(f"\n📈 النتيجة النهائية:")
    print(f"   ✅ نجح: {passed}")
    print(f"   ❌ فشل: {failed}")
    print(f"   📊 المعدل: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 النظام جاهز للتشغيل!")
        print("   يمكنك تشغيل النظام باستخدام:")
        print("   • تشغيل_شامل_مع_بيانات.bat")
        print("   • تشغيل_النظام_المتعدد.bat")
        print("   • python app.py")
    else:
        print(f"\n⚠️  يوجد {failed} مشكلة تحتاج إلى حل قبل التشغيل")
        print("   راجع التفاصيل أعلاه لحل المشاكل")
    
    # إنشاء تقرير
    generate_report()
    
    print("\n" + "=" * 70)
    print("انتهى الفحص")
    print("=" * 70)

if __name__ == '__main__':
    main()
    input("\nاضغط Enter للخروج...")