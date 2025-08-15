#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تشخيص مشكلة تسجيل الدخول
"""

import sqlite3
import hashlib
import os

def diagnose_login_issue():
    """تشخيص مشكلة تسجيل الدخول"""
    
    print("🔍 تشخيص مشكلة تسجيل الدخول")
    print("=" * 50)
    
    # فحص وجود قاعدة البيانات
    if not os.path.exists('management_system.db'):
        print("❌ قاعدة البيانات غير موجودة!")
        print("🔧 سيتم إنشاؤها...")
        create_database()
        return
    
    try:
        conn = sqlite3.connect('management_system.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # فحص جدول المستخدمين
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ جدول المستخدمين غير موجود!")
            print("🔧 سيتم إنشاؤه...")
            create_users_table(cursor)
            conn.commit()
        
        # فحص مستخدم admin
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        admin_user = cursor.fetchone()
        
        if not admin_user:
            print("❌ مستخدم admin غير موجود!")
            print("🔧 سيتم إنشاؤه...")
            create_admin_user(cursor)
            conn.commit()
        else:
            print("✅ مستخدم admin موجود")
            
            # فحص كلمة المرور
            expected_hash = hashlib.md5('admin123'.encode()).hexdigest()
            if admin_user['password_hash'] == expected_hash:
                print("✅ كلمة مرور admin صحيحة")
            else:
                print("❌ كلمة مرور admin غير صحيحة!")
                print("🔧 سيتم إصلاحها...")
                cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", 
                             (expected_hash,))
                conn.commit()
                print("✅ تم إصلاح كلمة المرور")
            
            # فحص حالة النشاط
            if admin_user['is_active']:
                print("✅ مستخدم admin نشط")
            else:
                print("❌ مستخدم admin غير نشط!")
                print("🔧 سيتم تفعيله...")
                cursor.execute("UPDATE users SET is_active = 1 WHERE username = 'admin'")
                conn.commit()
                print("✅ تم تفعيل المستخدم")
        
        # عرض معلومات المستخدم النهائية
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        final_admin = cursor.fetchone()
        
        print("\n📋 معلومات مستخدم admin:")
        print(f"   ID: {final_admin['id']}")
        print(f"   اسم المستخدم: {final_admin['username']}")
        print(f"   البريد: {final_admin['email']}")
        print(f"   الدور: {final_admin['role']}")
        print(f"   نشط: {'نعم' if final_admin['is_active'] else 'لا'}")
        
        conn.close()
        
        print("\n" + "=" * 50)
        print("✅ تم الانتهاء من التشخيص والإصلاح")
        print("\n🔑 بيانات تسجيل الدخول:")
        print("👤 اسم المستخدم: admin")
        print("📧 أو البريد: admin@rashid.com")
        print("🔑 كلمة المرور: admin123")
        
    except Exception as e:
        print(f"❌ خطأ في التشخيص: {e}")

def create_database():
    """إنشاء قاعدة البيانات"""
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        create_users_table(cursor)
        create_admin_user(cursor)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إنشاء قاعدة البيانات")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")

def create_users_table(cursor):
    """إنشاء جدول المستخدمين"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

def create_admin_user(cursor):
    """إنشاء مستخدم admin"""
    password_hash = hashlib.md5('admin123'.encode()).hexdigest()
    cursor.execute('''
        INSERT OR REPLACE INTO users (username, email, password_hash, role, is_active)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))

def test_login():
    """اختبار تسجيل الدخول"""
    print("\n🧪 اختبار تسجيل الدخول...")
    
    try:
        conn = sqlite3.connect('management_system.db')
        conn.row_factory = sqlite3.Row
        
        username = 'admin'
        password = 'admin123'
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        user = conn.execute(
            'SELECT * FROM users WHERE (username = ? OR email = ?) AND password_hash = ? AND is_active = 1',
            (username, username, password_hash)
        ).fetchone()
        
        if user:
            print("✅ اختبار تسجيل الدخول نجح!")
            print(f"   مرحباً {user['username']}")
        else:
            print("❌ اختبار تسجيل الدخول فشل!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ خطأ في اختبار تسجيل الدخول: {e}")

if __name__ == '__main__':
    diagnose_login_issue()
    test_login()
    
    print("\n" + "=" * 50)
    print("🚀 يمكنك الآن تشغيل النظام باستخدام:")
    print("   • تشغيل_مع_إصلاح.bat")
    print("   • RUN.bat")
    
    input("\nاضغط Enter للخروج...")