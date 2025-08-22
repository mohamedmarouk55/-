import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('car_management.db')

# عرض الجداول
tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("الجداول الموجودة:", tables)

# التحقق من وجود جدول بيانات المطور
if 'developer_info' in tables:
    print("\n✅ جدول بيانات المطور موجود")
    developer_data = conn.execute("SELECT * FROM developer_info").fetchall()
    if developer_data:
        print("بيانات المطور:", developer_data[0])
    else:
        print("⚠️ لا توجد بيانات في جدول المطور")
else:
    print("❌ جدول بيانات المطور غير موجود")

# التحقق من الإعدادات
settings = conn.execute("SELECT key, value FROM settings WHERE key LIKE 'developer_%'").fetchall()
if settings:
    print("\nإعدادات المطور:")
    for key, value in settings:
        print(f"  {key}: {value}")
else:
    print("\n⚠️ لا توجد إعدادات للمطور")

conn.close()
print("\n✅ تم الانتهاء من الفحص")