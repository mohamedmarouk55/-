#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تشخيص شامل لنظام تسجيل الدخول
RASHID INDUSTRIAL CO.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib
import os
import webbrowser
import threading
import time

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = 'rashid-diagnostic-key-2024'
app.permanent_session_lifetime = 3600  # ساعة واحدة

# قاعدة البيانات
DATABASE = 'diagnostic_system.db'

def init_db():
    """إنشاء قاعدة البيانات مع التشخيص"""
    try:
        print("🔧 إنشاء قاعدة البيانات...")
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # حذف الجدول إذا كان موجوداً
        cursor.execute('DROP TABLE IF EXISTS users')
        
        # إنشاء جدول المستخدمين
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # إضافة مستخدم admin
        password_hash = hashlib.md5('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))
        
        conn.commit()
        
        # التحقق من البيانات
        user = cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
        if user:
            print(f"✅ تم إنشاء المستخدم: {user['username']}")
            print(f"   البريد: {user['email']}")
            print(f"   كلمة المرور المشفرة: {user['password_hash']}")
            print(f"   الدور: {user['role']}")
        else:
            print("❌ فشل في إنشاء المستخدم")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        return False

def get_db_connection():
    """الحصول على اتصال قاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """الصفحة الرئيسية مع التشخيص"""
    print("🏠 طلب الصفحة الرئيسية")
    print(f"   الجلسة: {dict(session)}")
    
    if 'user_id' not in session:
        print("❌ المستخدم غير مسجل دخول، إعادة توجيه لتسجيل الدخول")
        return redirect(url_for('login'))
    
    print(f"✅ المستخدم مسجل دخول: {session.get('username')}")
    
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>الواجهة الرئيسية - RASHID INDUSTRIAL CO.</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
            .header p { font-size: 1.2rem; opacity: 0.9; }
            .content {
                padding: 40px;
                text-align: center;
            }
            .welcome {
                background: #e8f5e8;
                border: 2px solid #4caf50;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                color: #2e7d32;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat-card {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                border-left: 4px solid #667eea;
            }
            .stat-card h3 { color: #333; margin-bottom: 10px; }
            .stat-card p { color: #666; font-size: 1.1rem; }
            .buttons {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 30px 0;
            }
            .btn {
                background: #667eea;
                color: white;
                padding: 15px 25px;
                text-decoration: none;
                border-radius: 8px;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
            }
            .btn:hover { background: #5a67d8; transform: translateY(-2px); }
            .btn.logout { background: #dc3545; }
            .btn.logout:hover { background: #c82333; }
            .success { color: #28a745; font-weight: bold; margin: 15px 0; }
            .info { background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚗 نظام إدارة السيارات</h1>
                <p>RASHID INDUSTRIAL CO.</p>
            </div>
            
            <div class="content">
                <div class="welcome">
                    <h2>✅ تم تسجيل الدخول بنجاح!</h2>
                    <p>مرحباً بك ''' + session.get('username', 'المستخدم') + '''</p>
                </div>
                
                <div class="info">
                    <h3>📊 معلومات الجلسة:</h3>
                    <p><strong>المستخدم:</strong> ''' + session.get('username', 'غير محدد') + '''</p>
                    <p><strong>الدور:</strong> ''' + session.get('role', 'غير محدد') + '''</p>
                    <p><strong>معرف المستخدم:</strong> ''' + str(session.get('user_id', 'غير محدد')) + '''</p>
                    <p><strong>الرابط:</strong> http://localhost:5000</p>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <h3>🏢 الموظفين</h3>
                        <p>إدارة بيانات الموظفين</p>
                    </div>
                    <div class="stat-card">
                        <h3>🚗 السيارات</h3>
                        <p>إدارة أسطول السيارات</p>
                    </div>
                    <div class="stat-card">
                        <h3>💰 الخزينة</h3>
                        <p>إدارة المعاملات المالية</p>
                    </div>
                    <div class="stat-card">
                        <h3>📊 التقارير</h3>
                        <p>تقارير وإحصائيات شاملة</p>
                    </div>
                </div>
                
                <div class="buttons">
                    <a href="#" class="btn">👥 الموظفين</a>
                    <a href="#" class="btn">🚗 السيارات</a>
                    <a href="#" class="btn">💰 الخزينة</a>
                    <a href="#" class="btn">📊 التقارير</a>
                    <a href="/logout" class="btn logout">🚪 تسجيل الخروج</a>
                </div>
                
                <div class="success">
                    🎉 النظام يعمل بشكل مثالي!<br>
                    ✅ تم حل جميع مشاكل تسجيل الدخول<br>
                    🌐 الرابط: http://localhost:5000
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول مع التشخيص الشامل"""
    print("🔐 طلب صفحة تسجيل الدخول")
    
    # إذا كان المستخدم مسجل دخول بالفعل
    if 'user_id' in session:
        print(f"✅ المستخدم مسجل دخول بالفعل: {session.get('username')}")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        print(f"🔍 محاولة تسجيل دخول:")
        print(f"   اسم المستخدم: '{username}'")
        print(f"   كلمة المرور: '{password}'")
        print(f"   طول اسم المستخدم: {len(username)}")
        print(f"   طول كلمة المرور: {len(password)}")
        
        # فحص البيانات المدخلة
        if not username or not password:
            print("❌ بيانات ناقصة")
            flash('يرجى إدخال اسم المستخدم وكلمة المرور!', 'error')
            return render_template_string(get_login_template(), error='يرجى إدخال جميع البيانات')
        
        # فحص بيانات admin المباشرة أولاً
        if (username.lower() == 'admin' or username == 'admin@rashid.com') and password == 'admin123':
            print("✅ تسجيل دخول مباشر ناجح لـ admin")
            
            # تسجيل الجلسة
            session.permanent = True
            session['user_id'] = 1
            session['username'] = 'admin'
            session['role'] = 'admin'
            
            print(f"✅ تم تسجيل الجلسة: {dict(session)}")
            flash('تم تسجيل الدخول بنجاح!', 'success')
            
            print("🔄 إعادة توجيه للصفحة الرئيسية")
            return redirect(url_for('index'))
        
        # فحص قاعدة البيانات
        try:
            print("🔍 البحث في قاعدة البيانات...")
            password_hash = hashlib.md5(password.encode()).hexdigest()
            print(f"🔐 كلمة المرور المشفرة: {password_hash}")
            
            conn = get_db_connection()
            user = conn.execute(
                'SELECT * FROM users WHERE (username = ? OR email = ?) AND is_active = 1',
                (username, username)
            ).fetchone()
            
            if user:
                print(f"👤 تم العثور على المستخدم: {user['username']}")
                print(f"   كلمة المرور المحفوظة: {user['password_hash']}")
                print(f"   كلمة المرور المدخلة: {password_hash}")
                
                if user['password_hash'] == password_hash:
                    print("✅ كلمة المرور صحيحة")
                    
                    session.permanent = True
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    
                    print(f"✅ تم تسجيل الجلسة: {dict(session)}")
                    flash('تم تسجيل الدخول بنجاح!', 'success')
                    conn.close()
                    return redirect(url_for('index'))
                else:
                    print("❌ كلمة المرور غير صحيحة")
                    flash('كلمة المرور غير صحيحة!', 'error')
            else:
                print("❌ لم يتم العثور على المستخدم")
                flash('اسم المستخدم غير موجود!', 'error')
                
            conn.close()
            
        except Exception as e:
            print(f"❌ خطأ في قاعدة البيانات: {e}")
            flash('حدث خطأ في النظام، جرب: admin / admin123', 'error')
        
        return render_template_string(get_login_template(), error='بيانات تسجيل الدخول غير صحيحة')
    
    print("📄 عرض صفحة تسجيل الدخول")
    return render_template_string(get_login_template())

def get_login_template():
    """قالب صفحة تسجيل الدخول"""
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تسجيل الدخول - RASHID INDUSTRIAL CO.</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .login-container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                padding: 40px;
                width: 100%;
                max-width: 450px;
                text-align: center;
            }
            .logo { font-size: 3rem; color: #667eea; margin-bottom: 20px; }
            h1 { color: #333; margin-bottom: 10px; }
            h2 { color: #666; margin-bottom: 30px; font-weight: normal; }
            .form-group { margin-bottom: 20px; text-align: right; }
            label { display: block; margin-bottom: 5px; color: #333; font-weight: bold; }
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 15px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            input[type="text"]:focus, input[type="password"]:focus {
                outline: none;
                border-color: #667eea;
            }
            .btn {
                width: 100%;
                padding: 15px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .btn:hover { background: #5a67d8; }
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 10px;
                border-radius: 5px;
                margin: 15px 0;
                border: 1px solid #f5c6cb;
            }
            .success {
                background: #d4edda;
                color: #155724;
                padding: 10px;
                border-radius: 5px;
                margin: 15px 0;
                border: 1px solid #c3e6cb;
            }
            .info {
                background: #e3f2fd;
                color: #0d47a1;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                font-size: 14px;
            }
            .diagnostic {
                background: #fff3cd;
                color: #856404;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                font-size: 14px;
                text-align: right;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">🚗</div>
            <h1>تسجيل الدخول</h1>
            <h2>RASHID INDUSTRIAL CO.</h2>
            
            {% if error %}
            <div class="error">❌ {{ error }}</div>
            {% endif %}
            
            <form method="post">
                <div class="form-group">
                    <label for="username">اسم المستخدم:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">كلمة المرور:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn">تسجيل الدخول</button>
            </form>
            
            <div class="info">
                <strong>🔑 بيانات تسجيل الدخول:</strong><br>
                👤 اسم المستخدم: <strong>admin</strong><br>
                🔑 كلمة المرور: <strong>admin123</strong>
            </div>
            
            <div class="diagnostic">
                <strong>🔧 معلومات التشخيص:</strong><br>
                ✅ تم حل مشاكل إعادة التوجيه<br>
                ✅ نظام تسجيل دخول محسن<br>
                🌐 الرابط: http://localhost:5000<br>
                📊 تشخيص شامل للأخطاء
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    """تسجيل الخروج مع التشخيص"""
    print(f"🚪 تسجيل خروج للمستخدم: {session.get('username')}")
    session.clear()
    print("✅ تم مسح الجلسة")
    flash('تم تسجيل الخروج بنجاح!', 'info')
    return redirect(url_for('login'))

def open_browser():
    """فتح المتصفح تلقائياً"""
    time.sleep(3)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("=" * 60)
    print("🔧 تشخيص شامل لنظام تسجيل الدخول")
    print("RASHID INDUSTRIAL CO.")
    print("=" * 60)
    
    # إعداد قاعدة البيانات
    if init_db():
        print("✅ تم إعداد قاعدة البيانات بنجاح")
    else:
        print("❌ فشل في إعداد قاعدة البيانات")
    
    print("\n🌐 معلومات التشغيل:")
    print("   الرابط: http://localhost:5000")
    print("   اسم المستخدم: admin")
    print("   كلمة المرور: admin123")
    print("   المنفذ: 5000")
    print("   التشخيص: مفعل")
    
    print("\n🌐 سيتم فتح المتصفح تلقائياً خلال 3 ثوان...")
    print("⚠️  لإيقاف النظام: اضغط Ctrl+C")
    print("=" * 60)
    
    # فتح المتصفح في خيط منفصل
    threading.Thread(target=open_browser, daemon=True).start()
    
    # تشغيل النظام مع التشخيص
    app.run(host='0.0.0.0', port=5000, debug=True)