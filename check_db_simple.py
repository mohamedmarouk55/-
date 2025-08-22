import sqlite3

try:
    conn = sqlite3.connect('car_management.db')
    cursor = conn.cursor()
    
    # عرض الجداول
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("الجداول الموجودة:", [t[0] for t in tables])
    
    # التحقق من جدول المطور
    if any('developer_info' in t for t in tables):
        cursor.execute("SELECT * FROM developer_info")
        dev_data = cursor.fetchall()
        print("بيانات المطور:", dev_data)
    
    conn.close()
    print("✅ تم الفحص بنجاح")
    
except Exception as e:
    print(f"❌ خطأ: {e}")