import sqlite3

def test_treasury_queries():
    print("🧪 اختبار استعلامات الخزينة...")
    
    conn = sqlite3.connect('car_management.db')
    
    try:
        # اختبار الاستعلامات
        print("\n1. اختبار استعلام الإيداعات:")
        try:
            result = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "إيداع"').fetchone()
            print(f"   النتيجة: {result[0]}")
        except Exception as e:
            print(f"   خطأ: {e}")
        
        print("\n2. اختبار استعلام السحوبات:")
        try:
            result = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "سحب"').fetchone()
            print(f"   النتيجة: {result[0]}")
        except Exception as e:
            print(f"   خطأ: {e}")
        
        print("\n3. عرض جميع البيانات:")
        try:
            results = conn.execute('SELECT id, type, amount, description FROM treasury').fetchall()
            for row in results:
                print(f"   ID: {row[0]}, Type: {row[1]}, Amount: {row[2]}, Desc: {row[3]}")
        except Exception as e:
            print(f"   خطأ: {e}")
        
        print("\n4. اختبار استعلام الرصيد:")
        try:
            result = conn.execute('SELECT COALESCE(balance, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
            print(f"   الرصيد: {result[0] if result else 0}")
        except Exception as e:
            print(f"   خطأ: {e}")
            
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_treasury_queries()