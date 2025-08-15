#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار تسجيل الدخول المباشر
"""

from flask import Flask, request, session, redirect, url_for, render_template_string, flash
import os

app = Flask(__name__)
app.secret_key = 'test_secret_key_12345'

# HTML بسيط لتسجيل الدخول
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>اختبار تسجيل الدخول</title>
    <style>
        body { font-family: Arial; padding: 50px; background: #f0f0f0; }
        .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .error { color: red; margin: 10px 0; }
        .success { color: green; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🧪 اختبار تسجيل الدخول</h2>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="{{ 'error' if category == 'error' else 'success' }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <input type="text" name="username" placeholder="اسم المستخدم" required>
            <input type="password" name="password" placeholder="كلمة المرور" required>
            <button type="submit">تسجيل الدخول</button>
        </form>
        
        <p><strong>البيانات الصحيحة:</strong></p>
        <p>👤 اسم المستخدم: admin</p>
        <p>🔑 كلمة المرور: admin123</p>
    </div>
</body>
</html>
'''

SUCCESS_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>نجح تسجيل الدخول</title>
    <style>
        body { font-family: Arial; padding: 50px; background: #e8f5e8; text-align: center; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
        .success { color: #2e7d32; font-size: 24px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 نجح تسجيل الدخول!</h1>
        <div class="success">تم تسجيل الدخول بنجاح</div>
        <p>مرحباً {{ session.username }}!</p>
        <p>دورك: {{ session.role }}</p>
        <p>معرف المستخدم: {{ session.user_id }}</p>
        
        <hr>
        <p><strong>✅ اختبار تسجيل الدخول نجح!</strong></p>
        <p>يمكنك الآن استخدام النظام الأساسي</p>
        
        <a href="/logout" style="color: #dc3545;">تسجيل الخروج</a>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def test_login():
    if 'user_id' in session:
        return render_template_string(SUCCESS_HTML)
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        print(f"🔍 اختبار تسجيل الدخول:")
        print(f"   اسم المستخدم: '{username}'")
        print(f"   كلمة المرور: '{password}'")
        
        if not username or not password:
            flash('يرجى إدخال اسم المستخدم وكلمة المرور!', 'error')
            return render_template_string(LOGIN_HTML)
        
        # اختبار البيانات
        if (username == 'admin' or username == 'admin@rashid.com') and password == 'admin123':
            print("✅ البيانات صحيحة!")
            
            session['user_id'] = 1
            session['username'] = 'admin'
            session['role'] = 'admin'
            
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('test_login'))
        else:
            print("❌ البيانات غير صحيحة")
            flash('اسم المستخدم أو كلمة المرور غير صحيحة!', 'error')
    
    return render_template_string(LOGIN_HTML)

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج', 'success')
    return redirect(url_for('test_login'))

if __name__ == '__main__':
    print("🧪 تشغيل اختبار تسجيل الدخول...")
    print("🌐 افتح المتصفح واذهب إلى: http://localhost:5001")
    print("🔑 استخدم البيانات: admin / admin123")
    print("⚠️  لإيقاف الاختبار: اضغط Ctrl+C")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5001)