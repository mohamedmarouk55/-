#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
فحص قاعدة البيانات ومستخدم admin
"""

import sqlite3
import hashlib

def check_database():
    """فحص قاعدة البيانات والمستخدمين"""
    
    try:
        conn = sqlite3.connect('management_system.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("🔍 فحص قاعدة البيانات...")
        print("=" * 50)
        
        # فحص وجود جدول المستخدمين
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            print("✅ جدول المستخدمين موجود")
        else:
            print("❌ جدول المستخدمين غير موجود")
            return
        
        # فحص المستخدمين الموجودين
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        print(f"\n👥 عدد المستخدمين: {len(users)}")
        print("-" * 30)
        
        for user in users:
            print(f"ID: {user['id']}")
            print(f"اسم المستخدم: {user['username']}")
            print(f"البريد: {user['email']}")
            print(f"كلمة المرور المشفرة: {user['password_hash']}")
            print(f"الدور: {user['role']}")
            print(f"نشط: {'نعم' if user['is_active'] else 'لا'}")
            print("-" * 30)
        
        # فحص كلمة مرور admin
        admin_password = 'admin123'
        expected_hash = hashlib.md5(admin_password.encode()).hexdigest()
        
        print(f"\n🔑 فحص كلمة مرور admin:")
        print(f"كلمة المرور: {admin_password}")
        print(f"التشفير المتوقع: {expected_hash}")
        
        # البحث عن مستخدم admin
        cursor.execute("SELECT * FROM users WHERE username = 'admin' OR email = 'admin@rashid.com'")
        admin_user = cursor.fetchone()
        
        if admin_user:
            print(f"التشفير الموجود: {admin_user['password_hash']}")
            if admin_user['password_hash'] == expected_hash:
                print("✅ كلمة مرور admin صحيحة")
            else:
                print("❌ كلمة مرور admin غير صحيحة")
                print("🔧 سيتم إصلاحها...")
                
                # إصلاح كلمة المرور
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", 
                             (expected_hash, admin_user['id']))
                conn.commit()
                print("✅ تم إصلاح كلمة مرور admin")
        else:
            print("❌ مستخدم admin غير موجود")
            print("🔧 سيتم إنشاؤه...")
            
            # إنشاء مستخدم admin
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, is_active)
                VALUES (?, ?, ?, ?, ?)
            ''', ('admin', 'admin@rashid.com', expected_hash, 'admin', 1))
            conn.commit()
            print("✅ تم إنشاء مستخدم admin")
        
        conn.close()
        
        print("\n" + "=" * 50)
        print("🎉 انتهى فحص قاعدة البيانات")
        print("\n🔑 بيانات تسجيل الدخول:")
        print("👤 اسم المستخدم: admin")
        print("📧 أو البريد: admin@rashid.com")
        print("🔑 كلمة المرور: admin123")
        
    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")

def create_admin_user():
    """إنشاء مستخدم admin جديد"""
    try:
        conn = sqlite3.connect('management_system.db')
        cursor = conn.cursor()
        
        # حذف المستخدم الموجود إن وجد
        cursor.execute("DELETE FROM users WHERE username = 'admin' OR email = 'admin@rashid.com'")
        
        # إنشاء مستخدم جديد
        password_hash = hashlib.md5('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@rashid.com', password_hash, 'admin', 1))
        
        conn.commit()
        conn.close()
        
        print("✅ تم إنشاء مستخدم admin جديد بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء المستخدم: {e}")

if __name__ == '__main__':
    print("🔧 أدوات فحص قاعدة البيانات")
    print("=" * 50)
    print("1. فحص قاعدة البيانات")
    print("2. إنشاء مستخدم admin جديد")
    print("3. خروج")
    
    choice = input("\nاختر رقم الخيار (1-3): ")
    
    if choice == '1':
        check_database()
    elif choice == '2':
        create_admin_user()
    elif choice == '3':
        print("👋 وداعاً!")
    else:
        print("❌ خيار غير صحيح!")
    
    input("\nاضغط Enter للخروج...")