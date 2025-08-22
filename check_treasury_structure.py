import sqlite3

def check_treasury_structure():
    print("🔍 فحص هيكل جدول الخزينة...")
    
    conn = sqlite3.connect('car_management.db')
    cursor = conn.cursor()
    
    try:
        # فحص هيكل جدول الخزينة
        cursor.execute("PRAGMA table_info(treasury)")
        columns = cursor.fetchall()
        
        print(f"📊 أعمدة جدول الخزينة ({len(columns)} عمود):")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # فحص البيانات الموجودة
        cursor.execute("SELECT COUNT(*) FROM treasury")
        count = cursor.fetchone()[0]
        print(f"\n📈 عدد السجلات في الخزينة: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM treasury LIMIT 3")
            sample_data = cursor.fetchall()
            print("\n📋 عينة من البيانات:")
            for row in sample_data:
                print(f"  {row}")
        
        # التحقق من وجود عمود type
        column_names = [col[1] for col in columns]
        if 'type' in column_names:
            print("\n✅ عمود 'type' موجود في الجدول")
        else:
            print("\n❌ عمود 'type' غير موجود في الجدول")
            print("🔧 سيتم إضافة العمود...")
            
            # إضافة عمود type
            cursor.execute('ALTER TABLE treasury ADD COLUMN type TEXT')
            print("✅ تم إضافة عمود 'type'")
            
            # تحديث البيانات الموجودة
            cursor.execute('UPDATE treasury SET type = "إيداع" WHERE amount > 0')
            cursor.execute('UPDATE treasury SET type = "سحب" WHERE amount < 0')
            print("✅ تم تحديث البيانات الموجودة")
            
            conn.commit()
        
    except Exception as e:
        print(f"❌ خطأ في فحص الجدول: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_treasury_structure()