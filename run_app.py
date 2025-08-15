#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام الإدارة الشامل
ملف التشغيل الرئيسي المحسن
"""

import os
import sys
import logging
from datetime import datetime
import webbrowser
import threading
import time

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    from config import config
    from database import db_manager
    from reports import reports_manager
except ImportError as e:
    print(f"خطأ في استيراد الوحدات: {e}")
    print("تأكد من وجود جميع الملفات المطلوبة")
    sys.exit(1)

def setup_logging():
    """إعداد نظام السجلات"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # تقليل مستوى سجلات Werkzeug
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

def check_dependencies():
    """التحقق من المكتبات المطلوبة"""
    required_packages = [
        'flask',
        'werkzeug',
        'jinja2',
        'markupsafe',
        'itsdangerous',
        'click',
        'blinker'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ المكتبات التالية مفقودة:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nلتثبيت المكتبات المفقودة، قم بتشغيل:")
        print("pip install " + " ".join(missing_packages))
        return False
    
    return True

def initialize_database():
    """تهيئة قاعدة البيانات"""
    try:
        print("🔧 تهيئة قاعدة البيانات...")
        db_manager.init_database()
        print("✅ تم تهيئة قاعدة البيانات بنجاح")
        return True
    except Exception as e:
        print(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
        return False

def create_sample_data():
    """إنشاء بيانات تجريبية (اختياري)"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # التحقق من وجود بيانات
    cursor.execute('SELECT COUNT(*) FROM employees')
    employee_count = cursor.fetchone()[0]
    
    if employee_count == 0:
        print("📝 إنشاء بيانات تجريبية...")
        
        # إضافة موظفين تجريبيين
        sample_employees = [
            ('أحمد محمد', 'مدير عام', 'الإدارة', 15000, '0501234567', 'ahmed@company.com', '2023-01-15'),
            ('فاطمة علي', 'محاسبة', 'المحاسبة', 8000, '0507654321', 'fatima@company.com', '2023-02-01'),
            ('محمد سالم', 'سائق', 'النقل', 4000, '0509876543', 'mohammed@company.com', '2023-03-10'),
        ]
        
        for emp in sample_employees:
            cursor.execute('''
                INSERT INTO employees (name, position, department, salary, phone, email, hire_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', emp)
        
        # إضافة سيارات تجريبية
        sample_cars = [
            ('تويوتا', 'كامري', 2022, 'أ ب ج 1234', 'أبيض', 'متاح', 80000, 75000),
            ('هوندا', 'أكورد', 2021, 'د هـ و 5678', 'أسود', 'مستأجر', 70000, 65000),
            ('نيسان', 'التيما', 2020, 'ز ح ط 9012', 'فضي', 'صيانة', 60000, 50000),
        ]
        
        for car in sample_cars:
            cursor.execute('''
                INSERT INTO cars (brand, model, year, license_plate, color, status, purchase_price, current_value)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', car)
        
        # إضافة سجلات مالية تجريبية
        sample_financial = [
            ('إيراد', 'المبيعات', 25000, 'إيراد من تأجير السيارات', '2024-01-15'),
            ('مصروف', 'الوقود', 3000, 'وقود السيارات', '2024-01-16'),
            ('إيراد', 'الخدمات', 15000, 'خدمات الصيانة', '2024-01-20'),
            ('مصروف', 'الصيانة والإصلاح', 5000, 'صيانة السيارات', '2024-01-22'),
        ]
        
        for record in sample_financial:
            cursor.execute('''
                INSERT INTO financial_records (type, category, amount, description, date)
                VALUES (?, ?, ?, ?, ?)
            ''', record)
        
        conn.commit()
        print("✅ تم إنشاء البيانات التجريبية")
    
    conn.close()

def open_browser(url, delay=2):
    """فتح المتصفح تلقائياً"""
    def open_url():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"تعذر فتح المتصفح تلقائياً: {e}")
    
    thread = threading.Thread(target=open_url)
    thread.daemon = True
    thread.start()

def print_startup_info():
    """طباعة معلومات بدء التشغيل"""
    print("=" * 60)
    print("🚀 نظام الإدارة الشامل")
    print("=" * 60)
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 المجلد: {os.path.dirname(os.path.abspath(__file__))}")
    print("=" * 60)

def print_success_info(host, port):
    """طباعة معلومات النجاح"""
    print("\n" + "=" * 60)
    print("🎉 تم تشغيل النظام بنجاح!")
    print("=" * 60)
    print(f"🌐 الرابط: http://{host}:{port}")
    print("📱 يمكنك الوصول للنظام من أي جهاز على نفس الشبكة")
    print("⏹️  لإيقاف النظام: اضغط Ctrl+C")
    print("=" * 60)
    print("\n🔧 الميزات المتاحة:")
    print("   • إدارة الموظفين والرواتب")
    print("   • إدارة أسطول السيارات")
    print("   • تتبع البيانات المالية")
    print("   • تقارير وإحصائيات تفاعلية")
    print("   • واجهة متجاوبة وحديثة")
    print("\n📊 لوحة التحكم تحتوي على:")
    print("   • إحصائيات فورية")
    print("   • رسوم بيانية تفاعلية")
    print("   • إجراءات سريعة")
    print("=" * 60)

def main():
    """الدالة الرئيسية"""
    print_startup_info()
    
    # التحقق من المكتبات
    print("🔍 التحقق من المكتبات المطلوبة...")
    if not check_dependencies():
        return 1
    print("✅ جميع المكتبات متوفرة")
    
    # إعداد السجلات
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # تهيئة قاعدة البيانات
    if not initialize_database():
        return 1
    
    # إنشاء بيانات تجريبية
    create_sample_data()
    
    # إعداد التطبيق
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    # معلومات الخادم
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    # فتح المتصفح تلقائياً
    if not debug:
        open_browser(f'http://localhost:{port}')
    
    try:
        print_success_info(host, port)
        
        # تشغيل التطبيق
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=False,  # تجنب إعادة التشغيل المزدوج
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف النظام بواسطة المستخدم")
        logger.info("تم إيقاف النظام بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل النظام: {e}")
        logger.error(f"خطأ في تشغيل النظام: {e}")
        return 1
    
    print("👋 شكراً لاستخدام نظام الإدارة الشامل!")
    return 0

if __name__ == '__main__':
    sys.exit(main())