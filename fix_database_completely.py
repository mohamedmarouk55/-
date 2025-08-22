import sqlite3
import os
from datetime import datetime

def fix_database_completely():
    print("🔧 إصلاح قاعدة البيانات بالكامل...")
    
    # حذف قاعدة البيانات القديمة إذا كانت موجودة
    if os.path.exists('car_management.db'):
        os.remove('car_management.db')
        print("🗑️ تم حذف قاعدة البيانات القديمة")
    
    # إنشاء قاعدة بيانات جديدة
    conn = sqlite3.connect('car_management.db')
    cursor = conn.cursor()
    
    try:
        print("📊 إنشاء الجداول...")
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'admin',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الموظفين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                position TEXT,
                department TEXT,
                salary REAL,
                hire_date TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                status TEXT DEFAULT 'نشط' CHECK (status IN ('نشط', 'غير نشط', 'مفصول')),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول السيارات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                license_plate TEXT UNIQUE NOT NULL,
                color TEXT,
                fuel_type TEXT DEFAULT 'بنزين',
                status TEXT DEFAULT 'متاح' CHECK (status IN ('متاح', 'مستأجر', 'صيانة', 'غير متاح')),
                purchase_date TEXT,
                purchase_price REAL,
                current_value REAL,
                engine_number TEXT,
                chassis_number TEXT,
                responsible_employee_id INTEGER,
                insurance_expiry TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (responsible_employee_id) REFERENCES employees (id)
            )
        ''')
        
        # جدول المصروفات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_type TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                amount REAL NOT NULL,
                description TEXT,
                receipt_number TEXT,
                date TEXT NOT NULL,
                related_car_id INTEGER,
                related_employee_id INTEGER,
                approved_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (related_car_id) REFERENCES cars (id),
                FOREIGN KEY (related_employee_id) REFERENCES employees (id)
            )
        ''')
        
        # جدول الخزينة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treasury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK (type IN ('إيداع', 'سحب')),
                amount REAL NOT NULL,
                description TEXT,
                reference_number TEXT,
                date TEXT NOT NULL,
                balance REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول عهد السيارات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_custody (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                employee_number TEXT NOT NULL,
                car_id INTEGER NOT NULL,
                custody_date TEXT NOT NULL,
                expected_return TEXT,
                return_date TEXT,
                notes TEXT,
                return_notes TEXT,
                status TEXT DEFAULT 'نشط' CHECK (status IN ('نشط', 'مُسلم')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id),
                FOREIGN KEY (car_id) REFERENCES cars (id)
            )
        ''')
        
        # جدول بيانات المطور
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS developer_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_ar TEXT NOT NULL,
                name_en TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                company TEXT,
                website TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("✅ تم إنشاء جميع الجداول")
        
        # إدراج البيانات الافتراضية
        print("📝 إدراج البيانات الافتراضية...")
        
        # مستخدم افتراضي
        cursor.execute('''
            INSERT INTO users (username, password, email, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin123', 'admin@system.com', 'admin'))
        
        # موظفين افتراضيين
        employees_data = [
            ('EMP001', 'أحمد محمد علي', 'مدير عام', 'الإدارة', 8000.0, '2024-01-01', '0501234567', 'ahmed@company.com', 'الرياض', 'نشط', 'موظف متميز'),
            ('EMP002', 'فاطمة أحمد', 'محاسبة', 'المالية', 6000.0, '2024-01-15', '0507654321', 'fatima@company.com', 'جدة', 'نشط', 'خبرة في المحاسبة'),
            ('EMP003', 'محمد سالم', 'سائق', 'النقل', 4000.0, '2024-02-01', '0509876543', 'mohammed@company.com', 'الدمام', 'نشط', 'سائق محترف')
        ]
        
        for emp in employees_data:
            cursor.execute('''
                INSERT INTO employees (employee_number, name, position, department, salary, hire_date, phone, email, address, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', emp)
        
        # سيارات افتراضية
        cars_data = [
            ('تويوتا', 'كامري', 2023, 'أ ب ج 123', 'أبيض', 'بنزين', 'متاح', '2024-01-01', 85000.0, 80000.0, 'ENG123456', 'CHS789012', 1, '2025-12-31', 'سيارة جديدة'),
            ('هونداي', 'النترا', 2022, 'د هـ و 456', 'أسود', 'بنزين', 'متاح', '2024-01-15', 75000.0, 70000.0, 'ENG654321', 'CHS210987', 2, '2025-11-30', 'حالة ممتازة'),
            ('نيسان', 'التيما', 2023, 'ز ح ط 789', 'فضي', 'بنزين', 'متاح', '2024-02-01', 90000.0, 85000.0, 'ENG987654', 'CHS456789', 3, '2026-01-31', 'سيارة VIP')
        ]
        
        for car in cars_data:
            cursor.execute('''
                INSERT INTO cars (brand, model, year, license_plate, color, fuel_type, status, purchase_date, purchase_price, current_value, engine_number, chassis_number, responsible_employee_id, insurance_expiry, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', car)
        
        # رصيد افتراضي للخزينة
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO treasury (type, amount, description, reference_number, date, balance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('إيداع', 50000.0, 'رصيد افتراضي لبدء النظام', 'INIT-001', today, 50000.0))
        
        # مصروفات افتراضية
        expenses_data = [
            ('تشغيلي', 'وقود', 500.0, 'تعبئة وقود للسيارات', 'REC001', today, 1, 1, 'admin'),
            ('صيانة', 'صيانة دورية', 800.0, 'تغيير زيت وفلاتر', 'REC002', today, 2, 2, 'admin'),
            ('إداري', 'مكتبية', 200.0, 'أدوات مكتبية', 'REC003', today, None, None, 'admin')
        ]
        
        for exp in expenses_data:
            cursor.execute('''
                INSERT INTO expenses (expense_type, category, amount, description, receipt_number, date, related_car_id, related_employee_id, approved_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', exp)
        
        # بيانات المطور
        cursor.execute('''
            INSERT INTO developer_info (name_ar, name_en, email, phone, company, website)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('محمد مبروك عطية', 'Mohamed Marouk Atia', 'mohamedmarouk55@gmail.com', '+966570453337', 'Freelance Developer', 'https://github.com/mohamedmarouk'))
        
        conn.commit()
        print("✅ تم إدراج جميع البيانات الافتراضية")
        
        # عرض ملخص قاعدة البيانات
        print("\n📊 ملخص قاعدة البيانات الجديدة:")
        
        tables = ['users', 'employees', 'cars', 'expenses', 'treasury', 'car_custody', 'developer_info']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  📋 {table}: {count} سجل")
        
        # التحقق من عمود type في جدول treasury
        cursor.execute("PRAGMA table_info(treasury)")
        treasury_columns = cursor.fetchall()
        type_column_exists = any(col[1] == 'type' for col in treasury_columns)
        
        if type_column_exists:
            print("\n✅ عمود 'type' موجود في جدول treasury")
            
            # اختبار الاستعلام
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "إيداع"')
            income = cursor.fetchone()[0]
            print(f"✅ اختبار استعلام الإيداعات: {income}")
            
            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE type = "سحب"')
            expenses = cursor.fetchone()[0]
            print(f"✅ اختبار استعلام السحوبات: {expenses}")
        else:
            print("\n❌ عمود 'type' غير موجود!")
        
        print("\n🎉 تم إنشاء قاعدة البيانات بنجاح!")
        print("👤 اسم المستخدم: admin")
        print("🔑 كلمة المرور: admin123")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database_completely()