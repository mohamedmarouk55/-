import sqlite3

def update_database():
    print("🔧 تحديث هيكل قاعدة البيانات...")
    
    conn = sqlite3.connect('car_management.db')
    cursor = conn.cursor()
    
    try:
        # إضافة الحقول الجديدة لجدول السيارات
        try:
            cursor.execute('ALTER TABLE cars ADD COLUMN responsible_employee_id INTEGER')
            print("✅ تم إضافة حقل responsible_employee_id لجدول السيارات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل responsible_employee_id موجود بالفعل في جدول السيارات")
            else:
                print(f"⚠️ خطأ في إضافة حقل responsible_employee_id: {e}")
        
        try:
            cursor.execute('ALTER TABLE cars ADD COLUMN insurance_expiry TEXT')
            print("✅ تم إضافة حقل insurance_expiry لجدول السيارات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل insurance_expiry موجود بالفعل في جدول السيارات")
            else:
                print(f"⚠️ خطأ في إضافة حقل insurance_expiry: {e}")
        
        try:
            cursor.execute('ALTER TABLE cars ADD COLUMN current_value REAL')
            print("✅ تم إضافة حقل current_value لجدول السيارات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل current_value موجود بالفعل في جدول السيارات")
            else:
                print(f"⚠️ خطأ في إضافة حقل current_value: {e}")
        
        try:
            cursor.execute('ALTER TABLE cars ADD COLUMN engine_number TEXT')
            print("✅ تم إضافة حقل engine_number لجدول السيارات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل engine_number موجود بالفعل في جدول السيارات")
            else:
                print(f"⚠️ خطأ في إضافة حقل engine_number: {e}")
        
        try:
            cursor.execute('ALTER TABLE cars ADD COLUMN chassis_number TEXT')
            print("✅ تم إضافة حقل chassis_number لجدول السيارات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل chassis_number موجود بالفعل في جدول السيارات")
            else:
                print(f"⚠️ خطأ في إضافة حقل chassis_number: {e}")
        
        # إضافة الحقول الجديدة لجدول المصروفات
        try:
            cursor.execute('ALTER TABLE expenses ADD COLUMN expense_type TEXT')
            print("✅ تم إضافة حقل expense_type لجدول المصروفات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل expense_type موجود بالفعل في جدول المصروفات")
            else:
                print(f"⚠️ خطأ في إضافة حقل expense_type: {e}")
        
        try:
            cursor.execute('ALTER TABLE expenses ADD COLUMN related_car_id INTEGER')
            print("✅ تم إضافة حقل related_car_id لجدول المصروفات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل related_car_id موجود بالفعل في جدول المصروفات")
            else:
                print(f"⚠️ خطأ في إضافة حقل related_car_id: {e}")
        
        try:
            cursor.execute('ALTER TABLE expenses ADD COLUMN related_employee_id INTEGER')
            print("✅ تم إضافة حقل related_employee_id لجدول المصروفات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل related_employee_id موجود بالفعل في جدول المصروفات")
            else:
                print(f"⚠️ خطأ في إضافة حقل related_employee_id: {e}")
        
        try:
            cursor.execute('ALTER TABLE expenses ADD COLUMN approved_by TEXT')
            print("✅ تم إضافة حقل approved_by لجدول المصروفات")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ حقل approved_by موجود بالفعل في جدول المصروفات")
            else:
                print(f"⚠️ خطأ في إضافة حقل approved_by: {e}")
        
        # تحديث البيانات الموجودة
        cursor.execute('UPDATE expenses SET expense_type = "عام" WHERE expense_type IS NULL')
        cursor.execute('UPDATE expenses SET approved_by = "admin" WHERE approved_by IS NULL')
        
        conn.commit()
        print("✅ تم تحديث هيكل قاعدة البيانات بنجاح!")
        
        # عرض معلومات الجداول المحدثة
        cursor.execute("PRAGMA table_info(cars)")
        cars_columns = cursor.fetchall()
        print(f"\n📊 أعمدة جدول السيارات ({len(cars_columns)} عمود):")
        for col in cars_columns:
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute("PRAGMA table_info(expenses)")
        expenses_columns = cursor.fetchall()
        print(f"\n📊 أعمدة جدول المصروفات ({len(expenses_columns)} عمود):")
        for col in expenses_columns:
            print(f"  - {col[1]} ({col[2]})")
        
    except Exception as e:
        print(f"❌ خطأ في تحديث قاعدة البيانات: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_database()