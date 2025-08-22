import sqlite3
import os

def add_missing_columns():
    print("🔧 إضافة الأعمدة المفقودة...")
    
    # التحقق من قاعدة البيانات المستخدمة
    db_file = 'management_system.db'
    
    if not os.path.exists(db_file):
        print(f"❌ قاعدة البيانات {db_file} غير موجودة!")
        return
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    try:
        # فحص هيكل جدول الخزينة
        cursor.execute("PRAGMA table_info(treasury)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"📊 أعمدة جدول الخزينة الحالية: {column_names}")
        
        # إضافة عمود balance إذا لم يكن موجوداً
        if 'balance' not in column_names:
            print("⚠️ عمود 'balance' غير موجود، سيتم إضافته...")
            cursor.execute('ALTER TABLE treasury ADD COLUMN balance REAL DEFAULT 0')
            print("✅ تم إضافة عمود 'balance'")
            
            # حساب وتحديث الرصيد لكل سجل
            cursor.execute('SELECT id, amount, type FROM treasury ORDER BY created_at')
            records = cursor.fetchall()
            
            running_balance = 0
            for record in records:
                record_id, amount, record_type = record
                if record_type == 'إيداع':
                    running_balance += amount
                elif record_type == 'سحب':
                    running_balance -= amount
                
                cursor.execute('UPDATE treasury SET balance = ? WHERE id = ?', (running_balance, record_id))
            
            print("✅ تم تحديث أرصدة جميع السجلات")
        else:
            print("✅ عمود 'balance' موجود بالفعل")
        
        # التأكد من وجود عمود created_at
        if 'created_at' not in column_names:
            print("⚠️ عمود 'created_at' غير موجود، سيتم إضافته...")
            cursor.execute('ALTER TABLE treasury ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            print("✅ تم إضافة عمود 'created_at'")
        else:
            print("✅ عمود 'created_at' موجود بالفعل")
        
        # التأكد من وجود عمود updated_at
        if 'updated_at' not in column_names:
            print("⚠️ عمود 'updated_at' غير موجود، سيتم إضافته...")
            cursor.execute('ALTER TABLE treasury ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            print("✅ تم إضافة عمود 'updated_at'")
        else:
            print("✅ عمود 'updated_at' موجود بالفعل")
        
        conn.commit()
        
        # اختبار الاستعلامات
        print("\n🧪 اختبار الاستعلامات...")
        
        try:
            # اختبار استعلام الرصيد
            result = cursor.execute('SELECT COALESCE(balance, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
            print(f"✅ الرصيد الحالي: {result[0] if result else 0}")
            
            # اختبار استعلام الإيداعات
            result = cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "إيداع"').fetchone()
            print(f"✅ إجمالي الإيداعات: {result[0]}")
            
            # اختبار استعلام السحوبات
            result = cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "سحب"').fetchone()
            print(f"✅ إجمالي السحوبات: {result[0]}")
            
        except Exception as e:
            print(f"❌ خطأ في الاستعلام: {e}")
        
        # عرض الهيكل النهائي
        cursor.execute("PRAGMA table_info(treasury)")
        final_columns = cursor.fetchall()
        print(f"\n📊 الهيكل النهائي لجدول الخزينة ({len(final_columns)} عمود):")
        for col in final_columns:
            print(f"  - {col[1]} ({col[2]})")
        
    except Exception as e:
        print(f"❌ خطأ في إضافة الأعمدة: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    print("\n🎉 تم إصلاح جدول الخزينة بنجاح!")

if __name__ == "__main__":
    add_missing_columns()