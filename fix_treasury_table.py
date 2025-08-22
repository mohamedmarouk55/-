import sqlite3
import os

def fix_treasury_table():
    print("🔧 إصلاح جدول الخزينة...")
    
    # التحقق من وجود قاعدة البيانات
    db_files = []
    for filename in ['car_management.db', 'management_system.db']:
        if os.path.exists(filename):
            db_files.append(filename)
            print(f"📁 تم العثور على قاعدة البيانات: {filename}")
    
    if not db_files:
        print("❌ لم يتم العثور على أي قاعدة بيانات!")
        return
    
    # إصلاح كل قاعدة بيانات موجودة
    for db_file in db_files:
        print(f"\n🔧 إصلاح {db_file}...")
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        try:
            # فحص هيكل جدول الخزينة
            cursor.execute("PRAGMA table_info(treasury)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            print(f"📊 أعمدة جدول الخزينة الحالية: {column_names}")
            
            if 'type' not in column_names:
                print("⚠️ عمود 'type' غير موجود، سيتم إضافته...")
                
                # إضافة عمود type
                cursor.execute('ALTER TABLE treasury ADD COLUMN type TEXT')
                print("✅ تم إضافة عمود 'type'")
                
                # تحديث البيانات الموجودة
                cursor.execute('UPDATE treasury SET type = "إيداع" WHERE amount > 0')
                cursor.execute('UPDATE treasury SET type = "سحب" WHERE amount < 0')
                print("✅ تم تحديث البيانات الموجودة")
                
                conn.commit()
            else:
                print("✅ عمود 'type' موجود بالفعل")
            
            # اختبار الاستعلامات
            print("\n🧪 اختبار الاستعلامات...")
            
            try:
                result = cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "إيداع"').fetchone()
                print(f"✅ إجمالي الإيداعات: {result[0]}")
                
                result = cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "سحب"').fetchone()
                print(f"✅ إجمالي السحوبات: {result[0]}")
                
            except Exception as e:
                print(f"❌ خطأ في الاستعلام: {e}")
            
            # إضافة بيانات افتراضية إذا كان الجدول فارغاً
            cursor.execute('SELECT COUNT(*) FROM treasury')
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("📝 إضافة بيانات افتراضية...")
                from datetime import datetime
                today = datetime.now().strftime('%Y-%m-%d')
                
                cursor.execute('''
                    INSERT INTO treasury (type, amount, description, reference_number, date, balance)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ('إيداع', 50000.0, 'رصيد افتراضي لبدء النظام', 'INIT-001', today, 50000.0))
                
                conn.commit()
                print("✅ تم إضافة رصيد افتراضي: 50,000 ريال")
            
        except Exception as e:
            print(f"❌ خطأ في إصلاح {db_file}: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    print("\n🎉 تم إصلاح جميع قواعد البيانات!")

if __name__ == "__main__":
    fix_treasury_table()