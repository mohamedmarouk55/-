#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام الإدارة الشامل
ملف التشغيل الرئيسي المحسن - مدمج بالكامل
يدعم Supabase كقاعدة بيانات وتخزين
"""

import os
import sys
import logging
from datetime import datetime
import webbrowser
import threading
import time

# استيراد Flask وSQLAlchemy
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# استيراد Supabase للتخزين
from supabase import create_client

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ===========================
# 1. إنشاء التطبيق
# ===========================
app = Flask(__name__)

# ===========================
# 2. ربط قاعدة البيانات (Supabase PostgreSQL)
# ===========================
# استخدم DATABASE_URL من البيئة
database_url = os.getenv("DATABASE_URL", "sqlite:///management_system.db")

# تصحيح الرابط إذا بدأ بـ postgres://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إنشاء كائن قاعدة البيانات
db = SQLAlchemy(app)

# ===========================
# 3. ربط Supabase Storage
# ===========================
# مفاتيح Supabase من البيئة
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# متغير للاتصال بـ Supabase
supabase_client = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ اتصال Supabase نجح (Storage)")
else:
    print("⚠️ تحذير: لم تُضبط مفاتيح Supabase (Storage)")

# ===========================
# 4. دالة رفع الملفات إلى Supabase
# ===========================
def upload_to_supabase(file_path, file_name, bucket="car-photos"):
    """
    ترفع ملف إلى Supabase Storage
    """
    if not supabase_client:
        print("❌ لا يوجد اتصال بـ Supabase")
        return None

    try:
        with open(file_path, "rb") as f:
            supabase_client.storage.from_(bucket).upload(file_name, f.read())
        
        # احصل على الرابط العام
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{file_name}"
        print(f"✅ تم رفع الملف: {public_url}")
        return public_url

    except Exception as e:
        print(f"❌ خطأ في الرفع: {e}")
        return None

# ===========================
# 5. صفحة تجريبية لرفع صورة
# ===========================
@app.route('/test-upload')
def test_upload():
    test_image_path = "test.jpg"
    
    if not os.path.exists(test_image_path):
        return f"""
        ❌ الملف {test_image_path} غير موجود.<br>
        رجاءً ضع صورة باسم <strong>test.jpg</strong> في مجلد المشروع.
        """

    image_url = upload_to_supabase(test_image_path, "test_car.jpg", "car-photos")
    
    if image_url:
        return f"""
        <h3>✅ تم رفع الصورة بنجاح!</h3>
        <img src="{image_url}" width="300" style="border: 1px solid #ddd; border-radius: 8px;">
        <p><a href="{image_url}" target="_blank">افتح الصورة في نافذة جديدة</a></p>
        <p>الرابط: <a href="{image_url}" target="_blank">{image_url}</a></p>
        """
    else:
        return "❌ فشل في رفع الصورة. شوف السجلات (Logs) لمعرفة السبب."

# ===========================
# 6. إعداد السجلات
# ===========================
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
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

# ===========================
# 7. التحقق من المكتبات
# ===========================
def check_dependencies():
    """التحقق من المكتبات المطلوبة"""
    required_packages = [
        'flask', 'werkzeug', 'jinja2', 'markupsafe',
        'itsdangerous', 'click', 'blinker', 'flask_sqlalchemy', 'supabase'
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

# ===========================
# 8. تهيئة قاعدة البيانات
# ===========================
def initialize_database():
    """تهيئة قاعدة البيانات"""
    try:
        print("🔧 تهيئة قاعدة البيانات...")
        db.create_all()
        print("✅ تم تهيئة قاعدة البيانات بنجاح")
        return True
    except Exception as e:
        print(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
        return False

# ===========================
# 9. إنشاء بيانات تجريبية
# ===========================
def create_sample_data():
    """إنشاء بيانات تجريبية (اختياري)"""
    # هذه الوظيفة تحتاج تعريف الجداول أولاً
    pass

# ===========================
# 10. فتح المتصفح
# ===========================
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

# ===========================
# 11. رسائل التشغيل
# ===========================
def print_startup_info():
    print("=" * 60)
    print("🚀 نظام الإدارة الشامل")
    print("=" * 60)
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 المجلد: {os.path.dirname(os.path.abspath(__file__))}")
    print("=" * 60)

def print_success_info(host, port):
    print("\n" + "=" * 60)
    print("🎉 تم تشغيل النظام بنجاح!")
    print("=" * 60)
    print(f"🌐 الرابط: http://{host}:{port}")
    print("📱 يمكنك الوصول للنظام من أي جهاز على نفس الشبكة")
    print("⏹️  لإيقاف النظام: اضغط Ctrl+C")
    print("=" * 60)

# ===========================
# 12. الدالة الرئيسية
# ===========================
def main():
    print_startup_info()
    
    print("🔍 التحقق من المكتبات المطلوبة...")
    if not check_dependencies():
        return 1
    print("✅ جميع المكتبات متوفرة")
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    if not initialize_database():
        return 1
    
    create_sample_data()
    
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object('config.' + env if env != 'development' else 'config.DevConfig')
    
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    if not debug:
        open_browser(f'http://localhost:{port}')
    
    try:
        print_success_info(host, port)
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=False,
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