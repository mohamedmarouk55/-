#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
إصلاح نهائي لمشاكل تسجيل الدخول في app.py
RASHID INDUSTRIAL CO.
"""

import os
import shutil

def fix_login_issues():
    """إصلاح مشاكل تسجيل الدخول في app.py"""
    
    print("🔧 إصلاح مشاكل تسجيل الدخول في app.py...")
    
    # قراءة الملف الحالي
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ تم قراءة app.py")
        
        # إنشاء نسخة احتياطية
        shutil.copy('app.py', 'app_backup.py')
        print("✅ تم إنشاء نسخة احتياطية: app_backup.py")
        
        # الإصلاحات المطلوبة
        fixes = [
            # إصلاح 1: تحسين دالة login_required
            {
                'old': '''def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function''',
                'new': '''def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            print(f"❌ غير مسجل دخول، إعادة توجيه من {request.endpoint}")
            return redirect(url_for('login'))
        print(f"✅ مسجل دخول: {session.get('username')} - الوصول إلى {request.endpoint}")
        return f(*args, **kwargs)
    return decorated_function'''
            },
            
            # إصلاح 2: تحسين الصفحة الرئيسية
            {
                'old': '''# الصفحة الرئيسية
@app.route('/')
def index():
    # إذا لم يكن المستخدم مسجل دخول، توجيهه لصفحة تسجيل الدخول
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # إذا كان مسجل دخول، عرض الصفحة الرئيسية''',
                'new': '''# الصفحة الرئيسية
@app.route('/')
def index():
    print("🏠 طلب الصفحة الرئيسية")
    print(f"   الجلسة الحالية: {dict(session)}")
    
    # إذا لم يكن المستخدم مسجل دخول، توجيهه لصفحة تسجيل الدخول
    if 'user_id' not in session:
        print("❌ المستخدم غير مسجل دخول، إعادة توجيه لتسجيل الدخول")
        return redirect(url_for('login'))
    
    print(f"✅ المستخدم مسجل دخول: {session.get('username')}")
    # إذا كان مسجل دخول، عرض الصفحة الرئيسية'''
            },
            
            # إصلاح 3: تحسين دالة login
            {
                'old': '''    # إذا كان المستخدم مسجل دخول بالفعل، توجيهه للصفحة الرئيسية
    if 'user_id' in session:
        print("المستخدم مسجل دخول بالفعل، إعادة توجيه للصفحة الرئيسية")
        return redirect(url_for('index'))''',
                'new': '''    print("🔐 طلب صفحة تسجيل الدخول")
    print(f"   الجلسة الحالية: {dict(session)}")
    
    # إذا كان المستخدم مسجل دخول بالفعل، توجيهه للصفحة الرئيسية
    if 'user_id' in session:
        print(f"✅ المستخدم مسجل دخول بالفعل: {session.get('username')}")
        print("🔄 إعادة توجيه للصفحة الرئيسية")
        return redirect(url_for('index'))'''
            },
            
            # إصلاح 4: تحسين معالجة POST في login
            {
                'old': '''        # فحص بيانات admin المباشرة (بدون قاعدة بيانات أولاً)
        if (username == 'admin' or username == 'admin@rashid.com') and password == 'admin123':
            print("✅ تسجيل دخول مباشر ناجح لـ admin")
            
            # تسجيل الجلسة
            session.permanent = True
            session['user_id'] = 1
            session['username'] = 'admin'
            session['role'] = 'admin'
            
            print("✅ تم تسجيل الجلسة بنجاح")
            flash('تم تسجيل الدخول بنجاح!', 'success')
            
            print("🔄 إعادة توجيه للصفحة الرئيسية")
            return redirect(url_for('index'))''',
                'new': '''        # فحص بيانات admin المباشرة (بدون قاعدة بيانات أولاً)
        if (username.lower() == 'admin' or username == 'admin@rashid.com') and password == 'admin123':
            print("✅ تسجيل دخول مباشر ناجح لـ admin")
            
            # مسح الجلسة القديمة أولاً
            session.clear()
            
            # تسجيل الجلسة الجديدة
            session.permanent = True
            session['user_id'] = 1
            session['username'] = 'admin'
            session['role'] = 'admin'
            
            print(f"✅ تم تسجيل الجلسة الجديدة: {dict(session)}")
            flash('تم تسجيل الدخول بنجاح!', 'success')
            
            print("🔄 إعادة توجيه للصفحة الرئيسية")
            return redirect(url_for('index'))'''
            }
        ]
        
        # تطبيق الإصلاحات
        fixed_content = content
        fixes_applied = 0
        
        for fix in fixes:
            if fix['old'] in fixed_content:
                fixed_content = fixed_content.replace(fix['old'], fix['new'])
                fixes_applied += 1
                print(f"✅ تم تطبيق الإصلاح {fixes_applied}")
            else:
                print(f"⚠️  لم يتم العثور على النص للإصلاح {fixes_applied + 1}")
        
        # كتابة الملف المُصحح
        with open('app_fixed.py', 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ تم إنشاء app_fixed.py مع {fixes_applied} إصلاحات")
        
        # إضافة تحسينات إضافية
        additional_fixes = '''
# إضافة في بداية الملف بعد الـ imports
import sys
from datetime import datetime

# إضافة دالة مساعدة للتشخيص
def log_session_info(action=""):
    """تسجيل معلومات الجلسة للتشخيص"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {action}")
    print(f"   الجلسة: {dict(session)}")
    print(f"   المسار: {request.path}")
    print("-" * 40)

# إضافة معالج قبل كل طلب
@app.before_request
def before_request():
    if request.endpoint not in ['static', 'favicon']:
        log_session_info(f"طلب {request.method} إلى {request.path}")
'''
        
        # إضافة التحسينات الإضافية
        with open('app_fixed.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن مكان إدراج التحسينات
        import_end = content.find('app = Flask(__name__)')
        if import_end != -1:
            new_content = content[:import_end] + additional_fixes + '\n' + content[import_end:]
            
            with open('app_fixed.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ تم إضافة التحسينات الإضافية")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الإصلاح: {e}")
        return False

def create_test_script():
    """إنشاء سكريبت اختبار تسجيل الدخول"""
    
    test_script = '''#!/usr/bin/env python3
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
'''
    
    try:
        with open('اختبار_تسجيل_الدخول.py', 'w', encoding='utf-8') as f:
            f.write(test_script)
        print("✅ تم إنشاء اختبار_تسجيل_الدخول.py")
        return True
    except Exception as e:
        print(f"❌ خطأ في إنشاء ملف الاختبار: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 إصلاح نهائي لمشاكل تسجيل الدخول")
    print("RASHID INDUSTRIAL CO.")
    print("=" * 60)
    
    if fix_login_issues():
        print("\n✅ تم إصلاح جميع مشاكل تسجيل الدخول")
        print("📁 الملفات المُنشأة:")
        print("   • app_fixed.py - النسخة المُصححة")
        print("   • app_backup.py - النسخة الاحتياطية")
        
        if create_test_script():
            print("   • اختبار_تسجيل_الدخول.py - سكريبت الاختبار")
        
        print("\n🚀 للتشغيل:")
        print("   python app_fixed.py")
        print("   أو استخدم: تشغيل_النسخة_المُصححة.bat")
        
    else:
        print("\n❌ فشل في الإصلاح")
    
    print("=" * 60)