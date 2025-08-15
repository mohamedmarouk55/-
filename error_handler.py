#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
معالج الأخطاء الشامل
RASHID INDUSTRIAL CO.
"""

import traceback
import functools
from flask import flash, redirect, url_for, request
import werkzeug.routing.exceptions

def safe_route_handler(func):
    """ديكوريتر لمعالجة الأخطاء في جميع الدوال"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except werkzeug.routing.exceptions.BuildError as e:
            print(f'❌ خطأ في بناء الرابط في {func.__name__}: {e}')
            flash('الصفحة المطلوبة غير متوفرة حالياً', 'error')
            return redirect(url_for('index'))
        except Exception as e:
            print(f'❌ خطأ غير متوقع في {func.__name__}: {e}')
            traceback.print_exc()
            flash('حدث خطأ غير متوقع، يرجى المحاولة مرة أخرى', 'error')
            return redirect(url_for('index'))
    
    return wrapper

def setup_error_handlers(app):
    """إعداد معالجات الأخطاء للتطبيق"""
    
    @app.errorhandler(werkzeug.routing.exceptions.BuildError)
    def handle_build_error(error):
        print(f"❌ خطأ في بناء الرابط: {error}")
        print(f"   الطلب: {request.url}")
        flash('الصفحة المطلوبة غير متوفرة حالياً', 'error')
        return redirect(url_for('index'))
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        print(f"❌ خطأ داخلي في الخادم: {error}")
        traceback.print_exc()
        return '''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>خطأ في النظام</title>
            <style>
                body { font-family: Arial; padding: 50px; background: #f8f9fa; text-align: center; }
                .error-container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .error-icon { font-size: 4rem; color: #dc3545; margin-bottom: 20px; }
                h1 { color: #dc3545; margin-bottom: 20px; }
                .error-details { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: right; }
                .btn { display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px; }
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-icon">⚠️</div>
                <h1>خطأ في النظام</h1>
                <p>حدث خطأ داخلي في الخادم. النظام يعمل على إصلاح المشكلة.</p>
                
                <div class="error-details">
                    <strong>الحلول المقترحة:</strong><br>
                    • أعد تحميل الصفحة<br>
                    • تأكد من صحة البيانات المدخلة<br>
                    • جرب العودة للصفحة الرئيسية<br>
                    • إذا استمرت المشكلة، أعد تشغيل النظام
                </div>
                
                <a href="/" class="btn">الصفحة الرئيسية</a>
                <a href="/login" class="btn">تسجيل الدخول</a>
            </div>
        </body>
        </html>
        ''', 500
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return '''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>الصفحة غير موجودة</title>
            <style>
                body { font-family: Arial; padding: 50px; background: #f8f9fa; text-align: center; }
                .error-container { max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
                .error-icon { font-size: 4rem; color: #ffc107; margin-bottom: 20px; }
                .btn { display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px; }
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-icon">🔍</div>
                <h1>الصفحة غير موجودة</h1>
                <p>الصفحة التي تبحث عنها غير موجودة أو تم نقلها.</p>
                <a href="/" class="btn">الصفحة الرئيسية</a>
                <a href="/login" class="btn">تسجيل الدخول</a>
            </div>
        </body>
        </html>
        ''', 404
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
        return redirect(url_for('index'))
    
    print("✅ تم إعداد معالجات الأخطاء بنجاح")

def log_error(error_type, error_message, function_name=None):
    """تسجيل الأخطاء مع تفاصيل إضافية"""
    timestamp = traceback.format_exc()
    print(f"❌ [{error_type}] في {function_name or 'غير محدد'}: {error_message}")
    if timestamp:
        print(f"   التفاصيل: {timestamp}")